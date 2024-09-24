section .text
global _start

_start:
    ; 0x0068732f6e69622f
    mov al, 0x2f
    shl eax, 8
    mov al, 0x62
    shl eax, 8
    mov al, 0x69
    shl eax, 8
    mov al, 0x6e
    shl eax, 8
    
    ; Exit the program
    mov eax, 60   ; syscall: exit
    xor edi, edi  ; status: 0
    syscall