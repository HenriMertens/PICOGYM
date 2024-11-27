For this challenge we get a file with some assembly code in it and are tasked with getting the flag.


1) First thing i did was cat out the assembly file and see if I find something interesting:
```

	.file	"chall.c"
	.text
	.section	.rodata
	.align 8
.LC1:
	.string	"Correct! You entered the flag."
.LC2:
	.string	"No, that's not right."
	.align 8
.LC0:
	.string	"\207\312\304\371\307m\2753&V\035A"
	.string	"\231]\314~\025\345\225\343\177\013M\214\034SJG\246i\372\026\0323@\033jW\204\370\311}\221\350T\236pr"
	.text
	.globl	main
	.type	main, @function
main:
.LFB5:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	pushq	%rbx
	subq	$296, %rsp
	.cfi_offset 3, -24
	movl	%edi, -292(%rbp)
	movq	%rsi, -304(%rbp)
	movq	%fs:40, %rax
	movq	%rax, -24(%rbp)
	xorl	%eax, %eax
	movq	.LC0(%rip), %rax
	movq	8+.LC0(%rip), %rdx
	movq	%rax, -144(%rbp)
	movq	%rdx, -136(%rbp)
	movq	16+.LC0(%rip), %rax
	movq	24+.LC0(%rip), %rdx
	movq	%rax, -128(%rbp)
	movq	%rdx, -120(%rbp)
	movq	32+.LC0(%rip), %rax
	movq	40+.LC0(%rip), %rdx
	movq	%rax, -112(%rbp)
	movq	%rdx, -104(%rbp)
	movzwl	48+.LC0(%rip), %eax
	movw	%ax, -96(%rbp)
	movabsq	$6696342006613324260, %rax
	movabsq	$-8132455899522779815, %rdx
	movq	%rax, -80(%rbp)
	movq	%rdx, -72(%rbp)
	movabsq	$1620531284261501257, %rax
	movabsq	$-8910415579227789898, %rdx
	movq	%rax, -64(%rbp)
	movq	%rdx, -56(%rbp)
	movabsq	$-1220993050035004038, %rax
	movabsq	$9122898327681286650, %rdx
	movq	%rax, -48(%rbp)
	movq	%rdx, -40(%rbp)
	movw	$44, -32(%rbp)
	movq	stdin(%rip), %rdx
	leaq	-208(%rbp), %rax
	movl	$49, %esi
	movq	%rax, %rdi
	call	fgets@PLT
	movl	$0, -276(%rbp)
	jmp	.L2
.L3:
	movl	-276(%rbp), %eax
	cltq
	movzbl	-144(%rbp,%rax), %edx
	movl	-276(%rbp), %eax
	cltq
	movzbl	-80(%rbp,%rax), %eax
	xorl	%eax, %edx
	movl	-276(%rbp), %eax
	xorl	%edx, %eax
	xorl	$19, %eax
	movl	%eax, %edx
	movl	-276(%rbp), %eax
	cltq
	movb	%dl, -272(%rbp,%rax)
	addl	$1, -276(%rbp)
.L2:
	movl	-276(%rbp), %eax
	movslq	%eax, %rbx
	leaq	-144(%rbp), %rax
	movq	%rax, %rdi
	call	strlen@PLT
	cmpq	%rax, %rbx
	jb	.L3
	leaq	-272(%rbp), %rcx
	leaq	-208(%rbp), %rax
	movl	$49, %edx
	movq	%rcx, %rsi
	movq	%rax, %rdi
	call	memcmp@PLT
	testl	%eax, %eax
	je	.L4
	leaq	.LC1(%rip), %rdi
	call	puts@PLT
	movl	$0, %eax
	jmp	.L6
.L4:
	leaq	.LC2(%rip), %rdi
	call	puts@PLT
	movl	$1, %eax
.L6:
	movq	-24(%rbp), %rcx
	xorq	%fs:40, %rcx
	je	.L7
	call	__stack_chk_fail@PLT
.L7:
	addq	$296, %rsp
	popq	%rbx
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE5:
	.size	main, .-main
	.ident	"GCC: (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0"
	.section	.note.GNU-stack,"",@progbits

```

2) This is alot of assembly code that I dont really want to analyze so lets just compile it and see how it works: `gcc chall.s -o challl`
   
   ![image](https://github.com/user-attachments/assets/c9502b09-fb9e-46d5-a579-ac585e300093)

   Seems slightly broken lol

3) Since I dont want to analyze the assembly lets make ghidra do it (I laready renamed some variables):
   ![image](https://github.com/user-attachments/assets/6968ea12-c2d0-4fc7-b2be-b3eb563e193a)

  The logic itself is pretty straight-forward after you renamed the variables. There are two sets of encrypted data in the function, and everything just gets xored with each other and compared. In python it would look something like this:
  ```python
i^encr[i]^key[i]^19
```
  with encr and ket being the data thats intialised.

4) A simple python script doing this xor operation should do the trick, I asked chatgpt to format the data into a python array (also mentioned little endian) and then were basocally done.
```python

encr = [
    0x87, 0xca, 0xc4, 0xf9, 0xc7, 0x6d, 0xbd, 0x33,  # encr_data
    0x26, 0x56, 0x1d, 0x41, 0x00, 0x99, 0x5d, 0xcc,  # local_90
    0x7e, 0x15, 0xe5, 0x95, 0xe3, 0x7f, 0x0b, 0x4d,  # local_88
    0x8c, 0x1c, 0x53, 0x4a, 0x47, 0xa6, 0x69, 0xfa,  # local_80
    0x16, 0x1a, 0x33, 0x40, 0x1b, 0x6a, 0x57, 0x84,  # local_78
    0xf8, 0xc9, 0x7d, 0x91, 0xe8, 0x54, 0x9e, 0x70,  # local_70
    0x72                                           # local_68
]
key = [
    0xe4, 0xb1, 0xb6, 0x86, 0x93, 0x2f, 0xee, 0x5c,  # key
    0x59, 0x35, 0x6a, 0x6d, 0x72, 0xb6, 0x23, 0x8f,  # local_50
    0x49, 0x79, 0xd0, 0xf9, 0x9d, 0x48, 0x7d, 0x16,  # local_48
    0xb6, 0x65, 0x05, 0x77, 0x3d, 0xd8, 0x57, 0x84,  # local_40
    0x7a, 0x5d, 0x71, 0x43, 0x4a, 0x29, 0x0e, 0xef,  # local_38
    0xfa, 0xc1, 0x72, 0x9f, 0xb1, 0x0b, 0x9b, 0x7e,  # local_30
    0x2c                                           # local_28
]


password = ""

for i in range(len(encr)):
    k = i^encr[i]^key[i]^19
    password += chr(k)
print(password)

```
`picoCTF{dyn4m1c_4n4ly1s_1s_5up3r_us3ful_9266fa82}`

