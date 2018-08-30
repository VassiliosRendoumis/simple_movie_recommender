# -*- coding: utf-8 -*-

import imdb_wrangler_tools as tl
from imdb_data_wrangler import IMDBDataWrangler


def movie_recommender():
    """
    We will create a simple recommenders that recommends the top items based on
    a weighted rating that takes into account the average rating and the number
    of votes it has gathered.
    
    We will use some type of simulation in order to emulate a viewing history
    of the user. We will then recommend movies to the user which he hasn't
    viewed before.
    """

    """ Load data from IMDB metadata extraction """
    metadata = tl.load_data('IMDBdata_MainData_imdbVotes_to_int.csv')


    """ Create the data wrangler facilities object """
    imdb_data = IMDBDataWrangler(metadata)

    
    """ Create filter string from your favorite genres """
    genre_filter = imdb_data.select_fav_genres(set(['Action','Adventure',
                                                    'Sci-Fi', 'Fantasy']))


    """ Filter out movies which have only favorite genres """
    imdb_data.extract_fav_movie_entries(genre_filter)
    

    """ Calculate aggretate mean vote """
    imdb_data.compute_aggregate_mean_vote()


    """ Calculate Minimum votes by taking the 85th percentile """
    imdb_data.compute_minimum_votes(0.85)


    """ Extract qualified movies and substitute initial db"""
    imdb_data.movie_data = imdb_data.qualified_movies(imdb_data.minimum_votes)


    """ Define a new feature 'score' and calculate its value
        with `weighted_rating()`
    """
    imdb_data.create_score_feature()


    """ Sort movies based on score calculated above """
    imdb_data.sort_data_by_feature('score')


    """                    Simulation part                    """

    """ Simulate a viewing history for all movies """
    imdb_data.simulate_user_viewing_record()


    """ Create a subset of movies you you have not viewed based on the
        viewing history simulation
    """
    movies_not_viewed = imdb_data.viewed_movies(0, 1)

    """ From the movies we have not viewed, pick the first 5. Since they are 
        sorted by score they will be the 5 top rated.
    """
    print(
    movies_not_viewed[['Title', 'Plot', 'Year', 'score', 'ViewedSim']].head(5))


if __name__ == "__main__":
    movie_recommender()


