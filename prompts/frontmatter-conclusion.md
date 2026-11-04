请完成本综述的摘要与结语，使用中文学术文章语气。先读 /home/ubuntu/高级操作系统教程/virtualization-review/editorial/writing-brief.md 和新提纲 /home/ubuntu/高级操作系统教程/作业/期中报告_选题与提纲.md。可参考本项目 chapters/00-intro.tex 与 chapters/01-software.tex（已审校），不要读取其他旧稿或midterm。你只写下列两个新文件，不修改其他文件。

1. /home/ubuntu/高级操作系统教程/virtualization-review/chapters/frontmatter.tex
以 \begin{abstract} 开头，以 \end{abstract} 结束，然后另起一行关键词。摘要300–420汉字，概括问题、研究范围、四维框架、软件实现与硬件辅助分工、Turtles与HyperTurtle机制和综述判断。没有新实验，不使用“提出新系统/我们实验发现”，不要列性能数字，不放引用。

2. /home/ubuntu/高级操作系统教程/virtualization-review/chapters/conclusion.tex
以 \section*{结语}\phantomsection\addcontentsline{toc}{section}{结语} 开头。正文600–900汉字，不能重新逐节复述。集中三个判断：四维必须协作；硬件减少软件介入但管理/设备语义仍需软件；嵌套需要组合资源边界和上层策略，HyperTurtle适用的是可安全下放且一致性成本可控的热路径。说明不能由单机/固定绑核实验直接推断多租户生产收益，但不要编造不支持。可少量引用 source3/source4/source7/source8。
结语里加一张不超过\linewidth的tabularx对照表：列为维度、QEMU软件、Arm硬件辅助、x86-64嵌套；4行CPU/内存/中断/设备；每格简短（15–35汉字）。表头只一个短l列，其余用Y。

注意：正文不能反复使用“不是...而是...”、'下面我们来看'、'值得注意的是'、夸张比喻；不能有占位符。只通过write_file实际写入两个文件。最后只报告路径和完成情况。
