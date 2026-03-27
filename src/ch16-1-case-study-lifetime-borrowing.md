# 案例研究 3：框架通信 → 生命周期借用

> **你将学到什么：** 如何将 C++ 原始指针框架通信模式转换为 Rust 的基于生命周期的借用系统，在保持零成本抽象的同时消除悬空指针风险。

## C++ 模式：指向框架的原始指针
```cpp
// C++ 原始代码：每个诊断模块存储指向框架的原始指针
class DiagBase {
protected:
    DiagFramework* m_pFramework;  // 原始指针 —— 谁拥有这个？
public:
    DiagBase(DiagFramework* fw) : m_pFramework(fw) {}
    
    void LogEvent(uint32_t code, const std::string& msg) {
        m_pFramework->GetEventLog()->Record(code, msg);  // 希望它还活着！
    }
};
// 问题：m_pFramework 是没有生命周期保证的原始指针
// 如果框架在模块仍引用它时被销毁 → UB
```

## Rust 解决方案：带生命周期借用的 DiagContext
```rust
// 示例：module.rs —— 借用，不存储

/// 执行期间传递给诊断模块的上下文。
/// 生命周期 'a 保证框架比上下文活得长。
pub struct DiagContext<'a> {
    pub der_log: &'a mut EventLogManager,
    pub config: &'a ModuleConfig,
