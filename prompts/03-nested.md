请作为本篇中文综述的正式正文撰写者完成分配章节。
首先读取 /home/ubuntu/高级操作系统教程/virtualization-review/editorial/writing-brief.md 并遵守全部内容与LaTeX接口。
只允许写本次指定的章节文件；不得编辑其他文件。禁止参考旧midterm或旧第1章。
正文要连续论述和机制解释，不是要点提纲，不得写“待补”“待核验”或假造实测。

输出文件：/home/ubuntu/高级操作系统教程/virtualization-review/chapters/03-nested.tex
（编辑后已拆分为 chapters/03-turtles.tex 与 chapters/04-hyperturtle.tex；本文件仅作调用记录保留）
写第3部分x86-64嵌套虚拟化及主论文评议，目标5000–6500汉字，HyperTurtle至少占本章一半。
读取新提纲第169–262行、/home/ubuntu/高级操作系统教程/virtualization-review/editorial/evidence-nested-turtles.md、/home/ubuntu/高级操作系统教程/virtualization-review/editorial/evidence-hyperturtle.txt；必要时读取同目录hyperturtle-full.txt。若文本超过单次读取限制要分段读完所需部分。
输出以\section{嵌套虚拟化：从Turtles到HyperTurtle}\label{sec:nested}开头。
涵盖L0/L1/L2动机，Turtles CPU/内存/中断/设备四维（subsubsection），world-switch成本，HyperTurtle注册与状态共享，EPT核心处理细节及回退，网络和profiling，实验证据评议，局限与后续问题。不要复述大段eBPF基础。
明确Intel VMX/VMCS/EPT；Turtles当年的设计不等于当前KVM所有路径。HyperTurtle的VMCS/EPT软件机制不得移植术语成EL2。
至少一个实验数据表，写出论文数据、基线、配置，不要生成不存在的原始测量值。已核数据可用：正文§5.1说平均EPT fault延迟改善5.25倍/99p4.76倍（图9a标5.26，故文字用“约5.25”并注明是原论文）；§5.2图10普通嵌套比较HT，4KiB/2MiB页启动时间平均降27%/8%。网络或profiling数据必须从你读到的表图文字核实，不能凭印象。
评议必须提SMT关闭、固定NUMA/绑核、idle=poll/nopti；启动测到服务响应非仅boot；无L1策略的DVH不是同等管理能力基线；EPT hook一个L1一个L2限制不等于网络全受限。国内产业结合只给可推导的云/安全容器场景，不编造已部署事实。
插入 figures/turtles-architecture.png 与 figures/hyperupcall.tex 各一次，图的解释必须与算法/状态一致。（编辑后内存节改用 figures/turtles-mmu-models.png，原 TikZ 图已移除。）最后一节提出具体可测量的开放问题，不写空泛展望。
请现在读材料并实际写入指定文件，结束时只给简短交付摘要。
