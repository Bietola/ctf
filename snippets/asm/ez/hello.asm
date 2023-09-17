section .data
    hello db 'Hello, World!',0  ; Null-terminated string

section .text
global _start

; Function to print a null-terminated string
print_string:
    ; Input: RDI - Pointer to the string
    loop:
        mov al, [rdi]           ; Load the next character
        test al, al             ; Check if it's the null terminator
        jz done                  ; If null terminator, we are done
        mov rax, 1              ; syscall number for sys_write
        mov rdi, 1              ; file descriptor 1 (stdout)
        lea rsi, [rdi]          ; Address of the character to print
        mov rdx, 1              ; message length (1 byte)
        syscall
        inc rdi                 ; Move to the next character
        jmp loop                ; Repeat for the next character
    done:
        ret

_start:
    ; Call the print_string function to print "Hello, World!"
    mov rdi, hello            ; Pointer to the message
    call print_string

    ; Exit the program (syscall number for sys_exit is 60)
    mov rax, 60               ; syscall number for sys_exit
    xor rdi, rdi              ; exit status: 0
    syscall
