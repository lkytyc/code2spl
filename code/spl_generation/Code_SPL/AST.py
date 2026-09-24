import os
import ast
from pathlib import Path
from typing import Dict, List, Any
import json

from language_support import (
    analyze_source_file,
    analyze_specific_method_ast as analyze_method_with_language,
    detect_language,
    extract_source_members,
    iter_source_files,
)


class ASTProcessor:
    """Docstring."""

    def __init__(self):
        self.analysis_results = {}

    def extract_ast_from_python_file(self, file_path: Path) -> Dict[str, Any]:
        """Docstring."""
        print(f"鍒嗘瀽鏂囦欢: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            print(f"璇硶閿欒鍦ㄦ枃浠?{file_path}: {e}")
            return {"error": str(e)}

        file_ast = {
            "file_name": file_path.name,
            "file_path": str(file_path),
            "content_length": len(content),
            "classes": {},
            "global_functions": [],
            "imports": [],
            "global_variables": [],
            "ast_structure": {}
        }

        # 鎻愬彇瀵煎叆璇彞
        file_ast["imports"] = self._extract_imports(tree)

        # 鎻愬彇鍏ㄥ眬鍙橀噺
        file_ast["global_variables"] = self._extract_global_variables(tree, content)

        # 鎻愬彇绫诲拰鍑芥暟
        file_ast["classes"] = self._extract_classes(tree, content)
        file_ast["global_functions"] = self._extract_global_functions(tree, content)

        # 鐢熸垚瀹屾暣鐨凙ST缁撴瀯
        file_ast["ast_structure"] = self._generate_ast_structure(tree)

        return file_ast

    def _extract_imports(self, tree: ast.AST) -> List[Dict]:
        """Docstring."""
        imports = []

        for node in tree.body:
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append({
                        "type": "import",
                        "module": alias.name,
                        "alias": alias.asname,
                        "lineno": node.lineno
                    })
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    imports.append({
                        "type": "from_import",
                        "module": node.module,
                        "name": alias.name,
                        "alias": alias.asname,
                        "level": node.level,
                        "lineno": node.lineno
                    })

        return imports

    def _extract_global_variables(self, tree: ast.AST, content: str) -> List[Dict]:
        """Docstring."""
        global_vars = []

        for node in tree.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        var_code = ast.get_source_segment(content, node)
                        global_vars.append({
                            "name": target.id,
                            "code": var_code,
                            "lineno": node.lineno,
                            "type": "assignment"
                        })
            elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                var_code = ast.get_source_segment(content, node)
                global_vars.append({
                    "name": node.target.id,
                    "code": var_code,
                    "lineno": node.lineno,
                    "type": "annotated_assignment"
                })

        return global_vars

    def _extract_classes(self, tree: ast.AST, content: str) -> Dict[str, Any]:
        """Docstring."""
        classes = {}

        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                class_name = node.name
                classes[class_name] = {
                    "name": class_name,
                    "lineno": node.lineno,
                    "bases": [self._get_base_name(base) for base in node.bases],
                    "methods": [],
                    "class_variables": [],
                    "decorators": [self._get_decorator_name(decorator) for decorator in node.decorator_list]
                }

                # 鎻愬彇绫讳腑鐨勬柟娉?
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        method_info = self._extract_function_info(item, content)
                        classes[class_name]["methods"].append(method_info)

                    # 鎻愬彇绫诲彉閲?
                    elif isinstance(item, ast.Assign):
                        for target in item.targets:
                            if isinstance(target, ast.Name):
                                var_code = ast.get_source_segment(content, item)
                                classes[class_name]["class_variables"].append({
                                    "name": target.id,
                                    "code": var_code,
                                    "lineno": item.lineno
                                })

        return classes

    def _extract_global_functions(self, tree: ast.AST, content: str) -> List[Dict]:
        """Docstring."""
        global_functions = []

        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                # 璺宠繃榄旀湳鏂规硶锛堥櫎浜哶_init__锛?
                if not node.name.startswith('__') or node.name == '__init__':
                    func_info = self._extract_function_info(node, content)
                    global_functions.append(func_info)

        return global_functions

    def _extract_function_info(self, func_node: ast.FunctionDef, content: str) -> Dict[str, Any]:
        """Docstring."""
        func_code = ast.get_source_segment(content, func_node)

        # 鎻愬彇鍙傛暟淇℃伅
        args_info = self._extract_arguments_info(func_node.args)

        # 鍒嗘瀽鍑芥暟浣撶粨鏋?
        body_analysis = self._analyze_function_body(func_node.body, content)

        # 鐢熸垚绠€鍖栫殑AST缁撴瀯锛岄伩鍏嶅鏉傜殑宓屽
        simplified_ast = self._generate_simplified_ast_structure(func_node)

        return {
            "name": func_node.name,
            "code": func_code,
            "lineno": func_node.lineno,
            "args": args_info,
            "decorators": [self._get_decorator_name(decorator) for decorator in func_node.decorator_list],
            "returns": self._get_annotation_name(getattr(func_node, 'returns', None)),
            "body_analysis": body_analysis,
            "ast_structure": simplified_ast  # 浣跨敤绠€鍖栫殑AST缁撴瀯
        }

    def _generate_simplified_ast_structure(self, node: ast.AST) -> Dict[str, Any]:
        """Docstring."""
        node_type = type(node).__name__
        result = {
            "type": node_type,
            "lineno": getattr(node, 'lineno', None)
        }

        # 鍙鐞嗗叧閿俊鎭紝閬垮厤娣卞害閫掑綊
        if isinstance(node, ast.FunctionDef):
            result["name"] = node.name
            result["args_count"] = len(node.args.args)
        elif isinstance(node, ast.ClassDef):
            result["name"] = node.name
            result["bases_count"] = len(node.bases)

        return result

    def _get_annotation_name(self, annotation: Any) -> str:
        """Docstring."""
        if annotation is None:
            return None
        elif isinstance(annotation, ast.Name):
            return annotation.id
        elif isinstance(annotation, ast.Attribute):
            return ast.unparse(annotation)
        elif isinstance(annotation, ast.Subscript):
            return ast.unparse(annotation)
        else:
            return str(type(annotation).__name__)

    def _extract_arguments_info(self, args: ast.arguments) -> Dict[str, Any]:
        """Docstring."""
        arguments = {
            "args": [arg.arg for arg in args.args],
            "defaults": len(args.defaults),
            "vararg": args.vararg.arg if args.vararg else None,
            "kwarg": args.kwarg.arg if args.kwarg else None,
            "kwonlyargs": [arg.arg for arg in args.kwonlyargs]
        }

        return arguments

    def _analyze_function_body(self, body: List[ast.AST], content: str) -> Dict[str, Any]:
        """Docstring."""
        analysis = {
            "statements_count": len(body),
            "control_structures": [],
            "loops": [],
            "assignments": [],
            "function_calls": [],
            "switch_cases": []  # 鏂板锛歋witch璇彞鍒嗘瀽
        }

        for node in body:
            if isinstance(node, ast.If):
                analysis["control_structures"].append({
                    "type": "if",
                    "lineno": node.lineno,
                    "code": ast.get_source_segment(content, node)
                })
            elif isinstance(node, ast.For):
                analysis["loops"].append({
                    "type": "for",
                    "lineno": node.lineno,
                    "code": ast.get_source_segment(content, node)
                })
            elif isinstance(node, ast.While):
                analysis["loops"].append({
                    "type": "while",
                    "lineno": node.lineno,
                    "code": ast.get_source_segment(content, node)
                })
            elif isinstance(node, ast.Assign):
                analysis["assignments"].append({
                    "type": "assignment",
                    "lineno": node.lineno,
                    "code": ast.get_source_segment(content, node)
                })
            elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
                analysis["function_calls"].append({
                    "type": "function_call",
                    "lineno": node.lineno,
                    "code": ast.get_source_segment(content, node)
                })
            elif isinstance(node, ast.Match):  # Python 3.10+ 鐨刴atch璇彞锛堢被浼糞witch锛?
                analysis["switch_cases"].append({
                    "type": "match",
                    "lineno": node.lineno,
                    "code": ast.get_source_segment(content, node)
                })

        return analysis

    def _generate_ast_structure(self, node: ast.AST, depth: int = 0) -> Dict[str, Any]:
        """Docstring."""
        if depth > 10:  # 闃叉鏃犻檺閫掑綊
            return {"type": "max_depth_reached"}

        if not isinstance(node, ast.AST):
            return {"type": "non_ast_node", "value": str(node)}

        node_type = type(node).__name__
        result = {
            "type": node_type,
            "lineno": getattr(node, 'lineno', None),
            "col_offset": getattr(node, 'col_offset', None)
        }

        # 澶勭悊鐗瑰畾鑺傜偣绫诲瀷鐨勯澶栦俊鎭?- 鍙彁鍙栧彲搴忓垪鍖栫殑鏁版嵁
        try:
            if isinstance(node, ast.Name):
                result["id"] = node.id
                result["ctx"] = type(node.ctx).__name__
            elif isinstance(node, ast.Call):
                result["func"] = self._generate_ast_structure(node.func, depth + 1)
                result["args"] = [self._generate_ast_structure(arg, depth + 1) for arg in node.args]
                if node.keywords:
                    result["keywords"] = [{"arg": kw.arg, "value": self._generate_ast_structure(kw.value, depth + 1)}
                                          for kw in node.keywords]
            elif isinstance(node, ast.Assign):
                result["targets"] = [self._generate_ast_structure(target, depth + 1) for target in node.targets]
                result["value"] = self._generate_ast_structure(node.value, depth + 1)
            elif isinstance(node, ast.FunctionDef):
                result["name"] = node.name
                result["args"] = self._generate_ast_structure(node.args, depth + 1)
                result["decorator_list"] = [self._generate_ast_structure(decorator, depth + 1)
                                            for decorator in node.decorator_list]
            elif isinstance(node, ast.ClassDef):
                result["name"] = node.name
                result["bases"] = [self._generate_ast_structure(base, depth + 1) for base in node.bases]
                result["decorator_list"] = [self._generate_ast_structure(decorator, depth + 1)
                                            for decorator in node.decorator_list]
            elif isinstance(node, ast.arguments):
                # 澶勭悊鍙傛暟鑺傜偣
                result["args"] = [self._generate_ast_structure(arg, depth + 1) for arg in node.args]
                result["defaults"] = [self._generate_ast_structure(default, depth + 1) for default in node.defaults]
                if node.vararg:
                    result["vararg"] = self._generate_ast_structure(node.vararg, depth + 1)
                if node.kwarg:
                    result["kwarg"] = self._generate_ast_structure(node.kwarg, depth + 1)
            elif isinstance(node, ast.arg):
                result["arg"] = node.arg
                if node.annotation:
                    result["annotation"] = self._generate_ast_structure(node.annotation, depth + 1)
            elif isinstance(node, ast.Constant):
                # 缁熶竴澶勭悊甯搁噺鑺傜偣 (Python 3.8+)
                result["value"] = node.value
                result["kind"] = getattr(node, 'kind', None)
            elif hasattr(ast, 'Str') and isinstance(node, ast.Str):  # Python 3.7鍙婁互涓嬪吋瀹?
                # 浠呭湪ast.Str瀛樺湪鏃朵娇鐢紝閬垮厤璀﹀憡
                result["value"] = node.s
                result["_note"] = "legacy_Str_node"
            elif hasattr(ast, 'Num') and isinstance(node, ast.Num):  # Python 3.7鍙婁互涓嬪吋瀹?
                # 浠呭湪ast.Num瀛樺湪鏃朵娇鐢紝閬垮厤璀﹀憡
                result["value"] = node.n
                result["_note"] = "legacy_Num_node"
            elif isinstance(node, ast.Attribute):
                result["attr"] = node.attr
                result["value"] = self._generate_ast_structure(node.value, depth + 1)
                result["ctx"] = type(node.ctx).__name__
            elif isinstance(node, ast.Subscript):
                result["value"] = self._generate_ast_structure(node.value, depth + 1)
                result["slice"] = self._generate_ast_structure(node.slice, depth + 1)
                result["ctx"] = type(node.ctx).__name__
            elif hasattr(ast, 'Index') and isinstance(node, ast.Index):  # Python 3.8鍙婁互涓嬪吋瀹?
                result["value"] = self._generate_ast_structure(node.value, depth + 1)
                result["_note"] = "legacy_Index_node"
            elif hasattr(ast, 'Match') and isinstance(node, ast.Match):  # Python 3.10+ 鐨刴atch璇彞
                result["subject"] = self._generate_ast_structure(node.subject, depth + 1)
                result["cases"] = [self._generate_ast_structure(case, depth + 1) for case in node.cases]

            # 浣跨敤ast.unparse鏉ヨ幏鍙栦唬鐮佽〃绀?(Python 3.9+)
            if hasattr(ast, 'unparse') and hasattr(node, '_fields'):
                try:
                    result["code_snippet"] = ast.unparse(node)
                except Exception:
                    # 濡傛灉unparse澶辫触锛屽拷鐣ラ敊璇?
                    pass

            # 瀵逛簬鍏朵粬鑺傜偣绫诲瀷锛屽彧鎻愬彇瀛楁鍚?
            if hasattr(node, '_fields'):
                for field in node._fields:
                    if field not in result:  # 閬垮厤瑕嗙洊宸插鐞嗙殑瀛楁
                        field_value = getattr(node, field, None)
                        if field_value is not None:
                            if isinstance(field_value, list):
                                result[field] = [self._generate_ast_structure(item, depth + 1)
                                                 for item in field_value]
                            elif isinstance(field_value, ast.AST):
                                result[field] = self._generate_ast_structure(field_value, depth + 1)
                            else:
                                # 瀵逛簬鍩烘湰绫诲瀷锛岀洿鎺ュ瓨鍌?
                                try:
                                    json.dumps(field_value)  # 娴嬭瘯鏄惁鍙簭鍒楀寲
                                    result[field] = field_value
                                except (TypeError, ValueError):
                                    result[field] = str(field_value)

        except Exception as e:
            result["error"] = f"澶勭悊鑺傜偣鏃跺嚭閿? {str(e)}"

        return result

    def _get_base_name(self, base: ast.AST) -> str:
        """Docstring."""
        if isinstance(base, ast.Name):
            return base.id
        elif isinstance(base, ast.Attribute):
            return ast.unparse(base)
        else:
            return str(type(base).__name__)

    def _get_decorator_name(self, decorator: ast.AST) -> str:
        """Docstring."""
        if isinstance(decorator, ast.Name):
            return decorator.id
        elif isinstance(decorator, ast.Attribute):
            return ast.unparse(decorator)
        elif isinstance(decorator, ast.Call):
            return self._get_decorator_name(decorator.func)
        else:
            return str(type(decorator).__name__)


def extract_methods_from_python_file(file_path):
    return extract_source_members(file_path)
    """Docstring."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    try:
        tree = ast.parse(content)
    except SyntaxError as e:
        print(f"璇硶閿欒鍦ㄦ枃浠?{file_path}: {e}")
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
                    # 璺宠繃榄旀湳鏂规硶
                    if not method_name.startswith('__') or method_name == '__init__':
                        # 鎻愬彇鏂规硶婧愪唬鐮?
                        method_code = ast.get_source_segment(content, item)
                        classes[class_name].append({
                            'name': method_name,
                            'code': method_code
                        })

        elif isinstance(node, ast.FunctionDef):
            method_name = node.name
            # 璺宠繃榄旀湳鏂规硶
            if not method_name.startswith('__'):
                # 鎻愬彇鏂规硶婧愪唬鐮?
                method_code = ast.get_source_segment(content, node)
                global_methods.append({
                    'name': method_name,
                    'code': method_code
                })

    return classes, global_methods

def safe_json_serialize(obj):
    """Docstring."""
    if isinstance(obj, (str, int, float, bool, type(None))):
        return obj
    elif isinstance(obj, (list, tuple)):
        return [safe_json_serialize(item) for item in obj]
    elif isinstance(obj, dict):
        return {str(key): safe_json_serialize(value) for key, value in obj.items()}
    else:
        return str(obj)

def process_python_files_for_ast():
    """Docstring."""
    # 鑾峰彇褰撳墠鑴氭湰鎵€鍦ㄧ洰褰?
    current_dir = Path(__file__).parent
    print(f"褰撳墠鐩綍: {current_dir}")

    # 璺緞閰嶇疆 - 浣跨敤鐩稿璺緞锛堜笌method.py淇濇寔涓€鑷达級
    code_dir = current_dir / "Code"
    result_dir = current_dir / "AST_Result"

    # 妫€鏌ョ洰褰曟槸鍚﹀瓨鍦?
    print(f"Code鐩綍: {code_dir} - 瀛樺湪: {code_dir.exists()}")

    if not code_dir.exists():
        print(f"閿欒: Code鐩綍涓嶅瓨鍦? {code_dir}")
        return

    # 鍒涘缓缁撴灉鐩綍
    result_dir.mkdir(exist_ok=True)

    # 鍒濆鍖朅ST澶勭悊鍣?
    ast_processor = ASTProcessor()
    source_files = iter_source_files(code_dir)
    print(f"Found {len(source_files)} source files")

    all_ast_results = {}
    project_summary = {
        "total_files": len(source_files),
        "files_analyzed": 0,
        "files_failed": 0,
        "total_classes": 0,
        "total_methods": 0,
        "total_functions": 0
    }

    for source_file in source_files:
        print(f"Processing source file: {source_file.name}")
        language = detect_language(source_file)

        try:
            if language == "python":
                file_ast = ast_processor.extract_ast_from_python_file(source_file)
            else:
                file_ast = analyze_source_file(source_file)

            file_result_dir = result_dir / source_file.stem
            file_result_dir.mkdir(exist_ok=True)

            ast_json_file = file_result_dir / "ast_analysis.json"
            with open(ast_json_file, 'w', encoding='utf-8') as f:
                json.dump(safe_json_serialize(file_ast), f, ensure_ascii=False, indent=2)

            print(f"  Wrote AST analysis: {ast_json_file}")

            classes, global_methods = extract_methods_from_python_file(source_file)
            project_summary["total_classes"] += len(classes)
            project_summary["total_functions"] += len(global_methods)

            for class_name, methods in classes.items():
                project_summary["total_methods"] += len(methods)
                class_dir = file_result_dir / "classes" / class_name
                class_dir.mkdir(parents=True, exist_ok=True)

                class_json_file = class_dir / "class_info.json"
                with open(class_json_file, 'w', encoding='utf-8') as f:
                    json.dump({
                        "class_name": class_name,
                        "methods_count": len(methods),
                        "methods": [method['name'] for method in methods],
                        "language": language
                    }, f, ensure_ascii=False, indent=2)

                for method in methods:
                    try:
                        method_analysis = analyze_method_with_language(
                            method['code'],
                            method['name'],
                            method.get('language', language),
                            class_name
                        )
                        method_ast_file = class_dir / f"{method['name']}_ast.json"
                        with open(method_ast_file, 'w', encoding='utf-8') as f:
                            json.dump(safe_json_serialize(method_analysis), f, ensure_ascii=False, indent=2)
                        print(f"    Wrote method AST: {method_ast_file}")
                    except Exception as e:
                        print(f"    Failed to analyze method {method['name']}: {e}")

            if global_methods:
                global_func_dir = file_result_dir / "global_functions"
                global_func_dir.mkdir(parents=True, exist_ok=True)

                for method in global_methods:
                    try:
                        method_analysis = analyze_method_with_language(
                            method['code'],
                            method['name'],
                            method.get('language', language)
                        )
                        func_ast_file = global_func_dir / f"{method['name']}_ast.json"
                        with open(func_ast_file, 'w', encoding='utf-8') as f:
                            json.dump(safe_json_serialize(method_analysis), f, ensure_ascii=False, indent=2)
                        print(f"    Wrote global function AST: {func_ast_file}")
                    except Exception as e:
                        print(f"    Failed to analyze global function {method['name']}: {e}")

            all_ast_results[source_file.name] = {
                "file_info": {
                    "name": file_ast.get("file_name", source_file.name),
                    "path": file_ast.get("file_path", str(source_file)),
                    "content_length": file_ast.get("content_length", 0),
                    "language": file_ast.get("language", language)
                },
                "summary": {
                    "imports_count": len(file_ast.get("imports", [])),
                    "classes_count": len(file_ast.get("classes", {})),
                    "global_functions_count": len(file_ast.get("global_functions", [])),
                    "global_variables_count": len(file_ast.get("global_variables", []))
                }
            }

            project_summary["files_analyzed"] += 1

        except Exception as e:
            print(f"  Failed to process source file {source_file.name}: {e}")
            import traceback
            traceback.print_exc()
            all_ast_results[source_file.name] = {"error": str(e)}
            project_summary["files_failed"] += 1

    overview_file = result_dir / "ast_analysis_overview.json"
    with open(overview_file, 'w', encoding='utf-8') as f:
        json.dump({
            "project_summary": project_summary,
            "detailed_results": all_ast_results
        }, f, ensure_ascii=False, indent=2)

    print("\nAST analysis completed")
    print(f"Overview file: {overview_file}")
    print("\nSummary:")
    print(f"  - total_files: {project_summary['total_files']}")
    print(f"  - files_analyzed: {project_summary['files_analyzed']}")
    print(f"  - files_failed: {project_summary['files_failed']}")
    print(f"  - total_classes: {project_summary['total_classes']}")
    print(f"  - total_methods: {project_summary['total_methods']}")
    print(f"  - total_functions: {project_summary['total_functions']}")
    return

    # 澶勭悊姣忎釜Python鏂囦欢
    python_files = list(code_dir.glob("*.py"))
    print(f"鎵惧埌 {len(python_files)} 涓狿ython鏂囦欢")

    all_ast_results = {}
    project_summary = {
        "total_files": len(python_files),
        "files_analyzed": 0,
        "files_failed": 0,
        "total_classes": 0,
        "total_methods": 0,
        "total_functions": 0
    }

    for python_file in python_files:
        print(f"澶勭悊鏂囦欢: {python_file.name}")

        try:
            # 鎻愬彇AST淇℃伅
            file_ast = ast_processor.extract_ast_from_python_file(python_file)

            # 涓烘瘡涓狿ython鏂囦欢鍒涘缓鐩綍 - 纭繚璺緞姝ｇ‘
            file_result_dir = result_dir / python_file.stem
            file_result_dir.mkdir(exist_ok=True)

            # 淇濆瓨璇︾粏鐨凙ST鍒嗘瀽缁撴灉
            ast_json_file = file_result_dir / "ast_analysis.json"
            with open(ast_json_file, 'w', encoding='utf-8') as f:
                json.dump(file_ast, f, ensure_ascii=False, indent=2)

            print(f"  宸蹭繚瀛楢ST鍒嗘瀽: {ast_json_file}")

            # 淇濆瓨绫诲拰鏂规硶缁撴瀯
            classes, global_methods = extract_methods_from_python_file(python_file)

            # 鏇存柊椤圭洰缁熻
            project_summary["total_classes"] += len(classes)
            project_summary["total_functions"] += len(global_methods)

            for class_name, methods in classes.items():
                project_summary["total_methods"] += len(methods)

                # 鍒涘缓绫荤洰褰?- 纭繚璺緞涓巑ethod_analyzer.py鏈熸湜鐨勪竴鑷?
                class_dir = file_result_dir / "classes" / class_name
                class_dir.mkdir(parents=True, exist_ok=True)

                # 淇濆瓨绫讳俊鎭?
                class_json_file = class_dir / "class_info.json"
                with open(class_json_file, 'w', encoding='utf-8') as f:
                    json.dump({
                        "class_name": class_name,
                        "methods_count": len(methods),
                        "methods": [method['name'] for method in methods]
                    }, f, ensure_ascii=False, indent=2)

                # 淇濆瓨姣忎釜鏂规硶鐨勮缁咥ST鍒嗘瀽 - 鍏抽敭淇敼锛氱‘淇濇枃浠跺悕鏍煎紡姝ｇ‘
                for method in methods:
                    try:
                        # 瑙ｆ瀽鏂规硶浠ｇ爜鑾峰彇AST鑺傜偣
                        method_tree = ast.parse(method['code'])
                        if len(method_tree.body) == 1 and isinstance(method_tree.body[0], ast.FunctionDef):
                            func_node = method_tree.body[0]

                            # 浣跨敤鏂规硶鍒嗘瀽鍑芥暟
                            method_analysis = analyze_specific_method_ast(method['code'], method['name'])

                            # 淇濆瓨鏂规硶AST鏂囦欢 - 浣跨敤姝ｇ‘鐨勫懡鍚嶆牸寮?
                            method_ast_file = class_dir / f"{method['name']}_ast.json"
                            with open(method_ast_file, 'w', encoding='utf-8') as f:
                                json.dump(method_analysis, f, ensure_ascii=False, indent=2)

                            print(f"    宸蹭繚瀛樻柟娉旳ST: {method_ast_file}")
                        else:
                            print(f"    璀﹀憡: 鏃犳硶瑙ｆ瀽鏂规硶 {method['name']} 鐨凙ST")
                    except Exception as e:
                        print(f"    澶勭悊鏂规硶 {method['name']} 鏃跺嚭閿? {e}")

            # 淇濆瓨鍏ㄥ眬鍑芥暟 - 鍚屾牱纭繚璺緞姝ｇ‘
            if global_methods:
                global_func_dir = file_result_dir / "global_functions"
                global_func_dir.mkdir(parents=True, exist_ok=True)

                for method in global_methods:
                    try:
                        method_analysis = analyze_specific_method_ast(method['code'], method['name'])

                        # 淇濆瓨鍏ㄥ眬鍑芥暟AST鏂囦欢 - 浣跨敤姝ｇ‘鐨勫懡鍚嶆牸寮?
                        func_ast_file = global_func_dir / f"{method['name']}_ast.json"
                        with open(func_ast_file, 'w', encoding='utf-8') as f:
                            json.dump(method_analysis, f, ensure_ascii=False, indent=2)

                        print(f"    宸蹭繚瀛樺叏灞€鍑芥暟AST: {func_ast_file}")
                    except Exception as e:
                        print(f"    澶勭悊鍏ㄥ眬鍑芥暟 {method['name']} 鏃跺嚭閿? {e}")

            # 娣诲姞鍒版€荤粨鏋?
            all_ast_results[python_file.name] = {
                "file_info": {
                    "name": file_ast["file_name"],
                    "path": file_ast["file_path"],
                    "content_length": file_ast["content_length"]
                },
                "summary": {
                    "imports_count": len(file_ast["imports"]),
                    "classes_count": len(file_ast["classes"]),
                    "global_functions_count": len(file_ast["global_functions"]),
                    "global_variables_count": len(file_ast["global_variables"])
                }
            }

            project_summary["files_analyzed"] += 1

        except Exception as e:
            print(f"  澶勭悊鏂囦欢 {python_file.name} 鏃跺嚭閿? {e}")
            import traceback
            traceback.print_exc()
            all_ast_results[python_file.name] = {"error": str(e)}
            project_summary["files_failed"] += 1

    # 淇濆瓨鎬昏鏂囦欢
    overview_file = result_dir / "ast_analysis_overview.json"
    with open(overview_file, 'w', encoding='utf-8') as f:
        json.dump({
            "project_summary": project_summary,
            "detailed_results": all_ast_results
        }, f, ensure_ascii=False, indent=2)

    print("\nAST analysis completed")
    print(f"Overview file: {overview_file}")

    # 鎵撳嵃缁熻淇℃伅
    print("\nSummary:")
    print(f"  - total_files: {project_summary['total_files']}")
    print(f"  - files_analyzed: {project_summary['files_analyzed']}")
    print(f"  - files_failed: {project_summary['files_failed']}")
    print(f"  - total_classes: {project_summary['total_classes']}")
    print(f"  - total_methods: {project_summary['total_methods']}")
    print(f"  - total_functions: {project_summary['total_functions']}")


def analyze_specific_method_ast(method_code: str, method_name: str = "unknown_method", language: str = "python", class_name: str = None) -> Dict[str, Any]:
    return analyze_method_with_language(method_code, method_name, language, class_name)
    """Docstring."""
    ast_processor = ASTProcessor()

    try:
        # 瑙ｆ瀽鏂规硶浠ｇ爜
        method_tree = ast.parse(method_code)

        if len(method_tree.body) == 1 and isinstance(method_tree.body[0], ast.FunctionDef):
            func_node = method_tree.body[0]
            func_info = ast_processor._extract_function_info(func_node, method_code)

            return {
                "method_name": method_name,
                "code": method_code,
                "ast_analysis": func_info,
                "raw_ast": ast_processor._generate_ast_structure(func_node)
            }
        else:
            return {
                "method_name": method_name,
                "error": "Not a valid single function definition",
                "code": method_code,
                "ast_structure": ast_processor._generate_ast_structure(method_tree)
            }

    except Exception as e:
        return {
            "method_name": method_name,
            "error": str(e),
            "code": method_code
        }


if __name__ == "__main__":
    process_python_files_for_ast()