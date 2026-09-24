# diagram.py - 多轮LLM生成Mermaid + 自动转PNG
import json
import re
import subprocess
import shutil
import base64
import requests
from pathlib import Path
from llm_config import chat_completion_with_retry, create_client, get_openai_config

_api_key, _api_base, _model_name = get_openai_config()
client = create_client()


class MermaidGenerator:
    """三阶段Mermaid生成器"""

    def __init__(self):
        prompt_file = Path(__file__).parent / "prompt" / "diagram_planner.txt"
        if not prompt_file.exists():
            raise FileNotFoundError("缺少 prompt/diagram_planner.txt")

        content = prompt_file.read_text(encoding="utf-8")
        self.prompts = self._parse_prompts(content)

        # 调试：打印找到的提示词
        print(f"找到的提示词: {list(self.prompts.keys())}")

        # 检查mermaid-cli是否安装
        self._check_mmdc()

    def _check_mmdc(self):
        """检查mmdc是否可用"""
        if shutil.which("mmdc"):
            print("✓ 检测到 mermaid-cli (mmdc)")
            self.mmdc_available = True
        else:
            print("⚠ 未检测到 mermaid-cli")
            print("  将使用在线API生成图片...")
            self.mmdc_available = False

    def _parse_prompts(self, content: str) -> dict:
        """解析提示词文件"""
        prompts = {}
        pattern = r'PROMPT_(\w+)\s*=\s*"""(.*?)"""'
        matches = re.findall(pattern, content, re.DOTALL)
        for name, text in matches:
            prompts[name.lower()] = text.strip()
        return prompts

    def _call_llm(self, prompt: str) -> str:
        """调用LLM"""
        print(f"🤖 调用LLM中...")
        return chat_completion_with_retry(
            client,
            model=_model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=4096
        )

    def _clean_json_response(self, text: str) -> str:
        """清理JSON响应，提取纯JSON"""
        # 尝试提取JSON部分
        json_pattern = r'```json\s*(.*?)\s*```'
        match = re.search(json_pattern, text, re.DOTALL)
        if match:
            return match.group(1).strip()

        # 尝试提取{...}格式的JSON
        brace_pattern = r'(\{.*\})'
        match = re.search(brace_pattern, text, re.DOTALL)
        if match:
            return match.group(1).strip()

        return text.strip()

    def generate(self, spl_content: str) -> str:
        """三阶段生成Mermaid代码"""
        print("\n" + "=" * 60)
        print("第一阶段: 分析SPL结构（含并行识别）")
        print("=" * 60)

        # 第一阶段：结构分析（包含并行识别）
        structure_prompt = self.prompts.get('structure_analysis', '')
        if not structure_prompt:
            raise KeyError("找不到 structure_analysis 提示词")

        structure_prompt = structure_prompt.replace('{content}', spl_content)
        structure_json_str = self._call_llm(structure_prompt)

        # 清理JSON响应
        clean_json = self._clean_json_response(structure_json_str)

        try:
            # 验证JSON格式
            structure_data = json.loads(clean_json)

            # 统计并行节点
            parallel_count = 0
            for cmd in structure_data.get('commands', []):
                if cmd.get('can_parallel', False):
                    parallel_count += 1

            parallel_groups = structure_data.get('flow_structure', {}).get('parallel_groups', [])

            print(f"✓ 成功解析SPL结构")
            print(f"  - 共 {len(structure_data.get('commands', []))} 个命令")
            print(f"  - {parallel_count} 个可并行执行的命令")
            print(f"  - {len(parallel_groups)} 个并行执行组")

        except json.JSONDecodeError as e:
            print(f"❌ JSON解析失败: {e}")
            print(f"原始响应: {structure_json_str[:200]}...")
            # 尝试直接使用原始响应进行下一阶段
            structure_data = {"raw_content": structure_json_str}

        print("\n" + "=" * 60)
        print("第二阶段: 生成Mermaid代码（含并行编排）")
        print("=" * 60)

        # 第二阶段：生成Mermaid代码
        if isinstance(structure_data, dict) and 'commands' in structure_data:
            # 如果是有效的结构数据，转换为JSON字符串
            mermaid_prompt_content = json.dumps(structure_data, ensure_ascii=False, indent=2)
        else:
            # 否则使用原始内容
            mermaid_prompt_content = str(structure_data)

        mermaid_prompt = self.prompts.get('mermaid_generation', '')
        if not mermaid_prompt:
            raise KeyError("找不到 mermaid_generation 提示词")

        mermaid_prompt = mermaid_prompt.replace(
            '{structure_json}',
            mermaid_prompt_content
        )

        initial_code = self._call_llm(mermaid_prompt)
        mermaid_code = self._extract_mermaid(initial_code)

        # 检查并行语法使用情况
        if '&' in mermaid_code:
            print(f"✓ 生成了包含并行语法的Mermaid代码，共 {len(mermaid_code.splitlines())} 行")
        else:
            print(f"✓ 生成了Mermaid代码，共 {len(mermaid_code.splitlines())} 行")

        print("\n" + "=" * 60)
        print("第三阶段: 优化布局和样式（简洁黑白风格）")
        print("=" * 60)

        # 第三阶段：优化
        # 检查是否有优化提示词，如果没有就直接使用第二阶段的结果
        if 'mermaid_optimization' in self.prompts:
            optimization_prompt = self.prompts['mermaid_optimization'].replace(
                '{mermaid_code}',
                mermaid_code
            )

            optimized_code = self._call_llm(optimization_prompt)
            final_code = self._extract_mermaid(optimized_code)

            # 检查样式优化
            if 'style' in final_code and 'fill:' not in final_code:
                print(f"✓ 优化完成，应用了简洁黑白风格")
            else:
                print(f"✓ 优化完成")
            print(f"  - 最终代码 {len(final_code.splitlines())} 行")
        else:
            print("⚠ 未找到优化提示词，直接使用第二阶段结果")
            final_code = mermaid_code

        return final_code

    def _extract_mermaid(self, text: str) -> str:
        """提取Mermaid代码"""
        # 移除markdown代码块标记
        text = re.sub(r'```mermaid\n', '', text)
        text = re.sub(r'```\n?', '', text)

        # 如果以flowchart开头,保留完整内容
        if text.strip().startswith('flowchart'):
            return text.strip()

        # 尝试提取flowchart TD或LR部分
        match = re.search(r'(flowchart\s+(?:TD|LR|BT|RL).*)', text, re.DOTALL)
        if match:
            return match.group(1).strip()

        return text.strip()

    def to_image_local(self, mermaid_code: str, output_path: Path, format: str = "png"):
        """使用本地mmdc将Mermaid代码转为图片"""
        try:
            # 保存.mmd文件
            mmd_path = output_path.with_suffix('.mmd')
            mmd_path.write_text(mermaid_code, encoding='utf-8')
            print(f"📝 Mermaid代码: {mmd_path}")

            # 转换为图片
            img_path = output_path.with_suffix(f'.{format}')

            # 使用高质量参数
            cmd = [
                "mmdc",
                "-i", str(mmd_path),
                "-o", str(img_path),
                "-b", "transparent",  # 透明背景
                "-w", "2400",  # 宽度2400px (高分辨率)
                "-H", "1800",  # 高度1800px
                "--scale", "2"  # 2倍缩放 (提高清晰度)
            ]

            print(f"🎨 生成{format.upper()}图片中...")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                print(f"✅ 图片生成成功: {img_path}")
                print(f"   尺寸: 2400x1800px, 2倍缩放")
                return True
            else:
                print(f"❌ 图片生成失败: {result.stderr}")
                return False

        except Exception as e:
            print(f"❌ 本地图片生成出错: {e}")
            return False

    def to_image_online(self, mermaid_code: str, output_path: Path, format: str = "png"):
        """使用在线API将Mermaid代码转为图片"""
        print(f"🌐 使用在线API生成{format.upper()}图片...")

        try:
            # 方案1：使用 Mermaid.ink API
            try:
                # 编码Mermaid代码
                encoded_code = base64.urlsafe_b64encode(mermaid_code.encode()).decode()

                if format.lower() == "png":
                    url = f"https://mermaid.ink/img/{encoded_code}"
                elif format.lower() == "svg":
                    url = f"https://mermaid.ink/svg/{encoded_code}"
                else:
                    print(f"❌ 不支持的格式: {format}")
                    return False

                # 下载图片
                response = requests.get(url, timeout=30)
                if response.status_code == 200:
                    img_path = output_path.with_suffix(f'.{format}')
                    img_path.write_bytes(response.content)
                    print(f"✅ 图片生成成功: {img_path}")
                    print(f"   来源: Mermaid.ink API")
                    return True
                else:
                    print(f"❌ Mermaid.ink API失败: {response.status_code}")

            except Exception as e:
                print(f"⚠ Mermaid.ink失败: {e}")

            # 方案2：使用 kroki.io API
            try:
                print("🔄 尝试使用 Kroki.io API...")
                if format.lower() == "png":
                    api_url = "https://kroki.io/mermaid/png"
                elif format.lower() == "svg":
                    api_url = "https://kroki.io/mermaid/svg"
                else:
                    return False

                response = requests.post(
                    api_url,
                    data=mermaid_code.encode(),
                    headers={"Content-Type": "text/plain"},
                    timeout=30
                )

                if response.status_code == 200:
                    img_path = output_path.with_suffix(f'.{format}')
                    img_path.write_bytes(response.content)
                    print(f"✅ 图片生成成功: {img_path}")
                    print(f"   来源: Kroki.io API")
                    return True
                else:
                    print(f"❌ Kroki.io失败: {response.status_code}")

            except Exception as e:
                print(f"⚠ Kroki.io失败: {e}")

            # 方案3：使用 QuickChart API
            try:
                print("🔄 尝试使用 QuickChart API...")
                config = {
                    "type": "mermaid",
                    "chart": mermaid_code,
                    "backgroundColor": "transparent",
                    "width": 2400,
                    "height": 1800
                }

                response = requests.post(
                    "https://quickchart.io/mermaid",
                    json=config,
                    timeout=30
                )

                if response.status_code == 200:
                    img_path = output_path.with_suffix(f'.png')
                    img_path.write_bytes(response.content)
                    print(f"✅ 图片生成成功: {img_path}")
                    print(f"   来源: QuickChart API")
                    return True

            except Exception as e:
                print(f"⚠ QuickChart失败: {e}")

        except Exception as e:
            print(f"❌ 所有在线API都失败了: {e}")

        return False

    def to_image(self, mermaid_code: str, output_path: Path, format: str = "png"):
        """将Mermaid代码转为图片（自动选择方法）"""

        # 先尝试使用本地mmdc
        if self.mmdc_available:
            print(f"🖥️ 使用本地mmdc生成图片...")
            return self.to_image_local(mermaid_code, output_path, format)
        else:
            print(f"📶 mmdc不可用，尝试在线API...")
            return self.to_image_online(mermaid_code, output_path, format)


def main():
    generator = MermaidGenerator()
    result_dir = Path(__file__).parent / "Result"

    spl_files = list(result_dir.rglob("*.spl"))

    if not spl_files:
        print("❌ 未找到任何.spl文件")
        return

    print(f"\n📂 找到 {len(spl_files)} 个SPL文件")
    print(f"💡 生成策略:")
    print(f"  - 识别并行执行节点")
    print(f"  - 使用简洁黑白风格")
    print(f"  - 优先使用本地mmdc，失败时使用在线API")
    print(f"💡 输出格式: PNG图片 (高分辨率 2400x1800px) + SVG矢量图")

    success_count_png = 0
    success_count_svg = 0

    for i, spl_file in enumerate(spl_files, 1):
        print(f"\n{'=' * 60}")
        print(f"处理文件 [{i}/{len(spl_files)}]: {spl_file.name}")
        print(f"{'=' * 60}")

        try:
            # 检查缓存
            mmd_path = spl_file.with_suffix(".mmd")
            png_path = spl_file.with_name(spl_file.stem + "_diagram.png")
            svg_path = spl_file.with_name(spl_file.stem + "_diagram.svg")

            # 如果PNG和SVG都已存在，跳过
            if png_path.exists() and svg_path.exists():
                print("📁 图片文件已存在，跳过...")
                success_count_png += 1
                success_count_svg += 1
                continue

            if mmd_path.exists():
                print("💾 读取已有Mermaid代码...")
                mermaid_code = mmd_path.read_text(encoding='utf-8')
            else:
                # 读取SPL文件内容
                content = spl_file.read_text(encoding='utf-8')
                print(f"📄 读取SPL文件: {len(content)} 字符")

                # 生成Mermaid代码（三阶段）
                mermaid_code = generator.generate(content)

                # 保存Mermaid代码
                mmd_path.write_text(mermaid_code, encoding='utf-8')
                print(f"💾 保存Mermaid代码到: {mmd_path}")

            # 转换为PNG
            output_path = spl_file.with_name(spl_file.stem + "_diagram")

            # 生成PNG图片
            if not png_path.exists():
                print(f"\n📊 生成PNG图片...")
                if generator.to_image(mermaid_code, output_path, format="png"):
                    success_count_png += 1
            else:
                print(f"📊 PNG图片已存在: {png_path.name}")
                success_count_png += 1

            # 生成SVG矢量图
            if not svg_path.exists():
                print(f"\n🎨 生成SVG矢量图...")
                if generator.to_image(mermaid_code, output_path, format="svg"):
                    success_count_svg += 1
            else:
                print(f"🎨 SVG图片已存在: {svg_path.name}")
                success_count_svg += 1

        except Exception as e:
            print(f"❌ 处理失败: {e}")
            import traceback
            traceback.print_exc()

    # 总结
    print(f"\n{'=' * 60}")
    print(f"处理完成!")
    print(f"{'=' * 60}")
    print(f"✓ PNG图片生成: {success_count_png}/{len(spl_files)} 个")
    print(f"✓ SVG矢量图生成: {success_count_svg}/{len(spl_files)} 个")

    # 列出生成的文件
    print(f"\n📁 生成的文件:")
    for spl_file in spl_files:
        base_name = spl_file.stem
        mmd = spl_file.with_name(f"{base_name}.mmd")
        png = spl_file.with_name(f"{base_name}_diagram.png")
        svg = spl_file.with_name(f"{base_name}_diagram.svg")

        print(f"\n  {spl_file.name}:")
        if mmd.exists():
            print(f"    📝 {mmd.name} (Mermaid代码)")
        if png.exists():
            print(f"    🖼️  {png.name} (PNG图片)")
        if svg.exists():
            print(f"    🎨  {svg.name} (SVG矢量图)")

    # 提示信息
    print(f"\n💡 提示:")
    if not generator.mmdc_available:
        print(f"  1. 安装本地mmdc可提高生成速度: npm install -g @mermaid-js/mermaid-cli")
    print(f"  2. 或使用在线预览: https://mermaid.live")
    print(f"  3. 手动转换命令: npx -p @mermaid-js/mermaid-cli mmdc -i input.mmd -o output.png")
    print(f"  4. 注意: 所有节点使用矩形，样式为简洁黑白风格")


if __name__ == "__main__":
    main()
