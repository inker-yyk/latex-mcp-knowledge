#!/usr/bin/env python3
"""
快速测试 MCP 服务器的脚本
"""

import requests
import json
import sys

BASE_URL = "http://localhost:3000"

def test_health():
    """测试健康检查"""
    print("=" * 60)
    print("测试 1: 健康检查")
    print("=" * 60)

    try:
        response = requests.get(f"{BASE_URL}/mcp/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 服务器运行正常")
            print(f"   总知识点数: {data['total_items']}")
            print(f"   版本: {data['version']}")
            return True
        else:
            print(f"❌ 服务器返回错误状态: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ 无法连接到服务器")
        print(f"   请确保服务器正在运行:")
        print(f"   python3 scripts/mcp_server.py")
        return False
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False


def test_stats():
    """测试统计信息"""
    print("\n" + "=" * 60)
    print("测试 2: 获取统计信息")
    print("=" * 60)

    try:
        response = requests.get(f"{BASE_URL}/api/mcp/latex/stats", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 统计信息获取成功")
            print(f"\n按类型:")
            for k, v in data['by_type'].items():
                print(f"   - {k}: {v} 条")
            print(f"\n按包:")
            for k, v in data['by_package'].items():
                print(f"   - {k}: {v} 条")
            print(f"\n按图表类型 (前5个):")
            sorted_chart_types = sorted(
                data['by_chart_type'].items(),
                key=lambda x: -x[1]
            )[:5]
            for k, v in sorted_chart_types:
                print(f"   - {k}: {v} 条")
            return True
        else:
            print(f"❌ 失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False


def test_get_examples():
    """测试获取示例"""
    print("\n" + "=" * 60)
    print("测试 3: 获取折线图示例")
    print("=" * 60)

    try:
        response = requests.get(
            f"{BASE_URL}/api/mcp/latex/chart/example",
            params={
                'chart_type': 'line_chart',
                'limit': 3
            },
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 找到 {data['total']} 个折线图示例")
            print(f"   返回 {len(data['items'])} 个结果\n")

            for i, item in enumerate(data['items'], 1):
                print(f"示例 {i}:")
                print(f"  ID: {item['id']}")
                print(f"  包: {item['macro_package']}")
                code = item['content']['code']
                preview = code[:100] + "..." if len(code) > 100 else code
                print(f"  代码预览: {preview}\n")
            return True
        else:
            print(f"❌ 失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False


def test_search():
    """测试搜索功能"""
    print("\n" + "=" * 60)
    print("测试 4: 搜索 'addplot' 关键词")
    print("=" * 60)

    try:
        response = requests.post(
            f"{BASE_URL}/api/mcp/latex/chart/search",
            json={
                'query': 'addplot',
                'limit': 3
            },
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 搜索成功")
            print(f"   找到 {data['total']} 个匹配结果")
            print(f"   返回 {len(data['results'])} 个结果\n")

            for i, item in enumerate(data['results'], 1):
                print(f"结果 {i}:")
                print(f"  ID: {item['id']}")
                print(f"  类型: {item['type']}")
                print(f"  包: {item['macro_package']}")
                if 'chart_type' in item.get('metadata', {}):
                    print(f"  图表类型: {item['metadata']['chart_type']}")
                print()
            return True
        else:
            print(f"❌ 失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False


def test_mcp_tools():
    """测试 MCP 工具列表"""
    print("\n" + "=" * 60)
    print("测试 5: 获取 MCP 工具列表")
    print("=" * 60)

    try:
        response = requests.get(f"{BASE_URL}/mcp/tools", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 找到 {len(data['tools'])} 个 MCP 工具\n")

            for tool in data['tools']:
                print(f"工具: {tool['name']}")
                print(f"  描述: {tool['description']}")
                print()
            return True
        else:
            print(f"❌ 失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False


def main():
    print("\n")
    print("█" * 60)
    print("  LaTeX MCP 知识库 - 服务器测试")
    print("█" * 60)
    print()

    tests = [
        test_health,
        test_stats,
        test_get_examples,
        test_search,
        test_mcp_tools
    ]

    results = []
    for test in tests:
        result = test()
        results.append(result)

    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"通过: {passed}/{total}")

    if passed == total:
        print("\n🎉 所有测试通过！服务器运行正常。")
        print("\n下一步:")
        print("  1. 配置 Claude Desktop 使用 MCP")
        print("  2. 或者在你的代码中调用 REST API")
        print("  3. 或者部署到云端")
        print("\n详细说明请查看: MCP_SERVER_GUIDE.md")
    else:
        print("\n⚠️  部分测试失败，请检查服务器日志。")

    print()


if __name__ == '__main__':
    main()
