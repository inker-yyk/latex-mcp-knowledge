# 大模型如何调用 MCP 工具 - 完整流程详解

## 🎯 核心问题

**从用户提问到 MCP 服务器被调用，中间发生了什么？**

---

## 📊 完整流程图

```
用户提问
   ↓
Claude 分析意图
   ↓
查看可用工具列表（MCP 工具注册表）
   ↓
选择最合适的工具
   ↓
构造工具调用请求
   ↓
发送到 MCP 服务器
   ↓
服务器处理并返回结果
   ↓
Claude 整理结果
   ↓
回复用户
```

---

## 🔄 详细步骤解析

### 步骤 0：启动阶段（配置加载）

**发生时机**：Claude Desktop 启动时

**配置文件**：`~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "latex-knowledge": {
      "command": "python3",
      "args": [
        "/Users/yaoyongke/Documents/yyk/0212_task/latex-mcp-knowledge/scripts/mcp_server.py"
      ]
    }
  }
}
```

**Claude 做什么**：
1. 读取配置文件
2. 启动 `python3 mcp_server.py`
3. 请求 `GET /mcp/tools` 获取工具列表
4. 将工具保存到 Claude 的"工具箱"

**服务器返回的工具列表**：
```json
{
  "tools": [
    {
      "name": "get_latex_chart_example",
      "description": "Get executable LaTeX chart examples by type. Use this when user asks for LaTeX code examples, chart templates, or wants to see how to create visualizations.",
      "inputSchema": {
        "type": "object",
        "properties": {
          "chart_type": {
            "type": "string",
            "enum": ["line_chart", "bar_chart", "scatter_plot", "3d_plot", "flowchart", "node_graph", "pie_chart", "other"],
            "description": "Type of chart to retrieve examples for"
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
      "description": "Search the LaTeX knowledge base for code snippets, commands, or concepts. Use this for general searches or when user asks 'how to' questions.",
      "inputSchema": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "Search keywords or phrases"
          },
          "limit": {
            "type": "integer",
            "default": 10
          }
        },
        "required": ["query"]
      }
    },
    {
      "name": "get_command_spec",
      "description": "Get detailed specifications for TikZ/PGFPlots commands. Use when user asks about specific commands like \\draw, \\node, \\addplot.",
      "inputSchema": {
        "type": "object",
        "properties": {
          "command_name": {
            "type": "string",
            "description": "Command name (e.g., draw, node, addplot)"
          },
          "package": {
            "type": "string",
            "enum": ["tikz", "pgfplots"]
          }
        }
      }
    }
  ]
}
```

现在 Claude 的"工具箱"里有 3 个工具了！

---

### 步骤 1：用户提问

```
用户输入：
"给我一个画折线图的 LaTeX 代码例子"
```

---

### 步骤 2：Claude 分析用户意图

Claude 的内部推理（简化版）：

```
输入分析:
- 关键词: "折线图", "LaTeX", "代码", "例子"
- 意图: 用户想要获取示例代码
- 类型: line chart

判断:
- 需要执行某个动作
- 不是简单的对话回复
- 需要使用工具
```

---

### 步骤 3：选择工具

Claude 查看工具箱里的 3 个工具：

```python
# 工具 1: get_latex_chart_example
description = "Get executable LaTeX chart examples by type"
parameters = {
    "chart_type": ["line_chart", "bar_chart", ...],
    "limit": int
}

# 匹配度分析:
# - 用户要 "例子" ✅
# - 用户要 "折线图" ✅ 对应 "line_chart"
# - 这个工具就是为获取图表例子设计的 ✅
# 匹配度: 95%

---

# 工具 2: search_latex_knowledge
description = "Search the LaTeX knowledge base"
parameters = {
    "query": str,
    "limit": int
}

# 匹配度分析:
# - 也能找到折线图的例子 ✅
# - 但是不够精确，需要搜索 🟡
# - 适合更模糊的查询 🟡
# 匹配度: 60%

---

# 工具 3: get_command_spec
description = "Get command specifications"
parameters = {
    "command_name": str,
    "package": str
}

# 匹配度分析:
# - 用户没问具体命令 ❌
# - 用户要的是例子，不是命令文档 ❌
# 匹配度: 10%

---

决策: 使用工具 1 (get_latex_chart_example)
```

---

### 步骤 4：构造工具调用

Claude 根据用户问题填充参数：

```python
tool_call = {
    "name": "get_latex_chart_example",
    "arguments": {
        "chart_type": "line_chart",  # 从 "折线图" 推断
        "limit": 3                    # 默认值，用户没说要多少个
    }
}
```

---

### 步骤 5：发送到 MCP 服务器

Claude Desktop 将工具调用转为 HTTP 请求：

```http
GET /api/mcp/latex/chart/example?chart_type=line_chart&limit=3
Host: localhost:3000
```

---

### 步骤 6：服务器处理

**mcp_server.py 处理逻辑**：

```python
@app.route('/api/mcp/latex/chart/example', methods=['GET'])
def get_chart_examples():
    # 1. 获取参数
    chart_type = request.args.get('chart_type')  # "line_chart"
    limit = int(request.args.get('limit', 10))   # 3

    # 2. 从知识库中筛选
    results = [
        item for item in KNOWLEDGE_BASE  # 5,171 条知识点
        if item['type'] == 'executable_example'  # 只要可执行示例
        and item.get('metadata', {}).get('chart_type') == chart_type  # line_chart
    ]

    # 筛选结果: 从 5,171 条中找到 517 个折线图

    # 3. 限制数量
    results = results[:limit]  # 取前 3 个

    # 4. 返回结果
    return jsonify({
        'total': 517,  # 总共有 517 个折线图
        'items': results  # 返回 3 个
    })
```

**返回的 JSON**：
```json
{
  "total": 517,
  "items": [
    {
      "id": "d6f82f4b36bf",
      "type": "executable_example",
      "macro_package": "pgfplots",
      "content": {
        "code": "\\documentclass{article}\n\\usepackage{pgfplots}\n\\begin{document}\n  \\begin{tikzpicture}\n    \\begin{axis}\n      \\addplot {x^2};\n    \\end{axis}\n  \\end{tikzpicture}\n\\end{document}",
        "description": "Simple line chart with quadratic function",
        "dependencies": ["tikz", "pgfplots"]
      },
      "mcp_metadata": {
        "quality_score": 0.9,
        "executable": true
      }
    },
    {
      "id": "3d03935c3ab8",
      "content": {
        "code": "\\begin{tikzpicture}\n  \\begin{axis}[xlabel={x}, ylabel={y}]\n    \\addplot coordinates {(0,0) (1,1) (2,4) (3,9)};\n  \\end{axis}\n\\end{tikzpicture}",
        "description": "Line chart with coordinate points"
      }
    },
    {
      "id": "abc123xyz",
      "content": {
        "code": "\\begin{axis}\n  \\addplot table {data.csv};\n\\end{axis}",
        "description": "Line chart from CSV file"
      }
    }
  ],
  "query": {
    "chart_type": "line_chart",
    "limit": 3
  }
}
```

---

### 步骤 7：Claude 整理结果

Claude 收到 JSON 结果后，进行处理：

```python
# Claude 的内部处理
tool_result = receive_from_mcp_server()

# 分析结果
total_found = tool_result['total']  # 517
returned_items = tool_result['items']  # 3 个例子

# 选择最好的一个展示给用户
best_example = returned_items[0]

# 生成用户友好的回复
response = format_response(
    code=best_example['content']['code'],
    description=best_example['content']['description'],
    total_available=total_found
)
```

---

### 步骤 8：回复用户

Claude 生成最终回复：

```
我为您找到了一个折线图的 LaTeX 代码例子：

```latex
\documentclass{article}
\usepackage{pgfplots}
\begin{document}
  \begin{tikzpicture}
    \begin{axis}
      \addplot {x^2};
    \end{axis}
  \end{tikzpicture}
\end{document}
```

这个例子画了一个简单的抛物线（y = x²）。

**使用说明**：
- 需要安装 `pgfplots` 包
- 可以将 `x^2` 替换为其他函数，如 `sin(x)`, `exp(x)` 等
- 可以添加 `xlabel={x}`, `ylabel={y}` 等选项来自定义坐标轴

我在知识库中还找到了 516 个其他折线图的例子，需要看更多示例吗？
```

---

## 🧠 大模型的决策机制

### 关键因素 1：工具描述的质量

工具描述**直接影响**大模型是否会选择该工具。

**❌ 不好的描述**：
```json
{
  "name": "tool1",
  "description": "Get examples"
}
```
问题：太模糊，大模型不知道什么时候用。

**✅ 好的描述**：
```json
{
  "name": "get_latex_chart_example",
  "description": "Get executable LaTeX chart examples by type (line, bar, scatter, 3D, etc.). Use this tool when user asks for LaTeX code examples, chart templates, or wants to see how to create specific types of visualizations using TikZ or PGFPlots. Returns complete, compilable code with descriptions."
}
```
优点：
- 说明了什么时候用（"when user asks for..."）
- 说明了能做什么（"Returns complete, compilable code"）
- 给出了具体例子（"line, bar, scatter..."）

### 关键因素 2：参数的类型和约束

**参数越明确，大模型越容易正确调用**。

**❌ 不好的参数定义**：
```json
{
  "type": {
    "type": "string",
    "description": "Type"
  }
}
```

**✅ 好的参数定义**：
```json
{
  "chart_type": {
    "type": "string",
    "enum": ["line_chart", "bar_chart", "scatter_plot", "3d_plot", "flowchart", "node_graph", "pie_chart", "other"],
    "description": "Type of chart to retrieve examples for. Choose based on user's request: line_chart for time series, bar_chart for comparisons, scatter_plot for correlation, etc."
  }
}
```

优点：
- `enum` 限制了可选值
- 描述中给出了选择建议

### 关键因素 3：上下文理解

大模型会根据对话历史做决策：

```
对话历史:
用户: 我在用 PGFPlots 画图
Claude: 好的，PGFPlots 是一个强大的绘图包。

用户: 给我一个例子
Claude 推理:
- 上下文提到了 PGFPlots
- 用户要 "例子"
- 选择 get_latex_chart_example，并设置 package="pgfplots"
```

---

## 🎯 实战例子

### 例子 1：简单直接的请求

```
用户: "给我一个散点图的例子"

Claude 推理:
1. 意图: 获取例子
2. 类型: 散点图 → scatter_plot
3. 工具: get_latex_chart_example
4. 参数: {chart_type: "scatter_plot", limit: 3}

调用:
GET /api/mcp/latex/chart/example?chart_type=scatter_plot&limit=3

结果:
返回 3 个散点图例子
```

### 例子 2：模糊的请求（需要搜索）

```
用户: "如何在图表中添加网格线？"

Claude 推理:
1. 意图: 询问如何做某事
2. 关键词: "网格线", "grid"
3. 不确定具体图表类型
4. 工具: search_latex_knowledge（更适合模糊搜索）
5. 参数: {query: "grid", limit: 5}

调用:
POST /api/mcp/latex/chart/search
{
  "query": "grid",
  "limit": 5
}

结果:
返回包含 grid 相关的代码和文档
```

### 例子 3：复杂的多步骤请求

```
用户: "我需要画一个 3D 曲面图，要有颜色映射和坐标轴标签"

Claude 推理:
1. 主需求: 3D 曲面图
2. 附加需求: 颜色映射、坐标轴标签
3. 策略: 先找 3D 图例子，然后可能需要搜索颜色映射的用法

第 1 次工具调用:
get_latex_chart_example(chart_type="3d_plot", limit=5)

查看结果后，如果没有颜色映射的例子，第 2 次调用:
search_latex_knowledge(query="colormap 3d", limit=3)

整合两次结果，生成完整回答
```

---

## 📝 总结：关键要点

1. **工具注册**：Claude 启动时从 MCP 服务器获取工具列表
2. **意图理解**：Claude 分析用户提问，理解意图
3. **工具选择**：基于工具描述和参数匹配，选择最合适的工具
4. **参数构造**：从用户问题中提取或推断参数值
5. **调用执行**：发送 HTTP 请求到 MCP 服务器
6. **结果处理**：服务器查询知识库并返回结果
7. **回复生成**：Claude 将结果转化为用户友好的回复

**核心机制**：
- 依靠**工具描述**匹配用户意图
- 依靠**参数约束**正确填充参数
- 依靠**上下文理解**做出智能决策

---

## 🚀 如何优化你的 MCP 工具？

### 1. 写详细的工具描述
包含：
- 什么时候用这个工具
- 能做什么
- 具体例子

### 2. 明确参数约束
使用：
- `enum` 限制可选值
- `description` 解释每个参数
- `required` 标记必填参数

### 3. 返回结构化结果
确保：
- JSON 格式清晰
- 包含足够的上下文信息
- 有错误处理

### 4. 测试常见问法
测试：
- 直接的问题："给我一个折线图"
- 模糊的问题："如何画图？"
- 复杂的问题："我需要一个带图例的 3D 图"

---

**现在你明白了整个流程！** 🎉

大模型通过工具的**描述**和**参数定义**来决定何时、如何调用你的 MCP 服务器。

有问题随时问我！
