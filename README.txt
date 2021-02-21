Comp 472 - Assignment 1 Running Intructions

The main script file can be used to either train and save models or to test already-saved models. In order to use the testing option, make sure the corresponding `*.joblib` files are present in the directory. Running the script with the `--train` option will generate the necessary model files from the provided data file.

Script Usage: python main.py -i <datafile> [--train | --test]

To run this script in training mode - The data file `all_sentiment_shuffled.txt` should be in the scripts working directory:
    python main.py -i all_sentiment_shuffled.txt --train

This will generate output files containing the overall stats of the models as well as persist the models to the disk as `*.joblib` files. If persisting the models is not desired, simply run the above with the `--no-save` flag.
    python main.py -i all_sentiment_shuffled.txt --train --no-save

To run this script in testing mode - The data file `all_sentiment_shuffled.txt` should be in the scripts working directory:
    python main.py -i all_sentiment_shuffled.txt --test


