# Mintlify 配置文件说明

## 问题：为什么有两个 mint.json？

### 当前项目结构
```
latex-mcp-knowledge/
├── mint.json                          ← 根目录配置
├── mintlify-docs/
│   ├── mint.json                      ← 子目录配置
│   ├── introduction.mdx
│   ├── browse/
│   └── ...其他 MDX 文件
```

## Mintlify 的配置文件读取逻辑

### 情况1：子目录部署（推荐）
如果 Mintlify 配置为从 `mintlify-docs/` 目录部署：
- **读取**: `mintlify-docs/mint.json`
- **路径**: 相对于 `mintlify-docs/` 目录
- **示例**: `"pages": ["introduction", "browse/index"]`
- **所有 MDX 文件**: 必须在 `mintlify-docs/` 目录下

### 情况2：根目录部署
如果 Mintlify 配置为从根目录部署：
- **读取**: `./mint.json`（根目录）
- **路径**: 必须包含子目录前缀
- **示例**: `"pages": ["mintlify-docs/introduction", "mintlify-docs/browse/index"]`
- **所有 MDX 文件**: 在 `mintlify-docs/` 目录下

## 当前问题

您的 Mintlify 部署 URL 是 `https://baidu-a3d5180c.mintlify.app/`

访问 `https://baidu-a3d5180c.mintlify.app/mintlify-docs/introduction` 说明：
- Mintlify **可能**配置为根目录部署
- 但路径中包含 `/mintlify-docs/` 前缀

## 需要确认的信息

在 Mintlify Dashboard 中检查：
1. **部署源目录**：是 `/` 还是 `/mintlify-docs`？
2. **构建命令**：是否指定了 docs 目录？

## 解决方案

### 方案A：确认为子目录部署（推荐）
如果 Mintlify 设置为从 `mintlify-docs/` 部署：
- 删除根目录的 `mint.json`
- 只保留 `mintlify-docs/mint.json`
- 访问 URL：`https://baidu-a3d5180c.mintlify.app/introduction`

### 方案B：确认为根目录部署
如果 Mintlify 设置为从根目录部署：
- 保留根目录的 `mint.json`（已更新为 V2）
- 访问 URL：`https://baidu-a3d5180c.mintlify.app/mintlify-docs/introduction`

## 建议的检查步骤

1. 登录 Mintlify Dashboard
2. 查看项目设置 → Build Settings
3. 确认 "Docs Directory" 配置
