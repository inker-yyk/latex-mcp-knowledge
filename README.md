# LaTeX Chart Knowledge Base

> A comprehensive, MCP protocol-compliant knowledge base for LaTeX chart generation using TikZ and PGFPlots

[![Knowledge Items](https://img.shields.io/badge/Knowledge%20Items-5%2C171-blue)]()
[![Executable Examples](https://img.shields.io/badge/Examples-4%2C166-green)]()
[![MCP Protocol](https://img.shields.io/badge/MCP-v1.0-orange)]()
[![License](https://img.shields.io/badge/License-MIT-yellow)]()

## 📊 What's Inside

This knowledge base contains **5,171 structured knowledge items** extracted from official TikZ/PGF and PGFPlots manuals:

- **4,166 executable examples** - Ready-to-use LaTeX code
- **975 command specifications** - Complete syntax documentation
- **27 environment specifications** - LaTeX environment definitions
- **3 human feedback items** - Warnings and best practices

### By Package
- **TikZ/PGF**: 3,697 items
- **PGFPlots**: 1,474 items

### By Chart Type
- Line charts, bar charts, scatter plots
- 3D plots, surface plots, mesh plots
- Flowcharts, node graphs, diagrams
- Pie charts, and more!

## 🚀 Quick Start

### Browse the Documentation

Visit our hosted documentation (coming soon):
```
https://your-username.mintlify.app/
```

### Use the API

```bash
# Get line chart examples
curl "https://your-domain.mintlify.app/mcp/api/mcp/latex/chart/example?chart_type=line_chart&limit=5"

# Search for commands
curl "https://your-domain.mintlify.app/mcp/api/mcp/latex/chart/command?command_name=addplot"

# Universal search
curl "https://your-domain.mintlify.app/mcp/api/mcp/latex/chart/search?q=axis+labels"
```

### Download the Knowledge Base

The complete structured knowledge base is available as a single JSON file:
```bash
wget https://github.com/yourusername/latex-mcp-knowledge/raw/main/knowledge-base/latex-chart-knowledge-structured.json
```

## 📖 Documentation

- **[Quick Start Guide](mintlify-docs/quickstart.mdx)** - Get started in 5 minutes
- **[Installation & Deployment](mintlify-docs/installation.mdx)** - Deploy your own instance
- **[API Documentation](mintlify-docs/api/overview.mdx)** - Complete API reference
- **[Project Summary](PROJECT_SUMMARY.md)** - Detailed project overview

## 🏗️ Project Structure

```
latex-mcp-knowledge/
├── knowledge-base/              # Structured knowledge data (5,171 items)
│   ├── latex-chart-knowledge-structured.json  # Main knowledge base
│   └── *.json                                 # Raw and statistics files
├── mintlify-docs/               # Documentation site
│   ├── mint.json                # Mintlify configuration
│   ├── openapi.json             # MCP API specification
│   └── *.mdx                    # Documentation pages
└── scripts/                     # Build and server scripts
    ├── extract_tex_content.py   # Extract from LaTeX manuals
    ├── structure_knowledge.py   # Convert to MCP format
    └── mcp_server.py            # API server (Flask)
```

## 🔌 MCP API Endpoints

All endpoints implement the Model Context Protocol (MCP) v1.0:

| Endpoint | Description |
|----------|-------------|
| `GET /api/mcp/latex/chart/example` | Get executable chart examples |
| `GET /api/mcp/latex/chart/command` | Query command specifications |
| `GET /api/mcp/latex/chart/feedback` | Get warnings and best practices |
| `GET /api/mcp/latex/chart/search` | Universal knowledge search |

## 💻 Local Development

### Prerequisites
- Python 3.8+
- pip

### Setup

```bash
# Clone repository
git clone https://github.com/yourusername/latex-mcp-knowledge.git
cd latex-mcp-knowledge

# Install dependencies
pip install flask flask-cors

# Run API server
python scripts/mcp_server.py

# Test
curl http://localhost:3000/mcp/health
```

### Regenerate Knowledge Base

```bash
# Extract from manuals
python scripts/extract_tex_content.py

# Structure the data
python scripts/structure_knowledge.py
```

## 🌐 Deployment Options

### Option 1: Mintlify (Recommended)

1. Push to GitHub
2. Connect to [Mintlify](https://mintlify.com)
3. Deploy automatically

### Option 2: Vercel

```bash
npm install -g vercel
vercel --prod
```

### Option 3: Docker

```bash
docker build -t latex-mcp-api .
docker run -p 3000:3000 latex-mcp-api
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## 📊 Example Usage

### Python

```python
import requests

# Get line chart examples
response = requests.get(
    "https://your-domain.mintlify.app/mcp/api/mcp/latex/chart/example",
    params={"chart_type": "line_chart", "limit": 5}
)

examples = response.json()["data"]
for example in examples:
    print(example["content"]["code"])
```

### JavaScript

```javascript
const response = await fetch(
  'https://your-domain.mintlify.app/mcp/api/mcp/latex/chart/example?chart_type=line_chart&limit=5'
);

const { data } = await response.json();
data.forEach(example => console.log(example.content.code));
```

### cURL

```bash
# Get 3D plot examples
curl "https://your-domain.mintlify.app/mcp/api/mcp/latex/chart/example?chart_type=3d_plot&limit=3" | jq '.data[].content.code'
```

## 🎯 Use Cases

- **AI/ML**: Train models on authoritative LaTeX examples
- **Code Generation**: Build LaTeX chart generation agents
- **Documentation**: Reference official TikZ/PGFPlots documentation
- **Education**: Learn LaTeX charting with real examples
- **Research**: Find correct syntax for scientific plots

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) for details

## 🙏 Acknowledgments

Knowledge extracted from:
- [TikZ/PGF Manual](https://pgf-tikz.github.io/) by Till Tantau
- [PGFPlots Manual](https://ctan.org/pkg/pgfplots) by Christian Feuersänger

## 📞 Support

- 📖 [Documentation](mintlify-docs/)
- 🐛 [Issue Tracker](https://github.com/yourusername/latex-mcp-knowledge/issues)
- 💬 [Discussions](https://github.com/yourusername/latex-mcp-knowledge/discussions)

---

**Built with** ❤️ **using MCP Protocol**

[View Documentation](https://your-username.mintlify.app) • [API Reference](https://your-username.mintlify.app/api)
