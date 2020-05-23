"video_ids.csv" contains the list of the video ids of youtube that we have to scrap.

"scrap.py" file scraps the important data from youtube like 'title',
'channelTitle','tags','viewCount','likeCount','dislikeCount','commentCount',
'description','thumbnails' ,'transcript','categoryId'

But for building the models, we have took only handful of features from youtube videos, because extraction took
a lot of time for 12k video ids

"youtube_data.csv" contains the extracted fetaures from  youtube video arranged row wise.

After scrapping is done we need to preprocess the data for feeding into machine learning algorithms.
So now we go to "preprocessing" subfolder in the "ML" folder.