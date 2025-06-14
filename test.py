from psychopy import visual, event, core, gui
import random
import csv


Dane uczestnika
info = {'ID': '', 'Czy nosisz okulary?': ['tak', 'nie']}
dlg = gui.DlgFromDict(info, title="Dane uczestnika")
if not dlg.OK:
    core.quit()


Ustawienia
WIN_SIZE = [1440, 900] #rozmiar standardowego ekranu dla MacBooka
BG_COLOR = [0.866, 0.866, 0.866]
FIXATION_DURATION = 0.8
FEEDBACK_DURATION = 2.0
PAUSE_DURATION = 0.8
MAX_RT = 4.0

KEYS = {'left': 'z', 'right': 'm'}
EXIT_KEY = 'f7' #kod awaryjny, wyłacza program
FLANKER_TYPES = ['zgodny', 'niezgodny', 'neutralny']
FLANKER_PROB = [0.4, 0.4, 0.2]


Okno i bodźce
win = visual.Window(WIN_SIZE, color=BG_COLOR, fullscr=False, units='height')
#fullscreen ustalony na specyfikacji został zmieniony na rozmiar standardowego ekranu Maca ze wględu na to, że cały program
#działający na mniejszym oknie - na pełnym ekranie nie chciał nam chodzić ze względu na niemoc dwóch różnych MacBooków,
#które nam nie wyrabiały i się wieszały (sytuacja z zajęć)
fixation = visual.TextStim(win, text='+', color='black', height=0.1)
feedback = visual.TextStim(win, text='', color='black', height=0.08)
instruction = visual.TextStim(win, text='', color='black', height=0.035,
                              wrapWidth=1.5, pos=(0, 0.1))
stimulus = visual.TextStim(win, text='', color='black', height=0.1)
reminder = visual.TextStim(win, text='Z = "<"     M = ">"', pos=(0, -0.35),
#przypominajka w specyfikacji była u góry, ale po Pana sugesti z zajęć, że zazwyczaj jest na dole dałyśmy ją na dół
                           color='black', height=0.04)



zapisanie pliku z wynikiem
filename = f"flanker_{info['ID']}.csv"
with open(filename, mode='w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['sesja', 'typ_bodźca', 'ciąg', 'nr_próby', 'reakcja',
                     'poprawna', 'czas_reakcji(ms)', 'okulary'])


Generowanie prób
def generuj_proby(n):
    proby = []
    for _ in range(n):
        typ = random.choices(FLANKER_TYPES, weights=FLANKER_PROB)[0]
        kierunek = random.choice(['<', '>'])
        if typ == 'zgodny':
            ciag = kierunek * 5
        elif typ == 'niezgodny':
            flank = '>' if kierunek == '<' else '<'
            ciag = flank  2 + kierunek + flank  2
        else:
            ciag = '--' + kierunek + '--'
        proby.append((typ, kierunek, ciag))
    return proby


Pojedyncza próba
def wykonaj_probe(sesja, nr, typ, kierunek, ciag, feedback_on=True):
    fixation.draw()
    reminder.draw()
    win.flip()
    core.wait(FIXATION_DURATION)

    stimulus.setText(ciag)
    stimulus.draw()
    reminder.draw()
    win.flip()
    clock = core.Clock()
    keys = event.waitKeys(maxWait=MAX_RT, keyList=list(KEYS.values()) + [EXIT_KEY], timeStamped=clock)

    win.flip()
    core.wait(PAUSE_DURATION)

    if keys:
        key, rt = keys[0]
        if key == EXIT_KEY:
            core.quit()
        poprawna = (key == KEYS['left'] and kierunek == '<') or (key == KEYS['right'] and kierunek == '>') #ustalenie poprawnych odpowiedzi
    else:
        key, rt = 'brak', MAX_RT
        poprawna = False

    if feedback_on:
        feedback.setText("dobrze" if poprawna else "źle")
        feedback.draw()
        reminder.draw()
        win.flip()
        core.wait(FEEDBACK_DURATION)

    with open(filename, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([sesja, typ, ciag, nr, key, poprawna, int(rt * 1000), info['Czy nosisz okulary?']])


Instrukcja
instrukcja_tekst = (
    "W zadaniu, które za chwilę wykonasz, na ekranie będą pojawiać się ciągi znaków.\n"
    "W środku każdego z nich znajdować się będzie strzałka („<” lub „>”).\n"
    "Twoim zadaniem jest określenie kierunku tej środkowej strzałki, ignorując pozostałe znaki.\n\n"
    "    - Naciśnij klawisz Z, jeśli widzisz strzałkę w lewo („<”)\n"
    "    - Naciśnij klawisz M, jeśli widzisz strzałkę w prawo („>”)\n\n"
    "Postaraj się odpowiadać jak najszybciej i jak najdokładniej – mierzony będzie czas Twojej reakcji.\n\n"
    "Przed rozpoczęciem eksperymentu odbędzie się sesja treningowa. Po każdej odpowiedzi zostaniesz poinformowany o jej poprawności.\n"
    "W części eksperymentalnej ta informacja nie będzie się pojawiać.\n\n"
    "Aby przejść dalej naciśnij spację."
)
instruction.setText(instrukcja_tekst)
instruction.draw()
win.flip()
event.clearEvents()
event.waitKeys(keyList=['space'])


sesja treningowa
instruction.setText("Trening (20 prób)\n\n"
        "Zadanie zaraz się rozpocznie.\n"
        "Umieść lewą rękę na klawiszu Z, a prawą na klawiszu M. Skup wzrok na znaku +.\n\n"
        "Naciśnij SPACJĘ aby rozpocząć."
        )
instruction.draw()
reminder.draw()
win.flip()
event.clearEvents()
event.waitKeys(keyList=['space'])

for i, (typ, kier, ciag) in enumerate(generuj_proby(20), 1):
    wykonaj_probe("Trening", i, typ, kier, ciag, feedback_on=True)


Sesje eksperymentalne
for sesja_nr in range(1, 5):
    instruction.setText(
        f"Sesja eksperymentalna {sesja_nr} (100 prób)\n\n"
        "Zadanie zaraz się rozpocznie.\n"
        "Umieść lewą rękę na klawiszu Z, a prawą na klawiszu M. Skup wzrok na znaku '+'.\n\n"
        "Naciśnij SPACJĘ aby rozpocząć."
    )
    instruction.draw()
    reminder.draw()
    win.flip()
    event.clearEvents()
    event.waitKeys(keyList=['space'])

    for i, (typ, kier, ciag) in enumerate(generuj_proby(100), 1):
        wykonaj_probe(f"Sesja {sesja_nr}", i, typ, kier, ciag, feedback_on=False)

    if sesja_nr < 4:
        instruction.setText("Przerwa.\nAby kontynuować, naciśnij SPACJĘ.")
        instruction.draw()
        reminder.draw()
        win.flip()
        event.clearEvents()
        event.waitKeys(keyList=['space'])


Zakończenie
instruction.setText("To już koniec eksperymentu. Serdecznie dziękujemy za udział w badaniu!")
instruction.draw()
reminder.draw()
win.flip()
core.wait(4)

win.close()
core.quit()