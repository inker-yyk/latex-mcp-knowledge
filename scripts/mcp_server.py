#!/usr/bin/env python3
"""
LaTeX MCP Knowledge Base - MCP Server
符合 Model Context Protocol 的 API 服务器
支持 SSE (Server-Sent Events) 协议
"""

import json
from pathlib import Path
from typing import List, Dict, Optional
from flask import Flask, jsonify, request, Response, stream_with_context
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 加载知识库
KNOWLEDGE_BASE_PATH = Path(__file__).parent.parent / 'knowledge-base' / 'latex-chart-knowledge-structured.json'

with open(KNOWLEDGE_BASE_PATH, 'r', encoding='utf-8') as f:
    KNOWLEDGE_BASE = json.load(f)

print(f"✓ Loaded {len(KNOWLEDGE_BASE)} knowledge items")


# ========================================
# MCP API Endpoints
# ========================================

@app.route('/mcp/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        'status': 'ok',
        'total_items': len(KNOWLEDGE_BASE),
        'version': '1.0.0'
    })


@app.route('/api/mcp/latex/chart/example', methods=['GET'])
def get_chart_examples():
    """
    获取可执行的图表示例

    查询参数:
    - chart_type: line_chart, bar_chart, scatter_plot, 3d_plot, flowchart, node_graph, pie_chart, other
    - macro_package: tikz, pgfplots
    - limit: 最大返回数量 (默认 10)
    """
    chart_type = request.args.get('chart_type')
    macro_package = request.args.get('macro_package')
    limit = int(request.args.get('limit', 10))

    # 过滤可执行示例
    results = [
        item for item in KNOWLEDGE_BASE
        if item['type'] == 'executable_example'
    ]

    # 按 chart_type 过滤
    if chart_type:
        results = [
            item for item in results
            if item.get('metadata', {}).get('chart_type') == chart_type
        ]

    # 按 macro_package 过滤
    if macro_package:
        results = [
            item for item in results
            if item.get('macro_package') == macro_package
        ]

    # 限制数量
    results = results[:limit]

    return jsonify({
        'total': len(results),
        'items': results,
        'query': {
            'chart_type': chart_type,
            'macro_package': macro_package,
            'limit': limit
        }
    })


@app.route('/api/mcp/latex/chart/command', methods=['GET'])
def get_command_specs():
    """
    查询命令规范

    查询参数:
    - command_name: 命令名称 (如 draw, node, addplot)
    - macro_package: tikz, pgfplots
    - limit: 最大返回数量 (默认 10)
    """
    command_name = request.args.get('command_name')
    macro_package = request.args.get('macro_package')
    limit = int(request.args.get('limit', 10))

    # 过滤命令规范
    results = [
        item for item in KNOWLEDGE_BASE
        if item['type'] == 'command_specification'
    ]

    # 按 command_name 搜索
    if command_name:
        results = [
            item for item in results
            if command_name.lower() in item.get('content', {}).get('code', '').lower()
            or command_name.lower() in item.get('content', {}).get('description', '').lower()
        ]

    # 按 macro_package 过滤
    if macro_package:
        results = [
            item for item in results
            if item.get('macro_package') == macro_package
        ]

    # 限制数量
    results = results[:limit]

    return jsonify({
        'total': len(results),
        'items': results,
        'query': {
            'command_name': command_name,
            'macro_package': macro_package,
            'limit': limit
        }
    })


@app.route('/api/mcp/latex/chart/feedback', methods=['GET'])
def get_human_feedback():
    """
    获取人类反馈（警告和最佳实践）

    查询参数:
    - macro_package: tikz, pgfplots
    """
    macro_package = request.args.get('macro_package')

    # 过滤人类反馈
    results = [
        item for item in KNOWLEDGE_BASE
        if item['type'] == 'human_feedback'
    ]

    # 按 macro_package 过滤
    if macro_package:
        results = [
            item for item in results
            if item.get('macro_package') == macro_package
        ]

    return jsonify({
        'total': len(results),
        'items': results,
        'query': {
            'macro_package': macro_package
        }
    })


@app.route('/api/mcp/latex/chart/search', methods=['POST'])
def search_knowledge():
    """
    通用知识搜索

    请求体:
    {
        "query": "搜索关键词",
        "category": "tikz|pgfplots|charts|all",
        "limit": 10,
        "offset": 0,
        "filters": {
            "chart_type": "line_chart",
            "package": "tikz|pgfplots"
        }
    }
    """
    data = request.get_json()

    query = data.get('query', '').lower()
    category = data.get('category', 'all')
    limit = data.get('limit', 10)
    offset = data.get('offset', 0)
    filters = data.get('filters', {})

    # 搜索所有字段
    results = []
    for item in KNOWLEDGE_BASE:
        # 检查是否匹配查询
        if query:
            searchable_text = (
                str(item.get('content', {}).get('code', '')) +
                str(item.get('content', {}).get('description', '')) +
                str(item.get('metadata', {}).get('tags', [])) +
                str(item.get('type', ''))
            ).lower()

            if query not in searchable_text:
                continue

        # 应用分类过滤
        if category != 'all':
            package = item.get('macro_package', '')
            if category == 'tikz' and package != 'tikz':
                continue
            if category == 'pgfplots' and package != 'pgfplots':
                continue
            if category == 'charts' and item['type'] != 'executable_example':
                continue

        # 应用额外过滤器
        if filters:
            if 'chart_type' in filters:
                if item.get('metadata', {}).get('chart_type') != filters['chart_type']:
                    continue

            if 'package' in filters:
                if item.get('macro_package') != filters['package']:
                    continue

        results.append(item)

    # 分页
    total = len(results)
    results = results[offset:offset + limit]

    return jsonify({
        'results': results,
        'total': total,
        'query': query,
        'limit': limit,
        'offset': offset,
        'has_more': offset + limit < total,
        'next_offset': offset + limit if offset + limit < total else None
    })


@app.route('/api/mcp/latex/stats', methods=['GET'])
def get_statistics():
    """获取知识库统计信息"""
    stats = {
        'total_items': len(KNOWLEDGE_BASE),
        'by_type': {},
        'by_package': {},
        'by_chart_type': {}
    }

    for item in KNOWLEDGE_BASE:
        # 按类型统计
        item_type = item['type']
        stats['by_type'][item_type] = stats['by_type'].get(item_type, 0) + 1

        # 按包统计
        package = item['macro_package']
        stats['by_package'][package] = stats['by_package'].get(package, 0) + 1

        # 按图表类型统计（仅可执行示例）
        if item['type'] == 'executable_example':
            chart_type = item.get('metadata', {}).get('chart_type', 'other')
            stats['by_chart_type'][chart_type] = stats['by_chart_type'].get(chart_type, 0) + 1

    return jsonify(stats)


# ========================================
# MCP Protocol Endpoints
# ========================================

# ========================================
# MCP Protocol Endpoints
# ========================================

@app.route('/mcp', methods=['POST', 'OPTIONS'])
def mcp_endpoint():
    """
    MCP SSE (Server-Sent Events) 主端点
    处理所有 MCP 协议请求
    """
    if request.method == 'OPTIONS':
        # 处理 CORS 预检请求
        response = Response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

    try:
        data = request.get_json()
        method = data.get('method', '')
        params = data.get('params', {})

        # 根据方法路由到不同的处理函数
        if method == 'tools/list':
            result = handle_list_tools()
        elif method == 'tools/call':
            result = handle_tool_call(params)
        elif method == 'initialize':
            result = handle_initialize(params)
        else:
            result = {
                'error': {
                    'code': -32601,
                    'message': f'Method not found: {method}'
                }
            }

        # 返回 JSON-RPC 2.0 格式响应
        response_data = {
            'jsonrpc': '2.0',
            'id': data.get('id', 1),
            'result': result
        }

        return jsonify(response_data)

    except Exception as e:
        return jsonify({
            'jsonrpc': '2.0',
            'id': data.get('id', 1) if 'data' in locals() else 1,
            'error': {
                'code': -32603,
                'message': f'Internal error: {str(e)}'
            }
        }), 500


def handle_initialize(params):
    """处理初始化请求"""
    return {
        'protocolVersion': '2024-11-05',
        'capabilities': {
            'tools': {}
        },
        'serverInfo': {
            'name': 'latex-mcp-server',
            'version': '1.0.0'
        }
    }


def handle_list_tools():
    """处理工具列表请求"""
    return {
        'tools': [
            {
                "name": "get_latex_chart_example",
                "description": "Get executable LaTeX chart examples by type. Returns ready-to-use TikZ/PGFPlots code for various chart types.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "chart_type": {
                            "type": "string",
                            "enum": ["line_chart", "bar_chart", "scatter_plot", "3d_plot",
                                    "flowchart", "node_graph", "pie_chart", "other"],
                            "description": "Type of chart to get examples for"
                        },
                        "macro_package": {
                            "type": "string",
                            "enum": ["tikz", "pgfplots"],
                            "description": "LaTeX macro package (optional filter)"
                        },
                        "limit": {
                            "type": "integer",
                            "default": 5,
                            "description": "Maximum number of examples to return"
                        }
                    }
                }
            },
            {
                "name": "search_latex_knowledge",
                "description": "Search the LaTeX knowledge base for commands, examples, or concepts. Searches across code, descriptions, and tags.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query (searches in code, descriptions, tags)"
                        },
                        "category": {
                            "type": "string",
                            "enum": ["tikz", "pgfplots", "charts", "all"],
                            "default": "all",
                            "description": "Category to search in"
                        },
                        "limit": {
                            "type": "integer",
                            "default": 10,
                            "description": "Maximum number of results"
                        }
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "get_command_spec",
                "description": "Get detailed TikZ/PGFPlots command specifications including syntax, parameters, and usage examples.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "command_name": {
                            "type": "string",
                            "description": "Command name to look up (e.g., draw, node, addplot)"
                        },
                        "macro_package": {
                            "type": "string",
                            "enum": ["tikz", "pgfplots"],
                            "description": "LaTeX macro package (optional filter)"
                        },
                        "limit": {
                            "type": "integer",
                            "default": 10,
                            "description": "Maximum number of specifications to return"
                        }
                    },
                    "required": ["command_name"]
                }
            },
            {
                "name": "get_human_feedback",
                "description": "Get warnings, best practices, and human feedback about LaTeX chart generation.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "macro_package": {
                            "type": "string",
                            "enum": ["tikz", "pgfplots"],
                            "description": "LaTeX macro package (optional filter)"
                        }
                    }
                }
            }
        ]
    }


def handle_tool_call(params):
    """处理工具调用请求"""
    tool_name = params.get('name', '')
    arguments = params.get('arguments', {})

    try:
        if tool_name == 'get_latex_chart_example':
            chart_type = arguments.get('chart_type')
            macro_package = arguments.get('macro_package')
            limit = arguments.get('limit', 5)

            # 过滤示例
            results = [
                item for item in KNOWLEDGE_BASE
                if item['type'] == 'executable_example'
            ]

            if chart_type:
                results = [
                    item for item in results
                    if item.get('metadata', {}).get('chart_type') == chart_type
                ]

            if macro_package:
                results = [
                    item for item in results
                    if item.get('macro_package') == macro_package
                ]

            results = results[:limit]

            # 格式化返回内容
            content_parts = []
            for item in results:
                code = item['content']['code']
                desc = item['content'].get('description', '')
                content_parts.append(f"**Example ({item['macro_package']})**\n{desc}\n\n```latex\n{code}\n```\n")

            return {
                'content': [
                    {
                        'type': 'text',
                        'text': f"Found {len(results)} examples:\n\n" + "\n---\n\n".join(content_parts)
                    }
                ]
            }

        elif tool_name == 'search_latex_knowledge':
            query = arguments.get('query', '').lower()
            category = arguments.get('category', 'all')
            limit = arguments.get('limit', 10)

            results = []
            for item in KNOWLEDGE_BASE:
                searchable_text = (
                    str(item.get('content', {}).get('code', '')) +
                    str(item.get('content', {}).get('description', '')) +
                    str(item.get('metadata', {}).get('tags', []))
                ).lower()

                if query in searchable_text:
                    # 应用分类过滤
                    if category != 'all':
                        package = item.get('macro_package', '')
                        if category == 'tikz' and package != 'tikz':
                            continue
                        if category == 'pgfplots' and package != 'pgfplots':
                            continue
                        if category == 'charts' and item['type'] != 'executable_example':
                            continue

                    results.append(item)
                    if len(results) >= limit:
                        break

            # 格式化返回
            content_parts = []
            for item in results:
                item_type = item['type']
                package = item['macro_package']
                code = item['content'].get('code', '')
                desc = item['content'].get('description', '')

                content_parts.append(
                    f"**{item_type}** ({package})\n{desc}\n\n```latex\n{code}\n```"
                )

            return {
                'content': [
                    {
                        'type': 'text',
                        'text': f"Found {len(results)} results for '{query}':\n\n" + "\n---\n\n".join(content_parts)
                    }
                ]
            }

        elif tool_name == 'get_command_spec':
            command_name = arguments.get('command_name', '').lower()
            macro_package = arguments.get('macro_package')
            limit = arguments.get('limit', 10)

            results = [
                item for item in KNOWLEDGE_BASE
                if item['type'] == 'command_specification'
                and (command_name in item.get('content', {}).get('code', '').lower()
                     or command_name in item.get('content', {}).get('description', '').lower())
            ]

            if macro_package:
                results = [
                    item for item in results
                    if item.get('macro_package') == macro_package
                ]

            results = results[:limit]

            content_parts = []
            for item in results:
                code = item['content']['code']
                desc = item['content'].get('description', '')
                content_parts.append(
                    f"**{item['macro_package']} Command**\n{desc}\n\n```latex\n{code}\n```"
                )

            return {
                'content': [
                    {
                        'type': 'text',
                        'text': f"Found {len(results)} command specifications:\n\n" + "\n---\n\n".join(content_parts)
                    }
                ]
            }

        elif tool_name == 'get_human_feedback':
            macro_package = arguments.get('macro_package')

            results = [
                item for item in KNOWLEDGE_BASE
                if item['type'] == 'human_feedback'
            ]

            if macro_package:
                results = [
                    item for item in results
                    if item.get('macro_package') == macro_package
                ]

            content_parts = []
            for item in results:
                desc = item['content'].get('description', '')
                code = item['content'].get('code', '')
                content_parts.append(f"**{item['macro_package']}**\n{desc}\n\n```latex\n{code}\n```")

            return {
                'content': [
                    {
                        'type': 'text',
                        'text': f"Found {len(results)} feedback items:\n\n" + "\n---\n\n".join(content_parts)
                    }
                ]
            }

        else:
            return {
                'content': [
                    {
                        'type': 'text',
                        'text': f"Unknown tool: {tool_name}"
                    }
                ],
                'isError': True
            }

    except Exception as e:
        return {
            'content': [
                {
                    'type': 'text',
                    'text': f"Error executing tool {tool_name}: {str(e)}"
                }
            ],
            'isError': True
        }


@app.route('/mcp/tools', methods=['GET'])
def list_tools():
    """列出所有可用的 MCP 工具 (REST API 兼容)"""
    tools = handle_list_tools()
    return jsonify(tools)


# ========================================
# 启动服务器
# ========================================

if __name__ == '__main__':
    print("=" * 60)
    print("LaTeX MCP Knowledge Base - Server Starting")
    print("=" * 60)
    print()
    print(f"Total knowledge items: {len(KNOWLEDGE_BASE)}")
    print()
    print("Available MCP endpoints:")
    print("  POST /mcp                           (MCP Protocol SSE)")
    print("  GET  /mcp/health                    (Health check)")
    print("  GET  /mcp/tools                     (List tools)")
    print()
    print("Available REST API endpoints:")
    print("  GET  /api/mcp/latex/chart/example")
    print("  GET  /api/mcp/latex/chart/command")
    print("  GET  /api/mcp/latex/chart/feedback")
    print("  POST /api/mcp/latex/chart/search")
    print("  GET  /api/mcp/latex/stats")
    print()
    print("Server running at: http://localhost:3000")
    print("MCP endpoint: http://localhost:3000/mcp")
    print("=" * 60)
    print()

    app.run(host='0.0.0.0', port=3000, debug=True)
