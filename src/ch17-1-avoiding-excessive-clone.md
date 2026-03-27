## 避免过度 clone()

> **你将学到什么：** 为什么 `.clone()` 在 Rust 中是代码异味，如何重构所有权以消除不必要的拷贝，以及表明所有权设计问题的具体模式。

- 来自 C++，`.clone()` 感觉像一个安全的默认选项 —— "只是拷贝它"。但过度克隆隐藏了所有权问题并损害性能。
- **经验法则**：如果你克隆是为了满足借用检查器，你可能需要重构所有权。

### 何时 clone() 是错误的

```rust
// 坏：克隆 String 只是为了传递给只读取它的函数
fn log_message(msg: String) {  // 不必要地获取所有权
    println!("[LOG] {}", msg);
}
let message = String::from("GPU test passed");
log_message(message.clone());  // 浪费：分配一个全新的 String
log_message(message);           // 原始被消耗 —— 克隆无意义
```

```rust
// 好：接受借用 —— 零分配
fn log_message(msg: &str) {    // 借用，不拥有
    println!("[LOG] {}", msg);
}
let message = String::from("GPU test passed");
log_message(&message);          // 无克隆，无分配
log_message(&message);          // 可以再次调用 —— message 未被消耗
```
