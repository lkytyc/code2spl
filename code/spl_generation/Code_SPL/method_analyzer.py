import os
import ast
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
from llm_config import chat_completion_with_retry, create_client, get_openai_config

from language_support import (
    analyze_code_structure,
    detect_language,
    extract_source_members,
    iter_source_files,
)

# 固定 LLM 环境
api_key, api_base, model_name = get_openai_config()
client = create_client()


def load_spl_agent_prompt():
    """从prompt文件夹加载method_spl_agent文件中的SPL智能体定义"""
    current_dir = Path(__file__).parent
    prompt_file = current_dir / "prompt" / "method_spl_agent.txt"
    print(f"尝试加载SPL提示词从: {prompt_file}")

    if not prompt_file.exists():
        # 尝试其他可能的路径
        prompt_file = current_dir.parent / "prompt" / "method_spl_agent.txt"
        print(f"尝试备用路径: {prompt_file}")

    with open(prompt_file, 'r', encoding='utf-8') as f:
        return f.read().strip()


def load_analyzer_prompt(prompt_name: str):
    """加载分析器提示词"""
    current_dir = Path(__file__).parent
    prompt_file = current_dir / "prompt" / prompt_name
    print(f"加载提示词从: {prompt_file}")

    if not prompt_file.exists():
        prompt_file = current_dir.parent / "prompt" / prompt_name
        print(f"尝试备用路径: {prompt_file}")

    with open(prompt_file, 'r', encoding='utf-8') as f:
        return f.read().strip()


class LLMAnalyzer:
    """LLM分析器"""

    def __init__(self):
        self.client = client
        self.model_name = model_name
        self.prompts = self._load_all_prompts()

    def _load_all_prompts(self) -> Dict[str, str]:
        """加载所有提示词"""
        prompts = {}
        prompt_files = {
            'control_flow': 'control_flow_analyzer.txt',
            'function': 'function_analyzer.txt',
            'data_flow': 'data_flow_analyzer.txt',
            'class': 'class_analyzer.txt',
            'function_call': 'function_call_analyzer.txt',
            'method_converter': 'method_spl_agent.txt'
        }

        for key, filename in prompt_files.items():
            try:
                prompts[key] = load_analyzer_prompt(filename)
            except Exception as e:
                print(f"加载提示词 {filename} 失败: {e}")
                prompts[key] = ""

        return prompts

    def analyze_control_flow(self, code: str, context: str = "") -> str:
        """分析控制流"""
        prompt_template = self.prompts['control_flow']
        prompt = prompt_template.replace("_CONTROL_CODE", code).replace("_CONTEXT_INFO", context)
        return self._call_llm(prompt)

    def analyze_function(self, code: str) -> str:
        """分析函数"""
        prompt_template = self.prompts['function']
        prompt = prompt_template.replace("_FUNCTION_CODE", code)
        return self._call_llm(prompt)

    def analyze_data_flow(self, code: str) -> str:
        """分析数据流"""
        prompt_template = self.prompts['data_flow']
        prompt = prompt_template.replace("_ASSIGNMENT_CODE", code)
        return self._call_llm(prompt)

    def analyze_class(self, code: str) -> str:
        """分析类"""
        prompt_template = self.prompts['class']
        prompt = prompt_template.replace("_CLASS_CODE", code)
        return self._call_llm(prompt)

    def analyze_function_call(self, code: str) -> str:
        """分析函数调用"""
        prompt_template = self.prompts['function_call']

        # Extract the called function name from the code snippet so the LLM
        # can emit <SPL> cross-reference tags. Post-processing will remove
        # <SPL> tags that reference functions without their own SPL entry.
        called_name = ""
        m = re.search(r'(?:self\.|cls\.)?([A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*)\s*\(', code)
        if m:
            called_name = m.group(1)
        prompt = prompt_template.replace("_CALL_CODE", code)
        prompt = prompt.replace("_CALLED_FUNCTION_NAME_IF_SPL", called_name)
        return self._call_llm(prompt)

    def convert_to_template(self, template: str, code: str, sub_analyses: list) -> str:
        """
        Convert to template format:
        1) Call LLM to output JSON only
        2) Parse JSON
        3) Deterministically render JSON into SPL
        """
        prompt_template = self.prompts['method_converter']

        structured_sub_analyses = []
        for analysis in sub_analyses:
            structured_sub_analyses.append({
                'type': analysis.get('type', ''),
                'code_snippet': analysis.get('code', ''),
                'analysis_result': analysis.get('analysis', ''),
            })

        sub_analyses_str = json.dumps(structured_sub_analyses, ensure_ascii=False, indent=2)

        prompt = prompt_template.replace("_INPUT_TEMPLATE", template)
        prompt = prompt.replace("_INPUT_CODE", code)
        prompt = prompt.replace("_SUB_ANALYSIS_RESULTS", sub_analyses_str)

        llm_text = self._call_llm(prompt)

        # Parse JSON payload (tolerant extraction)
        try:
            payload = self._extract_json_payload(llm_text)
            json_obj = json.loads(payload)
        except Exception as e:
            # Return raw output to help debugging without breaking the pipeline
            return (
                f"# JSON_PARSE_ERROR: {str(e)}\n"
                f"# RAW_LLM_OUTPUT:\n{llm_text}"
            )

        # Render to SPL deterministically
        try:
            return self._json_to_spl(template, json_obj)
        except Exception as e:
            return (
                f"# SPL_RENDER_ERROR: {str(e)}\n"
                f"# JSON:\n{json.dumps(json_obj, ensure_ascii=False, indent=2)}"
            )

    def _extract_json_payload(self, text: str) -> str:
        """
        Extract a JSON object/array from LLM output.
        Primary target is a JSON object, but array is accepted for tolerance.
        """
        if text is None:
            raise ValueError("Empty LLM output")

        s = str(text).strip()
        if not s:
            raise ValueError("Empty LLM output")

        # Prefer JSON object
        first_obj = s.find("{")
        last_obj = s.rfind("}")
        if first_obj != -1 and last_obj != -1 and last_obj > first_obj:
            return s[first_obj:last_obj + 1].strip()

        # Fallback to JSON array
        first_arr = s.find("[")
        last_arr = s.rfind("]")
        if first_arr != -1 and last_arr != -1 and last_arr > first_arr:
            return s[first_arr:last_arr + 1].strip()

        raise ValueError("No JSON object/array found in LLM output")

    def _sanitize_desc(self, s) -> str:
        """
        Descriptions are placed inside double quotes in SPL.
        Replace internal double quotes to avoid breaking SPL syntax.
        """
        if s is None:
            return ""
        return str(s).replace('"', "'").strip()

    def _render_steps_block(self, steps: list, indent: str) -> list:
        """
        Render steps into multiple lines of:
        [COMMAND ... RESULT ...]
        """
        lines = []
        if not steps:
            return lines

        for step in steps:
            if not isinstance(step, dict):
                continue

            cmd = str(step.get("command", "")).strip()
            res = str(step.get("result", "")).strip()

            if not cmd:
                continue
            if not res:
                res = "result"

            lines.append(f"{indent}[COMMAND {cmd} RESULT {res}]")
        return lines

    def _json_to_spl(self, template: str, obj: dict) -> str:
        """
        Deterministically render JSON schema into SPL.

        Required (recommended) keys:
        - worker_name
        - brief_description (one-sentence summary generated from code)
        - main_flow

        Optional keys (can be missing):
        - inputs, outputs, alternative_flows, exception_flows
        """
        if not isinstance(obj, dict):
            raise ValueError("JSON root must be an object/dict")

        worker_name = str(obj.get("worker_name") or "MethodName").strip()

        # brief_description must be generated summary; fallback only if missing/empty
        brief_raw = obj.get("brief_description")
        brief = str(brief_raw or "").strip()
        if not brief:
            brief = "Here is a brief method description"

        inputs = obj.get("inputs") or []
        outputs = obj.get("outputs") or []
        main_flow = obj.get("main_flow") or []
        alternative_flows = obj.get("alternative_flows") or []
        exception_flows = obj.get("exception_flows") or []

        out_lines = []

        # Header
        out_lines.append(f'[DEFINE_WORKER: "{self._sanitize_desc(brief)}" {worker_name}]')

        # INPUTS
        out_lines.append("    [INPUTS]")
        if isinstance(inputs, list):
            for p in inputs:
                if not isinstance(p, dict):
                    continue
                name = str(p.get("name") or "").strip()
                if not name:
                    continue
                typ = str(p.get("type") or "data_type").strip()
                desc = self._sanitize_desc(p.get("desc") or "Parameter description")
                out_lines.append(f'        <REF> {name} </REF>: {typ} "{desc}"')
        out_lines.append("    [END_INPUTS]")
        out_lines.append("")

        # OUTPUTS
        out_lines.append("    [OUTPUTS]")
        if isinstance(outputs, list):
            for r in outputs:
                if not isinstance(r, dict):
                    continue
                name = str(r.get("name") or "").strip()
                if not name:
                    continue
                typ = str(r.get("type") or "data_type").strip()
                desc = self._sanitize_desc(r.get("desc") or "Return value description")
                out_lines.append(f'        <REF> {name} </REF>: {typ} "{desc}"')
        out_lines.append("    [END_OUTPUTS]")
        out_lines.append("")

        # MAIN_FLOW
        out_lines.append("    [MAIN_FLOW]")
        out_lines.append("        [SEQUENTIAL_BLOCK]")
        if isinstance(main_flow, list):
            out_lines.extend(self._render_steps_block(main_flow, indent="            "))
        out_lines.append("        [END_SEQUENTIAL_BLOCK]")
        out_lines.append("    [END_MAIN_FLOW]")

        # ALTERNATIVE_FLOW (optional; omit entirely if missing/empty)
        if isinstance(alternative_flows, list):
            for af in alternative_flows:
                if not isinstance(af, dict):
                    continue
                cond = str(af.get("condition") or "").strip()
                steps = af.get("steps") or []
                if not cond or not isinstance(steps, list) or len(steps) == 0:
                    # If it does not exist meaningfully, skip output
                    continue

                out_lines.append("")
                out_lines.append(f"    [ALTERNATIVE_FLOW: {cond}]")
                out_lines.append("        [SEQUENTIAL_BLOCK]")
                out_lines.extend(self._render_steps_block(steps, indent="            "))
                out_lines.append("        [END_SEQUENTIAL_BLOCK]")
                out_lines.append("    [END_ALTERNATIVE_FLOW]")

        # EXCEPTION_FLOW (optional; omit entirely if missing/empty)
        if isinstance(exception_flows, list):
            for ef in exception_flows:
                if not isinstance(ef, dict):
                    continue
                cond = str(ef.get("condition") or "").strip()
                if not cond:
                    continue

                log = self._sanitize_desc(ef.get("log") or "Exception information")
                thr = ef.get("throw") or {}
                if not isinstance(thr, dict):
                    thr = {}

                thr_name = str(thr.get("name") or "ExceptionName").strip()
                thr_desc = self._sanitize_desc(thr.get("desc") or "Exception description")

                out_lines.append("")
                out_lines.append(f"    [EXCEPTION_FLOW: {cond}]")
                out_lines.append(f'        [LOG "{log}"]')
                out_lines.append(f'        [THROW {thr_name} "{thr_desc}"]')
                out_lines.append("    [END_EXCEPTION_FLOW]")

        out_lines.append("")
        out_lines.append("[END_WORKER]")

        return "\n".join(out_lines)

    def _call_llm(self, prompt: str) -> str:
        """调用LLM"""
        try:
            return chat_completion_with_retry(
                self.client,
                model=self.model_name,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0,
                max_tokens=20000
            )
        except Exception as e:
            print(f"LLM调用错误: {e}")
            return f"分析失败: {str(e)}"


class ASTDataLoader:
    """AST数据加载器 - 从之前生成的AST结果中加载"""

    def __init__(self):
        self.current_dir = Path(__file__).parent
        self.ast_result_dir = self.current_dir / "AST_Result"
        print(f"AST结果目录: {self.ast_result_dir} - 存在: {self.ast_result_dir.exists()}")

    def load_method_ast_data(self, file_name: str, class_name: str = None, method_name: str = None) -> Dict:
        """加载方法的AST数据"""
        if class_name and method_name:
            # 类方法的AST数据路径: AST_Result/file_name/classes/class_name/method_name_ast.json
            ast_file = self.ast_result_dir / file_name / "classes" / class_name / f"{method_name}_ast.json"
        elif method_name:
            # 全局函数的AST数据路径: AST_Result/file_name/global_functions/method_name_ast.json
            ast_file = self.ast_result_dir / file_name / "global_functions" / f"{method_name}_ast.json"
        else:
            return {}

        print(f"尝试加载AST文件: {ast_file}")
        print(f"文件存在: {ast_file.exists()}")

        if ast_file.exists():
            try:
                with open(ast_file, 'r', encoding='utf-8') as f:
                    ast_data = json.load(f)
                print(f"成功加载AST数据: {method_name}, 数据键: {list(ast_data.keys())}")
                return ast_data
            except Exception as e:
                print(f"加载AST文件失败: {e}")
                return {}
        else:
            print(f"AST文件不存在: {ast_file}")
            # 列出目录内容以调试
            parent_dir = ast_file.parent
            if parent_dir.exists():
                print(f"目录内容: {list(parent_dir.iterdir())}")
            return {}


class ASTDecomposer:
    """AST分解器 - 优化版本，合并连续简单节点"""

    PREDEFINED_NODES = {
        'For', 'While', 'Assign', 'If', 'ClassDef', 'FunctionDef', 'Call', 'Return'
    }

    def __init__(self, depth_threshold: int = 3, size_threshold: int = 15):
        self.analyzer_map = {
            'For': 'control_flow',
            'While': 'control_flow',
            'If': 'control_flow',
            'Switch': 'control_flow',
            'Assign': 'data_flow',
            'FunctionDef': 'function',
            'ClassDef': 'class',
            'Call': 'function_call',
            'Block': 'data_flow'  # 新增：合并块类型
        }
        self.depth_threshold = depth_threshold
        self.size_threshold = size_threshold

        # 简单节点类型（需要合并的）
        self.simple_nodes = {'Assign'}

        # 复杂节点类型（保持独立）
        self.complex_nodes = {'For', 'While', 'If', 'FunctionDef', 'ClassDef', 'Call', 'Switch'}

    def extract_methods_from_python_file(self, file_path: Path):
        return extract_source_members(file_path)
        """从Python文件中提取类和方法 - 保持与method.py一致"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            print(f"语法错误在文件 {file_path}: {e}")
            return {}, []

        classes = {}
        global_methods = []

        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                class_name = node.name
                classes[class_name] = []

                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        method_name = item.name
                        if not method_name.startswith('__') or method_name == '__init__':
                            method_code = ast.get_source_segment(content, item)
                            classes[class_name].append({
                                'name': method_name,
                                'code': method_code
                            })

            elif isinstance(node, ast.FunctionDef):
                method_name = node.name
                if not method_name.startswith('__'):
                    method_code = ast.get_source_segment(content, node)
                    global_methods.append({
                        'name': method_name,
                        'code': method_code
                    })

        return classes, global_methods

    def decompose_from_ast_data(self, ast_data: Dict, depth: int = 0, max_depth: int = 5) -> List[Dict]:
        """从AST数据中递归分解 - 优化版本，合并简单节点"""
        if depth > max_depth:
            return []

        subcodes = []
        code = ast_data.get('code', '')
        language = ast_data.get('language') or ast_data.get('ast_analysis', {}).get('language', 'python')
        total_lines = len(code.split('\n')) if code else 0

        # 对于小函数，减少分解深度
        if total_lines < 20 and depth > 1:
            print(f"  小函数({total_lines}行)，深度{depth}停止分解")
            return []

        # 优先尝试直接从代码解析AST
        if code and depth == 0:
            print(f"  使用优化AST解析进行分解")
            direct_subcodes = self.decompose_from_code_with_merging(code, depth, language)
            if direct_subcodes:
                return direct_subcodes

        # 原有的分解逻辑
        ast_analysis = ast_data.get('ast_analysis', {})
        body_analysis = ast_analysis.get('body_analysis', {})

        if body_analysis:
            print(f"  使用body_analysis进行分解 (深度{depth})")
            subcodes = self._decompose_from_body_analysis_with_merging(ast_data, depth, max_depth)

        # 应用阈值过滤和递归分解
        filtered_subcodes = []
        for subcode in subcodes:
            code_snippet = subcode.get('code', '')
            line_count = len(code_snippet.split('\n')) if code_snippet else 0
            node_type = subcode.get('type', '')

            # 过滤条件：代码行数太少
            if line_count < 2 and depth > 0 and node_type != 'Block':
                print(f"    跳过细碎代码: {node_type} (仅{line_count}行)")
                continue

            # 只有复杂节点或足够大的代码块才递归分解
            should_recurse = (
                    line_count > self.size_threshold and
                    depth < self.depth_threshold and
                    (node_type in self.complex_nodes or line_count > 10)
            )

            if should_recurse:
                print(f"    代码块合适({line_count}行)，进行递归分解: {node_type}")

                sub_ast_data = {
                    'code': code_snippet,
                    'language': language,
                    'ast_analysis': {
                        'language': language,
                        'body_analysis': self._analyze_code_structure(code_snippet, language)
                    }
                }

                child_subcodes = self.decompose_from_ast_data(sub_ast_data, depth + 1, max_depth)
                if child_subcodes:
                    subcode['children'] = child_subcodes
                    print(f"      递归分解得到 {len(child_subcodes)} 个子节点")

            filtered_subcodes.append(subcode)

        print(f"  优化分解得到 {len(filtered_subcodes)} 个节点")
        return filtered_subcodes

    def decompose_from_code_with_merging(self, code: str, depth: int = 0, language: str = 'python') -> List[Dict]:
        if language != 'python':
            analysis = analyze_code_structure(code, language)
            return self._build_subcodes_from_body_analysis(analysis, depth)
        """从代码解析AST并分解 - 合并连续简单节点"""
        try:
            tree = ast.parse(code)
            subcodes = []

            # 获取函数体（如果是函数定义）
            body_nodes = []
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                    body_nodes = node.body
                    break
            else:
                # 如果不是函数或类，使用整个模块体
                body_nodes = tree.body

            # 合并连续简单节点
            current_block = []
            current_block_type = None

            for node in body_nodes:
                node_type = type(node).__name__

                if node_type in self.simple_nodes:
                    # 简单节点，添加到当前块
                    if not current_block:
                        current_block_type = 'Block'
                    current_block.append(node)
                else:
                    # 复杂节点，先处理当前块（如果有）
                    if current_block:
                        block_code = self._extract_nodes_code(current_block, code)
                        if block_code:
                            subcodes.append({
                                'type': 'Block',
                                'analyzer_type': 'data_flow',
                                'code': block_code,
                                'depth': depth,
                                'lineno': getattr(current_block[0], 'lineno', 0),
                                'node_count': len(current_block)
                            })
                        current_block = []

                    # 处理复杂节点
                    if node_type in self.complex_nodes:
                        subcode = ast.get_source_segment(code, node)
                        if subcode:
                            line_count = len(subcode.split('\n'))
                            if line_count >= 3:  # 至少3行才提取
                                subcodes.append({
                                    'type': node_type,
                                    'analyzer_type': self.analyzer_map.get(node_type, ''),
                                    'code': subcode,
                                    'depth': depth,
                                    'lineno': getattr(node, 'lineno', 0)
                                })

            # 处理最后的块（如果有）
            if current_block:
                block_code = self._extract_nodes_code(current_block, code)
                if block_code:
                    subcodes.append({
                        'type': 'Block',
                        'analyzer_type': 'data_flow',
                        'code': block_code,
                        'depth': depth,
                        'lineno': getattr(current_block[0], 'lineno', 0),
                        'node_count': len(current_block)
                    })

            print(
                f"  合并分解得到 {len(subcodes)} 个节点 (包含 {sum(1 for s in subcodes if s['type'] == 'Block')} 个合并块)")
            return subcodes

        except Exception as e:
            print(f"  AST解析错误: {e}")
            return []

    def _extract_nodes_code(self, nodes: List[ast.AST], full_code: str) -> str:
        """从节点列表中提取合并的代码"""
        if not nodes:
            return ""

        # 获取起始和结束行号
        start_lineno = min(getattr(node, 'lineno', float('inf')) for node in nodes)
        end_lineno = max(self._get_node_end_lineno(node, full_code) for node in nodes)

        if start_lineno == float('inf') or end_lineno == 0:
            # 回退到逐个提取
            code_parts = []
            for node in nodes:
                subcode = ast.get_source_segment(full_code, node)
                if subcode:
                    code_parts.append(subcode)
            return '\n'.join(code_parts)

        # 从行号提取代码
        lines = full_code.split('\n')
        if start_lineno <= len(lines) and end_lineno <= len(lines):
            return '\n'.join(lines[start_lineno - 1:end_lineno])

        return ""

    def _get_node_end_lineno(self, node: ast.AST, full_code: str) -> int:
        """获取节点的结束行号"""
        if hasattr(node, 'end_lineno') and node.end_lineno:
            return node.end_lineno

        # 如果没有end_lineno，估算结束行号
        start_lineno = getattr(node, 'lineno', 0)
        if not start_lineno:
            return 0

        # 简单估算：假设每个节点至少占1行
        node_code = ast.get_source_segment(full_code, node)
        if node_code:
            return start_lineno + len(node_code.split('\n')) - 1
        return start_lineno

    def _build_subcodes_from_body_analysis(self, body_analysis: Dict[str, Any], depth: int) -> List[Dict]:
        subcodes = []
        all_nodes = []

        for control in body_analysis.get('control_structures', []):
            control_type = control.get('type', 'If').capitalize()
            all_nodes.append({
                'type': control_type,
                'code': control.get('code', ''),
                'lineno': control.get('lineno', 0),
                'category': 'complex'
            })

        for loop in body_analysis.get('loops', []):
            loop_type = loop.get('type', 'For').capitalize()
            all_nodes.append({
                'type': loop_type,
                'code': loop.get('code', ''),
                'lineno': loop.get('lineno', 0),
                'category': 'complex'
            })

        for switch_case in body_analysis.get('switch_cases', []):
            all_nodes.append({
                'type': 'Switch',
                'code': switch_case.get('code', ''),
                'lineno': switch_case.get('lineno', 0),
                'category': 'complex'
            })

        for assignment in body_analysis.get('assignments', []):
            all_nodes.append({
                'type': 'Assign',
                'code': assignment.get('code', ''),
                'lineno': assignment.get('lineno', 0),
                'category': 'simple'
            })

        for call in body_analysis.get('function_calls', []):
            all_nodes.append({
                'type': 'Call',
                'code': call.get('code', ''),
                'lineno': call.get('lineno', 0),
                'category': 'simple'
            })

        for return_stmt in body_analysis.get('returns', []):
            all_nodes.append({
                'type': 'Return',
                'code': return_stmt.get('code', ''),
                'lineno': return_stmt.get('lineno', 0),
                'category': 'simple'
            })

        all_nodes.sort(key=lambda x: x['lineno'])

        current_block = []
        for node in all_nodes:
            if node['category'] == 'simple':
                current_block.append(node)
                continue

            if current_block:
                block_code = '\n'.join(n['code'] for n in current_block if n['code'])
                if block_code:
                    subcodes.append({
                        'type': 'Block',
                        'analyzer_type': 'data_flow',
                        'code': block_code,
                        'depth': depth,
                        'lineno': current_block[0]['lineno'],
                        'node_count': len(current_block)
                    })
                current_block = []

            if node['code']:
                subcodes.append({
                    'type': node['type'],
                    'analyzer_type': self.analyzer_map.get(node['type'], ''),
                    'code': node['code'],
                    'depth': depth,
                    'lineno': node['lineno']
                })

        if current_block:
            block_code = '\n'.join(n['code'] for n in current_block if n['code'])
            if block_code:
                subcodes.append({
                    'type': 'Block',
                    'analyzer_type': 'data_flow',
                    'code': block_code,
                    'depth': depth,
                    'lineno': current_block[0]['lineno'],
                    'node_count': len(current_block)
                })

        return subcodes

    def _decompose_from_body_analysis_with_merging(self, ast_data: Dict, depth: int, max_depth: int) -> List[Dict]:
        ast_analysis = ast_data.get('ast_analysis', {})
        body_analysis = ast_analysis.get('body_analysis', {})
        return self._build_subcodes_from_body_analysis(body_analysis, depth)
        """从body_analysis中分解AST - 合并连续简单节点"""
        subcodes = []
        ast_analysis = ast_data.get('ast_analysis', {})
        body_analysis = ast_analysis.get('body_analysis', {})
        code = ast_data.get('code', '')

        print(f"  body_analysis键: {list(body_analysis.keys())}")

        # 收集所有节点并按行号排序
        all_nodes = []

        # 处理控制结构
        for control in body_analysis.get('control_structures', []):
            control_type = control.get('type', 'If').capitalize()
            all_nodes.append({
                'type': control_type,
                'code': control.get('code', ''),
                'lineno': control.get('lineno', 0),
                'category': 'complex'
            })

        # 处理循环
        for loop in body_analysis.get('loops', []):
            loop_type = loop.get('type', 'For').capitalize()
            all_nodes.append({
                'type': loop_type,
                'code': loop.get('code', ''),
                'lineno': loop.get('lineno', 0),
                'category': 'complex'
            })

        # 处理赋值
        for assignment in body_analysis.get('assignments', []):
            all_nodes.append({
                'type': 'Assign',
                'code': assignment.get('code', ''),
                'lineno': assignment.get('lineno', 0),
                'category': 'simple'
            })

        # 处理函数调用
        for call in body_analysis.get('function_calls', []):
            all_nodes.append({
                'type': 'Call',
                'code': call.get('code', ''),
                'lineno': call.get('lineno', 0),
                'category': 'simple'
            })

        # 处理返回语句
        for return_stmt in body_analysis.get('returns', []):
            all_nodes.append({
                'type': 'Return',
                'code': return_stmt.get('code', ''),
                'lineno': return_stmt.get('lineno', 0),
                'category': 'simple'
            })

        # 按行号排序
        all_nodes.sort(key=lambda x: x['lineno'])

        # 合并连续简单节点
        current_block = []
        for node in all_nodes:
            if node['category'] == 'simple':
                current_block.append(node)
            else:
                # 复杂节点，先处理当前块
                if current_block:
                    block_code = '\n'.join(n['code'] for n in current_block if n['code'])
                    if block_code:
                        subcodes.append({
                            'type': 'Block',
                            'analyzer_type': 'data_flow',
                            'code': block_code,
                            'depth': depth,
                            'lineno': current_block[0]['lineno'],
                            'node_count': len(current_block)
                        })
                    current_block = []

                # 添加复杂节点
                if node['code']:
                    subcodes.append({
                        'type': node['type'],
                        'analyzer_type': self.analyzer_map.get(node['type'], ''),
                        'code': node['code'],
                        'depth': depth,
                        'lineno': node['lineno']
                    })

        # 处理最后的块
        if current_block:
            block_code = '\n'.join(n['code'] for n in current_block if n['code'])
            if block_code:
                subcodes.append({
                    'type': 'Block',
                    'analyzer_type': 'data_flow',
                    'code': block_code,
                    'depth': depth,
                    'lineno': current_block[0]['lineno'],
                    'node_count': len(current_block)
                })

        return subcodes

    def _analyze_code_structure(self, code: str, language: str = 'python') -> Dict[str, Any]:
        return analyze_code_structure(code, language)
        """分析代码结构 - 用于递归分解"""
        try:
            tree = ast.parse(code)
            analysis = {
                'control_structures': [],
                'loops': [],
                'assignments': [],
                'function_calls': [],
                'returns': []
            }

            for node in ast.walk(tree):
                if isinstance(node, ast.If):
                    analysis['control_structures'].append({
                        'type': 'if',
                        'code': ast.get_source_segment(code, node),
                        'lineno': getattr(node, 'lineno', 0)
                    })
                elif isinstance(node, ast.For):
                    analysis['loops'].append({
                        'type': 'for',
                        'code': ast.get_source_segment(code, node),
                        'lineno': getattr(node, 'lineno', 0)
                    })
                elif isinstance(node, ast.While):
                    analysis['loops'].append({
                        'type': 'while',
                        'code': ast.get_source_segment(code, node),
                        'lineno': getattr(node, 'lineno', 0)
                    })
                elif isinstance(node, ast.Assign):
                    analysis['assignments'].append({
                        'type': 'assignment',
                        'code': ast.get_source_segment(code, node),
                        'lineno': getattr(node, 'lineno', 0)
                    })
                elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
                    analysis['function_calls'].append({
                        'type': 'function_call',
                        'code': ast.get_source_segment(code, node),
                        'lineno': getattr(node, 'lineno', 0)
                    })
                elif isinstance(node, ast.Return):
                    analysis['returns'].append({
                        'type': 'return',
                        'code': ast.get_source_segment(code, node),
                        'lineno': getattr(node, 'lineno', 0)
                    })

            return analysis
        except Exception as e:
            print(f"    代码结构分析失败: {e}")
            return {
                'control_structures': [],
                'loops': [],
                'assignments': [],
                'function_calls': [],
                'returns': []
            }


class RecursiveAnalyzer:
    """递归分析器"""

    def __init__(self, llm_analyzer: LLMAnalyzer):
        self.llm = llm_analyzer
        self.analysis_functions = {
            'control_flow': self.llm.analyze_control_flow,
            'function': self.llm.analyze_function,
            'data_flow': self.llm.analyze_data_flow,
            'class': self.llm.analyze_class,
            'function_call': self.llm.analyze_function_call
        }

    def analyze_subcodes(self, subcodes: List[Dict]) -> List[Dict]:
        """分析子代码列表 - 增强版本，保留完整代码结构"""
        analyzed_results = []

        for subcode in subcodes:
            analyzer_type = subcode.get('analyzer_type')
            code = subcode['code']

            if analyzer_type and analyzer_type in self.analysis_functions:
                print(f"    [深度{subcode['depth']}] 分析 {subcode['type']} 节点...")

                try:
                    analysis_func = self.analysis_functions[analyzer_type]
                    analysis_result = analysis_func(code)

                    analyzed_subcode = subcode.copy()
                    analyzed_subcode['analysis'] = analysis_result
                    # 保留原始代码
                    analyzed_subcode['original_code'] = code

                    # 递归分析子节点
                    if 'children' in subcode:
                        analyzed_subcode['children'] = self.analyze_subcodes(subcode['children'])

                    analyzed_results.append(analyzed_subcode)

                except Exception as e:
                    print(f"      分析失败: {e}")
                    analyzed_subcode = subcode.copy()
                    analyzed_subcode['analysis'] = f"分析错误: {str(e)}"
                    analyzed_subcode['original_code'] = code
                    analyzed_results.append(analyzed_subcode)
            else:
                analyzed_subcode = subcode.copy()
                analyzed_subcode['analysis'] = "无对应分析器"
                analyzed_subcode['original_code'] = code
                analyzed_results.append(analyzed_subcode)

        return analyzed_results


class CodeAnalysisPipeline:
    """代码分析管道 - 完整工作流程"""

    def __init__(self):
        self.llm_analyzer = LLMAnalyzer()
        self.ast_loader = ASTDataLoader()
        self.ast_decomposer = ASTDecomposer()
        self.recursive_analyzer = RecursiveAnalyzer(self.llm_analyzer)

    def process_single_method(self, method_code: str, method_name: str, template: str,
                              file_name: str, class_name: str = None) -> str:
        """处理单个方法并返回SPL模板"""
        print(f"处理方法: {method_name}")

        try:
            # 1. 从AST结果中加载AST数据
            print("  加载AST数据...")
            ast_data = self.ast_loader.load_method_ast_data(file_name, class_name, method_name)

            if not ast_data:
                print(f"  未找到AST数据，使用基础转换")
                # 如果没有AST数据，直接使用基础转换
                return self.llm_analyzer.convert_to_template(template, method_code, [])

            print(f"  成功加载AST数据，包含 {len(ast_data)} 个键")

            # 2. AST分解 → 识别8种特殊节点类型
            print("  分解AST...")
            code_lines = len(method_code.split('\n'))
            if code_lines <= 10:
                depth_threshold = 2  # 短方法使用较小阈值
            elif code_lines <= 30:
                depth_threshold = 3  # 中等方法
            else:
                depth_threshold = 4  # 长方法

            self.ast_decomposer.depth_threshold = depth_threshold
            self.ast_decomposer.size_threshold = 8  # 每块8行左右

            subcodes = self.ast_decomposer.decompose_from_ast_data(ast_data)
            print(f"  找到 {len(subcodes)} 个子代码节点 (阈值: 深度{depth_threshold}, 大小8行)")

            # 3. 递归分析 → 对每个子代码调用对应的分析智能体
            analyzed_subcodes = []

            if subcodes:
                print("  递归分析子代码...")
                analyzed_subcodes = self.recursive_analyzer.analyze_subcodes(subcodes)

                # 4. 结果收集 → 收集所有子代码的分析结果
                sub_analyses = self._flatten_analyses(analyzed_subcodes)
                print(f"  收集到 {len(sub_analyses)} 个子分析结果")

                # 5. 模板转换 → 使用子分析结果辅助主转换智能体
                print("  进行模板转换...")
                converted_template = self.llm_analyzer.convert_to_template(
                    template, method_code, sub_analyses
                )
            else:
                # 如果没有找到子代码，使用基础转换
                print("  未找到可分析的子代码，使用基础转换")
                converted_template = self.llm_analyzer.convert_to_template(
                    template, method_code, []
                )

            return converted_template

        except Exception as e:
            print(f"  处理方法 {method_name} 时出错: {e}")
            import traceback
            traceback.print_exc()
            # 出错时返回错误信息
            return f"# 转换错误: {str(e)}\n# 原始代码:\n{method_code}"

    def _flatten_analyses(self, analyzed_subcodes: List[Dict]) -> List[Dict]:
        """扁平化分析结果 - 增强版本，包含代码和分析"""
        flat_analyses = []

        def flatten(analyses):
            for analysis in analyses:
                flat_analysis = {
                    'type': analysis['type'],
                    'analyzer_type': analysis.get('analyzer_type'),
                    'depth': analysis['depth'],
                    'code': analysis.get('original_code', analysis.get('code', '')),  # 确保包含代码
                    'analysis': analysis.get('analysis', ''),
                    'lineno': analysis.get('lineno', 0)
                }
                flat_analyses.append(flat_analysis)

                if 'children' in analysis:
                    flatten(analysis['children'])

        flatten(analyzed_subcodes)
        return flat_analyses

def process_python_files():
    """处理所有Python文件 - 按照method.py的格式"""
    # 获取当前脚本所在目录
    current_dir = Path(__file__).parent
    print(f"当前目录: {current_dir}")

    # 路径配置 - 使用相对路径
    code_dir = current_dir / "Code"
    template_dir = current_dir / "template"
    result_dir = current_dir / "Result"
    prompt_dir = current_dir / "prompt"

    # 检查目录是否存在
    print(f"Code目录: {code_dir} - 存在: {code_dir.exists()}")
    print(f"Template目录: {template_dir} - 存在: {template_dir.exists()}")
    print(f"Prompt目录: {prompt_dir} - 存在: {prompt_dir.exists()}")

    # 列出template目录下的文件
    if template_dir.exists():
        print(f"Template目录内容: {list(template_dir.iterdir())}")

    # 加载模板
    template_file = template_dir / "Method.txt"
    print(f"模板文件路径: {template_file}")

    if not template_file.exists():
        print(f"错误: 模板文件不存在: {template_file}")
        return

    with open(template_file, 'r', encoding='utf-8') as f:
        template_content = f.read().strip()

    # 创建结果目录
    result_dir.mkdir(exist_ok=True)

    # 初始化分析管道
    pipeline = CodeAnalysisPipeline()

    # 处理每个Python文件 - 添加调试信息
    python_files = iter_source_files(code_dir)
    print(f"找到 {len(python_files)} 个Python文件")

    # 列出Code目录中的所有文件用于调试
    if code_dir.exists():
        all_files = list(code_dir.iterdir())
        print(f"Code目录中的所有文件: {[f.name for f in all_files]}")

    for python_file in python_files:
        print(f"处理文件: {python_file.name}")

        # 提取类和方法
        classes, global_methods = pipeline.ast_decomposer.extract_methods_from_python_file(python_file)
        print(f"  找到 {len(classes)} 个类, {len(global_methods)} 个全局函数")

        # 为每个Python文件创建目录
        file_result_dir = result_dir / python_file.stem
        file_result_dir.mkdir(exist_ok=True)

        # 处理类中的方法
        for class_name, methods in classes.items():
            print(f"  处理类: {class_name}")
            print(f"    类中包含 {len(methods)} 个方法: {[m['name'] for m in methods]}")

            # 为每个类创建目录
            class_result_dir = file_result_dir / class_name
            class_result_dir.mkdir(exist_ok=True)

            # 处理每个方法
            for method in methods:
                print(f"    转换方法: {method['name']}")

                try:
                    # 使用分析管道进行转换
                    converted_code = pipeline.process_single_method(
                        method['code'],
                        method['name'],
                        template_content,
                        python_file.stem,
                        class_name
                    )

                    # 保存转换结果 - 按照method.py的格式
                    output_file = class_result_dir / f"{method['name']}.spl"
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(converted_code)

                    print(f"      已保存: {output_file}")

                except Exception as e:
                    print(f"      转换方法 {method['name']} 时出错: {e}")

        # 处理全局方法（不属于任何类）
        if global_methods:
            print(f"  处理全局方法:")
            print(f"    找到 {len(global_methods)} 个全局方法: {[m['name'] for m in global_methods]}")

            for method in global_methods:
                print(f"    转换全局方法: {method['name']}")

                try:
                    # 使用分析管道进行转换
                    converted_code = pipeline.process_single_method(
                        method['code'],
                        method['name'],
                        template_content,
                        python_file.stem
                    )

                    # 保存转换结果到文件目录下（不在类目录中）
                    output_file = file_result_dir / f"{method['name']}.spl"
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(converted_code)

                    print(f"      已保存: {output_file}")

                except Exception as e:
                    print(f"      转换全局方法 {method['name']} 时出错: {e}")

        print(f"完成处理: {python_file.name}\n")


if __name__ == "__main__":
    process_python_files()
    print("所有文件处理完成！")
