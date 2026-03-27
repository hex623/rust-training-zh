## 避免未检查索引

> **你将学到什么：** 为什么 `vec[i]` 在 Rust 中是危险的（越界时 panic），以及 `.get()`、迭代器和 `HashMap` 的 `entry()` API 等安全替代方案。用显式处理替代 C++ 的未定义行为。

- 在 C++ 中，`vec[i]` 和 `map[key]` 有未定义行为 / 缺失键自动插入。Rust 的 `[]` 在越界时 panic。
- **规则**：使用 `.get()` 代替 `[]`，除非你能 *证明* 索引有效。

### C++ → Rust 比较
```cpp
// C++ —— 静默 UB 或插入
std::vector<int> v = {1, 2, 3};
int x = v[10];        // UB！operator[] 无边界检查

std::map<std::string, int> m;
int y = m["missing"]; // 静默插入值为 0 的键！
```

```rust
// Rust —— 安全替代方案
let v = vec![1, 2, 3];

// 坏：如果索引越界则 panic
// let x = v[10];

// 好：返回 Option<&i32>
let x = v.get(10);              // None —— 无 panic
let x = v.get(1).copied().unwrap_or(0);  // 2，或缺失时为 0
```
