Put the data files (train.csv and test.csv) in this folder.

These files can be downloaded from the [competition data page](https://www.kaggle.com/c/FacebookRecruiting/data)

Remove the first line of train.csv

Then run the following command with n = Number of Entries you need.

shuf -n N train.csv > sample_down_train.csv

Append ,1 to the end of each line in the file

sed -e 's/$/,1/' -i sampled_down_train.csv

