#quando eu preciso que o programa entenda que é uma palavra, eu coloco entre aspas ""
# str significa string
import math

nome = "Davi"
idade = 40.9
professor = True
a = 1
b = -5
c = 6 
delta = (b**2 - 4*a*c)

if delta < 0:
    print("Não existem raízes reais")
elif delta == 0:
    x = -b / (2*a)
    print(f"A raiz da equação é: {x}")

def equacao2grau(a, b, c):
    x1 = -b + math.sqrt(b**2 - 4*a*c) / (2*a)
    return x1

def equacao2grau2(a, b, c):
    x2 = -b - math.sqrt(b**2 - 4*a*c) / (2*a)
    return x2


print(f"O resultado de x1 é: {equacao2grau(a, b, c)}")
print(f"O resultado de x2 é: {equacao2grau2(a, b, c)}")


# para importaer valores de variáveis ou funções dentro do Python, 
# devemos utilizar chaves {}

print(type(nome).__name__)

print(type(idade).__name__)
# códigos booleanos existem somente em duas condições, 
# "True" ou "False"
print(type(professor).__name__)

