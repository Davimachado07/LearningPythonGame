import pygame  # Importa a biblioteca pygame para criar jogos
import random  # Importa a biblioteca random para gerar números aleatórios
import sys  # Importa a biblioteca sys para sair do jogo

# Inicializa o Pygame
pygame.init()

# Configurações da tela
SCREEN_WIDTH = 1510  # Largura da tela
SCREEN_HEIGHT = 910  # Altura da tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Cria a tela do jogo
pygame.display.set_caption("Jogo de Plataforma")  # Define o título da janela do jogo

# Cores
WHITE = (255, 255, 255)  # Cor branca
BLACK = (0, 0, 0)  # Cor preta
RED = (255, 0, 0)  # Cor vermelha
GREEN = (0, 255, 0)  # Cor verde
BLUE = (0, 0, 255)  # Cor azul

# Carregar imagens
player_image = pygame.image.load("menino_skate.webp")  # Substitua pelo caminho da imagem do menino andando de skate
obstacle_image = pygame.image.load("hidrante.png")  # Substitua pelo caminho da imagem do hidrante
skate_park_image = pygame.image.load("pista-skate png.png")  # Substitua pelo caminho da imagem da pista de skate
background_image = pygame.image.load("imagem cidade.webp")  # Substitua pelo caminho da imagem do plano de fundo

# Função para ler a última pontuação e a melhor pontuação do arquivo
def read_scores():
    try:
        with open("scores.txt", "r") as file:
            scores = file.readlines()
            last_score = int(scores[0].strip())
            best_score = int(scores[1].strip())
            return last_score, best_score
    except:
        return 0, 0

# Função para salvar a última pontuação e a melhor pontuação no arquivo
def save_scores(last_score, best_score):
    with open("scores.txt", "w") as file:
        file.write(f"{last_score}\n{best_score}")

# Classe do Jogador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(player_image, (120, 120))  # Redimensiona a imagem para 120x120 pixels
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = SCREEN_HEIGHT - 100
        self.jump_speed = -30
        self.gravity = 1
        self.velocity_y = 0
        self.is_jumping = False

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not self.is_jumping:
            self.velocity_y = self.jump_speed
            self.is_jumping = True

        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        if self.rect.y >= SCREEN_HEIGHT - 100:
            self.rect.y = SCREEN_HEIGHT - 100
            self.is_jumping = False

# Classe dos Obstáculos
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.transform.scale(obstacle_image, (99, 99))  # Redimensiona a imagem para 70x70 pixels
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = SCREEN_HEIGHT - 100
        self.counted = False  # Adiciona um atributo para contar obstáculos pulados
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed
        if self.rect.x < -50:
            self.rect.x = SCREEN_WIDTH + random.randint(0, 100)
            self.counted = False  # Reseta o contador quando o obstáculo é reposicionado

# Função para desenhar o botão de voltar
def draw_back_button():
    font = pygame.font.Font(None, 36)
    text = font.render("Voltar", True, WHITE)
    button_rect = pygame.Rect(10, 10, 100, 50)
    pygame.draw.rect(screen, RED, button_rect)
    screen.blit(text, (20, 20))
    return button_rect

# Função para desenhar confetes
def draw_confetti():
    for _ in range(100):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        color = random.choice([RED, GREEN, BLUE])
        pygame.draw.circle(screen, color, (x, y), 5)

# Função principal do jogo
def main():
    clock = pygame.time.Clock()
    player = Player()
    obstacles = pygame.sprite.Group()

    initial_speed = 3  
    speed_increment = 0.01
    speed = initial_speed

    initial_distance = 200
    distance_increment = 1
    distance = initial_distance

    for _ in range(1):
        obstacle = Obstacle(speed)
        obstacle.rect.x += _ * distance  # Ajusta a posição inicial dos obstáculos
        obstacles.add(obstacle)

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(obstacles)

    start_time = pygame.time.get_ticks()
    obstacles_jumped = 0
    last_score, best_score = read_scores()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if draw_back_button().collidepoint(event.pos):
                    running = False

        all_sprites.update()

        screen.blit(background_image, (0, 0))  # Desenha o plano de fundo
        all_sprites.draw(screen)

        # Desenhar o botão de voltar
        draw_back_button()

        # Calcular o tempo de jogo
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
        font = pygame.font.Font(None, 36)
        time_text = font.render(f"Tempo: {elapsed_time:.2f}s", True, BLACK)
        screen.blit(time_text, (SCREEN_WIDTH - 200, 10))

        # Mostrar a contagem de obstáculos pulados
        obstacles_text = font.render(f"Obstáculos Pulados: {obstacles_jumped}", True, BLACK)
        screen.blit(obstacles_text, (SCREEN_WIDTH - 300, 50))

        # Mostrar a última pontuação
        last_score_text = font.render(f"Última Pontuação: {last_score}", True, BLACK)
        screen.blit(last_score_text, (SCREEN_WIDTH - 300, 90))

        # Mostrar a melhor pontuação
        best_score_text = font.render(f"Melhor Pontuação: {best_score}", True, BLACK)
        screen.blit(best_score_text, (SCREEN_WIDTH - 300, 130))

        pygame.display.flip()

        # Verificar colisão e contar obstáculos pulados
        if pygame.sprite.spritecollideany(player, obstacles):
            save_scores(obstacles_jumped, max(obstacles_jumped, best_score))
            running = False
        else:
            for obstacle in obstacles:
                if obstacle.rect.right < player.rect.left and not obstacle.counted:
                    obstacles_jumped += 1
                    obstacle.counted = True

        # Aumentar a velocidade dos obstáculos com o tempo
        speed += speed_increment
        for obstacle in obstacles:
            obstacle.speed = speed

        # Aumentar a distância entre os obstáculos com o tempo
        distance += distance_increment
        for i, obstacle in enumerate(obstacles):
            if obstacle.rect.x < -50:
                obstacle.rect.x = SCREEN_WIDTH + i * distance

        # Verificar se o jogador atingiu 100 pontos
        if obstacles_jumped >= 100:
            screen.fill(WHITE)
            screen.blit(skate_park_image, (0, 0))  # Desenha a imagem da pista de skate
            draw_confetti()  # Desenha confetes
            font = pygame.font.Font(None, 72)
            win_text = font.render("Você venceu!", True, RED)
            screen.blit(win_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 50))
            pygame.display.flip()
            pygame.time.wait(3000)  # Espera 3 segundos antes de fechar
            save_scores(obstacles_jumped, max(obstacles_jumped, best_score))
            running = False

        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()