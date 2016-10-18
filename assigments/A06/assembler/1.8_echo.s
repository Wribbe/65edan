.global _start
.data
buf: .skip 1024
.text
_start:
    movq $0, %rdi       # stdin file descriptor to destination index
    movq $buf, %rsi     # write buffer addres to source index
    movq $1024, %rdx    # write buffer length to accumulator
    movq $0, %rax       # write 0 to accumulator -> sys_read
    syscall

    movq $1, %rdi       # stdout file description to destination index
    movq $buf, %rsi     # write address for buf to source index
    movq %rax, %rdx     # copy message length to rdx-accumulator
    movq $1, %rax       # write 1 to a-accumulator -> sys_write
    syscall

    movq $0, %rdi       # Set destination index to a-accumulator -> stdin
    movq $60, %rax      # write
    syscall
