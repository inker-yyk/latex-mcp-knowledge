# LaTeX Knowledge Base - 综合LaTeX宏包知识库

> 一个全面的、符合MCP协议的LaTeX知识库，覆盖6个主流LaTeX绘图宏包

[![Knowledge Items](https://img.shields.io/badge/Knowledge%20Items-6%2C812-blue)]()
[![Packages](https://img.shields.io/badge/Packages-6-green)]()
[![MCP Protocol](https://img.shields.io/badge/MCP-v1.0-orange)]()
[![License](https://img.shields.io/badge/License-MIT-yellow)]()

## 📊 知识库概览

本知识库包含从6个官方LaTeX宏包手册中提取的 **6,812条结构化知识项**：

### 按宏包分类

| 宏包 | 知识项数 | 应用领域 | 复杂度 |
|------|---------|---------|--------|
| **tikz-pgf** | 3,696 | 通用绘图引擎 | 🔴 极复杂 |
| **pgfplots** | 1,472 | 数据可视化、科学绘图 | 🔴 复杂 |
| **circuitikz** | 816 | 电路图绘制 | 🟡 中等 |
| **tkz-euclide** | 467 | 欧几里得几何 | 🔴 复杂 |
| **chemfig** | 290 | 化学结构式 | 🟢 简单 |
| **tikz-network** | 71 | 网络图绘制 | 🟢 简单 |

### 知识类型分布

- **可执行示例** - 包含完整LaTeX代码的示例
- **命令定义** - 命令语法和参数说明
- **环境定义** - LaTeX环境规范
- **组件定义** - 特殊组件（如电路元件）
- **键值配置** - 配置选项和参数
- **人类反馈** - 警告和最佳实践

### 应用领域

#### 🔬 科学与工程
- **数学**: tikz-pgf, pgfplots, tkz-euclide
- **物理/电子**: circuitikz
- **化学**: chemfig

#### 📊 数据可视化
- **统计图表**: pgfplots
- **网络拓扑**: tikz-network
- **通用图形**: tikz-pgf

#### 📚 教育与出版
- **几何教学**: tkz-euclide
- **化学教材**: chemfig
- **工程文档**: circuitikz

---

## 🚀 快速开始

### 下载知识库

完整的结构化知识库可以直接下载：

```bash
# 下载所有宏包的合并知识库
wget https://github.com/yourusername/latex-mcp-knowledge/raw/main/latex-all-knowledge-raw.json

# 或下载单个宏包知识库
wget https://github.com/yourusername/latex-mcp-knowledge/raw/main/tikz-pgf-knowledge-raw.json
wget https://github.com/yourusername/latex-mcp-knowledge/raw/main/pgfplots-knowledge-raw.json
wget https://github.com/yourusername/latex-mcp-knowledge/raw/main/circuitikz-knowledge-raw.json
wget https://github.com/yourusername/latex-mcp-knowledge/raw/main/tkz-euclide-knowledge-raw.json
wget https://github.com/yourusername/latex-mcp-knowledge/raw/main/chemfig-knowledge-raw.json
wget https://github.com/yourusername/latex-mcp-knowledge/raw/main/tikz-network-knowledge-raw.json
```

### 浏览文档

访问我们的托管文档站点：
```
https://your-username.mintlify.app/
```

### 使用API

```bash
# 按宏包搜索示例
curl "https://your-domain.mintlify.app/api/latex/examples?package=circuitikz&limit=5"

# 按应用领域搜索
curl "https://your-domain.mintlify.app/api/latex/search?domain=chemistry"

# 获取命令文档
curl "https://your-domain.mintlify.app/api/latex/command?name=chemfig"
```

---

## 📖 文档

### 核心文档
- **[手册分类指南](MANUAL_CLASSIFICATION.md)** - 6个手册的详细分类
- **[提取方法详解](EXTRACTION_METHODS.md)** - 信息提取的技术细节
- **[项目总结](PROJECT_SUMMARY.md)** - 项目概览和部署指南
- **[快速开始](mintlify-docs/quickstart.mdx)** - 5分钟快速上手
- **[部署指南](DEPLOYMENT.md)** - 完整部署说明

### 技术文档
- **[MCP服务器指南](MCP_SERVER_GUIDE.md)** - MCP API服务器
- **[MCP工作原理](HOW_MCP_WORKS.md)** - 协议详解
- **[搜索示例](SEARCH_EXAMPLES.md)** - API使用示例
- **[知识库报告](KNOWLEDGE_BASE_REPORT.md)** - 统计分析

---

## 🏗️ 项目结构

```
latex-mcp-knowledge/
├── MANUAL_CLASSIFICATION.md         # 📋 手册分类指南（新增）
├── EXTRACTION_METHODS.md            # 🔧 提取方法详解（新增）
├── README.md                        # 📖 本文件（更新）
│
├── knowledge-base/                  # 💾 知识数据
│   ├── latex-all-knowledge-raw.json        # 合并知识库（6,812项）
│   ├── tikz-pgf-knowledge-raw.json         # TikZ/PGF（3,696项）
│   ├── pgfplots-knowledge-raw.json         # PGFPlots（1,472项）
│   ├── circuitikz-knowledge-raw.json       # CircuiTikZ（816项）
│   ├── tkz-euclide-knowledge-raw.json      # Tkz-Euclide（467项）
│   ├── chemfig-knowledge-raw.json          # Chemfig（290项）
│   ├── tikz-network-knowledge-raw.json     # TikZ-Network（71项）
│   └── extraction-stats.json               # 统计信息
│
├── scripts/                         # 🛠️ 工具脚本
│   ├── extract_tex_content_v2.py           # V2提取脚本（新增）
│   ├── extract_tex_content.py              # V1提取脚本（旧）
│   ├── structure_knowledge.py              # 结构化转换
│   └── mcp_server.py                       # API服务器
│
├── mintlify-docs/                   # 📚 文档站点
│   ├── mint.json                           # Mintlify配置
│   ├── openapi.json                        # API规范
│   └── *.mdx                               # 文档页面
│
└── tests/                          # 🧪 测试文件
```

---

## 🔍 知识库详细信息

### 文件大小

| 文件 | 大小 | 说明 |
|------|------|------|
| latex-all-knowledge-raw.json | 3.1 MB | 所有宏包合并 |
| tikz-pgf-knowledge-raw.json | 1.7 MB | TikZ/PGF核心 |
| pgfplots-knowledge-raw.json | 762 KB | 数据可视化 |
| circuitikz-knowledge-raw.json | 308 KB | 电路图 |
| tkz-euclide-knowledge-raw.json | 273 KB | 几何绘图 |
| chemfig-knowledge-raw.json | 113 KB | 化学结构 |
| tikz-network-knowledge-raw.json | 23 KB | 网络图 |

### 知识项分布（按等级）

#### 🟢 一级：单一宏包（简单）
- **tikz-network**: 71项 - 网络图绘制
- **chemfig**: 290项 - 化学结构式

#### 🟡 二级：中等规模宏包
- **circuitikz**: 816项 - 电路图（200+组件）

#### 🔴 三级：复杂多功能宏包
- **tkz-euclide**: 467项 - 欧几里得几何（32个模块）
- **pgfplots**: 1,472项 - 科学绘图
- **tikz-pgf**: 3,696项 - 通用绘图引擎（50+子库）

---

## 💻 本地开发

### 环境要求
- Python 3.8+
- pip

### 安装依赖

```bash
# 克隆仓库
git clone https://github.com/yourusername/latex-mcp-knowledge.git
cd latex-mcp-knowledge

# 安装Python依赖
pip install flask flask-cors
```

### 运行API服务器

```bash
python scripts/mcp_server.py

# 测试
curl http://localhost:3000/mcp/health
```

### 重新生成知识库

```bash
# 使用V2提取脚本（支持6个宏包）
python scripts/extract_tex_content_v2.py

# 结构化处理
python scripts/structure_knowledge.py
```

---

## 📊 使用示例

### Python

```python
import requests
import json

# 加载知识库
with open('latex-all-knowledge-raw.json', 'r') as f:
    knowledge = json.load(f)

# 按宏包筛选
circuitikz_items = [
    item for item in knowledge
    if item['macro_package'] == 'circuitikz'
]

print(f"CircuiTikZ: {len(circuitikz_items)} items")

# 按类型筛选
examples = [
    item for item in knowledge
    if item['type'] == 'executable_example'
]

print(f"Total examples: {len(examples)}")
```

### JavaScript

```javascript
// 加载知识库
fetch('latex-all-knowledge-raw.json')
  .then(response => response.json())
  .then(knowledge => {
    // 按应用领域筛选
    const chemistryItems = knowledge.filter(
      item => item.macro_package === 'chemfig'
    );

    console.log(`Chemistry items: ${chemistryItems.length}`);
  });
```

### 命令行

```bash
# 统计各宏包的知识项数量
jq 'group_by(.macro_package) | map({package: .[0].macro_package, count: length})' \
  latex-all-knowledge-raw.json

# 提取所有化学示例
jq '[.[] | select(.macro_package == "chemfig" and .type == "executable_example")]' \
  latex-all-knowledge-raw.json > chemfig-examples.json

# 查找包含特定命令的项
jq '[.[] | select(.code? and (.code | contains("\\addplot")))]' \
  latex-all-knowledge-raw.json
```

---

## 🎯 使用场景

### AI/机器学习
- 训练LaTeX代码生成模型
- 构建LaTeX代码补全系统
- 图表类型识别和推荐

### 代码生成Agent
- 根据自然语言描述生成LaTeX图表
- 自动选择合适的宏包和命令
- 提供可执行的示例代码

### 开发工具
- IDE插件的命令提示
- 在线LaTeX编辑器的模板库
- 语法高亮和错误检查

### 教育和文档
- 交互式LaTeX学习平台
- 宏包文档浏览器
- 示例代码搜索引擎

---

## 🌐 部署选项

### 选项1：Mintlify（推荐）

1. 推送到GitHub
2. 连接到 [Mintlify](https://mintlify.com)
3. 自动部署文档站点

### 选项2：Vercel

```bash
npm install -g vercel
vercel --prod
```

### 选项3：Docker

```bash
docker build -t latex-mcp-api .
docker run -p 3000:3000 latex-mcp-api
```

详见 [DEPLOYMENT.md](DEPLOYMENT.md)

---

## 🤝 贡献

欢迎贡献！请：

1. Fork本仓库
2. 创建特性分支
3. 提交Pull Request

### 贡献方向
- 添加新的LaTeX宏包支持
- 改进提取算法
- 增加更多示例
- 优化分类体系
- 完善文档

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

## 🙏 致谢

知识来源于以下官方手册：

- [TikZ/PGF Manual](https://pgf-tikz.github.io/) by Till Tantau
- [PGFPlots Manual](https://ctan.org/pkg/pgfplots) by Christian Feuersänger
- [CircuiTikZ Manual](https://ctan.org/pkg/circuitikz) by Massimo Redaelli et al.
- [Tkz-Euclide Manual](https://ctan.org/pkg/tkz-euclide) by Alain Matthes
- [Chemfig Manual](https://ctan.org/pkg/chemfig) by Christian Tellechea
- [TikZ-Network Manual](https://ctan.org/pkg/tikz-network) by Jürgen Hackl

---

## 📞 支持

- 📖 [完整文档](mintlify-docs/)
- 🐛 [问题追踪](https://github.com/yourusername/latex-mcp-knowledge/issues)
- 💬 [讨论区](https://github.com/yourusername/latex-mcp-knowledge/discussions)

---

## 🔄 更新日志

### v2.0 (2025-02-14)
- ✨ 新增4个宏包支持：chemfig, circuitikz, tkz-euclide, tikz-network
- 📈 知识库扩展至6,812项（从5,171项）
- 📚 新增手册分类指南
- 🔧 新增详细提取方法文档
- 🛠️ 重构提取脚本，支持多种提取策略

### v1.0 (2025-02-12)
- 🎉 初始版本
- 支持tikz-pgf和pgfplots
- 5,171条知识项
- MCP协议实现

---

**使用** ❤️ **和MCP协议构建**

[查看文档](https://your-username.mintlify.app) • [API参考](https://your-username.mintlify.app/api) • [贡献指南](CONTRIBUTING.md)
