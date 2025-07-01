# Compilador completo - Código MIPS generado
# Arquitectura: MIPS32
# Simulador: SPIM

.data
    newline: .asciiz "\n"
    space: .asciiz " "

.text
.globl main

main:
    li $v0, 10                # system call para exit
    syscall                   # terminar programa
    