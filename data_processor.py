import numpy as np
from collections import Counter
import string
from sklearn.preprocessing import StandardScaler


def generate_stop_words(datafile):
    print("Generating stopwords from:", datafile)
    return n_most_common_words(datafile)


def clean_string(text, stopwords):
    return [s.translate(str.maketrans('', '', string.punctuation)) for s in list(filter(lambda a: a not in stopwords, text))]


def split_data(features, labels, test_size):
    split_point = int(test_size * len(features))
    return features[split_point:], features[:split_point], labels[split_point:], labels[:split_point]


def n_most_common_words(datapath, n=100):
    words = []
    with open(datapath, encoding="utf8") as f:
        for line in f:
            for word in clean_string(line.split()[3:], {"pos", "neg"}):
                words.append(word)
    return Counter(words).most_common(n)


def scale_features(x_train, x_test):
    sc = StandardScaler()
    scaled_train = sc.fit_transform(x_train)
    scaled_test = sc.transform(x_test)
    return scaled_train, scaled_test


def build_dataset(datafile, remove_stopwords=False):
    freqs = []
    y = []
    stop_words = distinct = {}
    if remove_stopwords:
        stop_words = generate_stop_words(datafile)

    index = 0
    for row in open(datafile, encoding="utf-8"):
        word_list = row.split()
        if word_list[1] == "pos":
            y.append(1)
        elif word_list[1] == "neg":
            y.append(0)

        cleaned_words = clean_string(word_list[3:], stop_words)
        freqs.append(Counter(cleaned_words))

        for word in cleaned_words:
            if word not in distinct:
                distinct[word] = index
                index += 1

    y = np.array(y).reshape((len(y), 1))
    x = np.hstack((np.zeros((len(freqs), len(distinct)), dtype=int), y))

    row = 0
    for freq in freqs:
        for w, f in freq.items():
            if w in distinct:
                x[row][distinct[w]] = f
        row += 1

    return x
