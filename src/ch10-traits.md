# Rust trait

> **你将学到什么：** Trait —— Rust 对接口、抽象基类和运算符重载的回答。你将学习如何定义 trait、为类型实现它们，以及使用动态分发（`dyn Trait`）vs 静态分发（泛型）。面向 C++ 开发者：trait 替代虚函数、CRTP 和概念。面向 C 开发者：trait 是 Rust 实现多态的结构化方式。

- Rust trait 类似于其他语言中的接口
    - Trait 定义了实现该 trait 的类型必须定义的方法。
```rust
fn main() {
    trait Pet {
        fn speak(&self);
    }
    struct Cat;
    struct Dog;
    impl Pet for Cat {
        fn speak(&self) {
            println!("喵");
        }
    }
    impl Pet for Dog {
        fn speak(&self) {
            println!("汪!")
        }
    }
    let c = Cat{};
    let d = Dog{};
    c.speak();  // Cat 和 Dog 之间没有 "is a" 关系
    d.speak(); // Cat 和 Dog 之间没有 "is a" 关系
}
```

## Trait vs C++ 概念和接口

### 传统 C++ 继承 vs Rust Trait

```cpp
// C++ - 基于继承的多态
class Animal {
public:
    virtual void speak() = 0;  // 纯虚函数
    virtual ~Animal() = default;
};

class Cat : public Animal {  // "Cat IS-A Animal"
public:
    void speak() override {
        std::cout << "Meow" << std::endl;
    }
};

void make_sound(Animal* animal) {  // 运行时多态
    animal->speak();  // 虚函数调用
}
```

```rust
// Rust - 使用 trait 的组合优于继承
trait Animal {
    fn speak(&self);
}

struct Cat;  // Cat 不是 Animal，但实现了 Animal 行为

impl Animal for Cat {  // "Cat CAN-DO Animal behavior"
    fn speak(&self) {
        println!("喵");
    }
}

fn make_sound<T: Animal>(animal: &T) {  // 静态多态
    animal.speak();  // 直接函数调用（零成本）
}
```

```mermaid
graph TD
    subgraph "C++ 面向对象层次结构"
        CPP_ANIMAL["Animal<br/>(抽象基类)"]
        CPP_CAT["Cat : public Animal<br/>(IS-A 关系)"]
        CPP_DOG["Dog : public Animal<br/>(IS-A 关系)"]
        
        CPP_ANIMAL --> CPP_CAT
        CPP_ANIMAL --> CPP_DOG
        
        CPP_VTABLE["虚函数表<br/>(运行时分发)"]
        CPP_HEAP["通常需要<br/>堆分配"]
        CPP_ISSUES["[错误] 深层继承树<br/>[错误] 菱形问题<br/>[错误] 运行时开销<br/>[错误] 紧耦合"]
    end
    
    subgraph "Rust 基于 Trait 的组合"
        RUST_TRAIT["trait Animal<br/>(行为定义)"]
        RUST_CAT["struct Cat<br/>(仅数据)"]
        RUST_DOG["struct Dog<br/>(仅数据)"]
        
        RUST_CAT -.->|"impl Animal for Cat<br/>(CAN-DO 行为)"| RUST_TRAIT
        RUST_DOG -.->|"impl Animal for Dog<br/>(CAN-DO 行为)"| RUST_TRAIT
        
        RUST_STATIC["静态分发<br/>(编译时)"]
        RUST_STACK["栈分配<br/>可能"]
        RUST_BENEFITS["[正常] 无继承层次<br/>[正常] 多 trait 实现<br/>[正常] 零运行时成本<br/>[正常] 松耦合"]
    end
    
    style CPP_ISSUES fill:#ff6b6b,color:#000
    style RUST_BENEFITS fill:#91e5a3,color:#000
    style CPP_VTABLE fill:#ffa07a,color:#000
    style RUST_STATIC fill:#91e5a3,color:#000
```

### Trait Bounds 和泛型约束

```rust
use std::fmt::Display;
use std::ops::Add;

// C++ 模板等效（约束较少）
// template<typename T>
// T add_and_print(T a, T b) {
//     // 不保证 T 支持 + 或打印
//     return a + b;  // 可能在编译时失败
// }

// Rust - 显式 trait bounds
fn add_and_print<T>(a: T, b: T) -> T 
where 
    T: Display + Add<Output = T> + Copy,
{
    println!("Adding {} + {}", a, b);  // Display trait
    a + b  // Add trait
}
```

### C++ 运算符重载 → Rust `std::ops` Trait

在 C++ 中，你通过编写具有特殊名称的自由函数或成员函数来重载运算符（`operator+`、`operator<<`、`operator[]` 等）。在 Rust 中，每个运算符映射到 `std::ops`（或 `std::fmt` 用于输出）中的一个 trait。你 **实现 trait** 而不是编写具有魔法名称的函数。

#### 并排比较：`+` 运算符

```cpp
// C++：作为成员或自由函数的运算符重载
struct Vec2 {
    double x, y;
    Vec2 operator+(const Vec2& rhs) const {
        return {x + rhs.x, y + rhs.y};
    }
};

Vec2 a{1.0, 2.0}, b{3.0, 4.0};
Vec2 c = a + b;  // 调用 a.operator+(b)
```

```rust
use std::ops::Add;

#[derive(Debug, Clone, Copy)]
struct Vec2 { x: f64, y: f64 }

impl Add for Vec2 {
    type Output = Vec2;                     // 关联类型 — + 的结果
    fn add(self, rhs: Vec2) -> Vec2 {
        Vec2 { x: self.x + rhs.x, y: self.y + rhs.y }
    }
}

let a = Vec2 { x: 1.0, y: 2.0 };
let b = Vec2 { x: 3.0, y: 4.0 };
let c = a + b;  // 调用 <Vec2 as Add>::add(a, b)
println!("{c:?}"); // Vec2 { x: 4.0, y: 6.0 }
```

#### 与 C++ 的关键区别

| 方面 | C++ | Rust |
|--------|-----|------|
| **机制** | 魔法函数名称（`operator+`） | 实现 trait（`impl Add for T`） |
| **发现** | 搜索 `operator+` 或阅读头文件 | 查看 trait 实现 —— IDE 支持优秀 |
| **返回类型** | 自由选择 | 由 `Output` 关联类型固定 |
| **接收者** | 通常取 `const T&`（借用） | 默认按值取 `self`（移动！） |
| **对称性** | 可以写 `impl operator+(int, Vec2)` | 必须添加 `impl Add<Vec2> for i32`（适用孤儿规则） |
| **`<<` 用于打印** | `operator<<(ostream&, T)` —— 为 *任何* 流重载 | `impl fmt::Display for T` —— 一个规范的 `to_string` 表示 |

#### `self` 按值的问题

在 Rust 中，`Add::add(self, rhs)` 按值取 `self`。对于 `Copy` 类型（如上面的 `Vec2`，它派生 `Copy`）这没问题 —— 编译器会拷贝。但对于非 `Copy` 类型，`+` **消耗** 操作数：

```rust
let s1 = String::from("hello ");
let s2 = String::from("world");
let s3 = s1 + &s2;  // s1 被移入 s3！
// println!("{s1}");  // ❌ 编译错误：移动后使用值
println!("{s2}");     // ✅ s2 只是被借用（&s2）
```

这就是 `String + &str` 有效但 `&str + &str` 无效的原因 —— `Add` 只为 `String + &str` 实现，消耗左侧的 `String` 以重用其缓冲区。这在 C++ 中没有对应：`std::string::operator+` 总是创建新字符串。

#### 完整映射：C++ 运算符 → Rust trait

| C++ 运算符 | Rust Trait | 说明 |
|-------------|-----------|-------|
| `operator+` | `std::ops::Add` | `Output` 关联类型 |
| `operator-` | `std::ops::Sub` | |
| `operator*` | `std::ops::Mul` | 不是指针解引用 —— 那是 `Deref` |
| `operator/` | `std::ops::Div` | |
| `operator%` | `std::ops::Rem` | |
| `operator-`（一元） | `std::ops::Neg` | |
| `operator!` / `operator~` | `std::ops::Not` | Rust 对逻辑和位 NOT 都用 `!`（没有 `~` 运算符） |
| `operator&`, `|`, `^` | `BitAnd`, `BitOr`, `BitXor` | |
| `operator<<`, `>>`（移位） | `Shl`, `Shr` | 不是流 I/O！ |
| `operator+=` | `std::ops::AddAssign` | 取 `&mut self`（不是 `self`） |
| `operator[]` | `std::ops::Index` / `IndexMut` | 返回 `&Output` / `&mut Output` |
| `operator()` | `Fn` / `FnMut` / `FnOnce` | 闭包实现这些；你不能直接 `impl Fn` |
| `operator==` | `PartialEq` (+ `Eq`) | 在 `std::cmp` 中，不在 `std::ops` |
| `operator<` | `PartialOrd` (+ `Ord`) | 在 `std::cmp` 中 |
| `operator<<`（流） | `fmt::Display` | `println!("{}", x)` |
| `operator<<`（调试） | `fmt::Debug` | `println!("{:?}", x)` |
| `operator bool` | 无直接等效 | 使用 `impl From<T> for bool` 或命名方法如 `.is_empty()` |
| `operator T()`（隐式转换） | 无隐式转换 | 使用 `From`/`Into` trait（显式） |

#### 防护栏：Rust 阻止什么

1. **无隐式转换**：C++ `operator int()` 可导致静默、意外的转换。Rust 没有隐式转换运算符 —— 使用 `From`/`Into` 并显式调用 `.into()`。
2. **不重载 `&&` / `||`**：C++ 允许（破坏短路语义！）。Rust 不允许。
3. **不重载 `=`**：赋值总是移动或拷贝，从不用户定义。复合赋值（`+=`）可通过 `AddAssign` 等重载。
4. **不重载 `,`**：C++ 允许 `operator,()` —— 最著名的 C++ 坑之一。Rust 不允许。
5. **不重载 `&`（取地址）**：另一个 C++ 坑（`std::addressof` 存在来解决它）。Rust 的 `&` 始终表示"借用"。
6. **一致性规则**：你只能为 `Add<Foreign>` 为你自己的类型实现，或为 `Add<YourType>` 为外部类型实现 —— 绝不为 `Add<Foreign>` 为 `Foreign` 实现。这防止跨 crate 的冲突运算符定义。

> **底线**：在 C++ 中，运算符重载强大但基本无监管 —— 你几乎可以重载任何东西，包括逗号和取地址，隐式转换可静默触发。Rust 通过 trait 给你算术和比较运算符相同的表达能力，但 **阻止历史上危险的重载** 并强制所有转换都是显式的。

----
# Rust trait
- Rust 允许在甚至内置类型如本例中的 u32 上实现用户定义的 trait。然而，trait 或类型必须属于该 crate
```rust
trait IsSecret {
  fn is_secret(&self);
}
// IsSecret trait 属于该 crate，所以我们没问题
impl IsSecret for u32 {
  fn is_secret(&self) {
      if *self == 42 {
          println!("是生命秘密");
      }
  }
}

fn main() {
  42u32.is_secret();
  43u32.is_secret();
}
```


# Rust trait
- Trait 支持接口继承和默认实现
```rust
trait Animal {
  // 默认实现
  fn is_mammal(&self) -> bool {
    true
  }
}
trait Feline : Animal {
  // 默认实现
  fn is_feline(&self) -> bool {
    true
  }
}

struct Cat;
// 使用默认实现。注意 supertrait 的所有 trait 必须单独实现
impl Feline for Cat {}
impl Animal for Cat {}
fn main() {
  let c = Cat{};
  println!("{} {}", c.is_mammal(), c.is_feline());
}
```
----
# 练习：Logger trait 实现

🟡 **中级**

- 实现一个带有单个方法 `log()` 的 `Log trait`，接受 u64
    - 实现两个不同的 logger `SimpleLogger` 和 `ComplexLogger` 实现 `Log trait`。一个应该输出 "Simple logger" 带 `u64`，另一个应该输出 "Complex logger" 带 `u64`

<details><summary>解答（点击展开）</summary>

```rust
trait Log {
    fn log(&self, value: u64);
}

struct SimpleLogger;
struct ComplexLogger;

impl Log for SimpleLogger {
    fn log(&self, value: u64) {
        println!("Simple logger: {value}");
    }
}

impl Log for ComplexLogger {
    fn log(&self, value: u64) {
        println!("Complex logger: {value} (hex: 0x{value:x}, binary: {value:b})");
    }
}

fn main() {
    let simple = SimpleLogger;
    let complex = ComplexLogger;
    simple.log(42);
    complex.log(42);
}
// 输出：
// Simple logger: 42
// Complex logger: 42 (hex: 0x2a, binary: 101010)
```

</details>

----
# Rust trait 关联类型
```rust
#[derive(Debug)]
struct Small(u32);
#[derive(Debug)]
struct Big(u32);
trait Double {
    type T;
    fn double(&self) -> Self::T;
}

impl Double for Small {
    type T = Big;
    fn double(&self) -> Self::T {
        Big(self.0 * 2)
    }
}
fn main() {
    let a = Small(42);
    println!("{:?}", a.double());
}
```

# Rust trait impl
- `impl` 可以与 trait 一起使用来接受任何实现 trait 的类型
```rust
trait Pet {
    fn speak(&self);
}
struct Dog {}
struct Cat {}
impl Pet for Dog {
    fn speak(&self) {println!("汪!")}
}
impl Pet for Cat {
    fn speak(&self) {println!("喵")}
}
fn pet_speak(p: &impl Pet) {
    p.speak();
}
fn main() {
    let c = Cat {};
    let d = Dog {};
    pet_speak(&c);
    pet_speak(&d);
}
```

# Rust trait impl
- `impl` 也可以用于返回值
```rust
trait Pet {}
struct Dog;
struct Cat;
impl Pet for Cat {}
impl Pet for Dog {}
fn cat_as_pet() -> impl Pet {
    let c = Cat {};
    c
}
fn dog_as_pet() -> impl Pet {
    let d = Dog {};
    d
}
fn main() {
    let p = cat_as_pet();
    let d = dog_as_pet();
}
```
----
# Rust 动态 trait
- 动态 trait 可用于在不知道底层类型的情况下调用 trait 功能。这被称为 `类型擦除`
```rust
trait Pet {
    fn speak(&self);
}
struct Dog {}
struct Cat {x: u32}
impl Pet for Dog {
    fn speak(&self) {println!("汪!")}
}
impl Pet for Cat {
    fn speak(&self) {println!("喵")}
}
fn pet_speak(p: &dyn Pet) {
    p.speak();
}
fn main() {
    let c = Cat {x: 42};
    let d = Dog {};
    pet_speak(&c);
    pet_speak(&d);
}
```
----

## 在 `impl Trait`、`dyn Trait` 和 Enum 之间选择

这三种方法都实现多态性，但有不同的权衡：

| 方法 | 分发 | 性能 | 异构集合？ | 何时使用 |
|----------|----------|-------------|---------------------------|-------------|
| `impl Trait` / 泛型 | 静态（单态化） | 零成本 —— 编译时内联 | 否 —— 每个槽位有一个具体类型 | 默认选择。函数参数、返回类型 |
| `dyn Trait` | 动态（vtable） | 每次调用小开销（~1 个指针间接） | 是 —— `Vec<Box<dyn Trait>>` | 当你需要在集合中混合类型，或插件式可扩展性时 |
| `enum` | 匹配 | 零成本 —— 编译时已知变体 | 是 —— 但只有已知变体 | 当变体集合 **封闭** 且编译时已知时 |

```rust
trait Shape {
    fn area(&self) -> f64;
}
struct Circle { radius: f64 }
struct Rect { w: f64, h: f64 }
impl Shape for Circle { fn area(&self) -> f64 { std::f64::consts::PI * self.radius * self.radius } }
impl Shape for Rect   { fn area(&self) -> f64 { self.w * self.h } }

// 静态分发 —— 编译器为每种类型生成单独代码
fn print_area(s: &impl Shape) { println!("{}", s.area()); }

// 动态分发 —— 一个函数，适用于任何 Shape 背后的指针
fn print_area_dyn(s: &dyn Shape) { println!("{}", s.area()); }

// Enum —— 封闭集合，不需要 trait
enum ShapeEnum { Circle(f64), Rect(f64, f64) }
impl ShapeEnum {
    fn area(&self) -> f64 {
        match self {
            ShapeEnum::Circle(r) => std::f64::consts::PI * r * r,
            ShapeEnum::Rect(w, h) => w * h,
        }
    }
}
```

> **面向 C++ 开发者：** `impl Trait` 像 C++ 模板（单态化，零成本）。`dyn Trait` 像 C++ 虚函数（vtable 分发）。带 `match` 的 Rust enum 像 `std::variant` 带 `std::visit` —— 但穷尽匹配由编译器强制执行。

> **经验法则**：从 `impl Trait`（静态分发）开始。只有当你需要异构集合或无法在编译时知道具体类型时才使用 `dyn Trait`。当你拥有所有变体时使用 `enum`。
