''' Kniffel Simulator'''

import random
import time
from statistics import mode

kniffel = 0     # Anzahl der Kniffel

def simulate(times):

    global kniffel

    for _ in range(times):

        dices = []

        # 1. Wurf
        for i in range(0, 5):
            dices.append(random.randint(1, 5))

        # Check auf Kniffel
        if all(elem == dices[0] for elem in dices):
            kniffel += 1

        # Modus bestimmen
        mode_dices = mode(dices)

        # 2. Wurf
        for i in range(0, 5):
            if dices[i] == mode_dices:
                continue
            else:
                dices[i] = random.randint(1, 5)

        # Check auf Kniffel
        if all(elem == dices[0] for elem in dices):
            kniffel += 1

        # 3. Wurf
        for i in range(0, 5):
            if dices[i] == mode_dices:
                continue
            else:
                dices[i] = random.randint(1, 5)

        # Check auf Kniffel
        if all(elem == dices[0] for elem in dices):
            kniffel += 1


def probability(times):

    global kniffel
    
    probs = []
    num_kniffel = []

    runs = 10000
    
    for _ in range(times):
        simulate(runs)
        probs.append(kniffel / runs * 100)

        num_kniffel.append(kniffel)
        kniffel = 0
    
    # Mitelwert der Wahrscheinlichkeiten bestimmen
    avg = 0
    for elem in probs:
        avg += elem
    
    print('Wahrscheinlichkeit: ', round(avg / len(probs), 3))

# Get execution time
start_time = time.time()
probability(100)
print(f'Execution time: {round(time.time() - start_time, 2)} seconds')