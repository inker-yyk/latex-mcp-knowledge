#!/usr/bin/env python3
"""
生成精选 LaTeX 示例页面
每个包创建一个包含代码示例的页面，供 MCP 索引
"""

import json
from pathlib import Path
from typing import List, Dict

def escape_latex_for_mdx(code: str) -> str:
    """转义 LaTeX 代码中的特殊字符"""
    if not code:
        return code
    # 在代码块内部，我们使用 HTML 实体来转义大括号
    # 这样 MDX 解析器就不会把它们当作 JS 表达式
    code = code.replace('{', '&#123;')
    code = code.replace('}', '&#125;')
    return code

def generate_examples_page(package_name: str, items: List[Dict], output_dir: Path):
    """为每个包生成示例页面"""

    # 只选择有代码的可执行示例
    examples = [item for item in items if item.get('type') == 'executable_example' and item.get('code')]

    # 每个包最多 100 个示例
    examples = examples[:100]

    if not examples:
        print(f"  Skipping {package_name} - no executable examples")
        return

    # 生成页面内容
    content = f"""---
title: "{package_name.upper()} Code Examples"
description: "Executable LaTeX examples from {package_name} package"
---

# {package_name.upper()} Code Examples

This page contains {len(examples)} executable examples from the {package_name} package.

"""

    for idx, item in enumerate(examples, 1):
        code = item.get('code', '')
        chart_type = item.get('chart_type', 'other')
        item_id = item.get('id', 'N/A')

        # 转义代码
        escaped_code = escape_latex_for_mdx(code)

        # 限制代码长度
        if len(escaped_code) > 1500:
            escaped_code = escaped_code[:1500] + "\n... (truncated)"

        content += f"""## Example {idx}: {chart_type.replace('_', ' ').title()}

**ID**: `{item_id}`

<pre><code class="language-latex">
{escaped_code}
</code></pre>

---

"""

    # 写入文件
    output_file = output_dir / f"{package_name}-examples.mdx"
    output_file.write_text(content, encoding='utf-8')
    print(f"  ✓ Generated {package_name}-examples.mdx ({len(examples)} examples)")

def main():
    """主函数"""
    print("=" * 60)
    print("LaTeX Examples Pages Generator")
    print("=" * 60)
    print()

    # 加载数据
    knowledge_file = Path(__file__).parent.parent / 'knowledge-base' / 'latex-all-knowledge-raw.json'
    with open(knowledge_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"Loaded {len(data)} items")
    print()

    # 按包分组
    packages = {}
    for item in data:
        pkg = item.get('macro_package', 'unknown')
        packages.setdefault(pkg, []).append(item)

    # 输出目录
    output_dir = Path(__file__).parent.parent / 'mintlify-docs' / 'examples'
    output_dir.mkdir(parents=True, exist_ok=True)

    # 为每个包生成页面
    print("Generating example pages...")
    for package_name, items in sorted(packages.items()):
        generate_examples_page(package_name, items, output_dir)

    print()
    print("=" * 60)
    print("✓ All example pages generated!")
    print("=" * 60)

if __name__ == '__main__':
    main()
