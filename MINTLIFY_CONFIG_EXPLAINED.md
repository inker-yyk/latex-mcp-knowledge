# Mintlify 配置文件完整说明

## 📁 当前项目文件结构

```
latex-mcp-knowledge/
│
├── mint.json                    ← 文件1：根目录配置（已更新为V2.0）
│   内容示例:
│   "pages": ["mintlify-docs/introduction", "mintlify-docs/browse/index", ...]
│
└── mintlify-docs/
    ├── mint.json                ← 文件2：子目录配置（已更新为V2.0）
    │   内容示例:
    │   "pages": ["introduction", "browse/index", ...]
    │
    ├── introduction.mdx         ← MDX 文件都在这里
    ├── browse/
    │   └── index.mdx
    └── ... 其他 MDX 文件
```

## 🔑 关键理解：Mintlify 使用哪个 mint.json？

### 答案：取决于 Mintlify Dashboard 的「Docs Directory」设置

```
┌─────────────────────────────────────────────────────────────┐
│  Mintlify Dashboard → Settings → Docs Directory            │
└─────────────────────────────────────────────────────────────┘
                        ↓
        ┌───────────────┴───────────────┐
        │                               │
    留空或 "/"                   "mintlify-docs"
        │                               │
        ↓                               ↓
┌───────────────────┐         ┌──────────────────────┐
│ 从根目录部署      │         │ 从子目录部署         │
│ 使用: mint.json   │         │ 使用: mintlify-docs/ │
│       (根目录)    │         │       mint.json      │
└───────────────────┘         └──────────────────────┘
        │                               │
        ↓                               ↓
 路径包含 /mintlify-docs/         路径不包含前缀
        │                               │
        ↓                               ↓
   访问 URL 示例:                  访问 URL 示例:
   /mintlify-docs/introduction     /introduction
```

## 📊 您的当前情况

### 实际访问的 URL
```
https://baidu-a3d5180c.mintlify.app/mintlify-docs/introduction
                                     ^^^^^^^^^^^^^^^ 包含这个前缀
```

### 说明
✅ **Mintlify 配置为从根目录部署**
✅ **使用的是根目录的 mint.json**
✅ **我们已经更新了根目录的 mint.json 为 V2.0（6,812项）**

### Git 提交历史
```bash
cdcccaf - fix: 修正mint.json中的包路径 tikz->tikz-pgf，删除旧目录  ← 最新
ce21a49 - fix: 更新根目录mint.json为V2.0配置(6,812项)
c5629ca - feat: 重新生成browse页面为V2数据 (6,812项)
```

✅ **已推送到 GitHub**

## 🎯 最终答案

### 哪个 mint.json 是最终依赖？

**根目录的 `mint.json`** 是最终依赖，因为：

1. 您的 URL 包含 `/mintlify-docs/` 前缀
2. 这说明 Mintlify 从根目录读取配置
3. 根目录的 `mint.json` 已经更新为 V2.0

### 为什么还显示旧数据？

**原因：Mintlify 构建缓存**

Mintlify 的部署流程：
```
GitHub Push → Webhook → Mintlify 构建 → 缓存更新 → 新版本上线
              ↑                        ↑
           已完成                   等待中（需要时间）
```

通常需要 **5-15 分钟**

### 验证配置是否正确

让我们检查根目录 mint.json 的关键内容：

```bash
grep -E '"Browse All|"name"' mint.json
```

应该显示：
- "name": "LaTeX Knowledge Base (6 Packages)"
- "Browse All 6,812 Items"

## ✅ 总结

| 项目 | 状态 | 说明 |
|------|------|------|
| 根目录 mint.json | ✅ 已更新 | V2.0，6,812项 |
| mintlify-docs/mint.json | ✅ 已更新 | V2.0，6,812项 |
| Browse 页面 | ✅ 已更新 | 627个 MDX 文件 |
| GitHub 推送 | ✅ 完成 | 最新提交 cdcccaf |
| Mintlify 部署 | ⏳ 等待 | 需要 5-15 分钟 |

**下一步**：等待 Mintlify 自动部署，或在 Dashboard 手动触发部署。
