from pygame import *
import socket
import json
from threading import Thread
from menu import ConnectWindow

# --- Ініціалізація звуку ---
mixer.init()

# --- Вікно підключення ---
win = ConnectWindow()
win.mainloop()

host = win.host
port = win.port

# --- PYGAME НАЛАШТУВАННЯ ---
WIDTH, HEIGHT = 800, 600
init()
screen = display.set_mode((WIDTH, HEIGHT))
clock = time.Clock()
display.set_caption("Пінг-Понг")

# --- СЕРВЕР ---
def connect_to_server():
    while True:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((host, port))
            buffer = ""
            game_state = {}
            my_id = int(client.recv(24).decode())
            return my_id, game_state, buffer, client
        except:
            pass

def receive():
    global buffer, game_state, game_over
    while not game_over:
        try:
            data = client.recv(1024).decode()
            buffer += data
            while "\n" in buffer:
                packet, buffer = buffer.split("\n", 1)
                if packet.strip():
                    game_state = json.loads(packet)
        except:
            game_state["winner"] = -1
            break

# --- ШРИФТИ ---
font_win = font.Font(None, 72)
font_main = font.Font(None, 36)

# --- ЗОБРАЖЕННЯ ---
tennis_paddle_green = image.load("image/tennis_paddle_green.png")
tennis_paddle_green = transform.scale(tennis_paddle_green, (20, 100))
tennis_paddle = image.load("image/tennis_paddle.png")
tennis_paddle = transform.scale(tennis_paddle, (20, 100))
tennis_ball = image.load("image/tennis_ball.png")
tennis_ball = transform.scale(tennis_ball, (20, 20))
image_bg = image.load("image/table_tennis.png")
image_bg = transform.scale(image_bg, (WIDTH, HEIGHT))

# --- ЗВУКИ ---
mixer.music.load("music/tennis_misic.mp3")
bouncing_the_ball = mixer.Sound("music/tennis_ball_mus.wav")
bouncing_the_ball.set_volume(1)
bouncing_a_ball_off_a_wall = mixer.Sound("music/wall.wav")
bouncing_a_ball_off_a_wall.set_volume(1)
winner_sound = mixer.Sound("music/win.wav")
winner_sound.set_volume(1)
loser_sound = mixer.Sound("music/lose.wav")
loser_sound.set_volume(1)


music_playing = False

# --- ГРА ---
game_over = False
winner = None
you_winner = None
my_id, game_state, buffer, client = connect_to_server()
Thread(target=receive, daemon=True).start()

while True:
    for e in event.get():
        if e.type == QUIT:
            exit()

    if not music_playing:
        mixer.music.play(-1)
        music_playing = True

    if "countdown" in game_state and game_state["countdown"] > 0:
        if music_playing:
            mixer.music.stop()
            music_playing = False

        screen.fill((0, 0, 0))
        countdown_text = font.Font(None, 72).render(str(game_state["countdown"]), True, (255, 255, 255))
        screen.blit(countdown_text, (WIDTH // 2 - 20, HEIGHT // 2 - 30))
        display.update()
        continue

    if "winner" in game_state and game_state["winner"] is not None:
        if not music_playing:
            mixer.music.play(-1)
            music_playing = True

        screen.fill((20, 20, 20))
        if you_winner is None:
            if game_state["winner"] == my_id:
                you_winner = True
                winner_sound.play()
            else:
                you_winner = False
                loser_sound.play()

        if you_winner:
            text = "Ти переміг!"
        else:
            text = "Пощастить наступним разом!"

        win_text = font_win.render(text, True, (255, 215, 0))
        text_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(win_text, text_rect)

        text = font_win.render('К - рестарт', True, (255, 215, 0))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 120))
        screen.blit(text, text_rect)

        display.update()
        continue

    if game_state:
        if music_playing:
            mixer.music.stop()
            music_playing = False

        screen.blit(image_bg, (0, 0))
        screen.blit(tennis_paddle, (20, game_state['paddles']['0']))
        screen.blit(tennis_paddle_green, (WIDTH - 40, game_state['paddles']['1']))
        screen.blit(tennis_ball, (game_state['ball']['x'] - 10, game_state['ball']['y'] - 10))
        score_text = font_main.render(f"{game_state['scores'][0]} : {game_state['scores'][1]}", True, (255, 255, 255))
        screen.blit(score_text, (WIDTH // 2 - 25, 20))

        if game_state['sound_event']:
            if game_state['sound_event'] == 'wall_hit':
                bouncing_a_ball_off_a_wall.play()
            if game_state['sound_event'] == 'platform_hit':
                bouncing_the_ball.play()
    else:
        # Відображення тексту "Очікування гравців..." в режимі очікування
        waiting_text = font_main.render(f"Очікування гравців...", True, (255, 255, 255))
        screen.blit(waiting_text, (WIDTH // 2 - 25, 20))

    display.update()
    clock.tick(60)

    keys = key.get_pressed()
    if keys[K_w]:
        client.send(b"UP")
    elif keys[K_s]:
        client.send(b"DOWN")
