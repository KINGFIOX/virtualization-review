# 正文撰写简报（所有写作任务共用）

## 角色与交付

你是本项目的中文学术综述正文撰写者。请根据指定新提纲、主代理核验的证据包，写可以直接编译的 LaTeX 正文，而不是再写提纲。主代理负责审校、主文件、参考文献和图形。只写本次指派的 .tex 文件，不改其他章节、主文件、脚本、配置、技能或记忆。

项目根：`/home/ubuntu/高级操作系统教程/virtualization-review`。
新提纲：`/home/ubuntu/高级操作系统教程/作业/期中报告_选题与提纲.md`。
禁用材料：`/home/ubuntu/高级操作系统教程/midterm/` 全目录、`作业/第1章_软件虚拟化.md`。不得读取、复制或参考，也不得全目录搜索误扫到它们。旧章节不是来源。

## 论文主线

题目《虚拟化技术综述：从软件模拟到硬件辅助与嵌套虚拟化》。
0 引言(P&G 1974和四维工程框架)；1 QEMU全系统TCG软件虚拟化，RISC-V→TCG IR→x86_64；2 Armv8.6-A的EL2、S2、GICv3/4、SMMUv3+Linux KVM；3 x86-64/Intel VMX的Turtles与HyperTurtle；结语不编号。

按“资源与状态由谁控制、关键路径怎样执行、何时介入、代价何在”组织。CPU/内存/中断/设备在软件和硬件两部分必须各自成节。HyperTurtle是重点近期论文，但不要把整个报告变成eBPF入门。

## 行文

- 用中文学术文章的连续段落。不能把提纲逐条扩成短句列表，不能每段以加粗标签开头。不要读者问答、拟人修辞、夸张宣传、套话；避免“下面我们来看”“值得注意的是”反复出现。
- 每节形成因果解释：设计约束→实现→例子或执行路径→边界。写清谁读/写什么、箭头是什么，不空喊“软硬协同”。
- 术语首次出现给必要中英文，此后保持一致。寄存器/函数是证据，不罗列十几个名字代替解释。最多给很短的示意指令/伪代码，并标明不是实测。
- 不写自我介绍、个人实验经历、课堂评分、作业DDL、文件目录管理或“本机验证成功”等工作流元话语。
- 没有真实复现；性能数字只能写“论文报告”，并指明配置、指标、基线。未给来源的数量、历史首创、绝对安全性和性能范围不得添加。
- 论断引用使用下面限定的BibTeX键，段内合适处 `\cite{source7}`；可写 `\cite[\S3.3]{source7}`。不要手写[1]，也不要用Markdown链接。
- 原文可能两栏错行或OCR断词；以段落语义为准，无法可靠确定的细节删掉，不猜。

## 已核验的技术边界

1. P&G三性质是定义，敏感⊆特权是其机器模型的充分条件。四维是本文的工程框架，原文形式模型排除了I/O和中断。跨ISA的QEMU模拟不满足P&G的直接执行式效率定义，不能用TB缓存将其偷换成满足。
2. TCG是现代QEMU的翻译器，Bellard 2005用dyngen，是历史出处。TB不一定严格等于一个基本块；helper调用不必封块；guest异常存在，只是软件实现。指令示例不要声称ALU恒1:1。
3. 软件地址关系guest VA→guest PA→QEMU HVA；host MMU另管HVA→HPA。软件TLB miss不等于guest页故障。guest PA的RAM与MMIO通过MemoryRegion/AddressSpace分流。CPU页表不自动用于设备DMA。
4. QEMU中断路径区分设备状态、控制器pending、CPU通知/kick与架构投递；TB chaining不表示漏中断。软件中断模型选PLIC+CLINT，不展开AIA或guest H扩展。
5. Arm异常只自动记录必要异常返回信息，完整GPR/FP/系统寄存器由KVM软件管理。guest exit不等于一定返回QEMU；MMIO先走内核总线，未处理才KVM_EXIT_MMIO。
6. S2有TLB/page walk成本，不是免费；guest页表自身访存也走S2。HVA不是硬件翻译的第三阶段。
7. GICv3已经有虚拟CPU接口，GICv4添加vLPI直接注入；未驻留vPE需doorbell/调度，控制面并不全硬件化。GIC规范独立于Arm ISA版本。
8. SMMU管真实DMA，不能模拟设备。S2-only是一种架构路径；Linux普通直通域也会选宿主管理S1，不能据此推出guest有vIOMMU。guest管理的I/O S1是可选。软件设备访存不必经过物理SMMU。
9. amd64是ISA称谓，不等于AMD SVM。Turtles/HyperTurtle用Intel VMCS/EPT；Turtles的软件VMCS shadowing不是后来硬件同名功能。L0判断exit归属，不是所有事件都逐层转发。
10. HyperTurtle安装由L1 hypercall经L0 KVM/QEMU；热路径才在L0内核hook执行。受限helper、VM归属和并发同步与verifier共同保证隔离。EPT处理保留内存池/日志满、加锁失败等回退；原型EPT hook只支持一个L1的一个L2，网络hook不是同一限制。DVH是L0虚拟网卡分配给L2，不是物理网卡直通。
11. HyperTurtle评测有固定绑核/NUMA、SMT关闭、idle=poll/nopti，吞吐实验调整vCPU数量；启动测到应用响应请求，不仅是kernel boot。代码行数要分清系统总改动与某项改动。
12. 不引入Arm FEAT_NV/VNCR同构论，也不写“P&G定理第二层失效”。

## 引用键（固定，不得新增未核验来源）

- `source1`: Popek & Goldberg, Formal Requirements for Virtualizable Third Generation Architectures, CACM 17(7), 1974, 412–421。
- `source2`: Bellard, QEMU, a Fast and Portable Dynamic Translator, USENIX ATC FREENIX, 2005。
- `source3`: QEMU项目源码与开发文档，commit 56afd82bd4db9688f1c1c9d0e2ea163b8cde3283。
- `source4`: Arm Architecture Reference Manual Armv8-A, DDI0487F.b，2020。
- `source5`: Linux源码7.0.14，KVM/arm64、KVM/x86、SMMUv3。
- `source6`: Dall & Nieh, KVM/ARM: The Design and Implementation of the Linux ARM Hypervisor, ASPLOS 2014。历史ARMv7/Cortex-A15背景，不是Armv8.6实测。
- `source7`: Ben-Yehuda et al., The Turtles Project: Design and Implementation of Nested Virtualization, OSDI 2010。
- `source8`: Ben Zur et al., Accelerating Nested Virtualization with HyperTurtle, USENIX ATC 2025, 987–1002。
- `source9`: Arm GIC Architecture Specification, GICv3/v4, IHI0069D，2017。
- `source10`: Arm SMMU Architecture Specification, SMMUv3.0/3.1, IHI0070B，2017。

源码引用可写成段末引文，加短脚注，如 `\footnote{QEMU: \path{accel/tcg/cputlb.c}，\code{tlb_set_page_full()}。}`。优先函数+路径，不要将所有长本地绝对路径抄进正文。

## LaTeX接口

主文档使用XeLaTeX/ctexart；主代理提供amsmath、amssymb、booktabs、tabularx、longtable、listings、TikZ、enumitem、natbib[numbers]、hyperref、xurl。
正文文件不含documentclass、preamble、begin/end document或bibliography。
代码标识写 `\code{HCR_EL2}`（此宏可接受未转义下划线）；文件路径写 `\path{arch/arm64/kvm/mmu.c}`。普通文本中的百分号写\%，下划线写\_，x86_64正文最好写x86-64。
引用标签：章用sec:intro、sec:software、sec:hardware、sec:nested；小节标签自行加唯一前缀，跨章引用仅用这些章标签。

主代理会实际生成以下图文件，按任务指定在合适处插入一次 `\input{...}` 并在附近解释，勿重新定义同名label、勿写“图待补”。
- `figures/tcg-pipeline.tex`，label fig:tcg：译时三级流水线与运行时TB复用。
- `figures/software-memory.tex`，label fig:softmem：GVA→软件TLB/guest MMU→GPA→RAM或MMIO。
- `figures/software-interrupt.tex`，label fig:softirq：设备→PLIC→pending/kick→CPU异常。
- `figures/arm-platform.tex`，label fig:arm：CPU两阶段访存、设备SMMU、GIC中断三路分工。
- `figures/gic-delivery.tex`，label fig:gic：GICv3注入与GICv4驻留/doorbell分支。
- `figures/nested-mapping.tex`，label fig:nested：VMCS01/12/02与EPT逻辑/实际映射。
- `figures/hyperupcall.tex`，label fig:hyperupcall：普通事件L2→L0→L1→L0→L2与HT就地处理。

表格用tabularx或固定列宽，整表不超过\linewidth。不用复杂TikZ，你只需\input上述已分配的图文件。

## 操作顺序

用read_file读取本简报、任务指定的新提纲范围与证据包；资料足够后直接撰写，用write_file写指定正文。可以按小节分批写文件以免长输出丢失；若覆盖已经存在的文件先完整读取。最后简报仅报告路径、实际写了哪些小节及未解决的事实问题，不要把全文再复制到最终聊天。
