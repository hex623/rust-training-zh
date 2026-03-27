## 迭代器高级工具参考

> **你将学到什么：** 超越 `filter`/`map`/`collect` 的高级迭代器组合器 —— `enumerate`、`zip`、`chain`、`flat_map`、`scan`、`windows` 和 `chunks`。对于将 C 风格索引 `for` 循环替换为安全、表达性强的 Rust 迭代器至关重要。

基本的 `filter`/`map`/`collect` 链涵盖许多情况，但 Rust 的迭代器库
丰富得多。本节涵盖你每天会用的工具 —— 尤其是
翻译手动跟踪索引、累积结果或以固定大小块处理数据的 C 循环时。

### 快速参考表

| 方法 | C 等效 | 作用 | 返回 |
|--------|-------------|-------------|---------|
| `enumerate()` | `for (int i=0; ...)` | 将每个元素与其索引配对 | `(usize, T)` |
| `zip(other)` | 相同索引的并行数组 | 将两个迭代器的元素配对 | `(A, B)` |
| `chain(other)` | 先处理 array1 再处理 array2 | 连接两个迭代器 | `T` |
| `flat_map(f)` | 嵌套循环 | 映射然后展平一层 | `U` |
| `windows(n)` | `for (int i=0; i<len-n+1; i++) &arr[i..i+n]` | 大小为 `n` 的重叠切片 | `\u0026[T]` |
| `chunks(n)` | 一次处理 `n` 个元素 | 大小为 `n` 的不重叠切片 | `\u0026[T]` |
| `fold(init, f)` | `int acc = init; for (...) acc = f(acc, x);` | 归约为单个值 | `Acc` |
| `scan(init, f)` | 带输出的运行累加器 | 类似 `fold` 但产生中间结果 | `Option<B>` |
| `take(n)` / `skip(n)` | 从偏移开始循环 / 限制 | 前 `n` 个 / 跳过前 `n` 个元素 | `T` |
| `take_while(f)` / `skip_while(f)` | `while (pred) {...}` | 当谓词成立时取/跳过 | `T` |
| `peekable()` | 用 `arr[i+1]` 前瞻 | 允许 `.peek()` 而不消耗 | `T` |
| `step_by(n)` | `for (i=0; i<len; i+=n)` | 每第 n 个元素 | `T` |
| `unzip()` | 拆分并行数组 | 将配对收集到两个集合 | `(A, B)` |
| `sum()` / `product()` | 累积和/积 | 用 `+` 或 `*` 归约 | `T` |
| `min()` / `max()` | 找极值 | 返回 `Option<T>` | `Option<T>` |
| `any(f)` / `all(f)` | `bool found = false; for (...) ...` | 短路布尔搜索 | `bool` |
| `position(f)` | `for (i=0; ...) if (pred) return i;` | 第一个匹配的索引 | `Option<usize>` |
