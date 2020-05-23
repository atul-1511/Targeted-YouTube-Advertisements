This folder has all the files required for labelling the dataset.

"bad_words" folder is a collection of vulgar words which we are trying to find out in a youtube video.
"profanity.py" has all the methods to check the profanity percentage.
for labelling the videos run the "profanity_check" file, which will save the labelled dataset as "labelled_processed_youtube_data.csv"

Before running the profanity_check make sure that you change the directoy in which you are running the python code to "labelling"
folder. For eg. in our case we would change the directory to "C:\Users\vishal\Desktop\ML\labelling"

after labelling we have made a baseline model to classify the threat and non threat videos.
so we go to "baseline model" subfolder