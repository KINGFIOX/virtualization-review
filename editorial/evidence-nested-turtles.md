# 原始证据摘录：nested-turtles

这些是原文/源码，不是正文草稿。行号仅用于追溯。勿把页面断行当成语义断句。

## Ben-Yehuda et al. - 2010 - The Turtles Project Design and Implementation of Nested Virtualization.md
原始路径：/home/ubuntu/高级操作系统教程/references/Ben-Yehuda et al. - 2010 - The Turtles Project Design and Implementation of Nested Virtualization.md
行范围：24–44

```text
24: Abstract
25: In classical machine virtualization, a hypervisor runs
26: multiple operating systems simultaneously, each on its
27: own virtual machine. In nested virtualization, a hypervi-
28: sor can run multiple other hypervisors with their associ-
29: ated virtual machines. As operating systems gain hyper-
30: visor functionality—Microsoft Windows 7 already runs
31: Windows XP in a virtual machine—nested virtualization
32: will become necessary in hypervisors that wish to host
33: them. We present the design, implementation, analysis,
34: and evaluation of high-performance nested virtualization
35: on Intel x86-based systems. The Turtles project, which
36: is part of the Linux/KVM hypervisor, runs multiple un-
37: modiﬁed hypervisors (e.g., KVM and VMware) and op-
38: erating systems (e.g., Linux and Windows). Despite the
39: lack of architectural support for nested virtualization in
40: the x86 architecture, it can achieve performance that is
41: within 6-8% of single-level (non-nested) virtualization
42: for common workloads, through multi-dimensional pag-
43: ing for MMU virtualization and multi-level device as-
44: signment for I/O virtualization.
```

## Ben-Yehuda et al. - 2010 - The Turtles Project Design and Implementation of Nested Virtualization.md
原始路径：/home/ubuntu/高级操作系统教程/references/Ben-Yehuda et al. - 2010 - The Turtles Project Design and Implementation of Nested Virtualization.md
行范围：220–238

```text
220: The IBM Turtles nested virtualization project imple-
221: ments nested virtualization for Intel’s virtualization tech-
222: nology based on the KVM [29] hypervisor. It can host
223: multiple guest hypervisors simultaneously, each with its
224: own multiple nested guest operating systems. We have
225: tested it with unmodiﬁed KVM and VMware Server as
226: guest hypervisors, and unmodiﬁed Linux and Windows
227: as nested guest virtual machines. Since we treat nested
228: hypervisors and virtual machines as unmodiﬁed black
229: boxes, the Turtles project should also run any other x86
230: hypervisor and operating system.
231: The Turtles project is fairly mature: it has been tested
232: running multiple hypervisors simultaneously, supports
233: SMP, and takes advantage of two-dimensional page table
234: hardware where available in order to implement nested
235: MMU virtualization via multi-dimensional paging.
236: It
237: also makes use of multi-level device assignment for efﬁ-
238: cient nested I/O virtualization.
```

## Ben-Yehuda et al. - 2010 - The Turtles Project Design and Implementation of Nested Virtualization.md
原始路径：/home/ubuntu/高级操作系统教程/references/Ben-Yehuda et al. - 2010 - The Turtles Project Design and Implementation of Nested Virtualization.md
行范围：320–467

```text
320: The hypervisor was forced to re-
321: sort to on-the-ﬂy binary translation of privileged instruc-
322: tions [3], slow machine emulation [8], or changes to
323: guest operating systems at the source code level [6] or
324: during compilation [32].
325: In due time Intel and AMD incorporated hardware
326: virtualization extensions in their CPUs.
327: These exten-
328: sions introduced two new modes of operation: root mode
329: and guest mode, enabling the CPU to differentiate be-
330: tween running a virtual machine (guest mode) and run-
331: ning the hypervisor (root mode). Both Intel and AMD
332: also added special in-memory virtual machine control
333: structures (VMCS and VMCB, respectively) which con-
334: tain environment speciﬁcations for virtual machines and
335: the hypervisor.
336: The VMX instruction set and the VMCS layout are ex-
337: plained in detail in [27]. Data stored in the VMCS can be
338: divided into three groups. Guest state holds virtualized
339: CPU registers (e.g., control registers or segment regis-
340: ters) which are automatically loaded by the CPU when
341: switching from root mode to guest mode on VMEntry.
342: Host state is used by the CPU to restore register val-
343: ues when switching back from guest mode to root mode
344: on VMExit. Control data is used by the hypervisor to
345: inject events such as exceptions or interrupts into vir-
346: tual machines and to specify which events should cause
347: a VMExit; it is also used by the CPU to specify the
348: VMExit reason to the hypervisor.
349: In nested virtualization, the hypervisor running in root
350: mode (L0) runs other hypervisors (L1) in guest mode.
351: L1 hypervisors have the illusion they are running in root
352: mode.
353: Their virtual machines (L2) also run in guest
354: mode.
355: As can be seen in Figure 3, L0 is responsible for mul-
356: tiplexing the hardware between L1 and L2. The CPU
357: runs L1 using VMCS0→1 environment speciﬁcation. Re-
358: spectively, VMCS0→2 is used to run L2. Both of these
359: environment speciﬁcations are maintained by L0. In ad-
360: dition, L1 creates VMCS1→2 within its own virtualized
361: environment. Although VMCS1→2 is never loaded into
362: the processor, L0 uses it to emulate a VMX enabled CPU
363: for L1.
364: Figure 3: Extending VMX for nested virtualization
365: 3.2.1
366: VMX Trap and Emulate
367: VMX instructions can only execute successfully in root
368: mode. In the nested case, L1 uses VMX instructions in
369: guest mode to load and launch L2 guests, which causes
370: VMExits. This enables L0, running in root mode, to trap
371: and emulate the VMX instructions executed by L1.
372: In general, when L0 emulates VMX instructions, it
373: updates VMCS structures according to the update pro-
374: cess described in the next section. Then, L0 resumes
375: L1, as though the instructions were executed directly by
376: the CPU. Most of the VMX instructions executed by L1
377: cause, ﬁrst, a VMExit from L1 to L0, and then a VMEn-
378: try from L0 to L1.
379: For
380: the
381: instructions
382: used
383: to
384: run
385: a
386: new
387: VM,
388: vmresume and vmlaunch, the process is different,
389: since L0 needs to emulate a VMEntry from L1 to L2.
390: Therefore, any execution of these instructions by L1
391: cause, ﬁrst, a VMExit from L1 to L0, and then, a VMEn-
392: try from L0 to L2.
393: 3.2.2
394: VMCS Shadowing
395: L0 prepares a VMCS (VMCS0→1) to run L1, exactly in
396: the same way a hypervisor executes a guest with a single
397: level of virtualization. From the hardware’s perspective,
398: the processor is running a single hypervisor (L0) in root
399: mode and a guest (L1) in guest mode. L1 is not aware
400: that it is running in guest mode and uses VMX instruc-
401: tions to create the speciﬁcations for its own guest, L2.
402: L1 deﬁnes L2’s environment by creating a VMCS
403: (VMCS1→2) which contains L2’s environment from L1’s
404: perspective.
405: For example, the VMCS1→2 GUEST-CR3
406: ﬁeld points to the page tables that L1 prepared for L2.
407: L0 cannot use VMCS1→2 to execute L2 directly, since
408: VMCS1→2 is not valid in L0’s environment and L0 can-
409: not use L1’s page tables to run L2. Instead, L0 uses
410: 4
411: 
412: <!-- page 5 -->
413: 
414: VMCS1→2 to construct a new VMCS (VMCS0→2) that
415: holds L2’s environment from L0’s perspective.
416: L0
417: must consider all the speciﬁcations deﬁned
418: in VMCS1→2 and also the speciﬁcations deﬁned in
419: VMCS0→1 to create VMCS0→2. The host state deﬁned in
420: VMCS0→2 must contain the values required by the CPU
421: to correctly switch back from L2 to L0.
422: In addition,
423: VMCS1→2 host state must be copied to VMCS0→1 guest
424: state. Thus, when L0 emulates a switch between L2 to
425: L1, the processor loads the correct L1 speciﬁcations.
426: The guest state stored in VMCS1→2 does not require
427: any special handling in general, and most ﬁelds can be
428: copied directly to the guest state of VMCS0→2.
429: The control data of VMCS1→2 and VMCS0→1 must be
430: merged to correctly emulate the processor behavior. For
431: example, consider the case where L1 speciﬁes to trap an
432: event EA in VMCS1→2 but L0 does not trap such event
433: for L1 (i.e., a trap is not speciﬁed in VMCS0→1). To for-
434: ward the event EA to L1, L0 needs to specify the corre-
435: sponding trap in VMCS0→2. In addition, the ﬁeld used by
436: L1 to inject events to L2 needs to be merged, as well as
437: the ﬁelds used by the processor to specify the exit cause.
438: For the sake of brevity, we omit some details on how
439: speciﬁc VMCS ﬁelds are merged. For the complete de-
440: tails, the interested reader is encouraged to refer to the
441: KVM source code [29].
442: 3.2.3
443: VMEntry and VMExit Emulation
444: In nested environments, switches from L1 to L2 and back
445: must be emulated. When L2 is running and a VMExit
446: occurs there are two possible handling paths, depending
447: on whether the VMExit must be handled only by L0 or
448: must be forwarded to L1.
449: When the event causing the VMExit is related to L0
450: only, L0 handles the event and resumes L2. This kind of
451: event can be an external interrupt, a non-maskable inter-
452: rupt (NMI) or any trappable event speciﬁed in VMCS0→2
453: that was not speciﬁed in VMCS1→2. From L1’s perspec-
454: tive this event does not exist because it was generated
455: outside the scope of L1’s virtualized environment. By
456: analogy to the non-nested scenario, an event occurred at
457: the hardware level, the CPU transparently handled it, and
458: the hypervisor continued running as before.
459: The second handling path is caused by events related
460: to L1 (e.g., trappable events speciﬁed in VMCS1→2).
461: In this case L0 forwards the event to L1 by copying
462: VMCS0→2 ﬁelds updated by the processor to VMCS1→2
463: and resuming L1. The hypervisor running in L1 believes
464: there was a VMExit directly from L2 to L1. The L1 hy-
465: pervisor handles the event and later on resumes L2 by
466: executing vmresume or vmlaunch, both of which will
467: be emulated by L0.
```

## Ben-Yehuda et al. - 2010 - The Turtles Project Design and Implementation of Nested Virtualization.md
原始路径：/home/ubuntu/高级操作系统教程/references/Ben-Yehuda et al. - 2010 - The Turtles Project Design and Implementation of Nested Virtualization.md
行范围：468–616

```text
468: 3.3
469: MMU: Multi-dimensional Paging
470: In addition to virtualizing the CPU, a hypervisor also
471: needs to virtualize the MMU: A guest OS builds a guest
472: page table which translates guest virtual addresses to
473: guest physical addresses. These must be translated again
474: into host physical addresses. With nested virtualization,
475: a third layer of address translation is needed.
476: These translations can be done entirely in software,
477: or assisted by hardware. However, as we explain be-
478: low, current hardware supports only one or two dimen-
479: sions (levels) of translation, not the three needed for
480: nested virtualization. In this section we present a new
481: technique, multi-dimensional paging, for multiplexing
482: the three needed translation tables onto the two avail-
483: able in hardware. In Section 4.1.2 we demonstrate the
484: importance of this technique, showing that more na¨ıve
485: approaches (surveyed below) cause at least a three-fold
486: slowdown of some useful workloads.
487: When no hardware support for memory manage-
488: ment virtualization was available, a technique known as
489: shadow page tables [15] was used. A guest creates a
490: guest page table, which translates guest virtual addresses
491: to guest physical addresses. Based on this table, the hy-
492: pervisor creates a new page table, the shadow page ta-
493: ble, which translates guest virtual addresses directly to
494: the corresponding host physical address [3, 6]. The hy-
495: pervisor then runs the guest using this shadow page table
496: instead of the guest’s page table. The hypervisor has to
497: trap all guest paging changes, including page fault excep-
498: tions, the INVLPG instruction, context switches (which
499: cause the use of a different page table) and all the guest
500: updates to the page table.
501: To improve virtualization performance, x86 architec-
502: tures recently added two-dimensional page tables [13]—
503: a second translation table in the hardware MMU. When
504: translating a guest virtual address, the processor ﬁrst uses
505: the regular guest page table to translate it to a guest phys-
506: ical address. It then uses the second table, called EPT by
507: Intel (and NPT by AMD), to translate the guest physi-
508: cal address to a host physical address. When an entry
509: is missing in the EPT table, the processor generates an
510: EPT violation exception. The hypervisor is responsible
511: for maintaining the EPT table and its cache (which can
512: be ﬂushed with INVEPT), and for handling EPT viola-
513: tions, while guest page faults can be handled entirely by
514: the guest.
515: The hypervisor, depending on the processors capabil-
516: ities, decides whether to use shadow page tables or two-
517: dimensional page tables to virtualize the MMU. In nested
518: environments, both hypervisors, L0 and L1, determine
519: independently the preferred mechanism. Thus, L0 and
520: L1 hypervisors can use the same or a different MMU
521: virtualization mechanism. Figure 4 shows three differ-
522: 5
523: 
524: <!-- page 6 -->
525: 
526: ent nested MMU virtualization models.
527: Figure 4: MMU alternatives for nested virtualization
528: Shadow-on-shadow is used when the processor does
529: not support two-dimensional page tables, and is the least
530: efﬁcient method. Initially, L0 creates a shadow page ta-
531: ble to run L1 (SPT0→1). L1, in turn, creates a shadow
532: page table to run L2 (SPT1→2). L0 cannot use SPT1→2
533: to run L2 because this table translates L2 guest virtual
534: addresses to L1 host physical addresses. Therefore, L0
535: compresses SPT0→1 and SPT1→2 into a single shadow
536: page table, SPT0→2. This new table translates directly
537: from L2 guest virtual addresses to L0 host physical ad-
538: dresses. Speciﬁcally, for each guest virtual address in
539: SPT1→2, L0 creates an entry in SPT0→2 with the corre-
540: sponding L0 host physical address.
541: Shadow-on-EPT is the most straightforward approach
542: to use when the processor supports EPT. L0 uses the EPT
543: hardware, but L1 cannot use it, so it resorts to shadow
544: page tables. L1 uses SPT1→2 to run L2. L0 conﬁgures
545: the MMU to use SPT1→2 as the ﬁrst translation table and
546: EPT0→1 as the second translation table. In this way, the
547: processor ﬁrst translates from L2 guest virtual address to
548: L1 host physical address using SPT1→2, and then trans-
549: lates from the L1 host physical address to the L0 host
550: physical address using the EPT0→1.
551: Though the Shadow-on-EPT approach uses the EPT
552: hardware, it still has a noticeable overhead due to page
553: faults and page table modiﬁcations in L2. These must
554: be handled in L1, to maintain the shadow page ta-
555: ble.
556: Each of these faults and writes cause VMExits
557: and must be forwarded from L0 to L1 for handling. In
558: other words, Shadow-on-EPT is slow for the exactly the
559: same reasons that Shadow itself was slow for single-level
560: virtualization—but it is even slower because nested exits
561: are slower than non-nested exits.
562: In
563: multi-dimensional
564: page
565: tables,
566: as
567: in
568: two-
569: dimensional page tables, each level creates its own sepa-
570: rate translation table. For L1 to create an EPT table, L0
571: exposes EPT capabilities to L1, even though the hard-
572: ware only provides a single EPT table.
573: Since only one EPT table is available in hardware, the
574: two EPT tables should be compressed into one: Let us
575: assume that L0 runs L1 using EPT0→1, and that L1 cre-
576: ates an additional table, EPT1→2, to run L2, because L0
577: exposed a virtualized EPT capability to L1. The L0 hy-
578: pervisor could then compress EPT0→1 and EPT1→2 into
579: a single EPT0→2 table as shown in Figure 4. Then L0
580: could run L2 using EPT0→2, which translates directly
581: from the L2 guest physical address to the L0 host physi-
582: cal address, reducing the number of page fault exits and
583: improving nested virtualization performance.
584: In Sec-
585: tion 4.1.2 we demonstrate more than a three-fold speedup
586: of some useful workloads with multi-dimensional page
587: tables, compared to shadow-on-EPT.
588: The L0 hypervisor launches L2 with an empty EPT0→2
589: table, building the table on-the-ﬂy, on L2 EPT-violation
590: exits. These happen when a translation for a guest phys-
591: ical address is missing in the EPT table. If there is no
592: translation in EPT1→2 for the faulting address, L0 ﬁrst
593: lets L1 handle the exit and update EPT1→2. L0 can now
594: create an entry in EPT0→2 that translates the L2 guest
595: physical address directly to the L0 host physical address:
596: EPT1→2 is used to translate the L2 physical address to a
597: L1 physical address, and EPT0→1 translates that into the
598: desired L0 physical address.
599: To maintain correctness of EPT0→2, the L0 hypervisor
600: needs to know of any changes that L1 makes to EPT1→2.
601: L0 sets the memory area of EPT1→2 as read-only, thereby
602: causing a trap when L1 tries to update it. L0 will then up-
603: date EPT0→2 according to the changed entries in EPT1→2.
604: L0 also needs to trap all L1 INVEPT instructions, and in-
605: validate the EPT cache accordingly.
606: By using huge pages [34] to back guest memory, L0
607: can create smaller and faster EPT tables.
608: Finally, to
609: further improve performance, L0 also allows L1 to use
610: VPIDs. With this feature, the CPU tags each transla-
611: tion in the TLB with a numeric virtual-processor id,
612: eliminating the need for TLB ﬂushes on every VMEn-
613: try and VMExit. Since each hypervisor is free to choose
614: these VPIDs arbitrarily, they might collide and therefore
615: L0 needs to map the VPIDs that L1 uses into valid L0
616: VPIDs.
```

## Ben-Yehuda et al. - 2010 - The Turtles Project Design and Implementation of Nested Virtualization.md
原始路径：/home/ubuntu/高级操作系统教程/references/Ben-Yehuda et al. - 2010 - The Turtles Project Design and Implementation of Nested Virtualization.md
行范围：617–737

```text
617: 3.4
618: I/O: Multi-level Device Assignment
619: I/O is the third major challenge in server virtualization.
620: There are three approaches commonly used to provide
621: I/O services to a guest virtual machine. Either the hyper-
622: visor emulates a known device and the guest uses an un-
623: modiﬁed driver to interact with it [47], or a para-virtual
624: driver is installed in the guest [6,42], or the host assigns
625: a real device to the guest which then controls the device
626: directly [11,31,37,52,53]. Device assignment generally
627: provides the best performance [33,38,53], since it mini-
628: mizes the number of I/O-related world switches between
629: the virtual machine and its hypervisor, and although it
630: complicates live migration, device assignment and live
631: 6
632: 
633: <!-- page 7 -->
634: 
635: migration can peacefully coexist [26,28,54].
636: These three basic I/O approaches for a single-level
637: guest imply nine possible combinations in the two-level
638: nested guest case. Of the nine potential combinations
639: we evaluated the more interesting cases, presented in Ta-
640: ble 1. Implementing the ﬁrst four alternatives is straight-
641: forward.
642: We describe the last option, which we call
643: multi-level device assignment, below.
644: Multi-level de-
645: vice assignment lets the L2 guest access a device di-
646: rectly, bypassing both hypervisors. This direct device
647: access requires dealing with DMA, interrupts, MMIO,
648: and PIOs [53].
649: I/O virtualization method
650: I/O virtualization method
651: between L0 & L1
652: between L1 & L2
653: Emulation
654: Emulation
655: Para-virtual
656: Emulation
657: Para-virtual
658: Para-virtual
659: Device assignment
660: Para-virtual
661: Device assignment
662: Device assignment
663: Table 1: I/O combinations for a nested guest
664: Device DMA in virtualized environments is compli-
665: cated, because guest drivers use guest physical addresses,
666: while memory access in the device is done with host
667: physical addresses. The common solution to the DMA
668: problem is an IOMMU [2, 11], a hardware component
669: which resides between the device and main memory. It
670: uses a translation table prepared by the hypervisor to
671: translate the guest physical addresses to host physical
672: addresses. IOMMUs currently available, however, only
673: support a single level of address translation. Again, we
674: need to compress two levels of translation tables onto the
675: one level available in hardware.
676: For modiﬁed guests this can be done using a paravir-
677: tual IOMMU: the code in L1 which sets a mapping on
678: the IOMMU from L2 to L1 addresses is replaced by a
679: hypercall to L0. L0 changes the L1 address in that map-
680: ping to the respective L0 address, and puts the resulting
681: mapping (from L2 to L0 addresses) in the IOMMU.
682: A better approach, one which can run unmodiﬁed
683: guests, is for L0 to emulate an IOMMU for L1 [5]. L1
684: believes that it is running on a machine with an IOMMU,
685: and sets up mappings from L2 to L1 addresses on it. L0
686: intercepts these mappings, remaps the L1 addresses to
687: L0 addresses, and builds the L2-to-L0 map on the real
688: IOMMU.
689: In current x86 architecture, interrupts always cause a
690: guest exit to L0, which proceeds to forward the interrupt
691: to L1. L1 will then inject it into L2. The EOI (end of
692: interrupt) will also cause a guest exit. In Section 4.1.1 we
693: discuss the slowdown caused by these interrupt-related
694: exits, and propose ways to avoid it.
695: Memory-mapped I/O (MMIO) and Port I/O (PIO) for
696: a nested guest work the same way they work for a single-
697: level guest, without incurring exits on the critical I/O
698: path [53].
699: 3.5
700: Micro Optimizations
701: There are two main places where a guest of a nested hy-
702: pervisor is slower than the same guest running on a bare-
703: metal hypervisor. First, the transitions between L1 and
704: L2 are slower than the transitions between L0 and L1.
705: Second, the exit handling code running in the L1 hyper-
706: visor is slower than the same code running in L0. In this
707: section we discuss these two issues, and propose opti-
708: mizations that improve performance. Since we assume
709: that both L1 and L2 are unmodiﬁed, these optimizations
710: require modifying L0 only. We evaluate these optimiza-
711: tions in the evaluation section.
712: 3.5.1
713: Optimizing transitions between L1 and L2
714: As explained in Section 3.2.3, transitions between L1
715: and L2 involve an exit to L0 and then an entry.
716: In
717: L0, most of the time is spent merging the VMCS’s. We
718: optimize this merging code to only copy data between
719: VMCS’s if the relevant values were modiﬁed. Keeping
720: track of which values were modiﬁed has an intrinsic cost,
721: so one must carefully balance full copying versus partial
722: copying and tracking. We observed empirically that for
723: common workloads and hypervisors, partial copying has
724: a lower overhead.
725: VMCS merging could be further optimized by copy-
726: ing multiple VMCS ﬁelds at once. However, according to
727: Intel’s speciﬁcations, reads or writes to the VMCS area
728: must be performed using vmread and vmwrite in-
729: structions, which operate on a single ﬁeld. We empiri-
730: cally noted that under certain conditions one could ac-
731: cess VMCS data directly without ill side-effects, bypass-
732: ing vmread and vmwrite and copying multiple ﬁelds
733: at once with large memory copies. However, this opti-
734: mization does not strictly adhere to the VMX speciﬁca-
735: tions, and thus might not work on processors other than
736: the ones we have tested.
737: In the evaluation section, we show that this opti-
```

## Ben-Yehuda et al. - 2010 - The Turtles Project Design and Implementation of Nested Virtualization.md
原始路径：/home/ubuntu/高级操作系统教程/references/Ben-Yehuda et al. - 2010 - The Turtles Project Design and Implementation of Nested Virtualization.md
行范围：789–892

```text
789: Our setup consisted of an IBM x3650 machine booted
790: with a single Intel Xeon 2.9GHz core and with 3GB of
791: memory. The host OS was Ubuntu 9.04 with a kernel
792: that is based on the KVM git tree version kvm-87, with
793: our nested virtualization support added. For both L1 and
794: L2 guests we used an Ubuntu Jaunty guest with a kernel
795: that is based on the KVM git tree, version kvm-87. L1
796: was conﬁgured with 2GB of memory and L2 was conﬁg-
797: ured with 1GB of memory. For the I/O experiments we
798: used a Broadcom NetXtreme 1Gb/s NIC connected via
799: crossover-cable to an e1000e NIC on another machine.
800: 4.1
801: Macro Workloads
802: kernbench is a general purpose compilation-type
803: benchmark that compiles the Linux kernel multiple
804: times. The compilation process is, by nature, CPU- and
805: memory-intensive, and it also generates disk I/O to load
806: the compiled ﬁles into the guest’s page cache.
807: SPECjbb is an industry-standard benchmark de-
808: signed to measure the server-side performance of Java
809: run-time environments. It emulates a three-tier system
810: and is primarily CPU-intensive.
811: We executed kernbench and SPECjbb in four se-
812: tups: host, single-level guest, nested guest, and nested
813: guest optimized with direct read and write (DRW) as de-
814: scribed in Section 3.5.2. The optimizations described
815: in Section 3.5.1 did not make a signiﬁcant difference to
816: these benchmarks, and are thus omitted from the results.
817: We used KVM as both L0 and L1 hypervisor with multi-
818: dimensional paging. The results are depicted in Table 2.
819: Kernbench
820: Host
821: Guest
822: Nested
823: NestedDRW
824: Run time
825: 324.3
826: 355
827: 406.3
828: 391.5
829: STD dev.
830: 1.5
831: 10
832: 6.7
833: 3.1
834: % overhead
835: vs. host
836: -
837: 9.5
838: 25.3
839: 20.7
840: % overhead
841: vs. guest
842: -
843: -
844: 14.5
845: 10.3
846: %CPU
847: 93
848: 97
849: 99
850: 99
851: SPECjbb
852: Host
853: Guest
854: Nested
855: NestedDRW
856: Score
857: 90493
858: 83599
859: 77065
860: 78347
861: STD dev.
862: 1104
863: 1230
864: 1716
865: 566
866: % degradati-
867: on vs. host
868: -
869: 7.6
870: 14.8
871: 13.4
872: % degradati-
873: on vs. guest
874: -
875: -
876: 7.8
877: 6.3
878: %CPU
879: 100
880: 100
881: 100
882: 100
883: Table 2: kernbench and SPECjbb results
884: We compared the impact of running the workloads in a
885: nested guest with running the same workload in a single-
886: level guest, i.e., the overhead added by the additional
887: level of virtualization. For kernbench, the overhead
888: of nested virtualization is 14.5%, while for SPECjbb the
889: score is degraded by 7.82%.
890: When we discount the
891: Intel-speciﬁc vmread and vmwrite overhead in L1,
892: the overhead is 10.3% and 6.3% respectively.
```

## Ben-Yehuda et al. - 2010 - The Turtles Project Design and Implementation of Nested Virtualization.md
原始路径：/home/ubuntu/高级操作系统教程/references/Ben-Yehuda et al. - 2010 - The Turtles Project Design and Implementation of Nested Virtualization.md
行范围：1186–1200

```text
1186: 4.2
1187: VMware Server as a Guest Hypervisor
1188: We also evaluated VMware as the L1 hypervisor to ana-
1189: lyze how a different guest hypervisor affects nested vir-
1190: tualization performance.
1191: We used the hosted version,
1192: VMWare Server v2.0.1, build 156745 x86-64, on top of
1193: Ubuntu based on kernel 2.6.28-11. We intentionally did
1194: not install VMware tools for the L2 guest, thereby in-
1195: creasing nested virtualization overhead. Due to similar
1196: results obtained for VMware and KVM as the nested hy-
1197: pervisor, we show only kernbench and SPECjbb re-
1198: sults below.
1199: Benchmark
1200: % overhead vs. single-level guest
```
