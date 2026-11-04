# 技术审校说明

正文初稿由指定 DeepSeek 模型撰写，随后依据原论文与源码做内容审校。以下说明仅保留在编辑目录，不放进课程报告。

## 已处理的关键问题

- P&G 的效率条件是统计上占主导的 guest 指令直接执行，不是“敏感指令直接执行”。四维框架由本文采用，原论文的形式模型明确排除中断与 I/O。
- QEMU 2005 年的 dyngen 与现代 TCG 分开。TB 不等于严格单基本块，helper 不自动终止 TB，优化后宿主指令数不能由 guest 指令数推算。
- 软件 TLB 按 guest 虚拟页与 MMU 上下文查询；代码页与 TB 的物理地址关联是不同结构。未沿用开发文档中“所有缓存物理索引”的过宽概括。
- RISC-V 全系统异常路径使用目标 MMU/异常逻辑，不套用其他 ISA 的除法异常或 user-mode 的宿主信号处理流程。
- TCG 的轻量退出请求检查和完整 guest 中断仲裁分开：`accel/tcg/translator.c:gen_tb_start()`、`tcg-accel-ops.c:tcg_handle_interrupt()`、`cpu-exec.c` 与 RISC-V 目标中断函数构成不同层次。
- CLINT 兼容定时器复用 ACLINT 实现并使用 `QEMU_CLOCK_VIRTUAL`；虚拟时钟不等于默认保证确定性重放。MMIO 指的是 guest 设备访问的分发，不是先对宿主物理 MMIO 写一次。
- VHE 是让 host Linux 内核运行 EL2 的实现支持，不是仅把 EL2 当入口。硬件异常记录 ELR/SPSR 等，GPR/FP/系统寄存器管理仍由 KVM 软件负责。
- guest 正常 Stage-1 fault 通常直接交 guest，不能写成一律由 KVM 注入；Stage-2 fault 和内核/用户态 MMIO 处理分别说明。
- GIC 的 VMCR 控制虚拟接口状态，VTR 报告实现能力；GICv3 已有虚拟接口，GICv4 vLPI 直接注入不等于所有中断都免软件介入。
- SMMU 配置/命令由软件生产，但事件/PRI 队列是硬件向软件报告；普通宿主 S1 域不意味着 guest 存在 vIOMMU。映射 BAR 的直接访问和受控 MMIO 模拟没有混成同一条路径。
- Turtles 的 L0 VMCS 合并优化与修改 L1 的 DRW 实验区分。14.5% kernbench、约7.8% SPECjbb 以及 DRW 配置不可合并成统一6–8%性能上界。
- HyperTurtle 的 EPT、网络与 profiling 按各自实验度量整理。没有把动机分析绝对延迟与另一实验加速比拼接推算新数据；保留 §5.1 文本5.25和图9a标注5.26的末位差异说明。
- HyperTurtle 实验配置与生产环境的差异作为外推限制，没有代作者声称这些设置是为了“放大切换占比”；`idle=poll` 也不是“关闭中断合并”。

## 排版与构建

使用独立项目和 XeLaTeX/BibTeX。图形先单独编译，再整合正文；修复了字体解析、标题字体命令、长代码标识的断行问题。实际诊断与自动检查保存在 `build/main-diagnostics.json` 和 `build/verification.json`，以最终构建结果为准。

## 尚不声称完成的工作

- 没有运行 QEMU/KVM/HyperTurtle 性能复现实验。
- 没有完成多租户安全证明或生产部署验证。
- 没有代作者提交课程系统、上传 Overleaf 或同步 Notion。
