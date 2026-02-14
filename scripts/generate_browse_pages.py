#!/usr/bin/env python3
"""
生成 Mintlify 浏览页面
从 knowledge-base JSON 生成静态 MDX 文件，用于在 Mintlify 中展示全部知识点
"""

import json
from pathlib import Path
from typing import List, Dict, Tuple

ITEMS_PER_PAGE = 50


def main():
    """主函数"""
    print("=" * 60)
    print("LaTeX MCP Knowledge Base - Browse Pages Generator")
    print("=" * 60)
    print()

    # 1. 加载数据 - V2.0 使用合并的知识库
    print("Loading knowledge base...")
    knowledge_file = Path(__file__).parent.parent / 'knowledge-base' / 'latex-all-knowledge-raw.json'

    with open(knowledge_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"✓ Loaded {len(data)} items from V2.0 (6 packages)")
    print()

    # 2. 生成全部条目页面
    print("Generating pages...")
    print("-" * 60)

    generate_all_pages(data)
    generate_by_type_pages(data)
    generate_by_chart_type_pages(data)
    generate_by_package_pages(data)

    print()

    # 3. 生成首页
    generate_index_page(data)

    print()
    print("=" * 60)
    print("✓ All pages generated successfully!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Update mintlify-docs/mint.json with browse navigation")
    print("2. Run: cd mintlify-docs && npx mintlify dev")
    print("3. Verify the pages in your browser")
    print()


def generate_all_pages(data: List[Dict]):
    """生成所有条目的分页"""
    output_dir = Path(__file__).parent.parent / 'mintlify-docs' / 'browse' / 'all'
    output_dir.mkdir(parents=True, exist_ok=True)

    total_pages = (len(data) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE

    for page_num in range(total_pages):
        start_idx = page_num * ITEMS_PER_PAGE
        end_idx = min(start_idx + ITEMS_PER_PAGE, len(data))
        page_items = data[start_idx:end_idx]

        content = generate_page_content(
            title=f"All Items - Page {page_num + 1}",
            items=page_items,
            page_num=page_num,
            total_pages=total_pages,
            total_items=len(data),
            base_path="all"
        )

        output_file = output_dir / f"page-{page_num:03d}.mdx"
        output_file.write_text(content, encoding='utf-8')

    print(f"  [All Items] Generated {total_pages} pages ({len(data)} items)")


def generate_by_type_pages(data: List[Dict]):
    """按类型生成分页"""
    types = {}
    for item in data:
        item_type = item['type']
        types.setdefault(item_type, []).append(item)

    for item_type, items in types.items():
        output_dir = Path(__file__).parent.parent / 'mintlify-docs' / 'browse' / 'by-type' / item_type
        output_dir.mkdir(parents=True, exist_ok=True)

        total_pages = (len(items) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE

        for page_num in range(total_pages):
            start_idx = page_num * ITEMS_PER_PAGE
            end_idx = min(start_idx + ITEMS_PER_PAGE, len(items))
            page_items = items[start_idx:end_idx]

            content = generate_page_content(
                title=f"{item_type.replace('_', ' ').title()} - Page {page_num + 1}",
                items=page_items,
                page_num=page_num,
                total_pages=total_pages,
                total_items=len(items),
                base_path=f"by-type/{item_type}"
            )

            output_file = output_dir / f"page-{page_num:03d}.mdx"
            output_file.write_text(content, encoding='utf-8')

        print(f"  [{item_type}] Generated {total_pages} pages ({len(items)} items)")


def generate_by_chart_type_pages(data: List[Dict]):
    """按图表类型生成分页"""
    chart_types = {}
    for item in data:
        if item['type'] == 'executable_example':
            chart_type = item.get('chart_type', 'other')  # V2: 直接使用chart_type字段
            chart_types.setdefault(chart_type, []).append(item)

    for chart_type, items in chart_types.items():
        output_dir = Path(__file__).parent.parent / 'mintlify-docs' / 'browse' / 'by-chart-type' / chart_type
        output_dir.mkdir(parents=True, exist_ok=True)

        total_pages = (len(items) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE

        for page_num in range(total_pages):
            start_idx = page_num * ITEMS_PER_PAGE
            end_idx = min(start_idx + ITEMS_PER_PAGE, len(items))
            page_items = items[start_idx:end_idx]

            content = generate_page_content(
                title=f"{chart_type.replace('_', ' ').title()} - Page {page_num + 1}",
                items=page_items,
                page_num=page_num,
                total_pages=total_pages,
                total_items=len(items),
                base_path=f"by-chart-type/{chart_type}"
            )

            output_file = output_dir / f"page-{page_num:03d}.mdx"
            output_file.write_text(content, encoding='utf-8')

        print(f"  [{chart_type}] Generated {total_pages} pages ({len(items)} items)")


def generate_by_package_pages(data: List[Dict]):
    """按包生成分页"""
    packages = {}
    for item in data:
        package = item['macro_package']
        packages.setdefault(package, []).append(item)

    for package, items in packages.items():
        output_dir = Path(__file__).parent.parent / 'mintlify-docs' / 'browse' / 'by-package' / package
        output_dir.mkdir(parents=True, exist_ok=True)

        total_pages = (len(items) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE

        for page_num in range(total_pages):
            start_idx = page_num * ITEMS_PER_PAGE
            end_idx = min(start_idx + ITEMS_PER_PAGE, len(items))
            page_items = items[start_idx:end_idx]

            content = generate_page_content(
                title=f"{package.upper()} - Page {page_num + 1}",
                items=page_items,
                page_num=page_num,
                total_pages=total_pages,
                total_items=len(items),
                base_path=f"by-package/{package}"
            )

            output_file = output_dir / f"page-{page_num:03d}.mdx"
            output_file.write_text(content, encoding='utf-8')

        print(f"  [{package}] Generated {total_pages} pages ({len(items)} items)")


def generate_page_content(title: str, items: List[Dict],
                          page_num: int, total_pages: int,
                          total_items: int, base_path: str) -> str:
    """生成单个页面的 MDX 内容"""
    start_item = page_num * ITEMS_PER_PAGE + 1
    end_item = start_item + len(items) - 1

    # 导航链接
    prev_link = f"[← Previous](page-{page_num-1:03d})" if page_num > 0 else ""
    next_link = f"[Next →](page-{page_num+1:03d})" if page_num < total_pages - 1 else ""

    nav_line = " | ".join(filter(None, [prev_link, next_link]))

    content = f"""---
title: "{title}"
description: "Showing items {start_item}-{end_item} of {total_items}"
---

# {title}

Showing items **{start_item}-{end_item}** of **{total_items}** | Page **{page_num + 1}** of **{total_pages}**

{nav_line}

---

"""

    # 添加每个条目
    for i, item in enumerate(items, start=start_item):
        content += format_item(i, item)

    # 底部导航
    content += f"\n---\n\n{nav_line}\n"

    return content


def format_item(index: int, item: Dict) -> str:
    """格式化单个条目为 MDX"""
    item_type = item['type']
    item_id = item.get('id', 'N/A')
    package = item.get('macro_package', 'N/A')

    # 基础信息
    output = f"## {index}. "

    if item_type == 'executable_example':
        chart_type = item.get('metadata', {}).get('chart_type', 'other')
        output += f"{chart_type.replace('_', ' ').title()} Example\n\n"
    elif item_type == 'command_specification':
        output += f"Command Specification\n\n"
    else:
        output += f"{item_type.replace('_', ' ').title()}\n\n"

    # 元数据表格
    output += f"**ID**: `{item_id}`  \n"
    output += f"**Type**: {item_type}  \n"
    output += f"**Package**: {package}  \n"

    if item_type == 'executable_example':
        chart_type = item.get('metadata', {}).get('chart_type', 'N/A')
        output += f"**Chart Type**: {chart_type}  \n"

    output += "\n"

    # 描述
    description = item.get('content', {}).get('description', '')
    if description and description.strip():
        output += "### Description\n\n"
        # 限制描述长度
        if len(description) > 500:
            description = description[:500] + "..."
        output += f"{description}\n\n"

    # 代码
    code = item.get('content', {}).get('code', '')
    if code and code.strip():
        output += "### Code\n\n"
        # 限制代码长度
        if len(code) > 2000:
            output += f"```latex\n{code[:2000]}\n... (truncated)\n```\n\n"
        else:
            output += f"```latex\n{code}\n```\n\n"

    # 依赖
    dependencies = item.get('content', {}).get('dependencies', [])
    if dependencies:
        output += f"**Dependencies**: {', '.join(dependencies)}  \n"

    # MCP 元数据
    mcp_meta = item.get('mcp_metadata', {})
    if mcp_meta:
        quality_score = mcp_meta.get('quality_score', 'N/A')
        priority = mcp_meta.get('priority', 'N/A')
        executable = mcp_meta.get('executable', False)

        output += f"**Quality Score**: {quality_score}  \n"
        output += f"**Priority**: {priority}  \n"
        output += f"**Executable**: {'Yes' if executable else 'No'}  \n"

    output += "\n---\n\n"

    return output


def generate_index_page(data: List[Dict]):
    """生成浏览首页"""
    print("Generating index page...")

    # 统计信息
    types = {}
    chart_types = {}
    packages = {}

    for item in data:
        item_type = item['type']
        types[item_type] = types.get(item_type, 0) + 1

        package = item['macro_package']
        packages[package] = packages.get(package, 0) + 1

        if item_type == 'executable_example':
            chart_type = item.get('chart_type', 'other')  # V2: 直接使用chart_type字段
            chart_types[chart_type] = chart_types.get(chart_type, 0) + 1

    # 生成类型列表
    types_list = '\n'.join(
        f"- **{t.replace('_', ' ').title()}**: {c} items"
        for t, c in sorted(types.items(), key=lambda x: -x[1])
    )

    packages_list = '\n'.join(
        f"- **{p.upper()}**: {c} items"
        for p, c in sorted(packages.items(), key=lambda x: -x[1])
    )

    chart_types_list = '\n'.join(
        f"- **{ct.replace('_', ' ').title()}**: {c} items"
        for ct, c in sorted(chart_types.items(), key=lambda x: -x[1])
    )

    # 生成浏览链接
    browse_by_type = '\n'.join(
        f"- [{t.replace('_', ' ').title()}](by-type/{t}/page-000) - {c} items"
        for t, c in sorted(types.items(), key=lambda x: -x[1])
    )

    browse_by_chart = '\n'.join(
        f"- [{ct.replace('_', ' ').title()}](by-chart-type/{ct}/page-000) - {c} items"
        for ct, c in sorted(chart_types.items(), key=lambda x: -x[1]) if c > 0
    )

    browse_by_package = '\n'.join(
        f"- [{p.upper()}](by-package/{p}/page-000) - {c} items"
        for p, c in sorted(packages.items(), key=lambda x: -x[1])
    )

    content = f"""---
title: "Browse Knowledge Base"
description: "Explore all {len(data)} items in the LaTeX knowledge base"
---

# Browse Knowledge Base

Welcome to the complete LaTeX chart knowledge base browser. Explore all **{len(data)} items** extracted from TikZ and PGFPlots documentation.

## Statistics

### By Type
{types_list}

### By Package
{packages_list}

### By Chart Type (Executable Examples Only)
{chart_types_list}

## Browse Options

### [Browse All Items →](all/page-000)
View all {len(data)} items in sequential order (50 items per page).

### Browse by Type
{browse_by_type}

### Browse by Chart Type
{browse_by_chart}

### Browse by Package
{browse_by_package}

## Search

Use the search box in the top navigation bar to search across all items. The search index includes:
- Code snippets
- Descriptions
- Command names
- Package names
- Chart types

## Download Full Dataset

Download the complete knowledge base for offline use or programmatic access:

- [Structured JSON (6 MB)](https://github.com/inker-yyk/latex-mcp-knowledge/raw/master/knowledge-base/latex-chart-knowledge-structured.json)
- [Statistics](https://github.com/inker-yyk/latex-mcp-knowledge/raw/master/knowledge-base/knowledge-stats.json)
- [TikZ Raw Data](https://github.com/inker-yyk/latex-mcp-knowledge/raw/master/knowledge-base/tikz-knowledge-raw.json)
- [PGFPlots Raw Data](https://github.com/inker-yyk/latex-mcp-knowledge/raw/master/knowledge-base/pgfplots-knowledge-raw.json)

## About This Knowledge Base

This knowledge base was automatically extracted from:
- TikZ/PGF Manual v3.1.10
- PGFPlots Manual v1.18

Each item includes:
- Executable LaTeX code
- Dependencies and requirements
- Quality scores and priority ratings
- MCP protocol metadata

For more information, see the [Knowledge Base Overview](../knowledge/overview).
"""

    output_file = Path(__file__).parent.parent / 'mintlify-docs' / 'browse' / 'index.mdx'
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(content, encoding='utf-8')

    print("  ✓ Generated browse/index.mdx")


if __name__ == '__main__':
    main()
