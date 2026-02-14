#!/usr/bin/env python3
"""
TEX 内容提取脚本
从 LaTeX 手册源文件中提取核心知识内容
"""

import re
import json
import os
from pathlib import Path
from typing import List, Dict, Any
import hashlib

class TexContentExtractor:
    """LaTeX 内容提取器"""

    def __init__(self, manual_dir: str):
        self.manual_dir = Path(manual_dir)
        self.knowledge_items = []

    def extract_commands(self, content: str, filepath: str) -> List[Dict[str, Any]]:
        """提取命令定义（\\begin{command}...\\end{command}）"""
        items = []
        # 匹配 \begin{command}{...} ... \end{command}
        pattern = r'\\begin\{command\}\{([^}]+)\}(.*?)\\end\{command\}'
        matches = re.finditer(pattern, content, re.DOTALL)

        for match in matches:
            command_name = match.group(1).strip()
            command_body = match.group(2).strip()

            # 提取描述
            description = self._extract_description(command_body)

            # 提取代码示例
            examples = self._extract_code_examples(command_body)

            items.append({
                "type": "command",
                "macro_package": self._detect_package(filepath),
                "command_name": command_name,
                "description": description,
                "examples": examples,
                "source_file": str(filepath),
                "id": self._generate_id(f"cmd_{command_name}")
            })

        return items

    def extract_environments(self, content: str, filepath: str) -> List[Dict[str, Any]]:
        """提取环境定义（\\begin{environment}...\\end{environment}）"""
        items = []
        # 匹配 \begin{environment}{...} ... \end{environment}
        pattern = r'\\begin\{environment\}\{([^}]+)\}(.*?)\\end\{environment\}'
        matches = re.finditer(pattern, content, re.DOTALL)

        for match in matches:
            env_name = match.group(1).strip()
            env_body = match.group(2).strip()

            description = self._extract_description(env_body)
            examples = self._extract_code_examples(env_body)

            items.append({
                "type": "environment",
                "macro_package": self._detect_package(filepath),
                "environment_name": env_name,
                "description": description,
                "examples": examples,
                "source_file": str(filepath),
                "id": self._generate_id(f"env_{env_name}")
            })

        return items

    def extract_code_examples(self, content: str, filepath: str) -> List[Dict[str, Any]]:
        """提取代码示例（codeexample 环境）"""
        items = []
        # 匹配 \begin{codeexample}[...] ... \end{codeexample}
        pattern = r'\\begin\{codeexample\}(\[.*?\])?(.*?)\\end\{codeexample\}'
        matches = re.finditer(pattern, content, re.DOTALL)

        for idx, match in enumerate(matches):
            options = match.group(1) or ""
            code = match.group(2).strip()

            # 判断图表类型
            chart_type = self._detect_chart_type(code)

            items.append({
                "type": "executable_example",
                "macro_package": self._detect_package(filepath),
                "chart_type": chart_type,
                "code": code,
                "options": options,
                "description": f"Executable example from {filepath.name}",
                "source_file": str(filepath),
                "id": self._generate_id(f"example_{filepath.stem}_{idx}")
            })

        return items

    def extract_warnings(self, content: str, filepath: str) -> List[Dict[str, Any]]:
        """提取警告和注意事项"""
        items = []
        # 匹配常见的警告模式
        patterns = [
            r'\\textbf\{Warning[:\s]*\}(.*?)(?=\\\\|\n\n)',
            r'\\textbf\{Note[:\s]*\}(.*?)(?=\\\\|\n\n)',
            r'\\textbf\{Attention[:\s]*\}(.*?)(?=\\\\|\n\n)',
        ]

        for pattern in patterns:
            matches = re.finditer(pattern, content, re.DOTALL | re.IGNORECASE)
            for match in matches:
                warning_text = match.group(1).strip()

                items.append({
                    "type": "feedback",
                    "macro_package": self._detect_package(filepath),
                    "feedback_type": "warning",
                    "content": warning_text,
                    "source_file": str(filepath),
                    "id": self._generate_id(f"warning_{warning_text[:20]}")
                })

        return items

    def _extract_description(self, text: str) -> str:
        """从文本中提取描述性内容"""
        # 移除 LaTeX 命令和环境
        text = re.sub(r'\\begin\{codeexample\}.*?\\end\{codeexample\}', '', text, flags=re.DOTALL)
        text = re.sub(r'\\[a-zA-Z]+\{([^}]*)\}', r'\1', text)
        text = re.sub(r'\\[a-zA-Z]+', '', text)
        text = ' '.join(text.split())  # 规范化空白
        return text[:500]  # 限制长度

    def _extract_code_examples(self, text: str) -> List[str]:
        """从文本中提取代码示例"""
        examples = []
        pattern = r'\\begin\{codeexample\}.*?(.*?)\\end\{codeexample\}'
        matches = re.finditer(pattern, text, re.DOTALL)
        for match in matches:
            examples.append(match.group(1).strip())
        return examples

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
            if 'circle' in code or 'rectangle' in code:
                return "flowchart"
            else:
                return "node_graph"
        elif '\\pie' in code:
            return "pie_chart"
        else:
            return "other"

    def _detect_package(self, filepath: Path) -> str:
        """根据文件路径检测所属宏包"""
        if 'pgfplots' in str(filepath):
            return "pgfplots"
        elif 'tikz' in str(filepath) or 'pgf' in str(filepath):
            return "tikz"
        else:
            return "unknown"

    def _generate_id(self, base: str) -> str:
        """生成唯一 ID"""
        return hashlib.md5(base.encode()).hexdigest()[:12]

    def process_file(self, filepath: Path) -> List[Dict[str, Any]]:
        """处理单个 TEX 文件"""
        print(f"Processing: {filepath}")

        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            return []

        items = []
        items.extend(self.extract_commands(content, filepath))
        items.extend(self.extract_environments(content, filepath))
        items.extend(self.extract_code_examples(content, filepath))
        items.extend(self.extract_warnings(content, filepath))

        return items

    def process_directory(self) -> List[Dict[str, Any]]:
        """处理整个目录"""
        all_items = []

        # 遍历所有 .tex 文件
        for tex_file in self.manual_dir.rglob("*.tex"):
            items = self.process_file(tex_file)
            all_items.extend(items)

        return all_items

    def save_to_json(self, output_path: str, items: List[Dict[str, Any]]):
        """保存为 JSON 格式"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(items, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(items)} items to {output_path}")


def main():
    """主函数"""
    # 配置路径
    manual_base = Path("/Users/yaoyongke/Documents/yyk/0212_task/manual")
    output_base = Path("/Users/yaoyongke/Documents/yyk/0212_task/latex-mcp-knowledge")

    # 处理 TikZ/PGF 手册
    print("\n=== Processing TikZ/PGF Manual ===")
    tikz_extractor = TexContentExtractor(manual_base / "tikz-pgf-manual")
    tikz_items = tikz_extractor.process_directory()
    tikz_extractor.save_to_json(output_base / "tikz-knowledge-raw.json", tikz_items)

    # 处理 PGFPlots 手册
    print("\n=== Processing PGFPlots Manual ===")
    pgfplots_extractor = TexContentExtractor(manual_base / "pgfplots-manual")
    pgfplots_items = pgfplots_extractor.process_directory()
    pgfplots_extractor.save_to_json(output_base / "pgfplots-knowledge-raw.json", pgfplots_items)

    # 合并所有知识
    all_items = tikz_items + pgfplots_items
    combined_path = output_base / "latex-chart-knowledge-raw.json"

    with open(combined_path, 'w', encoding='utf-8') as f:
        json.dump(all_items, f, indent=2, ensure_ascii=False)

    print(f"\n=== Summary ===")
    print(f"TikZ items: {len(tikz_items)}")
    print(f"PGFPlots items: {len(pgfplots_items)}")
    print(f"Total items: {len(all_items)}")
    print(f"Combined output: {combined_path}")


if __name__ == "__main__":
    main()
