## C++ → Rust 语义深度解析

> **你将学到什么：** 没有明显 Rust 等效物的 C++ 概念的详细映射 —— 四个命名转换、SFINAE vs trait bounds、CRTP vs 关联类型，以及翻译期间的其他常见摩擦点。

以下部分映射没有明显 1:1 Rust 等效物的 C++ 概念。这些差异经常在翻译工作中绊倒 C++ 程序员。

### 转换层次结构：四个 C++ 转换 → Rust 等效物

C++ 有四个命名转换。Rust 用不同、更明确的机制替代它们：

```cpp
// C++ 转换层次结构
int i = static_cast<int>(3.14);            // 1. 数字 / 向上转换
Derived* d = dynamic_cast<Derived*>(base); // 2. 运行时向下转换
int* p = const_cast<int*>(cp);              // 3. 去除 const
auto* raw = reinterpret_cast<char*>(&obj); // 4. 位级重解释
```

| C++ 转换 | Rust 等效 | 安全 | 说明 |
|----------|----------------|--------|-------|
| `static_cast`（数字） | `as` 关键字 | 安全但可能截断/回绕 | `let i = 3.14_f64 as i32;` —— 截断为 3 |
| `static_cast`（数字，检查） | `From`/`Into` | 安全，编译时验证 | `let i: i32 = 42_u8.into();` —— 只扩展 |
| `static_cast`（数字，可能失败） | `TryFrom`/`TryInto` | 安全，返回 `Result` | `let i: u8 = 300_u16.try_into()?;` —— 返回 Err |
| `dynamic_cast`（向下转换） | enum 上的 `match` / `Any::downcast_ref` | 安全 | enum 用模式匹配；trait 对象用 `Any` |
| `const_cast` | 无等效 | | Rust 无法在 safe 代码中将 `\u0026` → `\u0026mut` 转换。使用 `Cell`/`RefCell` 进行内部可变性 |
| `reinterpret_cast` | `std::mem::transmute` | **`unsafe`** | 重解释位模式。几乎总是错的 —— 优先使用 `from_le_bytes()` 等。 |

```rust
