## 用闭包折叠赋值金字塔

> **你将学到什么：** Rust 的基于表达式的语法和闭包如何将深层嵌套的 C++ `if/else` 验证链展平为干净、线性的代码。

- C++ 通常需要多块 `if/else` 链来赋值变量，尤其是涉及验证或回退逻辑时。Rust 的基于表达式的语法和闭包将这些折叠为扁平、线性的代码。

### 模式 1：使用 `if` 表达式的元组赋值
```cpp
// C++ —— 跨多块 if/else 链设置三个变量
uint32_t fault_code;
const char* der_marker;
const char* action;
if (is_c44ad) {
    fault_code = 32709; der_marker = "CSI_WARN"; action = "No action";
} else if (error.is_hardware_error()) {
    fault_code = 67956; der_marker = "CSI_ERR"; action = "Replace GPU";
} else {
    fault_code = 32709; der_marker = "CSI_WARN"; action = "No action";
}
```

```rust
// Rust 等效：accel_fieldiag.rs
// 单个表达式一次分配所有三个：
let (fault_code, der_marker, recommended_action) = if is_c44ad {
    (32709u32, "CSI_WARN", "No action")
} else if error.is_hardware_error() {
    (67956u32, "CSI_ERR", "Replace GPU")
} else {
    (32709u32, "CSI_WARN", "No action")
