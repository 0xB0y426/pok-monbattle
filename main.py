import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 400
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pokemon Battle")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

background_img = pygame.image.load("wall.png")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

pokemon_images = {
    "Pikachu": pygame.image.load("pokemon1.png"),
    "Charmander": pygame.image.load("pokemon2.png"),
    "Charizard": pygame.image.load("charizard.png")
}

for key in pokemon_images:
    pokemon_images[key] = pygame.transform.scale(pokemon_images[key], (150, 150))

class Pokemon:
    def __init__(self, name, health, attack, img, x, y, special_attack_name, special_attack_damage):
        self.name = name
        self.max_health = health
        self.health = health
        self.attack = attack
        self.img = img
        self.x = x
        self.y = y
        self.special_attack_name = special_attack_name
        self.special_attack_damage = special_attack_damage

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))
        health_bar_width = 150
        health_bar = health_bar_width * (self.health / self.max_health)
        pygame.draw.rect(win, RED, (self.x, self.y - 20, health_bar_width, 10))
        pygame.draw.rect(win, GREEN, (self.x, self.y - 20, health_bar, 10))
        pygame.draw.rect(win, BLACK, (self.x, self.y - 20, health_bar_width, 10), 2)

        font = pygame.font.SysFont("comicsans", 20)
        color = YELLOW if self.name == "Pikachu" else ORANGE
        name_text = font.render(f"{self.name}", True, color)
        win.blit(name_text, (self.x + (150 - name_text.get_width()) // 2, self.y - 40))

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def special_attack(self, enemy):
        damage = self.special_attack_damage + random.randint(0, 10)
        enemy.take_damage(damage)
        return damage

def display_attack_effect(win, x, y):
    for _ in range(15):
        rand_x = x + random.randint(-20, 20)
        rand_y = y + random.randint(-20, 20)
        size = random.randint(5, 10)
        pygame.draw.circle(win, YELLOW, (rand_x, rand_y), size)
    pygame.display.update()
    pygame.time.delay(100)

def explode(win, x, y):
    pygame.draw.circle(win, (255, 165, 0), (x, y), 40)
    pygame.draw.circle(win, (255, 0, 0), (x, y), 30)
    pygame.draw.circle(win, (255, 255, 0), (x, y), 20)
    pygame.display.update()
    pygame.time.delay(150)

def draw_text(win, text, x, y):
    font = pygame.font.SysFont("comicsans", 28)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(x, y))

    shadow_surface = font.render(text, True, PURPLE)
    win.blit(shadow_surface, (text_rect.x + 2, text_rect.y + 2))

    win.blit(text_surface, text_rect)

def game_loop():
    clock = pygame.time.Clock()
    running = True

    pokemon_names = list(pokemon_images.keys())
    selected_pokemons = random.sample(pokemon_names, 2)

    pokemon1 = Pokemon(
        selected_pokemons[0], 100, 10, pokemon_images[selected_pokemons[0]], 50, HEIGHT // 2, 
        "Relâmpago" if selected_pokemons[0] == "Pikachu" else "Fogo Cruzado", 20
    )
    pokemon2 = Pokemon(
        selected_pokemons[1], 100, 10, pokemon_images[selected_pokemons[1]], WIDTH - 200, HEIGHT // 2, 
        "Relâmpago" if selected_pokemons[1] == "Pikachu" else "Fogo Cruzado", 25
    )

    attack_message = ""
    turn = 1

    while running:
        clock.tick(30)
        win.blit(background_img, (0, 0))

        pokemon1.draw(win)
        pokemon2.draw(win)

        draw_text(win, attack_message, WIDTH // 2, 50)

        pygame.display.update()

        if pokemon1.health <= 0 or pokemon2.health <= 0:
            winner = pokemon1.name if pokemon1.health > 0 else pokemon2.name
            win.blit(background_img, (0, 0))
            draw_text(win, f"{winner} venceu!", WIDTH // 2, HEIGHT // 2)
            pygame.display.update()
            pygame.time.delay(3000)
            running = False
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if turn == 1:
                        explode(win, pokemon2.x + 75, pokemon2.y + 75)
                        display_attack_effect(win, pokemon2.x + 75, pokemon2.y + 75)
                        
                        damage = pokemon1.special_attack(pokemon2)
                        attack_message = f"{pokemon1.name} usa {pokemon1.special_attack_name} e causa {damage} de dano!"
                        turn = -1
                    else:
                        explode(win, pokemon1.x + 75, pokemon1.y + 75)
                        display_attack_effect(win, pokemon1.x + 75, pokemon1.y + 75)

                        damage = pokemon2.special_attack(pokemon1)
                        attack_message = f"{pokemon2.name} usa {pokemon2.special_attack_name} e causa {damage} de dano!"
                        turn = 1

    pygame.quit()

game_loop()
