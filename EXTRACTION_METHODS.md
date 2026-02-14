# LaTeX 手册信息提取方法详解

## 📚 概述

本文档详细说明了如何从6个不同的LaTeX手册中提取结构化知识。每个手册都有独特的文档结构和代码组织方式，需要定制化的提取策略。

---

## 🎯 通用提取原则

### 1. 知识类型分类
所有手册提取的知识统一分为以下类型：

```python
KNOWLEDGE_TYPES = {
    "command": "命令定义",
    "environment": "环境定义",
    "executable_example": "可执行示例",
    "key_value": "键值对配置",
    "component": "组件定义（circuitikz专用）",
    "feedback": "警告和最佳实践"
}
```

### 2. 通用元数据结构

```json
{
  "id": "unique_hash_id",
  "type": "command|environment|executable_example|...",
  "macro_package": "package_name",
  "name": "command_or_component_name",
  "description": "简短描述",
  "syntax": "命令语法",
  "parameters": {
    "required": ["arg1", "arg2"],
    "optional": ["opt1", "opt2"]
  },
  "examples": ["example code"],
  "source_file": "path/to/file.tex",
  "line_number": 123,
  "category": "specific_category",
  "tags": ["tag1", "tag2"]
}
```

---

## 🟢 一级手册提取方法

## 1. TIKZ-NETWORK 提取方法

### 手册特征
- **文档环境**: docspec, docspecdef
- **命令定义**: `\doccmddef{CommandName}`
- **代码示例**: lstlisting环境
- **图示**: tikzpicture (含边注marginfigure)

### 提取策略

#### Step 1: 章节结构提取
```python
import re

def extract_chapters(content):
    """提取章节结构"""
    pattern = r'\\chapter\{([^}]+)\}'
    chapters = re.findall(pattern, content)

    section_pattern = r'\\section\{([^}]+)\}'
    sections = re.findall(section_pattern, content)

    return {
        "chapters": chapters,
        "sections": sections
    }
```

#### Step 2: 命令定义提取
```python
def extract_commands(content):
    """提取命令定义"""
    items = []

    # 匹配 \doccmddef{CommandName}
    pattern = r'\\doccmddef\{([^}]+)\}'
    matches = re.finditer(pattern, content)

    for match in matches:
        cmd_name = match.group(1)

        # 查找后续的 docspecdef 环境
        start_pos = match.end()
        docspec_pattern = r'\\begin\{docspecdef\}(.*?)\\end\{docspecdef\}'
        docspec_match = re.search(docspec_pattern, content[start_pos:], re.DOTALL)

        if docspec_match:
            syntax = docspec_match.group(1)

            items.append({
                "type": "command",
                "macro_package": "tikz-network",
                "name": cmd_name,
                "syntax": extract_syntax(syntax),
                "source_file": "tikz-network.tex"
            })

    return items

def extract_syntax(syntax_text):
    """从docspec中提取语法"""
    # 提取 \docopt{} 和 \docarg{}
    opts = re.findall(r'\\docopt\{([^}]+)\}', syntax_text)
    args = re.findall(r'\\docarg\{([^}]+)\}', syntax_text)

    return {
        "optional": opts,
        "required": args
    }
```

#### Step 3: 选项表格提取
```python
def extract_option_tables(content):
    """提取选项表格"""
    items = []

    # 查找 tabular 环境
    pattern = r'\\begin\{tabular\}\{([^}]+)\}(.*?)\\end\{tabular\}'
    matches = re.finditer(pattern, content, re.DOTALL)

    for match in matches:
        table_content = match.group(2)

        # 解析表格行
        rows = table_content.split('\\\\')
        for row in rows[1:]:  # 跳过表头
            cells = row.split('&')
            if len(cells) >= 3:
                option_name = cells[0].strip()
                default_value = cells[1].strip()
                description = cells[2].strip()

                items.append({
                    "type": "key_value",
                    "macro_package": "tikz-network",
                    "key": option_name,
                    "default": default_value,
                    "description": description
                })

    return items
```

#### Step 4: 代码示例提取
```python
def extract_examples(content):
    """提取lstlisting示例"""
    items = []

    pattern = r'\\begin\{lstlisting\}(.*?)\\end\{lstlisting\}'
    matches = re.finditer(pattern, content, re.DOTALL)

    for idx, match in enumerate(matches):
        code = match.group(1).strip()

        # 检测是否包含tikz-network命令
        if '\\Vertex' in code or '\\Edge' in code:
            items.append({
                "type": "executable_example",
                "macro_package": "tikz-network",
                "code": code,
                "chart_type": "network_graph",
                "id": f"tikz-network-ex-{idx}"
            })

    return items
```

### 完整提取流程
```python
class TikzNetworkExtractor:
    def __init__(self, manual_path):
        self.manual_path = manual_path

    def process(self):
        with open(self.manual_path, 'r', encoding='utf-8') as f:
            content = f.read()

        knowledge_items = []
        knowledge_items.extend(extract_chapters(content))
        knowledge_items.extend(extract_commands(content))
        knowledge_items.extend(extract_option_tables(content))
        knowledge_items.extend(extract_examples(content))

        return knowledge_items
```

---

## 2. CHEMFIG 提取方法

### 手册特征
- **自定义宏**: `\exemple`, `\exemple*`
- **分隔符**: 使用 `/` 或 `|` 分隔代码
- **键值系统**: `\CFkey{}`, `\CFkv{}{}`
- **特殊语法**: catcode技巧

### 提取策略

#### Step 1: 识别\exemple宏
```python
def extract_chemfig_examples(content):
    """提取chemfig的\exemple宏"""
    items = []

    # 匹配 \exemple{title}/code/
    pattern = r'\\exemple(\*)?(?:\[([^\]]*)\])?\{([^/\|]*)\}([/\|])(.*?)\4'
    matches = re.finditer(pattern, content, re.DOTALL)

    for idx, match in enumerate(matches):
        is_starred = match.group(1) is not None
        ratio = match.group(2) or "65"
        title = match.group(3)
        delimiter = match.group(4)
        code = match.group(5).strip()

        items.append({
            "type": "executable_example",
            "macro_package": "chemfig",
            "title": title,
            "code": code,
            "display_mode": "full_width" if is_starred else "split",
            "ratio": ratio,
            "chart_type": "chemical_structure",
            "id": f"chemfig-ex-{idx}"
        })

    return items
```

#### Step 2: 提取键值对文档
```python
def extract_chemfig_keys(content):
    """提取chemfig的键值对文档"""
    items = []

    # 提取 \CFkey{keyname}
    key_pattern = r'\\CFkey\{([^}]+)\}'
    keys = re.finditer(key_pattern, content)

    for match in keys:
        key_name = match.group(1)

        # 在附近查找描述文本
        start = match.end()
        description = extract_nearby_text(content, start, 200)

        items.append({
            "type": "key_value",
            "macro_package": "chemfig",
            "key": key_name,
            "description": description
        })

    # 提取 \CFkv{key}{value}
    kv_pattern = r'\\CFkv\{([^}]+)\}\{([^}]+)\}'
    kvs = re.finditer(kv_pattern, content)

    for match in kvs:
        key = match.group(1)
        value = match.group(2)

        items.append({
            "type": "key_value",
            "macro_package": "chemfig",
            "key": key,
            "default": value
        })

    return items
```

#### Step 3: 提取命令文档
```python
def extract_chemfig_commands(content):
    """提取chemfig命令"""
    items = []

    # chemfig的主要命令
    main_commands = [
        r'\\chemfig',
        r'\\setchemfig',
        r'\\schemename',
        r'\\chemrel',
        r'\\setlewis',
        r'\\lewis'
    ]

    for cmd_pattern in main_commands:
        # 在文档中查找命令首次出现
        pattern = f'{cmd_pattern}(?:\\[([^\\]]*)])?(?:\\{{([^}}]*)\\}})?'
        matches = re.finditer(pattern, content)

        for match in matches:
            cmd_name = cmd_pattern.replace('\\\\', '')
            opt_args = match.group(1)
            req_args = match.group(2)

            items.append({
                "type": "command",
                "macro_package": "chemfig",
                "name": cmd_name,
                "optional_args": opt_args,
                "required_args": req_args
            })
            break  # 只取第一次出现

    return items
```

#### Step 4: 处理特殊语法
```python
def extract_chemfig_syntax(content):
    """提取chemfig的化学语法规则"""
    items = []

    # 化学键类型
    bond_types = {
        '-': 'single bond',
        '=': 'double bond',
        '~': 'triple bond',
        '>': 'right bond',
        '<': 'left bond',
        '>:': 'Cram bond (front)',
        '<:': 'Cram bond (back)'
    }

    for symbol, description in bond_types.items():
        items.append({
            "type": "syntax_rule",
            "macro_package": "chemfig",
            "symbol": symbol,
            "description": description,
            "category": "bond_type"
        })

    return items
```

### 完整提取流程
```python
class ChemfigExtractor:
    def __init__(self, manual_dir):
        self.manual_dir = Path(manual_dir)

    def process(self):
        main_file = self.manual_dir / "chemfig-en.tex"

        with open(main_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        items = []
        items.extend(extract_chemfig_examples(content))
        items.extend(extract_chemfig_keys(content))
        items.extend(extract_chemfig_commands(content))
        items.extend(extract_chemfig_syntax(content))

        return items
```

---

## 🟡 二级手册提取方法

## 3. CIRCUITIKZ 提取方法

### 手册特征
- **组件描述**: `\circuitdesc`, `\circuitdescbip`
- **示例环境**: LTXexample (showexpl包)
- **代码展示**: lstlisting
- **自定义工具**: ctikzmanutils.sty

### 提取策略

#### Step 1: 组件定义提取
```python
def extract_circuitikz_components(content):
    """提取circuitikz组件定义"""
    items = []

    # 匹配 \circuitdesc*{name}{description}{}(anchors)
    pattern = r'\\circuitdesc(\*)?(?:\[([^\]]*)\])?\{([^}]+)\}\{([^}]+)\}\{([^}]*)\}\(([^)]+)\)'
    matches = re.finditer(pattern, content)

    for match in matches:
        is_fillable = match.group(1) is not None
        options = match.group(2)
        component_name = match.group(3)
        description = match.group(4)
        aliases = match.group(5)
        anchors_spec = match.group(6)

        # 解析锚点
        anchors = parse_anchors(anchors_spec)

        items.append({
            "type": "component",
            "macro_package": "circuitikz",
            "component_type": "node",
            "name": component_name,
            "description": description,
            "aliases": aliases.split(',') if aliases else [],
            "fillable": is_fillable,
            "anchors": anchors
        })

    # 匹配 \circuitdescbip{name}{description}{aliases}
    bipolar_pattern = r'\\circuitdescbip(?:\[([^\]]*)\])?\{([^}]+)\}\{([^}]+)\}\{([^}]*)\}'
    bip_matches = re.finditer(bipolar_pattern, content)

    for match in bip_matches:
        options = match.group(1)
        component_name = match.group(2)
        description = match.group(3)
        aliases = match.group(4)

        items.append({
            "type": "component",
            "macro_package": "circuitikz",
            "component_type": "bipole",
            "name": component_name,
            "description": description,
            "aliases": aliases.split(',') if aliases else []
        })

    return items

def parse_anchors(anchors_spec):
    """解析锚点规范: name/angle/distance"""
    anchors = []
    for anchor_str in anchors_spec.split(','):
        parts = anchor_str.strip().split('/')
        if len(parts) >= 3:
            anchors.append({
                "name": parts[0].strip(),
                "angle": parts[1].strip(),
                "distance": parts[2].strip()
            })
    return anchors
```

#### Step 2: LTXexample环境提取
```python
def extract_ltxexamples(content):
    """提取LTXexample环境"""
    items = []

    pattern = r'\\begin\{LTXexample\}(?:\[([^\]]*)\])?(.*?)\\end\{LTXexample\}'
    matches = re.finditer(pattern, content, re.DOTALL)

    for idx, match in enumerate(matches):
        options = match.group(1) or ""
        code = match.group(2).strip()

        # 解析选项
        opts = parse_ltx_options(options)

        items.append({
            "type": "executable_example",
            "macro_package": "circuitikz",
            "code": code,
            "chart_type": "circuit",
            "display_options": opts,
            "id": f"circuitikz-ex-{idx}"
        })

    return items

def parse_ltx_options(options_str):
    """解析LTXexample选项"""
    opts = {}
    if not options_str:
        return opts

    # varwidth, pos, preset等
    for opt in options_str.split(','):
        if '=' in opt:
            key, value = opt.split('=', 1)
            opts[key.strip()] = value.strip()
        else:
            opts[opt.strip()] = True

    return opts
```

#### Step 3: 配置键提取
```python
def extract_circuitikz_keys(content):
    """提取circuitikz配置键"""
    items = []

    # 查找 \ctikzset{key=value} 或 \tikzset{key=value}
    set_patterns = [
        r'\\ctikzset\{([^}]+)\}',
        r'\\tikzset\{([^}]+)\}'
    ]

    for pattern in set_patterns:
        matches = re.finditer(pattern, content)
        for match in matches:
            kv_content = match.group(1)

            # 解析键值对
            kvs = parse_key_values(kv_content)
            for key, value in kvs.items():
                items.append({
                    "type": "key_value",
                    "macro_package": "circuitikz",
                    "key": key,
                    "default": value
                })

    return items
```

#### Step 4: 选项表格提取
```python
def extract_component_options(content):
    """提取组件选项表格"""
    items = []

    # 在每个组件描述后，通常有选项表格
    # 查找 tabular 环境
    pattern = r'\\begin\{tabular\}\{[^}]+\}(.*?)\\end\{tabular\}'
    matches = re.finditer(pattern, content, re.DOTALL)

    for match in matches:
        table_content = match.group(1)
        rows = parse_booktabs_table(table_content)

        for row in rows:
            if len(row) >= 2:
                items.append({
                    "type": "component_option",
                    "macro_package": "circuitikz",
                    "option": row[0],
                    "description": row[1],
                    "default": row[2] if len(row) > 2 else None
                })

    return items

def parse_booktabs_table(table_content):
    """解析booktabs表格"""
    rows = []
    lines = table_content.split('\\\\')

    for line in lines:
        # 跳过 \toprule, \midrule, \bottomrule
        if 'rule' in line:
            continue

        cells = [cell.strip() for cell in line.split('&')]
        if cells and cells[0]:
            rows.append(cells)

    return rows[1:]  # 跳过表头
```

### 完整提取流程
```python
class CircuitikzExtractor:
    def __init__(self, manual_dir):
        self.manual_dir = Path(manual_dir)

    def process(self):
        main_file = self.manual_dir / "circuitikzmanual.tex"

        with open(main_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        items = []
        items.extend(extract_circuitikz_components(content))
        items.extend(extract_ltxexamples(content))
        items.extend(extract_circuitikz_keys(content))
        items.extend(extract_component_options(content))

        return items
```

---

## 🔴 三级手册提取方法

## 4. TKZ-EUCLIDE 提取方法

### 手册特征
- **多文件结构**: 32个tex文件
- **自定义环境**: NewMacroBox
- **示例环境**: tkzexample
- **文档类**: tkz-doc

### 提取策略

#### Step 1: 处理多文件结构
```python
class TkzEuclideExtractor:
    def __init__(self, manual_dir):
        self.manual_dir = Path(manual_dir)
        self.main_file = self.manual_dir / "TKZdoc-euclide-main.tex"

    def get_file_order(self):
        """从main文件获取输入顺序"""
        with open(self.main_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 提取 \input{filename}
        pattern = r'\\input\{([^}]+)\}'
        matches = re.findall(pattern, content)

        return [self.manual_dir / f"{name}.tex" for name in matches]

    def process(self):
        """按顺序处理所有文件"""
        files = self.get_file_order()
        all_items = []

        for file_path in files:
            if file_path.exists():
                items = self.process_file(file_path)
                all_items.extend(items)

        return all_items
```

#### Step 2: NewMacroBox环境提取
```python
def extract_newmacrobox(content, source_file):
    """提取NewMacroBox环境"""
    items = []

    # 匹配 \begin{NewMacroBox}{commandname}{syntax}
    pattern = r'\\begin\{NewMacroBox\}\{([^}]+)\}\{([^}]+)\}(.*?)\\end\{NewMacroBox\}'
    matches = re.finditer(pattern, content, re.DOTALL)

    for match in matches:
        cmd_name = match.group(1)
        syntax = match.group(2)
        body = match.group(3)

        # 解析syntax中的参数
        params = parse_tkz_syntax(syntax)

        # 提取tabular表格
        tables = extract_tables_from_body(body)

        items.append({
            "type": "command",
            "macro_package": "tkz-euclide",
            "name": cmd_name,
            "syntax": syntax,
            "parameters": params,
            "arguments_table": tables.get("arguments", []),
            "options_table": tables.get("options", []),
            "source_file": str(source_file)
        })

    return items

def parse_tkz_syntax(syntax):
    """解析tkz命令语法"""
    params = {
        "optional": [],
        "required": []
    }

    # \oarg{} - optional argument
    opt_pattern = r'\\oarg\{([^}]+)\}'
    params["optional"] = re.findall(opt_pattern, syntax)

    # \marg{} - mandatory argument
    req_pattern = r'\\marg\{([^}]+)\}'
    params["required"] = re.findall(req_pattern, syntax)

    # \parg{} - parenthesized argument
    paren_pattern = r'\\parg\{([^}]+)\}'
    params["parenthesized"] = re.findall(paren_pattern, syntax)

    return params

def extract_tables_from_body(body):
    """从NewMacroBox body中提取表格"""
    tables = {}

    # 查找包含 "arguments" 的表格
    arg_pattern = r'arguments.*?\\begin\{tabular\}(.*?)\\end\{tabular\}'
    arg_match = re.search(arg_pattern, body, re.DOTALL | re.IGNORECASE)

    if arg_match:
        tables["arguments"] = parse_tkz_table(arg_match.group(1))

    # 查找包含 "options" 的表格
    opt_pattern = r'options.*?\\begin\{tabular\}(.*?)\\end\{tabular\}'
    opt_match = re.search(opt_pattern, body, re.DOTALL | re.IGNORECASE)

    if opt_match:
        tables["options"] = parse_tkz_table(opt_match.group(1))

    return tables

def parse_tkz_table(table_content):
    """解析tkz表格（使用TAline/TOline宏）"""
    rows = []

    # \TAline{name}{default}{description}
    ta_pattern = r'\\TAline\{([^}]*)\}\{([^}]*)\}\{([^}]*)\}'
    ta_matches = re.finditer(ta_pattern, table_content)

    for match in ta_matches:
        rows.append({
            "name": match.group(1),
            "default": match.group(2),
            "description": match.group(3),
            "type": "argument"
        })

    # \TOline{name}{default}{description}
    to_pattern = r'\\TOline\{([^}]*)\}\{([^}]*)\}\{([^}]*)\}'
    to_matches = re.finditer(to_pattern, table_content)

    for match in to_matches:
        rows.append({
            "name": match.group(1),
            "default": match.group(2),
            "description": match.group(3),
            "type": "option"
        })

    return rows
```

#### Step 3: tkzexample环境提取
```python
def extract_tkzexamples(content, source_file):
    """提取tkzexample环境"""
    items = []

    pattern = r'\\begin\{tkzexample\}(?:\[([^\]]*)\])?(.*?)\\end\{tkzexample\}'
    matches = re.finditer(pattern, content, re.DOTALL)

    for idx, match in enumerate(matches):
        options = match.group(1) or ""
        code = match.group(2).strip()

        # 解析选项
        opts = parse_tkz_options(options)

        items.append({
            "type": "executable_example",
            "macro_package": "tkz-euclide",
            "code": code,
            "chart_type": "geometry",
            "display_options": opts,
            "source_file": str(source_file),
            "id": f"tkz-ex-{source_file.stem}-{idx}"
        })

    return items

def parse_tkz_options(options_str):
    """解析tkzexample选项"""
    opts = {}
    if not options_str:
        return opts

    # 常见选项: latex=7cm, small, vbox, code only
    for opt in options_str.split(','):
        opt = opt.strip()
        if '=' in opt:
            key, value = opt.split('=', 1)
            opts[key.strip()] = value.strip()
        else:
            opts[opt] = True

    return opts
```

#### Step 4: 命令分类
```python
def categorize_tkz_commands(items):
    """根据命令前缀分类"""
    categories = {
        "tkzDef": "definition",
        "tkzGet": "retrieval",
        "tkzCalc": "calculation",
        "tkzDraw": "drawing",
        "tkzMark": "marking",
        "tkzLabel": "labeling",
        "tkzFill": "filling",
        "tkzClip": "clipping",
        "tkzSetUp": "setup"
    }

    for item in items:
        if item["type"] == "command":
            cmd_name = item["name"]
            for prefix, category in categories.items():
                if cmd_name.startswith(prefix):
                    item["category"] = category
                    break

    return items
```

### 完整提取流程
```python
class TkzEuclideExtractor:
    def process_file(self, file_path):
        """处理单个文件"""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        items = []
        items.extend(extract_newmacrobox(content, file_path))
        items.extend(extract_tkzexamples(content, file_path))

        # 分类
        items = categorize_tkz_commands(items)

        return items
```

---

## 🛠️ 辅助工具函数

### 通用LaTeX解析
```python
def extract_nearby_text(content, start_pos, max_length=200):
    """提取附近的纯文本描述"""
    text = content[start_pos:start_pos+max_length]

    # 移除LaTeX命令
    text = re.sub(r'\\[a-zA-Z]+', '', text)
    # 移除花括号
    text = re.sub(r'[{}]', '', text)
    # 规范化空白
    text = ' '.join(text.split())

    return text

def clean_latex_text(text):
    """清理LaTeX文本"""
    # 移除注释
    text = re.sub(r'%.*$', '', text, flags=re.MULTILINE)
    # 移除多余空白
    text = ' '.join(text.split())
    return text

def parse_key_values(kv_string):
    """解析键值对字符串"""
    kvs = {}
    # 简单的键值对解析（不处理嵌套）
    pairs = kv_string.split(',')
    for pair in pairs:
        if '=' in pair:
            key, value = pair.split('=', 1)
            kvs[key.strip()] = value.strip()
    return kvs
```

### ID生成
```python
import hashlib

def generate_id(base_string):
    """生成唯一ID"""
    return hashlib.md5(base_string.encode()).hexdigest()[:12]
```

---

## 📊 质量评分系统

### 示例质量评分
```python
def score_example(example_item):
    """为示例评分"""
    score = 0

    # 代码长度合理
    code_length = len(example_item["code"])
    if 50 < code_length < 500:
        score += 0.3

    # 有注释
    if '%' in example_item["code"]:
        score += 0.2

    # 结构完整
    if '\\begin{tikzpicture}' in example_item["code"] and \
       '\\end{tikzpicture}' in example_item["code"]:
        score += 0.3

    # 不太复杂
    if example_item["code"].count('\\') < 20:
        score += 0.2

    return min(score, 1.0)
```

---

## 🔧 统一接口

### 提取器工厂
```python
class ExtractorFactory:
    @staticmethod
    def create(package_name, manual_dir):
        extractors = {
            "tikz-network": TikzNetworkExtractor,
            "chemfig": ChemfigExtractor,
            "circuitikz": CircuitikzExtractor,
            "tkz-euclide": TkzEuclideExtractor
        }

        extractor_class = extractors.get(package_name)
        if extractor_class:
            return extractor_class(manual_dir)
        else:
            raise ValueError(f"Unknown package: {package_name}")
```

### 批量处理
```python
def process_all_manuals(base_dir):
    """处理所有手册"""
    packages = [
        "tikz-network",
        "chemfig",
        "circuitikz",
        "tkz-euclide"
    ]

    all_knowledge = []

    for package in packages:
        manual_dir = Path(base_dir) / f"{package}-manual"
        extractor = ExtractorFactory.create(package, manual_dir)

        items = extractor.process()
        all_knowledge.extend(items)

        print(f"Processed {package}: {len(items)} items")

    return all_knowledge
```

---

**文档创建日期**: 2025-02-14
**覆盖手册**: 6个LaTeX宏包手册
**提取类型**: 命令、环境、示例、键值对、组件
