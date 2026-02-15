#!/usr/bin/env python3
"""
LaTeX 手册内容提取脚本 - 支持所有 19 个手册包
基于 extract_tex_content_v2.py 扩展
"""

import re
import json
import os
from pathlib import Path
from typing import List, Dict, Any
import hashlib
from abc import ABC, abstractmethod


class BaseExtractor(ABC):
    """提取器基类"""

    def __init__(self, manual_dir: str, package_name: str):
        self.manual_dir = Path(manual_dir)
        self.package_name = package_name
        self.knowledge_items = []

    @abstractmethod
    def process(self) -> List[Dict[str, Any]]:
        """处理手册，返回知识项列表"""
        pass

    def _generate_id(self, base: str) -> str:
        """生成唯一 ID"""
        return hashlib.md5(base.encode()).hexdigest()[:12]

    def _clean_text(self, text: str) -> str:
        """清理LaTeX文本"""
        # 移除注释
        text = re.sub(r'%.*$', '', text, flags=re.MULTILINE)
        # 移除LaTeX命令
        text = re.sub(r'\\[a-zA-Z]+\{([^}]*)\}', r'\1', text)
        text = re.sub(r'\\[a-zA-Z]+', '', text)
        # 规范化空白
        text = ' '.join(text.split())
        return text[:500]


class TikzNetworkExtractor(BaseExtractor):
    """tikz-network 提取器"""

    def process(self) -> List[Dict[str, Any]]:
        main_file = self.manual_dir / "tikz-network.tex"
        if not main_file.exists():
            print(f"Warning: {main_file} not found")
            return []

        with open(main_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        items = []
        items.extend(self._extract_commands(content))
        items.extend(self._extract_examples(content))

        return items

    def _extract_commands(self, content: str) -> List[Dict[str, Any]]:
        """提取命令定义"""
        items = []
        pattern = r'\\doccmddef\{([^}]+)\}'
        matches = re.finditer(pattern, content)

        for match in matches:
            cmd_name = match.group(1)
            items.append({
                "type": "command",
                "macro_package": self.package_name,
                "command_name": cmd_name,
                "description": f"Command for {cmd_name}",
                "source_file": "tikz-network.tex",
                "id": self._generate_id(f"cmd_{cmd_name}")
            })

        return items

    def _extract_examples(self, content: str) -> List[Dict[str, Any]]:
        """提取示例"""
        items = []
        pattern = r'\\begin\{lstlisting\}(.*?)\\end\{lstlisting\}'
        matches = re.finditer(pattern, content, re.DOTALL)

        for idx, match in enumerate(matches):
            code = match.group(1).strip()
            if '\\Vertex' in code or '\\Edge' in code:
                items.append({
                    "type": "executable_example",
                    "macro_package": self.package_name,
                    "chart_type": "network",
                    "code": code,
                    "source_file": "tikz-network.tex",
                    "id": self._generate_id(f"example_{idx}")
                })

        return items


class ChemfigExtractor(BaseExtractor):
    """chemfig 提取器"""

    def process(self) -> List[Dict[str, Any]]:
        main_file = self.manual_dir / "chemfig-en.tex"
        if not main_file.exists():
            print(f"Warning: {main_file} not found")
            return []

        with open(main_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        items = []
        items.extend(self._extract_examples(content))
        items.extend(self._extract_keys(content))

        return items

    def _extract_examples(self, content: str) -> List[Dict[str, Any]]:
        """提取\exemple宏"""
        items = []
        pattern = r'\\exemple(\*)?(?:\[([^\]]*)\])?\{([^/\|]*)\}([/\|])(.*?)\4'
        matches = re.finditer(pattern, content, re.DOTALL)

        for idx, match in enumerate(matches):
            title = match.group(3)
            code = match.group(5).strip()

            items.append({
                "type": "executable_example",
                "macro_package": self.package_name,
                "chart_type": "chemistry",
                "title": title,
                "description": title,
                "code": code,
                "source_file": "chemfig-en.tex",
                "id": self._generate_id(f"example_{idx}")
            })

        return items

    def _extract_keys(self, content: str) -> List[Dict[str, Any]]:
        """提取键值对"""
        items = []
        pattern = r'\\CFkey\{([^}]+)\}'
        matches = re.finditer(pattern, content)

        for match in matches:
            key_name = match.group(1)
            items.append({
                "type": "key_value",
                "macro_package": self.package_name,
                "key_name": key_name,
                "description": f"Configuration key: {key_name}",
                "source_file": "chemfig-en.tex",
                "id": self._generate_id(f"key_{key_name}")
            })

        return items


class CircuitikzExtractor(BaseExtractor):
    """circuitikz 提取器"""

    def process(self) -> List[Dict[str, Any]]:
        main_file = self.manual_dir / "circuitikzmanual.tex"
        if not main_file.exists():
            print(f"Warning: {main_file} not found")
            return []

        with open(main_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        items = []
        items.extend(self._extract_components(content))
        items.extend(self._extract_examples(content))

        return items

    def _extract_components(self, content: str) -> List[Dict[str, Any]]:
        """提取组件定义"""
        items = []

        # \circuitdesc{name}{description}
        pattern = r'\\circuitdesc(?:\*)?(?:\[[^\]]*\])?\{([^}]+)\}\{([^}]+)\}'
        matches = re.finditer(pattern, content)

        for match in matches:
            component_name = match.group(1)
            description = match.group(2)

            items.append({
                "type": "component",
                "macro_package": self.package_name,
                "component_name": component_name,
                "description": description,
                "source_file": "circuitikzmanual.tex",
                "id": self._generate_id(f"comp_{component_name}")
            })

        # \circuitdescbip{name}{description}{aliases}
        bip_pattern = r'\\circuitdescbip(?:\[[^\]]*\])?\{([^}]+)\}\{([^}]+)\}\{([^}]*)\}'
        bip_matches = re.finditer(bip_pattern, content)

        for match in bip_matches:
            component_name = match.group(1)
            description = match.group(2)

            items.append({
                "type": "component",
                "macro_package": self.package_name,
                "component_name": component_name,
                "description": description,
                "source_file": "circuitikzmanual.tex",
                "id": self._generate_id(f"comp_{component_name}")
            })

        return items

    def _extract_examples(self, content: str) -> List[Dict[str, Any]]:
        """提取示例"""
        items = []

        # LTXexample环境
        pattern = r'\\begin\{LTXexample\}(?:\[([^\]]*)\])?(.*?)\\end\{LTXexample\}'
        matches = re.finditer(pattern, content, re.DOTALL)

        for idx, match in enumerate(matches):
            code = match.group(2).strip()

            items.append({
                "type": "executable_example",
                "macro_package": self.package_name,
                "chart_type": "circuit",
                "code": code,
                "source_file": "circuitikzmanual.tex",
                "id": self._generate_id(f"example_{idx}")
            })

        return items


class TkzEuclideExtractor(BaseExtractor):
    """tkz-euclide 提取器"""

    def process(self) -> List[Dict[str, Any]]:
        # 获取所有tex文件
        tex_files = list(self.manual_dir.glob("*.tex"))

        items = []
        for tex_file in tex_files:
            with open(tex_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            items.extend(self._extract_commands(content, tex_file))
            items.extend(self._extract_examples(content, tex_file))

        return items

    def _extract_commands(self, content: str, source_file: Path) -> List[Dict[str, Any]]:
        """提取NewMacroBox命令"""
        items = []

        # \begin{NewMacroBox}{commandname}{syntax}
        pattern = r'\\begin\{NewMacroBox\}\{([^}]+)\}\{([^}]+)\}'
        matches = re.finditer(pattern, content)

        for match in matches:
            cmd_name = match.group(1)
            syntax = match.group(2)

            items.append({
                "type": "command",
                "macro_package": self.package_name,
                "command_name": cmd_name,
                "syntax": syntax,
                "description": f"Geometry command: {cmd_name}",
                "source_file": source_file.name,
                "id": self._generate_id(f"cmd_{cmd_name}")
            })

        return items

    def _extract_examples(self, content: str, source_file: Path) -> List[Dict[str, Any]]:
        """提取tkzexample环境"""
        items = []

        pattern = r'\\begin\{tkzexample\}(?:\[([^\]]*)\])?(.*?)\\end\{tkzexample\}'
        matches = re.finditer(pattern, content, re.DOTALL)

        for idx, match in enumerate(matches):
            code = match.group(2).strip()

            items.append({
                "type": "executable_example",
                "macro_package": self.package_name,
                "chart_type": "geometry",
                "code": code,
                "source_file": source_file.name,
                "id": self._generate_id(f"example_{source_file.stem}_{idx}")
            })

        return items


class StandardExtractor(BaseExtractor):
    """标准提取器 (用于tikz-pgf和pgfplots)"""

    def process(self) -> List[Dict[str, Any]]:
        """使用已有的提取逻辑"""
        tex_files = list(self.manual_dir.rglob("*.tex"))

        items = []
        for tex_file in tex_files:
            with open(tex_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            items.extend(self._extract_commands(content, tex_file))
            items.extend(self._extract_environments(content, tex_file))
            items.extend(self._extract_codeexamples(content, tex_file))

        return items

    def _extract_commands(self, content: str, filepath: Path) -> List[Dict[str, Any]]:
        """提取命令定义"""
        items = []
        pattern = r'\\begin\{command\}\{([^}]+)\}(.*?)\\end\{command\}'
        matches = re.finditer(pattern, content, re.DOTALL)

        for match in matches:
            command_name = match.group(1).strip()
            command_body = match.group(2).strip()
            description = self._clean_text(command_body)

            items.append({
                "type": "command",
                "macro_package": self.package_name,
                "command_name": command_name,
                "description": description,
                "source_file": str(filepath.relative_to(self.manual_dir)),
                "id": self._generate_id(f"cmd_{command_name}_{filepath.stem}")
            })

        return items

    def _extract_environments(self, content: str, filepath: Path) -> List[Dict[str, Any]]:
        """提取环境定义"""
        items = []
        pattern = r'\\begin\{environment\}\{([^}]+)\}(.*?)\\end\{environment\}'
        matches = re.finditer(pattern, content, re.DOTALL)

        for match in matches:
            env_name = match.group(1).strip()
            env_body = match.group(2).strip()
            description = self._clean_text(env_body)

            items.append({
                "type": "environment",
                "macro_package": self.package_name,
                "environment_name": env_name,
                "description": description,
                "source_file": str(filepath.relative_to(self.manual_dir)),
                "id": self._generate_id(f"env_{env_name}_{filepath.stem}")
            })

        return items

    def _extract_codeexamples(self, content: str, filepath: Path) -> List[Dict[str, Any]]:
        """提取codeexample环境"""
        items = []
        pattern = r'\\begin\{codeexample\}(\[.*?\])?(.*?)\\end\{codeexample\}'
        matches = re.finditer(pattern, content, re.DOTALL)

        for idx, match in enumerate(matches):
            code = match.group(2).strip()

            # 判断图表类型
            chart_type = self._detect_chart_type(code)

            items.append({
                "type": "executable_example",
                "macro_package": self.package_name,
                "chart_type": chart_type,
                "code": code,
                "source_file": str(filepath.relative_to(self.manual_dir)),
                "id": self._generate_id(f"example_{filepath.stem}_{idx}")
            })

        return items

    def _detect_chart_type(self, code: str) -> str:
        """检测图表类型"""
        if '\\addplot' in code:
            if 'ybar' in code or 'xbar' in code:
                return "bar_chart"
            elif 'scatter' in code:
                return "scatter_plot"
            elif 'mesh' in code or 'surf' in code:
                return "3d_plot"
            else:
                return "line_chart"
        elif '\\node' in code and '\\draw' in code:
            return "node_graph"
        elif '\\pie' in code:
            return "pie_chart"
        else:
            return "other"


class GenericTeXExtractor(BaseExtractor):
    """通用 TeX 提取器 - 用于新增的手册包"""

    def process(self) -> List[Dict[str, Any]]:
        """通用提取逻辑"""
        tex_files = list(self.manual_dir.rglob("*.tex"))

        items = []
        for tex_file in tex_files:
            try:
                with open(tex_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                # 尝试提取各种环境
                items.extend(self._extract_generic_examples(content, tex_file))
            except Exception as e:
                print(f"  Error processing {tex_file.name}: {e}")
                continue

        return items

    def _extract_generic_examples(self, content: str, filepath: Path) -> List[Dict[str, Any]]:
        """提取通用示例环境"""
        items = []

        # 尝试多种常见的示例环境
        environments = [
            'codeexample', 'lstlisting', 'verbatim', 'example',
            'LTXexample', 'tkzexample', 'examplecode'
        ]

        for env in environments:
            pattern = rf'\\begin\{{{env}\}}(\[.*?\])?(.*?)\\end\{{{env}\}}'
            matches = re.finditer(pattern, content, re.DOTALL)

            for idx, match in enumerate(matches):
                code = match.group(2).strip()

                # 只保存有效的 LaTeX 代码（长度 > 10 且包含反斜杠）
                if len(code) > 10 and '\\' in code:
                    items.append({
                        "type": "executable_example",
                        "macro_package": self.package_name,
                        "chart_type": "other",
                        "code": code,
                        "source_file": str(filepath.relative_to(self.manual_dir)),
                        "id": self._generate_id(f"example_{filepath.stem}_{env}_{idx}")
                    })

        return items


class ExtractorFactory:
    """提取器工厂"""

    @staticmethod
    def create(package_name: str, manual_dir: Path) -> BaseExtractor:
        # 专用提取器
        specialized_extractors = {
            "tikz-network": TikzNetworkExtractor,
            "chemfig": ChemfigExtractor,
            "circuitikz": CircuitikzExtractor,
            "tkz-euclide": TkzEuclideExtractor,
            "pgfplots": StandardExtractor,
            "tikz-pgf": StandardExtractor
        }

        extractor_class = specialized_extractors.get(package_name, GenericTeXExtractor)
        return extractor_class(manual_dir, package_name)


def main():
    """主函数"""
    manual_base = Path("/Users/yaoyongke/Documents/yyk/0212_task/manual")
    output_base = Path("/Users/yaoyongke/Documents/yyk/0212_task/latex-mcp-knowledge/knowledge-base")

    # 自动发现所有手册包
    manual_dirs = [d for d in manual_base.iterdir() if d.is_dir() and not d.name.startswith('.')]

    all_items = []
    stats = {}

    print("=" * 70)
    print("LaTeX Manual Knowledge Extraction - All Packages")
    print("=" * 70)
    print(f"\nFound {len(manual_dirs)} manual packages\n")

    for manual_dir in sorted(manual_dirs):
        # 从目录名推导包名（移除 -manual 后缀）
        package_name = manual_dir.name.replace('-manual', '')

        print(f"=== Processing {package_name} ===")

        try:
            extractor = ExtractorFactory.create(package_name, manual_dir)
            items = extractor.process()

            if items:
                # 保存单独的包知识
                output_file = output_base / f"{package_name}-knowledge-raw.json"
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(items, f, indent=2, ensure_ascii=False)

                all_items.extend(items)
                stats[package_name] = len(items)
                print(f"  ✓ {len(items)} items extracted")
            else:
                print(f"  ⚠ No items found")
                stats[package_name] = 0

        except Exception as e:
            print(f"  ✗ Error: {e}")
            stats[package_name] = 0
            continue

    # 保存合并知识库
    combined_path = output_base / "latex-all-knowledge-raw.json"
    with open(combined_path, 'w', encoding='utf-8') as f:
        json.dump(all_items, f, indent=2, ensure_ascii=False)

    # 保存统计信息
    stats_path = output_base / "extraction-stats.json"
    stats["total"] = len(all_items)
    with open(stats_path, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)

    # 打印摘要
    print("\n" + "=" * 70)
    print("Extraction Summary")
    print("=" * 70)

    # 按数量排序
    sorted_stats = sorted([(k, v) for k, v in stats.items() if k != "total"],
                         key=lambda x: x[1], reverse=True)

    for package, count in sorted_stats:
        print(f"{package:25s}: {count:6d} items")

    print("-" * 70)
    print(f"{'Total':25s}: {stats['total']:6d} items")
    print(f"\nCombined output: {combined_path}")
    print(f"Statistics: {stats_path}")
    print("=" * 70)


if __name__ == "__main__":
    main()
