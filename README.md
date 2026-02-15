# LaTeX Graphics Knowledge Base

A comprehensive Mintlify-powered documentation site containing 6,812 structured knowledge items from 6 major LaTeX graphics packages, optimized for AI model consumption via Model Context Protocol (MCP).

## 📚 Included Packages

| Package | Items | Domain |
|---------|-------|--------|
| **tikz-pgf** | 3,696 | General-purpose graphics engine |
| **pgfplots** | 1,472 | Data visualization & scientific plots |
| **circuitikz** | 816 | Electronic circuit diagrams |
| **tkz-euclide** | 467 | Euclidean geometry |
| **chemfig** | 290 | Chemical structure formulas |
| **tikz-network** | 71 | Network & graph visualization |

## 🎯 Purpose

This project enables AI models (Claude, GPT, Cursor, etc.) to access LaTeX graphics knowledge through MCP, allowing them to:

- Search 6,812+ examples and specifications
- Generate accurate LaTeX graphics code
- Reference package documentation in context
- Provide executable examples with proper syntax

## 🔌 Using the MCP Server

Mintlify automatically provides an MCP server at `/mcp` endpoint. Connect to it from your AI tools:

### Quick Connect

**URL**: `https://baidu-a3d5180c.mintlify.app/mcp`

### Supported Clients

- **Claude Desktop**: Add MCP server URL in settings
- **Cursor**: Click "Connect to Cursor" in the docs contextual menu
- **VS Code**: Click "Connect to VS Code" in the docs contextual menu
- **Claude Code**: Use `npx add-mcp <server-url>`

### MCP Search Examples

```json
{
  "tool": "search_latex_knowledge",
  "arguments": {
    "query": "circuit diagram resistor",
    "package": "circuitikz"
  }
}
```

```json
{
  "tool": "search_latex_knowledge",
  "arguments": {
    "query": "bar chart pgfplots",
    "category": "charts"
  }
}
```

## 📖 Documentation Structure

```
mintlify-docs/
├── introduction.mdx          # Getting started
├── knowledge/                # Package-specific guides
│   ├── tikz-pgf.mdx
│   ├── pgfplots.mdx
│   ├── circuitikz.mdx
│   ├── tkz-euclide.mdx
│   ├── chemfig.mdx
│   └── tikz-network.mdx
├── charts/                   # Chart type guides
│   ├── line-chart.mdx
│   ├── bar-chart.mdx
│   ├── circuit.mdx
│   ├── geometry.mdx
│   └── ...
└── browse/                   # Browse all 6,812 items
    ├── all/                  # All items (145 pages)
    ├── by-type/              # Grouped by type
    ├── by-package/           # Grouped by package
    └── by-chart-type/        # Grouped by chart type
```

## 🛠️ Development

### Scripts

- `extract_tex_content_v2.py` - Extract knowledge from LaTeX manuals
- `generate_browse_pages.py` - Generate MDX browse pages
- `structure_knowledge.py` - Structure extracted knowledge

### Knowledge Base

All structured data is in `knowledge-base/`:

- Individual package JSON files
- `latex-all-knowledge-raw.json` - Combined knowledge base
- `extraction-stats.json` - Statistics

### MCP Configuration

The project uses Mintlify's built-in MCP server. Configuration in `mintlify-docs/mint.json`:

```json
{
  "seo": {
    "indexing": "all"
  },
  "contextualMenu": {
    "items": ["mcp", "add-mcp", "cursor", "vscode"]
  }
}
```

## 📊 Knowledge Statistics

- **Total Items**: 6,812
- **Executable Examples**: 5,325 (78.2%)
- **Command Specs**: 1,103 (16.2%)
- **Component Defs**: 315 (4.6%)
- **Coverage**: 100% extraction success

## 🚀 Deployment

The documentation is deployed on Mintlify:

- **Live URL**: https://baidu-a3d5180c.mintlify.app/mintlify-docs/introduction
- **MCP Server**: https://baidu-a3d5180c.mintlify.app/mcp
- **GitHub Repo**: https://github.com/inker-yyk/latex-mcp-knowledge

Changes pushed to the GitHub repository are automatically deployed by Mintlify.

## 📝 Additional Documentation

- [EXTRACTION_METHODS.md](EXTRACTION_METHODS.md) - How knowledge is extracted
- [MANUAL_CLASSIFICATION.md](MANUAL_CLASSIFICATION.md) - Package classification
- [VALIDATION_REPORT.md](VALIDATION_REPORT.md) - Quality validation
- [UPGRADE_REPORT.md](UPGRADE_REPORT.md) - V1 → V2 changes
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Detailed project overview

## 🤝 Contributing

To add more packages or improve extraction:

1. Add new manual PDFs to source directory
2. Update `extract_tex_content_v2.py` with new extractors
3. Run extraction and generation scripts
4. Update `mint.json` navigation
5. Push to GitHub for automatic deployment

## 📄 License

This project contains knowledge extracted from open-source LaTeX packages. Refer to individual package licenses for usage terms.

---

**Powered by [Mintlify](https://mintlify.com) • Built for AI integration via MCP**
