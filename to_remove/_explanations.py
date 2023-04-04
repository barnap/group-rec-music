import sys
import math

import config

sys.path.append('../')
'''
In this file put explanation generation! Not that in DB the tables are created such that explanations can be saved 
for each combination of aggregation strategy and explanation style, for groups and also personalized explanations can be
saved as well. See helper_functions.generate_group_explanations and  helper_functions.generate_personalized_explanations
'''


def ordinal(n):
    '''
    Takes an integer and returns the ordinal e.g 1 - 1st 2- 2nd 3 - 3rd ...
    :param n:
    :return:
    '''
    return "%d%s" % (n, "tsnrhtdd"[(math.floor(n / 10) % 10 != 1) * (n % 10 < 4) * n % 10::4])


# TODO for now for demonstration purposes we will generate the following explanation for the groups, assuming that
# TODO the only aggregation strategy used is average!
# TODO Change this to song Name!
def highest_rated(ranking, songID, user_ratings, aggregation_strategy):
    '''
    Note that for now I am using songID here, maybe if we decide to use song Name, then from DB song name information
    must be collected before!
    :param aggregation_strategy:
    :param user_ratings:
    :param ranking:
    :param songID:
    :return:
    '''
    return "The song is recommended to the group since it achieves the " + ordinal(ranking) + \
           " highest average rating."


# TODO for now for demonstration purposes we will generate the following explanation for the groups, assuming that
def highest_rated_personalized(user_id, ranking, songID, user_ratings, aggregation_strategy):
    user_rating = user_ratings[user_id]
    rating_type = "highly rated" if user_rating >= config.HIGHLY_RATED_THRESHOLD else "not highly rated"
    return "This song is recommended to the group since it achieves the " + ordinal(
        ranking) + " highest average rating and you " + rating_type + " it."


if __name__ == '__main__':
    print(ordinal(1))
