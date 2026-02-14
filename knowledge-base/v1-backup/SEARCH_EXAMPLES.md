# LaTeX MCP 搜索示例 - 完整演示

## 📝 搜索是如何工作的？

当你发送搜索请求时，服务器会：
1. 接收你的查询参数
2. 遍历全部 5,171 条知识点
3. 检查每条知识点的内容是否匹配
4. 返回匹配的结果

---

## 🎯 示例 1：搜索包含 "addplot" 的 PGFPlots 折线图

### 第 1 步：发送搜索请求

```bash
curl -X POST http://localhost:3000/api/mcp/latex/chart/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "addplot",
    "category": "pgfplots",
    "limit": 2,
    "filters": {
      "chart_type": "line_chart"
    }
  }'
```

### 第 2 步：服务器处理逻辑

服务器会执行以下步骤：

```python
# 伪代码展示搜索逻辑

results = []

for item in KNOWLEDGE_BASE:  # 遍历 5,171 条知识点

    # 步骤 1: 检查关键词 "addplot"
    searchable_text = (
        item['content']['code'] +           # LaTeX 代码
        item['content']['description'] +    # 描述文本
        str(item['metadata']['tags']) +     # 标签
        item['type']                        # 类型
    ).lower()

    if "addplot" not in searchable_text:
        continue  # 不匹配，跳过

    # 步骤 2: 检查分类 "pgfplots"
    if item['macro_package'] != 'pgfplots':
        continue  # 不是 pgfplots，跳过

    # 步骤 3: 检查图表类型 "line_chart"
    if item['metadata']['chart_type'] != 'line_chart':
        continue  # 不是折线图，跳过

    # 通过所有条件，加入结果
    results.append(item)

# 返回前 2 条结果（limit=2）
return results[:2]
```

### 第 3 步：返回的结果（示例）

```json
{
  "results": [
    {
      "id": "d6f82f4b36bf",
      "type": "executable_example",
      "macro_package": "pgfplots",
      "metadata": {
        "chart_type": "line_chart",
        "tags": ["pgfplots", "line_chart", "example"],
        "source_file": "pgfplots.importexport.tex",
        "created_at": "2026-02-12T21:06:38Z"
      },
      "content": {
        "description": "Executable example from pgfplots.importexport.tex",
        "code": "\\documentclass{article}\n\\usepackage{pgfplots}\n\\usepgfplotslibrary{external}\n\\tikzexternalize\n\\begin{document}\n  \\begin{figure}\n    \\begin{tikzpicture}\n      \\begin{axis}\n        \\addplot {x^2};\n      \\end{axis}\n    \\end{tikzpicture}\n    \\caption{Our first external graphics example}\n  \\end{figure}\n\\end{document}",
        "dependencies": ["tikz", "pgfplots"],
        "options": "[preamble=\\usepackage{pgfplots}]"
      },
      "mcp_metadata": {
        "searchable_fields": ["code", "description", "tags", "chart_type"],
        "priority": 10,
        "quality_score": 0.9,
        "executable": true
      }
    },
    {
      "id": "3d03935c3ab8",
      "type": "executable_example",
      "macro_package": "pgfplots",
      "metadata": {
        "chart_type": "line_chart",
        "tags": ["pgfplots", "line_chart", "addplot"],
        "source_file": "pgfplots.importexport.tex"
      },
      "content": {
        "description": "Simple line plot with addplot command",
        "code": "\\begin{tikzpicture}\n  \\begin{axis}[\n    xlabel={x},\n    ylabel={y}\n  ]\n    \\addplot coordinates {\n      (0,0) (1,1) (2,4) (3,9)\n    };\n  \\end{axis}\n\\end{tikzpicture}",
        "dependencies": ["tikz", "pgfplots"]
      },
      "mcp_metadata": {
        "priority": 8,
        "quality_score": 0.85,
        "executable": true
      }
    }
  ],
  "total": 487,
  "query": "addplot",
  "limit": 2,
  "offset": 0,
  "has_more": true,
  "next_offset": 2
}
```

### 结果解读

- **找到了 487 条**包含 "addplot" 的 PGFPlots 折线图
- **返回前 2 条**（因为 `limit: 2`）
- **每条结果包含**：
  - 完整的 LaTeX 代码
  - 描述信息
  - 依赖包列表
  - 质量分数
  - 是否可执行

---

## 🎯 示例 2：简单关键词搜索

### 请求：搜索 "scatter"

```bash
curl -X POST http://localhost:3000/api/mcp/latex/chart/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "scatter",
    "limit": 3
  }'
```

### 匹配逻辑

```python
# 搜索 "scatter" 会匹配：

# 匹配 1: 代码中包含 scatter
code = "\\begin{axis}[scatter/classes=...] \\addplot[scatter]..."
if "scatter" in code.lower():  # ✅ 匹配

# 匹配 2: 描述中包含 scatter
description = "Example of scatter plot with custom markers"
if "scatter" in description.lower():  # ✅ 匹配

# 匹配 3: 图表类型是 scatter_plot
metadata = {"chart_type": "scatter_plot"}
if "scatter" in str(metadata):  # ✅ 匹配

# 匹配 4: 标签中包含 scatter
tags = ["pgfplots", "scatter", "markers"]
if "scatter" in str(tags).lower():  # ✅ 匹配
```

### 返回结果

```json
{
  "results": [
    {
      "id": "abc123",
      "type": "executable_example",
      "metadata": {
        "chart_type": "scatter_plot",
        "tags": ["scatter", "pgfplots", "markers"]
      },
      "content": {
        "code": "\\begin{axis}\n  \\addplot[scatter, only marks] table {data.dat};\n\\end{axis}",
        "description": "Scatter plot with custom markers"
      }
    },
    // ... 更多结果
  ],
  "total": 41,
  "query": "scatter"
}
```

---

## 🎯 示例 3：组合过滤搜索

### 请求：查找 TikZ 的节点图示例

```bash
curl -X POST http://localhost:3000/api/mcp/latex/chart/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "node",
    "category": "tikz",
    "limit": 5,
    "filters": {
      "chart_type": "node_graph",
      "package": "tikz"
    }
  }'
```

### 过滤条件层层递进

```python
# 原始数据: 5,171 条

# 第 1 层过滤: 关键词 "node"
matches_query = [item for item in data if "node" in item_text]
# 剩余: ~2,000 条

# 第 2 层过滤: 分类 "tikz"
matches_category = [item for item in matches_query if item['macro_package'] == 'tikz']
# 剩余: ~1,500 条

# 第 3 层过滤: 图表类型 "node_graph"
matches_chart_type = [item for item in matches_category
                      if item['metadata']['chart_type'] == 'node_graph']
# 剩余: ~120 条

# 第 4 层过滤: 包名 "tikz" (已包含在第2层)
final_results = matches_chart_type

# 返回前 5 条
return final_results[:5]
```

---

## 🔥 实际测试：用真实数据

### 测试脚本

```python
#!/usr/bin/env python3
import requests
import json

# 搜索配置
search_requests = [
    {
        "name": "搜索折线图",
        "payload": {
            "query": "line",
            "filters": {"chart_type": "line_chart"},
            "limit": 3
        }
    },
    {
        "name": "搜索 \\addplot 命令",
        "payload": {
            "query": "addplot",
            "category": "pgfplots",
            "limit": 5
        }
    },
    {
        "name": "搜索流程图",
        "payload": {
            "query": "flowchart",
            "limit": 2
        }
    }
]

# 执行搜索
for req in search_requests:
    print(f"\n{'='*60}")
    print(f"测试: {req['name']}")
    print('='*60)

    response = requests.post(
        'http://localhost:3000/api/mcp/latex/chart/search',
        json=req['payload']
    )

    if response.status_code == 200:
        data = response.json()
        print(f"✅ 找到 {data['total']} 条结果")
        print(f"   返回 {len(data['results'])} 条")

        for i, item in enumerate(data['results'], 1):
            print(f"\n结果 {i}:")
            print(f"  ID: {item['id']}")
            print(f"  类型: {item['type']}")
            print(f"  包: {item['macro_package']}")

            # 显示代码预览
            code = item['content'].get('code', '')
            if code:
                preview = code[:80] + "..." if len(code) > 80 else code
                print(f"  代码: {preview}")
    else:
        print(f"❌ 请求失败: {response.status_code}")
```

---

## 📊 搜索参数完整说明

### 请求体参数

```json
{
  "query": "搜索关键词",           // 必填，在代码、描述、标签中搜索
  "category": "all|tikz|pgfplots|charts",  // 可选，分类过滤
  "limit": 10,                    // 可选，返回数量限制（默认10）
  "offset": 0,                    // 可选，分页偏移（默认0）
  "filters": {                    // 可选，额外过滤条件
    "chart_type": "line_chart",   // 图表类型
    "package": "tikz"             // 包名
  }
}
```

### 返回结果结构

```json
{
  "results": [                    // 匹配的知识点数组
    {
      "id": "唯一ID",
      "type": "类型",
      "macro_package": "包名",
      "metadata": { ... },
      "content": {
        "code": "LaTeX代码",
        "description": "描述",
        "dependencies": ["依赖列表"]
      },
      "mcp_metadata": {
        "quality_score": 0.9,
        "executable": true
      }
    }
  ],
  "total": 487,                   // 匹配总数
  "query": "addplot",             // 搜索关键词
  "limit": 2,                     // 返回限制
  "offset": 0,                    // 当前偏移
  "has_more": true,               // 是否有更多结果
  "next_offset": 2                // 下一页偏移
}
```

---

## 💡 搜索技巧

### 技巧 1：精确匹配

```json
{
  "query": "\\addplot",           // 搜索命令
  "category": "pgfplots"
}
```

### 技巧 2：宽泛搜索

```json
{
  "query": "plot",                // 会匹配 addplot, barplot, scatter plot 等
  "limit": 20
}
```

### 技巧 3：组合过滤

```json
{
  "query": "axis",
  "filters": {
    "chart_type": "3d_plot",      // 只要3D图表
    "package": "pgfplots"         // 只要PGFPlots
  }
}
```

### 技巧 4：分页浏览

```json
// 第一页
{"query": "node", "limit": 10, "offset": 0}

// 第二页
{"query": "node", "limit": 10, "offset": 10}

// 第三页
{"query": "node", "limit": 10, "offset": 20}
```

---

## 🎬 完整示例：Python 交互式搜索

```python
#!/usr/bin/env python3
import requests

def search_latex(query, **kwargs):
    """搜索 LaTeX 知识库"""
    payload = {"query": query, **kwargs}

    response = requests.post(
        'http://localhost:3000/api/mcp/latex/chart/search',
        json=payload
    )

    if response.status_code == 200:
        return response.json()
    else:
        print(f"错误: {response.status_code}")
        return None

# 使用示例
if __name__ == '__main__':
    # 搜索折线图
    results = search_latex("line chart", limit=3)

    if results:
        print(f"找到 {results['total']} 条结果\n")

        for i, item in enumerate(results['results'], 1):
            print(f"{'='*60}")
            print(f"结果 {i}/{len(results['results'])}")
            print(f"{'='*60}")
            print(f"ID: {item['id']}")
            print(f"类型: {item['type']}")
            print(f"包: {item['macro_package']}")

            if 'chart_type' in item.get('metadata', {}):
                print(f"图表: {item['metadata']['chart_type']}")

            print(f"\n代码:\n{item['content']['code']}\n")

            if item['content'].get('dependencies'):
                print(f"依赖: {', '.join(item['content']['dependencies'])}")

            print()
```

运行输出：
```
找到 517 条结果

============================================================
结果 1/3
============================================================
ID: d6f82f4b36bf
类型: executable_example
包: pgfplots
图表: line_chart

代码:
\documentclass{article}
\usepackage{pgfplots}
\begin{document}
  \begin{tikzpicture}
    \begin{axis}
      \addplot {x^2};
    \end{axis}
  \end{tikzpicture}
\end{document}

依赖: tikz, pgfplots

============================================================
结果 2/3
...
```

---

## 🚀 现在试试！

1. **启动服务器**:
   ```bash
   python3 scripts/mcp_server.py
   ```

2. **运行搜索测试**:
   ```bash
   curl -X POST http://localhost:3000/api/mcp/latex/chart/search \
     -H "Content-Type: application/json" \
     -d '{"query": "scatter", "limit": 3}'
   ```

3. **查看结果**:
   - 会看到匹配的知识点
   - 包含完整的 LaTeX 代码
   - 可以直接复制使用

---

**问题？** 随时告诉我！
