import string
import collections
import numpy as np
import matplotlib.pyplot as plt

from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

SPLIT = 0

# Pre-calculated to avoid 2N looping
NUM_WORDS = 54090
NUM_INSTANCES = 11914

def pre_process(file):
    global SPLIT, NUM_WORDS, NUM_INSTANCES

    labels = []
    features = [[0]*NUM_WORDS for _ in range(NUM_INSTANCES)]
    word_hash = collections.defaultdict(int)

    i = 0
    for j, line in enumerate(file):
        line = line.split()
        if line[1] == 'pos':
            labels.append(1)
        else:
            labels.append(0)
        
        line = line[3:]
        for w in line:
            w = w.translate(str.maketrans('', '', string.punctuation))
            if w:
                if w not in word_hash:
                    features[j][i] += 1
                    word_hash[w] = i
                    i += 1
                else:
                    features[j][word_hash[w]] += 1

    file.close()
    SPLIT = int(0.8 * len(labels))
    return features[:SPLIT], features[SPLIT:], labels[:SPLIT], labels[SPLIT:]

def plot(labels):
    pos = sum(labels)
    classes = ['Positive', 'Negative']
    dist = [pos, len(labels) - pos]

    plt.bar(classes, dist)
    plt.ylabel('Count')
    plt.xlabel("Sentiment")
    plt.title('Sentiment Count')
    plt.show()

def write_stats(y_pred, y_test, out_name, params=False):
    global SPLIT

    if not params:
        file = open(out_name, 'w')
    else:
        report = classification_report(y_test, y_pred, target_names=["Negative", "Positive"], output_dict=True)
        file = open(f'{out_name}-{report["accuracy"]}.txt', 'w')
        file.write("Best-DT Params Used: \n")
        file.write(f"criterion : {params[0]}\n")
        file.write(f"splitter : best\n")
        file.write(f"max_depth : None\n")
        file.write(f"min_samples_split : {params[1]}\n")
        file.write(f"min_samples_leaf : {params[2]}\n")
        file.write(f"max_features : None\n\n")
        
    file.write("Classification Report:\n")
    file.write(f'{classification_report(y_test, y_pred, target_names=["Negative", "Positive"])}\n')

    file.write("Confusion Matrix:\n")
    file.write(f'{np.array2string(confusion_matrix(y_test, y_pred))}\n\n')

    file.write('Instance #, Prediction:\n')
    file.writelines(f'{i}, {n}\n' for i, n in enumerate(y_pred, SPLIT))

    file.close()