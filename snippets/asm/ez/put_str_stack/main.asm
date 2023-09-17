section .data
hello   db 'Hello world!!',0
promess db ' So many possibilities!!',0

section .text

global _start

put_str:
    mov rbx, [rsp + 8]
    
    loop:
        cmp byte [rbx], 0
        je end

        mov rax, 1    ; putc(rbx)
        mov rdi, 1
        mov rsi, rbx
        mov rdx, 1
        syscall

        inc rbx
        jmp loop
    end: 
        ret

_start:
    mov rbp, rsp
    push hello
    call put_str
    mov rsp, rbp

    mov rbp, rsp
    push promess
    call put_str
    mov rsp, rbp

    mov rbp, rsp
    push hello
    call put_str
    mov rsp, rbp

    mov rbp, rsp
    push hello
    call put_str
    mov rsp, rbp

    mov rax, 60       ; exit(0)
    xor rbx, rbx
    syscall
