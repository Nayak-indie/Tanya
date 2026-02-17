; Tanya - Assembly RSS Header Parser
; NASM x86-64 Linux
; Build: nasm -f elf64 -o bin/parser asm_parser.o
; Link: ld -o bin/parser asm_parser.o
; Run: ./bin/parser

section .data
    prompt db "Enter RSS URL to parse: ", 0
    prompt_len equ $ - prompt
    buffer resb 4096
    header db "<?xml", 0
    rss_tag db "<rss", 0
    atom_tag db "<feed", 0
    
section .bss
    url_buffer resb 512

section .text
    global _start

_start:
    ; Print prompt
    mov rax, 1              ; sys_write
    mov rdi, 1              ; stdout
    mov rsi, prompt
    mov rdx, prompt_len
    syscall
    
    ; Read URL input
    mov rax, 0              ; sys_read
    mov rdi, 0              ; stdin
    mov rsi, url_buffer
    mov rdx, 511
    syscall
    
    ; Check if RSS or Atom
    mov rsi, url_buffer
    mov rdi, header
    call compare_strings
    cmp rax, 1
    je .is_xml
    
    mov rsi, url_buffer
    mov rdi, rss_tag
    call compare_strings
    cmp rax, 1
    je .is_rss
    
    mov rsi, url_buffer
    mov rdi, atom_tag
    call compare_strings
    cmp rax, 1
    je .is_atom
    
    jmp .unknown

.is_xml:
    mov rsi, msg_xml
    jmp .print_msg
    
.is_rss:
    mov rsi, msg_rss
    jmp .print_msg
    
.is_atom:
    mov rsi, msg_atom
    jmp .print_msg
    
.unknown:
    mov rsi, msg_unknown

.print_msg:
    mov rdx, rsi
    mov rdx, [rdx]
    ; Print and exit
    mov rax, 60             ; sys_exit
    xor rdi, rdi            ; exit code 0
    syscall

compare_strings:
    ; Simple string comparison
    ; Input: rsi = string1, rdi = string2
    ; Output: rax = 1 if equal, 0 if not
    push rbx
    push rcx
    push rsi
    push rdi
    
    xor rcx, rcx
.loop:
    mov al, [rsi + rcx]
    mov bl, [rdi + rcx]
    cmp al, bl
    jne .not_equal
    cmp al, 0
    je .equal
    inc rcx
    jmp .loop
    
.equal:
    mov rax, 1
    jmp .done
    
.not_equal:
    mov rax, 0
    
.done:
    pop rdi
    pop rsi
    pop rcx
    pop rbx
    ret

msg_xml db "Detected: XML format", 10, 0
msg_rss db "Detected: RSS feed", 10, 0
msg_atom db "Detected: Atom feed", 10, 0
msg_unknown db "Unknown format", 10, 0
