# 原始证据摘录：hardware

这些是原文/源码，不是正文草稿。行号仅用于追溯。勿把页面断行当成语义断句。

## armv8_arm_v8.6.md
原始路径：/home/ubuntu/aarch64/manuals/armv8_arm_v8.6.md
行范围：154270–154322

```text
154270: D1.5
154271: Virtualization
154272: The support for virtualization described in this section applies only to an implementation that includes EL2.
154273: When enabled in the current Security state, EL2 provides a set of features that support virtualizing an Armv8-A 
154274: implementation. The basic model of a virtualized system involves:
154275: •
154276: A hypervisor, running in EL2, that is responsible for switching between virtual machines. A virtual machine 
154277: comprises EL1 and EL0.
154278: •
154279: A number of Guest operating systems. A Guest OS runs on a virtual machine in EL1.
154280: •
154281: For each Guest operating system, applications, that run on the virtual machine of that Guest OS, usually in 
154282: EL0.
154283: Note
154284:  In some systems, a Guest OS is unaware that it is running on a virtual machine, and is unaware of any other Guest 
154285: OS. In other systems, a hypervisor makes the Guest OS aware of these facts. The Armv8-A architecture supports 
154286: both of these models.
154287: The hypervisor assigns a virtual machine identifier (VMID) to each virtual machine.
154288: EL2 supports Guest OS management and provides controls to:
154289: •
154290: Provide virtual values for the contents of a small number of identification registers. A read of one of these 
154291: registers by a Guest OS or the applications for a Guest OS returns the virtual value.
154292: •
154293: Trap various operations, including memory management operations and accesses to many other registers. A 
154294: trapped operation generates an exception that is taken to EL2. See Configurable instruction enables and 
154295: disables, and trap controls on page D1-2373.
154296: •
154297: Route interrupts to the appropriate one of:
154298: —
154299: The current Guest OS.
154300: —
154301: A Guest OS that is not currently running.
154302: —
154303: The hypervisor.
154304: Armv8.1 introduces the Virtualization Host Extensions (VHE) that provide enhanced support for Type 2 
154305: hypervisors. For more information, see Virtualization Host Extensions on page D5-2638.
154306: In an implementation that includes EL2:
154307: •
154308: The implementation provides an independent translation regime for memory accesses from EL2, the EL2 
154309: translation regime. An implementation that includes ARMv8.1-VHE also supports an alternative EL2&0 
154310: translation regime.
154311: Note
154312:  
154313: An implementation that includes ARMv8.1-VHE can be configured so that the EL2&0 translation regime is 
154314: used both for accesses from EL2 and for accesses from EL0.
154315: •
154316: For the EL1&0 translation regime, address translation occurs in two stages:
154317: —
154318: Stage 1 maps the virtual address (VA) to an intermediate physical address (IPA). This is managed at 
154319: EL1, usually by a Guest OS. The Guest OS believes that the IPA is the physical address (PA).
154320: —
154321: Stage 2 maps the IPA to the PA. This is managed at EL2. The Guest OS might be completely unaware 
154322: of this stage.
```

## armv8_arm_v8.6.md
原始路径：/home/ubuntu/aarch64/manuals/armv8_arm_v8.6.md
行范围：155402–155436

```text
155402: On taking an exception to AArch64 state:
155403: •
155404: The PE state is saved in the SPSR_ELx at the target Exception level. See Saved Program Status Registers 
155405: (SPSRs) on page D1-2324.
155406: •
155407: The preferred return address is saved in the ELR_ELx at the target Exception level. See Exception Link 
155408: Registers (ELRs) on page D1-2328.
155409: •
155410: All of PSTATE.{D, A, I, F} are set to 1. See Process state, PSTATE on page D1-2330.
155411: •
155412: PSTATE.SSBS is set to the value of SCTLR_ELx.DSSBS.
155413: •
155414: If ARMv8.2-UAO is implemented, PSTATE.UAO is set to 0. See Process state, PSTATE on page D1-2330.
155415: •
155416: If the exception is a synchronous exception or an SError interrupt, information characterizing the reason for 
155417: the exception is saved in the ESR_ELx at the target Exception level. See Use of the ESR_EL1, ESR_EL2, and 
155418: ESR_EL3 on page D1-2342.
155419: •
155420: If ARMv8.5-MemTag is implemented: 
155421: —
155422: PSTATE.TCO is set to 1. See Process state, PSTATE on page D1-2330.
155423: —
155424: A synchronous exception due to a Tag Check Fault is reported to as a Data Abort with a Data Fault 
155425: Status Code of Synchronous Tag Check Fault and the faulting virtual address is reported in FAR_ELx.
155426: For more information see PE handling of Tag Check Fault on page D6-2696.
155427: •
155428: If ARMv8.5-BTI is implemented, on taking an asynchronous exception from AArch64 to AArch64, 
155429: PSTATE.BTYPE is copied to SPSR_ELx.BTYPE and then set to 0.
155430: •
155431: If ARMv8.5-BTI is implemented, on taking certain types of synchronous exception from AArch64 to 
155432: AArch64, PSTATE.BTYPE is copied to SPSR_ELx.BTYPE and then set to 0. These types of synchronous 
155433: exceptions are:
155434: —
155435: Software Step exception.
155436: —
```

## armv8_arm_v8.6.md
原始路径：/home/ubuntu/aarch64/manuals/armv8_arm_v8.6.md
行范围：169645–169685

```text
169645: Non-secure EL1&0 stage 2
169646: Non-secure EL2
169647: SCTLR_EL2.EE
169648: HCR_EL2.VM
169649: VTCR_EL2
169650: VTTBR_EL2
169651: Non-secure EL1&0 stage 1
169652: Non-secure EL1
169653: SCTLR_EL1.{EE, M}
169654: TCR_EL1
169655: TTBR0_EL1
169656: TTBR1_EL1
169657: 
169658: <!-- page 2547 -->
169659: 
169660: The AArch64 Virtual Memory System Architecture 
169661: D5.2 The VMSAv8-64 address translation system
169662: ARM DDI 0487F.b
169663: Copyright © 2013-2020 Arm Limited or its affiliates. All rights reserved.
169664: D5-2547
169665: ID040120
169666: Non-Confidential
169667: •
169668: If ARMv8.5-MemTag is implemented and enabled, Chapter D6 Armv8.5 Memory Tagging Extension 
169669: provides further controls for the checking of Tagged and Untagged addresses.
169670: System registers relevant to MMU operation
169671: In AArch64 state, System registers have a suffix, that indicates the lowest Exception level from which they can be 
169672: accessed. In some general descriptions of MMU control and address translation, this chapter uses a Common 
169673: abbreviation for each of the System registers that affects MMU operation, as Table D5-3 shows. The common 
169674: abbreviation is used when describing features that apply to multiple translation regimes or stages.
169675: Note
169676:  The only translation regime that supports a stage 2 translation is the EL1&0 translation regime, when EL2 is 
169677: enabled.
169678: Address size configuration
169679: The following subsubsections specify the configuration of the PA size and of the input and output address sizes for 
169680: each of the stages of address translation:
169681: •
169682: Physical address size on page D5-2548.
169683: •
169684: Output address size on page D5-2548.
169685: •
```

## arm.c
原始路径：/home/ubuntu/linux-source-7.0.0/arch/arm64/kvm/arm.c
行范围：1191–1220

```text
1191: /*
1192:  * Actually run the vCPU, entering an RCU extended quiescent state (EQS) while
1193:  * the vCPU is running.
1194:  *
1195:  * This must be noinstr as instrumentation may make use of RCU, and this is not
1196:  * safe during the EQS.
1197:  */
1198: static int noinstr kvm_arm_vcpu_enter_exit(struct kvm_vcpu *vcpu)
1199: {
1200: 	int ret;
1201: 
1202: 	guest_state_enter_irqoff();
1203: 	ret = kvm_call_hyp_ret(__kvm_vcpu_run, vcpu);
1204: 	guest_state_exit_irqoff();
1205: 
1206: 	return ret;
1207: }
1208: 
1209: /**
1210:  * kvm_arch_vcpu_ioctl_run - the main VCPU run function to execute guest code
1211:  * @vcpu:	The VCPU pointer
1212:  *
1213:  * This function is called through the VCPU_RUN ioctl called from user space. It
1214:  * will execute VM code in a loop until the time slice for the process is used
1215:  * or some emulation is needed from user space in which case the function will
1216:  * return with return value 0 and with the kvm_run structure filled in with the
1217:  * required data for the requested emulation.
1218:  */
1219: int kvm_arch_vcpu_ioctl_run(struct kvm_vcpu *vcpu)
1220: {
```

## entry.S
原始路径：/home/ubuntu/linux-source-7.0.0/arch/arm64/kvm/hyp/entry.S
行范围：70–88

```text
70: 	// Restore the guest's sp_el0
71: 	restore_sp_el0 x29, x0
72: 
73: 	// Restore guest regs x0-x17
74: 	ldp	x0, x1,   [x29, #CPU_XREG_OFFSET(0)]
75: 	ldp	x2, x3,   [x29, #CPU_XREG_OFFSET(2)]
76: 	ldp	x4, x5,   [x29, #CPU_XREG_OFFSET(4)]
77: 	ldp	x6, x7,   [x29, #CPU_XREG_OFFSET(6)]
78: 	ldp	x8, x9,   [x29, #CPU_XREG_OFFSET(8)]
79: 	ldp	x10, x11, [x29, #CPU_XREG_OFFSET(10)]
80: 	ldp	x12, x13, [x29, #CPU_XREG_OFFSET(12)]
81: 	ldp	x14, x15, [x29, #CPU_XREG_OFFSET(14)]
82: 	ldp	x16, x17, [x29, #CPU_XREG_OFFSET(16)]
83: 
84: 	// Restore guest regs x18-x29, lr
85: 	restore_callee_saved_regs x29
86: 
87: 	// Do not touch any register after this!
88: 	eret
```

## entry.S
原始路径：/home/ubuntu/linux-source-7.0.0/arch/arm64/kvm/hyp/entry.S
行范围：121–151

```text
121: SYM_INNER_LABEL(__guest_exit, SYM_L_GLOBAL)
122: 	// x0: return code
123: 	// x1: vcpu
124: 	// x2-x29,lr: vcpu regs
125: 	// vcpu x0-x1 on the stack
126: 
127: 	add	x1, x1, #VCPU_CONTEXT
128: 
129: 	ALTERNATIVE(nop, SET_PSTATE_PAN(1), ARM64_HAS_PAN)
130: 
131: 	// Store the guest regs x2 and x3
132: 	stp	x2, x3,   [x1, #CPU_XREG_OFFSET(2)]
133: 
134: 	// Retrieve the guest regs x0-x1 from the stack
135: 	ldp	x2, x3, [sp], #16	// x0, x1
136: 
137: 	// Store the guest regs x0-x1 and x4-x17
138: 	stp	x2, x3,   [x1, #CPU_XREG_OFFSET(0)]
139: 	stp	x4, x5,   [x1, #CPU_XREG_OFFSET(4)]
140: 	stp	x6, x7,   [x1, #CPU_XREG_OFFSET(6)]
141: 	stp	x8, x9,   [x1, #CPU_XREG_OFFSET(8)]
142: 	stp	x10, x11, [x1, #CPU_XREG_OFFSET(10)]
143: 	stp	x12, x13, [x1, #CPU_XREG_OFFSET(12)]
144: 	stp	x14, x15, [x1, #CPU_XREG_OFFSET(14)]
145: 	stp	x16, x17, [x1, #CPU_XREG_OFFSET(16)]
146: 
147: 	// Store the guest regs x18-x29, lr
148: 	save_callee_saved_regs x1
149: 
150: 	// Store the guest's sp_el0
151: 	save_sp_el0	x1, x2
```

## mmu.c
原始路径：/home/ubuntu/linux-source-7.0.0/arch/arm64/kvm/mmu.c
行范围：2153–2226

```text
2153: 	gfn = ipa >> PAGE_SHIFT;
2154: 	memslot = gfn_to_memslot(vcpu->kvm, gfn);
2155: 	hva = gfn_to_hva_memslot_prot(memslot, gfn, &writable);
2156: 	write_fault = kvm_is_write_fault(vcpu);
2157: 	if (kvm_is_error_hva(hva) || (write_fault && !writable)) {
2158: 		/*
2159: 		 * The guest has put either its instructions or its page-tables
2160: 		 * somewhere it shouldn't have. Userspace won't be able to do
2161: 		 * anything about this (there's no syndrome for a start), so
2162: 		 * re-inject the abort back into the guest.
2163: 		 */
2164: 		if (is_iabt) {
2165: 			ret = -ENOEXEC;
2166: 			goto out;
2167: 		}
2168: 
2169: 		if (kvm_vcpu_abt_iss1tw(vcpu)) {
2170: 			ret = kvm_inject_sea_dabt(vcpu, kvm_vcpu_get_hfar(vcpu));
2171: 			goto out_unlock;
2172: 		}
2173: 
2174: 		/*
2175: 		 * Check for a cache maintenance operation. Since we
2176: 		 * ended-up here, we know it is outside of any memory
2177: 		 * slot. But we can't find out if that is for a device,
2178: 		 * or if the guest is just being stupid. The only thing
2179: 		 * we know for sure is that this range cannot be cached.
2180: 		 *
2181: 		 * So let's assume that the guest is just being
2182: 		 * cautious, and skip the instruction.
2183: 		 */
2184: 		if (kvm_is_error_hva(hva) && kvm_vcpu_dabt_is_cm(vcpu)) {
2185: 			kvm_incr_pc(vcpu);
2186: 			ret = 1;
2187: 			goto out_unlock;
2188: 		}
2189: 
2190: 		/*
2191: 		 * The IPA is reported as [MAX:12], so we need to
2192: 		 * complement it with the bottom 12 bits from the
2193: 		 * faulting VA. This is always 12 bits, irrespective
2194: 		 * of the page size.
2195: 		 */
2196: 		ipa |= FAR_TO_FIPA_OFFSET(kvm_vcpu_get_hfar(vcpu));
2197: 		ret = io_mem_abort(vcpu, ipa);
2198: 		goto out_unlock;
2199: 	}
2200: 
2201: 	/* Userspace should not be able to register out-of-bounds IPAs */
2202: 	VM_BUG_ON(ipa >= kvm_phys_size(vcpu->arch.hw_mmu));
2203: 
2204: 	if (esr_fsc_is_access_flag_fault(esr)) {
2205: 		handle_access_fault(vcpu, fault_ipa);
2206: 		ret = 1;
2207: 		goto out_unlock;
2208: 	}
2209: 
2210: 	VM_WARN_ON_ONCE(kvm_vcpu_trap_is_permission_fault(vcpu) &&
2211: 			!write_fault && !kvm_vcpu_trap_is_exec_fault(vcpu));
2212: 
2213: 	if (kvm_slot_has_gmem(memslot))
2214: 		ret = gmem_abort(vcpu, fault_ipa, nested, memslot,
2215: 				 esr_fsc_is_permission_fault(esr));
2216: 	else
2217: 		ret = user_mem_abort(vcpu, fault_ipa, nested, memslot, hva,
2218: 				     esr_fsc_is_permission_fault(esr));
2219: 	if (ret == 0)
2220: 		ret = 1;
2221: out:
2222: 	if (ret == -ENOEXEC)
2223: 		ret = kvm_inject_sea_iabt(vcpu, kvm_vcpu_get_hfar(vcpu));
2224: out_unlock:
2225: 	srcu_read_unlock(&vcpu->kvm->srcu, idx);
2226: 	return ret;
```

## mmio.c
原始路径：/home/ubuntu/linux-source-7.0.0/arch/arm64/kvm/mmio.c
行范围：225–259

```text
225: 
226: 		trace_kvm_mmio(KVM_TRACE_MMIO_WRITE, len, fault_ipa, &data);
227: 		kvm_mmio_write_buf(data_buf, len, data);
228: 
229: 		ret = kvm_io_bus_write(vcpu, KVM_MMIO_BUS, fault_ipa, len,
230: 				       data_buf);
231: 	} else {
232: 		trace_kvm_mmio(KVM_TRACE_MMIO_READ_UNSATISFIED, len,
233: 			       fault_ipa, NULL);
234: 
235: 		ret = kvm_io_bus_read(vcpu, KVM_MMIO_BUS, fault_ipa, len,
236: 				      data_buf);
237: 	}
238: 
239: 	/* Now prepare kvm_run for the potential return to userland. */
240: 	run->mmio.is_write	= is_write;
241: 	run->mmio.phys_addr	= fault_ipa;
242: 	run->mmio.len		= len;
243: 	vcpu->mmio_needed	= 1;
244: 
245: 	if (!ret) {
246: 		/* We handled the access successfully in the kernel. */
247: 		if (!is_write)
248: 			memcpy(run->mmio.data, data_buf, len);
249: 		vcpu->stat.mmio_exit_kernel++;
250: 		kvm_handle_mmio_return(vcpu);
251: 		return 1;
252: 	}
253: 
254: 	if (is_write)
255: 		memcpy(run->mmio.data, data_buf, len);
256: 	vcpu->stat.mmio_exit_user++;
257: 	run->exit_reason	= KVM_EXIT_MMIO;
258: 	return 0;
259: }
```

## ARM_IHI0069D_GIC_Architecture_Spec_v3.0_v4.0.md
原始路径：/home/ubuntu/aarch64/manuals/ARM_IHI0069D_GIC_Architecture_Spec_v3.0_v4.0.md
行范围：4204–4286

```text
4204: 5.1
4205: About GIC support for virtualization
4206: An operating system that is executing at EL1 under the control of a hypervisor executing at EL2 is sometimes 
4207: referred as a virtual machine (VM). A VM can support multiprocessing, which means that multiple virtual PEs 
4208: (vPEs), that are scheduled by the hypervisor are executing on one or more physical PEs. When a vPE is executing 
4209: on a PE, that vPE of the VM is referred to as being scheduled on the physical PE.
4210: In ARMv8, when EL2 is implemented and enabled, the  CPU interface provides mechanisms to minimize the 
4211: hypervisor overhead of routing interrupts to a VM. For more information about vPEs, see Operation overview on 
4212: page 5-79.
4213: For more information about EL2 and virtual interrupts, see ARM® Architecture Reference Manual, ARMv8, for 
4214: ARMv8-A architecture profile.
4215: In GICv4, for the directly injected virtual LPIs , the scheduled vPE is determined by GICR_VPENDBASER. For 
4216: more information, see Doorbell interrupts on page 5-87
4217: Note
4218:  The GIC does not provide additional mechanisms for the virtualization of the GICD_*, GICR_*, and GITS_* 
4219: registers. To virtualize VM accesses to these registers, the hypervisor must set stage 2 data aborts to those memory 
4220: locations so that the hypervisor can emulate these effects. For more information about stage 2 data aborts, see ARM® 
4221: Architecture Reference Manual, ARMv8, for ARMv8-A architecture profile.
4222: When a GIC provides support for virtualization, the VM operates in an environment that has the following features:
4223: •
4224: The vPE can be configured to receive virtual Group 0 interrupts.
4225: •
4226: The vPE can be configured to receive virtual Group 1 interrupts.
4227: •
4228: Virtual Group 0 interrupts are signaled using the virtual FIQ signal to Non-secure EL1.
4229: •
4230: Virtual Group 1 interrupts are signaled using the virtual IRQ signal to Non-secure EL1.
4231: •
4232: Virtual interrupts can be handled by the vPE as if they were physical interrupts.
4233: Note
4234:  This applies when affinity routing and System register access are enabled. For information about support for virtual 
4235: interrupts in legacy operation, see Support for legacy operation of VMs on page 10-715.
4236: EL2 controls the generation of virtual interrupts for a VM. This allows software executing at EL2 to:
4237: •
4238: Generate virtual Group 0 and Group 1 interrupts for the vPE. 
4239: •
4240: Save and restore the interrupt state of the vPE.
4241: •
4242: Control the prioritization of the virtual interrupts.
4243: •
4244: Change the vPE that is scheduled.
4245: GICv4 introduces the ability to present virtual LPIs from an ITS directly to a vPE, without hypervisor intervention.
4246: Handling virtual interrupts in legacy operation requires a GICV_* memory-mapped interface. See Support for 
4247: legacy operation of VMs on page 10-715 for more information.
4248: 
4249: <!-- page 79 -->
4250: 
4251: 5 Virtual Interrupt Handling and Prioritization 
4252: 5.2 Operation overview
4253: ARM IHI 0069D
4254: Copyright © 2008, 2011, 2015-2017 ARM Limited or its affiliates. All rights reserved.
4255: 5-79
4256: ID072617
4257: Non-Confidential
4258: 5.2
4259: Operation overview
4260: GICv3 supports the ARMv8-A virtualization functionality. A hypervisor executing at EL2 uses the ICH_* System 
4261: register interface to configure and control a virtual PE (vPE) executing at Non-secure EL1. For information about 
4262: the VM control interface, see Configuration and control of VMs on page 5-83. A vPE uses the ICC_*_EL1 System 
4263: register interface to communicate with the GIC. The configuration of HCR_EL2.{IMO, FMO} determines whether 
4264: the virtual or the physical interface registers are accessed. 
4265: Note
4266:  This chapter describes the handling of virtual interrupts in the context of the AArch64 execution state with System 
4267: register access enabled. The individual AArch64 System register descriptions that are cross-referenced in this 
4268: chapter contain a reference to the AArch32 System register that provides the same functionality. For information 
4269: about VMs in legacy operation, see Support for legacy operation of VMs on page 10-715.
4270: Software executing at EL3 or EL2 configures the PE to route physical interrupts to EL2. The interrupt can be:
4271: •
4272: An interrupt targeting a vPE. The hypervisor sets the corresponding virtual INTID to the pending state on the 
4273: target vPE and includes the information about the associated physical INTID. When the vPE is not scheduled 
4274: on a PE, the hypervisor might choose to reschedule the vPE. Otherwise the interrupt is left pending on the 
4275: vPE for scheduling by the hypervisor at a later time. 
4276: •
4277: An interrupt targeting the hypervisor. This interrupt might:
4278: —
4279: Have been generated by the system.
4280: —
4281: Be a maintenance interrupt associated with a scheduled VM. See Maintenance interrupts on page 5-85 
4282: for more details.
4283: —
4284: In GICv4, be a doorbell interrupt from an ITS. In GICv4, a virtual interrupt can be presented to a vPE 
4285: without hypervisor involvement. A doorbell interrupt must be generated when a virtual interrupt is 
4286: made pending for a vPE but the vPE is not scheduled on a PE. 
```

## ARM_IHI0069D_GIC_Architecture_Spec_v3.0_v4.0.md
原始路径：/home/ubuntu/aarch64/manuals/ARM_IHI0069D_GIC_Architecture_Spec_v3.0_v4.0.md
行范围：4380–4432

```text
4380: •
4381: Accesses to ICC_PMR_EL1 access ICV_PMR_EL1.
4382: A virtual write to ICC_SGI0R_EL1, ICC_SGI1R_EL1, or ICC_ASGI1R_EL1 traps to EL2.
4383: Software executing at EL2 can access some ICV_* register state using ICH_VMCR_EL2 and ICH_VTR_EL2 as 
4384: follows:
4385: •
4386: ICV_PMR_EL1.Priority aliases ICH_VMCR_EL2.VPMR.
4387: •
4388: ICV_BPR0_EL1.BinaryPoint aliases ICH_VMCR_EL2.VBPR0.
4389: •
4390: ICV_BPR1_EL1.BinaryPoint aliases ICH_VMCR_EL2.VBPR1.
4391: •
4392: ICV_CTLR_EL1.EOImode aliases ICH_VMCR_EL2.VEOIM.
4393: •
4394: ICV_CTLR_EL1.CBPR aliases ICH_VMCR_EL2.VCBPR.
4395: •
4396: ICV_IGRPEN0_EL1aliases ICH_VMCR_EL2.VENG0.
4397: •
4398: ICV_IGRPEN1_EL1. aliases ICH_VMCR_EL2.VENG1.
4399: •
4400: ICV_CTLR_EL1.PRIbits aliases ICH_VTR_EL2.PRIbits.
4401: 
4402: <!-- page 81 -->
4403: 
4404: 5 Virtual Interrupt Handling and Prioritization 
4405: 5.2 Operation overview
4406: ARM IHI 0069D
4407: Copyright © 2008, 2011, 2015-2017 ARM Limited or its affiliates. All rights reserved.
4408: 5-81
4409: ID072617
4410: Non-Confidential
4411: •
4412: ICV_CTLR_EL1.IDbits aliases ICH_VTR_EL2.IDbits.
4413: •
4414: ICV_CTLR_EL1.SEIS aliases ICH_VTR_EL2.SEIS.
4415: •
4416: ICV_CTLR_EL1.A3V aliases ICH_VTR_EL2.A3V.
4417: 5.2.1
4418: Usage model for the List registers
4419: A fundamental function of an interrupt controller is to develop list of pending interrupts in priority order for each 
4420: PE, and then to present the highest priority interrupt to the PE if the interrupt is of sufficient priority. For physical 
4421: interrupts, this task is performed entirely in hardware by the GIC. However, in order to reduce the cost in hardware, 
4422: the GIC handles virtual interrupts using both hardware and software.
4423: For each physical interrupt received that is targeting a vPE, the hypervisor adds that interrupt to a prioritized list of 
4424: pending virtual interrupts that is presented to the vPE. The GIC hardware also provides a set of List registers, 
4425: ICH_LR<n>_EL2, that holds an IMPLEMENTATION DEFINED number of the top entries in the prioritized list for the 
4426: currently running vPE. Typically, there are at most only a few pending virtual interrupts for that vPE. The interrupts 
4427: in the List register are then handled by the vPE in hardware, providing the same behavior for the VM as is seen by 
4428: a non-virtualized operating system handling physical interrupts.
4429: However, the total number of interrupts that are pending, active and pending, or active, can exceed the number of 
4430: List registers available. In this case, the hypervisor can save one or more entries to memory, and later restore them 
4431: to the List registers based on their priority. In this way, the List registers act as a cache for the list of pending, active, 
4432: or active and pending interrupts that is controlled by software, for a vPE.
```

## ARM_IHI0069D_GIC_Architecture_Spec_v3.0_v4.0.md
原始路径：/home/ubuntu/aarch64/manuals/ARM_IHI0069D_GIC_Architecture_Spec_v3.0_v4.0.md
行范围：4648–4776

```text
4648: 5.3.3
4649: Maintenance interrupts
4650: Maintenance interrupts can signal key events in the operation of a GIC that implements virtualization. These events 
4651: are processed by the hypervisor.
4652: Note
4653:  •
4654: Maintenance interrupts are generated only when the global enable bit for the virtual CPU interface, 
4655: ICH_HCR_EL2.En, is set to 1.
4656: •
4657: ARM strongly recommends that maintenance interrupts are configured to use INTID 25. For more 
4658: information, see Server Base System Architecture (SBSA).
4659: Maintenance interrupts are level-sensitive interrupts. Configuration bits in ICH_HCR_EL2 can be set to 1 to enable 
4660: the generation of maintenance interrupts when:
4661: •
4662: Group 0 virtual interrupts are enabled.
4663: •
4664: Group 1 virtual interrupts are enabled.
4665: •
4666: Group 0 virtual interrupts are disabled.
4667: •
4668: Group 1 virtual interrupts are disabled.
4669: •
4670: There are no pending interrupts in the List registers.
4671: •
4672: At least one EOI request occurs with no valid List register entry for the corresponding interrupt.
4673: •
4674: There are no valid entries, or there is only one valid entry, in the List registers. This is an underflow condition.
4675: •
4676: At least one List register entry has received an EOI request.
4677: See ICH_MISR_EL2, Interrupt Controller Maintenance Interrupt State Register on page 8-300 for more 
4678: information about the control and status reporting of maintenance interrupts.
4679: 
4680: <!-- page 86 -->
4681: 
4682: 5 Virtual Interrupt Handling and Prioritization 
4683: 5.4 Virtual LPI support
4684: 5-86
4685: Copyright © 2008, 2011, 2015-2017 ARM Limited or its affiliates. All rights reserved.
4686: ARM IHI 0069D
4687: Non-Confidential
4688: ID072617
4689: 5.4
4690: Virtual LPI support
4691: In GICv3 LPIs can be presented to a virtualized system by the hypervisor, which must be using the System registers. 
4692: A virtual LPI is generated when the hypervisor writes a vINTID corresponding to the LPI range, that is a vINTID 
4693: that is greater than 8191, to a List register. Because an LPI does not have an active state, it is not possible to associate 
4694: a virtual LPI with a physical interrupt.
4695: GICv4 provides support for the direct injection of virtual LPIs, vLPIs, in the LPI INTID range. With the direct 
4696: injection of vLPIs, the GICR_* registers use structures in memory for each vPE to hold LPI configuration and 
4697: pending information for vLPIs in the same way that they use structures in memory to hold LPI configuration and 
4698: pending information for physical LPIs. However, the virtual structures are different from the physical structures, 
4699: with the vLPI tables for the current vPE scheduled on a PE by GICR_VPENDBASER and GICR_VPROPBASER 
4700: in the Redistributor associated with that PE, For more information about the physical LPI tables, see LPI 
4701: Configuration tables on page 6-95 and LPI Pending tables on page 6-97.
4702: The Redistributor associated with the PE on which the vPE is scheduled determines the highest priority pending 
4703: vLPI, and forwards this to the virtual CPU interface of the vPE. This vLPI and the interrupts in the List register are 
4704: then prioritized together to determine the highest priority pending virtual interrupt for the vPE. 
4705: For information about virtual LPIs and the virtual CPU tables, see The vPE table on page 6-104.
4706: 5.4.1
4707: Direct injection of virtual interrupts
4708: The ITS maps an EventID and a DeviceID to an INTID associated with a PE, see The ITS on page 6-99 for more 
4709: information. GICv4 introduces the ability to generate a virtual LPI without involving the hypervisor. In this case an 
4710: ITS maps the EventID for the interrupt translation using the following mechanism:
4711: •
4712: The ITS interruption translation table entry for a vLPI is configured with:
4713: —
4714: A control flag that indicates the EventID is associated with a virtual LPI.
4715: —
4716: A vPEID to index into the ITS vPE table. For more information about vPEID and the vPE table, see 
4717: The vPE table on page 6-104. The vPE table provides:
4718: 1.
4719: The base address of the GICR_* registers in the format defined by GITS_TYPER.PTA.
4720: 2.
4721: The base address of the virtual LPI Pending table associated with the target VM.
4722: —
4723: A virtual INTID, vINTID, that indicates which vLPI becomes pending.
4724: —
4725: A physical INTID, pINTID, that can be used as a doorbell interrupt to the hypervisor if the vPE is not 
4726: scheduled on a PE. The value 1023 is used where a doorbell interrupt is not required, otherwise an 
4727: INTID in the physical LPI range must be provided. 
4728: For more information about:
4729: •
4730: Physical LPIs, see LPIs on page 6-92.
4731: •
4732: The ITS and format of an Interrupt translation table (ITT), see The ITS on page 6-99.
4733: •
4734: The commands used to control the handling of virtual LPIs associated with an ITS, see Table 6-6 on 
4735: page 6-108 and the following commands:
4736: —
4737: VINVALL on page 6-125.
4738: —
4739: VMAPI on page 6-126.
4740: —
4741: VMAPP on page 6-127.
4742: —
4743: VMAPTI on page 6-129.
4744: —
4745: VMOVI on page 6-130.
4746: —
4747: VMOVP on page 6-132.
4748: —
4749: VSYNC on page 6-134.
4750: The GIC hardware determines whether the vPE is scheduled on a PE when:
4751: •
4752: GICR_VPENDBASER.Valid == 1.
4753: •
4754: GICR_VPENDBASER.Physical_Address holds the same value as defined in the VPT_addr field in the 
4755: VMAPP command for the vPE that is the target of the vLPI.
4756: 
4757: <!-- page 87 -->
4758: 
4759: 5 Virtual Interrupt Handling and Prioritization 
4760: 5.4 Virtual LPI support
4761: ARM IHI 0069D
4762: Copyright © 2008, 2011, 2015-2017 ARM Limited or its affiliates. All rights reserved.
4763: 5-87
4764: ID072617
4765: Non-Confidential
4766: If, at the time that a vPE is descheduled from a PE, there are one or more vLPIs pending for the PE, 
4767: GICR_VPENDBASER.PendingLast is set to 1. This can be used by the hypervisor to make scheduling decisions. 
4768: 5.4.2
4769: Doorbell interrupts
4770: When an interrupt that targets a vPE becomes pending, it might target a vPE that is not currently scheduled on a PE. 
4771: Where those interrupts are presented as physical interrupts, the hypervisor can schedule in the vPE as a result of that 
4772: interrupt. In this case the hypervisor can make the scheduling decisions for the vPE based on the full set of pending 
4773: virtual interrupts for the vPE.
4774: The equivalent capability is provided in the case of direct injections of vLPIs by the provision of doorbell LPIs. 
4775: For a vLPI, the ITS can configure a physical LPI that is sent to a PE when the vLPI becomes pending and the vPE 
4776: is not scheduled on that PE. This physical LPI is a Doorbell LPI.
```

## vgic-v3.c
原始路径：/home/ubuntu/linux-source-7.0.0/arch/arm64/kvm/vgic/vgic-v3.c
行范围：366–397

```text
366: void vgic_v3_populate_lr(struct kvm_vcpu *vcpu, struct vgic_irq *irq, int lr)
367: {
368: 	u32 model = vcpu->kvm->arch.vgic.vgic_model;
369: 	u64 val = vgic_v3_compute_lr(vcpu, irq);
370: 
371: 	vcpu->arch.vgic_cpu.vgic_v3.vgic_lr[lr] = val;
372: 
373: 	if (val & ICH_LR_PENDING_BIT) {
374: 		if (irq->config == VGIC_CONFIG_EDGE)
375: 			irq->pending_latch = false;
376: 
377: 		if (vgic_irq_is_sgi(irq->intid) &&
378: 		    model == KVM_DEV_TYPE_ARM_VGIC_V2) {
379: 			u32 src = ffs(irq->source);
380: 
381: 			irq->source &= ~BIT(src - 1);
382: 			if (irq->source)
383: 				irq->pending_latch = true;
384: 		}
385: 	}
386: 
387: 	/*
388: 	 * Level-triggered mapped IRQs are special because we only observe
389: 	 * rising edges as input to the VGIC.  We therefore lower the line
390: 	 * level here, so that we can take new virtual IRQs.  See
391: 	 * vgic_v3_fold_lr_state for more info.
392: 	 */
393: 	if (vgic_irq_is_mapped_level(irq) && (val & ICH_LR_PENDING_BIT))
394: 		irq->line_level = false;
395: 
396: 	irq->on_lr = true;
397: }
```

## vgic-v4.c
原始路径：/home/ubuntu/linux-source-7.0.0/arch/arm64/kvm/vgic/vgic-v4.c
行范围：84–105

```text
84: static irqreturn_t vgic_v4_doorbell_handler(int irq, void *info)
85: {
86: 	struct kvm_vcpu *vcpu = info;
87: 
88: 	/* We got the message, no need to fire again */
89: 	if (!kvm_vgic_global_state.has_gicv4_1 &&
90: 	    !irqd_irq_disabled(&irq_to_desc(irq)->irq_data))
91: 		disable_irq_nosync(irq);
92: 
93: 	/*
94: 	 * The v4.1 doorbell can fire concurrently with the vPE being
95: 	 * made non-resident. Ensure we only update pending_last
96: 	 * *after* the non-residency sequence has completed.
97: 	 */
98: 	raw_spin_lock(&vcpu->arch.vgic_cpu.vgic_v3.its_vpe.vpe_lock);
99: 	vcpu->arch.vgic_cpu.vgic_v3.its_vpe.pending_last = true;
100: 	raw_spin_unlock(&vcpu->arch.vgic_cpu.vgic_v3.its_vpe.vpe_lock);
101: 
102: 	kvm_make_request(KVM_REQ_IRQ_PENDING, vcpu);
103: 	kvm_vcpu_kick(vcpu);
104: 
105: 	return IRQ_HANDLED;
```

## smmuv3.txt
原始路径：/home/ubuntu/.hermes/cache/scratch/virtualization-outline/smmuv3.txt
行范围：1142–1239

```text
1142: 
1143: The registers indicate the base addresses of the structures and queues, provide feature detection and
1144: identification registers and a global control register to enable queue processing and translation of traffic. When
1145: security is supported, an additional register set exists to allow Secure software to maintain Secure device
1146: structures, issue commands on a second Secure Command queue and read Secure events from a Secure Event
1147: queue.
1148: 
1149: 
1150: In virtualization scenarios allowing stage 1 translation, a guest OS is presented with exactly the same
1151: programming interface and therefore believes it is in control of a real SMMU (albeit stage 1-only) with the same
1152: format of Command, Event, and optionally PRI, queues, and in-memory data structures.
1153: 
1154: 
1155: Certain fields in architected SMMU registers and structures are marked as IMPLEMENTATION DEFINED. The content
1156: of these fields is specific to the SMMU implementation, but implementers must not use these fields in such a way
1157: that a generic SMMUv3 driver becomes unusable. Unless a driver has extended knowledge of particular
1158: IMPLEMENTATION DEFINED fields or features, the driver must treat all such fields as reserved and set them to 0. An
1159: implementation only uses IMPLEMENTATION DEFINED fields to enable extended functionality or features, and
1160: remains compatible with generic driver software by maintaining architected behavior when these fields are set to
1161: 0.
1162: 
1163: 
1164: 
1165: 3.2 Stream numbering
1166: An incoming transaction has an address, size, and attributes such as read/write, Secure/Non-secure, Shareability,
1167: Cacheability. If more than one client device uses the SMMU traffic must also have a sideband StreamID so the
1168: sources can be differentiated. How a StreamID is constructed and carried through the system is IMPLEMENTATION
1169: DEFINED. Logically, a StreamID corresponds to a device that initiated a transaction.
1170: Note: The mapping of a physical device to StreamID must be described to system software.
1171: ARM recommends that StreamID be a dense namespace starting at 0. The StreamID namespace is per-SMMU.
1172: Devices assigned the same StreamID but behind different SMMUs are seen to be different sources. A device
1173: might emit traffic with more than one StreamID, representing data streams differentiated by device-specific state.
1174: 
1175: 
1176: StreamID is of IMPLEMENTATION DEFINED size, between 0 and 32 bits.
1177: 
1178: 
1179: The StreamID is used to select a Stream Table Entry (STE) in a Stream table, which contains per-device
1180: configuration. The maximum size of in-memory configuration structures relates to the maximum StreamID span
1181:                                      StreamIDSize
1182: (see 3.3 below), with a maximum of 2              entries in the Stream table.
1183: 
1184: 
1185: Page 24 of 427                  Copyright © 2016-2017 ARM or its affiliates. All rights reserved.     ARM IHI 0070B
1186:                                                      Non-Confidential
1187: 
1188: Another property, SubstreamID, might optionally be provided to an SMMU implementing stage 1 translation. The
1189: SubstreamID is of IMPLEMENTATION DEFINED size, between 0 and 20 bits, and differentiates streams of traffic
1190: originating from the same logical block in order to associate different application address translations to each.
1191: Note: An example would be a compute accelerator with 8 contexts that might each map to a different user
1192: process, but where the single device has common configuration meaning it must be assigned to a VM whole.
1193: Note: The SubstreamID is equivalent to a PCIe PASID. Because the concept can be applied to non-PCIe
1194: systems, it has been given a more generic name in the SMMU. The maximum size of SubstreamID, 20 bits,
1195: matches the maximum size of a PCIe PASID.
1196: 
1197: 
1198: The incoming transaction flags whether or not a SubstreamID is supplied and this might differ on a per-transaction
1199: basis.
1200: 
1201: 
1202: Both of these properties and sizes are discoverable through the SMMU_IDR1 register. See section 16.4 for
1203: recommendations on StreamID and SubstreamID sizing.
1204: 
1205: 
1206: The StreamID is the key that identifies all configuration for a transaction. A StreamID is configured to bypass or be
1207: subject to translation and such configuration determines which stage 1 or stage 2 translation to apply. The
1208: SubstreamID provides a modifier that selects between a set of stage 1 translations indicated by the StreamID but
1209: has no effect on the stage 2 translation which is selected by the StreamID only.
1210: 
1211: 
1212: A stage 2-only implementation does not take a SubstreamID input. An implementation with stage 1 is not
1213: required to support substreams, therefore is not required to take a SubstreamID input.
1214: 
1215: 
1216: The SMMU optionally supports two Security states and, if supported, the StreamID input to the SMMU is qualified
1217: by a SEC_SID flag that determines whether the input StreamID value refers to the Secure or Non-secure
1218: StreamID namespace. A Non-secure StreamID identifies an STE within the Non-secure Stream table and a
1219: Secure StreamID identifies an STE within the Secure Stream table. In this document, the term StreamID implicitly
1220: refers to the StreamID disambiguated by SEC_SID (if present) and does not refer solely to a literal StreamID input
1221: value (which would be associated with two STEs when security is supported) unless explicitly stated otherwise.
1222: See section 3.10.
1223: 
1224: 
1225: ARM expects that, for PCI, StreamID is generated from the PCI RequesterID so that StreamID[15:0] ==
1226: RequesterID[15:0]. When more than one Root Complex is hosted by one SMMU, ARM recommends that the 16-
1227: bit RequesterID namespaces are arranged into a larger StreamID namespace by using upper bits of StreamID to
1228: differentiate the contiguous RequesterID namespaces, so that StreamID[N:16] indicates which Root Complex
1229: (PCIe domain/segment) is the source of the stream source. In PCIe systems, the SubstreamID is intended to be
1230: directly provided from the PASID [2] in a one to one fashion.
1231: 
1232: 
1233: Therefore, for SMMU implementations intended for use with PCI clients, supported StreamID size must be at least
1234: 16 bits.
1235: 
1236: 
1237: 
1238: 3.3 Data structures and translation procedure
1239: The SMMU uses a set of data structures in memory to locate translation data. Registers hold the base addresses
```

## smmuv3.txt
原始路径：/home/ubuntu/.hermes/cache/scratch/virtualization-outline/smmuv3.txt
行范围：1391–1427

```text
1391:                                                  2
1392: 1                  Y      0x2f20               2
1393: 
1394: 2                  N      –                    –
1395:                                                  0
1396: 3                  Y      0x4000               2
1397: 
1398: In this example:
1399:     •    StreamIDs 0-1023 (4 × 8-bit level 2 tables) are represented, though not all are valid.
1400:     •    StreamIDs 0-255 are configured by the array of STEs at 0x1000 (each of which separately enables the
1401:          relevant StreamID).
1402:     •    StreamIDs 256-259 are configured by the array of STEs at 0x2F20.
1403:     •    StreamIDs 512-767 are all invalid.
1404:     •    The STE of StreamID 768 is at 0x4000.
1405: 
1406: 
1407: A two-level table with a split point of 8 can reduce the memory usage compared to a large and sparse linear table
1408: used with PCIe. If the full 256 PCIe bus numbers are supported, the RequesterID or StreamID space is 16-bits.
1409: However, because there is usually one PCIe bus for each physical link and potentially one device for each bus, in
1410: the worst case a valid StreamID might only appear once every 256 StreamIDs.
1411: 
1412: 
1413: Alternatively, a split point of 6 provides 64 bottom-level STEs, enabling use of a 4KB page for each bottom-level
1414: table.
1415: 
1416: 
1417: 
1418: 3.3.2 StreamIDs to Context Descriptors
1419: The STE contains the configuration for each stream indicating:
1420:     •    Whether traffic from the device is enabled.
1421:     •    Whether it is subject to stage 1 translation.
1422:     •    Whether it is subject to stage 2 translation, and the relevant translation tables.
1423:     •    Which data structures locate translation tables for stage 1.
1424: 
1425: 
1426: If stage 1 is used, the STE indicates the address of one or more CDs in memory.
1427: 
```

## smmuv3.txt
原始路径：/home/ubuntu/.hermes/cache/scratch/virtualization-outline/smmuv3.txt
行范围：2456–2528

```text
2456: The commit point, 4, represents the conceptual point after which the event will definitely be written to the queue
2457: and eventually become visible. Until commit, the event write might not happen (for example, if the queue is full
2458: and software never consumes any entries, the event write will never commit).
2459: 
2460: 
2461: An event write that has committed is guaranteed to become visible in the Event queue, if the subsequent write
2462: does not experience an external abort, see section 7.2.
2463: 
2464: 
2465: The write of a stall event record must not commit until the queue entry is deemed writable (the queue is enabled
2466: and not full). If it is not writable, the stall record is buffered until the queue is next writable, unless one of the
2467: exceptions in section 7.2 causes the record to be discarded.
2468: 
2469: 
2470: 
2471: 3.5.5 Event merging
2472: Implementations are permitted to merge some event records together. This might happen where multiple identical
2473: events occurred, and can be used to reduce the volume of events recorded into the Event queue where individual
2474: events do not supply additional useful information.
2475: 
2476: 
2477: Page 46 of 427                    Copyright © 2016-2017 ARM or its affiliates. All rights reserved.         ARM IHI 0070B
2478:                                                        Non-Confidential
2479: 
2480: Events can be merged where all of the following conditions are upheld:
2481:     •    The event types and all fields are identical, except fields explicitly indicated in section 7.3.
2482:     •    If present, the Stall field is 0. Stall fault records are not merged, see section 3.12.2.
2483: 
2484: 
2485: An implementation is not required to merge any events, but one that does is required to support the STE.MEV flag
2486: to enable or inhibit merging of events relating to a given stream.
2487: 
2488: 
2489: Note: For debugging purposes, merging of some events can be disabled on a per-stream basis using the
2490: STE.MEV flag.
2491: 
2492: 
2493: Software implementations (for example a virtual emulation of an SMMU) are not required to respect STE.MEV. A
2494: hypervisor might cause events to continue to be merged after a guest requests merging to be disabled, for
2495: example if it determines a misbehaving guest to be causing too many debug events.
2496: 
2497: 
2498: See section 7.3.1 for details.
2499: 
2500: 
2501: 
2502: 3.6 Structure and queue ownership
2503: ARM expects that the Non-secure Stream table, Command queue, Event queue and PRI queue are controlled by
2504: the most privileged Non-secure system software.
2505: 
2506: 
2507: If present, ARM expects that the Secure Stream table, Secure Command queue and Secure Event queue are
2508: controlled by Secure software. For example, these would be controlled by software in EL3 if a separation in
2509: control between Secure EL1 and EL3 is required.
2510: 
2511: 
2512: ARM expects that the stage 2 translation tables indicated by all STEs are controlled by a hypervisor.
2513: 
2514: 
2515: The ownership of stage 1 CDs and translation tables depends on the configuration in use. If pointed to by a
2516: Secure STE, they are controlled by Secure software (either EL3 or EL1). If pointed to by a Non-secure STE, the
2517: context might be one of the following:
2518:     •    Used by a bare-metal OS, which controls the descriptor and translation tables and is addressed by PA.
2519:     •    Used internally by a hypervisor, which controls the descriptor and translation tables and is addressed by
2520:          PA.
2521:     •    Used by a guest, in which case ARM expects that the CD and translation tables are controlled by the
2522:          guest, and addressed by IPA.
2523: 
2524: 
2525: Note: ARM expects that the Non-secure Event queue is managed by the hypervisor, which forwards events into
2526: guest VMs as appropriate. StreamIDs might be mapped from physical to virtual equivalents during this process.
2527: 
2528: 
```

## arm-smmu-v3.c
原始路径：/home/ubuntu/linux-source-7.0.0/drivers/iommu/arm/arm-smmu-v3/arm-smmu-v3.c
行范围：3368–3404

```text
3368: static struct iommu_domain *
3369: arm_smmu_domain_alloc_paging_flags(struct device *dev, u32 flags,
3370: 				   const struct iommu_user_data *user_data)
3371: {
3372: 	struct arm_smmu_master *master = dev_iommu_priv_get(dev);
3373: 	struct arm_smmu_device *smmu = master->smmu;
3374: 	const u32 PAGING_FLAGS = IOMMU_HWPT_ALLOC_DIRTY_TRACKING |
3375: 				 IOMMU_HWPT_ALLOC_PASID |
3376: 				 IOMMU_HWPT_ALLOC_NEST_PARENT;
3377: 	struct arm_smmu_domain *smmu_domain;
3378: 	int ret;
3379: 
3380: 	if (flags & ~PAGING_FLAGS)
3381: 		return ERR_PTR(-EOPNOTSUPP);
3382: 	if (user_data)
3383: 		return ERR_PTR(-EOPNOTSUPP);
3384: 
3385: 	smmu_domain = arm_smmu_domain_alloc();
3386: 	if (IS_ERR(smmu_domain))
3387: 		return ERR_CAST(smmu_domain);
3388: 
3389: 	switch (flags) {
3390: 	case 0:
3391: 		/* Prefer S1 if available */
3392: 		if (smmu->features & ARM_SMMU_FEAT_TRANS_S1)
3393: 			smmu_domain->stage = ARM_SMMU_DOMAIN_S1;
3394: 		else
3395: 			smmu_domain->stage = ARM_SMMU_DOMAIN_S2;
3396: 		break;
3397: 	case IOMMU_HWPT_ALLOC_NEST_PARENT:
3398: 		if (!(smmu->features & ARM_SMMU_FEAT_NESTING)) {
3399: 			ret = -EOPNOTSUPP;
3400: 			goto err_free;
3401: 		}
3402: 		smmu_domain->stage = ARM_SMMU_DOMAIN_S2;
3403: 		smmu_domain->nest_parent = true;
3404: 		break;
```

## Dall and Nieh - 2014 - KVMARM the design and implementation of the linux ARM hypervisor.md
原始路径：/home/ubuntu/高级操作系统教程/references/Dall and Nieh - 2014 - KVMARM the design and implementation of the linux ARM hypervisor.md
行范围：14–34

```text
14: As ARM CPUs become increasingly common in mobile devices
15: and servers, there is a growing demand for providing the ben-
16: efits of virtualization for ARM-based devices. We present our
17: experiences building the Linux ARM hypervisor, KVM/ARM,
18: the first full system ARM virtualization solution that can run
19: unmodified guest operating systems on ARM multicore hard-
20: ware. KVM/ARM introduces split-mode virtualization, allowing
21: a hypervisor to split its execution across CPU modes and be inte-
22: grated into the Linux kernel. This allows KVM/ARM to leverage
23: existing Linux hardware support and functionality to simplify hy-
24: pervisor development and maintainability while utilizing recent
25: ARM hardware virtualization extensions to run virtual machines
26: with comparable performance to native execution. KVM/ARM
27: has been successfully merged into the mainline Linux kernel,
28: ensuring that it will gain wide adoption as the virtualization
29: platform of choice for ARM. We provide the first measurements
30: on real hardware of a complete hypervisor using ARM hardware
31: virtualization support. Our results demonstrate that KVM/ARM
32: has modest virtualization performance and power costs, and
33: can achieve lower performance and power costs compared to
34: x86-based Linux virtualization on multicore hardware.
```

## Dall and Nieh - 2014 - KVMARM the design and implementation of the linux ARM hypervisor.md
原始路径：/home/ubuntu/高级操作系统教程/references/Dall and Nieh - 2014 - KVMARM the design and implementation of the linux ARM hypervisor.md
行范围：165–177

```text
165: concluding remarks.
166: 2.
167: ARM Virtualization Extensions
168: Because the ARM architecture is not classically virtualiz-
169: able [27], ARM introduced hardware virtualization support
170: as an optional extension in the latest ARMv7 [6] and ARMv8 [7]
171: architectures. For example, the Cortex-A15 [4] is a current
172: ARMv7 CPU with hardware virtualization support. We present
173: a brief overview of the ARM virtualization extensions.
174: CPU Virtualization
175: Figure 1 shows the CPU modes on the
176: ARMv7 architecture, including TrustZone (Security Extensions)
177: and a new CPU mode called Hyp mode. TrustZone splits the
```
