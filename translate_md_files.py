#!/usr/bin/env python3
"""
Rust 培训文档翻译脚本
使用 AI API 批量翻译 markdown 文件

使用方法:
    python3 translate_md_files.py --file src/chXX-name.md
    python3 translate_md_files.py --all
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path

# 翻译提示词模板
TRANSLATION_PROMPT = """请将以下 Rust 培训文档从英文翻译为中文。

翻译要求：
1. 保持所有 Markdown 格式不变（标题、代码块、表格等）
2. 代码示例本身保持不变，但代码中的注释需要翻译
3. 技术术语首次出现时保留英文并加括号，如：ownership（所有权）
4. 保持原有的 Mermaid 图表语法不变
5. 面向 C/C++ 开发者的角度进行翻译
6. 保持原有的提示块格式（> **Note:** 等）
7. 不要添加任何解释，直接输出翻译后的内容

原始内容：

{content}
"""

def translate_with_cli(content: str) -> str:
    """
    使用 OpenClaw CLI 或其他 AI 工具进行翻译
    这里只是一个框架，需要接入实际的 AI API
    """
    # 实际实现应该调用 AI API
    # 例如：openai.ChatCompletion.create(...) 或 anthropic 等
    # 由于这需要 API key 和外部服务，这里提供框架
    
    # 临时方案：将内容分段保存，提示用户使用外部工具
    return None

def translate_file(file_path: str, dry_run: bool = False) -> bool:
    """翻译单个文件"""
    path = Path(file_path)
    if not path.exists():
        print(f"❌ 文件不存在: {file_path}")
        return False
    
    content = path.read_text(encoding='utf-8')
    char_count = len(content)
    
    print(f"📄 {path.name} ({char_count} 字符)")
    
    if dry_run:
        print("   [试运行模式，跳过翻译]")
        return True
    
    # 这里应该调用实际的翻译 API
    # translated = translate_with_api(content)
    
    print("   ⚠️  需要接入 AI API 进行翻译")
    print("   建议使用: OpenAI API / Claude API / DeepL API")
    return False

def get_all_md_files(src_dir: str = "src") -> list:
    """获取所有 markdown 文件"""
    src_path = Path(src_dir)
    files = sorted(src_path.glob("ch*.md"))
    return [str(f) for f in files]

def batch_translate(files: list, batch_size: int = 3):
    """批量翻译文件"""
    total = len(files)
    print(f"\n🚀 开始批量翻译: {total} 个文件")
    print("=" * 50)
    
    for i, file_path in enumerate(files, 1):
        print(f"\n[{i}/{total}] ", end="")
        translate_file(file_path, dry_run=True)
        
        # 每批次后提示休息
        if i % batch_size == 0 and i < total:
            print(f"\n⏸️  已完成 {i}/{total} 个文件，建议休息一下")

def estimate_cost(char_count: int, price_per_1k: float = 0.01) -> float:
    """估算翻译成本 (OpenAI GPT-4 价格)"""
    # GPT-4 通常输入 $0.01/1K tokens, 输出 $0.03/1K tokens
    # 估算 1 个字符约等于 0.5 个 token (对于英文)
    estimated_tokens = char_count * 0.5
    cost = (estimated_tokens / 1000) * price_per_1k * 2  # 输入+输出
    return cost

def main():
    parser = argparse.ArgumentParser(description='Rust 培训文档翻译工具')
    parser.add_argument('--file', help='翻译单个文件')
    parser.add_argument('--all', action='store_true', help='翻译所有文件')
    parser.add_argument('--dry-run', action='store_true', help='试运行模式')
    parser.add_argument('--estimate', action='store_true', help='估算成本')
    
    args = parser.parse_args()
    
    if args.estimate:
        files = get_all_md_files()
        total_chars = sum(len(Path(f).read_text(encoding='utf-8')) for f in files)
        cost = estimate_cost(total_chars)
        print(f"📊 翻译成本估算")
        print(f"   总字符数: {total_chars:,}")
        print(f"   预估成本: ${cost:.2f} USD (使用 GPT-4)")
        return
    
    if args.file:
        translate_file(args.file, dry_run=args.dry_run)
    elif args.all:
        files = get_all_md_files()
        batch_translate(files)
    else:
        parser.print_help()
        print("\n💡 示例:")
        print("   python3 translate_md_files.py --estimate")
        print("   python3 translate_md_files.py --file src/ch00-introduction.md")
        print("   python3 translate_md_files.py --all --dry-run")

if __name__ == "__main__":
    main()
