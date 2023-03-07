import pygame #Criação de Jogos
import os #Integrar arquivos do computador
import random #Gerar números aleatórios

tela_largura = 500
tela_altura = 800

imagem_cano = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png'))) #colocar a imagem que está dentro da pasta imgs em uma scala maior
imagem_chao = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png'))) #colocar a imagem que está dentro da pasta imgs em uma scala maior
imagem_fundo = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png'))) #colocar a imagem que está dentro da pasta imgs em uma scala maior
imagens_passaro = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png')))
]

#Texto da marcação das pontuações
pygame.font.init() #Inicializar a fonte
fonte_pontos = pygame.font.SysFont('arial', 50) #Fonte arial, tamanho 50



class Passaro:
    imagens = imagens_passaro #Imagens do pássaro

    #Para animação da rotação
    rotacao_max = 25
    velacidade_rotacao = 20
    tempo_animacao = 5

    def __init__(self, x, y):
        self.x = x #Posição do passaro em x
        self.y = y #Posição do passaro em y
        self.angulo = 0 #Começa reto
        self.velocidade = 0 #Começa com velocidade 0 (velocidade de cima pra baixo que é como ele se movimenta)
        self.altura = self.y
        self.tempo = 0 #Animação do cair do passaro para ser uma parábola
        self.contagem_imagem = 0 #Para saber qual imagem usar no momento
        self.imagem = self.imgs[0] #Começa com a imagem bird1

    def pular(self):
        self.velocidade = -10.5 #Pra poder subir
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        #Calculando o deslocamento do passaro
        self.tempo += 1
        deslocamento = 1.5 * (self.tempo**2) + self.velocidade * self.tempo #1.5 foi um valor que ficou bom - (** é elevado) - isso é uma fórmula de tempo

        #Restringindo o deslocamento na tela
        if deslocamento > 16:
            deslocamento = 16

        elif deslocamento < 0:
            deslocamento -= 2

        self.y += deslocamento #Mexe o y dele conforme deslocamento

        #Mexer o angulo do passaro
        if deslocamento < 0 or self.y < (self.altura + 50): #Se o passaro está se deslocando para cima (< 0) ou ainda acima de 50 no y, é para ele ficar de bico pra cima
            if self.angulo < self.rotacao_max:
                self.angulo = self.rotacao_max
        else:
            if self.angulo > - 90:
                self.angulo -= self.velacidade_rotacao

    def desenhar(self, tela):
        #Definir qual imagem vai usar (movimento de batida de asa)
        self.contagem_imagem += 1

        if self.contagem_imagem < self.tempo_animacao:
            self.imagem = self.imgs[0]
        elif self.contagem_imagem < self.tempo_animacao * 2:
            self.imgs[1]
        elif self.contagem_imagem < self.tempo_animacao * 3:
            self.imgs[2]
        elif self.contagem_imagem < self.tempo_animacao * 4:
            self.imgs[1]
        elif self.contagem_imagem < self.tempo_animacao * 4 + 1:
            self.imgs[0]
            self.contagem_imagem = 0

        #Pássaro caindo (asa não bate)
        if self.angulo <= - 80:
            self.imagem = self.imgs[1] # imagem parada
            self.contagem_imagem = self.tempo_animacao * 2 # Para a próxima batida de asa vai ser a imagem 2 que é a batida pra baixo

        #Desenhar Imagem
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        posicao_centro_imagem = self.imagem.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=posicao_centro_imagem)
        tela.blit(imagem_rotacionada, retangulo.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.imagem) # Separar em quadradinhos menores pra ver se o mesmo pixels do passaro bate com o do cano (pra ver se bateu)



class Cano:
    distancia = 200 # distancia entre o cano de cima e de baixo
    velocidade = 5 # andar de 5 em 5

    def __init__(self, x): #Apenas a posição x, pq a altura(y) será gerada aleatoriamente
        self.x = x
        self.altura = 0 #inicial
        self.posicao_topo = 0 #inicial
        self.posicao_base = 0 #inicial
        self.imagem_cano_topo = pygame.transform.flip(imagem_cano, False, True) #false eixo x e true eixo y (de ponta cabeca)
        self.imagem_cano_base = imagem_cano
        self.passou = False #pra ver se o passaro já passou do cano
        self.definir_altura()

    def definir_altura(self):
        self.altura = random.randrange(50, 450) # Pra não deixar o cano ser muito lá em cima e nem muito lá em baixo
        self.posicao_topo = self.altura - self.imagem_cano_topo.get_height() #Do ponto do cano de cima até o começo da tela
        self.posicao_base = self.altura + self.distancia #Onde ficou o cano de cima mais a distancia (passagem)

    def mover(self):
        self.x -= self.velocidade #Movendo o cano para trás

    def desenhar(self, tela):
        tela.blit(self.imagem_cano_topo, (self.x, self.posicao_topo))
        tela.blit(self.imagem_cano_base, (self.x, self.posicao_base))

    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.imagem_cano_topo)
        base_mask = pygame.mask.from_surface(self.imagem_cano_base)

        distancia_topo = (self.x - passaro.x, self.posicao_topo - round(passaro.y)) #round é para arredondar para numero inteiro
        distancia_base = (self.x - passaro.x, self.posicao_base - round(passaro.y))  # round é para arredondar para numero inteiro
        topo_ponto_colisao = passaro_mask.overlap(base_mask, distancia_topo)  # Pra ver se tem dois pontos iguais, ou seja, bateu
        base_ponto_colisao = passaro_mask.overlap(base_mask, distancia_base) #Pra ver se tem dois pontos iguais, ou seja, bateu

        if base_ponto_colisao or topo_ponto_colisao: #se um desses dois for verdadeiro (acontecer)
            return True
        else:
            return False


class Chao:
    velocidade = 5 #mesma do cano
    largura = imagem_chao.get_width()
    imagem = imagem_chao

    def __init__(self, y):
        self.y = y
        self.x1 = 0 #x1 = imagem chao 1 / x2, imagem chao
        self.x2 = self.largura

    def mover(self):
        self.x1 -= self.velocidade
        self.x2 -= self.velocidade

        if self.x1 + self.largura < 0: #Se a imagem saiu da tela
            self.x1 = self.x2 + self.largura #Manda a primeira imagem pra trás

        if self.x2 + self.largura < 0:
            self.x2 = self.x1 + self.largura

    def desenhar(self, tela):
        tela.blit(self.imagem, (self.x1, self.y))
        tela.blit(self.imagem, (self.x2, self.y))


def desenhar_tela(tela, passaros, canos, chao, pontos):
    tela.blit(imagem_fundo, (0, 0)) #desenhando o fundo da tela. Posicao zero, pq ela pega a tela inteira

    for passaro in passaros:
        passaro.desenhar(tela) #com vários pássaros, apenas pra usar a IA e ajudar a zerar o jogo, assim ele pode fazer com vários pássaros de uma vez

    for cano in canos:
        cano.desenhar(tela)

    texto = fonte_pontos.render(f"Pontuação: {pontos}", 1, (255, 255, 255)) #parametro 1 pra deixar o texto certo e não ruim na tela pra ler e da cor branca(RGB)
    tela.blit(texto, (tela_largura - 10 - texto.get_width(), 10)) #tamanho da tela, menos um espaço de 10 - o espaço do texto
    chao.desenhar(tela)

    pygame.display.update()



def main():
    passaros = [Passaro(230, 350)] #[passaro] = instancia da classe com posicao x e y conforme pede na classe
    chao = Chao(730)
    canos = [Cano(700)]
    tela = pygame.display.set_mode((tela_largura, tela_altura)) #criando a tela
    pontos = 0 #começa com pontuação igual a zero
    relogio = pygame.time.clock() #relogio interno do jogo


    rodando = True
    while rodando: #enquanto rodando for true...
        relogio.tick(30) #30 frames ou FPS por segundo que vai ficar rodando

        #Interação com usuário
        for evento in pygame.event.get(): #Ele consegue conhecer os eventos que estao acontecendo, por ex: clicar, apertar espaço, etc
            if evento.type == pygame.QUIT: #Se clicar no x
                rodando = False
                pygame.quit() #fecha o jogo
                quit()#fecha o python
            if evento.type == pygame.KEYDOWN: #Se alguma tecla do teclado foi apertada
                if evento.key == pygame.K_SPACE: #Se a tecla for o espaço
                    for passaro in passaros: #se não for varios passaros, um só ta bom (sem o for)
                        passaro.pular()

        #Mover objetos na tela
        for passaro in passaros:
            passaro.mover()
        chao.mover()

        adicionar_cano = False
        remover_canos = []

        for cano in canos:
            for i, passaro in enumerate(passaros): #pegar a posicao do passaro dentro da lista
                if cano.colidir(passaro): #se o passaro bater com o cano
                    passaros.pop(i) #excluir o passaro
                if not cano.passou and passaro.x > cano.x: #se a variavel passou é falsa e o x do passaro for maior que o x do cano, quer dizer que o passaro ainda passou do cano
                    cano.passou = True
                    adicionar_cano = True
                cano.mover()

                if cano.x + cano.imagem_cano_topo.get_wodth() < 0: #ver se o cano ainda vai aparecer na tela
                    remover_canos.append(cano)
        if adicionar_cano: #se adicionar_cano for verdadeiro
            pontos += 1
            cano.append(Cano(600)) #adiciona uma instancia da classe Cano comecando na posicao y = 600

        for cano in remover_canos:
            canos.remove(cano)

        for i, passaro in enumerate(passaros):
            if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
                passaros.pop(i)

        desenhar_tela(tela, passaros, canos, chao, pontos)

if __name__ == '__main__': #Se executar esse arquivo python, ele executa essa funcao - essa parte é sempre assim, independente do nome da funcao princial
    main() #nome da funcao principal
