# 为什么 C/C++ 开发者需要 Rust

> **你将学到什么：**
> - Rust 消除的完整问题列表 —— 内存安全、未定义行为、数据竞争等等
> - 为什么 `shared_ptr`、`unique_ptr` 和其他 C++ 缓解措施只是创可贴，不是解决方案
> - 在 safe Rust 中结构不可能出现的具体 C 和 C++ 漏洞示例

> **想直接看代码？** 跳转到 [给我看代码](ch02-getting-started.md#够了给我看代码)

## Rust 消除了什么 —— 完整列表

在深入示例之前，这里是执行摘要。Safe Rust **从结构上防止** 这个列表中的每一个问题 —— 不是通过规范、工具或代码审查，而是通过类型系统和编译器：

| **消除的问题** | **C** | **C++** | **Rust 如何预防** |
|----------------------|:-----:|:-------:|--------------------------|
| 缓冲区溢出 / 下溢 | ✅ | ✅ | 所有数组、切片和字符串都携带边界；索引在运行时检查 |
| 内存泄漏（不需要 GC） | ✅ | ✅ | `Drop` trait = 正确实现的 RAII；自动清理，不需要 Rule of Five |
| 悬空指针 | ✅ | ✅ | 生命周期系统在编译时证明引用比其引用对象活得更长 |
| 释放后使用 | ✅ | ✅ | 所有权系统使其成为编译错误 |
| 移动后使用 | — | ✅ | 移动是 **破坏性的** —— 原始绑定不再存在 |
| 未初始化变量 | ✅ | ✅ | 所有变量必须在使用前初始化；编译器强制执行 |
| 整数溢出 / 下溢 UB | ✅ | ✅ | Debug 构建在溢出时 panic；Release 构建包装（两种方式都是定义行为） |
| 空指针解引用 / SEGV | ✅ | ✅ | 没有空指针；`Option<T>` 强制显式处理 |
| 数据竞争 | ✅ | ✅ | `Send`/`Sync` trait + 借用检查器使数据竞争成为编译错误 |
| 不受控制的副作用 | ✅ | ✅ | 默认不可变；变异需要显式 `mut` |
| 没有继承（更好的可维护性） | — | ✅ | Trait + 组合替代类层次结构；促进无耦合的重用 |
| 没有异常；可预测的控制流 | — | ✅ | 错误是值（`Result<T, E>`）；不可能忽略，没有隐藏的 `throw` 路径 |
| 迭代器失效 | — | ✅ | 借用检查器禁止在迭代时变异集合 |
| 引用循环 / 泄漏的终结器 | — | ✅ | 所有权是树状的；`Rc` 循环是可选的，可用 `Weak` 捕获 |
| 没有忘记互斥锁解锁 | ✅ | ✅ | `Mutex<T>` 包装数据；锁守卫是唯一访问路径 |
| 未定义行为（一般） | ✅ | ✅ | Safe Rust 有 **零** 未定义行为；`unsafe` 块是显式和可审计的 |

> **底线：** 这些不是通过编码规范执行的愿望目标。它们是 **编译时保证**。如果你的代码编译了，这些 bug 就不可能存在。

---

## C 和 C++ 共同的问题

> **想跳过示例？** 跳转到 [Rust 如何解决这一切](#rust-如何解决这一切) 或直接跳转到 [给我看代码](ch02-getting-started.md#够了给我看代码)

这两种语言共享一组核心内存安全问题，是超过 70% 的 CVE（常见漏洞和暴露）的根源：

### 缓冲区溢出

C 数组、指针和字符串没有内在边界。超出它们非常容易：

```c
#include <stdlib.h>
#include <string.h>

void buffer_dangers() {
    char buffer[10];
    strcpy(buffer, "This string is way too long!");  // 缓冲区溢出

    int arr[5] = {1, 2, 3, 4, 5};
    int *ptr = arr;           // 丢失大小信息
    ptr[10] = 42;             // 没有边界检查 —— 未定义行为
}
```

在 C++ 中，`std::vector::operator[]` 仍然不执行边界检查。只有 `.at()` 会 —— 但谁捕获异常？

### 悬空指针和释放后使用

```c
int *bar() {
    int i = 42;
    return &i;    // 返回栈变量地址 —— 悬空！
}

void use_after_free() {
    char *p = (char *)malloc(20);
    free(p);
    *p = '\0';   // 释放后使用 —— 未定义行为
}
```

### 未初始化变量和未定义行为

C 和 C++ 都允许未初始化变量。结果值是不确定的，读取它们是未定义行为：

```c
int x;               // 未初始化
if (x > 0) { ... }  // UB —— x 可能是任何东西
```

整数溢出在 C 中对无符号类型是 **定义的**，但对有符号类型是 **未定义的**。在 C++ 中，有符号溢出也是未定义行为。两个编译器都可以而且确实利用这一点进行"优化"，以令人惊讶的方式破坏程序。

### 空指针解引用

```c
int *ptr = NULL;
*ptr = 42;           // SEGV —— 但编译器不会阻止你
```

在 C++ 中，`std::optional<T>` 有帮助，但繁琐，经常用 `.value()` 绕过，这会抛出。

### 可视化：共同的问题

```mermaid
graph TD
    ROOT["C/C++ 内存安全问题"] --> BUF["缓冲区溢出"]
    ROOT --> DANGLE["悬空指针"]
    ROOT --> UAF["释放后使用"]
    ROOT --> UNINIT["未初始化变量"]
    ROOT --> NULL["空解引用"]
    ROOT --> UB["未定义行为"]
    ROOT --> RACE["数据竞争"]

    BUF --> BUF1["数组/指针没有边界"]
    DANGLE --> DANGLE1["返回栈地址"]
    UAF --> UAF1["重用已释放内存"]
    UNINIT --> UNINIT1["不确定值"]
    NULL --> NULL1["没有强制空检查"]
    UB --> UB1["有符号溢出、别名"]
    RACE --> RACE1["没有编译时安全"]

    style ROOT fill:#ff6b6b,color:#000
    style BUF fill:#ffa07a,color:#000
    style DANGLE fill:#ffa07a,color:#000
    style UAF fill:#ffa07a,color:#000
    style UNINIT fill:#ffa07a,color:#000
    style NULL fill:#ffa07a,color:#000
    style UB fill:#ffa07a,color:#000
    style RACE fill:#ffa07a,color:#000
```

---

## C++ 额外增加的问题

> **C 读者**：如果你不使用 C++，可以[跳到 Rust 如何解决这些问题](#rust-如何解决这一切)。
>
> **想直接看代码？** 跳转到 [给我看代码](ch02-getting-started.md#够了给我看代码)

C++ 引入了智能指针、RAII、移动语义和异常来解决 C 的问题。这些是 **创可贴，不是治愈** —— 它们将失败模式从"运行时崩溃"转移到"运行时更微妙的 bug"：

### `unique_ptr` 和 `shared_ptr` —— 创可贴，不是解决方案

C++ 智能指针比原始 `malloc`/`free` 有显著改进，但它们没有解决根本问题：

| C++ 缓解措施 | 修复了什么 | **没有** 修复什么 |
|----------------|---------------|------------------------|
| `std::unique_ptr` | 通过 RAII 防止泄漏 | **移动后使用** 仍然编译；留下僵尸 nullptr |
| `std::shared_ptr` | 共享所有权 | **引用循环** 静默泄漏；`weak_ptr` 规范是手动的 |
| `std::optional` | 替代一些空使用 | `.value()` **抛出** 如果为空 —— 隐藏控制流 |
| `std::string_view` | 避免拷贝 | 如果源字符串被释放则 **悬空** —— 没有生命周期检查 |
| 移动语义 | 高效传输 | 移动后的对象处于 **"有效但未指定状态"** —— UB 等待发生 |
| RAII | 自动清理 | 需要 **Rule of Five** 才能正确；一个错误破坏一切 |

```cpp
// unique_ptr：移动后使用干净地编译
std::unique_ptr<int> ptr = std::make_unique<int>(42);
std::unique_ptr<int> ptr2 = std::move(ptr);
std::cout << *ptr;  // 编译！运行时未定义行为。
                     // 在 Rust 中，这是编译错误："移动后使用值"
```

```cpp
// shared_ptr：引用循环静默泄漏
struct Node {
    std::shared_ptr<Node> next;
    std::shared_ptr<Node> parent;  // 循环！析构函数从未调用。
};
auto a = std::make_shared<Node>();
auto b = std::make_shared<Node>();
a->next = b;
b->parent = a;  // 内存泄漏 —— 引用计数从未达到 0
                 // 在 Rust 中，Rc<T> + Weak<T> 使循环显式和可打破
```

### 移动后使用 —— 无声杀手

C++ `std::move` 不是移动 —— 它是类型转换。原始对象保持在"有效但未指定状态"。编译器让你继续使用它：

```cpp
auto vec = std::make_unique<std::vector<int>>({1, 2, 3});
auto vec2 = std::move(vec);
vec->size();  // 编译！但解引用空指针 —— 运行时崩溃
```

在 Rust 中，移动是 **破坏性的**。原始绑定消失了：

```rust
let vec = vec![1, 2, 3];
let vec2 = vec;           // 移动 —— vec 被消耗
// vec.len();             // 编译错误：移动后使用值
```

### 迭代器失效 —— 来自生产 C++ 的真实 bug

这些不是牵强的示例 —— 它们代表在大型 C++ 代码库中发现的 **真实 bug 模式**：

```cpp
// BUG 1：erase 没有重新赋值迭代器（未定义行为）
while (it != pending_faults.end()) {
    if (*it != nullptr && (*it)->GetId() == fault->GetId()) {
        pending_faults.erase(it);   // ← 迭代器失效！
        removed_count++;            //   下一轮循环使用悬空迭代器
    } else {
        ++it;
    }
}
// 修复：it = pending_faults.erase(it);
```

```cpp
// BUG 2：基于索引的 erase 跳过元素
for (auto i = 0; i < entries.size(); i++) {
    if (config_status == ConfigDisable::Status::Disabled) {
        entries.erase(entries.begin() + i);  // ← 移动元素
    }                                         //   i++ 跳过被移动的
}
```

```cpp
// BUG 3：一条 erase 路径正确，另一条不正确
while (it != incomplete_ids.end()) {
    if (current_action == nullptr) {
        incomplete_ids.erase(it);  // ← BUG：迭代器没有重新赋值
        continue;
    }
    it = incomplete_ids.erase(it); // ← 正确路径
}
```

**这些编译没有任何警告。** 在 Rust 中，借用检查器使这三个都成为编译错误 —— 你不能在迭代时变异集合，句号。

### 异常安全和 `dynamic_cast`/`new` 模式

现代 C++ 代码库仍然严重依赖没有编译时安全的模式：

```cpp
// 典型的 C++ 工厂模式 —— 每个分支都是潜在的 bug
DriverBase* driver = nullptr;
if (dynamic_cast<ModelA*>(device)) {
    driver = new DriverForModelA(framework);
} else if (dynamic_cast<ModelB*>(device)) {
    driver = new DriverForModelB(framework);
}
// 如果 driver 仍然是 nullptr？如果 new 抛出？谁拥有 driver？
```

在典型的 10 万行 C++ 代码库中，你可能会发现数百个 `dynamic_cast` 调用（每个都是潜在的运行时失败），数百个原始 `new` 调用（每个都是潜在的泄漏），以及数百个 `virtual`/`override` 方法（到处都是 vtable 开销）。

### 悬空引用和 lambda 捕获

```cpp
int& get_reference() {
    int x = 42;
    return x;  // 悬空引用 —— 编译，运行时 UB
}

auto make_closure() {
    int local = 42;
    return [&local]() { return local; };  // 悬空捕获！
}
```

### 可视化：C++ 额外的问题

```mermaid
graph TD
    ROOT["C++ 额外的问题<br/>（在 C 问题之上）"] --> UAM["移动后使用"]
    ROOT --> CYCLE["引用循环"]
    ROOT --> ITER["迭代器失效"]
    ROOT --> EXC["异常安全"]
    ROOT --> TMPL["模板错误信息"]

    UAM --> UAM1["std::move 留下僵尸<br/>编译无警告"]
    CYCLE --> CYCLE1["shared_ptr 循环泄漏<br/>析构函数从未调用"]
    ITER --> ITER1["erase() 使迭代器失效<br/>真实的生产 bug"]
    EXC --> EXC1["部分构造<br/>new 没有 try/catch"]
    TMPL --> TMPL1["30+ 行嵌套<br/>模板实例化错误"]

    style ROOT fill:#ff6b6b,color:#000
    style UAM fill:#ffa07a,color:#000
    style CYCLE fill:#ffa07a,color:#000
    style ITER fill:#ffa07a,color:#000
    style EXC fill:#ffa07a,color:#000
    style TMPL fill:#ffa07a,color:#000
```

---

## Rust 如何解决这一切

上面列出的每个问题 —— 从 C 和 C++ —— 都被 Rust 的编译时保证所阻止：

| 问题 | Rust 的解决方案 |
|---------|-----------------|
| 缓冲区溢出 | 切片携带长度；索引是边界检查的 |
| 悬空指针 / 释放后使用 | 生命周期系统在编译时证明引用有效 |
| 移动后使用 | 移动是破坏性的 —— 编译器拒绝让你接触原始值 |
| 内存泄漏 | `Drop` trait = 不需要 Rule of Five 的 RAII；自动、正确的清理 |
| 引用循环 | 所有权是树状的；`Rc` + `Weak` 使循环显式 |
| 迭代器失效 | 借用检查器禁止在借用时变异集合 |
| 空指针 | 没有空。`Option<T>` 通过模式匹配强制显式处理 |
| 数据竞争 | `Send`/`Sync` trait 使数据竞争成为编译错误 |
| 未初始化变量 | 所有变量必须初始化；编译器强制执行 |
| 整数 UB | Debug 在溢出时 panic；Release 包装（都是定义行为） |
| 异常 | 没有异常；`Result<T, E>` 在类型签名中可见，用 `?` 传播 |
| 继承复杂性 | Trait + 组合；没有菱形问题，没有 vtable 脆弱性 |
| 忘记互斥锁解锁 | `Mutex<T>` 包装数据；锁守卫是唯一访问路径 |

```rust
fn rust_prevents_everything() {
    // ✅ 没有缓冲区溢出 —— 边界检查
    let arr = [1, 2, 3, 4, 5];
    // arr[10];  // 运行时 panic，永远不会 UB

    // ✅ 没有移动后使用 —— 编译错误
    let data = vec![1, 2, 3];
    let moved = data;
    // data.len();  // 错误：移动后使用值

    // ✅ 没有悬空指针 —— 生命周期错误
    // let r;
    // { let x = 5; r = &x; }  // 错误：x 存活时间不够长

    // ✅ 没有空 —— Option 强制处理
    let maybe: Option<i32> = None;
    // maybe.unwrap();  // panic，但你会用 match 或 if let 代替

    // ✅ 没有数据竞争 —— 编译错误
    // let mut shared = vec![1, 2, 3];
    // std::thread::spawn(|| shared.push(4));  // 错误：闭包可能存活
    // shared.push(5);                         //   超过借用值
}
```

### Rust 的安全模型 —— 全貌

```mermaid
graph TD
    RUST["Rust 安全保证"] --> OWN["所有权系统"]
    RUST --> BORROW["借用检查器"]
    RUST --> TYPES["类型系统"]
    RUST --> TRAITS["Send/Sync Trait"]

    OWN --> OWN1["没有释放后使用<br/>没有移动后使用<br/>没有双重释放"]
    BORROW --> BORROW1["没有悬空引用<br/>没有迭代器失效<br/>没有通过引用的数据竞争"]
    TYPES --> TYPES1["没有 NULL（Option<T>）<br/>没有异常（Result<T,E>）<br/>没有未初始化值"]
    TRAITS --> TRAITS1["没有数据竞争<br/>Send = 安全传输<br/>Sync = 安全共享"]

    style RUST fill:#51cf66,color:#000
    style OWN fill:#91e5a3,color:#000
    style BORROW fill:#91e5a3,color:#000
    style TYPES fill:#91e5a3,color:#000
    style TRAITS fill:#91e5a3,color:#000
```

## 快速参考：C vs C++ vs Rust

| **概念** | **C** | **C++** | **Rust** | **关键区别** |
|-------------|-------|---------|----------|-------------------|
| 内存管理 | `malloc()/free()` | `unique_ptr`, `shared_ptr` | `Box<T>`, `Rc<T>`, `Arc<T>` | 自动，无循环，无僵尸 |
| 数组 | `int arr[10]` | `std::vector<T>`, `std::array<T>` | `Vec<T>`, `[T; N]` | 默认边界检查 |
| 字符串 | `char*` 带 `\0` | `std::string`, `string_view` | `String`, `&str` | 保证 UTF-8，生命周期检查 |
| 引用 | `int*` (原始) | `T&`, `T&&` (移动) | `&T`, `&mut T` | 生命周期 + 借用检查 |
| 多态 | 函数指针 | 虚函数、继承 | Trait、trait 对象 | 组合优于继承 |
| 泛型 | 宏 / `void*` | 模板 | 泛型 + trait bounds | 清晰的错误信息 |
| 错误处理 | 返回码，`errno` | 异常，`std::optional` | `Result<T, E>`, `Option<T>` | 无隐藏控制流 |
| 空安全 | `ptr == NULL` | `nullptr`, `std::optional<T>` | `Option<T>` | 强制空检查 |
| 线程安全 | 手动 (pthreads) | 手动 (`std::mutex` 等) | 编译时 `Send`/`Sync` | 数据竞争不可能 |
| 构建系统 | Make, CMake | CMake, Make 等 | Cargo | 集成工具链 |
| 未定义行为 | 猖獗 | 微妙（有符号溢出、别名） | Safe 代码中为零 | 安全保证 |

***
