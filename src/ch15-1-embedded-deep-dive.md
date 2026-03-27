## MMIO 和易失寄存器访问

> **你将学到什么：** 嵌入式 Rust 中的类型安全硬件寄存器访问 —— 易变 MMIO 模式、寄存器抽象 crate，以及 Rust 的类型系统如何编码 C 的 `volatile` 关键字无法编码的寄存器权限。

在 C 固件中，你通过 `volatile` 指针访问特定内存地址的硬件寄存器。Rust 有等效机制 —— 但有类型安全。

### C volatile vs Rust volatile

```c
// C —— 典型的 MMIO 寄存器访问
#define GPIO_BASE     0x40020000
#define GPIO_MODER    (*(volatile uint32_t*)(GPIO_BASE + 0x00))
#define GPIO_ODR      (*(volatile uint32_t*)(GPIO_BASE + 0x14))

void toggle_led(void) {
    GPIO_ODR ^= (1 << 5);  // 切换引脚 5
}
```

```rust
// Rust —— 原始易变（底层，很少直接使用）
use core::ptr;

const GPIO_BASE: usize = 0x4002_0000;
const GPIO_ODR: *mut u32 = (GPIO_BASE + 0x14) as *mut u32;

/// # 安全
/// 调用者必须确保 GPIO_BASE 是有效的映射外设地址。
unsafe fn toggle_led() {
    // ...
}
```
