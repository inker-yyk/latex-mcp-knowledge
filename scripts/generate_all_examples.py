#!/usr/bin/env python3
"""
生成完整的 LaTeX 示例页面集合
确保所有 5,325 个可执行示例都能被 MCP 索引
"""

import json
from pathlib import Path
from typing import List, Dict

ITEMS_PER_PAGE = 30  # 每页示例数

def escape_for_mdx(text: str) -> str:
    """转义文本中可能导致 MDX 解析错误的字符"""
    if not text:
        return text
    # 转义大括号
    text = text.replace('{', '&#123;')
    text = text.replace('}', '&#125;')
    # 转义其他可能的问题字符
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    # 转义 MDX/JavaScript 保留关键字（在行首）
    # 在 export/import 前添加零宽度空格
    import re
    zwsp = '\u200B'  # 零宽度空格
    text = re.sub(r'^(export|import)(\s)', lambda m: m.group(1) + zwsp + m.group(2), text, flags=re.MULTILINE)
    return text

def generate_package_pages(package_name: str, items: List[Dict], output_dir: Path):
    """为每个包生成多个页面，包含所有示例"""

    # 只选择有代码的可执行示例
    examples = [item for item in items if item.get('type') == 'executable_example' and item.get('code')]

    if not examples:
        print(f"  Skipping {package_name} - no executable examples")
        return

    total_pages = (len(examples) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE

    for page_num in range(total_pages):
        start_idx = page_num * ITEMS_PER_PAGE
        end_idx = min(start_idx + ITEMS_PER_PAGE, len(examples))
        page_examples = examples[start_idx:end_idx]

        # 生成页面内容
        page_title = f"{package_name.upper()} Examples - Page {page_num + 1}"
        content = f"""---
title: "{page_title}"
description: "LaTeX examples {start_idx + 1}-{end_idx} from {package_name} ({len(examples)} total)"
---

# {page_title}

Showing examples **{start_idx + 1}-{end_idx}** of **{len(examples)}** from the {package_name} package.

"""

        # 添加导航
        if total_pages > 1:
            nav_parts = []
            if page_num > 0:
                nav_parts.append(f"[← Previous]({package_name}-page-{page_num - 1:03d})")
            nav_parts.append(f"Page {page_num + 1} of {total_pages}")
            if page_num < total_pages - 1:
                nav_parts.append(f"[Next →]({package_name}-page-{page_num + 1:03d})")
            content += " | ".join(nav_parts) + "\n\n---\n\n"

        # 添加示例
        for idx, item in enumerate(page_examples, start=start_idx + 1):
            code = item.get('code', '')
            chart_type = item.get('chart_type', 'other')
            item_id = item.get('id', 'N/A')
            description = item.get('description', '') or item.get('title', '')

            # 转义代码和描述
            escaped_code = escape_for_mdx(code)
            escaped_desc = escape_for_mdx(description) if description else None

            # 限制代码长度
            if len(escaped_code) > 2000:
                escaped_code = escaped_code[:2000] + "\n... (truncated)"

            content += f"""## Example {idx}: {chart_type.replace('_', ' ').title()}

**ID**: `{item_id}`
**Package**: {package_name}

"""

            if escaped_desc:
                content += f"**Description**: {escaped_desc}\n\n"

            content += f"""<pre><code class="language-latex">
{escaped_code}
</code></pre>

---

"""

        # 底部导航
        if total_pages > 1:
            content += "\n" + " | ".join(nav_parts) + "\n"

        # 写入文件
        output_file = output_dir / f"{package_name}-page-{page_num:03d}.mdx"
        output_file.write_text(content, encoding='utf-8')

    print(f"  ✓ Generated {total_pages} pages for {package_name} ({len(examples)} examples)")

def generate_index_page(packages_info: List[tuple], output_dir: Path):
    """生成索引页面"""
    content = """---
title: "All LaTeX Code Examples"
description: "Browse 5,325+ executable LaTeX examples from 6 packages"
---

# All LaTeX Code Examples

Complete collection of executable LaTeX examples from all 6 packages.

## By Package

"""

    for package_name, count, pages in packages_info:
        content += f"- **{package_name}**: {count} examples across {pages} pages\n"
        for page_num in range(pages):
            content += f"  - [Page {page_num + 1}]({package_name}-page-{page_num:03d})\n"

    content += f"\n**Total**: {sum(c for _, c, _ in packages_info)} executable examples\n"

    output_file = output_dir / "all-examples.mdx"
    output_file.write_text(content, encoding='utf-8')
    print(f"  ✓ Generated index page")

def main():
    """主函数"""
    print("=" * 70)
    print("Complete LaTeX Examples Generator - All 5,325+ Examples")
    print("=" * 70)
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
    output_dir = Path(__file__).parent.parent / 'mintlify-docs' / 'examples-full'
    output_dir.mkdir(parents=True, exist_ok=True)

    # 为每个包生成页面
    print(f"Generating pages ({ITEMS_PER_PAGE} examples per page)...")
    packages_info = []

    for package_name, items in sorted(packages.items()):
        examples = [item for item in items if item.get('type') == 'executable_example' and item.get('code')]
        if examples:
            generate_package_pages(package_name, items, output_dir)
            total_pages = (len(examples) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
            packages_info.append((package_name, len(examples), total_pages))

    # 生成索引页面
    print()
    print("Generating index page...")
    generate_index_page(packages_info, output_dir)

    total_examples = sum(c for _, c, _ in packages_info)
    total_pages = sum(p for _, _, p in packages_info)

    print()
    print("=" * 70)
    print(f"✓ Generated {total_pages} pages with {total_examples} examples!")
    print("=" * 70)
    print()
    print("Summary:")
    for package_name, count, pages in packages_info:
        print(f"  {package_name:20s}: {count:4d} examples in {pages:3d} pages")
    print()

if __name__ == '__main__':
    main()
