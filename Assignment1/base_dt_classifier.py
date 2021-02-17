from sklearn.tree import DecisionTreeClassifier
from data_helper import pre_process, plot, write_stats

# Pre-process/Extract data
x_train, x_test, y_train, y_test = pre_process(open('all_sentiment_shuffled.txt', encoding="utf8"))

# Plot the class counts
plot(y_train + y_test)

# Define DT Clf
clf = DecisionTreeClassifier(random_state=0)
clf.fit(x_train, y_train)
y_pred = clf.predict(x_test)

# Write stats to file
write_stats(y_pred, y_test, 'BaseDT-Sentiment.txt')