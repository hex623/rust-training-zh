## 日志与追踪：syslog/printf → `log` + `tracing`

> **你将学到什么：** Rust 的两层日志架构（门面 + 后端）、`log` 和 `tracing` crate、带 span 的结构化日志，以及这如何替代 `printf`/`syslog` 调试。

C++ 诊断代码通常使用 `printf`、`syslog` 或自定义日志框架。
Rust 有标准化的两层日志架构：**门面** crate（`log` 或
`tracing`）和 **后端**（实际的日志实现）。

### `log` 门面 —— Rust 的通用日志 API

`log` crate 提供镜像 syslog 严重级别的宏。库使用
`log` 宏；二进制文件选择后端：

```rust
// Cargo.toml
// [dependencies]
// log = "0.4"
// env_logger = "0.11"    # 众多后端之一

use log::{info, warn, error, debug, trace};

fn check_sensor(id: u32, temp: f64) {
    trace!("读取传感器 {id}");           // 最细粒度
    debug!("传感器 {id} 原始值: {temp}"); // 开发时细节

    if temp > 85.0 {
        warn!("传感器 {id} 高温: {temp}°C");
    }
    if temp > 95.0 {
        error!("传感器 {id} 严重: {temp}°C —— 正在启动关闭");
