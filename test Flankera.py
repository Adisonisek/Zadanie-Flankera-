# ======================
# Importy i biblioteki
# ======================
from psychopy import visual, event, core, gui
import random
import csv

# ======================
# Dane uczestnika
# ======================
info = {'ID': '', 'Czy nosisz okulary?': ['tak', 'nie']}
dlg = gui.DlgFromDict(info, title="Dane uczestnika")
if not dlg.OK:
    core.quit()

# ======================
# Stałe eksperymentu
# ======================
WIN_SIZE = [1440, 900]
BG_COLOR = [0.866, 0.866, 0.866]
FIXATION_DURATION = 0.8
FEEDBACK_DURATION = 2.0
MAX_RT = 4.0
KEYS = {'left': 'z', 'right': 'm'}
EXIT_KEY = 'f7'
FLANKER_TYPES = ['zgodny', 'niezgodny', 'neutralny']
FLANKER_PROB = [0.4, 0.4, 0.2]

# ======================
# Okno i bodźce
# ======================
win = visual.Window(WIN_SIZE, color=BG_COLOR, fullscr=False, units='height')
fixation = visual.TextStim(win, text='+', color='black', height=0.1)
feedback = visual.TextStim(win, text='', color='black', height=0.08)
instruction = visual.TextStim(win, text='', color='black', height=0.035, wrapWidth=1.5, pos=(0, 0.1))
stimulus = visual.TextStim(win, text='', color='black', height=0.1)
reminder = visual.TextStim(win, text='Z = "<"     M = ">"', pos=(0, -0.35), color='black', height=0.04)

# ======================
# Plik wynikowy
# ======================
filename = f"flanker_{info['ID']}.csv"
with open(filename, mode='w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['sesja', 'typ_bodzca', 'ciag', 'nr_proby', 'reakcja', 'poprawna', 'czas_reakcji(ms)', 'okulary'])

# ======================
# Generowanie listy prób
# ======================
def generuj_proby(n):
    """
    Generuje listę prób eksperymentu z określonym typem flankerów i kierunkiem.
    """
    proby = []
    for _ in range(n):
        flanker_type = random.choices(FLANKER_TYPES, weights=FLANKER_PROB)[0]
        direction = random.choice(['<', '>'])
        if flanker_type == 'zgodny':
            sequence = direction * 5
        elif flanker_type == 'niezgodny':
            flank = '>' if direction == '<' else '<'
            sequence = flank * 2 + direction + flank * 2
        else:
            sequence = '--' + direction + '--'
        proby.append((flanker_type, direction, sequence))
    return proby

# ======================
# Pojedyncza próba
# ======================
def wykonaj_probe(sesja, nr, flanker_type, direction, sequence, feedback_on=True):
    """
    Przeprowadza pojedynczą próbę eksperymentu.
    """
    # Fixation
    fixation.draw()
    win.flip()
    core.wait(FIXATION_DURATION)

    # Bodziec + przypomnienie
    stimulus.setText(sequence)
    stimulus.draw()
    reminder.draw()
    win.flip()

    clock = core.Clock()
    keys = event.waitKeys(maxWait=MAX_RT, keyList=list(KEYS.values()) + [EXIT_KEY], timeStamped=clock)

    # Ocena odpowiedzi
    if keys:
        key, rt = keys[0]
        if key == EXIT_KEY:
            core.quit()
        poprawna = (key == KEYS['left'] and direction == '<') or (key == KEYS['right'] and direction == '>')
    else:
        key, rt = 'brak', MAX_RT
        poprawna = False

    # Feedback bez przypomnienia
    if feedback_on:
        feedback.setText("dobrze" if poprawna else "żle")
        feedback.draw()
        win.flip()
        core.wait(FEEDBACK_DURATION)

    # Losowa przerwa (jitter)
    jitter = random.uniform(0.2, 0.5)
    win.flip()
    core.wait(jitter)

    # Zapis danych
    with open(filename, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([sesja, flanker_type, sequence, nr, key, poprawna, int(rt * 1000), info['Czy nosisz okulary?']])

# ======================
# Instrukcja
# ======================
text_intro = (
    "W zadaniu, ktore za chwile wykonasz, na ekranie beda pojawiac sie ciagi znakow.\n"
    "W srodku kazdego z nich znajdowac sie bedzie strzalka ('<' lub '>').\n"
    "Twoim zadaniem jest okreslenie kierunku tej srodkowej strzalki, ignorujac pozostale znaki.\n\n"
    "- Nacisnij klawisz Z, jesli widzisz strzalke w lewo ('<')\n"
    "- Nacisnij klawisz M, jesli widzisz strzalke w prawo ('>')\n\n"
    "Postaraj sie odpowiadac jak najszybciej i jak najdokladniej.\n"
    "Najpierw odbedzie sie sesja treningowa.\n\n"
    "Aby przejsc dalej, nacisnij spacje."
)
instruction.setText(text_intro)
instruction.draw()
win.flip()
event.waitKeys(keyList=['space'])

# ======================
# Trening
# ======================
instruction.setText("Trening (20 prob)\n\nNacisnij spacje, aby rozpoczac.")
instruction.draw()
reminder.draw()
win.flip()
event.waitKeys(keyList=['space'])

for i, (flanker_type, direction, sequence) in enumerate(generuj_proby(20), 1):
    wykonaj_probe("Trening", i, flanker_type, direction, sequence, feedback_on=True)

# ======================
# Sesje eksperymentalne
# ======================
for sesja_nr in range(1, 5):
    instruction.setText(
        f"Sesja {sesja_nr} (100 prob)\n\nUmiesc rece na klawiszach Z i M.\nSkup sie na znaku +.\n\nNacisnij spacje, aby rozpoczac."
    )
    instruction.draw()
    reminder.draw()
    win.flip()
    event.waitKeys(keyList=['space'])

    for i, (flanker_type, direction, sequence) in enumerate(generuj_proby(100), 1):
        wykonaj_probe(f"Sesja {sesja_nr}", i, flanker_type, direction, sequence, feedback_on=False)

    if sesja_nr < 4:
        instruction.setText("Przerwa.\n\nNacisnij spacje, aby kontynuowac.")
        instruction.draw()
        reminder.draw()
        win.flip()
        event.waitKeys(keyList=['space'])

# ======================
# Zakonączenie
# ======================
instruction.setText("To juz koniec eksperymentu.\nDziekujemy za udzial!")
instruction.draw()
win.flip()
core.wait(4)

win.close()
core.quit()
