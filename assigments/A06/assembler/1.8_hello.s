.global _start
.data
message: .ascii "Hello edan65!\n"
.text
_start:
    movq $1, %rdi       # stdout file descriptor
    movq $message, %rsi # message to print
    movq $14, %rdx      # message length
    movq $1, %rax       # sys write
    syscall
    movq $0, %rdi       # exit code = 0
    movq $60, %rax      # sys_exit
    syscall
