# 原始证据摘录：intro

这些是原文/源码，不是正文草稿。行号仅用于追溯。勿把页面断行当成语义断句。

## Popek and Goldberg - 1974 - Formal requirements for virtualizable third generation architectures.md
原始路径：/home/ubuntu/高级操作系统教程/references/Popek and Goldberg - 1974 - Formal requirements for virtualizable third generation architectures.md
行范围：151–218

```text
151: 1. Virtual Machine Concepts 
152: There are currently a number of viewpoints suggest- 
153: ing what a virtual machine is, how it ought to be con- 
154: structed, and what hardware and operating system 
155: implications result [1, 6, 7, 9, 12]. This pap¢r examines 
156: computer architectures of third-generation-like machines 
157: and demonstrates a simple condition which may be 
158: tested to determine whether an architecture can support 
159: a virtual machine. This condition may also be employed 
160: in machine design. In the following, we specify in- 
161: tuitively what is meant by the above, then develop a 
162: more exact model of third-generation-like machines, 
163: and finally state and prove a sufficient condition for 
164: such a system to be virtualizable. 
165: A virtual machine is taken to be an efficient, iso- 
166: lated duplicate of the real machine. We explain these 
167: notions through the idea of a virtual machine monitor 
168: (V~M). See Figure 1. As a piece of software a VMM has 
169: three essential characteristics. First, the VMM provides 
170: an environment for programs which is essentially iden- 
171: tical with the original machine; second, programs run 
172: in this environment show at worst only minor decreases 
173: in speed; and last, the VMM is in complete control of 
174: system resources. 
175: By an "essentially identical" environment, the first 
176: characteristic, is meant the following. Any program 
177: run under the VMM should exhibit an effect identical 
178: with that demonstrated if the program had been run 
179: on the original machine directly, with the possible 
180: exception of differences caused by the availability of 
181: system resources and differences caused by timing de- 
182: pendencies. The latter qualification is required because 
183: Fig. 1. The virtual machine monitor. 
184: VMM 
185: I 
186: Hardware 
187: 413 
188: of the intervening level of software and because of the 
189: effect of any other virtual machines concurrently exist- 
190: ing on the same hardware. The former qualification 
191: arises, for example, from the desire to include in our 
192: definition the ability to have varying amounts of memory 
193: made available by the virtual machine monitor. The 
194: identical environment requirement excludes the behavior 
195: of the usual time-sharing operating system from being 
196: classed as a virtual machine monitor. 
197: The second characteristic of a virtual machine 
198: monitor is efficiency. It demands that a statistically 
199: dominant subset of the virtual processor's instructions 
200: be executed directly by the real processor, with no 
201: software intervention by the VMM. This statement rules 
202: out traditional emulators and complete software in- 
203: terpreters (simulators) from the virtual machine um- 
204: brella. 
205: The third characteristic, resource control, labels as 
206: resources the usual items such as memory, peripherals, 
207: and the like, although not necessarily processor activity. 
208: The VMM is said to have complete control of these 
209: resources if (1) it is not possible for a program running 
210: under it in the created environment to access any 
211: resource not explicitly allocated to it, and (2) it is 
212: possible under certain circumstances for the VMM to 
213: regain control of resources already allocated. 
214: A vh'tual machine is the environment created by the 
215: virtual machine monitor. This definition is intended not 
216: only to reflect generally accepted notions of virtual 
217: machines, but also to provide a reasonable environ- 
218: ment for a proof. 
```

## Popek and Goldberg - 1974 - Formal requirements for virtualizable third generation architectures.md
原始路径：/home/ubuntu/高级操作系统教程/references/Popek and Goldberg - 1974 - Formal requirements for virtualizable third generation architectures.md
行范围：250–328

```text
250: <!-- page 3 -->
251: 
252: addressable memory. For the purposes of the formal 
253: part of this paper, we assume that I/o instructions 
254: and interrupts don't exist, although they may be added 
255: as extensions. 
256: The computer is presented by stating several neces- 
257: sary assumptions about its behavior, describing its 
258: state-space, and specifying how changes of state may 
259: occur. 
260: The processor is a conventional one with two modes 
261: of operation, supervisor and user. In supervisor mode, 
262: the complete instruction repertoire is available to the 
263: precessor. In user mode, it is not. Memory addressing 
264: is done relative to the contents of a relocation register. 
265: The instruction set consists of the usual complement of 
266: instructions for doing arithmetic, testing, branching, 
267: moving data in memory, and the like. In particular, 
268: with these instructions, it is possible to perform a table 
269: lookup on a table of arbitrary size, key, and value, and 
270: having obtained the value, move it anywhere in memory 
271: (the table look-up and copy property). 1 
272: The machine can exist in any one of a finite number 
273: of states where each state has four components : execut- 
274: able storage E, processor mode M, program counter P, 
275: and relocation-bounds register R. 
276: S = (E, M, P,R) 
277: Executable storage is a conventional word or byte 
278: addressed memory of size q. The notation Eli] will 
279: refer to the contents of the ith unit of storage in E, i.e. 
280: E = E' if and only if Eli] = E'[i] for any 0 _< i < q. 
281: The relocation-bounds register, R = (l, b) is always 
282: active, regardless of the machine's current mode. The 
283: relocation part l of the register gives an absolute address, 
284: which will correspond to the apparent address 0. The 
285: bounds part b will give the absolute size (not the largest 
286: valid address) of the virtual memory. If it is desired to 
287: access all of memory, the relocation must be set to 0 
288: and the bounds to q -- 1. 
289: If an instruction produces the address a, the address 
290: development is as follows: 
291: if a 4- / > q then memorytrap else 
292: if a > b then memorytrap 
293: else use E[a + l]. 
294: The meaning of "memorytrap" used here will be dis- 
295: cussed in detail in the next section. 
296: The mode M of the processor is either s or u, super- 
297: visor or user. The program counter P is an address rela- 
298: tive to the contents of R, which acts as an index into E, 
299: indicating the next instruction to be executed. Note 
300: that the state S is intended to specify the current state 
301: of the real computer system, not some portion of it, 
302: or some virtual machine. 
303: The contents of the triplet (M, P, R) are often 
304: referred to as the program status word, or PSW. To 
305: make our proof easier, we will assume that a PSW can 
306: be recorded in one storage location. This restriction 
307: can be easily removed. We shall have occasion to use 
308: El0] and El1] to store an old-Psw and fetch a new-Psw 
309: respectively. 
310: Each component of S can take on only a finite 
311: number of values. Call the finite set of states C. 
312: Then an instruction i is a function from C to C. 
313: i : C-~ C. So, for example, i(S1) = $2, or 
314: i(E1, /141, PI,R1) = (E2, M2, P2,R2). 
315: So far, this specification of a conventional third 
316: generation computer should not be too surprising. 
317: After superficial complexities in such systems are re- 
318: moved, what remains is generally a primitive protection 
319: system built around a supervisor/user mode concept, 
320: and a simple memory allocation system built around a 
321: relocation-bounds system. In this model, for simplicity, 
322: we have departed slightly from most common reloca- 
323: tion systems by assuming it to be active in the super- 
324: visor as well as user mode. This difference will not be 
325: important to the proof of our result. Note also that all 
326: references made by the processor to memory are 
327: assumed to be relocated. 
328: One key restriction in the model is the exclusion of 
```

## Popek and Goldberg - 1974 - Formal requirements for virtualizable third generation architectures.md
原始路径：/home/ubuntu/高级操作系统教程/references/Popek and Goldberg - 1974 - Formal requirements for virtualizable third generation architectures.md
行范围：383–431

```text
383: 3. Instruction Behavior 
384: In the following, we classify instructions on the 
385: basis of their behavior as a function of the state S of 
386: the machine. Which groups an instruction falls into 
387: will determine whether the real machine is virtualizable. 
388: Instruction i is privileged if and only if for any pair 
389: of states 5'1 = (e, s, p, r) and 5'2 = (e, u, p, r) in which 
390: i(S~) and i(S2) do not memory trap: i(S2) traps and 
391: i(S1) does not. 
392: The states 5'1 and $2 differ only in that the mode of 
393: St is supervisor and the mode of $2 is user. The trap 
394: that occurs under these conditions is often called a 
395: privileged instruction trap. 
396: This notion of a privileged instruction is close to the 
397: conventional one. Privileged instructions are independ- 
398: ent of the virtualization process. They are merely 
399: characteristics of the machine which may be determined 
400: from reading the principles of operation. Note, however, 
401: that the way we have defined privileged instructions 
402: requires them to trap. Merely NoPing the instruction 
403: without trapping is insufficient. The latter case should 
404: not be called a privileged instruction; maybe "user 
405: mode NOP" would be more accurate. 
406: Examples of privileged instructions in common third 
407: generation machines: 
408: (1) if M = s then load_PSW 
409: else trap; 
410: (2) if M = s then load_R 
411: else trap; 
412: IBM System/360 LPSW 
413: Honeywell 6000 LBAR, 
414: DEC PDP-10 DATAO APR 
415: Another important group of instructions will be 
416: called sensitive instructions [4]. The members of this 
417: group will have a major bearing on the virtualizability 
418: of a particular machine. We define two types of sensi- 
419: tive instructions. 
420: An instruction i is control sensitive if there exists a 
421: state 5'1 = (ei, ml, Pl, rl), and i(S1) = $2 = @2, m.2, 
422: p2,/'2) such that i(&) does not memory trap, and either: 
423: (a) rl ~ r2, or (b) ml ~ m2, or both. 
424: That is, an instruction is control sensitive if it 
425: attempts to change the amount of (memory) resources 
426: available, or affects the processor mode without going 
427: through the memory trap sequence. 2 The examples 
428: given of privileged instructions are also-control sen- 
429: sitive. Another example of a control sensitive instruction 
430: is JRST 1, on the DEC PDP-10, which is a return to user 
431: mode. 
```

## Popek and Goldberg - 1974 - Formal requirements for virtualizable third generation architectures.md
原始路径：/home/ubuntu/高级操作系统教程/references/Popek and Goldberg - 1974 - Formal requirements for virtualizable third generation architectures.md
行范围：510–548

```text
510: are now ready for a definition of the second kind of 
511: sensitive instruction. An instruction i is behavior sen- 
512: sitive ~ if there exist an integer x and states: 
513: (a) & = (e I r, mr,p, r), and 
514: (b) & = (e[r @ x,m.,,p,r @ x), 
515: where 
516: (c) i(&) = (e, I r, ml,p,, 
517: r), 
518: (d) i(&) = (e2 I r @ x, m.2,p.e, r @ x), and 
519: (e) neither i(&) or i(&) memorytrap, 
520: such that either 
521: (a) el[r# 
522: e21rO x, or 
523: (b) pl # p2, or both. 
524: Intuitively, an instruction is behavior sensitive if the 
525: effect of its execution depends on the value of the reloca- 
526: tion-bounds register, i.e. upon its location in real 
527: memory, or on the mode. The other two cases, where 
528: the location-bounds register or the modes do not 
529: match after the instruction is executed, fall into the 
530: class of control sensitive instructions. 
531: In our model, there are really two kinds of behavior 
532: sensitivity. In one case, which might be called location 
533: sensitivity, 
534: an instruction's 
535: execution 
536: behavior de- 
537: pends on its location in real memory. In the other, an 
538: instruction's behavior is affected by the machine's mode. 
539: Example of behavior sensitive instructions: 
540: Location sensitive--load physical address (IBM 360/ 
541: 67 ERA). 
542: Mode sensitive--move from previous instruction 
543: space (DeC PDP-11/45 MVPI). (This instruction forms its 
544: effective address from information that depends on the 
545: current mode.) 
546: By definition, we shall say that an instruction i is 
547: sensitive if it is either control sensitive or behavior 
548: sensitive. If i is not sensitive, then it is innocuous. 
```

## Popek and Goldberg - 1974 - Formal requirements for virtualizable third generation architectures.md
原始路径：/home/ubuntu/高级操作系统教程/references/Popek and Goldberg - 1974 - Formal requirements for virtualizable third generation architectures.md
行范围：643–730

```text
643: 5. The Virtual Machine Properties 
644: There are three properties of interest when any 
645: arbitrary program is run while the control program is 
646: resident: efficiency, resource control, and equivalence. 
647: The efficiency property. All innocuous instructions 
648: are executed by the hardware directly, with no interven- 
649: tion at all on the part of the control program. 
650: The resource control property. It must be impossible 
651: for that arbitrary program to affect the system re- 
652: sources, i.e. memory, available to it; the allocator of the 
653: control program is to be invoked upon any attempt. 
654: The equivalence property. Any program K executing 
655: with a control program resident, with two possible 
656: exceptions, performs in a manner indistinguishable from 
657: the case when the control program did not exist and K 
658: had whatever freedom of access to privileged instruc- 
659: tions that the programmer had intended. 
660: As mentioned earlier, the two exceptions result from 
661: timing and resource availability problems. Because of 
662: the occasional intervention of the control program, 
663: certain instruction sequences in K may take longer to 
664: execute, so assumptions about the length of time re- 
665: quired for execution might lead to incorrect results. 
666: In our simple system we will assume for the time being 
667: that there are no such difficulties. 
668: The resource availability problem is the following. 
669: It might be the case, for example, that the allocator 
670: does not satisfy a particular request for space (an 
671: attempt to change the relocation-bounds register). The 
672: program may then be unable to function in the same 
673: manner as it would if the space were made available. 
674: The problem could easily occur, since the control pro- 
675: gram itself takes space. 
676: One way around this difficulty is to realize that the 
677: virtual machine environment being produced is a 
678: "smaller" version of the actual hardware: logically the 
679: same, but with a lesser quantity of certain resources. 
680: Then the equivalence to be guaranteed is that between 
681: running on an actual smaller hardware machine and the 
682: environment we have created. On a paged machine, the 
683: resource consumed is more likely drum space to hold 
684: the pages of the VMM. In any case, we will specify this 
685: equivalence property more precisely. But first, a defi- 
686: nition and the statement of our major theorem are in 
687: order. 
688: We say that a virtual machine monitor (VMM) is any 
689: control program that satisfies the three properties of 
690: 417 
691: efficiency, resource control, and equivalence. Then 
692: functionally, the environment which any program sees 
693: when running with a virtual machine monitor present is 
694: called a virtual machine. It is composed of the original 
695: real machine and the virtual machine monitor. This 
696: informal definition should agree with the intuitive de- 
697: scription early in this paper. 
698: That done, we may now state our basic theorem. 
699: THEOREM 1. For any conventional thh'd generation 
700: computer, a virtual machine monitor may be constructed 
701: if the set of sensitive instructions for that computer is a 
702: subset of the set of privileged instructions. 
703: 6. Discussion of Theorem 
704: Before discussing the import of this theorem, it 
705: would be appropriate to clarify what is meant by "con- 
706: ventional third generation computer." This phrase is 
707: intended to imply all the assumptions made so far in 
708: this paper regarding the operation of: relocation mech- 
709: anisms, supervisor/user mode, and trap mechanisms. 
710: The assumptions were chosen to provide both clarity 
711: and a reasonable reflection of the relevant practices in 
712: common third generation machines. Also, the phrase 
713: is meant to imply that the instruction set is of general 
714: purpose enough to allow the construction of a dis- 
715: patcher, allocator, and a generalized table lookup 
716: procedure. The need of the last will appear later in this 
717: discussion. 
718: The theorem provides a fairly simple condition 
719: sufficient to guarantee virtualizability, assuming, of 
720: course, that the requisite features of "conventional 
721: third generation machines" are present. 
722: However, 
723: those features which have been assumed are fairly 
724: standard ones, so the relationship between the sets of 
725: sensitive and privileged instructions is the only new 
726: constraint. It is a very modest one, easy to check. 
727: Further, it is also a simple matter for hardware designers 
728: to use as a design requirement. Of course, we have not 
729: characterized the requirements which result from in- 
730: terrupt handling or I/O. They are of a very similar nature. 
```

## Popek and Goldberg - 1974 - Formal requirements for virtualizable third generation architectures.md
原始路径：/home/ubuntu/高级操作系统教程/references/Popek and Goldberg - 1974 - Formal requirements for virtualizable third generation architectures.md
行范围：950–991

```text
950: 7. Recursive Virtualization 
951: A number of related results can quickly follow from 
952: this approach. One simple example is the idea of 
953: recursive virtualization. Is it possible for a virtual 
954: machine system to run under itself a copy of the VMM, 
955: and will that copy also exhibit all the properties of a 
956: VMM? If this procedure can be repeated until the 
957: resources of the system are consumed (since each con- 
958: trol program takes up space), then the original machine 
959: is recursively virtualizable [2, 6]. 
960: THEOREM 2. A conventional third generation computer 
961: is" recursively virtualizable if it is: (a) virtualizable, and 
962: (b) a VMM without any timing dependencies can be 
963: constructed for it. 
964: PROOF. This property is nearly trivial to demon- 
965: strate. A VMM is guaranteed, by definition, to produce an 
966: environment in which a large class of programs run 
967: with effect identical to that on the real machine. Then it 
968: is merely necessary to demonstrate that a VMM which 
969: belongs to that class of programs can be constructed. 
970: If it can, then the performance of the VMM running on 
971: the real machine and under other VMMS will be in- 
972: distinguishable. 
973: The only programs excluded from the class of 
974: identically performing programs are those which are 
975: resource bound, or have timing dependencies. The 
976: second limitation is mentioned in the statement of the 
977: Communications 
978: July 1974 
979: of 
980: Volume 17 
981: the ACM 
982: Number 7
983: 
984: <!-- page 9 -->
985: 
986: theorem. The resource bound for our skeletal model is 
987: only memory, and it just limits the depth (number of 
988: nested VMMS) of the recursion, as pointed out in the 
989: definition of recursive virtualization. Hence the VMM as 
990: constructed earlier qualifies as a member of that "large 
991: class of programs." Q.E.D. 
```

## Bellard - 2005 - QEMU, a Fast and Portable Dynamic Translator.md
原始路径：/home/ubuntu/高级操作系统教程/references/Bellard - 2005 - QEMU, a Fast and Portable Dynamic Translator.md
行范围：3–57

```text
3: QEMU, a Fast and Portable Dynamic Translator
4: Fabrice Bellard
5: Abstract
6: We present the internals of QEMU, a fast machine em-
7: ulator using an original portable dynamic translator. It
8: emulates several CPUs (x86, PowerPC, ARM and Sparc)
9: on several hosts (x86, PowerPC, ARM, Sparc, Alpha and
10: MIPS). QEMU supports full system emulation in which
11: a complete and unmodiﬁed operating system is run in a
12: virtual machine and Linux user mode emulation where a
13: Linux process compiled for one target CPU can be run
14: on another CPU.
15: 1
16: Introduction
17: QEMU is a machine emulator: it can run an unmodiﬁed
18: target operating system (such as Windows or Linux) and
19: all its applications in a virtual machine. QEMU itself
20: runs on several host operating systems such as Linux,
21: Windows and Mac OS X. The host and target CPUs can
22: be different.
23: The primary usage of QEMU is to run one operating
24: system on another, such as Windows on Linux or Linux
25: on Windows. Another usage is debugging because the
26: virtual machine can be easily stopped, and its state can
27: be inspected, saved and restored. Moreover, speciﬁc em-
28: bedded devices can be simulated by adding new machine
29: descriptions and new emulated devices.
30: QEMU also integrates a Linux speciﬁc user mode em-
31: ulator. It is a subset of the machine emulator which runs
32: Linux processes for one target CPU on another CPU. It
33: is mainly used to test the result of cross compilers or to
34: test the CPU emulator without having to start a complete
35: virtual machine.
36: QEMU is made of several subsystems:
37: • CPU emulator (currently x861, PowerPC, ARM and
38: Sparc)
39: • Emulated devices (e.g.
40: VGA display, 16450 se-
41: rial port, PS/2 mouse and keyboard, IDE hard disk,
42: NE2000 network card, ...)
43: • Generic devices (e.g. block devices, character de-
44: vices, network devices) used to connect the emu-
45: lated devices to the corresponding host devices
46: • Machine descriptions (e.g. PC, PowerMac, Sun4m)
47: instantiating the emulated devices
48: • Debugger
49: • User interface
50: This article examines the implementation of the dy-
51: namic translator used by QEMU. The dynamic transla-
52: tor performs a runtime conversion of the target CPU in-
53: structions into the host instruction set. The resulting bi-
54: nary code is stored in a translation cache so that it can
55: be reused. The advantage compared to an interpreter is
56: that the target instructions are fetched and decoded only
57: once.
```
