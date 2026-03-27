### Rust 数组类型

> **你将学到什么：** Rust 的核心数据结构 —— 数组、元组、切片、字符串、结构体、`Vec` 和 `HashMap`。这是密集的一章；重点理解 `String` vs `&str` 以及结构体如何工作。你将在第7章深入回顾引用和借用。

- 数组包含固定数量的相同类型元素
    - 像所有其他 Rust 类型一样，数组默认不可变（除非使用 mut）
    - 数组使用 [] 索引，并且是边界检查的。len() 方法可用于获取数组长度
```rust
    fn get_index(y : usize) -> usize {
        y+1        
    }
    
    fn main() {
        // 初始化一个包含 10 个元素的数组，全部设为 42
        let a : [u8; 3] = [42; 3];
        // 替代语法
        // let a = [42u8, 42u8, 42u8];
        for x in a {
            println!("{x}");
        }
        let y = get_index(a.len());
        // 注释掉下面的代码会导致 panic
        //println!("{}", a[y]);
    }
```

----
### Rust 数组类型（续）
- 数组可以嵌套
    - Rust 有几种内置的打印格式化器。在下面，`:?` 是 `debug` 打印格式化器。`:#?` 格式化器可用于 `pretty print`。这些格式化器可以按类型自定义（稍后详述）
```rust
    fn main() {
        let a = [
            [40, 0], // 定义嵌套数组
            [41, 0],
            [42, 1],
        ];
        for x in a {
            println!("{x:?}");
        }
    }
```
----
### Rust 元组
- 元组有固定大小，可以将任意类型组合成单一复合类型
    - 组成类型可以通过相对位置索引（.0、.1、.2、...）。空元组，即 () 称为单元值，等同于 void 返回值
    - Rust 支持元组解构，便于将变量绑定到单个元素
```rust
fn get_tuple() -> (u32, bool) {
    (42, true)        
}

fn main() {
   let t : (u8, bool) = (42, true);
   let u : (u32, bool) = (43, false);
   println!("{}, {}", t.0, t.1);
   println!("{}, {}", u.0, u.1);
   let (num, flag) = get_tuple(); // 元组解构
   println!("{num}, {flag}");
}
```

### Rust 引用
- Rust 中的引用大致等同于 C 中的指针，但有一些关键区别
    - 在任何时候拥有任意数量的只读（不可变）引用是合法的。引用不能比变量作用域活得更长（这是称为 **生命周期** 的关键概念；稍后详细讨论）
    - 只允许对可变变量有一个可写（可变）引用，并且它不能与其他任何引用重叠。
```rust
fn main() {
    let mut a = 42;
    {
        let b = &a;
        let c = b;
        println!("{} {}", *b, *c); // 编译器自动解引用 *c
        // 非法，因为 b 和 c 仍在作用域内
        // let d = &mut a;
    }
    let d = &mut a; // 正常：b 和 c 不在作用域内
    *d = 43;
}
```

----
# Rust 切片
- Rust 引用可用于创建数组的子集
    - 与在编译时确定静态固定大小的数组不同，切片可以是任意大小。内部实现为"胖指针"，包含切片长度和指向原始数组起始元素的指针
```rust
fn main() {
    let a = [40, 41, 42, 43];
    let b = &a[1..a.len()]; // 从原始数组第二个元素开始的切片
    let c = &a[1..]; // 与上面相同
    let d = &a[..]; // 等同于 &a[0..] 或 &a[0..a.len()]
    println!("{b:?} {c:?} {d:?}");
}
```
----
# Rust 常量与静态变量
- `const` 关键字可用于定义常量值。常量值在 **编译时** 求值并内联到程序中
- `static` 关键字用于定义类似 C/C++ 中全局变量的等效物。静态变量有可寻址的内存位置，创建一次并持续程序的整个生命周期
```rust
const SECRET_OF_LIFE: u32 = 42;
static GLOBAL_VARIABLE : u32 = 2;
fn main() {
    println!("生命秘密是 {}", SECRET_OF_LIFE);
    println!("全局变量值是 {GLOBAL_VARIABLE}")
}
```

----
# Rust 字符串：String vs &str

- Rust 有 **两种** 字符串类型，服务于不同目的
    - `String` —— 拥有的、堆分配的、可增长的（类似 C 的 `malloc` 缓冲区，或 C++ 的 `std::string`）
    - `&str` —— 借用的、轻量级引用（类似 C 的 `const char*` 带长度，或 C++ 的 `std::string_view` —— 但 `&str` 是 **生命周期检查的**，所以永远不会悬空）
    - 与 C 的空终止字符串不同，Rust 字符串跟踪其长度并保证有效的 UTF-8

> **面向 C++ 开发者：** `String` ≈ `std::string`，`&str` ≈ `std::string_view`。与 `std::string_view` 不同，`&str` 通过借用检查器保证在其整个生命周期内有效。

## String vs &str：拥有的 vs 借用的

> **生产模式：** 参见 [JSON 处理：nlohmann::json → serde](ch17-2-avoiding-unchecked-indexing.md#json-处理-nlohmannjson--serde) 了解生产代码中 serde 如何处理字符串。

| **方面** | **C `char*`** | **C++ `std::string`** | **Rust `String`** | **Rust `&str`** |
|------------|--------------|----------------------|-------------------|----------------|
| **内存** | 手动 (`malloc`/`free`) | 堆分配，拥有缓冲区 | 堆分配，自动释放 | 借用引用（生命周期检查） |
| **可变性** | 总是可通过指针可变 | 可变 | 用 `mut` 可变 | 总是不可变 |
| **大小信息** | 无（依赖 `'\0'`） | 跟踪长度和容量 | 跟踪长度和容量 | 跟踪长度（胖指针） |
| **编码** | 未指定（通常是 ASCII） | 未指定（通常是 ASCII） | 保证有效 UTF-8 | 保证有效 UTF-8 |
| **空终止** | 需要 | 需要（`c_str()`） | 不使用 | 不使用 |

```rust
fn main() {
    // &str - 字符串切片（借用的、不可变的，通常是字符串字面量）
    let greeting: &str = "Hello";  // 指向只读内存

    // String - 拥有的、堆分配的、可增长的
    let mut owned = String::from(greeting);  // 复制数据到堆
    owned.push_str(", World!");        // 增长字符串
    owned.push('!');                   // 追加单个字符

    // String 和 &str 之间的转换
    let slice: &str = &owned;          // String -> &str（免费，只是借用）
    let owned2: String = slice.to_string();  // &str -> String（分配）
    let owned3: String = String::from(slice); // 同上

    // 字符串连接（注意：+ 消耗左操作数）
    let hello = String::from("Hello");
    let world = String::from(", World!");
    let combined = hello + &world;  // hello 被移动（消耗），world 被借用
    // println!("{hello}");  // 不会编译：hello 已被移动

    // 使用 format! 避免移动问题
    let a = String::from("Hello");
    let b = String::from("World");
    let combined = format!("{a}, {b}!");  // a 和 b 都不会被消耗

    println!("{combined}");
}
```

## 为什么不能用 `[]` 索引字符串
```rust
fn main() {
    let s = String::from("hello");
    // let c = s[0];  // 不会编译！Rust 字符串是 UTF-8，不是字节数组

    // 安全的替代方案：
    let first_char = s.chars().next();           // Option<char>: Some('h')
    let as_bytes = s.as_bytes();                 // &[u8]: 原始 UTF-8 字节
    let substring = &s[0..1];                    // &str: "h"（字节范围，必须是有效的 UTF-8 边界）

    println!("第一个字符: {:?}", first_char);
    println!("字节: {:?}", &as_bytes[..5]);
}
```

## 练习：字符串操作

🟢 **入门**
- 写一个函数 `fn count_words(text: &str) -> usize` 计算字符串中空格分隔的单词数量
- 写一个函数 `fn longest_word(text: &str) -> &str` 返回最长的单词（提示：你需要考虑生命周期 —— 为什么返回类型需要是 `&str` 而不是 `String`？）

<details><summary>解答（点击展开）</summary>

```rust
fn count_words(text: &str) -> usize {
    text.split_whitespace().count()
}

fn longest_word(text: &str) -> &str {
    text.split_whitespace()
        .max_by_key(|word| word.len())
        .unwrap_or("")
}

fn main() {
    let text = "the quick brown fox jumps over the lazy dog";
    println!("单词数: {}", count_words(text));       // 9
    println!("最长单词: {}", longest_word(text));     // "jumps"
}
```

</details>

# Rust 结构体
- `struct` 关键字声明用户定义的结构体类型
    - `struct` 成员可以是有名的，也可以是匿名的（元组结构体）
- 与 C++ 等语言不同，Rust 中没有"数据继承"的概念
```rust
fn main() {
    struct MyStruct {
        num: u32,
        is_secret_of_life: bool,
    }
    let x = MyStruct {
        num: 42,
        is_secret_of_life: true,
    };
    let y = MyStruct {
        num: x.num,
        is_secret_of_life: x.is_secret_of_life,
    };
    let z = MyStruct { num: x.num, ..x }; // .. 表示复制剩余的
    println!("{} {} {}", x.num, y.is_secret_of_life, z.num);
}
```

# Rust 元组结构体
- Rust 元组结构体类似于元组，单个字段没有名称
    - 像元组一样，单个元素使用 .0、.1、.2、.... 访问。元组结构体的常见用例是包装基本类型以创建自定义类型。**这有助于避免混合不同类型的值**
```rust
struct WeightInGrams(u32);
struct WeightInMilligrams(u32);
fn to_weight_in_grams(kilograms: u32) -> WeightInGrams {
    WeightInGrams(kilograms * 1000)
}

fn to_weight_in_milligrams(w : WeightInGrams) -> WeightInMilligrams  {
    WeightInMilligrams(w.0 * 1000)
}

fn main() {
    let x = to_weight_in_grams(42);
    let y = to_weight_in_milligrams(x);
    // let z : WeightInGrams = x;  // 不会编译：x 已被移入 to_weight_in_milligrams()
    // let a : WeightInGrams = y;   // 不会编译：类型不匹配（WeightInMilligrams vs WeightInGrams）
}
```


**注意**：`#[derive(...)]` 属性自动为结构体和枚举生成常见的 trait 实现。你将在整个课程中看到这种用法：
```rust
#[derive(Debug, Clone, PartialEq)]
struct Point { x: i32, y: i32 }

fn main() {
    let p = Point { x: 1, y: 2 };
    println!("{:?}", p);           // Debug: 因为 #[derive(Debug)] 而工作
    let p2 = p.clone();           // Clone: 因为 #[derive(Clone)] 而工作
    assert_eq!(p, p2);            // PartialEq: 因为 #[derive(PartialEq)] 而工作
}
```
我们稍后将深入讨论 trait 系统，但 `#[derive(Debug)]` 非常有用，你应该为你创建的几乎每个 `struct` 和 `enum` 添加它。

# Rust Vec 类型
- `Vec<T>` 类型实现动态堆分配缓冲区（类似 C 中手动管理的 `malloc`/`realloc` 数组，或 C++ 的 `std::vector`）
    - 与固定大小的数组不同，`Vec` 可以在运行时增长和收缩
    - `Vec` 拥有其数据并自动管理内存分配/释放
- 常用操作：`push()`、`pop()`、`insert()`、`remove()`、`len()`、`capacity()`
```rust
fn main() {
    let mut v = Vec::new();    // 空向量，类型从使用推断
    v.push(42);                // 在末尾添加元素 - Vec<i32>
    v.push(43);                
    
    // 安全迭代（推荐）
    for x in &v {              // 借用元素，不消耗向量
        println!("{x}");
    }
    
    // 初始化快捷方式
    let mut v2 = vec![1, 2, 3, 4, 5];           // 初始化的宏
    let v3 = vec![0; 10];                       // 10 个零
    
    // 安全访问方法（比索引更好）
    match v2.get(0) {
        Some(first) => println!("第一个: {first}"),
        None => println!("空向量"),
    }
    
    // 有用的方法
    println!("长度: {}, 容量: {}", v2.len(), v2.capacity());
    if let Some(last) = v2.pop() {             // 移除并返回最后一个元素
        println!("弹出: {last}");
    }
    
    // 危险：直接索引（可能 panic！）
    // println!("{}", v2[100]);  // 会在运行时 panic
}
```
> **生产模式**：参见 [避免未检查索引](ch17-2-avoiding-unchecked-indexing.md#避免未检查索引) 了解生产 Rust 代码中安全的 `.get()` 模式。

# Rust HashMap 类型
- `HashMap` 实现泛型 `key` -> `value` 查找（又称 `dictionary` 或 `map`）
```rust
fn main() {
    use std::collections::HashMap;  // 需要显式导入，不像 Vec
    let mut map = HashMap::new();       // 分配空 HashMap
    map.insert(40, false);  // 类型推断为 int -> bool
    map.insert(41, false);
    map.insert(42, true);
    for (key, value) in map {
        println!("{key} {value}");
    }
    let map = HashMap::from([(40, false), (41, false), (42, true)]);
    if let Some(x) = map.get(&43) {
        println!("43 映射到 {x:?}");
    } else {
        println!("没有找到 43 的映射");
    }
    let x = map.get(&43).or(Some(&false));  // 如果未找到键则返回默认值
    println!("{x:?}"); 
}
```

# 练习：Vec 和 HashMap

🟢 **入门**
- 创建一个 `HashMap<u32, bool>`，包含几个条目（确保一些值是 `true`，另一些是 `false`）。遍历哈希映射中的所有元素，将键放入一个 `Vec`，将值放入另一个

<details><summary>解答（点击展开）</summary>

```rust
use std::collections::HashMap;

fn main() {
    let map = HashMap::from([(1, true), (2, false), (3, true), (4, false)]);
    let mut keys = Vec::new();
    let mut values = Vec::new();
    for (k, v) in &map {
        keys.push(*k);
        values.push(*v);
    }
    println!("键:   {keys:?}");
    println!("值: {values:?}");

    // 替代方案：使用迭代器与 unzip()
    let (keys2, values2): (Vec<u32>, Vec<bool>) = map.into_iter().unzip();
    println!("键 (unzip):   {keys2:?}");
    println!("值 (unzip): {values2:?}");
}
```

</details>

---

## 深度解析：C++ 引用 vs Rust 引用

> **面向 C++ 开发者：** C++ 程序员通常假设 Rust 的 `&T` 工作方式类似于 C++ 的 `T&`。虽然表面上相似，但存在根本差异会导致混淆。C 开发者可以跳过本节 —— Rust 引用在 [所有权与借用](ch07-ownership-and-borrowing.md) 中介绍。

#### 1. 没有右值引用或万能引用

在 C++ 中，`&&` 根据上下文有两种含义：

```cpp
// C++: && 表示不同的东西：
int&& rref = 42;           // 右值引用 —— 绑定到临时对象
void process(Widget&& w);   // 右值引用 —— 调用者必须 std::move

// 万能（转发）引用 —— 推导的模板上下文：
template<typename T>
void forward(T&& arg) {     // 不是右值引用！推导为 T& 或 T&&
    inner(std::forward<T>(arg));  // 完美转发
}
```

**在 Rust 中：这些都不存在。** `&&` 只是逻辑与运算符。

```rust
// Rust: && 只是布尔与
let a = true && false; // false

// Rust 没有右值引用，没有万能引用，没有完美转发。
// 取而代之的是：
//   - 移动是非 Copy 类型的默认行为（不需要 std::move）
//   - 泛型 + trait bounds 替代万能引用
//   - 没有临时绑定区分 —— 值就是值

fn process(w: Widget) { }      // 取得所有权（类似 C++ 值参数 + 隐式移动）
fn process_ref(w: &Widget) { } // 不可变借用（类似 C++ const T&）
fn process_mut(w: &mut Widget) { } // 可变借用（类似 C++ T&，但是独占的）
```

| C++ 概念 | Rust 等效 | 说明 |
|-------------|-----------------|-------|
| `T&` (左值引用) | `&T` 或 `&mut T` | Rust 分为共享 vs 独占 |
| `T&&` (右值引用) | 就是 `T` | 按值取 = 取得所有权 |
| 模板中的 `T&&` (万能引用) | `impl Trait` 或 `<T: Trait>` | 泛型替代转发 |
| `std::move(x)` | `x`（直接用） | 移动是默认的 |
| `std::forward<T>(x)` | 不需要等效 | 没有万能引用需要转发 |

#### 2. 移动是位拷贝 —— 没有移动构造函数

在 C++ 中，移动是 *用户定义的操作*（移动构造函数 / 移动赋值）。在 Rust 中，移动始终是 **位拷贝** 值，源被失效：

```rust
// Rust 移动 = 字节 memcpy，标记源为无效
let s1 = String::from("hello");
let s2 = s1; // s1 的字节被复制到 s2 的栈槽
              // s1 现在无效 —— 编译器强制执行
// println!("{s1}"); // ❌ 编译错误：移动后使用值
```

```cpp
// C++ 移动 = 调用移动构造函数（用户定义的！）
std::string s1 = "hello";
std::string s2 = std::move(s1); // 调用 string 的移动构造函数
// s1 现在处于"有效但未指定状态"的僵尸状态
std::cout << s1; // 编译！打印... 一些东西（通常是空字符串）
```

**后果**：
- Rust 没有 Rule of Five（不需要定义拷贝构造、移动构造、拷贝赋值、移动赋值、析构函数）
- 没有移动后的"僵尸"状态 —— 编译器只是阻止访问
- 移动没有 `noexcept` 考虑 —— 位拷贝不会抛出

#### 3. 自动解引用：编译器看穿间接

Rust 通过 `Deref` trait 自动解引用多层指针/包装器。这在 C++ 中没有等效：

```rust
use std::sync::{Arc, Mutex};

// 嵌套包装：Arc<Mutex<Vec<String>>>
let data = Arc::new(Mutex::new(vec!["hello".to_string()]));

// 在 C++ 中，你需要显式解锁和每层手动解引用。
// 在 Rust 中，编译器自动解引用 Arc → Mutex → MutexGuard → Vec：
let guard = data.lock().unwrap(); // Arc 自动解引用到 Mutex
let first: &str = &guard[0];      // MutexGuard→Vec (Deref), Vec[0] (Index),
                                   // &String→&str (Deref 强制转换)
println!("第一个: {first}");

// 方法调用也自动解引用：
let boxed_string = Box::new(String::from("hello"));
println!("长度: {}", boxed_string.len());  // Box→String, 然后 String::len()
// 不需要 (*boxed_string).len() 或 boxed_string->len()
```

**Deref 强制转换** 也适用于函数参数 —— 编译器插入解引用以使类型匹配：

```rust
fn greet(name: &str) {
    println!("Hello, {name}");
}

fn main() {
    let owned = String::from("Alice");
    let boxed = Box::new(String::from("Bob"));
    let arced = std::sync::Arc::new(String::from("Carol"));

    greet(&owned);  // &String → &str  (1 次 deref 强制转换)
    greet(&boxed);  // &Box<String> → &String → &str  (2 次 deref 强制转换)
    greet(&arced);  // &Arc<String> → &String → &str  (2 次 deref 强制转换)
    greet("Dave");  // &str 已经是 —— 不需要强制转换
}
// 在 C++ 中你需要为每种情况调用 .c_str() 或显式转换。
```

**Deref 链**：当你调用 `x.method()` 时，Rust 的方法解析尝试接收器类型 `T`，然后 `&T`，然后 `&mut T`。如果没有匹配，它通过 `Deref` trait 解引用并用目标类型重复。这会继续穿过多层 —— 这就是为什么 `Box<Vec<T>>` "刚好工作"像 `Vec<T>`。Deref *强制转换*（用于函数参数）是一个单独但相关的机制，通过链式 `Deref` impl 自动将 `&Box<String>` 转换为 `&str`。

#### 4. 没有空引用，没有可选引用

```cpp
// C++：引用不能为空，但指针可以，而且区分模糊
Widget& ref = *ptr;  // 如果 ptr 为空 → UB
Widget* opt = nullptr;  // 通过指针的"可选"引用
```

```rust
// Rust：引用总是有效的 —— 借用检查器保证
// 在 safe 代码中无法创建空引用或悬空引用
let r: &i32 = &42; // 总是有效

// "可选引用"是显式的：
let opt: Option<&Widget> = None; // 意图清晰，没有空指针
if let Some(w) = opt {
    w.do_something(); // 只有存在时才可到达
}
```

#### 5. 引用不能重新绑定

```cpp
// C++：引用是别名 —— 不能重新绑定
int a = 1, b = 2;
int& r = a;
r = b;  // 这将 b 的值赋给 a —— 并没有重新绑定 r！
// a 现在是 2，r 仍然引用 a
```

```rust
// Rust：let 绑定可以遮蔽，但引用遵循不同的规则
let a = 1;
let b = 2;
let r = &a;
// r = &b;   // ❌ 不能赋值给不可变变量
let r = &b;  // ✅ 但你可以用新绑定遮蔽 r
             // 旧绑定消失了，不是重新绑定

// 使用 mut：
let mut r = &a;
r = &b;      // ✅ r 现在指向 b —— 这是重新绑定（不是通过赋值）
```

> **心理模型**：在 C++ 中，引用是一个对象的永久别名。
> 在 Rust 中，引用是一个值（带生命周期保证的指针），遵循
> 普通变量绑定规则 —— 默认不可变，只有声明为 `mut` 才能重新绑定。
