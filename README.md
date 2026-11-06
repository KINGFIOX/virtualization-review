# 虚拟化技术综述 · LaTeX 初稿

主文件：`main.tex`。正文按新提纲组织为第 0—4 部分（嵌套虚拟化拆为两章），结语不编号；软件与硬件两部分各自覆盖 CPU、内存、中断、设备四个维度，嵌套两章分别处理“把多层语义做对”与“削减跨层往返”。

## 构建

在本目录运行：

```sh
python scripts/build_latex.py main
python scripts/verify_latex.py
```

输出：`build/main.pdf`。构建脚本实际执行 XeLaTeX → BibTeX → XeLaTeX → XeLaTeX，不依赖 latexmk 或 biber，也不启用 shell escape。

环境依赖：XeLaTeX、BibTeX、Poppler（`pdftotext`/`pdfinfo`）、ctex、TikZ、natbib、booktabs、tabularx、xurl，以及 Noto CJK、DejaVu Sans Mono、URW Nimbus OpenType 字体。`preamble.tex` 对 Nimbus 的 OTF 文件作了显式选择，避免本机同名字体的 Type-1 路径解析问题；其他机器可在此调整字体。

## 文件结构

- `chapters/00-intro.tex`：Popek–Goldberg 与四维框架。
- `chapters/01-software.tex`：QEMU TCG 全系统软件虚拟化。
- `chapters/02-hardware.tex`：Armv8.6-A 与 KVM 的硬件辅助机制。
- `chapters/03-turtles.tex`：嵌套问题建立、Turtles 四维机制、Turtles 开销与评测、小结。
- `chapters/04-hyperturtle.tex`：性能问题重新定位、HyperTurtle 通用机制与两个案例、实验评议、局限与开放问题。
- 两个嵌套章节由同一次写作任务（`prompts/03-nested.md`）产出后拆分，`logs/03-nested-usage.json` 记录那次调用。
- `chapters/frontmatter.tex` / `conclusion.tex`：摘要、关键词与结语。
- `figures/`：可直接编辑的 TikZ 机制图与规范/论文原图（`.png`）两类；原图在 caption 中注明出处。
- `references.bib`：原论文、架构手册及源码资料。
- `editorial/`：写作简报、原始证据摘录、资料定位与审校说明（不进入论文）。
- `prompts/` / `logs/`：DeepSeek 写作任务与实际模型用量/完成记录（不进入论文）。
- `build/`：编译产物、日志、文字抽取、排版校验结果与预览。

## 写作与证据边界

正文初稿通过用户确认的 `glm-gateway-r`（via feilian）调用 `deepseek-v4-pro` 撰写，调用以 `logs/*-usage.json` 记录的模型为准。Hermes 负责定界、证据准备、技术审校、图形、参考文献与编译验证。

正文没有使用旧 `midterm/` 或 `作业/第1章_软件虚拟化.md`。报告是文献与源码综述，不声称复现论文实验；表中性能数字均标明原论文和基线。QEMU 源码基准为 commit `56afd82bd4db9688f1c1c9d0e2ea163b8cde3283`，Linux 源码基准为 Makefile 标识的 7.0.14，CPU 规范采用 DDI 0487F.b。GIC 与 SMMU 使用各自独立规范。

`verify_latex.py` 检查章节与四维小节、所有 TeX 输入、引用键、交叉引用标签、机制图数量、残留占位符，以及实际 PDF 的文字边界和编译诊断。它不能替代技术审稿；关键语义与数值已另行对原文核查，说明见 `editorial/review-notes.md`。

这是一份可继续修改的课程报告初稿。提交前仍需作者通读，确认观点、篇幅和课程要求；未上传到选课系统、Notion 或 Overleaf。
