section .data
hello db 'Hello world!!',0

section .text

global _start

put_str:
    mov rbx, rax     ; arg1
    
    loop:
        cmp byte [rbx], 0x0
        je end

        mov rax, 1     ; putc(rbx)
        mov rdi, 1
        mov rsi, rbx
        mov rdx, 1
        syscall
        
        inc rbx
        jmp loop
    end:
        ret

_start:
    mov rax, hello
    call put_str

    mov rax, 60  ; exit
    xor rbx, rbx
    syscall

