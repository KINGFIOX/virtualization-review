#!/usr/bin/env python3
"""Build bounded, line-anchored primary-source packs for chapter writers."""
from pathlib import Path
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT.parent
Q = Path('/home/ubuntu/qemu')
K = Path('/home/ubuntu/linux-source-7.0.0')
A = Path('/home/ubuntu/aarch64/manuals')
R = COURSE / 'references'
SCRATCH = Path('/home/ubuntu/.hermes/cache/scratch/virtualization-outline')
OUT = ROOT / 'editorial'
OUT.mkdir(parents=True, exist_ok=True)

sources = {
    'pg': R / 'Popek and Goldberg - 1974 - Formal requirements for virtualizable third generation architectures.md',
    'bellard': R / 'Bellard - 2005 - QEMU, a Fast and Portable Dynamic Translator.md',
    'kvmarm': R / 'Dall and Nieh - 2014 - KVMARM the design and implementation of the linux ARM hypervisor.md',
    'turtles': R / 'Ben-Yehuda et al. - 2010 - The Turtles Project Design and Implementation of Nested Virtualization.md',
    'arm': A / 'armv8_arm_v8.6.md',
    'gic': A / 'ARM_IHI0069D_GIC_Architecture_Spec_v3.0_v4.0.md',
    'smmu': SCRATCH / 'smmuv3.txt',
}
cache = {}
manifest = []

def excerpt(path, start, end, title=''):
    path = Path(path).resolve()
    assert 'midterm' not in path.parts
    assert path.name != '第1章_软件虚拟化.md'
    if path not in cache:
        cache[path] = path.read_text(encoding='utf-8').splitlines()
    lines = cache[path]
    if not (1 <= start <= end <= len(lines)):
        raise ValueError((str(path), start, end, len(lines)))
    manifest.append({'path': str(path), 'first_line': start, 'last_line': end})
    body = '\n'.join(f'{i}: {lines[i-1]}' for i in range(start, end+1))
    return f'\n## {title or path.name}\n原始路径：{path}\n行范围：{start}–{end}\n\n```text\n{body}\n```\n'

def pack(name, specs):
    body = '# 原始证据摘录：' + name + '\n\n这些是原文/源码，不是正文草稿。行号仅用于追溯。勿把页面断行当成语义断句。\n'
    for spec in specs:
        body += excerpt(*spec)
    target = OUT / f'evidence-{name}.md'
    target.write_text(body, encoding='utf-8')
    print(json.dumps({'pack': str(target), 'characters': len(body), 'lines': len(body.splitlines())}, ensure_ascii=False))

pack('intro', [
    (sources['pg'],151,218), (sources['pg'],250,328),
    (sources['pg'],383,431), (sources['pg'],510,548),
    (sources['pg'],643,730), (sources['pg'],950,991),
    (sources['bellard'],3,57),
])
pack('software', [
    (Q/'docs/devel/tcg.rst',1,191),
    (Q/'docs/devel/memory.rst',1,95),
    (Q/'docs/system/riscv/virt.rst',1,40),
    (Q/'docs/system/riscv/virt.rst',109,139),
    (Q/'target/riscv/insn32.decode',142,169),
    (Q/'target/riscv/tcg/insn_trans/trans_rvi.c.inc',700,723),
    (Q/'tcg/tcg.c',6606,6655),
    (Q/'include/tcg/tcg-opc.h',28,45),
    (Q/'accel/tcg/cpu-exec.c',940,1010),
    (Q/'accel/tcg/tcg-accel-ops.c',97,111),
    (Q/'target/riscv/tcg/cpu_helper.c',497,518),
    (Q/'target/riscv/tcg/cpu_helper.c',645,684),
    (Q/'target/riscv/tcg/cpu_helper.c',1853,1910),
    (Q/'accel/tcg/cputlb.c',1025,1104),
    (Q/'hw/intc/sifive_plic.c',76,136),
    (Q/'hw/intc/sifive_plic.c',353,361),
    (Q/'hw/char/serial-mm.c',33,84),
    (Q/'hw/char/serial.c',123,151),
    (Q/'hw/block/virtio-blk.c',57,69),
    (Q/'hw/block/virtio-blk.c',1098,1146),
    (sources['bellard'],50,112),
])
pack('hardware', [
    (sources['arm'],154270,154322),
    (sources['arm'],155402,155436),
    (sources['arm'],169645,169685),
    (K/'arch/arm64/kvm/arm.c',1191,1220),
    (K/'arch/arm64/kvm/hyp/entry.S',70,88),
    (K/'arch/arm64/kvm/hyp/entry.S',121,151),
    (K/'arch/arm64/kvm/mmu.c',2153,2226),
    (K/'arch/arm64/kvm/mmio.c',225,259),
    (sources['gic'],4204,4286),
    (sources['gic'],4380,4432),
    (sources['gic'],4648,4776),
    (K/'arch/arm64/kvm/vgic/vgic-v3.c',366,397),
    (K/'arch/arm64/kvm/vgic/vgic-v4.c',84,105),
    (sources['smmu'],1142,1239),
    (sources['smmu'],1391,1427),
    (sources['smmu'],2456,2528),
    (K/'drivers/iommu/arm/arm-smmu-v3/arm-smmu-v3.c',3368,3404),
    (sources['kvmarm'],14,34),
    (sources['kvmarm'],165,177),
])
pack('nested-turtles', [
    (sources['turtles'],24,44),
    (sources['turtles'],220,238),
    (sources['turtles'],320,467),
    (sources['turtles'],468,616),
    (sources['turtles'],617,737),
    (sources['turtles'],789,892),
    (sources['turtles'],1186,1200),
])
# Re-extract the complete formal paper, avoiding web_extract's internal truncation.
subprocess.run(['pdftotext', str(SCRATCH/'hyperturtle.pdf'), str(OUT/'hyperturtle-full.txt')], check=True)
subprocess.run(['pdftotext', '-f', '5', '-l', '14', str(SCRATCH/'hyperturtle.pdf'), str(OUT/'evidence-hyperturtle.txt')], check=True)
# Retain locally available original sources in a map, without copying excluded drafts.
(OUT/'source-map.json').write_text(json.dumps({k:str(v) for k,v in sources.items()}, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
(OUT/'evidence-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print('Evidence packs complete; all source ranges validated.')
