#!/usr/bin/env python3
"""
知识库结构化转换脚本
将提取的原始知识转换为 MCP 协议标准格式
"""

import json
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime


class KnowledgeStructurer:
    """知识结构化处理器"""

    def __init__(self):
        self.schema_version = "1.0.0"

    def structure_command(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """结构化命令类型知识"""
        return {
            "id": item["id"],
            "type": "command_specification",
            "macro_package": item["macro_package"],
            "metadata": {
                "command_name": item["command_name"],
                "category": "latex_command",
                "tags": self._generate_tags(item),
                "source_file": item["source_file"],
                "schema_version": self.schema_version,
                "created_at": datetime.now().isoformat()
            },
            "content": {
                "description": item["description"],
                "syntax": item["command_name"],
                "parameters": self._extract_parameters(item["command_name"]),
                "examples": item.get("examples", []),
                "notes": []
            },
            "mcp_metadata": {
                "searchable_fields": ["command_name", "description", "macro_package"],
                "priority": self._calculate_priority(item),
                "quality_score": 0.8
            }
        }

    def structure_environment(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """结构化环境类型知识"""
        return {
            "id": item["id"],
            "type": "environment_specification",
            "macro_package": item["macro_package"],
            "metadata": {
                "environment_name": item["environment_name"],
                "category": "latex_environment",
                "tags": self._generate_tags(item),
                "source_file": item["source_file"],
                "schema_version": self.schema_version,
                "created_at": datetime.now().isoformat()
            },
            "content": {
                "description": item["description"],
                "begin_syntax": f"\\begin{{{item['environment_name']}}}",
                "end_syntax": f"\\end{{{item['environment_name']}}}",
                "parameters": [],
                "examples": item.get("examples", []),
                "notes": []
            },
            "mcp_metadata": {
                "searchable_fields": ["environment_name", "description", "macro_package"],
                "priority": self._calculate_priority(item),
                "quality_score": 0.8
            }
        }

    def structure_executable_example(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """结构化可执行示例"""
        return {
            "id": item["id"],
            "type": "executable_example",
            "macro_package": item["macro_package"],
            "metadata": {
                "chart_type": item.get("chart_type", "unknown"),
                "category": "code_example",
                "tags": self._generate_tags(item),
                "source_file": item["source_file"],
                "schema_version": self.schema_version,
                "created_at": datetime.now().isoformat()
            },
            "content": {
                "description": item.get("description", ""),
                "code": item["code"],
                "options": item.get("options", ""),
                "dependencies": self._extract_dependencies(item["code"]),
                "parameters": self._extract_code_parameters(item["code"]),
                "output_type": "visual"
            },
            "mcp_metadata": {
                "searchable_fields": ["chart_type", "macro_package", "description"],
                "priority": self._calculate_priority(item),
                "quality_score": 0.9,
                "executable": True
            }
        }

    def structure_feedback(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """结构化反馈/警告类型知识"""
        return {
            "id": item["id"],
            "type": "human_feedback",
            "macro_package": item["macro_package"],
            "metadata": {
                "feedback_type": item.get("feedback_type", "warning"),
                "category": "best_practice",
                "tags": self._generate_tags(item),
                "source_file": item["source_file"],
                "schema_version": self.schema_version,
                "created_at": datetime.now().isoformat()
            },
            "content": {
                "message": item["content"],
                "severity": self._determine_severity(item),
                "context": "",
                "recommended_action": ""
            },
            "mcp_metadata": {
                "searchable_fields": ["feedback_type", "message", "macro_package"],
                "priority": self._calculate_priority(item),
                "quality_score": 0.7
            }
        }

    def _generate_tags(self, item: Dict[str, Any]) -> List[str]:
        """生成标签"""
        tags = [item["macro_package"]]

        if item["type"] == "executable_example":
            tags.append(item.get("chart_type", "unknown"))
            tags.append("example")
        elif item["type"] == "command":
            tags.append("command")
        elif item["type"] == "environment":
            tags.append("environment")
        elif item["type"] == "feedback":
            tags.append("feedback")
            tags.append(item.get("feedback_type", "warning"))

        return tags

    def _extract_parameters(self, command_name: str) -> List[Dict[str, str]]:
        """从命令名称中提取参数"""
        # 简化版：提取 \marg{} 和 \oarg{} 标记
        params = []
        import re
        margs = re.findall(r'\\marg\{([^}]+)\}', command_name)
        oargs = re.findall(r'\\oarg\{([^}]+)\}', command_name)

        for arg in margs:
            params.append({"name": arg, "type": "required"})
        for arg in oargs:
            params.append({"name": arg, "type": "optional"})

        return params

    def _extract_dependencies(self, code: str) -> List[str]:
        """提取代码依赖"""
        deps = set()
        if '\\begin{tikzpicture}' in code:
            deps.add('tikz')
        if '\\begin{axis}' in code or '\\addplot' in code:
            deps.add('pgfplots')
        if '\\usetikzlibrary' in code:
            import re
            libs = re.findall(r'\\usetikzlibrary\{([^}]+)\}', code)
            for lib in libs:
                deps.update(lib.split(','))

        return list(deps)

    def _extract_code_parameters(self, code: str) -> List[str]:
        """提取代码中的关键参数"""
        params = []
        import re

        # 提取常见参数
        patterns = [
            r'xlabel\s*=\s*\{([^}]+)\}',
            r'ylabel\s*=\s*\{([^}]+)\}',
            r'title\s*=\s*\{([^}]+)\}',
            r'width\s*=\s*([^,\]]+)',
            r'height\s*=\s*([^,\]]+)',
        ]

        for pattern in patterns:
            matches = re.findall(pattern, code)
            params.extend(matches)

        return params[:10]  # 限制数量

    def _determine_severity(self, item: Dict[str, Any]) -> str:
        """判断警告严重程度"""
        content = item.get("content", "").lower()
        if "error" in content or "fail" in content:
            return "high"
        elif "warning" in content:
            return "medium"
        else:
            return "low"

    def _calculate_priority(self, item: Dict[str, Any]) -> int:
        """计算优先级"""
        if item["type"] == "executable_example":
            return 10  # 可执行示例优先级最高
        elif item["type"] == "command":
            return 8
        elif item["type"] == "environment":
            return 7
        elif item["type"] == "feedback":
            return 6
        else:
            return 5

    def structure_all(self, raw_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """结构化所有知识项"""
        structured_items = []

        for item in raw_items:
            try:
                if item["type"] == "command":
                    structured = self.structure_command(item)
                elif item["type"] == "environment":
                    structured = self.structure_environment(item)
                elif item["type"] == "executable_example":
                    structured = self.structure_executable_example(item)
                elif item["type"] == "feedback":
                    structured = self.structure_feedback(item)
                else:
                    continue

                structured_items.append(structured)
            except Exception as e:
                print(f"Error structuring item {item.get('id', 'unknown')}: {e}")

        return structured_items


def main():
    """主函数"""
    base_path = Path("/root/task_0813/latex-mcp-knowledge/knowledge-base")

    # 读取原始知识
    raw_file = base_path / "latex-chart-knowledge-raw.json"
    with open(raw_file, 'r', encoding='utf-8') as f:
        raw_items = json.load(f)

    print(f"Loaded {len(raw_items)} raw knowledge items")

    # 结构化处理
    structurer = KnowledgeStructurer()
    structured_items = structurer.structure_all(raw_items)

    print(f"Structured {len(structured_items)} knowledge items")

    # 保存结构化知识库
    output_file = base_path / "latex-chart-knowledge-structured.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(structured_items, f, indent=2, ensure_ascii=False)

    print(f"Saved to {output_file}")

    # 生成统计信息
    stats = {
        "total_items": len(structured_items),
        "by_type": {},
        "by_package": {},
        "schema_version": "1.0.0",
        "generated_at": datetime.now().isoformat()
    }

    for item in structured_items:
        item_type = item["type"]
        package = item["macro_package"]

        stats["by_type"][item_type] = stats["by_type"].get(item_type, 0) + 1
        stats["by_package"][package] = stats["by_package"].get(package, 0) + 1

    stats_file = base_path / "knowledge-stats.json"
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)

    print(f"\nStatistics:")
    print(f"  Total: {stats['total_items']}")
    print(f"  By type: {stats['by_type']}")
    print(f"  By package: {stats['by_package']}")


if __name__ == "__main__":
    main()
