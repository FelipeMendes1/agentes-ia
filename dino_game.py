import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import pygame
import random
from agent_rule_based import RuleBasedAgent
from agent_rl import RLAgent
import numpy as np

# Inicializar o Pygame
pygame.init()
print("Pygame inicializado")

# Constantes do Jogo
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
BG_COLOR = (255, 255, 255)  # Cor de fundo

# Inicializar a tela do Pygame
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dino Game")
print("Janela do Pygame configurada")

# Carregar imagens com transparência e redimensioná-las
try:
    DINO_IMG = pygame.image.load(os.path.join("assets", "dino.png")).convert_alpha()
    DINO_IMG = pygame.transform.scale(DINO_IMG, (60, 80))
    print("Imagem do dinossauro carregada")

    CACTUS_IMG = pygame.image.load(os.path.join("assets", "cactus.png")).convert_alpha()
    CACTUS_IMG = pygame.transform.scale(CACTUS_IMG, (40, 60))
    print("Imagem do cacto carregada")

    BG_IMG = pygame.image.load(os.path.join("assets", "background.png")).convert()
    print("Imagem do fundo carregada")
except Exception as e:
    print(f"Erro ao carregar imagens: {e}")

# Fonte para exibição da pontuação
font = pygame.font.Font(None, 36)

# Classe Dinossauro
class Dino:
    def __init__(self):
        self.image = DINO_IMG
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = 50
        self.dino_rect.y = SCREEN_HEIGHT - 150  # Ajuste a posição y do dinossauro

        self.is_jumping = False
        self.jump_velocity = 8.5
        self.is_on_ground = True  # Nova variável para verificar se está no chão

    def update(self):
        if self.is_jumping:
            self.jump()

    def jump(self):
        if self.is_jumping:
            self.dino_rect.y -= self.jump_velocity * 4
            self.jump_velocity -= 0.8
            if self.jump_velocity < -8.5:
                self.dino_rect.y = SCREEN_HEIGHT - 150  # Reset y position to the ground level
                self.is_jumping = False
                self.jump_velocity = 8.5
                self.is_on_ground = True  # Define que está no chão ao finalizar o pulo

    def draw(self, screen):
        screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

# Classe Obstáculo
class Obstacle:
    def __init__(self):
        self.image = CACTUS_IMG
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = SCREEN_HEIGHT - 120  # Ajuste a posição y do cacto

    def update(self):
        self.rect.x -= 10
        if self.rect.x < -self.rect.width:
            self.rect.x = SCREEN_WIDTH

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

def main():
    global screen
    clock = pygame.time.Clock()
    running = True
    dino = Dino()
    obstacle = Obstacle()
    points = 0  # Variável de contagem de pontos
    print("Iniciando o loop principal")
    
    # Instanciar agentes
    rule_based_agent = RuleBasedAgent()
    rl_agent = RLAgent()
    use_rl_agent = False  # Mudar para True para usar o agente de aprendizado por reforço
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not dino.is_jumping and dino.is_on_ground:
                    dino.is_jumping = True
                    dino.is_on_ground = False  # Define que não está mais no chão

        dino.update()
        obstacle.update()

        # Incrementar pontos quando o Dino passar pelo cacto
        if obstacle.rect.x + obstacle.rect.width < dino.dino_rect.x:
            points += 1
            obstacle.rect.x = SCREEN_WIDTH  # Reiniciar o obstáculo

        # Ações do agente
        state = np.array([dino.dino_rect.x, dino.dino_rect.y, obstacle.rect.x, obstacle.rect.y])
        if use_rl_agent:
            action = rl_agent.get_action(state)
            if action == 1 and not dino.is_jumping and dino.is_on_ground:
                dino.is_jumping = True
                dino.is_on_ground = False  # Define que não está mais no chão
        else:
            action = rule_based_agent.get_action(dino, obstacle)
            if action == "jump" and not dino.is_jumping and dino.is_on_ground:
                dino.is_jumping = True
                dino.is_on_ground = False  # Define que não está mais no chão

        screen.fill(BG_COLOR)
        screen.blit(BG_IMG, (0, 0))
        dino.draw(screen)
        obstacle.draw(screen)
        
        # Desenhar a pontuação
        points_text = font.render(f"Points: {points}", True, (0, 0, 0))
        screen.blit(points_text, (SCREEN_WIDTH - 150, 10))

        pygame.display.update()
        clock.tick(30)
        print("Loop principal executado")

    pygame.quit()
    print("Pygame encerrado")

if __name__ == "__main__":
    main()
