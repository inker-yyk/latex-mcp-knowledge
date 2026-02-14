# Mintlify 文档更新说明

## ⚠️ 重要：Browse 页面需要重新生成

### 当前状态
- ✅ `introduction.mdx` - 已更新为V2.0（6,812项）
- ✅ `mint.json` - 已更新导航，添加新宏包
- ✅ `quickstart.mdx` - 已更新为5,325个示例
- ✅ `api/overview.mdx` - 已更新
- ⚠️ `browse/` 目录 - **包含V1数据（5,171项），需要重新生成**

### 需要重新生成的文件

`browse/` 目录下的所有文件都是通过脚本自动生成的，基于V1的知识库数据：

```
mintlify-docs/browse/
├── index.mdx                     ⚠️ 显示5,171项
├── all/page-*.mdx                ⚠️ 104个页面，基于V1数据
├── by-type/*/page-*.mdx          ⚠️ 按类型浏览
├── by-chart-type/*/page-*.mdx    ⚠️ 按图表类型
└── by-package/*/page-*.mdx       ⚠️ 仅tikz和pgfplots
```

### 解决方案

需要运行生成脚本重新创建这些页面：

```bash
# 使用V2的知识库数据重新生成browse页面
python scripts/generate_browse_pages.py
```

**注意**：
1. 脚本需要更新以支持6个宏包
2. 新的browse页面将显示6,812项
3. 需要添加4个新宏包的浏览页面：
   - circuitikz (816项)
   - tkz-euclide (467项)
   - chemfig (290项)
   - tikz-network (71项)

### 临时方案

如果暂时不想重新生成，可以：
1. 删除 `browse/` 目录
2. 从 `mint.json` 中移除相关导航
3. 用户将看不到browse功能，但其他功能正常

### 推荐做法

1. 更新 `generate_browse_pages.py` 脚本
2. 使用 `latex-all-knowledge-raw.json` 作为数据源
3. 重新生成所有browse页面
4. 提交新生成的页面到git

---

**创建日期**: 2025-02-14
**状态**: 待处理
