import openai
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, Polygon, Arrow
import matplotlib.lines as mlines
from openai import OpenAI
import os
import re
import math
import numpy as np

# Set fonts
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['axes.unicode_minus'] = False


class CodeFlowGenerator:
    def __init__(self):
        api_key = os.environ.get("OPENAI_API_KEY")
        api_base = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is required to generate a diagram.")
        self.client = OpenAI(api_key=api_key, base_url=api_base)
        self.entities = []
        self.relationships = []
        self.graph_structure = {}

    def read_prompt(self, filename):
        """Read prompt file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print(f"Error: Cannot find file {filename}")
            return None

    def call_llm(self, prompt, user_input):
        """Call LLM API"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.3
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"API call error: {e}")
            return None

    def extract_entities(self, text):
        """Extract code entities"""
        print("=== Starting entity extraction ===")
        prompt = self.read_prompt('entity_extraction.txt')
        if not prompt:
            return None

        result = self.call_llm(prompt, text)

        if result:
            print("Entity extraction result:")
            print(result)

        # Parse entity results
        self.entities = []
        for line in result.strip().split('\n'):
            if '|' in line:
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 3 and parts[0].startswith('$N'):
                    entity = {
                        'id': parts[0],
                        'label': parts[1],
                        'type': parts[2]
                    }
                    self.entities.append(entity)

        print(f"Successfully extracted {len(self.entities)} entities")
        return self.entities

    def extract_relationships(self, text):
        """Extract code relationships"""
        print("=== Starting relationship extraction ===")
        if not self.entities:
            print("Error: Please extract entities first")
            return None

        entities_str = '\n'.join([f"{e['id']} - {e['label']} ({e['type']})" for e in self.entities])
        prompt_template = self.read_prompt('relationship_extraction.txt')
        if not prompt_template:
            return None

        prompt = prompt_template.replace('{entities}', entities_str)

        result = self.call_llm(prompt, text)

        if result:
            print("Relationship extraction result:")
            print(result)

        # Parse relationship results
        self.relationships = []
        for line in result.strip().split('\n'):
            if '|' in line:
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 3:
                    relationship = {
                        'source': parts[0],
                        'target': parts[1],
                        'type': parts[2],
                        'description': parts[3] if len(parts) > 3 else ''
                    }
                    self.relationships.append(relationship)

        print(f"Successfully extracted {len(self.relationships)} relationships")
        return self.relationships

    def generate_graph_structure(self):
        """Generate code flow chart structure"""
        print("=== Generating code flow chart structure ===")
        if not self.entities or not self.relationships:
            print("Error: Please extract entities and relationships first")
            return None

        entities_str = '\n'.join([f"{e['id']} - {e['label']} ({e['type']})" for e in self.entities])
        relationships_str = '\n'.join([f"{r['source']} -> {r['target']} ({r['type']})" for r in self.relationships])

        prompt_template = self.read_prompt('graph_structure_generation.txt')
        if not prompt_template:
            return None

        prompt = prompt_template.replace('{entities}', entities_str)
        prompt = prompt.replace('{relationships}', relationships_str)

        result = self.call_llm(prompt, "")

        if result:
            print("Code flow chart structure generation result:")
            print(result)

        # 修复解析逻辑 - 直接解析所有行
        self.graph_structure = {
            'nodes': [],
            'edges': []
        }

        lines = result.strip().split('\n')

        # 首先解析所有节点
        for line in lines:
            line = line.strip()
            if '|' in line and line.startswith('$N'):
                parts = [p.strip() for p in line.split('|')]

                # 节点格式: $N1 | trajectory_points | data | 0 | 0
                if len(parts) >= 5 and parts[0].startswith('$N'):
                    try:
                        x_pos = float(parts[3])
                        y_pos = float(parts[4])
                    except ValueError:
                        # 使用默认位置
                        x_pos = len(self.graph_structure['nodes']) % 10
                        y_pos = len(self.graph_structure['nodes']) // 10

                    node_info = {
                        'id': parts[0],
                        'label': parts[1],
                        'node_type': parts[2],
                        'x': x_pos,
                        'y': y_pos
                    }
                    self.graph_structure['nodes'].append(node_info)

        # 然后解析所有边
        for line in lines:
            line = line.strip()
            if '|' in line and line.startswith('$N'):
                parts = [p.strip() for p in line.split('|')]

                # 边格式: $N1 | $N7 | data_flow | input data
                if len(parts) >= 3 and parts[0].startswith('$N') and parts[1].startswith('$N'):
                    # 检查源节点和目标节点是否存在
                    source_exists = any(node['id'] == parts[0] for node in self.graph_structure['nodes'])
                    target_exists = any(node['id'] == parts[1] for node in self.graph_structure['nodes'])

                    if source_exists and target_exists:
                        edge_info = {
                            'source': parts[0],
                            'target': parts[1],
                            'type': parts[2] if len(parts) > 2 else 'control_flow',
                            'description': parts[3] if len(parts) > 3 else ''
                        }
                        self.graph_structure['edges'].append(edge_info)

        print(
            f"Code flow chart structure generated: {len(self.graph_structure['nodes'])} nodes, {len(self.graph_structure['edges'])} edges")
        return self.graph_structure

    def auto_layout_nodes(self):
        """自动布局节点，确保合理的分布"""
        nodes = self.graph_structure['nodes']

        if not nodes:
            return

        # 按类型分组
        type_groups = {}
        for node in nodes:
            node_type = node.get('node_type', 'variable')
            if node_type not in type_groups:
                type_groups[node_type] = []
            type_groups[node_type].append(node)

        # 为每种类型分配区域
        x_start, y_start = 0, 0
        max_width = 8

        for node_type, group in type_groups.items():
            for i, node in enumerate(group):
                row = i // max_width
                col = i % max_width

                # 根据类型设置基本位置
                if node_type == 'data':
                    base_x, base_y = 0, 6
                elif node_type == 'variable':
                    base_x, base_y = 0, 4
                elif node_type == 'assignment':
                    base_x, base_y = 3, 6
                elif node_type == 'calculation':
                    base_x, base_y = 3, 4
                elif node_type == 'condition':
                    base_x, base_y = 6, 6
                elif node_type == 'loop':
                    base_x, base_y = 6, 4
                elif node_type == 'call':
                    base_x, base_y = 9, 6
                elif node_type == 'return':
                    base_x, base_y = 9, 4
                else:
                    base_x, base_y = 0, 0

                node['x'] = base_x + col * 1.5
                node['y'] = base_y - row * 1.2

    def create_graphologue_style_chart(self, output_filename="code_flow_chart.png"):
        """Create Graphologue-style flow chart"""
        print("=== Creating Graphologue-style flow chart ===")
        if not self.graph_structure.get('nodes'):
            print("Error: Please generate graph structure first")
            return False

        # 自动布局节点
        self.auto_layout_nodes()

        # Create figure with appropriate size
        fig, ax = plt.subplots(figsize=(20, 16))

        # Define node styles - 使用黑白配色
        node_styles = {
            'data': {'color': '#FFFFFF', 'shape': 'ellipse', 'text_color': '#000000', 'edge_color': '#000000'},
            'variable': {'color': '#F5F5F5', 'shape': 'rect', 'text_color': '#000000', 'edge_color': '#000000'},
            'assignment': {'color': '#E8E8E8', 'shape': 'rect', 'text_color': '#000000', 'edge_color': '#000000'},
            'calculation': {'color': '#DCDCDC', 'shape': 'rect', 'text_color': '#000000', 'edge_color': '#000000'},
            'condition': {'color': '#D3D3D3', 'shape': 'diamond', 'text_color': '#000000', 'edge_color': '#000000'},
            'loop': {'color': '#C0C0C0', 'shape': 'hexagon', 'text_color': '#000000', 'edge_color': '#000000'},
            'call': {'color': '#A9A9A9', 'shape': 'rect', 'text_color': '#000000', 'edge_color': '#000000'},
            'return': {'color': '#808080', 'shape': 'ellipse', 'text_color': '#FFFFFF', 'edge_color': '#000000'}
        }

        # Define relationship styles - 使用黑白配色
        relation_styles = {
            'data_flow': {'color': '#000000', 'style': 'solid', 'width': 2.0, 'arrowstyle': '->'},
            'control_flow': {'color': '#333333', 'style': 'solid', 'width': 2.0, 'arrowstyle': '->'},
            'assignment': {'color': '#666666', 'style': 'solid', 'width': 1.5, 'arrowstyle': '->'},
            'calculation': {'color': '#999999', 'style': 'solid', 'width': 1.5, 'arrowstyle': '->'},
            'condition': {'color': '#CCCCCC', 'style': 'dashed', 'width': 1.5, 'arrowstyle': '->'},
            'iteration': {'color': '#000000', 'style': 'solid', 'width': 2.0, 'arrowstyle': '->'}
        }

        # Calculate bounds for auto-scaling
        all_x = [node['x'] for node in self.graph_structure['nodes']]
        all_y = [node['y'] for node in self.graph_structure['nodes']]

        if all_x and all_y:
            min_x, max_x = min(all_x), max(all_x)
            min_y, max_y = min(all_y), max(all_y)

            # Add padding
            padding_x = (max_x - min_x) * 0.2 + 2
            padding_y = (max_y - min_y) * 0.2 + 2

            ax.set_xlim(min_x - padding_x, max_x + padding_x)
            ax.set_ylim(min_y - padding_y, max_y + padding_y)

        # 首先绘制边
        print(f"Drawing {len(self.graph_structure['edges'])} edges...")
        drawn_edges = 0
        for edge in self.graph_structure['edges']:
            source_id = edge['source']
            target_id = edge['target']

            source_node = next((node for node in self.graph_structure['nodes'] if node['id'] == source_id), None)
            target_node = next((node for node in self.graph_structure['nodes'] if node['id'] == target_id), None)

            if source_node and target_node:
                x1, y1 = source_node['x'], source_node['y']
                x2, y2 = target_node['x'], target_node['y']

                rel_type = edge.get('type', 'control_flow')
                style = relation_styles.get(rel_type, relation_styles['control_flow'])

                # 绘制箭头
                ax.annotate('',
                            xy=(x2, y2),
                            xytext=(x1, y1),
                            arrowprops=dict(
                                arrowstyle=style['arrowstyle'],
                                color=style['color'],
                                lw=style['width'],
                                linestyle=style['style'],
                                alpha=0.8,
                                shrinkA=15,
                                shrinkB=15
                            ))
                drawn_edges += 1

        print(f"Successfully drew {drawn_edges} edges")

        # 然后绘制节点
        print(f"Drawing {len(self.graph_structure['nodes'])} nodes...")
        for node in self.graph_structure['nodes']:
            node_id = node['id']
            label = node['label']
            node_type = node.get('node_type', 'variable')
            x, y = node['x'], node['y']

            style = node_styles.get(node_type, node_styles['variable'])

            # 根据形状绘制节点
            if style['shape'] == 'ellipse':
                node_patch = patches.Ellipse((x, y), 1.5, 1.0,
                                             facecolor=style['color'],
                                             edgecolor=style['edge_color'],
                                             linewidth=1.5,
                                             alpha=0.9)
            elif style['shape'] == 'diamond':
                points = [
                    (x, y + 0.7),
                    (x + 0.7, y),
                    (x, y - 0.7),
                    (x - 0.7, y)
                ]
                node_patch = patches.Polygon(points,
                                             facecolor=style['color'],
                                             edgecolor=style['edge_color'],
                                             linewidth=1.5,
                                             alpha=0.9)
            elif style['shape'] == 'hexagon':
                points = [
                    (x - 0.5, y + 0.4),
                    (x + 0.5, y + 0.4),
                    (x + 0.6, y),
                    (x + 0.5, y - 0.4),
                    (x - 0.5, y - 0.4),
                    (x - 0.6, y)
                ]
                node_patch = patches.Polygon(points,
                                             facecolor=style['color'],
                                             edgecolor=style['edge_color'],
                                             linewidth=1.5,
                                             alpha=0.9)
            else:  # rectangle
                node_patch = patches.Rectangle((x - 0.7, y - 0.5), 1.4, 1.0,
                                               facecolor=style['color'],
                                               edgecolor=style['edge_color'],
                                               linewidth=1.5,
                                               alpha=0.9)

            ax.add_patch(node_patch)

            # 添加节点标签，自动调整文本大小
            wrapped_text = self.wrap_text(label, max_chars=15)
            ax.text(x, y, wrapped_text,
                    ha='center', va='center', fontsize=8,
                    fontweight='bold', color=style['text_color'],
                    wrap=True)

        # 设置标题
        plt.title("Code Flow Chart", fontsize=16, fontweight='bold', pad=20)

        # 创建图例
        self.create_simple_legend(ax, node_styles, relation_styles)

        # 移除坐标轴
        ax.set_aspect('equal')
        plt.axis('off')
        plt.tight_layout()

        # 保存图片
        plt.savefig(output_filename, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close(fig)

        print(f"Code flow chart saved as '{output_filename}'")

        # 显示统计信息
        print("\n=== Statistics ===")
        print(f"Entities: {len(self.entities)}")
        print(f"Relationships: {len(self.relationships)}")
        print(f"Flow chart nodes: {len(self.graph_structure['nodes'])}")
        print(f"Flow chart edges: {len(self.graph_structure['edges'])}")
        return True

    def create_simple_legend(self, ax, node_styles, relation_styles):
        """Create a simple legend"""
        legend_elements = []

        # 添加节点类型到图例
        for node_type, style in node_styles.items():
            legend_elements.append(
                patches.Rectangle((0, 0), 1, 1,
                                  facecolor=style['color'],
                                  edgecolor='black',
                                  label=node_type)
            )

        # 添加关系到图例
        for rel_type, style in relation_styles.items():
            legend_elements.append(
                mlines.Line2D([], [], color=style['color'],
                              linestyle=style['style'],
                              linewidth=style['width'],
                              label=rel_type)
            )

        # 创建图例
        ax.legend(handles=legend_elements,
                  loc='upper right',
                  bbox_to_anchor=(1, 1),
                  frameon=True,
                  fancybox=True,
                  shadow=True,
                  ncol=2,
                  fontsize=7)

    def wrap_text(self, text, max_chars=15):
        """Wrap text to fit in nodes"""
        if len(text) <= max_chars:
            return text

        # 简单的换行逻辑
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            if len(current_line) + len(word) + 1 <= max_chars:
                if current_line:
                    current_line += " " + word
                else:
                    current_line = word
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
                if len(current_line) > max_chars:
                    # 如果单个单词太长，强制分割
                    while len(current_line) > max_chars:
                        lines.append(current_line[:max_chars])
                        current_line = current_line[max_chars:]

        if current_line:
            lines.append(current_line)

        return '\n'.join(lines)

    def generate_complete_flow_chart(self, text, output_filename="code_flow_chart.png"):
        """Complete code flow chart generation process"""
        print("Starting code description processing...")
        print(f"Code description: {text[:100]}...\n")

        # Step 1: Extract entities
        entities = self.extract_entities(text)
        if not entities:
            print("Entity extraction failed")
            return False

        # Step 2: Extract relationships
        relationships = self.extract_relationships(text)
        if not relationships:
            print("Relationship extraction failed")
            return False

        # Step 3: Generate graph structure
        graph_structure = self.generate_graph_structure()
        if not graph_structure:
            print("Graph structure generation failed")
            return False

        # Step 4: Create flow chart
        success = self.create_graphologue_style_chart(output_filename)
        return success


# Example usage
if __name__ == "__main__":
    # Create generator instance
    generator = CodeFlowGenerator()

    # Sample code description
    sample_code = """
[INPUTS]
    <REF> trajectory_points </REF>: List[TrajectoryPoint] "Ordered trajectory points; each has time: float, path_point.theta: float, and v: float"
    <REF> centripedal_acc_threshold </REF>: float "Maximum allowable value for the proxy of centripetal acceleration computed as v * |Δθ| / Δt"
    <REF> normalize_angle </REF>: Callable[[float], float] "Function that normalizes an angle difference into a canonical range before taking its absolute value"
[END_INPUTS]

[OUTPUTS]
    <REF> is_valid </REF>: bool "True if all adjacent trajectory segments satisfy the centripetal-acceleration threshold; otherwise False"
[END_OUTPUTS]

[MAIN_FLOW]
    [SEQUENTIAL_BLOCK]
        [COMMAND Initialize is_valid to True RESULT <REF>is_valid</REF>]
        [COMMAND Iterate over each adjacent pair of trajectory_points by index i from 0 to len(trajectory_points) - 2]
        [COMMAND For the current index i, set p0 = trajectory_points[i] and p1 = trajectory_points[i + 1]]
        [COMMAND Compute segment_time_diff as abs(p1.time - p0.time) RESULT segment_time_diff]
        [COMMAND Compute raw_heading_delta as p1.path_point.theta - p0.path_point.theta then normalize it via normalize_angle and take abs to obtain segment_theta_diff RESULT segment_theta_diff]
        [COMMAND Compute segment_avg_speed as (p0.v + p1.v) * 0.5 RESULT segment_avg_speed]
        [COMMAND Compute segment_angular_accel as segment_avg_speed * segment_theta_diff divided by segment_time_diff RESULT segment_angular_accel]
        [COMMAND If segment_angular_accel > centripedal_acc_threshold then set is_valid to False and terminate the iteration early RESULT <REF>is_valid</REF>]
        [COMMAND After iterating all adjacent pairs or terminating early, return is_valid where True means no threshold breach occurred and False indicates a breach was detected RESULT <REF>is_valid</REF>]
    [END_SEQUENTIAL_BLOCK]
[END_MAIN_FLOW]

[ALTERNATIVE_FLOW: threshold_exceeded]
    [SEQUENTIAL_BLOCK]
        [COMMAND When a segment's computed angular acceleration exceeds centripedal_acc_threshold, immediately conclude the trajectory is invalid by returning False RESULT <REF>is_valid</REF>]
    [END_SEQUENTIAL_BLOCK]
[END_ALTERNATIVE_FLOW]

[EXCEPTION_FLOW: zero_time_interval]
    [LOG "Division by zero encountered because segment_time_diff equals 0 while computing segment_angular_accel"]
    [THROW ZeroDivisionError "segment_time_diff is zero; cannot compute angular acceleration for this segment"]
[END_EXCEPTION_FLOW]
"""

    # Generate complete code flow chart
    success = generator.generate_complete_flow_chart(sample_code, "my_code_flow_chart.png")

    if success:
        print("\n🎉 Code flow chart generation completed!")
    else:
        print("\n❌ Code flow chart generation failed!")
