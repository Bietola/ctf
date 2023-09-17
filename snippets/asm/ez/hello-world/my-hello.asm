section .data

hello db 'Hello world!!',0

section .text

global _start

put_str:
    mov rbx, rax   ; arg1

    mov rax, 1     ; sys_write
    mov rdi, 1
    mov rsi, rbx
    mov rdx, 14    ; TODO: Make this variablevariable
    syscall

    ret

_start:
    mov rax, hello ; arg1
    call put_str

    mov rax, 60                 ; syscall number for sys_exit
    xor rdi, rdi                ; exit status: 0
    syscall
