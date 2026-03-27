# 够了，给我看代码

> **你将学到什么：** 你的第一个 Rust 程序 —— `fn main()`, `println!()`, 以及 Rust 宏与 C/C++ 预处理器宏的根本区别。学完本节，你将能够编写、编译和运行简单的 Rust 程序。

```rust
fn main() {
    println!("Hello world from Rust");
}
```
- 上述语法对任何熟悉 C 风格语言的人来说应该都很相似
    - Rust 中的所有函数都以 `fn` 关键字开头
    - 可执行文件的默认入口点是 `main()`
    - `println!` 看起来像一个函数，但实际上是一个 **宏**。Rust 中的宏与 C/C++ 预处理器宏非常不同 —— 它们是卫生的、类型安全的，操作的是语法树而不是文本替换
- 两种快速尝试 Rust 代码片段的好方法：
    - **在线**：[Rust Playground](https://play.rust-lang.org/) —— 粘贴代码，点击运行，分享结果。无需安装
    - **本地 REPL**：安装 [`evcxr_repl`](https://github.com/evcxr/evcxr) 获得交互式 Rust REPL（类似 Python 的 REPL，但用于 Rust）：
```bash
cargo install --locked evcxr_repl
evcxr   # 启动 REPL，交互式输入 Rust 表达式
```

### Rust 本地安装
- Rust 可以通过以下方法本地安装
    - Windows：https://static.rust-lang.org/rustup/dist/x86_64-pc-windows-msvc/rustup-init.exe
    - Linux / WSL：```curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh```
- Rust 生态系统由以下组件组成
    - `rustc` 是独立编译器，但很少直接使用
    - 首选工具 `cargo` 是瑞士军刀，用于依赖管理、构建、测试、格式化、linting 等
    - Rust 工具链有 `stable`、`beta` 和 `nightly`（实验性）通道，但我们将使用 `stable`。使用 `rustup update` 命令升级每六周发布的 `stable` 版本
- 我们还将为 VSCode 安装 `rust-analyzer` 插件

# Rust 包（crates）
- Rust 二进制文件使用包（以下简称 crates）创建
    - 一个 crate 可以是独立的，也可以依赖其他 crates。依赖项的 crates 可以是本地或远程的。第三方 crates 通常从名为 `crates.io` 的集中仓库下载。
    - `cargo` 工具自动处理 crates 及其依赖项的下载。这在概念上等同于链接 C 库
    - Crate 依赖项在一个名为 `Cargo.toml` 的文件中表达。它还定义 crate 的目标类型：独立可执行文件、静态库、动态库（不常见）
    - 参考：https://doc.rust-lang.org/cargo/reference/cargo-targets.html

## Cargo 与传统 C 构建系统对比

### 依赖管理对比

```mermaid
graph TD
    subgraph "传统 C 构建流程"
        CC["C 源文件<br/>(.c, .h)"]
        CM["手动 Makefile<br/>或 CMake"]
        CL["链接器"]
        CB["最终二进制文件"]
        
        CC --> CM
        CM --> CL
        CL --> CB
        
        CDep["手动依赖<br/>管理"]
        CLib1["libcurl-dev<br/>(apt install)"]
        CLib2["libjson-dev<br/>(apt install)"]
        CInc["手动包含路径<br/>-I/usr/include/curl"]
        CLink["手动链接<br/>-lcurl -ljson"]
        
        CDep --> CLib1
        CDep --> CLib2
        CLib1 --> CInc
        CLib2 --> CInc
        CInc --> CM
        CLink --> CL
        
        C_ISSUES["[错误] 版本冲突<br/>[错误] 平台差异<br/>[错误] 缺少依赖<br/>[错误] 链接顺序重要<br/>[错误] 没有自动更新"]
    end
    
    subgraph "Rust Cargo 构建流程"
        RS["Rust 源文件<br/>(.rs)"]
        CT["Cargo.toml<br/>[dependencies]<br/>reqwest = '0.11'<br/>serde_json = '1.0'"]
        CRG["Cargo 构建系统"]
        RB["最终二进制文件"]
        
        RS --> CRG
        CT --> CRG
        CRG --> RB
        
        CRATES["crates.io<br/>(包注册表)"]
        DEPS["自动依赖<br/>解析"]
        LOCK["Cargo.lock<br/>(版本锁定)"]
        
        CRATES --> DEPS
        DEPS --> CRG
        CRG --> LOCK
        
        R_BENEFITS["[正常] 语义版本<br/>[正常] 自动下载<br/>[正常] 跨平台<br/>[正常] 传递依赖<br/>[正常] 可重现构建"]
    end
    
    style C_ISSUES fill:#ff6b6b,color:#000
    style R_BENEFITS fill:#91e5a3,color:#000
    style CM fill:#ffa07a,color:#000
    style CDep fill:#ffa07a,color:#000
    style CT fill:#91e5a3,color:#000
    style CRG fill:#91e5a3,color:#000
    style DEPS fill:#91e5a3,color:#000
    style CRATES fill:#91e5a3,color:#000
```

### Cargo 项目结构

```text
my_project/
|-- Cargo.toml          # 项目配置（类似 package.json）
|-- Cargo.lock          # 精确依赖版本（自动生成）
|-- src/
|   |-- main.rs         # 二进制文件的主入口
|   |-- lib.rs          # 库根（如果创建库）
|   `-- bin/            # 额外的二进制目标
|-- tests/              # 集成测试
|-- examples/           # 示例代码
|-- benches/            # 基准测试
`-- target/             # 构建产物（类似 C 的 build/ 或 obj/）
    |-- debug/          # Debug 构建（编译快，运行慢）
    `-- release/        # Release 构建（编译慢，运行快）
```

### 常用 Cargo 命令

```mermaid
graph LR
    subgraph "项目生命周期"
        NEW["cargo new my_project<br/>[文件夹] 创建新项目"]
        CHECK["cargo check<br/>[搜索] 快速语法检查"]
        BUILD["cargo build<br/>[构建] 编译项目"]
        RUN["cargo run<br/>[运行] 构建并执行"]
        TEST["cargo test<br/>[测试] 运行所有测试"]
        
        NEW --> CHECK
        CHECK --> BUILD
        BUILD --> RUN
        BUILD --> TEST
    end
    
    subgraph "高级命令"
        UPDATE["cargo update<br/>[图表] 更新依赖"]
        FORMAT["cargo fmt<br/>[闪光] 格式化代码"]
        LINT["cargo clippy<br/>[扳手] Lint 和建议"]
        DOC["cargo doc<br/>[书籍] 生成文档"]
        PUBLISH["cargo publish<br/>[包] 发布到 crates.io"]
    end
    
    subgraph "构建配置"
        DEBUG["cargo build<br/>(debug 配置)<br/>编译快<br/>运行慢<br/>调试符号"]
        RELEASE["cargo build --release<br/>(release 配置)<br/>编译慢<br/>运行快<br/>优化"]
    end
    
    style NEW fill:#a3d5ff,color:#000
    style CHECK fill:#91e5a3,color:#000
    style BUILD fill:#ffa07a,color:#000
    style RUN fill:#ffcc5c,color:#000
    style TEST fill:#c084fc,color:#000
    style DEBUG fill:#94a3b8,color:#000
    style RELEASE fill:#ef4444,color:#000
```

# 示例：cargo 和 crates
- 在本示例中，我们有一个没有其他依赖项的独立可执行 crate
- 使用以下命令创建一个名为 `helloworld` 的新 crate
```bash
cargo new helloworld
cd helloworld
cat Cargo.toml
```
- 默认情况下，`cargo run` 将编译并运行 crate 的 `debug`（未优化）版本。要执行 `release` 版本，使用 `cargo run --release`
- 注意实际二进制文件位于 `target` 文件夹下的 `debug` 或 `release` 文件夹中
- 我们可能还注意到源文件同目录中有一个名为 `Cargo.lock` 的文件。它是自动生成的，不应手动修改
    - 我们稍后会重新讨论 `Cargo.lock` 的具体用途
