# Rust 并发

> **你将学到什么：** Rust 的并发模型 —— 线程、`Send`/`Sync` 标记 trait、`Mutex<T>`、`Arc<T>`、通道，以及编译器如何在编译时防止数据竞争。不使用的线程安全没有运行时开销。

- Rust 内置支持并发，类似于 C++ 中的 `std::thread`
    - 关键区别：Rust **在编译时通过 `Send` 和 `Sync` 标记 trait 防止数据竞争**
    - 在 C++ 中，在没有互斥锁的情况下跨线程共享 `std::vector` 是 UB，但能干净地编译。在 Rust 中，它不会编译。
    - Rust 中的 `Mutex<T>` 包装 **数据**，不只是访问 —— 你实际上不能在没有锁定的情况下读取数据
- `thread::spawn()` 可用于创建并行执行闭包 `||` 的单独线程
```rust
use std::thread;
use std::time::Duration;
fn main() {
    let handle = thread::spawn(|| {
        for i in 0..10 {
            println!("线程中的计数: {i}!");
            thread::sleep(Duration::from_millis(5));
        }
    });

    for i in 0..5 {
        println!("主线程: {i}");
        thread::sleep(Duration::from_millis(5));
    }

    handle.join().unwrap(); // handle.join() 确保生成的线程退出
}
```

# Rust 并发
- 在需要从环境借用的情况下可以使用 `thread::scope()`。这有效是因为 `thread::scope` 等待内部线程返回
- 尝试不用 `thread::scope` 执行这个练习看看问题
```rust
use std::thread;
fn main() {
  let a = [0, 1, 2];
  thread::scope(|scope| {
      scope.spawn(|| {
          for x in &a {
            println!("{x}");
          }
      });
  });
}
```
----
# Rust 并发
- 我们也可以使用 `move` 将所有权转移给线程。对于像 `[i32; 3]` 这样的 `Copy` 类型，`move` 关键字将数据拷贝到闭包中，原始数据仍然可用
```rust
use std::thread;
fn main() {
  let mut a = [0, 1, 2];
  let handle = thread::spawn(move || {
      for x in a {
        println!("{x}");
      }
  });
  a[0] = 42;    // 不影响发送到线程的拷贝
  handle.join().unwrap();
}
```

# Rust 并发
- `Arc<T>` 可用于在多个线程之间共享 *只读* 引用
    - `Arc` 代表原子引用计数。引用直到引用计数达到 0 才被释放
    - `Arc::clone()` 只增加引用计数而不克隆数据
```rust
use std::sync::Arc;
use std::thread;
fn main() {
    let a = Arc::new([0, 1, 2]);
    let mut handles = Vec::new();
    for i in 0..2 {
        let arc = Arc::clone(&a);
        handles.push(thread::spawn(move || {
            println!("线程: {i} {arc:?}");
        }));
    }
    handles.into_iter().for_each(|h| h.join().unwrap());
}
```

# Rust 并发
- `Arc<T>` 可以与 `Mutex<T>` 结合提供可变引用。
    - `Mutex` 守卫受保护的数据并确保只有持有锁的线程有访问权。
    - `MutexGuard` 在超出作用域时自动释放（RAII）。注意：`std::mem::forget` 仍可能泄漏守卫 —— 所以"不可能忘记解锁"比"不可能泄漏"更准确。
```rust
use std::sync::{Arc, Mutex};
use std::thread;

fn main() {
    let counter = Arc::new(Mutex::new(0));
    let mut handles = Vec::new();

    for _ in 0..5 {
        let counter = Arc::clone(&counter);
        handles.push(thread::spawn(move || {
            let mut num = counter.lock().unwrap();
            *num += 1;
            // MutexGuard 在这里 drop —— 锁自动释放
        }));
    }

    for handle in handles {
        handle.join().unwrap();
    }

    println!("最终计数: {}", *counter.lock().unwrap());
    // 输出: 最终计数: 5
}
```

# Rust 并发：RwLock
- `RwLock<T>` 允许 **多个并发读取者** 或 **一个独占写入者** —— C++ 的读/写锁模式（`std::shared_mutex`）
    - 当读取远多于写入时使用 `RwLock`（例如，配置、缓存）
    - 当读/写频率相似或临界区很短时使用 `Mutex`
```rust
use std::sync::{Arc, RwLock};
use std::thread;

fn main() {
    let config = Arc::new(RwLock::new(String::from("v1.0")));
    let mut handles = Vec::new();

    // 生成 5 个读取者 —— 都可以并发运行
    for i in 0..5 {
        let config = Arc::clone(&config);
        handles.push(thread::spawn(move || {
            let val = config.read().unwrap();  // 多个读取者 OK
            println!("读取者 {i}: {val}");
        }));
    }

    // 一个写入者 —— 阻塞直到所有读取者完成
    {
        let config = Arc::clone(&config);
        handles.push(thread::spawn(move || {
            let mut val = config.write().unwrap();  // 独占访问
            *val = String::from("v2.0");
            println!("写入者: 更新为 {val}");
        }));
    }

    for handle in handles {
        handle.join().unwrap();
    }
}
```

# Rust 并发：Mutex 中毒
- 如果线程在持有 `Mutex` 或 `RwLock` 时 **panic**，锁变成 **中毒的**
    - 后续对 `.lock()` 的调用返回 `Err(PoisonError)` —— 数据可能处于不一致状态
    - 如果你确信数据仍然有效，可以用 `.into_inner()` 恢复
    - 这在 C++ 中没有等效 —— `std::mutex` 没有中毒概念；panic 的线程只是让锁保持持有
```rust
use std::sync::{Arc, Mutex};
use std::thread;

fn main() {
    let data = Arc::new(Mutex::new(vec![1, 2, 3]));

    let data2 = Arc::clone(&data);
    let handle = thread::spawn(move || {
        let mut guard = data2.lock().unwrap();
        guard.push(4);
        panic!("oops!");  // 锁现在中毒了
    });

    let _ = handle.join();  // 线程 panic 了

    // 后续锁尝试返回 Err(PoisonError)
    match data.lock() {
        Ok(guard) => println!("数据: {guard:?}"),
        Err(poisoned) => {
            println!("锁中毒了！正在恢复...");
            let guard = poisoned.into_inner();  // 无论如何访问数据
            println!("恢复的数据: {guard:?}");  // [1, 2, 3, 4] —— panic 前 push 成功了
        }
    }
}
```

# Rust 并发：原子操作
- 对于简单的计数器和标志，`std::sync::atomic` 类型避免了 `Mutex` 的开销
    - `AtomicBool`、`AtomicI32`、`AtomicU64`、`AtomicUsize` 等
    - 等同于 C++ `std::atomic<T>` —— 相同的内存序模型（`Relaxed`、`Acquire`、`Release`、`SeqCst`）
```rust
use std::sync::atomic::{AtomicU64, Ordering};
use std::sync::Arc;
use std::thread;

fn main() {
    let counter = Arc::new(AtomicU64::new(0));
    let mut handles = Vec::new();

    for _ in 0..10 {
        let counter = Arc::clone(&counter);
        handles.push(thread::spawn(move || {
            for _ in 0..1000 {
                counter.fetch_add(1, Ordering::Relaxed);
            }
        }));
    }

    for handle in handles {
        handle.join().unwrap();
    }

    println!("计数器: {}", counter.load(Ordering::SeqCst));
    // 输出: 计数器: 10000
}
```

| 原语 | 何时使用 | C++ 等效 |
|-----------|-------------|----------------|
| `Mutex<T>` | 通用可变共享状态 | `std::mutex` + 手动数据关联 |
| `RwLock<T>` | 读密集型工作负载 | `std::shared_mutex` |
| `Atomic*` | 简单计数器、标志、无锁模式 | `std::atomic<T>` |
| `Condvar` | 等待条件变为真 | `std::condition_variable` |

# Rust 并发：Condvar
- `Condvar`（条件变量）让线程 **休眠直到另一个线程发出信号** 条件已改变
    - 总是与 `Mutex` 配对 —— 模式是：锁定、检查条件、如果没准备好则等待、准备好时行动
    - 等同于 C++ `std::condition_variable` / `std::condition_variable::wait`
    - 处理 **虚假唤醒** —— 总是在循环中重新检查条件（或使用 `wait_while`/`wait_until`）
```rust
use std::sync::{Arc, Condvar, Mutex};
use std::thread;

fn main() {
    let pair = Arc::new((Mutex::new(false), Condvar::new()));

    // 生成一个等待信号的 worker
    let pair2 = Arc::clone(&pair);
    let worker = thread::spawn(move || {
        let (lock, cvar) = &*pair2;
        let mut ready = lock.lock().unwrap();
        // wait: 休眠直到被信号唤醒（总是循环重新检查虚假唤醒）
        while !*ready {
            ready = cvar.wait(ready).unwrap();
        }
        println!("Worker: 条件满足，继续执行！");
    });

    // 主线程做一些工作，然后信号 worker
    thread::sleep(std::time::Duration::from_millis(100));
    {
        let (lock, cvar) = &*pair;
        let mut ready = lock.lock().unwrap();
        *ready = true;
        cvar.notify_one();  // 唤醒一个等待线程（notify_all() 唤醒所有）
    }

    worker.join().unwrap();
}
```

> **何时使用 Condvar vs 通道：** 当线程共享可变状态并需要等待该状态的条件时使用 `Condvar`（例如，"缓冲区非空"）。当线程需要传递 *消息* 时使用通道（`mpsc`）。通道通常更容易推理。

# Rust 并发
- Rust 通道可用于在 `Sender` 和 `Receiver` 之间交换消息
    - 这使用一种称为 `mpsc` 或 `多生产者，单消费者` 的范式
    - `send()` 和 `recv()` 都可以阻塞线程
```rust
use std::sync::mpsc;

fn main() {
    let (tx, rx) = mpsc::channel();
    
    tx.send(10).unwrap();
    tx.send(20).unwrap();
    
    println!("接收: {:?}", rx.recv());
    println!("接收: {:?}", rx.recv());

    let tx2 = tx.clone();
    tx2.send(30).unwrap();
    println!("接收: {:?}", rx.recv());
}
```

# Rust 并发
- 通道可以与线程结合使用
```rust
use std::sync::mpsc;
use std::thread;
use std::time::Duration;

fn main() {
    let (tx, rx) = mpsc::channel();
    for _ in 0..2 {
        let tx2 = tx.clone();
        thread::spawn(move || {
            let thread_id = thread::current().id();
            for i in 0..10 {
                tx2.send(format!("消息 {i}")).unwrap();
                println!("{thread_id:?}: 发送消息 {i}");
            }
            println!("{thread_id:?}: 完成");
        });
    }

        // 丢弃原始发送者，以便当所有克隆发送者被丢弃时 rx.iter() 终止
    drop(tx);

    thread::sleep(Duration::from_millis(100));

    for msg in rx.iter() {
        println!("主线程: 收到 {msg}");
    }
}
```



## 为什么 Rust 能防止数据竞争：Send 和 Sync

- Rust 使用两个标记 trait 在编译时强制执行线程安全：
    - `Send`：如果类型可以安全地 **转移** 到另一个线程，则它是 `Send`
    - `Sync`：如果类型可以通过 `&T` 在线程之间安全地 **共享**，则它是 `Sync`
- 大多数类型自动是 `Send + Sync`。显著例外：
    - `Rc<T>` **既不是** Send 也不是 Sync（线程使用 `Arc<T>`）
    - `Cell<T>` 和 `RefCell<T>` **不是** Sync（使用 `Mutex<T>` 或 `RwLock<T>`）
    - 原始指针（`*const T`、`*mut T`）**既不是** Send 也不是 Sync
- 这就是编译器阻止你跨线程使用 `Rc<T>` 的原因 —— 它实际上没有实现 `Send`
- `Arc<Mutex<T>>` 是 `Rc<RefCell<T>>` 的线程安全等效

> **直觉** *(Jon Gjengset)*：把值想象成玩具。
> **`Send`** = 你可以 **把你的玩具送给** 另一个孩子（线程）—— 转移所有权是安全的。
> **`Sync`** = 你可以 **让其他人同时玩你的玩具** —— 共享引用是安全的。
> `Rc<T>` 有一个脆弱（非原子）的引用计数器；传递或共享它会破坏计数，所以它既不是 `Send` 也不是 `Sync`。


# 练习：多线程单词计数

🔴 **挑战** —— 结合线程、Arc、Mutex 和 HashMap

- 给定文本行的 `Vec<String>`，为每行生成一个线程来计数该行中的单词
- 使用 `Arc<Mutex<HashMap<String, usize>>>` 收集结果
- 打印所有行的总单词数
- **加分**：尝试用通道（`mpsc`）而不是共享状态实现

<details><summary>解答（点击展开）</summary>

```rust
use std::collections::HashMap;
use std::sync::{Arc, Mutex};
use std::thread;

fn main() {
    let lines = vec![
        "the quick brown fox".to_string(),
        "jumps over the lazy dog".to_string(),
        "the fox is quick".to_string(),
    ];

    let word_counts: Arc<Mutex<HashMap<String, usize>>> =
        Arc::new(Mutex::new(HashMap::new()));

    let mut handles = vec![];
    for line in &lines {
        let line = line.clone();
        let counts = Arc::clone(&word_counts);
        handles.push(thread::spawn(move || {
            for word in line.split_whitespace() {
                let mut map = counts.lock().unwrap();
                *map.entry(word.to_lowercase()).or_insert(0) += 1;
            }
        }));
    }

    for handle in handles {
        handle.join().unwrap();
    }

    let counts = word_counts.lock().unwrap();
    let total: usize = counts.values().sum();
    println!("词频: {counts:#?}");
    println!("总单词数: {total}");
}
// 输出（顺序可能不同）：
// 词频: {
//     "the": 3,
//     "quick": 2,
//     "brown": 1,
//     "fox": 2,
//     "jumps": 1,
//     "over": 1,
//     "lazy": 1,
//     "dog": 1,
//     "is": 1,
// }
// 总单词数: 13
```

</details>

