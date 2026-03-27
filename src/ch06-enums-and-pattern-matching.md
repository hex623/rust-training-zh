# Rust 枚举类型

> **你将学到什么：** Rust 枚举作为判别联合（正确实现的标记联合），`match` 用于穷尽式模式匹配，以及枚举如何以编译器强制执行的安全性替代 C++ 类层次结构和 C 标记联合。

- 枚举类型是判别联合，即它们是几种可能不同类型的和类型，带有标识具体变体的标签
    - 对于 C 开发者：Rust 中的枚举可以携带数据（正确实现的标记联合 —— 编译器跟踪哪个变体是活动的）
    - 对于 C++ 开发者：Rust 枚举类似于 `std::variant`，但有穷尽式模式匹配，没有 `std::get` 异常，也没有 `std::visit` 样板代码
    - `enum` 的大小是最大可能类型的大小。单个变体彼此无关，可以有完全不同的类型
    - `enum` 类型是语言最强大的特性之一 —— 它们替代 C++ 中的整个类层次结构（更多内容见案例研究）
```rust
fn main() {
    enum Numbers {
        Zero,
        SmallNumber(u8),
        BiggerNumber(u32),
        EvenBiggerNumber(u64),
    }
    let a = Numbers::Zero;
    let b = Numbers::SmallNumber(42);
    let c : Numbers = a; // 正常 -- a 的类型是 Numbers
    let d : Numbers = b; // 正常 -- b 的类型是 Numbers
}
```
----
# Rust match 语句
- Rust 的 `match` 是增强版 C "switch"
    - `match` 可用于简单数据类型、`struct`、`enum` 的模式匹配
    - `match` 语句必须是穷尽的，即必须覆盖给定 `type` 的所有可能情况。`_` 可以用作"所有其他"情况的通配符
    - `match` 可以产生一个值，但所有分支（`=>`）必须返回相同类型的值

```rust
fn main() {
    let x = 42;
    // 在这种情况下，_ 覆盖除显式列出的所有数字
    let is_secret_of_life = match x {
        42 => true, // 返回类型是布尔值
        _ => false, // 返回类型布尔值
        // 这不会编译，因为返回类型不是布尔值
        // _ => 0  
    };
    println!("{is_secret_of_life}");
}
```

# Rust match 语句
- `match` 支持范围、布尔过滤器和 `if` 守卫语句
```rust
fn main() {
    let x = 42;
    match x {
        // 注意 =41 确保包含范围
        0..=41 => println!("小于生命秘密"),
        42 => println!("生命秘密"),
        _ => println!("大于生命秘密"),
    }
    let y = 100;
    match y {
        100 if x == 43 => println!("y 是 100% 不是生命秘密"),
        100 if x == 42 => println!("y 是 100% 生命秘密"),
        _ => (),    // 什么都不做
    }
}
```

# Rust match 语句
- `match` 和 `enum` 经常一起使用
    - match 语句可以将包含的值绑定到变量。如果值是不关心的，使用 `_`
    - `matches!` 宏可用于匹配特定变体
```rust
fn main() {
    enum Numbers {
        Zero,
        SmallNumber(u8),
        BiggerNumber(u32),
        EvenBiggerNumber(u64),
    }
    let b = Numbers::SmallNumber(42);
    match b {
        Numbers::Zero => println!("Zero"),
        Numbers::SmallNumber(value) => println!("小数 {value}"),
        Numbers::BiggerNumber(_) | Numbers::EvenBiggerNumber(_) => println!("某个大数或更大的数"),
    }
    
    // 特定变体的布尔测试
    if matches!(b, Numbers::Zero | Numbers::SmallNumber(_)) {
        println!("匹配 Zero 或小数字");
    }
}
```

# Rust match 语句
- `match` 还可以使用解构和切片进行匹配
```rust
fn main() {
    struct Foo {
        x: (u32, bool),
        y: u32
    }
    let f = Foo {x: (42, true), y: 100};
    match f {
        // 将 x 的值捕获到名为 tuple 的变量
        Foo{y: 100, x : tuple} => println!("匹配 x: {tuple:?}"),
        _ => ()
    }
    let a = [40, 41, 42];
    match a {
        // 切片的最后一个元素必须是 42。@ 用于绑定匹配
        [rest @ .., 42] => println!("{rest:?}"),
        // 切片的第一个元素必须是 42。@ 用于绑定匹配
        [42, rest @ ..] => println!("{rest:?}"),
        _ => (),
    }
}
```

# 练习：使用 match 和 enum 实现加法和减法

🟢 **入门**

- 写一个函数，对无符号 64 位数字实现算术运算
- **步骤 1**：定义运算枚举：
```rust
enum Operation {
    Add(u64, u64),
    Subtract(u64, u64),
}
```
- **步骤 2**：定义结果枚举：
```rust
enum CalcResult {
    Ok(u64),                    // 成功结果
    Invalid(String),            // 无效运算的错误信息
}
```
- **步骤 3**：实现 `calculate(op: Operation) -> CalcResult`
    - 对于 Add：返回 Ok(和)
    - 对于 Subtract：如果第一个 >= 第二个返回 Ok(差)，否则返回 Invalid("下溢")
- **提示**：在函数中使用模式匹配：
```rust
match op {
    Operation::Add(a, b) => { /* 你的代码 */ },
    Operation::Subtract(a, b) => { /* 你的代码 */ },
}
```

<details><summary>解答（点击展开）</summary>

```rust
enum Operation {
    Add(u64, u64),
    Subtract(u64, u64),
}

enum CalcResult {
    Ok(u64),
    Invalid(String),
}

fn calculate(op: Operation) -> CalcResult {
    match op {
        Operation::Add(a, b) => CalcResult::Ok(a + b),
        Operation::Subtract(a, b) => {
            if a >= b {
                CalcResult::Ok(a - b)
            } else {
                CalcResult::Invalid("下溢".to_string())
            }
        }
    }
}

fn main() {
    match calculate(Operation::Add(10, 20)) {
        CalcResult::Ok(result) => println!("10 + 20 = {result}"),
        CalcResult::Invalid(msg) => println!("错误: {msg}"),
    }
    match calculate(Operation::Subtract(5, 10)) {
        CalcResult::Ok(result) => println!("5 - 10 = {result}"),
        CalcResult::Invalid(msg) => println!("错误: {msg}"),
    }
}
// 输出：
// 10 + 20 = 30
// 错误: 下溢
```

</details>

# Rust 关联方法
- `impl` 可以为类型（如 `struct`、`enum` 等）定义关联方法
    - 方法可以选择性地将 `self` 作为参数。`self` 在概念上类似于 C 中将指向结构体的指针作为第一个参数传递，或 C++ 中的 `this`
    - 对 `self` 的引用可以是不可变的（默认：`&self`）、可变的（`&mut self`）或 `self`（转移所有权）
    - `Self` 关键字可用作类型的快捷方式
```rust
struct Point {x: u32, y: u32}
impl Point {
    fn new(x: u32, y: u32) -> Self {
        Point {x, y}
    }
    fn increment_x(&mut self) {
        self.x += 1;
    }
}
fn main() {
    let mut p = Point::new(10, 20);
    p.increment_x();
}
```

# 练习：Point 的 add 和 transform

🟡 **中级** —— 需要理解从方法签名看移动 vs 借用
- 为 `Point` 实现以下关联方法
    - `add()` 将接受另一个 `Point` 并就地增加 x 和 y 值（提示：使用 `&mut self`）
    - `transform()` 将消耗一个现有的 `Point`（提示：使用 `self`）并返回一个新的 `Point`，将 x 和 y 平方

<details><summary>解答（点击展开）</summary>

```rust
struct Point { x: u32, y: u32 }

impl Point {
    fn new(x: u32, y: u32) -> Self {
        Point { x, y }
    }
    fn add(&mut self, other: &Point) {
        self.x += other.x;
        self.y += other.y;
    }
    fn transform(self) -> Point {
        Point { x: self.x * self.x, y: self.y * self.y }
    }
}

fn main() {
    let mut p1 = Point::new(2, 3);
    let p2 = Point::new(10, 20);
    p1.add(&p2);
    println!("add 后: x={}, y={}", p1.x, p1.y);           // x=12, y=23
    let p3 = p1.transform();
    println!("transform 后: x={}, y={}", p3.x, p3.y);     // x=144, y=529
    // p1 不再可访问 —— transform() 消耗了它
}
```

</details>

----
