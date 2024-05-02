import os
import random

import pygame
import requests

all_siti = []

try:
    os.mkdir('photo')
except Exception:
    pass


def get_info(siti):
    siti = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={siti}&format=json"
    response = requests.get(siti)
    if response:
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_pos = toponym["Point"]["pos"]
    else:
        return None
    return toponym_pos


def load_image(name_siti):
    map_file = name_siti
    all_siti.append(f"{name_siti}.png")
    cords = ','.join(get_info(name_siti).split())
    siti = f"https://static-maps.yandex.ru/1.x/?ll={cords}&spn=0.02,0.02&l={random.choice(['sat', 'map'])}"
    response = requests.get(siti)
    with open(f'photo/{name_siti}.png', 'wb') as file:
        file.write(response.content)


# ----------------------------------
# Вписать все города, которые будут показываться
siti = ['Москва', 'Ярославль', 'Санкт-Петербург', 'Сочи', 'Екатеринбург', 'Махачкала', 'Калининград', 'Казань', 'Уфа',
        'Самара', 'Магнитогорск', 'Владимир', 'Тула', 'Калуга', 'Набережные Челны', 'Белгород']
# ----------------------------------
for i in siti:
    load_image(i)


def main():
    this_siti = 0
    pygame.init()
    screen = pygame.display.set_mode((600, 500))
    screen.blit(pygame.image.load('photo/' + all_siti[this_siti]), (0, 0))
    pygame.display.flip()

    pygame.display.set_caption('Угадай название города')
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                last = this_siti
                this_siti = (this_siti + random.randint(1, 100)) % len(all_siti)
                while this_siti == last:
                    this_siti = (this_siti + random.randint(1, 100)) % len(all_siti)
                screen.blit(pygame.image.load('photo/' + all_siti[this_siti]), (0, 0))
                my_font = pygame.font.SysFont('Comic Sans MS', 30)
                text_surface = my_font.render(f'Предыдущий город: {siti[last]}', False, (0, 0, 255))
                screen.blit(text_surface, (0, 450))
                pygame.display.flip()
                screen.fill((0, 0, 0))
    pygame.quit()


if __name__ == '__main__':
    main()
