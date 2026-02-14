# LaTeX MCP 知识库 - 服务器使用指南

## 📋 这个服务器做了什么？

这个 MCP 服务器提供了一个 **HTTP API**，让各种应用（包括 Claude Desktop、GPT-4、你的代码等）可以查询 LaTeX 图表知识库。

### 核心功能

1. **加载知识库** - 启动时加载 5,171 条 LaTeX 知识点
2. **提供 REST API** - 7 个 HTTP 接口供查询
3. **支持 MCP 协议** - 可被 Claude Desktop 等 MCP 客户端调用

---

## 🚀 快速开始

### 第一步：安装依赖

```bash
cd /Users/yaoyongke/Documents/yyk/0212_task/latex-mcp-knowledge

# 安装 Python 依赖
pip3 install -r requirements.txt
```

### 第二步：启动服务器

```bash
python3 scripts/mcp_server.py
```

你会看到：
```
============================================================
LaTeX MCP Knowledge Base - Server Starting
============================================================

Total knowledge items: 5171

Available endpoints:
  GET  /mcp/health
  GET  /mcp/tools
  GET  /api/mcp/latex/chart/example
  GET  /api/mcp/latex/chart/command
  GET  /api/mcp/latex/chart/feedback
  POST /api/mcp/latex/chart/search
  GET  /api/mcp/latex/stats

Server running at: http://localhost:3000
============================================================
```

### 第三步：测试服务器

打开另一个终端，测试健康检查：

```bash
curl http://localhost:3000/mcp/health
```

返回：
```json
{
  "status": "ok",
  "total_items": 5171,
  "version": "1.0.0"
}
```

✅ 如果看到这个，说明服务器运行成功！

---

## 📡 API 接口说明

### 1. 健康检查
```bash
curl http://localhost:3000/mcp/health
```

### 2. 获取图表示例
```bash
# 获取折线图示例（最多 5 个）
curl "http://localhost:3000/api/mcp/latex/chart/example?chart_type=line_chart&limit=5"

# 获取 PGFPlots 的示例
curl "http://localhost:3000/api/mcp/latex/chart/example?macro_package=pgfplots&limit=10"
```

### 3. 搜索知识
```bash
curl -X POST http://localhost:3000/api/mcp/latex/chart/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "addplot",
    "limit": 5
  }'
```

### 4. 查询命令规范
```bash
curl "http://localhost:3000/api/mcp/latex/chart/command?command_name=draw&limit=5"
```

### 5. 获取统计信息
```bash
curl http://localhost:3000/api/mcp/latex/stats
```

返回：
```json
{
  "total_items": 5171,
  "by_type": {
    "executable_example": 4166,
    "command_specification": 975,
    "environment_specification": 27,
    "human_feedback": 3
  },
  "by_package": {
    "tikz": 3697,
    "pgfplots": 1474
  },
  "by_chart_type": {
    "line_chart": 517,
    "bar_chart": 32,
    "3d_plot": 115,
    ...
  }
}
```

---

## 🤖 如何让 Claude Desktop 使用（MCP 协议）

### 第一步：保持服务器运行

```bash
# 在一个终端保持运行
python3 scripts/mcp_server.py
```

### 第二步：配置 Claude Desktop

编辑配置文件：

**macOS/Linux**:
```bash
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Windows**:
```
%APPDATA%\Claude\claude_desktop_config.json
```

添加配置：
```json
{
  "mcpServers": {
    "latex-knowledge": {
      "command": "python3",
      "args": [
        "/Users/yaoyongke/Documents/yyk/0212_task/latex-mcp-knowledge/scripts/mcp_server.py"
      ],
      "env": {}
    }
  }
}
```

### 第三步：重启 Claude Desktop

关闭并重新打开 Claude Desktop。

### 第四步：测试 MCP 工具

在 Claude Desktop 中输入：

```
请使用 latex-knowledge 工具搜索一个折线图的例子
```

Claude 会自动调用你的 MCP 服务器！

---

## 🌐 如何让其他大模型使用（REST API）

### Python 示例

```python
import requests

# 搜索折线图
response = requests.post(
    'http://localhost:3000/api/mcp/latex/chart/search',
    json={
        'query': 'line chart',
        'limit': 5,
        'filters': {
            'chart_type': 'line_chart'
        }
    }
)

results = response.json()
print(f"找到 {results['total']} 个结果")

for item in results['results']:
    print(f"\nID: {item['id']}")
    print(f"Code:\n{item['content']['code'][:200]}...")
```

### JavaScript 示例

```javascript
// 获取图表示例
fetch('http://localhost:3000/api/mcp/latex/chart/example?chart_type=bar_chart&limit=5')
  .then(res => res.json())
  .then(data => {
    console.log(`找到 ${data.total} 个柱状图示例`);
    data.items.forEach(item => {
      console.log(item.content.code);
    });
  });
```

### 在 GPT-4 中使用（通过 Function Calling）

```python
import openai

# 定义函数
functions = [{
    "name": "search_latex_knowledge",
    "description": "搜索 LaTeX 图表知识库",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "搜索关键词"},
            "limit": {"type": "integer", "default": 5}
        },
        "required": ["query"]
    }
}]

# GPT-4 对话
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "给我一个画折线图的 LaTeX 代码"}],
    functions=functions,
    function_call="auto"
)

# 如果 GPT-4 决定调用函数
if response.choices[0].message.get("function_call"):
    function_args = json.loads(
        response.choices[0].message["function_call"]["arguments"]
    )

    # 调用你的 API
    result = requests.post(
        'http://localhost:3000/api/mcp/latex/chart/search',
        json=function_args
    )

    # 将结果返回给 GPT-4
    second_response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": "给我一个画折线图的 LaTeX 代码"},
            response.choices[0].message,
            {
                "role": "function",
                "name": "search_latex_knowledge",
                "content": result.text
            }
        ]
    )

    print(second_response.choices[0].message.content)
```

---

## 🔧 技术架构

```
┌─────────────────────────────────────────┐
│  客户端（Client）                        │
│  - Claude Desktop (MCP)                 │
│  - GPT-4 (Function Calling)             │
│  - 你的 Python/JS 代码 (HTTP)           │
└──────────────┬──────────────────────────┘
               │
               │ HTTP Request
               ↓
┌─────────────────────────────────────────┐
│  MCP Server (Flask)                     │
│  scripts/mcp_server.py                  │
│                                         │
│  - 7 个 REST API 端点                   │
│  - MCP 协议支持                         │
│  - CORS 跨域支持                        │
└──────────────┬──────────────────────────┘
               │
               │ Load & Query
               ↓
┌─────────────────────────────────────────┐
│  Knowledge Base (JSON)                  │
│  knowledge-base/                        │
│  latex-chart-knowledge-structured.json  │
│                                         │
│  5,171 条 LaTeX 知识点                  │
└─────────────────────────────────────────┘
```

---

## 🎯 完整测试流程

### 测试 1：启动并验证

```bash
# 1. 启动服务器
python3 scripts/mcp_server.py

# 2. 新终端，测试健康检查
curl http://localhost:3000/mcp/health

# 3. 获取统计信息
curl http://localhost:3000/api/mcp/latex/stats
```

### 测试 2：搜索功能

```bash
# 搜索 "addplot" 关键词
curl -X POST http://localhost:3000/api/mcp/latex/chart/search \
  -H "Content-Type: application/json" \
  -d '{"query": "addplot", "limit": 3}'
```

### 测试 3：获取特定类型示例

```bash
# 获取 3D 图表示例
curl "http://localhost:3000/api/mcp/latex/chart/example?chart_type=3d_plot&limit=5"
```

### 测试 4：MCP 工具列表

```bash
# 查看可用的 MCP 工具
curl http://localhost:3000/mcp/tools
```

---

## 📚 API 参考

### GET /mcp/health
健康检查

**响应**:
```json
{
  "status": "ok",
  "total_items": 5171,
  "version": "1.0.0"
}
```

### GET /api/mcp/latex/chart/example
获取可执行示例

**参数**:
- `chart_type`: line_chart, bar_chart, scatter_plot, 3d_plot, flowchart, node_graph, pie_chart, other
- `macro_package`: tikz, pgfplots
- `limit`: 数量限制（默认 10）

**响应**:
```json
{
  "total": 517,
  "items": [
    {
      "id": "abc123",
      "type": "executable_example",
      "macro_package": "pgfplots",
      "content": {
        "code": "\\begin{tikzpicture}...",
        "description": "..."
      },
      "mcp_metadata": {
        "quality_score": 0.9,
        "executable": true
      }
    }
  ],
  "query": {...}
}
```

### POST /api/mcp/latex/chart/search
通用搜索

**请求体**:
```json
{
  "query": "line chart",
  "category": "all",
  "limit": 10,
  "offset": 0,
  "filters": {
    "chart_type": "line_chart",
    "package": "pgfplots"
  }
}
```

**响应**:
```json
{
  "results": [...],
  "total": 517,
  "query": "line chart",
  "has_more": true,
  "next_offset": 10
}
```

---

## ❓ 常见问题

### Q1: 服务器启动失败
```
ModuleNotFoundError: No module named 'flask'
```

**解决**:
```bash
pip3 install -r requirements.txt
```

### Q2: 端口 3000 已被占用
```
OSError: [Errno 48] Address already in use
```

**解决**:
方法 1 - 关闭占用端口的程序：
```bash
lsof -ti:3000 | xargs kill -9
```

方法 2 - 修改端口：
编辑 `mcp_server.py` 最后一行：
```python
app.run(host='0.0.0.0', port=5000, debug=True)  # 改为 5000
```

### Q3: CORS 错误（浏览器调用时）
浏览器控制台显示 CORS 错误。

**解决**:
服务器已启用 CORS，确保使用正确的 URL（http://localhost:3000）

### Q4: Claude Desktop 无法连接
MCP 工具不出现在 Claude Desktop 中。

**解决**:
1. 确认配置文件路径正确
2. 确认 Python 路径正确（`which python3`）
3. 完全重启 Claude Desktop
4. 查看 Claude Desktop 日志

---

## 🚀 下一步：部署到云端

如果你想让服务器 24 小时运行，可以部署到：

1. **Vercel** (免费)
2. **Railway** (免费额度)
3. **Render** (免费)
4. **你自己的服务器**

需要帮助部署吗？告诉我你的选择！

---

## 📞 需要帮助？

如果遇到问题：
1. 检查服务器是否正常运行（`curl http://localhost:3000/mcp/health`）
2. 查看服务器日志
3. 确认知识库文件存在
4. 检查 Python 版本（需要 Python 3.7+）

---

**项目地址**: https://github.com/inker-yyk/latex-mcp-knowledge
**Mintlify 文档**: https://baidu-a3d5180c.mintlify.app/
