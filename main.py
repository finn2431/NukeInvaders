import curses
import random
import time

# Spielfeldgröße
WIDTH = 30
HEIGHT = 20

# Spielerposition
player_pos = WIDTH // 2

# Schüsse
shot_symbol = "|"
shots = []

# Aliens
alien_symbol = [
    " /\\ ",
    "/[]\\",
    " /\\ ",
    "/__\\"
]
alien_height = len(alien_symbol)
alien_width = max(len(line) for line in alien_symbol)
aliens = [(random.randint(0, WIDTH - alien_width), 0)]

# Spieler
player_symbol = [
    "   A   ",
    "  / \\  ",
    " |---| ",
    " |   | "
]
player_height = len(player_symbol)
player_width = max(len(line) for line in player_symbol)

# Zähler für Alien-Bewegung
alien_move_counter = 0
ALIEN_MOVE_DELAY = 5  # Je höher der Wert, desto langsamer bewegen sich die Aliens

# Zähler für die Zeitsteuerung
last_time = time.time()

# Score
score = 0

# Bildschirm aktualisieren
def draw(screen):
    screen.clear()
    for x, y in shots:
        if 0 <= y < HEIGHT:
            screen.addch(y, x, shot_symbol)
    for x, y in aliens:
        if 0 <= y < HEIGHT - alien_height:
            for i, line in enumerate(alien_symbol):
                screen.addstr(y + i, x, line)
    for i, line in enumerate(player_symbol):
        screen.addstr(HEIGHT - player_height + i, player_pos, line)
    screen.addstr(0, 0, f'Score: {score}')
    screen.refresh()

# Schüsse bewegen
def move_shots():
    global shots
    shots = [(x, y - 1) for x, y in shots if y > 0]

# Aliens bewegen
def move_aliens():
    global aliens
    aliens = [(x, y + 1) for x, y in aliens if y < HEIGHT - alien_height]

# Kollisionen überprüfen
def check_collisions():
    global shots, aliens, score
    new_shots = []
    new_aliens = []

    for sx, sy in shots:
        hit = False
        for ax, ay in aliens:
            if ax <= sx < ax + alien_width and ay <= sy < ay + alien_height:
                hit = True
                score += 1  # Score erhöhen bei Kollision
                break
        if not hit:
            new_shots.append((sx, sy))

    for ax, ay in aliens:
        hit = False
        for sx, sy in shots:
            if ax <= sx < ax + alien_width and ay <= sy < ay + alien_height:
                hit = True
                break
        if not hit:
            new_aliens.append((ax, ay))

    shots = new_shots
    aliens = new_aliens

# Spielzustand überprüfen
def game_over():
    return any(y >= HEIGHT - alien_height for _, y in aliens)

def main(screen):
    global player_pos, alien_move_counter, last_time

    # Cursor deaktivieren
    curses.curs_set(0)

    # Nicht blockierend auf Eingaben warten
    screen.nodelay(True)

    while True:
        current_time = time.time()
        elapsed_time = current_time - last_time

        # Eingabe verarbeiten
        key = screen.getch()
        if key == curses.KEY_LEFT:
            player_pos = max(0, player_pos - 1)
        elif key == curses.KEY_RIGHT:
            player_pos = min(WIDTH - player_width, player_pos + 1)
        elif key == ord(' '):
            shots.append((player_pos + player_width // 2, HEIGHT - player_height - 1))

        # Spielmechanik
        move_shots()

        # Aliens nur bewegen, wenn der Zähler den festgelegten Wert erreicht hat
        if alien_move_counter >= ALIEN_MOVE_DELAY:
            move_aliens()
            alien_move_counter = 0
        else:
            alien_move_counter += 1

        check_collisions()

        # Neue Aliens erzeugen (Wahrscheinlichkeit weiter gesenkt)
        if random.random() < 0.02:  # 2% Wahrscheinlichkeit pro Frame
            aliens.append((random.randint(0, WIDTH - alien_width), 0))

        # Bildschirm zeichnen
        draw(screen)

        # Spielzustand überprüfen
        if game_over():
            screen.addstr(HEIGHT // 2, WIDTH // 2 - 5, "Game Over!")
            screen.refresh()
            time.sleep(2)
            break

        # Wartezeit an die vergangene Zeit anpassen
        if elapsed_time < 0.1:
            time.sleep(0.1 - elapsed_time)
        last_time = current_time

if __name__ == "__main__":
    curses.wrapper(main)

