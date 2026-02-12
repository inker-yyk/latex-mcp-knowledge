# Mintlify 部署指南

## 方案概述

本项目使用 **Mintlify** 作为文档站点和 MCP 服务器的部署平台。Mintlify 会：

1. 托管所有的 Markdown 文档页面
2. 自动读取 `openapi.json` 生成 API 文档
3. 在 `/mcp` 路径下自动提供 MCP 协议兼容的服务
4. 提供搜索、导航等开箱即用功能

## 部署架构

```
GitHub Repo
    ↓
Mintlify (自动部署)
    ↓
生成的服务:
├── https://your-domain.mintlify.app/           # 文档首页
├── https://your-domain.mintlify.app/api/       # API 参考文档
├── https://your-domain.mintlify.app/examples/  # 示例页面
└── https://your-domain.mintlify.app/mcp/       # MCP 服务器 (自动生成)
```

## 第一步：准备 Mintlify 文档目录结构

已创建的文件结构：

```
latex-mcp-knowledge/
├── mintlify-docs/              # Mintlify 文档根目录
│   ├── mint.json              # 配置文件 (已创建)
│   ├── openapi.json           # OpenAPI 规范 (已创建)
│   ├── introduction.mdx       # 首页 (待创建)
│   ├── quickstart.mdx         # 快速开始 (待创建)
│   ├── installation.mdx       # 安装指南 (待创建)
│   ├── knowledge/             # 知识库页面
│   │   ├── overview.mdx
│   │   ├── tikz.mdx
│   │   ├── pgfplots.mdx
│   │   └── search.mdx
│   ├── charts/                # 图表类型页面
│   │   ├── line-chart.mdx
│   │   ├── bar-chart.mdx
│   │   └── ...
│   ├── api/                   # API 文档页面
│   │   ├── overview.mdx
│   │   ├── chart-example.mdx
│   │   └── ...
│   └── examples/              # 示例页面
│       ├── basic.mdx
│       └── advanced.mdx
└── knowledge-base/            # 结构化知识库数据
    └── *.json                 # 由脚本生成
```

## 第二步：GitHub 仓库设置

### 2.1 创建 GitHub 仓库

```bash
cd /root/task_0813/latex-mcp-knowledge
git init
git add .
git commit -m "Initial commit: LaTeX MCP Knowledge Base"

# 创建 GitHub 仓库后
git remote add origin https://github.com/你的用户名/latex-mcp-knowledge.git
git branch -M main
git push -u origin main
```

### 2.2 目录结构建议

推荐将 `mintlify-docs/` 作为仓库根目录，或者在仓库中明确指定文档路径。

## 第三步：连接 Mintlify

### 3.1 注册并创建项目

1. 访问 https://mintlify.com/
2. 使用 GitHub 账号登录
3. 点击 "New Project"
4. 选择你的 GitHub 仓库：`latex-mcp-knowledge`
5. 指定文档目录：`mintlify-docs` (如果不是根目录)

### 3.2 Mintlify 配置

Mintlify 会自动读取 `mint.json` 配置文件：

```json
{
  "name": "LaTeX Chart Knowledge Base",
  "openapi": "/openapi.json",  // 自动集成 OpenAPI
  "api": {
    "baseUrl": "https://your-domain.mintlify.app/mcp"  // MCP 服务地址
  }
}
```

### 3.3 部署触发

- 每次 push 到 `main` 分支时，Mintlify 会自动重新部署
- 部署时间约 1-3 分钟

## 第四步：知识库数据注入

有两种方式将结构化知识库注入 Mintlify：

### 方案 A：静态 JSON 文件（推荐新手）

将生成的 JSON 文件放在 `mintlify-docs/data/` 目录下：

```bash
mkdir -p mintlify-docs/data
cp knowledge-base/latex-chart-knowledge-structured.json mintlify-docs/data/
```

然后在 MDX 页面中引用：

```mdx
---
title: "Knowledge Browser"
---

import KnowledgeData from '/data/latex-chart-knowledge-structured.json';

<KnowledgeExplorer data={KnowledgeData} />
```

### 方案 B：通过 API 动态加载（进阶）

使用 Mintlify 的自定义组件功能，从外部 API 加载数据：

```jsx
// mintlify-docs/components/KnowledgeLoader.jsx
export default function KnowledgeLoader() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch('/mcp/api/mcp/latex/chart/search?q=example')
      .then(res => res.json())
      .then(setData);
  }, []);

  return <div>...</div>;
}
```

## 第五步：MCP 接口实现

### 关键问题：Mintlify 的 MCP 支持

**重要提示**：Mintlify 会在 `/mcp` 路径下提供基础的 MCP 服务，但**可能需要额外配置**才能实现完整的自定义接口。

有两种实现方式：

### 方式 1：使用 Mintlify 的内置 MCP（限制较多）

Mintlify 会根据你的 `openapi.json` 自动生成 API 文档，但**不会自动实现接口逻辑**。

你需要：
1. 使用 Mintlify 的数据绑定功能
2. 将知识库 JSON 数据通过静态文件方式提供
3. 前端通过 Mintlify 的自定义组件访问数据

### 方式 2：部署独立的 MCP 服务器（推荐）

更灵活的方式是单独部署一个 API 服务器：

1. **部署后端服务**（使用我创建的 `mcp_server.py`）
   - 部署到 Vercel/Railway/Fly.io
   - 或使用 Cloudflare Workers

2. **Mintlify 只作为文档站点**
   - 展示 API 文档
   - 提供使用指南
   - 链接到独立的 MCP 服务器

3. **配置 CORS**
   - 允许 Mintlify 站点访问你的 API

## 第六步：验证部署

部署完成后，验证以下内容：

```bash
# 1. 检查文档站点
curl https://your-domain.mintlify.app/

# 2. 检查 OpenAPI 文档
curl https://your-domain.mintlify.app/openapi.json

# 3. 测试 MCP 接口（如果实现了）
curl "https://your-domain.mintlify.app/mcp/api/mcp/latex/chart/example?chart_type=line_chart"
```

## 推荐的混合部署方案

我建议采用以下架构：

```
┌─────────────────────────────────────────┐
│  Mintlify (文档 + API 文档)              │
│  https://your-domain.mintlify.app       │
│  - 展示知识库内容                        │
│  - OpenAPI 文档                         │
│  - 使用示例                              │
└─────────────────────────────────────────┘
                    │
                    ↓ (链接到)
┌─────────────────────────────────────────┐
│  MCP API 服务器 (独立部署)               │
│  https://api.your-domain.com/mcp        │
│  - 实际的 API 接口实现                   │
│  - 知识库查询逻辑                        │
│  - 数据处理                              │
└─────────────────────────────────────────┘
```

## 下一步操作

1. 我可以帮你创建所有的 MDX 页面内容
2. 设置 GitHub 仓库
3. 部署独立的 MCP 服务器（如果需要）
4. 创建完整的测试脚本

你想先进行哪一步？或者你有关于 Mintlify 部署的其他问题吗？
