# config.py – stałe do eksperymentu Flankera

# === Wygląd okna i bodźców ===
WIN_SIZE = [1280, 720]
BG_COLOR = 'white'

# === Czasy ===
FIXATION_DURATION = 0.5          # czas trwania krzyżyka fiksacyjnego (sekundy)
FEEDBACK_DURATION = 0.6          # czas wyświetlania informacji zwrotnej
MAX_RT = 2.5                     # maksymalny czas reakcji (sekundy)
PAUSE_DURATION_RANGE = (0.2, 0.5)  # losowa przerwa między próbami (jitter)

# === Klawisze sterujące ===
KEYS = {
    'left': 'z',
    'right': 'm'
}
EXIT_KEY = 'escape'

# === Bodźce ===
FLANKER_TYPES = ['zgodny', 'niezgodny', 'neutralny']
FLANKER_PROB = [0.4, 0.4, 0.2]  # prawdopodobieństwa wystąpienia

# === Liczba prób ===
TRAINING_TRIALS = 20
SESSION_TRIALS = 100
NUM_SESSIONS = 4

# === Inne ===
FINAL_SCREEN_DURATION = 4  # czas trwania ekranu końcowego (sekundy)
