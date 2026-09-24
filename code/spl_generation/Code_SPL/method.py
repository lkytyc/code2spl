import os
import ast
from pathlib import Path
from llm_config import chat_completion_with_retry, create_client, get_openai_config

from language_support import extract_source_members, iter_source_files

# 固定 LLM 环境
api_key, api_base, model_name = get_openai_config()
client = create_client()


def load_spl_agent_prompt():
    """从prompt文件夹加载method_spl文件中的SPL智能体定义"""
    current_dir = Path(__file__).parent
    prompt_file = current_dir / "prompt" / "method_spl"
    print(f"尝试加载SPL提示词从: {prompt_file}")

    if not prompt_file.exists():
        # 尝试其他可能的路径
        prompt_file = current_dir.parent / "prompt" / "method_spl"
        print(f"尝试备用路径: {prompt_file}")

    with open(prompt_file, 'r', encoding='utf-8') as f:
        return f.read().strip()


def llm_query(spl_agent_prompt: str, template: str, method_code: str) -> str:
    """使用SPL智能体提示词进行转换"""
    user_prompt = f"""
请作为SPL智能体执行转换任务：

输入模板结构：
{template}

需要转换的Python方法代码：
{method_code}

请按照SPL语法将上述Python方法转换为模板格式。
"""

    return chat_completion_with_retry(
        client,
        model=model_name,
        messages=[
            {"role": "system", "content": spl_agent_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0,
        max_tokens=20000
    )


def extract_methods_from_python_file(file_path):
    return extract_source_members(file_path)
    """从Python文件中提取类和方法"""
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
                    # 跳过魔术方法
                    if not method_name.startswith('__') or method_name == '__init__':
                        # 提取方法源代码
                        method_code = ast.get_source_segment(content, item)
                        classes[class_name].append({
                            'name': method_name,
                            'code': method_code
                        })

        elif isinstance(node, ast.FunctionDef):
            method_name = node.name
            # 跳过魔术方法
            if not method_name.startswith('__'):
                # 提取方法源代码
                method_code = ast.get_source_segment(content, node)
                global_methods.append({
                    'name': method_name,
                    'code': method_code
                })

    return classes, global_methods


def process_python_files():
    """处理所有Python文件"""
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

    # 加载模板和SPL智能体提示词
    template_file = template_dir / "Method.txt"
    print(f"模板文件路径: {template_file}")

    if not template_file.exists():
        print(f"错误: 模板文件不存在: {template_file}")
        return

    with open(template_file, 'r', encoding='utf-8') as f:
        template_content = f.read().strip()

    spl_agent_prompt = load_spl_agent_prompt()

    # 创建结果目录
    result_dir.mkdir(exist_ok=True)

    # 处理每个Python文件
    python_files = iter_source_files(code_dir)
    print(f"找到 {len(python_files)} 个Python文件")

    for python_file in python_files:
        print(f"处理文件: {python_file.name}")

        # 提取类和方法
        classes, global_methods = extract_methods_from_python_file(python_file)

        # 为每个Python文件创建目录
        file_result_dir = result_dir / python_file.stem
        file_result_dir.mkdir(exist_ok=True)

        # 处理类中的方法
        for class_name, methods in classes.items():
            print(f"  处理类: {class_name}")

            # 为每个类创建目录
            class_result_dir = file_result_dir / class_name
            class_result_dir.mkdir(exist_ok=True)

            # 处理每个方法
            for method in methods:
                print(f"    转换方法: {method['name']}")

                try:
                    # 使用SPL智能体进行转换
                    converted_code = llm_query(
                        spl_agent_prompt,
                        template_content,
                        method['code']
                    )

                    # 保存转换结果
                    output_file = class_result_dir / f"{method['name']}.spl"
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(converted_code)

                    print(f"      已保存: {output_file}")

                except Exception as e:
                    print(f"      转换方法 {method['name']} 时出错: {e}")

        # 处理全局方法（不属于任何类）
        if global_methods:
            print(f"  处理全局方法:")

            for method in global_methods:
                print(f"    转换全局方法: {method['name']}")

                try:
                    # 使用SPL智能体进行转换
                    converted_code = llm_query(
                        spl_agent_prompt,
                        template_content,
                        method['code']
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
