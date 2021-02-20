from joblib import load
from data_helper import pre_process, write_stats

# Pre Process Data
x_test, y_test = pre_process(open('all_sentiment_shuffled.txt', encoding="utf8"), True)

# Load Classifier
clf = load('BestDT_Sentiment_Clf.joblib')

# Predict
y_pred = clf.predict(x_test)

# Write stats to file
write_stats(y_pred, y_test, 'BestDT-Sentiment-GivenDataset.txt', False, True)
