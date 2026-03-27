# Rust 内置类型

> **你将学到什么：** Rust 的基础类型（`i32`、`u64`、`f64`、`bool`、`char`）、类型推导、显式类型注解，以及它们与 C/C++ 基本类型的比较。没有隐式转换 —— Rust 需要显式转换。

- Rust 有类型推导，但也允许显式指定类型 

|  **描述**  |            **类型**            |          **示例**          |
|:-----------------:|:------------------------------:|:-----------------------------:|
| 有符号整数   | i8, i16, i32, i64, i128, isize | -1, 42, 1_00_000, 1_00_000i64 |
| 无符号整数 | u8, u16, u32, u64, u128, usize | 0, 42, 42u32, 42u64           |
| 浮点数    | f32, f64                       | 0.0, 0.42                     |
| Unicode           | char                           | 'a', '$'                      |
| 布尔值           | bool                           | true, false                   |

- Rust 允许在数字之间任意使用 `_` 以便于阅读
----
### Rust 类型规范与赋值
- Rust 使用 `let` 关键字给变量赋值。变量类型可以在 `:` 后选择性指定
```rust
fn main() {
    let x : i32 = 42;
    // 以下两个赋值在逻辑上是等价的
    let y : u32 = 42;
    let z = 42u32;
}
``` 
- 函数参数和返回值（如果有）需要显式类型。以下函数接受 u8 参数并返回 u32
```rust
fn foo(x : u8) -> u32
{
    return x as u32 * x as u32;
}
```
- 未使用的变量前缀为 `_` 以避免编译器警告
----
# Rust 类型规范与推导
- Rust 可以根据上下文自动推导变量类型。
- [▶ 在 Rust Playground 中试试](https://play.rust-lang.org/)
```rust
fn secret_of_life_u32(x : u32) {
    println!("The u32 secret_of_life is {}", x);
}

fn secret_of_life_u8(x : u8) {
    println!("The u8 secret_of_life is {}", x);
}

fn main() {
    let a = 42; // let 关键字赋值；a 的类型是 u32
    let b = 42; // let 关键字赋值；b 的推导类型是 u8
    secret_of_life_u32(a);
    secret_of_life_u8(b);
}
```

# Rust 变量与可变性
- Rust 变量 **默认不可变**，除非使用 `mut` 关键字表示变量是可变的。例如，以下代码不会编译，除非将 `let a = 42` 改为 `let mut a = 42`
```rust
fn main() {
    let a = 42; // 必须改为 let mut a = 42 才能允许下面的赋值
    a = 43;  // 除非上面更改，否则不会编译
}
```
- Rust 允许重用变量名（遮蔽）
```rust
fn main() {
    let a = 42;
    {
        let a = 43; //正常：同名不同变量
    }
    // a = 43; // 不允许
    let a = 43; // 正常：新变量和赋值
}
```

