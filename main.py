import pygame
import os
import pygame_gui
import random

pygame.init()
pygame.mixer.init()  # Инициализация микшера для звука

# Настройки экрана
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Blackjack Game")

# Инициализация менеджера ресурсов Pygame GUI
manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))

# Функция для подсчета очков карты
def get_card_value(card_name):
    value = card_name.split('_')[0]  # Извлекаем значение из имени карты
    if value in ['J', 'Q', 'K']:
        return 10
    elif value == 'A':
        return 1  # Туз считается как 1 очко
    else:
        return int(value)  # Цифровые карты возвращают свое значение

# Загрузка изображений карт
def load_card_images(image_path):
    card_images = {}
    suits = ['hearts', 'diamonds', 'clubs', 'spades']
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    for suit in suits:
        for value in values:
            image_name = f"{value}_of_{suit}.png"
            image_file = os.path.join(image_path, image_name)
            try:
                card_images[f"{value}_of_{suit}"] = pygame.image.load(image_file).convert_alpha()
            except FileNotFoundError:
                print(f"File not found: {image_file}")
    # Загрузка изображения для обратной стороны карты
    back_image_name = "back.png"
    back_image_file = os.path.join(image_path, back_image_name)
    try:
        card_images["back"] = pygame.image.load(back_image_file).convert_alpha()
    except FileNotFoundError:
        print(f"File not found: {back_image_file}")
    return card_images

# Загрузка звуковых файлов
image_folder = r'C:\Users\admin\PycharmProjects\pythonProject\img'  # Измените этот путь
click_sound = pygame.mixer.Sound(os.path.join(image_folder, 'card-sounds-35956.mp3'))
win_sound = pygame.mixer.Sound(os.path.join(image_folder, 'win.mp3'))
lose_sound = pygame.mixer.Sound(os.path.join(image_folder, 'lose.mp3'))
draw_sound = pygame.mixer.Sound(os.path.join(image_folder, 'draw.mp3'))

# Пример использования
card_images = load_card_images(image_folder)

# Функция для отрисовки карты на экране
def draw_card(card_name, position, size=(SCREEN_WIDTH // 6, SCREEN_HEIGHT // 3)):
    card_image = card_images.get(card_name)
    if card_image:
        card_image = pygame.transform.scale(card_image, size)
        screen.blit(card_image, position)
    else:
        print(f"Card {card_name} not found.")

# Функция для отображения текста на экране
def draw_text(text, font_size, color, position):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=position)
    screen.blit(text_surface, text_rect)

# Кнопка "Start"
start_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((SCREEN_WIDTH - 200) // 2, (SCREEN_HEIGHT + 100) // 2, 200, 50),
    text="Start",
    manager=manager
)
start_button.shape_corner_radius = 10
start_button.colours['normal_text'] = pygame.Color("black")
start_button.colours['normal_bg'] = pygame.Color("white")

# Кнопка "Restart"
restart_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(20, SCREEN_HEIGHT - 70, 150, 50),
    text="Restart",
    manager=manager
)
restart_button.shape_corner_radius = 10
restart_button.colours['normal_text'] = pygame.Color("black")
restart_button.colours['normal_bg'] = pygame.Color("white")

# Переменные состояния игры
game_started = False
game_over = False
bottom_card_clicked = False
one_pressed = False
two_pressed = False
three_pressed = False
bottom_card = None
adjacent_bottom_card = None
second_adjacent_bottom_card = None
third_adjacent_bottom_card = None
player_score = 0
dealer_cards = []
dealer_score = 0
dealer_turn = False

# Функция для автоматической раздачи карт дилеру
def dealer_draw_cards():
    global dealer_score, dealer_cards  # Используем глобальные переменные
    while dealer_score < 17:  # Дилер берет карты, пока его счет меньше 17
        selected_card = random.choice(list(card_images.keys()))
        if selected_card != 'back':  # Игнорируем карту задней стороны
            dealer_cards.append(selected_card)
            dealer_score += get_card_value(selected_card)
            if dealer_score >= 17:  # Прекращаем раздачу, если достигли 17 или более
                break

# Основной игровой цикл
running = True
clock = pygame.time.Clock()
while running:
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        manager.process_events(event)
        if event.type == pygame.USEREVENT and event.ui_element == start_button:
            start_button.hide()
            game_started = True
        if event.type == pygame.MOUSEBUTTONDOWN and not bottom_card_clicked:
            mouse_pos = event.pos
            if 0 <= mouse_pos[0] <= SCREEN_WIDTH // 6 and (SCREEN_HEIGHT - SCREEN_HEIGHT // 3) // 2 <= mouse_pos[1] <= (SCREEN_HEIGHT + SCREEN_HEIGHT // 3) // 2:
                click_sound.play()  # Воспроизведение звука нажатия
                cards_list = list(card_images.keys())
                cards_list.remove('back')  # Удаление 'back', чтобы она не выбиралась случайно
                selected_card = random.choice(cards_list)
                bottom_card = selected_card
                player_score += get_card_value(selected_card)  # Обновляем счет игрока
                bottom_card_clicked = True  # Предотвращаем повторное нажатие
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1 and not one_pressed:
                cards_list = list(card_images.keys())
                cards_list.remove('back')  # Убедитесь, что 'back' не выбирается
                selected_card = random.choice(cards_list)
                adjacent_bottom_card = selected_card
                click_sound.play()  # Воспроизведение звука нажатия
                player_score += get_card_value(selected_card)  # Обновляем счет игрока
                one_pressed = True  # Предотвращаем повторное нажатие
            elif event.key == pygame.K_2 and not two_pressed:
                cards_list = list(card_images.keys())
                cards_list.remove('back')
                selected_card = random.choice(cards_list)
                second_adjacent_bottom_card = selected_card
                click_sound.play()
                player_score += get_card_value(selected_card)
                two_pressed = True  # Предотвращаем повторное нажатие
            elif event.key == pygame.K_3 and not three_pressed:
                cards_list = list(card_images.keys())
                cards_list.remove('back')
                selected_card = random.choice(cards_list)
                third_adjacent_bottom_card = selected_card
                click_sound.play()
                player_score += get_card_value(selected_card)
                three_pressed = True  # Предотвращаем повторное нажатие
            if event.key == pygame.K_SPACE and not dealer_turn:  # Используйте пробел для начала хода дилера
                dealer_turn = True
                dealer_draw_cards()
            if event.key == pygame.K_0 and not dealer_turn:  # Нажмите 0, чтобы завершить ход игрока
                dealer_turn = True
                dealer_draw_cards()
                pygame.time.wait(1000)  # Подождите 1 секунду перед проверкой результатов
                # Определение победителя и отображение результата
                game_over = True
                if player_score > 21:
                    game_result_text = "Dealer Wins!"
                    game_result_color = pygame.Color('red')
                    lose_sound.play()  # Воспроизводим звук проигрыша
                elif dealer_score > 21:
                    game_result_text = "Player Wins!"
                    game_result_color = pygame.Color('green')
                    win_sound.play()  # Воспроизводим звук выигрыша
                elif abs(21 - player_score) < abs(21 - dealer_score):
                    game_result_text = "Player Wins!"
                    game_result_color = pygame.Color('green')
                    win_sound.play()  # Воспроизводим звук выигрыша
                elif abs(21 - player_score) > abs(21 - dealer_score):
                    game_result_text = "Dealer Wins!"
                    game_result_color = pygame.Color('red')
                    lose_sound.play()  # Воспроизводим звук проигрыша
                else:
                    game_result_text = "It's a Tie!"
                    game_result_color = pygame.Color('yellow')
                    draw_sound.play()  # Воспроизводим звук ничьи
        if game_over and event.type == pygame.MOUSEBUTTONDOWN and restart_button.rect.collidepoint(event.pos):
            # Сброс переменных игры для перезапуска
            game_started = False
            game_over = False
            bottom_card_clicked = False
            one_pressed = False
            two_pressed = False
            three_pressed = False
            bottom_card = None
            adjacent_bottom_card = None
            second_adjacent_bottom_card = None
            third_adjacent_bottom_card = None
            player_score = 0
            dealer_cards = []
            dealer_score = 0
            dealer_turn = False

    # Очистка экрана и отрисовка элементов
    screen.fill((0, 122, 0))  # Зеленый фон стола
    manager.update(time_delta)
    manager.draw_ui(screen)

    if game_started:
        draw_card('back', (0, (SCREEN_HEIGHT - SCREEN_HEIGHT // 3) // 2), size=(SCREEN_WIDTH // 6, SCREEN_HEIGHT // 3))
        if bottom_card:
            draw_card(bottom_card, ((SCREEN_WIDTH - SCREEN_WIDTH // 6) // 2, SCREEN_HEIGHT * 5 // 6 - SCREEN_HEIGHT // 6), size=(SCREEN_WIDTH // 6, SCREEN_HEIGHT // 3))
        if adjacent_bottom_card:
            draw_card(adjacent_bottom_card, ((SCREEN_WIDTH - SCREEN_WIDTH // 6) // 2 + SCREEN_WIDTH // 6 + 20, SCREEN_HEIGHT * 5 // 6 - SCREEN_HEIGHT // 6), size=(SCREEN_WIDTH // 6, SCREEN_HEIGHT // 3))
        if second_adjacent_bottom_card:
            draw_card(second_adjacent_bottom_card, ((SCREEN_WIDTH - SCREEN_WIDTH // 6) // 2 + 2 * (SCREEN_WIDTH // 6 + 20), SCREEN_HEIGHT * 5 // 6 - SCREEN_HEIGHT // 6), size=(SCREEN_WIDTH // 6, SCREEN_HEIGHT // 3))
        if third_adjacent_bottom_card:
            draw_card(third_adjacent_bottom_card, ((SCREEN_WIDTH - SCREEN_WIDTH // 6) // 2 - SCREEN_WIDTH // 6 - 20, SCREEN_HEIGHT * 5 // 6 - SCREEN_HEIGHT // 6), size=(SCREEN_WIDTH // 6, SCREEN_HEIGHT // 3))

    # Отображаем счет игрока
    font = pygame.font.Font(None, 36)  # Вы можете выбрать другой шрифт или размер
    score_text = font.render(f'Player Score: {player_score}', True, pygame.Color('white'))
    screen.blit(score_text, (50, 50))  # Позиционируем счет в левом верхнем углу

    # Отображение карт и счета дилера, если его ход начался
    if dealer_turn:
        y_offset = 50  # Начальное смещение для карт дилера
        for card in dealer_cards:
            draw_card(card, (SCREEN_WIDTH - 150, y_offset), size=(SCREEN_WIDTH // 10, SCREEN_HEIGHT // 5))
            y_offset += 30  # Смещаем каждую следующую карту дилера вниз
        # Отображаем счет дилера
        dealer_score_text = font.render(f'Dealer Score: {dealer_score}', True, pygame.Color('white'))
        dealer_score_rect = dealer_score_text.get_rect()
        dealer_score_rect.topleft = (50, 10)
        screen.blit(dealer_score_text, dealer_score_rect)

    # Отображение результата игры
    if game_over:
        draw_text(game_result_text, 50, game_result_color, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    pygame.display.flip()

pygame.quit()

