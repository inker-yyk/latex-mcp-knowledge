#!/usr/bin/env python3
"""
更新根目录的 mint.json，添加 mintlify-docs/ 前缀
"""
import json
from pathlib import Path

def add_prefix_to_paths(obj, prefix="mintlify-docs/", key=None):
    """递归添加前缀到所有路径"""
    if isinstance(obj, dict):
        return {k: add_prefix_to_paths(v, prefix, k) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [add_prefix_to_paths(item, prefix, key) for item in obj]
    elif isinstance(obj, str):
        # 不处理 group 字段（它是显示文本，不是路径）
        if key == 'group':
            return obj
        # 只处理相对路径（不包含 http:// 或 https://）
        # 即使没有 /，只要不是特殊开头，都添加前缀
        if not obj.startswith(('http://', 'https://', '/', '#', 'mintlify-docs/')):
            return prefix + obj
        return obj
    else:
        return obj

def main():
    # 读取 mintlify-docs/mint.json
    source_file = Path('mintlify-docs/mint.json')
    target_file = Path('mint.json')

    with open(source_file, 'r', encoding='utf-8') as f:
        config = json.load(f)

    # 需要添加前缀的字段
    if 'navigation' in config:
        for group in config['navigation']:
            if 'pages' in group:
                group['pages'] = add_prefix_to_paths(group['pages'])

    if 'tabs' in config:
        for tab in config['tabs']:
            if 'url' in tab and not tab['url'].startswith(('http://', 'https://', '/')):
                tab['url'] = 'mintlify-docs/' + tab['url']

    if 'openapi' in config and config['openapi'].startswith('/'):
        config['openapi'] = '/mintlify-docs' + config['openapi']

    # 写入根目录
    with open(target_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    print(f"✓ Updated {target_file}")
    print(f"  Added 'mintlify-docs/' prefix to all relative paths")

if __name__ == '__main__':
    main()
