import itertools

from sklearn.tree import DecisionTreeClassifier
from data_helper import pre_process, plot, write_stats

# Pre-process/Extract data
x_train, x_test, y_train, y_test = pre_process(open('all_sentiment_shuffled.txt', encoding="utf8"))

# Plot the class counts
plot(y_train + y_test)

# Define classifier parameters to test
param_dict= {
    "criterion" : ['gini','entropy'],
    'min_samples_split': [5, 10],
    'min_samples_leaf' : [3, 5],
}

# Define classifier + Train & Predict
for params in itertools.product(*param_dict.values()):
    clf = DecisionTreeClassifier(criterion=params[0], \
                                    splitter='best', \
                                    max_depth=None, \
                                    min_samples_split=params[1], \
                                    min_samples_leaf=params[2], \
                                    max_features=None,
                                    random_state=0)

    clf.fit(x_train, y_train)
    y_pred = clf.predict(x_test)

    # Write stats to file
    write_stats(y_pred, y_test, 'BestDT-Sentiment', params)