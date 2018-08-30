# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 21:32:19 2018

@author: Vassilios Rendoumis
"""
import random
from collections import Counter


class IMDBDataWrangler(object):
    """ This class acts as a data wrangling facility to transform IMDB metadata
        into a usable data frame. The final data frame can be digested by a
        set of tool present in this class, which will create a list of movies
        recommended to the user.


    Attributes:

        movie_data (panda data frame):  A data frame of IMDB metadata

        minimum_votes (int):            Minimum number of votes received by a
                                        movie.
        
        aggregate_mean_vote (double):   Mean of the imdb rating score
        
        favorite_genres (set):          A set of the favorite genres of user
        
        imdb_movie_genres (set):        A set of the most popular movie genres
                                        in IMDB

    """

    def __init__(self, movie_metadata):

        self.movie_data = movie_metadata
        self.minimum_votes = None
        self.aggregate_mean_vote = None
        self.favorite_genres = set([])
        self.imdb_movie_genres = set(['Drama', 'Adventure', 'Action',
                                      'Comedy', 'Sci-Fi', 'Thriller',
                                      'Crime',  'Fantasy', 'Mystery',
                                      'Romance', 'Animation', 'Family',
                                      'Biography', 'Horror', 'War',
                                      'History', 'Music', 'Sport',
                                      'Western'])

    
    def select_fav_genres(self, genres):
        """ Let user select its favorite genres of movies. Returns a string
            for partial string match.

            Input parameters:
                genre - a set of genres
        """
    
        self.favorite_genres = self.favorite_genres.union(genres)

        return '|'.join([genre for genre in self.favorite_genres])


    def extract_fav_movie_entries(self, genre_filter):
        """ Selects only the movies which match the favorite genres of user

            Input parameters:
                genre_filter - a string for partial string match with movie
                               genres.
        """

        self.movie_data = \
        self.movie_data[self.movie_data['Genre'].str.contains(
                                                       genre_filter, na=False)]
    
    
    def compute_aggregate_mean_vote(self):
        """ Calculates the mean of the imdb rating score

            Input parameters:
                None
        """

        self.aggregate_mean_vote = self.movie_data['imdbRating'].mean()


    def compute_minimum_votes(self, percentile):
        """ Caclulates the minimum number of votes received by a movie in
            the n-th percentile.

            Input parameters:
                percentile - the n-th percentile in the sample/list
        """

        self.minimum_votes = self.movie_data['imdbVotes'].quantile(percentile)


    def qualified_movies(self, minimum_votes):
        """ Creates a lsit of movies which qualify for the chart, based on
            their vote counts

            Input parameters:
                minimum_votes - minimum number of votes received by a movie
                                      in the n-th percentile
        """

        if minimum_votes is not None:
            return self.movie_data.copy().loc[self.movie_data['imdbVotes'] >=
                                              minimum_votes]
        else:
            raise Exception("Minimum votes must be computed")


    def number_of_movies(self):
        """ Calculates the number of movies in the movie list

            Input parameters:
                None
        """

        return self.movie_data.shape[0]


    def create_score_feature(self):
        """ Define a new feature 'score' and calculate its value with
            weighted_rating()

            Input parameters:
                qualified_movies - a panda data frame of the qualified movies
        """

        self.movie_data['score'] = self.movie_data.apply(self.weigted_rating,
                                                         axis=1)


    def sort_data_by_feature(self, feature, ascend=False):
        """ Sort movies based on feature

            Input parameters:
                feature - a numeric type feature
        """

        self.movie_data = self.movie_data.sort_values(feature,
                                                              ascending=ascend)


    def weigted_rating(self, movie_entry):
        """ Calculates the weighted rating metric/score for a movie

            Input parameters:
                movie_entry - a movie in the movie list
        """

        if (self.minimum_votes is not None) and \
           (self.aggregate_mean_vote is not None):

            # number of votes for the movie
            number_of_votes = movie_entry['imdbVotes']

            # average rating of the movie
            average_rating = movie_entry['imdbRating']

            return (number_of_votes / (number_of_votes + self.minimum_votes)
                    * average_rating) + (self.minimum_votes / (self.minimum_votes \
                    + number_of_votes) * self.aggregate_mean_vote)
        else:
            raise Exception('Minimum votes or aggregate mean vote are not \
                            provided')


    def simulate_user_viewing_record(self):
        """ Simulates a viewing history for all moviesby creating a viewing
            feature/column

            Input parameters:
                None
        """

        number_of_movies = self.number_of_movies()
        self.movie_data = self.movie_data.assign(
            ViewedSim=[random.choice([0, 1]) for i in range(number_of_movies)])

        return self.movie_data


    def create_viewing_feature(self):
        """ Creates a features indicating whether a movie has been viewed. The
            default value will me 0 (not viewed)

            Input parameters:
                None
        """

        number_of_movies = self.number_of_movies()
        self.movie_data = self.movie_data.assign(
                                   Viewed=[0 for i in range(number_of_movies)])
        return self.movie_data


    def viewed_movies(self, response, sim=0):
        """ Creates a data frame of movies which filters out either the movies
            which have been watch by user or not. It can also used simulated
            viewing responses.

            Input parameters:
                response - eiter 1 (viewed) or 0 (not viewed)
                sim - indicating whether is is a simulation (1) or not (0).
                      If it is a simulation the function will create the data
                      frame from the 'ViewedSim' entries, else it will use the
                      entries from the 'Viewed' column.
        """

        view_entries = 'Viewed'
        if sim == 1:
            view_entries = 'ViewedSim'
            
        return self.movie_data.copy().loc[self.movie_data[view_entries] ==
                                          response]


    def get_genres_of_movies(self):
        """ Return the genres of all movies with the frequency in the movie
            data frame

            Input parameters:
                None
        """

        genres = ''.join([''.join([row, ' '])
                          for row
                          in self.movie_data['Genre']])

        genres = genres.replace(',', '')
        genres_list = genres.split()

        return Counter(genres_list).most_common()
