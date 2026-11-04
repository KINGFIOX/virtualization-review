# 原始证据摘录：software

这些是原文/源码，不是正文草稿。行号仅用于追溯。勿把页面断行当成语义断句。

## tcg.rst
原始路径：/home/ubuntu/qemu/docs/devel/tcg.rst
行范围：1–191

```text
1: .. _tcg_internals:
2: 
3: ====================
4: Translator Internals
5: ====================
6: 
7: QEMU is a dynamic translator. When it first encounters a piece of code,
8: it converts it to the host instruction set. Usually dynamic translators
9: are very complicated and highly CPU dependent. QEMU uses some tricks
10: which make it relatively easily portable and simple while achieving good
11: performances.
12: 
13: QEMU's dynamic translation backend is called TCG, for "Tiny Code
14: Generator". For more information, please take a look at :ref:`tcg-ops-ref`.
15: 
16: The following sections outline some notable features and implementation
17: details of QEMU's dynamic translator.
18: 
19: CPU state optimisations
20: -----------------------
21: 
22: The target CPUs have many internal states which change the way they
23: evaluate instructions. In order to achieve a good speed, the
24: translation phase considers that some state information of the virtual
25: CPU cannot change in it. The state is recorded in the Translation
26: Block (TB). If the state changes (e.g. privilege level), a new TB will
27: be generated and the previous TB won't be used anymore until the state
28: matches the state recorded in the previous TB. The same idea can be applied
29: to other aspects of the CPU state.  For example, on x86, if the SS,
30: DS and ES segments have a zero base, then the translator does not even
31: generate an addition for the segment base.
32: 
33: Direct block chaining
34: ---------------------
35: 
36: After each translated basic block is executed, QEMU uses the simulated
37: Program Counter (PC) and other CPU state information (such as the CS
38: segment base value) to find the next basic block.
39: 
40: In its simplest, less optimized form, this is done by exiting from the
41: current TB, going through the TB epilogue, and then back to the
42: main loop. That’s where QEMU looks for the next TB to execute,
43: translating it from the guest architecture if it isn’t already available
44: in memory. Then QEMU proceeds to execute this next TB, starting at the
45: prologue and then moving on to the translated instructions.
46: 
47: Exiting from the TB this way will cause the ``cpu_exec_interrupt()``
48: callback to be re-evaluated before executing additional instructions.
49: It is mandatory to exit this way after any CPU state changes that may
50: unmask interrupts.
51: 
52: In order to accelerate the cases where the TB for the new
53: simulated PC is already available, QEMU has mechanisms that allow
54: multiple TBs to be chained directly, without having to go back to the
55: main loop as described above. These mechanisms are:
56: 
57: ``lookup_and_goto_ptr``
58: ^^^^^^^^^^^^^^^^^^^^^^^
59: 
60: Calling ``tcg_gen_lookup_and_goto_ptr()`` will emit a call to
61: ``helper_lookup_tb_ptr``. This helper will look for an existing TB that
62: matches the current CPU state. If the destination TB is available its
63: code address is returned, otherwise the address of the JIT epilogue is
64: returned. The call to the helper is always followed by the tcg ``goto_ptr``
65: opcode, which branches to the returned address. In this way, we either
66: branch to the next TB or return to the main loop.
67: 
68: ``goto_tb + exit_tb``
69: ^^^^^^^^^^^^^^^^^^^^^
70: 
71: The translation code usually implements branching by performing the
72: following steps:
73: 
74: 1. Call ``tcg_gen_goto_tb()`` passing a jump slot index (either 0 or 1)
75:    as a parameter.
76: 
77: 2. Emit TCG instructions to update the CPU state with any information
78:    that has been assumed constant and is required by the main loop to
79:    correctly locate and execute the next TB. For most guests, this is
80:    just the PC of the branch destination, but others may store additional
81:    data. The information updated in this step must be inferable from both
82:    ``cpu_get_tb_cpu_state()`` and ``cpu_restore_state()``.
83: 
84: 3. Call ``tcg_gen_exit_tb()`` passing the address of the current TB and
85:    the jump slot index again.
86: 
87: Step 1, ``tcg_gen_goto_tb()``, will emit a ``goto_tb`` TCG
88: instruction that later on gets translated to a jump to an address
89: associated with the specified jump slot. Initially, this is the address
90: of step 2's instructions, which update the CPU state information. Step 3,
91: ``tcg_gen_exit_tb()``, exits from the current TB returning a tagged
92: pointer composed of the last executed TB’s address and the jump slot
93: index.
94: 
95: The first time this whole sequence is executed, step 1 simply jumps
96: to step 2. Then the CPU state information gets updated and we exit from
97: the current TB. As a result, the behavior is very similar to the less
98: optimized form described earlier in this section.
99: 
100: Next, the main loop looks for the next TB to execute using the
101: current CPU state information (creating the TB if it wasn’t already
102: available) and, before starting to execute the new TB’s instructions,
103: patches the previously executed TB by associating one of its jump
104: slots (the one specified in the call to ``tcg_gen_exit_tb()``) with the
105: address of the new TB.
106: 
107: The next time this previous TB is executed and we get to that same
108: ``goto_tb`` step, it will already be patched (assuming the destination TB
109: is still in memory) and will jump directly to the first instruction of
110: the destination TB, without going back to the main loop.
111: 
112: For the ``goto_tb + exit_tb`` mechanism to be used, the following
113: conditions need to be satisfied:
114: 
115: * The change in CPU state must be constant, e.g., a direct branch and
116:   not an indirect branch.
117: 
118: * The direct branch cannot cross a page boundary. Memory mappings
119:   may change, causing the code at the destination address to change.
120: 
121: Note that, on step 3 (``tcg_gen_exit_tb()``), in addition to the
122: jump slot index, the address of the TB just executed is also returned.
123: This address corresponds to the TB that will be patched; it may be
124: different than the one that was directly executed from the main loop
125: if the latter had already been chained to other TBs.
126: 
127: Self-modifying code and translated code invalidation
128: ----------------------------------------------------
129: 
130: Self-modifying code is a special challenge in x86 emulation because no
131: instruction cache invalidation is signaled by the application when code
132: is modified.
133: 
134: User-mode emulation marks a host page as write-protected (if it is
135: not already read-only) every time translated code is generated for a
136: basic block.  Then, if a write access is done to the page, Linux raises
137: a SEGV signal. QEMU then invalidates all the translated code in the page
138: and enables write accesses to the page.  For system emulation, write
139: protection is achieved through the software MMU.
140: 
141: Correct translated code invalidation is done efficiently by maintaining
142: a linked list of every translated block contained in a given page. Other
143: linked lists are also maintained to undo direct block chaining.
144: 
145: On RISC targets, correctly written software uses memory barriers and
146: cache flushes, so some of the protection above would not be
147: necessary. However, QEMU still requires that the generated code always
148: matches the target instructions in memory in order to handle
149: exceptions correctly.
150: 
151: Exception support
152: -----------------
153: 
154: longjmp() is used when an exception such as division by zero is
155: encountered.
156: 
157: The host SIGSEGV and SIGBUS signal handlers are used to get invalid
158: memory accesses.  QEMU keeps a map from host program counter to
159: target program counter, and looks up where the exception happened
160: based on the host program counter at the exception point.
161: 
162: On some targets, some bits of the virtual CPU's state are not flushed to the
163: memory until the end of the translation block.  This is done for internal
164: emulation state that is rarely accessed directly by the program and/or changes
165: very often throughout the execution of a translation block---this includes
166: condition codes on x86, delay slots on SPARC, conditional execution on
167: Arm, and so on.  This state is stored for each target instruction, and
168: looked up on exceptions.
169: 
170: MMU emulation
171: -------------
172: 
173: For system emulation QEMU uses a software MMU. In that mode, the MMU
174: virtual to physical address translation is done at every memory
175: access.
176: 
177: QEMU uses an address translation cache (TLB) to speed up the translation.
178: In order to avoid flushing the translated code each time the MMU
179: mappings change, all caches in QEMU are physically indexed.  This
180: means that each basic block is indexed with its physical address.
181: 
182: In order to avoid invalidating the basic block chain when MMU mappings
183: change, chaining is only performed when the destination of the jump
184: shares a page with the basic block that is performing the jump.
185: 
186: The MMU can also distinguish RAM and ROM memory areas from MMIO memory
187: areas.  Access is faster for RAM and ROM because the translation cache also
188: hosts the offset between guest address and host memory.  Accessing MMIO
189: memory areas instead calls out to C code for device emulation.
190: Finally, the MMU helps tracking dirty pages and pages pointed to by
191: translation blocks.
```

## memory.rst
原始路径：/home/ubuntu/qemu/docs/devel/memory.rst
行范围：1–95

```text
1: ==============
2: The memory API
3: ==============
4: 
5: The memory API models the memory and I/O buses and controllers of a QEMU
6: machine.  It attempts to allow modelling of:
7: 
8: - ordinary RAM
9: - memory-mapped I/O (MMIO)
10: - memory controllers that can dynamically reroute physical memory regions
11:   to different destinations
12: 
13: The memory model provides support for
14: 
15: - tracking RAM changes by the guest
16: - setting up coalesced memory for kvm
17: - setting up ioeventfd regions for kvm
18: 
19: Memory is modelled as an acyclic graph of MemoryRegion objects.  Sinks
20: (leaves) are RAM and MMIO regions, while other nodes represent
21: buses, memory controllers, and memory regions that have been rerouted.
22: 
23: In addition to MemoryRegion objects, the memory API provides AddressSpace
24: objects for every root and possibly for intermediate MemoryRegions too.
25: These represent memory as seen from the CPU or a device's viewpoint.
26: 
27: Types of regions
28: ----------------
29: 
30: There are multiple types of memory regions (all represented by a single C type
31: MemoryRegion):
32: 
33: - RAM: a RAM region is simply a range of host memory that can be made available
34:   to the guest.
35:   You typically initialize these with memory_region_init_ram().  Some special
36:   purposes require the variants memory_region_init_resizeable_ram(),
37:   memory_region_init_ram_from_file(), or memory_region_init_ram_ptr().
38: 
39: - MMIO: a range of guest memory that is implemented by host callbacks;
40:   each read or write causes a callback to be called on the host.
41:   You initialize these with memory_region_init_io(), passing it a
42:   MemoryRegionOps structure describing the callbacks.
43: 
44: - ROM: a ROM memory region works like RAM for reads (directly accessing
45:   a region of host memory), and forbids writes. You initialize these with
46:   memory_region_init_rom().
47: 
48: - ROM device: a ROM device memory region works like RAM for reads
49:   (directly accessing a region of host memory), but like MMIO for
50:   writes (invoking a callback).  You initialize these with
51:   memory_region_init_rom_device().
52: 
53: - IOMMU region: an IOMMU region translates addresses of accesses made to it
54:   and forwards them to some other target memory region.  As the name suggests,
55:   these are only needed for modelling an IOMMU, not for simple devices.
56:   You initialize these with memory_region_init_iommu().
57: 
58: - container: a container simply includes other memory regions, each at
59:   a different offset.  Containers are useful for grouping several regions
60:   into one unit.  For example, a PCI BAR may be composed of a RAM region
61:   and an MMIO region.
62: 
63:   A container's subregions are usually non-overlapping.  In some cases it is
64:   useful to have overlapping regions; for example a memory controller that
65:   can overlay a subregion of RAM with MMIO or ROM, or a PCI controller
66:   that does not prevent card from claiming overlapping BARs.
67: 
68:   You initialize a pure container with memory_region_init().
69: 
70: - alias: a subsection of another region. Aliases allow a region to be
71:   split apart into discontiguous regions. Examples of uses are memory
72:   banks used when the guest address space is smaller than the amount
73:   of RAM addressed, or a memory controller that splits main memory to
74:   expose a "PCI hole". You can also create aliases to avoid trying to
75:   add the original region to multiple parents via
76:   `memory_region_add_subregion`.
77: 
78:   Aliases may point to any type of region, including other aliases,
79:   but an alias may not point back to itself, directly or indirectly.
80:   You initialize these with memory_region_init_alias().
81: 
82: - reservation region: a reservation region is primarily for debugging.
83:   It claims I/O space that is not supposed to be handled by QEMU itself.
84:   The typical use is to track parts of the address space which will be
85:   handled by the host kernel when KVM is enabled.  You initialize these
86:   by passing a NULL callback parameter to memory_region_init_io().
87: 
88: It is valid to add subregions to a region which is not a pure container
89: (that is, to an MMIO, RAM or ROM region). This means that the region
90: will act like a container, except that any addresses within the container's
91: region which are not claimed by any subregion are handled by the
92: container itself (ie by its MMIO callbacks or RAM backing). However
93: it is generally possible to achieve the same effect with a pure container
94: one of whose subregions is a low priority "background" region covering
95: the whole address range; this is often clearer and is preferred.
```

## virt.rst
原始路径：/home/ubuntu/qemu/docs/system/riscv/virt.rst
行范围：1–40

```text
1: 'virt' Generic Virtual Platform (``virt``)
2: ==========================================
3: 
4: The ``virt`` board is a platform which does not correspond to any real hardware;
5: it is designed for use in virtual machines. It is the recommended board type
6: if you simply want to run a guest such as Linux and do not care about
7: reproducing the idiosyncrasies and limitations of a particular bit of
8: real-world hardware.
9: 
10: Supported devices
11: -----------------
12: 
13: The ``virt`` machine supports the following devices:
14: 
15: * Up to 512 generic RV32GC/RV64GC cores, with optional extensions
16: * Core Local Interruptor (CLINT)
17: * Platform-Level Interrupt Controller (PLIC)
18: * CFI parallel NOR flash memory
19: * Either 1 or 2 NS16550 compatible UARTs
20: * 1 Google Goldfish RTC
21: * 1 SiFive Test device
22: * 8 virtio-mmio transport devices
23: * 1 generic PCIe host bridge
24: * The fw_cfg device that allows a guest to obtain data from QEMU
25: 
26: The hypervisor extension has been enabled for the default CPU, so virtual
27: machines with hypervisor extension can simply be used without explicitly
28: declaring.
29: 
30: The second UART only exists if a backend is configured explicitly (e.g.
31: with a second ``-serial`` command line option).
32: 
33: Hardware configuration information
34: ----------------------------------
35: 
36: The ``virt`` machine automatically generates a device tree blob ("dtb")
37: which it passes to the guest, if there is no ``-dtb`` option. This provides
38: information about the addresses, interrupt lines and other configuration of
39: the various devices in the system. Guest software should discover the devices
40: that are present in the generated DTB.
```

## virt.rst
原始路径：/home/ubuntu/qemu/docs/system/riscv/virt.rst
行范围：109–139

```text
109: Machine-specific options
110: ------------------------
111: 
112: The following machine-specific options are supported:
113: 
114: - aclint=[on|off]
115: 
116:   When this option is "on", ACLINT devices will be emulated instead of
117:   SiFive CLINT. When not specified, this option is assumed to be "off".
118:   This option is restricted to the TCG accelerator.
119: 
120: - acpi=[on|off|auto]
121: 
122:   When this option is "on" (which is the default), ACPI tables are generated and
123:   exposed as firmware tables etc/acpi/rsdp and etc/acpi/tables.
124: 
125: - aia=[none|aplic|aplic-imsic]
126: 
127:   This option allows selecting interrupt controller defined by the AIA
128:   (advanced interrupt architecture) specification. The "aia=aplic" selects
129:   APLIC (advanced platform level interrupt controller) to handle wired
130:   interrupts whereas the "aia=aplic-imsic" selects APLIC and IMSIC (incoming
131:   message signaled interrupt controller) to handle both wired interrupts and
132:   MSIs. When not specified, this option is assumed to be "none" which selects
133:   SiFive PLIC to handle wired interrupts.
134: 
135:   This option also interacts with '-accel kvm'.  When using "aia=aplic-imsic"
136:   with KVM, it is possible to set the use of the kernel irqchip in split mode
137:   by using "-accel kvm,kernel-irqchip=split".  In this case the ``virt`` machine
138:   will emulate the APLIC controller instead of using the APLIC controller from
139:   the irqchip.  See :ref:`riscv-aia` for more details on all available AIA
```

## insn32.decode
原始路径：/home/ubuntu/qemu/target/riscv/insn32.decode
行范围：142–169

```text
142: lb       ............     ..... 000 ..... 0000011 @i
143: lh       ............     ..... 001 ..... 0000011 @i
144: lw       ............     ..... 010 ..... 0000011 @i
145: lbu      ............     ..... 100 ..... 0000011 @i
146: lhu      ............     ..... 101 ..... 0000011 @i
147: sb       .......  .....   ..... 000 ..... 0100011 @s
148: sh       .......  .....   ..... 001 ..... 0100011 @s
149: sw       .......  .....   ..... 010 ..... 0100011 @s
150: addi     ............     ..... 000 ..... 0010011 @i
151: slti     ............     ..... 010 ..... 0010011 @i
152: sltiu    ............     ..... 011 ..... 0010011 @i
153: xori     ............     ..... 100 ..... 0010011 @i
154: # cbo.prefetch_{i,r,m} instructions are ori with rd=x0 and not decoded.
155: ori      ............     ..... 110 ..... 0010011 @i
156: andi     ............     ..... 111 ..... 0010011 @i
157: slli     00000. ......    ..... 001 ..... 0010011 @sh
158: srli     00000. ......    ..... 101 ..... 0010011 @sh
159: srai     01000. ......    ..... 101 ..... 0010011 @sh
160: add      0000000 .....    ..... 000 ..... 0110011 @r
161: sub      0100000 .....    ..... 000 ..... 0110011 @r
162: sll      0000000 .....    ..... 001 ..... 0110011 @r
163: slt      0000000 .....    ..... 010 ..... 0110011 @r
164: sltu     0000000 .....    ..... 011 ..... 0110011 @r
165: xor      0000000 .....    ..... 100 ..... 0110011 @r
166: srl      0000000 .....    ..... 101 ..... 0110011 @r
167: sra      0100000 .....    ..... 101 ..... 0110011 @r
168: or       0000000 .....    ..... 110 ..... 0110011 @r
169: and      0000000 .....    ..... 111 ..... 0110011 @r
```

## trans_rvi.c.inc
原始路径：/home/ubuntu/qemu/target/riscv/tcg/insn_trans/trans_rvi.c.inc
行范围：700–723

```text
700:     if (shamt >= 64) {
701:         tcg_gen_sari_tl(retl, src1h, shamt - 64);
702:         tcg_gen_sari_tl(reth, src1h, 63);
703:     } else {
704:         tcg_gen_extract2_tl(retl, src1l, src1h, shamt);
705:         tcg_gen_sari_tl(reth, src1h, shamt);
706:     }
707: }
708: 
709: static bool trans_srai(DisasContext *ctx, arg_srai *a)
710: {
711:     return gen_shift_imm_fn_per_ol(ctx, a, EXT_NONE,
712:                                    tcg_gen_sari_tl, gen_sraiw, gen_srai_i128);
713: }
714: 
715: static bool trans_add(DisasContext *ctx, arg_add *a)
716: {
717:     return gen_arith(ctx, a, EXT_NONE, tcg_gen_add_tl, tcg_gen_add2_tl);
718: }
719: 
720: static bool trans_sub(DisasContext *ctx, arg_sub *a)
721: {
722:     return gen_arith(ctx, a, EXT_NONE, tcg_gen_sub_tl, tcg_gen_sub2_tl);
723: }
```

## tcg.c
原始路径：/home/ubuntu/qemu/tcg/tcg.c
行范围：6606–6655

```text
6606: int tcg_gen_code(TCGContext *s, TranslationBlock *tb, uint64_t pc_start)
6607: {
6608:     int i, num_insns;
6609:     TCGOp *op;
6610: 
6611:     if (unlikely(qemu_loglevel_mask(CPU_LOG_TB_OP)
6612:                  && qemu_log_in_addr_range(pc_start))) {
6613:         FILE *logfile = qemu_log_trylock();
6614:         if (logfile) {
6615:             fprintf(logfile, "OP:\n");
6616:             tcg_dump_ops(s, logfile, false);
6617:             fprintf(logfile, "\n");
6618:             qemu_log_unlock(logfile);
6619:         }
6620:     }
6621: 
6622: #ifdef CONFIG_DEBUG_TCG
6623:     /* Ensure all labels referenced have been emitted.  */
6624:     {
6625:         TCGLabel *l;
6626:         bool error = false;
6627: 
6628:         QSIMPLEQ_FOREACH(l, &s->labels, next) {
6629:             if (unlikely(!l->present) && !QSIMPLEQ_EMPTY(&l->branches)) {
6630:                 qemu_log_mask(CPU_LOG_TB_OP,
6631:                               "$L%d referenced but not present.\n", l->id);
6632:                 error = true;
6633:             }
6634:         }
6635:         assert(!error);
6636:     }
6637: #endif
6638: 
6639:     /* Do not reuse any EBB that may be allocated within the TB. */
6640:     tcg_temp_ebb_reset_freed(s);
6641: 
6642:     tcg_optimize(s);
6643: 
6644:     reachable_code_pass(s);
6645:     liveness_pass_0(s);
6646:     liveness_pass_1(s);
6647: 
6648:     if (s->nb_indirects > 0) {
6649:         if (unlikely(qemu_loglevel_mask(CPU_LOG_TB_OP_IND)
6650:                      && qemu_log_in_addr_range(pc_start))) {
6651:             FILE *logfile = qemu_log_trylock();
6652:             if (logfile) {
6653:                 fprintf(logfile, "OP before indirect lowering:\n");
6654:                 tcg_dump_ops(s, logfile, false);
6655:                 fprintf(logfile, "\n");
```

## tcg-opc.h
原始路径：/home/ubuntu/qemu/include/tcg/tcg-opc.h
行范围：28–45

```text
28: 
29: /* predefined ops */
30: DEF(discard, 1, 0, 0, TCG_OPF_NOT_PRESENT)
31: DEF(set_label, 0, 0, 1, TCG_OPF_BB_END | TCG_OPF_NOT_PRESENT)
32: 
33: /* variable number of parameters */
34: DEF(call, 0, 0, 3, TCG_OPF_CALL_CLOBBER | TCG_OPF_NOT_PRESENT)
35: 
36: DEF(br, 0, 0, 1, TCG_OPF_BB_END | TCG_OPF_NOT_PRESENT)
37: DEF(brcond, 0, 2, 2, TCG_OPF_BB_END | TCG_OPF_COND_BRANCH | TCG_OPF_INT)
38: 
39: DEF(mb, 0, 0, 1, TCG_OPF_NOT_PRESENT)
40: 
41: DEF(mov, 1, 1, 0, TCG_OPF_INT | TCG_OPF_NOT_PRESENT)
42: 
43: DEF(add, 1, 2, 0, TCG_OPF_INT)
44: DEF(and, 1, 2, 0, TCG_OPF_INT)
45: DEF(andc, 1, 2, 0, TCG_OPF_INT)
```

## cpu-exec.c
原始路径：/home/ubuntu/qemu/accel/tcg/cpu-exec.c
行范围：940–1010

```text
940: /* main execution loop */
941: 
942: static int __attribute__((noinline))
943: cpu_exec_loop(CPUState *cpu, SyncClocks *sc)
944: {
945:     int excp;
946: 
947:     /* if an exception is pending, we execute it here */
948:     while (!cpu_handle_exception(cpu, &excp)) {
949:         TranslationBlock *last_tb = NULL;
950:         int tb_exit = 0;
951: 
952:         while (!cpu_handle_interrupt(cpu, &last_tb)) {
953:             TranslationBlock *tb;
954:             TCGTBCPUState s = cpu->cc->tcg_ops->get_tb_cpu_state(cpu);
955:             s.cflags = cpu->cflags_next_tb;
956: 
957:             /*
958:              * When requested, use an exact setting for cflags for the next
959:              * execution.  This is used for icount, precise smc, and stop-
960:              * after-access watchpoints.  Since this request should never
961:              * have CF_INVALID set, -1 is a convenient invalid value that
962:              * does not require tcg headers for cpu_common_reset.
963:              */
964:             if (s.cflags == -1) {
965:                 s.cflags = curr_cflags(cpu);
966:             } else {
967:                 cpu->cflags_next_tb = -1;
968:             }
969: 
970:             if (check_for_breakpoints(cpu, s.pc, &s.cflags)) {
971:                 break;
972:             }
973: 
974:             tb = tb_lookup(cpu, s);
975:             if (tb == NULL) {
976:                 CPUJumpCache *jc;
977:                 uint32_t h;
978: 
979:                 mmap_lock();
980:                 tb = tb_gen_code(cpu, s);
981:                 mmap_unlock();
982: 
983:                 /*
984:                  * We add the TB in the virtual pc hash table
985:                  * for the fast lookup
986:                  */
987:                 h = tb_jmp_cache_hash_func(s.pc);
988:                 jc = cpu->tb_jmp_cache;
989:                 jc->array[h].pc = s.pc;
990:                 qatomic_set(&jc->array[h].tb, tb);
991:             }
992: 
993: #ifndef CONFIG_USER_ONLY
994:             /*
995:              * We don't take care of direct jumps when address mapping
996:              * changes in system emulation.  So it's not safe to make a
997:              * direct jump to a TB spanning two pages because the mapping
998:              * for the second page can change.
999:              */
1000:             if (tb_page_addr1(tb) != -1) {
1001:                 last_tb = NULL;
1002:             }
1003: #endif
1004:             /* See if we can patch the calling TB. */
1005:             if (last_tb) {
1006:                 tb_add_jump(last_tb, tb_exit, tb);
1007:             }
1008: 
1009:             cpu_loop_exec_tb(cpu, tb, s.pc, &last_tb, &tb_exit);
1010: 
```

## tcg-accel-ops.c
原始路径：/home/ubuntu/qemu/accel/tcg/tcg-accel-ops.c
行范围：97–111

```text
97: /* mask must never be zero, except for A20 change call */
98: void tcg_handle_interrupt(CPUState *cpu, int mask)
99: {
100:     cpu_set_interrupt(cpu, mask);
101: 
102:     /*
103:      * If called from iothread context, wake the target cpu in
104:      * case its halted.
105:      */
106:     if (!qemu_cpu_is_self(cpu)) {
107:         qemu_cpu_kick(cpu);
108:     } else {
109:         qatomic_set(&cpu->neg.icount_decr.u16.high, -1);
110:     }
111: }
```

## cpu_helper.c
原始路径：/home/ubuntu/qemu/target/riscv/tcg/cpu_helper.c
行范围：497–518

```text
497: bool riscv_cpu_exec_interrupt(CPUState *cs, int interrupt_request)
498: {
499:     uint32_t mask = CPU_INTERRUPT_HARD | CPU_INTERRUPT_RNMI;
500: 
501:     if (interrupt_request & mask) {
502:         RISCVCPU *cpu = RISCV_CPU(cs);
503:         CPURISCVState *env = &cpu->env;
504: 
505:         if (cpu->cfg.ext_sdext && !env->debug_mode &&
506:             (env->dcsr & DCSR_STEP) && !(env->dcsr & DCSR_STEPIE)) {
507:             return false;
508:         }
509: 
510:         int interruptno = riscv_cpu_local_irq_pending(env);
511:         if (interruptno >= 0) {
512:             cs->exception_index = RISCV_EXCP_INT_FLAG | interruptno;
513:             riscv_cpu_do_interrupt(cs);
514:             return true;
515:         }
516:     }
517:     return false;
518: }
```

## cpu_helper.c
原始路径：/home/ubuntu/qemu/target/riscv/tcg/cpu_helper.c
行范围：645–684

```text
645: void riscv_cpu_interrupt(CPURISCVState *env)
646: {
647:     uint64_t gein, vsgein = 0, vstip = 0, irqf = 0;
648:     CPUState *cs = env_cpu(env);
649: 
650:     BQL_LOCK_GUARD();
651: 
652:     if (env->virt_enabled) {
653:         gein = get_field(env->hstatus, HSTATUS_VGEIN);
654:         vsgein = (env->hgeip & (1ULL << gein)) ? MIP_VSEIP : 0;
655:         irqf = env->hvien & env->hvip & env->vsie;
656:     } else {
657:         irqf = env->mvien & env->mvip & env->sie;
658:     }
659: 
660:     vstip = env->vstime_irq ? MIP_VSTIP : 0;
661: 
662:     if (riscv_cpu_get_mip(env) | vsgein | vstip | irqf) {
663:         cpu_interrupt(cs, CPU_INTERRUPT_HARD);
664:     } else {
665:         cpu_reset_interrupt(cs, CPU_INTERRUPT_HARD);
666:     }
667: }
668: 
669: uint64_t riscv_cpu_update_mip(CPURISCVState *env, uint64_t mask, uint64_t value)
670: {
671:     uint64_t old;
672: 
673:     /* No need to update mip for VSTIP */
674:     mask = ((mask == MIP_VSTIP) && env->vstime_irq) ? 0 : mask;
675: 
676:     BQL_LOCK_GUARD();
677: 
678:     old = riscv_cpu_get_mip(env);
679:     qatomic_set(&env->mip, (old & ~mask) | (value & mask));
680: 
681:     riscv_cpu_interrupt(env);
682: 
683:     return old;
684: }
```

## cpu_helper.c
原始路径：/home/ubuntu/qemu/target/riscv/tcg/cpu_helper.c
行范围：1853–1910

```text
1853:     } else {
1854:         /* Single stage lookup */
1855:         ret = get_physical_address(env, &pa, &prot, address, NULL,
1856:                                    access_type, mmu_idx, true, false, false,
1857:                                    probe);
1858: 
1859:         qemu_log_mask(CPU_LOG_MMU,
1860:                       "%s address=%" VADDR_PRIx " ret %d physical "
1861:                       HWADDR_FMT_plx " prot %d\n",
1862:                       __func__, address, ret, pa, prot);
1863: 
1864:         if (ret == TRANSLATE_SUCCESS) {
1865:             ret = get_physical_address_pmp(env, &prot_pmp, pa,
1866:                                            size, access_type, mode);
1867:             tlb_size = pmp_get_tlb_size(env, pa);
1868: 
1869:             qemu_log_mask(CPU_LOG_MMU,
1870:                           "%s PMP address=" HWADDR_FMT_plx " ret %d prot"
1871:                           " %d tlb_size %" HWADDR_PRIu "\n",
1872:                           __func__, pa, ret, prot_pmp, tlb_size);
1873: 
1874:             prot &= prot_pmp;
1875:         }
1876:     }
1877: 
1878:     if (ret == TRANSLATE_PMP_FAIL || ret == TRANSLATE_PMA_FAIL) {
1879:         pmp_pma_violation = true;
1880:     }
1881: 
1882:     if (ret == TRANSLATE_SUCCESS) {
1883:         tlb_set_page(cs, address & ~(tlb_size - 1), pa & ~(tlb_size - 1),
1884:                      prot, mmu_idx, tlb_size);
1885:         return true;
1886:     } else if (probe) {
1887:         return false;
1888:     } else {
1889:         int wp_access = 0;
1890: 
1891:         if (access_type == MMU_DATA_LOAD) {
1892:             wp_access |= BP_MEM_READ;
1893:         } else if (access_type == MMU_DATA_STORE) {
1894:             wp_access |= BP_MEM_WRITE;
1895:         }
1896: 
1897:         /*
1898:          * If a watchpoint isn't found for 'addr' this will
1899:          * be a no-op and we'll resume the mmu_exception path.
1900:          * Otherwise we'll throw a debug exception and execution
1901:          * will continue elsewhere.
1902:          */
1903:         cpu_check_watchpoint(cs, address, size, MEMTXATTRS_UNSPECIFIED,
1904:                              wp_access, retaddr);
1905: 
1906:         raise_mmu_exception(env, address, access_type, pmp_pma_violation,
1907:                             first_stage_error, two_stage_lookup,
1908:                             two_stage_indirect_error);
1909:         cpu_loop_exit_restore(cs, retaddr);
1910:     }
```

## cputlb.c
原始路径：/home/ubuntu/qemu/accel/tcg/cputlb.c
行范围：1025–1104

```text
1025: void tlb_set_page_full(CPUState *cpu, int mmu_idx,
1026:                        vaddr addr, CPUTLBEntryFull *full)
1027: {
1028:     CPUTLB *tlb = &cpu->neg.tlb;
1029:     CPUTLBDesc *desc = &tlb->d[mmu_idx];
1030:     MemoryRegionSection *section;
1031:     unsigned int index, read_flags, write_flags;
1032:     uintptr_t addend;
1033:     CPUTLBEntry *te, tn;
1034:     hwaddr iotlb, xlat, sz, paddr_page;
1035:     vaddr addr_page;
1036:     int asidx, wp_flags, prot;
1037:     bool is_ram, is_romd;
1038: 
1039:     assert_cpu_is_self(cpu);
1040: 
1041:     if (full->lg_page_size <= TARGET_PAGE_BITS) {
1042:         sz = TARGET_PAGE_SIZE;
1043:     } else {
1044:         sz = (hwaddr)1 << full->lg_page_size;
1045:         tlb_add_large_page(cpu, mmu_idx, addr, sz);
1046:     }
1047:     addr_page = addr & TARGET_PAGE_MASK;
1048:     paddr_page = full->phys_addr & TARGET_PAGE_MASK;
1049: 
1050:     prot = full->prot;
1051:     asidx = cpu_asidx_from_attrs(cpu, full->attrs);
1052:     section = address_space_translate_for_iotlb(cpu, asidx, paddr_page,
1053:                                                 &xlat, &sz, full->attrs, &prot);
1054:     assert(sz >= TARGET_PAGE_SIZE);
1055: 
1056:     tlb_debug("vaddr=%016" VADDR_PRIx " paddr=0x" HWADDR_FMT_plx
1057:               " prot=%x idx=%d\n",
1058:               addr, full->phys_addr, prot, mmu_idx);
1059: 
1060:     read_flags = full->tlb_fill_flags;
1061:     if (full->lg_page_size < TARGET_PAGE_BITS) {
1062:         /* Repeat the MMU check and TLB fill on every access.  */
1063:         read_flags |= TLB_INVALID_MASK;
1064:     }
1065: 
1066:     is_ram = memory_region_is_ram(section->mr);
1067:     is_romd = memory_region_is_romd(section->mr);
1068: 
1069:     if (is_ram || is_romd) {
1070:         /* RAM and ROMD both have associated host memory. */
1071:         addend = (uintptr_t)memory_region_get_ram_ptr(section->mr) + xlat;
1072:     } else {
1073:         /* I/O does not; force the host address to NULL. */
1074:         addend = 0;
1075:     }
1076: 
1077:     write_flags = read_flags;
1078:     if (is_ram) {
1079:         iotlb = memory_region_get_ram_addr(section->mr) + xlat;
1080:         assert(!(iotlb & ~TARGET_PAGE_MASK));
1081:         /*
1082:          * Computing is_clean is expensive; avoid all that unless
1083:          * the page is actually writable.
1084:          */
1085:         if (prot & PAGE_WRITE) {
1086:             if (section->readonly) {
1087:                 write_flags |= TLB_DISCARD_WRITE;
1088:             } else if (physical_memory_is_clean(iotlb)) {
1089:                 write_flags |= TLB_NOTDIRTY;
1090:             }
1091:         }
1092:     } else {
1093:         /* I/O or ROMD */
1094:         iotlb = xlat;
1095:         /*
1096:          * Writes to romd devices must go through MMIO to enable write.
1097:          * Reads to romd devices go through the ram_ptr found above,
1098:          * but of course reads to I/O must go through MMIO.
1099:          */
1100:         write_flags |= TLB_MMIO;
1101:         if (!is_romd) {
1102:             read_flags = write_flags;
1103:         }
1104:     }
```

## sifive_plic.c
原始路径：/home/ubuntu/qemu/hw/intc/sifive_plic.c
行范围：76–136

```text
76: {
77:     uint32_t max_irq = 0;
78:     uint32_t max_prio = plic->target_priority[addrid];
79:     int i, j;
80:     int num_irq_in_word = 32;
81: 
82:     for (i = 0; i < plic->bitfield_words; i++) {
83:         uint32_t pending_enabled_not_claimed =
84:                         (plic->pending[i] & ~plic->claimed[i]) &
85:                             plic->enable[addrid * plic->bitfield_words + i];
86: 
87:         if (!pending_enabled_not_claimed) {
88:             continue;
89:         }
90: 
91:         if (i == (plic->bitfield_words - 1)) {
92:             /*
93:              * If plic->num_sources is not multiple of 32, num-of-irq in last
94:              * word is not 32. Compute the num-of-irq of last word to avoid
95:              * out-of-bound access of source_priority array.
96:              */
97:             num_irq_in_word = plic->num_sources - ((plic->bitfield_words - 1) << 5);
98:         }
99: 
100:         for (j = 0; j < num_irq_in_word; j++) {
101:             int irq = (i << 5) + j;
102:             uint32_t prio = plic->source_priority[irq];
103:             int enabled = pending_enabled_not_claimed & (1 << j);
104: 
105:             if (enabled && prio > max_prio) {
106:                 max_irq = irq;
107:                 max_prio = prio;
108:             }
109:         }
110:     }
111: 
112:     return max_irq;
113: }
114: 
115: static void sifive_plic_update(SiFivePLICState *plic)
116: {
117:     int addrid;
118: 
119:     /* raise irq on harts where this irq is enabled */
120:     for (addrid = 0; addrid < plic->num_addrs; addrid++) {
121:         uint32_t hartid = plic->addr_config[addrid].hartid;
122:         PLICMode mode = plic->addr_config[addrid].mode;
123:         bool level = !!sifive_plic_claimed(plic, addrid);
124: 
125:         switch (mode) {
126:         case PLICMode_M:
127:             qemu_set_irq(plic->m_external_irqs[hartid - plic->hartid_base], level);
128:             break;
129:         case PLICMode_S:
130:             qemu_set_irq(plic->s_external_irqs[hartid - plic->hartid_base], level);
131:             break;
132:         default:
133:             break;
134:         }
135:     }
136: }
```

## sifive_plic.c
原始路径：/home/ubuntu/qemu/hw/intc/sifive_plic.c
行范围：353–361

```text
353: static void sifive_plic_irq_request(void *opaque, int irq, int level)
354: {
355:     SiFivePLICState *s = opaque;
356: 
357:     if (level > 0) {
358:         sifive_plic_set_pending(s, irq, true);
359:         sifive_plic_update(s);
360:     }
361: }
```

## serial-mm.c
原始路径：/home/ubuntu/qemu/hw/char/serial-mm.c
行范围：33–84

```text
33: static uint64_t serial_mm_read(void *opaque, hwaddr addr, unsigned size)
34: {
35:     SerialMM *s = SERIAL_MM(opaque);
36:     return serial_io_ops.read(&s->serial, addr >> s->regshift, 1);
37: }
38: 
39: static void serial_mm_write(void *opaque, hwaddr addr,
40:                             uint64_t value, unsigned size)
41: {
42:     SerialMM *s = SERIAL_MM(opaque);
43:     value &= 255;
44:     serial_io_ops.write(&s->serial, addr >> s->regshift, value, 1);
45: }
46: 
47: static const MemoryRegionOps serial_mm_ops[] = {
48:     [DEVICE_NATIVE_ENDIAN] = {
49:         .read = serial_mm_read,
50:         .write = serial_mm_write,
51:         .endianness = DEVICE_NATIVE_ENDIAN,
52:         .valid.max_access_size = 8,
53:         .impl.max_access_size = 8,
54:     },
55:     [DEVICE_LITTLE_ENDIAN] = {
56:         .read = serial_mm_read,
57:         .write = serial_mm_write,
58:         .endianness = DEVICE_LITTLE_ENDIAN,
59:         .valid.max_access_size = 8,
60:         .impl.max_access_size = 8,
61:     },
62:     [DEVICE_BIG_ENDIAN] = {
63:         .read = serial_mm_read,
64:         .write = serial_mm_write,
65:         .endianness = DEVICE_BIG_ENDIAN,
66:         .valid.max_access_size = 8,
67:         .impl.max_access_size = 8,
68:     },
69: };
70: 
71: static void serial_mm_realize(DeviceState *dev, Error **errp)
72: {
73:     SerialMM *smm = SERIAL_MM(dev);
74:     SerialState *s = &smm->serial;
75: 
76:     if (!qdev_realize(DEVICE(s), NULL, errp)) {
77:         return;
78:     }
79: 
80:     memory_region_init_io(&s->io, OBJECT(dev),
81:                           &serial_mm_ops[smm->endianness], smm, "serial",
82:                           8 << smm->regshift);
83:     sysbus_init_mmio(SYS_BUS_DEVICE(smm), &s->io);
84:     sysbus_init_irq(SYS_BUS_DEVICE(smm), &smm->serial.irq);
```

## serial.c
原始路径：/home/ubuntu/qemu/hw/char/serial.c
行范围：123–151

```text
123: static void serial_update_irq(SerialState *s)
124: {
125:     uint8_t tmp_iir = UART_IIR_NO_INT;
126: 
127:     if ((s->ier & UART_IER_RLSI) && (s->lsr & UART_LSR_INT_ANY)) {
128:         tmp_iir = UART_IIR_RLSI;
129:     } else if ((s->ier & UART_IER_RDI) && s->timeout_ipending) {
130:         /* Note that(s->ier & UART_IER_RDI) can mask this interrupt,
131:          * this is not in the specification but is observed on existing
132:          * hardware.  */
133:         tmp_iir = UART_IIR_CTI;
134:     } else if ((s->ier & UART_IER_RDI) && (s->lsr & UART_LSR_DR) &&
135:                (!(s->fcr & UART_FCR_FE) ||
136:                 fifo8_num_used(&s->recv_fifo) >= s->recv_fifo_itl)) {
137:         tmp_iir = UART_IIR_RDI;
138:     } else if ((s->ier & UART_IER_THRI) && s->thr_ipending) {
139:         tmp_iir = UART_IIR_THRI;
140:     } else if ((s->ier & UART_IER_MSI) && (s->msr & UART_MSR_ANY_DELTA)) {
141:         tmp_iir = UART_IIR_MSI;
142:     }
143: 
144:     s->iir = tmp_iir | (s->iir & 0xF0);
145: 
146:     if (tmp_iir != UART_IIR_NO_INT) {
147:         qemu_irq_raise(s->irq);
148:     } else {
149:         qemu_irq_lower(s->irq);
150:     }
151: }
```

## virtio-blk.c
原始路径：/home/ubuntu/qemu/hw/block/virtio-blk.c
行范围：57–69

```text
57: void virtio_blk_req_complete(VirtIOBlockReq *req, unsigned char status)
58: {
59:     VirtIOBlock *s = req->dev;
60:     VirtIODevice *vdev = VIRTIO_DEVICE(s);
61: 
62:     trace_virtio_blk_req_complete(vdev, req, status);
63: 
64:     stb_p(&req->in->status, status);
65:     iov_discard_undo(&req->inhdr_undo);
66:     iov_discard_undo(&req->outhdr_undo);
67:     virtqueue_push(req->vq, &req->elem, req->in_len);
68:     virtio_notify(vdev, req->vq);
69: }
```

## virtio-blk.c
原始路径：/home/ubuntu/qemu/hw/block/virtio-blk.c
行范围：1098–1146

```text
1098: void virtio_blk_handle_vq(VirtIOBlock *s, VirtQueue *vq)
1099: {
1100:     VirtIOBlockReq *req;
1101:     MultiReqBuffer mrb = {};
1102:     bool suppress_notifications = virtio_queue_get_notification(vq);
1103: 
1104:     defer_call_begin();
1105: 
1106:     do {
1107:         if (suppress_notifications) {
1108:             virtio_queue_set_notification(vq, 0);
1109:         }
1110: 
1111:         while ((req = virtio_blk_get_request(s, vq))) {
1112:             if (virtio_blk_handle_request(req, &mrb)) {
1113:                 virtqueue_detach_element(req->vq, &req->elem, 0);
1114:                 g_free(req);
1115:                 break;
1116:             }
1117:         }
1118: 
1119:         if (suppress_notifications) {
1120:             virtio_queue_set_notification(vq, 1);
1121:         }
1122:     } while (!virtio_queue_empty(vq));
1123: 
1124:     if (mrb.num_reqs) {
1125:         virtio_blk_submit_multireq(s, &mrb);
1126:     }
1127: 
1128:     defer_call_end();
1129: }
1130: 
1131: static void virtio_blk_handle_output(VirtIODevice *vdev, VirtQueue *vq)
1132: {
1133:     VirtIOBlock *s = (VirtIOBlock *)vdev;
1134: 
1135:     if (!s->ioeventfd_disabled && !s->ioeventfd_started) {
1136:         /* Some guests kick before setting VIRTIO_CONFIG_S_DRIVER_OK so start
1137:          * ioeventfd here instead of waiting for .set_status().
1138:          */
1139:         virtio_device_start_ioeventfd(vdev);
1140:         if (!s->ioeventfd_disabled) {
1141:             return;
1142:         }
1143:     }
1144: 
1145:     virtio_blk_handle_vq(s, vq);
1146: }
```

## Bellard - 2005 - QEMU, a Fast and Portable Dynamic Translator.md
原始路径：/home/ubuntu/高级操作系统教程/references/Bellard - 2005 - QEMU, a Fast and Portable Dynamic Translator.md
行范围：50–112

```text
50: This article examines the implementation of the dy-
51: namic translator used by QEMU. The dynamic transla-
52: tor performs a runtime conversion of the target CPU in-
53: structions into the host instruction set. The resulting bi-
54: nary code is stored in a translation cache so that it can
55: be reused. The advantage compared to an interpreter is
56: that the target instructions are fetched and decoded only
57: once.
58: Usually dynamic translators are difﬁcult to port from
59: one host to another because the whole code generator
60: must be rewritten. It represents about the same amount
61: of work as adding a new target to a C compiler. QEMU
62: is much simpler because it just concatenates pieces of
63: machine code generated off line by the GNU C Compiler
64: [5].
65: A CPU emulator also faces other more classical but
66: difﬁcult [2] problems:
67: • Management of the translated code cache
68: • Register allocation
69: • Condition code optimizations
70: • Direct block chaining
71: • Memory management
72: • Self-modifying code support
73: FREENIX Track: 2005 USENIX Annual Technical Conference
74: USENIX Association
75: 41
76: 
77: <!-- page 2 -->
78: 
79: • Exception support
80: • Hardware interrupts
81: • User mode emulation
82: 2
83: Portable dynamic translation
84: 2.1
85: Description
86: The ﬁrst step is to split each target CPU instruction into
87: fewer simpler instructions called micro operations. Each
88: micro operation is implemented by a small piece of C
89: code. This small C source code is compiled by GCC to
90: an object ﬁle. The micro operations are chosen so that
91: their number is much smaller (typically a few hundreds)
92: than all the combinations of instructions and operands
93: of the target CPU. The translation from target CPU in-
94: structions to micro operations is done entirely with hand
95: coded code. The source code is optimized for readability
96: and compactness because the speed of this stage is less
97: critical than in an interpreter.
98: A compile time tool called dyngen uses the object
99: ﬁle containing the micro operations as input to generate a
100: dynamic code generator. This dynamic code generator is
101: invoked at runtime to generate a complete host function
102: which concatenates several micro operations.
103: The process is similar to [1], but more work is done
104: at compile time to get better performance. In particu-
105: lar, a key idea is that in QEMU constant parameters can
106: be given to micro operations. For that purpose, dummy
107: code relocations are generated with GCC for each con-
108: stant parameter. This enables the dyngen tool to locate
109: the relocations and generate the appropriate C code to re-
110: solve them when building the dynamic code. Relocations
111: are also supported to enable references to static data and
112: to other functions in the micro operations.
```
