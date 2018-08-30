# simple_movie_recommender
An implementation of a simple movie recommender based on a weighted rating by votes and favorite genres.

The data which was used are metadata csv files with the following labels:

Movie genres --> Genre

IMDB rating  --> imdbRating

IMDB votes   --> imdbVotes (votes must be integers and not strings)

Movie title  --> Title

Movie plot   --> Plot

Movie year   --> Year


The labels should be exactly like the above right side representation.


The recommender engine can use either simulated data or data which have been entered by the user. For this particular implementation we used a simulation mechanism to create a list of movies which have been not viewed buy the user. Positive (viewed) and negative (not viewed) markers have been equally distributed among the qualified movies in the movie list. Qualified movies are those which have a viewing rate above a particular threshold.

The code can be run by executing the below script from command line:

-> python movie_recommender.py

The output will be 5 movies recommended by the engine and base up on the weighted rating score of the IMDB scores. As weights we use the votes and in particular we choose to use as minimum threshold the 85-th percentile of the sample.
