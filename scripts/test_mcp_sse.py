#!/usr/bin/env python3
"""
测试 MCP SSE 协议端点
"""

import requests
import json

BASE_URL = "http://127.0.0.1:3000/mcp"

def test_initialize():
    """测试初始化"""
    print("=" * 60)
    print("测试 1: MCP Initialize")
    print("=" * 60)

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "test-client",
                "version": "1.0.0"
            }
        }
    }

    response = requests.post(BASE_URL, json=payload)
    if response.status_code == 200:
        data = response.json()
        print("✅ Initialize 成功")
        print(f"   协议版本: {data['result']['protocolVersion']}")
        print(f"   服务器: {data['result']['serverInfo']['name']} v{data['result']['serverInfo']['version']}")
        return True
    else:
        print(f"❌ 失败: {response.status_code}")
        return False


def test_list_tools():
    """测试工具列表"""
    print("\n" + "=" * 60)
    print("测试 2: List Tools")
    print("=" * 60)

    payload = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {}
    }

    response = requests.post(BASE_URL, json=payload)
    if response.status_code == 200:
        data = response.json()
        tools = data['result']['tools']
        print(f"✅ 找到 {len(tools)} 个工具:\n")
        for tool in tools:
            print(f"   - {tool['name']}")
            print(f"     {tool['description'][:60]}...")
        return True
    else:
        print(f"❌ 失败: {response.status_code}")
        return False


def test_get_chart_example():
    """测试获取图表示例"""
    print("\n" + "=" * 60)
    print("测试 3: Get Chart Example")
    print("=" * 60)

    payload = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "get_latex_chart_example",
            "arguments": {
                "chart_type": "line_chart",
                "limit": 2
            }
        }
    }

    response = requests.post(BASE_URL, json=payload)
    if response.status_code == 200:
        data = response.json()
        content = data['result']['content'][0]['text']
        lines = content.split('\n')
        print("✅ 成功获取示例")
        print(f"\n前10行预览:")
        for line in lines[:10]:
            print(f"   {line}")
        return True
    else:
        print(f"❌ 失败: {response.status_code}")
        return False


def test_search_knowledge():
    """测试知识搜索"""
    print("\n" + "=" * 60)
    print("测试 4: Search Knowledge")
    print("=" * 60)

    payload = {
        "jsonrpc": "2.0",
        "id": 4,
        "method": "tools/call",
        "params": {
            "name": "search_latex_knowledge",
            "arguments": {
                "query": "addplot",
                "limit": 3
            }
        }
    }

    response = requests.post(BASE_URL, json=payload)
    if response.status_code == 200:
        data = response.json()
        content = data['result']['content'][0]['text']
        lines = content.split('\n')
        print("✅ 搜索成功")
        print(f"\n前10行预览:")
        for line in lines[:10]:
            print(f"   {line}")
        return True
    else:
        print(f"❌ 失败: {response.status_code}")
        return False


def test_get_command_spec():
    """测试获取命令规范"""
    print("\n" + "=" * 60)
    print("测试 5: Get Command Spec")
    print("=" * 60)

    payload = {
        "jsonrpc": "2.0",
        "id": 5,
        "method": "tools/call",
        "params": {
            "name": "get_command_spec",
            "arguments": {
                "command_name": "draw",
                "limit": 2
            }
        }
    }

    response = requests.post(BASE_URL, json=payload)
    if response.status_code == 200:
        data = response.json()
        content = data['result']['content'][0]['text']
        lines = content.split('\n')
        print("✅ 成功获取命令规范")
        print(f"\n前10行预览:")
        for line in lines[:10]:
            print(f"   {line}")
        return True
    else:
        print(f"❌ 失败: {response.status_code}")
        return False


def main():
    print("\n")
    print("█" * 60)
    print("  LaTeX MCP 服务器 - SSE 协议测试")
    print("█" * 60)
    print()

    tests = [
        test_initialize,
        test_list_tools,
        test_get_chart_example,
        test_search_knowledge,
        test_get_command_spec
    ]

    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ 测试异常: {e}")
            results.append(False)

    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"通过: {passed}/{total}")

    if passed == total:
        print("\n🎉 所有测试通过！MCP SSE 端点运行正常。")
        print("\n✅ 现在可以在 Cline 中使用此 MCP 服务器了！")
        print("\n配置文件位置:")
        print("  ~/Library/Application Support/Code/User/globalStorage/")
        print("  saoudrizwan.claude-dev/settings/cline_mcp_settings.json")
        print("\n重启 VSCode 以应用配置。")
    else:
        print("\n⚠️  部分测试失败，请检查服务器日志。")

    print()


if __name__ == '__main__':
    main()
