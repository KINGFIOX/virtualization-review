请作为本篇中文综述的正式正文撰写者完成分配章节。
首先读取 /home/ubuntu/高级操作系统教程/virtualization-review/editorial/writing-brief.md 并遵守全部内容与LaTeX接口。
只允许写本次指定的章节文件；不得编辑其他文件。禁止参考旧midterm或旧第1章。
正文要连续论述和机制解释，不是要点提纲，不得写“待补”“待核验”或假造实测。

输出文件：/home/ubuntu/高级操作系统教程/virtualization-review/chapters/02-hardware.tex
写第2部分Armv8.6-A硬件辅助虚拟化与KVM，目标4000–5000汉字。
读取新提纲第113–167行及 /home/ubuntu/高级操作系统教程/virtualization-review/editorial/evidence-hardware.md。
输出以\section{硬件辅助虚拟化：Arm架构与KVM}\label{sec:hardware}开头。
必须五个subsection：CPU EL2与上下文；内存VA→IPA→PA；GICv3/v4中断；SMMUv3设备；协作小结。每个维度有完整处理路径及硬件/软件归属。以EL2/HCR/SPSR/ELR/eret基本机制为重，VHE/nVHE和FGT等只点到为止。
给两阶段翻译式并解释guest页表访存走S2、TLB和权限。说明MMIO并不都返回QEMU。
GICv3已经虚拟CPU接口，解释ICH状态与guest ICC访问；GICv4只是vLPI直达等，不全硬件化。
SMMU先讲DMA再STE/CD/S1/S2，普通直通可无vIOMMU且Linux可能用host S1；完整设备直通需VFIO/GIC/复位，软件设备并非经物理SMMU。
插入\input{figures/arm-platform.tex}、\input{figures/gic-delivery.tex}各一次并解释。不得写Arm NV/NV2/VNCR章节。
请现在读材料并实际写入指定文件，结束时只给简短交付摘要。
