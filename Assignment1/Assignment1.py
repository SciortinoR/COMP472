from matplotlib import pyplot as plt
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix
import math


def main():
    # Task 0
    read_documents('all_sentiment_shuffled.txt')
    all_docs, all_labels = read_documents('all_sentiment_shuffled.txt')

    # Task 1
    x = ["neg", "pos"]
    y = [0, 0]

    for i in range(len(all_labels)):
        if all_labels[i] == "neg":
            y[0] += 1
        else:
            y[1] += 1

    plt.bar(x, y)

    plt.title("Distribution")
    plt.ylabel("Number of instances")
    plt.xlabel("Label")
    plt.show()

    # Task 2
    split = 0.8*len(all_docs)
    vectorizer = CountVectorizer(stop_words='english')
    all_features = vectorizer.fit_transform(all_docs)
    x_train, x_test, y_train, y_test = train_test_split(all_features, all_labels, test_size=0.2)

    # Naive Bayes
    classifier = MultinomialNB()
    classifier.fit(x_train, y_train)
    nb_score = classifier.score(x_test, y_test)
    nb_prediction = classifier.predict(x_test)

    # Base DT
    base_dt = DecisionTreeClassifier(criterion="entropy")
    base_dt.fit(x_train, y_train)
    base_dt_score = base_dt.score(x_test, y_test)
    base_dt_prediction = base_dt.predict(x_test)

    # Best DT
    best_dt = DecisionTreeClassifier(criterion="entropy", splitter="random", random_state=69)
    best_dt.fit(x_train, y_train)
    best_dt_score = best_dt.score(x_test, y_test)
    best_dt_prediction = best_dt.predict(x_test)

    # Task 3
    write_file(nb_prediction, y_test, "NaiveBayes", str(nb_score), split)
    write_file(base_dt_prediction, y_test, "BaseDT", str(base_dt_score), split)
    write_file(best_dt_prediction, y_test, "BestDT", str(best_dt_score), split)


def read_documents(filename):
    input_file = open(filename, encoding='utf8')
    lines = input_file.readlines()
    docs = []
    labels = []

    for line in lines:
        words = line.split(" ", 3)
        docs.append(words[3])
        labels.append(words[1])

    return docs, labels


def write_file(y_pred, y_true, model, accuracy, split):
    filename = model + "-all_sentiment_shuffled.txt"
    file = open(filename, "w")

    file.write("Accuracy: " + accuracy + "\n")
    file.write("Precision score: " + str(precision_score(y_true, y_pred, pos_label="pos")) + "\n")
    file.write("Recall score: " + str(recall_score(y_true, y_pred, pos_label="pos")) + "\n")
    file.write("F1 score: " + str(f1_score(y_true, y_pred, pos_label="pos")) + "\n")

    file.write("Confusion matrix:\n" + str(confusion_matrix(y_true, y_pred)) + "\n")

    file.write("Row number, predicted class, correct class\n")
    for i in range(len(y_true)):
        file.write(str(math.ceil(i + split)) + ", " + str(y_pred[i]) + ", " + str(y_true[i]) + "\n")


if __name__ == "__main__":
    main()
