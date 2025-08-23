import meu_modulo as mm

print(mm.soma(2,6))
print(mm.saudacao('1986','2025  '))

valor_a = int(input('Insira o primeiro valor:'))
valor_b = int(input('Insira o segundo valor:'))

print(mm.soma(valor_a,valor_b))

usuarioNasc = int(input('Informe o ano em que nasceu: '))
usuarioatual = int(input('Informe o ano atual: '))
idade = mm.calcularIdade(usuarioNasc,usuarioatual)
print(f 'Você tem {idade} anos')

                  