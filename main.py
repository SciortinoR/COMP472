import numpy as np
import matplotlib.pyplot as plt

from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
from sklearn.naive_bayes import MultinomialNB

from data_processor import build_dataset, split_data


# Train and test the Multinomial Naive Bayes classifier
def train_and_test_nb(x_train, x_test, y_train, y_test):
    print("Training Multinomial Naive Bayes Classifier....")

    # Train & predict
    classifier = MultinomialNB().fit(x_train, y_train)
    y_pred = classifier.predict(x_test)

    write_stats(y_pred, y_test, "Multinomial_Naive_Bayes-Sentiment.txt", 0.2)


def plot_labels(labels):
    """ Creates a bar chart of the overall sentiment from the data set """
    pos = sum(labels)
    dist = [pos, len(labels) - pos]
    plt.bar(["Pos", "Neg"], dist)
    plt.ylabel('Count')
    plt.xlabel("Sentiment")
    plt.title('Sentiment Count')


def write_stats(y_pred, y_test, fname, test_size):
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


if __name__ == "__main__":
    # Read and clean the raw data
    dataset = build_dataset("./all_sentiment_shuffled.txt", True)

    # Split the data. We use 20% of the date as a test partition
    # and the the other 80% to train the models.
    x_train, x_test, y_train, y_test = split_data(
        dataset[:, :-1], dataset[:, -1], test_size=0.2)

    # Naive Base Classification
    train_and_test_nb(x_train, x_test, y_train, y_test)

    # Plot labels
    plot_labels(np.concatenate([y_train, y_test]))

    # Keep plot figure persistent. This is a blocking call.
    plt.show()
