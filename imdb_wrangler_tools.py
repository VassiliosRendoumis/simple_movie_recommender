# -*- coding: utf-8 -*-
import pandas as pd


def load_data(file_path):
    """ Loads csv data into a panda data frame and returns it

        Input parameters:
            file_path - the path of the csv file
    """

    return pd.read_csv(file_path, low_memory=False)
