# 面向 C/C++ 程序员的 Rust 入门课程

## 课程概述
- 课程概述
    - 为什么选择 Rust（从 C 和 C++ 两个角度）
    - 本地安装
    - 类型、函数、控制流、模式匹配
    - 模块、cargo
    - Trait、泛型
    - 集合、错误处理
    - 闭包、内存管理、生命周期、智能指针
    - 并发
    - Unsafe Rust，包括外部函数接口（FFI）
    - `no_std` 和嵌入式 Rust 基础，适用于固件团队
    - 案例研究：真实世界的 C++ 到 Rust 翻译模式
- 本课程不涉及 `async` Rust —— 请参阅配套的 [Async Rust 培训](../async-book/) 以全面了解 futures、执行器、`Pin`、tokio 和生产级 async 模式


---

# 自学指南

本材料既可作为讲师指导的课程，也适合自学。如果你正在独立学习，以下是充分利用它的方法：

**学习进度建议：**

| 章节 | 主题 | 建议时间 | 检查点 |
|----------|-------|---------------|------------|
| 1–4 | 环境搭建、类型、控制流 | 1 天 | 你可以编写一个 CLI 温度转换器 |
| 5–7 | 数据结构、所有权 | 1–2 天 | 你能解释 *为什么* `let s2 = s1` 会使 `s1` 失效 |
| 8–9 | 模块、错误处理 | 1 天 | 你可以创建一个多文件项目，使用 `?` 传播错误 |
| 10–12 | Trait、泛型、闭包 | 1–2 天 | 你可以编写带 trait bounds 的泛型函数 |
| 13–14 | 并发、unsafe/FFI | 1 天 | 你可以使用 `Arc<Mutex<T>>` 编写线程安全的计数器 |
| 15–16 | 深度解析 | 按你自己的节奏 | 参考资料 —— 需要时阅读 |
| 17–19 | 最佳实践与参考 | 按你自己的节奏 | 编写真实代码时查阅 |

**如何使用练习：**
- 每章都有动手练习，难度标记为：🟢 入门、🟡 中级、🔴 挑战
- **一定要先尝试练习，再查看解答。** 与借用检查器搏斗是学习的一部分 —— 编译器的错误信息就是你的老师
- 如果你卡住超过 15 分钟，展开解答，学习它，然后关闭并从头再试一次
- [Rust Playground](https://play.rust-lang.org/) 让你无需本地安装即可运行代码

**当你遇到困难时：**
- 仔细阅读编译器错误信息 —— Rust 的错误提示非常有帮助
- 重新阅读相关章节；像所有权（第7章）这样的概念通常在第二遍阅读时豁然开朗
- [Rust 标准库文档](https://doc.rust-lang.org/std/) 非常优秀 —— 搜索任何类型或方法
- 对于 async 模式，请参阅配套的 [Async Rust 培训](../async-book/)

---

# 目录

## 第一部分 — 基础

### 1. 介绍与动机
- [讲师介绍与一般方法](ch01-introduction-and-motivation.md#讲师介绍与一般方法)
- [为什么选择 Rust](ch01-introduction-and-motivation.md#为什么选择-rust)
- [Rust 如何解决这些问题？](ch01-introduction-and-motivation.md#rust-如何解决这些问题)
- [Rust 的其他独特卖点和特性](ch01-introduction-and-motivation.md#rust-的其他独特卖点和特性)
- [快速参考：Rust vs C/C++](ch01-introduction-and-motivation.md#快速参考rust-vs-cc)
- [为什么 C/C++ 开发者需要 Rust](ch01-1-why-c-cpp-developers-need-rust.md)
  - [Rust 消除了什么 —— 完整列表](ch01-1-why-c-cpp-developers-need-rust.md#rust-消除了什么--完整列表)
  - [C 和 C++ 共同的问题](ch01-1-why-c-cpp-developers-need-rust.md#c-和-c-共同的问题)
  - [C++ 额外增加的问题](ch01-1-why-c-cpp-developers-need-rust.md#c-额外增加的问题)
  - [Rust 如何解决这一切](ch01-1-why-c-cpp-developers-need-rust.md#rust-如何解决这一切)

### 2. 入门
- [够了，给我看代码](ch02-getting-started.md#够了给我看代码)
- [Rust 本地安装](ch02-getting-started.md#rust-本地安装)
- [Rust 包（crates）](ch02-getting-started.md#rust-包-crates)
- [示例：cargo 和 crates](ch02-getting-started.md#示例cargo-和-crates)

### 3. 基本类型与变量
- [Rust 内置类型](ch03-built-in-types.md#rust-内置类型)
- [Rust 类型规范与赋值](ch03-built-in-types.md#rust-类型规范与赋值)
- [Rust 类型规范与推导](ch03-built-in-types.md#rust-类型规范与推导)
- [Rust 变量与可变性](ch03-built-in-types.md#rust-变量与可变性)

### 4. 控制流
- [Rust if 关键字](ch04-control-flow.md#rust-if-关键字)
- [使用 while 和 for 的 Rust 循环](ch04-control-flow.md#使用-while-和-for-的-rust-循环)
- [使用 loop 的 Rust 循环](ch04-control-flow.md#使用-loop-的-rust-循环)
- [Rust 表达式块](ch04-control-flow.md#rust-表达式块)

### 5. 数据结构与集合
- [Rust 数组类型](ch05-data-structures.md#rust-数组类型)
- [Rust 元组](ch05-data-structures.md#rust-元组)
- [Rust 引用](ch05-data-structures.md#rust-引用)
- [C++ 引用 vs Rust 引用 —— 关键区别](ch05-data-structures.md#c-引用-vs-rust-引用--关键区别)
- [Rust 切片](ch05-data-structures.md#rust-切片)
- [Rust 常量与静态变量](ch05-data-structures.md#rust-常量与静态变量)
- [Rust 字符串：String vs &str](ch05-data-structures.md#rust-字符串string-vs-str)
- [Rust 结构体](ch05-data-structures.md#rust-结构体)
- [Rust Vec\<T\>](ch05-data-structures.md#rust-vec-类型)
- [Rust HashMap](ch05-data-structures.md#rust-hashmap-类型)
- [练习：Vec 和 HashMap](ch05-data-structures.md#练习vec-和-hashmap)

### 6. 模式匹配与枚举
- [Rust 枚举类型](ch06-enums-and-pattern-matching.md#rust-枚举类型)
- [Rust match 语句](ch06-enums-and-pattern-matching.md#rust-match-语句)
- [练习：使用 match 和 enum 实现加法和减法](ch06-enums-and-pattern-matching.md#练习使用-match-和-enum-实现加法和减法)

### 7. 所有权与内存管理
- [Rust 内存管理](ch07-ownership-and-borrowing.md#rust-内存管理)
- [Rust 所有权、借用与生命周期](ch07-ownership-and-borrowing.md#rust-所有权借用与生命周期)
- [Rust 移动语义](ch07-ownership-and-borrowing.md#rust-移动语义)
- [Rust Clone](ch07-ownership-and-borrowing.md#rust-clone)
- [Rust Copy trait](ch07-ownership-and-borrowing.md#rust-copy-trait)
- [Rust Drop trait](ch07-ownership-and-borrowing.md#rust-drop-trait)
- [练习：Move、Copy 和 Drop](ch07-ownership-and-borrowing.md#练习move-copy-和-drop)
- [Rust 生命周期与借用](ch07-1-lifetimes-and-borrowing-deep-dive.md#rust-生命周期与借用)
- [Rust 生命周期注解](ch07-1-lifetimes-and-borrowing-deep-dive.md#rust-生命周期注解)
- [练习：带生命周期的切片存储](ch07-1-lifetimes-and-borrowing-deep-dive.md#练习带生命周期的切片存储)
- [生命周期省略规则深度解析](ch07-1-lifetimes-and-borrowing-deep-dive.md#生命周期省略规则深度解析)
- [Rust Box\<T\>](ch07-2-smart-pointers-and-interior-mutability.md#rust-boxt)
- [内部可变性：Cell\<T\> 和 RefCell\<T\>](ch07-2-smart-pointers-and-interior-mutability.md#内部可变性-cellt-和-refcellt)
- [共享所有权：Rc\<T\>](ch07-2-smart-pointers-and-interior-mutability.md#共享所有权-rct)
- [练习：共享所有权与内部可变性](ch07-2-smart-pointers-and-interior-mutability.md#练习共享所有权与内部可变性)

### 8. 模块与 Crates
- [Rust crates 和模块](ch08-crates-and-modules.md#rust-crates-和模块)
- [练习：模块与函数](ch08-crates-and-modules.md#练习模块与函数)
- [工作空间与 crates（包）](ch08-crates-and-modules.md#工作空间与-crates包)
- [练习：使用工作空间和包依赖](ch08-crates-and-modules.md#练习使用工作空间和包依赖)
- [使用来自 crates.io 的社区 crates](ch08-crates-and-modules.md#使用来自-cratesio-的社区-crates)
- [Crates 依赖与 SemVer](ch08-crates-and-modules.md#crates-依赖与-semver)
- [练习：使用 rand crate](ch08-crates-and-modules.md#练习使用-rand-crate)
- [Cargo.toml 和 Cargo.lock](ch08-crates-and-modules.md#cargotoml-和-cargolock)
- [Cargo test 特性](ch08-crates-and-modules.md#cargo-test-特性)
- [其他 Cargo 特性](ch08-crates-and-modules.md#其他-cargo-特性)
- [测试模式](ch08-1-testing-patterns.md)

### 9. 错误处理
- [将枚举连接到 Option 和 Result](ch09-error-handling.md#将枚举连接到-option-和-result)
- [Rust Option 类型](ch09-error-handling.md#rust-option-类型)
- [Rust Result 类型](ch09-error-handling.md#rust-result-类型)
- [练习：使用 Option 实现 log() 函数](ch09-error-handling.md#练习使用-option-实现-log-函数)
- [Rust 错误处理](ch09-error-handling.md#rust-错误处理)
- [练习：错误处理](ch09-error-handling.md#练习错误处理)
- [错误处理最佳实践](ch09-1-error-handling-best-practices.md)

### 10. Trait 与泛型
- [Rust trait](ch10-traits.md#rust-trait)
- [C++ 运算符重载 → Rust std::ops Trait](ch10-traits.md#c-运算符重载--rust-stdops-trait)
- [练习：Logger trait 实现](ch10-traits.md#练习logger-trait-实现)
- [何时使用 enum vs dyn Trait](ch10-traits.md#何时使用-enum-vs-dyn-trait)
- [练习：翻译前请三思](ch10-traits.md#练习翻译前请三思)
- [Rust 泛型](ch10-1-generics.md#rust-泛型)
- [练习：泛型](ch10-1-generics.md#练习泛型)
- [结合 Rust trait 与泛型](ch10-1-generics.md#结合-rust-trait-与泛型)
- [数据类型中的 Rust trait 约束](ch10-1-generics.md#数据类型中的-rust-trait-约束)
- [练习：Trait 约束与泛型](ch10-1-generics.md#练习trait-约束与泛型)
- [Rust 类型状态模式与泛型](ch10-1-generics.md#rust-类型状态模式与泛型)
- [Rust 构建器模式](ch10-1-generics.md#rust-构建器模式)

### 11. 类型系统高级特性
- [Rust From 和 Into trait](ch11-from-and-into-traits.md#rust-from-和-into-trait)
- [练习：From 和 Into](ch11-from-and-into-traits.md#练习from-和-into)
- [Rust Default trait](ch11-from-and-into-traits.md#rust-default-trait)
- [其他 Rust 类型转换](ch11-from-and-into-traits.md#其他-rust-类型转换)

### 12. 函数式编程
- [Rust 闭包](ch12-closures.md#rust-闭包)
- [练习：闭包与捕获](ch12-closures.md#练习闭包与捕获)
- [Rust 迭代器](ch12-closures.md#rust-迭代器)
- [练习：Rust 迭代器](ch12-closures.md#练习rust-迭代器)
- [迭代器高级工具参考](ch12-1-iterator-power-tools.md#迭代器高级工具参考)

### 13. 并发
- [Rust 并发](ch13-concurrency.md#rust-并发)
- [为什么 Rust 能防止数据竞争：Send 和 Sync](ch13-concurrency.md#为什么-rust-能防止数据竞争send-和-sync)
- [练习：多线程单词计数](ch13-concurrency.md#练习多线程单词计数)

### 14. Unsafe Rust 与 FFI
- [Unsafe Rust](ch14-unsafe-rust-and-ffi.md#unsafe-rust)
- [简单 FFI 示例](ch14-unsafe-rust-and-ffi.md#简单-ffi-示例rust-库函数被-c-调用)
- [复杂 FFI 示例](ch14-unsafe-rust-and-ffi.md#复杂-ffi-示例)
- [确保 unsafe 代码的正确性](ch14-unsafe-rust-and-ffi.md#确保-unsafe-代码的正确性)
- [练习：编写安全的 FFI 包装器](ch14-unsafe-rust-and-ffi.md#练习编写安全的-ffi-包装器)

## 第二部分 — 深度解析

### 15. no_std — 裸机 Rust
- [什么是 no_std？](ch15-no_std-rust-without-the-standard-library.md#什么是-no_std)
- [何时使用 no_std vs std](ch15-no_std-rust-without-the-standard-library.md#何时使用-no_std-vs-std)
- [练习：no_std 环形缓冲区](ch15-no_std-rust-without-the-standard-library.md#练习no_std-环形缓冲区)
- [嵌入式深度解析](ch15-1-embedded-deep-dive.md)

### 16. 案例研究：真实世界的 C++ 到 Rust 翻译
- [案例研究 1：继承层次结构 → Enum 分发](ch16-case-studies.md#案例研究-1继承层次结构--enum-分发)
- [案例研究 2：shared_ptr 树 → Arena/索引模式](ch16-case-studies.md#案例研究-2shared_ptr-树--arena索引模式)
- [案例研究 3：框架通信 → 生命周期借用](ch16-1-case-study-lifetime-borrowing.md#案例研究-3框架通信--生命周期借用)
- [案例研究 4：上帝对象 → 可组合状态](ch16-1-case-study-lifetime-borrowing.md#案例研究-4上帝对象--可组合状态)
- [案例研究 5：Trait 对象 —— 何时它们是正确的选择](ch16-1-case-study-lifetime-borrowing.md#案例研究-5trait-对象--何时它们是正确的选择)

## 第三部分 — 最佳实践与参考

### 17. 最佳实践
- [Rust 最佳实践总结](ch17-best-practices.md#rust-最佳实践总结)
- [避免过度 clone()](ch17-1-avoiding-excessive-clone.md#避免过度-clone)
- [避免未检查索引](ch17-2-avoiding-unchecked-indexing.md#避免未检查索引)
- [折叠赋值金字塔](ch17-3-collapsing-assignment-pyramids.md#折叠赋值金字塔)
- [顶点练习：诊断事件管道](ch17-3-collapsing-assignment-pyramids.md#顶点练习诊断事件管道)
- [日志与追踪生态系统](ch17-4-logging-and-tracing-ecosystem.md#日志与追踪生态系统)

### 18. C++ → Rust 语义深度解析
- [类型转换、预处理器、模块、volatile、static、constexpr、SFINAE 等等](ch18-cpp-rust-semantic-deep-dives.md)

### 19. Rust 宏
- [声明式宏（`macro_rules!`）](ch19-macros.md#声明式宏-macro_rules)
- [常见标准库宏](ch19-macros.md#常见标准库宏)
- [派生宏](ch19-macros.md#派生宏)
- [属性宏](ch19-macros.md#属性宏)
- [过程宏](ch19-macros.md#过程宏概念概述)
- [何时使用什么：宏 vs 函数 vs 泛型](ch19-macros.md#何时使用什么宏-vs-函数-vs-泛型)
- [练习](ch19-macros.md#练习)
