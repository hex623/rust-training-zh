### Unsafe Rust

> **你将学到什么：** 何时以及如何使用 `unsafe` —— 原始指针解引用、FFI（外部函数接口）用于从 Rust 调用 C 和反之、`CString`/`CStr` 用于字符串互操作，以及如何编写不安全代码的安全包装器。

- `unsafe` 解锁对 Rust 编译器通常不允许的功能的访问
    - 解引用原始指针
    - 访问 *可变* 静态变量
    - https://doc.rust-lang.org/book/ch19-01-unsafe-rust.html
- 能力越大，责任越大
    - `unsafe` 告诉编译器"我，程序员，负责维护编译器通常保证的不变量"
    - 必须保证没有混叠的可变和不可变引用、没有悬空指针、没有无效引用，...
    - `unsafe` 的使用应限制在最小可能的作用域
    - 所有使用 `unsafe` 的代码都应该有一个"安全"注释描述假设

### Unsafe Rust 示例
```rust
unsafe fn harmless() {}
fn main() {
    // 安全：我们正在调用一个无害的 unsafe 函数
    unsafe {
        harmless();
    }
    let a = 42u32;
    let p = &a as *const u32;
    // 安全：p 是指向将保持作用域的变量的有效指针
    unsafe {
        println!("{}", *p);
    }
    // 安全：不安全；仅用于说明目的
    let dangerous_buffer = 0xb8000 as *mut u32;
    unsafe {
        println!("即将爆炸！！！");
        *dangerous_buffer = 0; // 这在大多数现代机器上会 SEGV
    }
}
```

### 简单 FFI 示例（Rust 库函数被 C 调用）

## FFI 字符串：CString 和 CStr

FFI 代表 *Foreign Function Interface* —— Rust 用于调用用其他语言（如 C）编写的函数的机制，反之亦然。

当与 C 代码交互时，Rust 的 `String` 和 `\u0026str` 类型（UTF-8 无空终止符）与 C 字符串（空终止字节数组）不直接兼容。Rust 从 `std::ffi` 提供 `CString`（拥有）和 `CStr`（借用）：

| 类型 | 类似于 | 何时使用 |
|------|-------------|----------|
| `CString` | `String`（拥有） | 从 Rust 数据创建 C 字符串 |
| `\u0026CStr` | `\u0026str`（借用） | 从外部代码接收 C 字符串 |

```rust
use std::ffi::{CString, CStr};
use std::os::raw::c_char;

fn demo_ffi_strings() {
    // 创建 C 兼容字符串（添加空终止符）
    let c_string = CString::new("Hello from Rust").expect("CString::new 失败");
    let ptr: *const c_char = c_string.as_ptr();

    // 将 C 字符串转换回 Rust（不安全因为我们信任指针）
    // 安全：ptr 有效且以空终止（我们刚刚在上面创建了它）
    let back_to_rust: &CStr = unsafe { CStr::from_ptr(ptr) };
    let rust_str: &str = back_to_rust.to_str().expect("无效 UTF-8");
    println!("{}", rust_str);
}
```

> **警告**：如果输入包含内部空字节（`\0`），`CString::new()` 将返回错误。始终处理 `Result`。你将在下面的 FFI 示例中广泛使用 `CStr`。

- `FFI` 方法必须用 `#[no_mangle]` 标记以确保编译器不会混淆名称
- 我们将把 crate 编译为静态库
    ```
    #[no_mangle] 
    pub extern "C" fn add(left: u64, right: u64) -> u64 {
        left + right
    }
    ```
- 我们将编译以下 C 代码并链接到我们的静态库。
    ```
    #include <stdio.h>
    #include <stdint.h>
    extern uint64_t add(uint64_t, uint64_t);
    int main() {
        printf("Add returned %llu\n", add(21, 21));
    }
    ``` 

### 复杂 FFI 示例
- 在以下示例中，我们将创建一个 Rust 日志接口并暴露给
[PYTHON] 和 `C`
    - 我们将看到相同的接口如何能从 Rust 和 C 原生使用
    - 我们将探索使用 `cbindgen` 等工具为 `C` 生成头文件
    - 我们将看到 `unsafe` 包装器如何充当安全 Rust 代码的桥梁

## Logger 辅助函数
```rust
fn create_or_open_log_file(log_file: &str, overwrite: bool) -> Result<File, String> {
    if overwrite {
        File::create(log_file).map_err(|e| e.to_string())
    } else {
        OpenOptions::new()
            .write(true)
            .append(true)
            .open(log_file)
            .map_err(|e| e.to_string())
    }
}

fn log_to_file(file_handle: &mut File, message: &str) -> Result<(), String> {
    file_handle
        .write_all(message.as_bytes())
        .map_err(|e| e.to_string())
}
```

## Logger 结构体
```rust
struct SimpleLogger {
    log_level: LogLevel,
    file_handle: File,
}

impl SimpleLogger {
    fn new(log_file: &str, overwrite: bool, log_level: LogLevel) -> Result<Self, String> {
        let file_handle = create_or_open_log_file(log_file, overwrite)?;
        Ok(Self {
            file_handle,
            log_level,
        })
    }

    fn log_message(&mut self, log_level: LogLevel, message: &str) -> Result<(), String> {
        if log_level as u32 <= self.log_level as u32 {
            let timestamp = Local::now().format("%Y-%m-%d %H:%M:%S").to_string();
            let message = format!("Simple: {timestamp} {log_level} {message}\n");
            log_to_file(&mut self.file_handle, &message)
        } else {
            Ok(())
        }
    }
}
```

## 测试
- 用 Rust 测试功能是简单的
    - 测试方法用 `#[test]` 装饰，不是编译二进制文件的一部分
    - 很容易为测试目的创建 mock 方法
```rust
#[test]
fn testfunc() -> Result<(), String> {
    let mut logger = SimpleLogger::new("test.log", false, LogLevel::INFO)?;
    logger.log_message(LogLevel::TRACELEVEL1, "Hello world")?;
    logger.log_message(LogLevel::CRITICAL, "Critical message")?;
    Ok(()) // 编译器在这里自动 drop logger
}
```
```bash
cargo test
```

## (C)-Rust FFI
- cbindgen 是为导出的 Rust 函数生成头文件的好工具
    - 可以用 cargo 安装
```bash
cargo install cbindgen
cbindgen 
```
- 函数和结构可以用 `#[no_mangle]` 和 `#[repr(C)]` 导出
    - 我们将假设传递 `**` 到实际实现并返回 0 表示成功、非零表示错误的常见接口模式
    - **不透明 vs 透明结构体**：我们的 `SimpleLogger` 作为 *不透明指针*（`*mut SimpleLogger`）传递 —— C 端从不访问其字段，所以 `#[repr(C)]` **不需要**。当 C 代码需要直接读/写结构体字段时使用 `#[repr(C)]`：

```rust
// 不透明 —— C 只持有指针，从不检查字段。不需要 #[repr(C)]。
struct SimpleLogger { /* Rust-only fields */ }

// 透明 —— C 读写字段。必须使用 #[repr(C)]。
#[repr(C)]
pub struct Point {
    pub x: f64,
    pub y: f64,
}
```
```c
typedef struct SimpleLogger SimpleLogger;
uint32_t create_simple_logger(const char *file_name, struct SimpleLogger **out_logger);
uint32_t log_entry(struct SimpleLogger *logger, const char *message);
uint32_t drop_logger(struct SimpleLogger *logger);
```

- 注意我们需要很多健全性检查
- 我们必须显式泄漏内存以防止 Rust 自动释放
```rust
#[no_mangle] 
pub extern "C" fn create_simple_logger(file_name: *const std::os::raw::c_char, out_logger: *mut *mut SimpleLogger) -> u32 {
    use std::ffi::CStr;
    // 确保指针不是 NULL
    if file_name.is_null() || out_logger.is_null() {
        return 1;
    }
    // 安全：传入的指针根据契约要么是 NULL 要么是以 0 终止的
    let file_name = unsafe {
        CStr::from_ptr(file_name)
    };
    let file_name = file_name.to_str();
    // 确保 file_name 没有垃圾字符
    if file_name.is_err() {
        return 1;
    }
    let file_name = file_name.unwrap();
    // 假设一些默认值；我们将在实际生活中传入它们
    let new_logger = SimpleLogger::new(file_name, false, LogLevel::CRITICAL);
    // 检查我们能够构造 logger
    if new_logger.is_err() {
        return 1;
    }
    let new_logger = Box::new(new_logger.unwrap());
    // 这防止 Box 在超出作用域时被 drop
    let logger_ptr: *mut SimpleLogger = Box::leak(new_logger);
    // 安全：logger 非空且 logger_ptr 有效
    unsafe {
        *out_logger = logger_ptr;
    }
    return 0;
}
```

- 我们在 `log_entry()` 中有类似的错误检查
```rust
#[no_mangle]
pub extern "C" fn log_entry(logger: *mut SimpleLogger, message: *const std::os::raw::c_char) -> u32 {
    use std::ffi::CStr;
    if message.is_null() || logger.is_null() {
        return 1;
    }
    // 安全：message 非空
    let message = unsafe {
        CStr::from_ptr(message)
    };
    let message = message.to_str();
    // 确保 file_name 没有垃圾字符
    if message.is_err() {
        return 1;
    }
    // 安全：logger 是之前由 create_simple_logger() 构造的有效指针
    unsafe {
        (*logger).log_message(LogLevel::CRITICAL, message.unwrap()).is_err() as u32
    }
}

#[no_mangle]
pub extern "C" fn drop_logger(logger: *mut SimpleLogger) -> u32 {
    if logger.is_null() {
        return 1;
    }
    // 安全：logger 是之前由 create_simple_logger() 构造的有效指针
    unsafe {
        // 这构造一个 Box<SimpleLogger>，在超出作用域时 drop
        let _ = Box::from_raw(logger);
    }
    0
}
```

- 我们可以使用 Rust 或编写 (C)-程序测试我们的 (C)-FFI
```rust
#[test]
fn test_c_logger() {
    // c".." 创建以 NULL 终止的字符串
    let file_name = c"test.log".as_ptr() as *const std::os::raw::c_char;
    let mut c_logger: *mut SimpleLogger = std::ptr::null_mut();
    assert_eq!(create_simple_logger(file_name, &mut c_logger), 0);
    // 这是手动创建 c"..." 字符串的方式
    let message = b"message from C\0".as_ptr() as *const std::os::raw::c_char;
    assert_eq!(log_entry(c_logger, message), 0);
    drop_logger(c_logger);
}
```
```c
#include "logger.h"
...
int main() {
    SimpleLogger *logger = NULL;
    if (create_simple_logger("test.log", &logger) == 0) {
        log_entry(logger, "Hello from C");
        drop_logger(logger); /*需要关闭句柄等*/
    } 
    ...
}
```

## 确保 unsafe 代码的正确性
- TL;DR 版本是使用 `unsafe` 需要深思熟虑
    - 始终记录代码所做的安全假设并与专家审查
    - 使用 cbindgen、Miri、Valgrind 等工具帮助验证正确性
    - **永远不要让 panic 跨越 FFI 边界展开** —— 这是 UB。在 FFI 入口点使用 `std::panic::catch_unwind`，或在配置中设置 `panic = "abort"`
    - 如果结构体跨 FFI 共享，标记为 `#[repr(C)]` 以保证 C 兼容内存布局
    - 参考 https://doc.rust-lang.org/nomicon/intro.html（"Rustonomicon" —— unsafe Rust 的黑魔法）
    - 寻求内部专家的帮助

### 验证工具：Miri vs Valgrind
