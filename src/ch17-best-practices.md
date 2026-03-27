# Rust 最佳实践总结

> **你将学到什么：** 编写惯用 Rust 的实用指南 —— 代码组织、命名约定、错误处理模式和文档。你会经常回顾的快速参考章节。

## 代码组织
- **优先小函数**：易于测试和推理
- **使用描述性名称**：`calculate_total_price()` vs `calc()`
- **将相关功能分组**：使用模块和单独文件
- **编写文档**：对公共 API 使用 `///`

## 错误处理
- **避免 `unwrap()` 除非可靠**：仅在 100% 确定不会 panic 时使用
```rust
// 坏：可能 panic
let value = some_option.unwrap();

// 好：处理 None 情况
let value = some_option.unwrap_or(default_value);
let value = some_option.unwrap_or_else(|| expensive_computation());
let value = some_option.unwrap_or_default(); // 使用 Default trait

// 对于 Result<T, E>
let value = some_result.unwrap_or(fallback_value);
let value = some_result.unwrap_or_else(|err| {
    eprintln!("发生错误: {err}");
    default_value
});
```
- **使用 `expect()` 带描述性消息**：当 unwrap 合理时，解释原因
```rust
