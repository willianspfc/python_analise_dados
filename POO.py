class Carro:
    def __init__(self,modelo,cor):
        # atributos do carro
        self.modelo = modelo
        self.cor = cor
        self.velocidade = 0 # o carro começa parado

    def acelerar(self,incremento):
        self.velocidade += incremento
        print (f'O {self.modelo} acelerou para{self.velocidade}km/h')

    def desacelerar(self,decremento):
        self.velocidade -= decremento
        print (f'O {self.modelo} desacelerou para{self.velocidade}km/h')

    def parar(self):
        self.velocidade = 0
        print (f'O {self.modelo} parou')

    def reduzir_velocidade(self,reducao):
        while self.velocidade > 0 :
            self.velocidade -= reducao
            print(f'O {self.modelo} reduziu para {self.velocidade}km/h')
        print(f'O {self.modelo} está parado')

#criar o objeto carro
meu_carro = Carro('Fusca','Amarelo')
outro_carro = Carro('Uno','Laranja')

# Usar os metodos:
meu_carro.acelerar(20)
meu_carro.acelerar(40)
outro_carro.acelerar(60)
meu_carro.desacelerar(30)
meu_carro.parar()

outro_carro.reduzir_velocidade(reducao=10)