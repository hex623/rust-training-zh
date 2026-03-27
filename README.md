# Rust 培训笔记（中文版）

> 面向 C/C++ 程序员的 Rust 快速入门与进阶指南

[![mdBook](https://img.shields.io/badge/Built%20with-mdBook-orange.svg)](https://rust-lang.github.io/mdBook/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

## 📖 项目简介

本项目是一份面向 C/C++ 开发者的 Rust 语言培训笔记，采用 [mdBook](https://rust-lang.github.io/mdBook/) 格式组织，共包含 **33 章** 内容，涵盖从基础语法到高级特性的完整知识体系。

**总字数**: 约 8 万字（245,131 字符）

---

## 📚 内容结构

### 第一部分 — 基础（14 章）

| 章节 | 标题 | 核心内容 |
|------|------|----------|
| ch01 | 介绍与动机 | 为什么 C/C++ 开发者需要 Rust |
| ch02 | 入门 | 环境搭建、Hello World |
| ch03 | 内置类型 | 标量类型、复合类型 |
| ch04 | 控制流 | if/else、循环、match |
| ch05 | 数据结构 | struct、enum、数组、Vec、HashMap |
| ch06 | 枚举与模式匹配 | Option、Result、模式匹配深度解析 |
| ch07 | 所有权与借用 | Rust 核心机制：所有权、借用、生命周期 |
| ch08 | Crates 与模块 | 包管理、模块系统、可见性 |
| ch09 | 错误处理 | panic!、Result、? 运算符 |
| ch10 | Trait | 接口抽象、泛型编程 |
| ch11 | From 与 Into | 类型转换最佳实践 |
| ch12 | 闭包 | 闭包语法、Fn/FnMut/FnOnce、迭代器 |
| ch13 | 并发 | 线程、通道、Arc、Mutex、Send/Sync |
| ch14 | Unsafe Rust 与 FFI | 不安全代码、C 互操作 |

### 第二部分 — 深度解析（4 章）

| 章节 | 标题 | 核心内容 |
|------|------|----------|
| ch15 | no_std | 无标准库的 Rust、嵌入式开发 |
| ch16 | 案例研究 | 真实世界的 C++ 到 Rust 迁移案例 |

### 第三部分 — 最佳实践与参考（6 章）

| 章节 | 标题 | 核心内容 |
|------|------|----------|
| ch17 | 最佳实践 | 避免过度 clone、索引检查、日志追踪 |
| ch18 | C++ → Rust 语义深度解析 | 内存模型对比、RAII 差异 |
| ch19 | Rust 宏 | 声明宏与过程宏 |

---

## 🚀 快速开始

### 在线阅读

📚 **GitHub Pages**: https://hex623.github.io/rust-training-zh

### 本地阅读

1. **安装 mdBook**
   ```bash
   cargo install mdbook
   ```

2. **克隆仓库**
   ```bash
   git clone https://github.com/hex623/rust-training-zh.git
   cd rust-training-zh
   ```

3. **构建并预览**
   ```bash
   mdbook serve --open
   ```

---

## 📁 目录结构

```
rust-training-zh/
├── book.toml              # mdBook 配置文件
├── src/
│   ├── SUMMARY.md         # 目录结构
│   ├── ch00-introduction.md
│   ├── ch01-introduction-and-motivation.md
│   ├── ch01-1-why-c-cpp-developers-need-rust.md
│   ├── ch02-getting-started.md
│   ├── ...
│   └── ch19-macros.md
├── mermaid.min.js         # Mermaid 图表支持
└── mermaid-init.js
```

---

## 🎯 适用人群

- 有 C/C++ 基础，想快速掌握 Rust 的开发者
- 希望理解 Rust 所有权和借用机制的程序员
- 需要进行 C/C++ 到 Rust 迁移的工程师
- 对系统编程和内存安全感兴趣的开发者

---

## ✨ 特色亮点

- **C/C++ 对比视角**：每章都有与 C/C++ 的对比，帮助理解差异
- **实战案例**：真实代码示例，可直接运行
- **深度解析**：所有权、生命周期、并发等核心概念深入讲解
- **最佳实践**：来自生产环境的经验总结
- **中文本地化**：专为中文读者优化，术语对照清晰

---

## 🛠️ 构建说明

### 依赖

- [Rust](https://rustup.rs/) (最新稳定版)
- [mdBook](https://github.com/rust-lang/mdBook)
- [mdbook-mermaid](https://github.com/badboy/mdbook-mermaid) (可选，用于渲染 Mermaid 图表)

### 构建命令

```bash
# 构建静态站点
mdbook build

# 本地预览
mdbook serve

# 构建输出到 book/ 目录
mdbook build --dest-dir ./book
```

---

## 🤝 贡献

欢迎提交 Issue 和 PR！

- 发现错误？请提交 [Issue](../../issues)
- 想改进内容？请 Fork 并提交 [Pull Request](../../pulls)

---

## 📄 许可证

本项目采用 [MIT License](LICENSE) 开源协议。

---

## 🙏 致谢

- [The Rust Programming Language](https://doc.rust-lang.org/book/)
- [Rust By Example](https://doc.rust-lang.org/rust-by-example/)
- [mdBook](https://rust-lang.github.io/mdBook/)

---

<p align="center">
  Built with ❤️ by Hexu
</p>
