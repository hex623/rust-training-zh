#!/bin/bash
# translate-rust-book.sh
# Rust 培训文档翻译脚本

# 这是一个占位符脚本，实际翻译应该使用以下方法之一：
# 1. 使用 AI 翻译 API（如 OpenAI、Claude API）批量处理
# 2. 使用专门的翻译工具
# 3. 分章节人工翻译

echo "Rust 培训文档翻译方案"
echo "======================"
echo ""
echo "推荐翻译方法："
echo ""
echo "方法 1: 使用 AI API 批量翻译（推荐）"
echo "  - 使用 OpenAI API 或 Claude API"
echo "  - 编写脚本批量处理所有文件"
echo "  - 保留 Markdown 格式"
echo ""
echo "方法 2: 使用 mdbook 翻译插件"
echo "  - 搜索现有的 mdbook 翻译工具"
echo "  - 或使用 mdbook-i18n 支持"
echo ""
echo "方法 3: 分批次手动翻译"
echo "  - 每批 5-6 个文件"
echo "  - 共需 6 批完成"
echo "  - 每次翻译后提交"
echo ""
echo "当前文件数量统计："
ls -1 ~/Documents/GitHub/rust-training-zh/src/*.md | wc -l
echo " 个文件"
echo ""
echo "总字符数："
cat ~/Documents/GitHub/rust-training-zh/src/*.md | wc -m
echo " 字符"
