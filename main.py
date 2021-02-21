from joblib import dump, load
import numpy as np
import matplotlib.pyplot as plt
import sys
import getopt
import os

from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier

from data_processor import build_dataset, split_data


# Train and test the Multinomial Naive Bayes classifier
def train_nb(x_train, x_test, y_train, y_test):
    print("Training Multinomial Naive Bayes Classifier....")

    # Train & predict
    classifier = MultinomialNB().fit(x_train, y_train)
    test_classifer(classifier, x_test, y_test,
                   "Multinomial_Naive_Bayes-Sentiment.txt")
    return classifier


# Train and test the Base Decision Tree Classifier
def train_base_dt(x_train, x_test, y_train, y_test):
    print("Training Decision Tree Classifier...")

    classifier = DecisionTreeClassifier(criterion="entropy").fit(
        x_train, y_train)
    test_classifer(classifier, x_test, y_test,
                   "Base_Decision_Tree-Sentiment.txt")
    return classifier


def test_classifer(classifer, features, labels, out):
    y_pred = classifer.predict(features)
    write_stats(y_pred, labels, out.split('.')[0] + ".txt")


def plot_labels(labels):
    """ Creates a bar chart of the overall sentiment from the data set """
    pos = sum(labels)
    dist = [pos, len(labels) - pos]
    plt.bar(["Pos", "Neg"], dist)
    plt.ylabel('Count')
    plt.xlabel("Sentiment")
    plt.title('Sentiment Count')


def write_stats(y_pred, y_test, fname):
    """ Write overall classifier metrics to file """
    with open(fname, 'w') as f:
        f.write("Classification Report:\n")
        f.write(
            f'{classification_report(y_test, y_pred, target_names=["Negative", "Positive"])}\n')
        f.write("Confusion Matrix:\n")
        f.write(f'{np.array2string(confusion_matrix(y_test, y_pred))}\n\n')
        f.write('Instance #, Predicted, Actual:\n')
        f.writelines(f'{i + 1}: {t[0]} {t[1]}\n' for i, t in enumerate(
            zip(y_pred, y_test), 0))


def write_model(classifier, filename):
    base_filename = filename.split('.')[0]
    filename_suffix = "joblib"
    print(f"Writing {base_filename} classifier to disk...")
    dump(classifier, os.path.join(os.getcwd(),
                                  base_filename + "." + filename_suffix))


def load_model(filename):
    base_filename = filename.split('.')[0]
    filename_suffix = "joblib"
    try:
        return load(os.path.join(os.getcwd(), base_filename + "." + filename_suffix))
    except FileNotFoundError:
        print("Error loading models, make sure a joblib model file is present in the current directory.")
        print("Running this script with the `--train` option will generate the necessary files.")
        sys.exit(1)


def train_models(filename, persist_models=True):
    # Read and clean the raw data
    dataset = build_dataset(filename, True)

    # Split the data. We use 20% of the date as a test partition
    # and the the other 80% to train the models.
    x_train, x_test, y_train, y_test = split_data(
        dataset[:, :-1], dataset[:, -1], test_size=0.2)

    # Naive Base Classification
    cnb = train_nb(x_train, x_test, y_train, y_test)
    if persist_models:
        write_model(cnb, "multinomial-model")

    # Base Decision Tree Classification
    cdt = train_base_dt(x_train, x_test, y_train, y_test)
    if persist_models:
        write_model(cdt, "decision-tree-model")

    # Plot labels
    plot_labels(np.concatenate([y_train, y_test]))

    # Keep plot figure persistent. This is a blocking call.
    plt.show()


def test_models(filename):
    # Read and clean the raw data
    dataset = build_dataset(filename, True)
    features, labels = dataset[:, :-1], dataset[:, -1]

    # Test Multinomal Naive Bayes Model
    cnb = load_model("multinomial-model")
    test_classifer(cnb, features, labels, "multinomial-test.txt")

    # Test Base Decision Tree Model
    cnb = load_model("decision-tree-model")
    test_classifer(cnb, features, labels, "decision-tree-test.txt")


if __name__ == "__main__":
    datafile = None
    train = None
    persist = True

    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(
            argv, "i:", ["train", "test", "no-save", "input="])
    except getopt.GetoptError:
        print("Usage: python main.py -i <datafile> [--train | --test] ")
        sys.exit(2)

    for opt, arg in opts:
        if opt in ["-i", "--input"]:
            datafile = os.path.join(os.getcwd(), arg)
        elif opt == "--train":
            train = True
        elif opt == "--test":
            train = False
        elif opt == "--no-save":
            persist = False

    if datafile is None:
        print("Please specify a source data file")
        print("Usage: python main.py -i <datafile> [--train | --test]")
        sys.exit(2)
    if train is None:
        print("Please specify whether to train or test on this data")
        print("Usage: python main.py -i <datafile> [--train | --test]")
        sys.exit(2)

    if train:
        train_models(datafile, persist)
    else:
        test_models(datafile)
