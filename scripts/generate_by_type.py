#!/usr/bin/env python3
"""
生成完整的分类知识库页面
按类型分类：可执行示例、命令规范、组件定义等
"""

import json
from pathlib import Path
from typing import List, Dict

ITEMS_PER_PAGE = 50  # 每页条目数

def escape_for_mdx(text: str) -> str:
    """转义可能导致 MDX 解析错误的字符"""
    if not text:
        return text
    text = text.replace('{', '&#123;')
    text = text.replace('}', '&#125;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    return text

def generate_type_pages(type_name: str, items: List[Dict], output_dir: Path):
    """为每种类型生成页面"""

    if not items:
        return

    total_pages = (len(items) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE

    # 类型显示名称
    type_display = {
        'executable_example': 'Executable Examples',
        'command': 'Command Specifications',
        'component': 'Component Definitions',
        'environment': 'Environment Specifications',
        'key_value': 'Key-Value Options'
    }.get(type_name, type_name.replace('_', ' ').title())

    for page_num in range(total_pages):
        start_idx = page_num * ITEMS_PER_PAGE
        end_idx = min(start_idx + ITEMS_PER_PAGE, len(items))
        page_items = items[start_idx:end_idx]

        # 生成页面
        page_title = f"{type_display} - Page {page_num + 1}"
        content = f"""---
title: "{page_title}"
description: "Items {start_idx + 1}-{end_idx} of {len(items)} {type_display.lower()}"
---

# {page_title}

Showing items **{start_idx + 1}-{end_idx}** of **{len(items)}**

"""

        # 导航
        if total_pages > 1:
            nav_parts = []
            if page_num > 0:
                nav_parts.append(f"[← Previous]({type_name}-page-{page_num - 1:03d})")
            nav_parts.append(f"Page {page_num + 1} of {total_pages}")
            if page_num < total_pages - 1:
                nav_parts.append(f"[Next →]({type_name}-page-{page_num + 1:03d})")
            content += " | ".join(nav_parts) + "\n\n---\n\n"

        # 添加条目
        for idx, item in enumerate(page_items, start=start_idx + 1):
            item_id = item.get('id', 'N/A')
            package = item.get('macro_package', 'N/A')

            content += f"## {idx}. "

            # 根据类型显示不同内容
            if type_name == 'executable_example':
                chart_type = item.get('chart_type', 'other')
                content += f"{chart_type.replace('_', ' ').title()}\n\n"
                content += f"**ID**: `{item_id}`  \n"
                content += f"**Package**: {package}  \n"
                content += f"**Type**: Executable Example  \n\n"

                # 代码
                code = item.get('code', '')
                if code:
                    escaped_code = escape_for_mdx(code)
                    if len(escaped_code) > 2000:
                        escaped_code = escaped_code[:2000] + "\n... (truncated)"

                    content += f"""<pre><code class="language-latex">
{escaped_code}
</code></pre>

"""

            elif type_name == 'command':
                cmd_name = item.get('command_name', 'Unknown')
                content += f"Command: `{cmd_name}`\n\n"
                content += f"**ID**: `{item_id}`  \n"
                content += f"**Package**: {package}  \n"
                content += f"**Type**: Command Specification  \n\n"

                description = item.get('description', '')
                if description:
                    content += f"**Description**: {escape_for_mdx(description)}\n\n"

                # 语法
                syntax = item.get('syntax', '')
                if syntax:
                    content += f"**Syntax**:\n```latex\n{syntax}\n```\n\n"

            elif type_name == 'component':
                comp_name = item.get('component_name', 'Unknown')
                content += f"Component: `{comp_name}`\n\n"
                content += f"**ID**: `{item_id}`  \n"
                content += f"**Package**: {package}  \n"
                content += f"**Type**: Component Definition  \n\n"

                description = item.get('description', '')
                if description:
                    content += f"**Description**: {escape_for_mdx(description)}\n\n"

            elif type_name == 'environment':
                env_name = item.get('environment_name', 'Unknown')
                content += f"Environment: `{env_name}`\n\n"
                content += f"**ID**: `{item_id}`  \n"
                content += f"**Package**: {package}  \n"
                content += f"**Type**: Environment Specification  \n\n"

                description = item.get('description', '')
                if description:
                    content += f"**Description**: {escape_for_mdx(description)}\n\n"

            elif type_name == 'key_value':
                key_name = item.get('key_name', 'Unknown')
                content += f"Option: `{key_name}`\n\n"
                content += f"**ID**: `{item_id}`  \n"
                content += f"**Package**: {package}  \n"
                content += f"**Type**: Key-Value Option  \n\n"

                description = item.get('description', '')
                if description:
                    content += f"**Description**: {escape_for_mdx(description)}\n\n"

            content += "---\n\n"

        # 底部导航
        if total_pages > 1:
            content += "\n" + " | ".join(nav_parts) + "\n"

        # 写入文件
        output_file = output_dir / f"{type_name}-page-{page_num:03d}.mdx"
        output_file.write_text(content, encoding='utf-8')

    print(f"  ✓ {type_display:30s}: {total_pages:3d} pages ({len(items):5d} items)")

def generate_index_page(type_stats: List[tuple], output_dir: Path):
    """生成索引页面"""
    content = """---
title: "Knowledge Base by Type"
description: "Browse all 6,812 knowledge items by type"
---

# Knowledge Base by Type

Complete categorization of all LaTeX knowledge items.

## By Type

"""

    for type_name, display_name, count, pages in type_stats:
        content += f"### {display_name} ({count} items)\n\n"
        content += f"- Total: {count} items across {pages} pages\n"
        content += f"- [View {display_name}]({type_name}-page-000)\n\n"

    total = sum(c for _, _, c, _ in type_stats)
    content += f"**Total**: {total} knowledge items\n"

    output_file = output_dir / "by-type-index.mdx"
    output_file.write_text(content, encoding='utf-8')
    print(f"  ✓ Generated index page")

def main():
    """主函数"""
    print("=" * 70)
    print("Complete Knowledge Base Generator - All Types")
    print("=" * 70)
    print()

    # 加载数据
    knowledge_file = Path(__file__).parent.parent / 'knowledge-base' / 'latex-all-knowledge-raw.json'
    with open(knowledge_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"Loaded {len(data)} items")
    print()

    # 按类型分组
    types = {}
    for item in data:
        item_type = item.get('type', 'unknown')
        types.setdefault(item_type, []).append(item)

    # 输出目录
    output_dir = Path(__file__).parent.parent / 'mintlify-docs' / 'knowledge-by-type'
    output_dir.mkdir(parents=True, exist_ok=True)

    # 为每种类型生成页面
    print("Generating pages by type...")
    type_stats = []

    for type_name, items in sorted(types.items(), key=lambda x: -len(x[1])):
        generate_type_pages(type_name, items, output_dir)
        total_pages = (len(items) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE

        display_name = {
            'executable_example': 'Executable Examples',
            'command': 'Command Specifications',
            'component': 'Component Definitions',
            'environment': 'Environment Specifications',
            'key_value': 'Key-Value Options'
        }.get(type_name, type_name.replace('_', ' ').title())

        type_stats.append((type_name, display_name, len(items), total_pages))

    # 生成索引
    print()
    print("Generating index page...")
    generate_index_page(type_stats, output_dir)

    total_items = sum(c for _, _, c, _ in type_stats)
    total_pages = sum(p for _, _, _, p in type_stats)

    print()
    print("=" * 70)
    print(f"✓ Generated {total_pages} pages with {total_items} items!")
    print("=" * 70)

if __name__ == '__main__':
    main()
