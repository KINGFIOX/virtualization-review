请作为本篇中文综述的正式正文撰写者完成分配章节。
首先读取 /home/ubuntu/高级操作系统教程/virtualization-review/editorial/writing-brief.md 并遵守全部内容与LaTeX接口。
只允许写本次指定的章节文件；不得编辑其他文件。禁止参考旧midterm或旧第1章。
正文要连续论述和机制解释，不是要点提纲，不得写“待补”“待核验”或假造实测。

输出文件：/home/ubuntu/高级操作系统教程/virtualization-review/chapters/01-software.tex
写第1部分QEMU全系统软件虚拟化，目标4000–5000汉字。
读取新提纲第49–111行及 /home/ubuntu/高级操作系统教程/virtualization-review/editorial/evidence-software.md。
输出以\section{软件虚拟化：QEMU的全系统实现}\label{sec:software}开头。
必须五个subsection：CPU虚拟化、内存虚拟化、中断虚拟化、设备虚拟化、能力与成本。CPU篇幅不超过本章一半。
CPU必须有RISC-V→TCG IR→x86-64三级路径、示意add/lw/CSR的区别，TB缓存与链接，以及helper语义边界。只给语义示意，未跑trace，不声称具体宿主机器码实测。
内存写完整miss refill与guest fault区分；中断写串口→PLIC→pending/kick→架构投递与定时器；设备写MMIO回调及virtio-blk提交/后端/完成链，区分软件DMA与CPU页表。
恰当插入\input{figures/tcg-pipeline.tex}、\input{figures/software-memory.tex}、\input{figures/software-interrupt.tex}各一次并解释。无需自己画TikZ。
请现在读材料并实际写入指定文件，结束时只给简短交付摘要。
