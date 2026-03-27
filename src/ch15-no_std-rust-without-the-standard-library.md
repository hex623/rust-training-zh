# `no_std` — 无标准库的 Rust

> **你将学到什么：** 如何使用 `#![no_std]` 为裸机和嵌入式目标编写 Rust —— `core` 和 `alloc` crate 分割、panic 处理程序，以及这与没有 `libc` 的嵌入式 C 的比较。

如果你来自嵌入式 C，你已经习惯在没有 `libc` 或只有最小运行时的情况下工作。Rust 有一流等效： **`#![no_std]`** 属性。

## 什么是 `no_std`？

当你在 crate 根目录添加 `#![no_std]` 时，编译器移除隐式 `extern crate std;` 并只链接 **`core`**（和可选 **`alloc`**）。

| 层 | 提供什么 | 需要 OS / 堆？ |
|-------|-----------------|---------------------|
| `core` | 基本类型、`Option`、`Result`、`Iterator`、数学、`slice`、`str`、原子操作、`fmt` | **否** —— 在裸机上运行 |
| `alloc` | `Vec`、`String`、`Box`、`Rc`、`Arc`、`BTreeMap` | 需要全局分配器，但 **不需要 OS** |
| `std` | `HashMap`、`fs`、`net`、`thread`、`io`、`env`、`process` | **是** —— 需要 OS |

> **嵌入式开发者的经验法则：** 如果你的 C 项目链接 `-lc` 并使用 `malloc`，你可能可以使用 `core` + `alloc`。如果它在没有 `malloc` 的裸机上运行，只用 `core`。

## 声明 `no_std`

```rust
// src/lib.rs （或带有 #![no_main] 的二进制文件的 src/main.rs）
#![no_std]

// 你仍然获得 `core` 中的所有内容：
use core::fmt;
