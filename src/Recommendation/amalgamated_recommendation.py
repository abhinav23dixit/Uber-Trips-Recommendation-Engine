import numpy as np
import pandas as pd
from constants import ratings_dataset_path, interests_dataset_path, users_dataset_path, USERS,time_classes
from Recommendation.als_collaborative_filtering import initialize_cf_model, get_cf_user_recommendations
from Recommendation.user_behaviour import get_highly_rated_interests, get_highly_rated_activities, generate_complete_user_interest_dataset
from Recommendation.utils import read_dataset
ratings = None
interests = None
users = None
users_to_user_id_map = None
user_id_to_users_map = None
interest_id_inv_mapper = None
model_details = None
rating_interest_df = None


def load_datasets():
    global ratings
    global interests
    global users
    global users_to_user_id_map
    global user_id_to_users_map
    global interest_id_inv_mapper
    global rating_interest_df
    ratings = read_dataset(ratings_dataset_path)
    interests = read_dataset(interests_dataset_path)
    users = read_dataset(users_dataset_path)
    users_to_user_id_map = dict(zip(users['USER*'], users['USER_ID*']))
    user_id_to_users_map = dict(zip(users['USER_ID*'], users['USER*']))
    interest_id_inv_mapper = dict(zip(interests['INTEREST_ID*'], interests['INTEREST*']))
    rating_interest_df = generate_complete_user_interest_dataset(ratings, interests)


def convert_user_idx_to_users(user_indexes):
    user_names = []
    for idx in user_indexes:
        if int(idx) in user_id_to_users_map:
            user_names.append(user_id_to_users_map[int(idx)])
        else:
            print("User index does not exist for value {}".format(idx))
    return user_names


def initialize_models():
    global model_details
    # load datasets
    load_datasets()
    # initialize models
    model_details = initialize_cf_model(ratings, interests)


def get_user_recommendations(user_name: str):
    if user_name in users_to_user_id_map:
        user_id = users_to_user_id_map[user_name]
        cf_recommendations = get_cf_user_recommendations(user_id, model_details, interest_id_inv_mapper)
        top_rated_interests = get_highly_rated_interests(user_id, rating_interest_df)
        top_rated_activities = get_highly_rated_activities(user_id, rating_interest_df)
        amalgamated_recommendations = get_amalgamated_reco(cf_recommendations, top_rated_interests, top_rated_activities)
        return get_expanded_interests(amalgamated_recommendations)
    else:
        print("User name {} unavailable".format(user_name))
        return []


def get_expanded_interests(recommended_interests: list):
    expanded_interests = []
    for interest in recommended_interests:
        activity = interest[:interest.rindex(" ")]
        time_class = int(interest.split()[-1])
        start_hrs = time_classes[time_class][0].hour
        end_hrs = time_classes[time_class][1].hour+1
        expanded_interests.append(activity + " between " + str(start_hrs) + " and " + str(end_hrs) + " hours in 24 "
                                                                                                     "hour format")
    return expanded_interests


def check_already_in_list(reco_item, reco_list):
    return reco_item in reco_list


def check_activity_in_list(activity, reco_list):
    for interest in reco_list:
        if activity in interest:
            return True
    return False


def get_amalgamated_reco(cf_recommendations, top_interests, top_activties):
    amalgamated_reco = []
    top_interest_counter = 0
    activity_counter = 0
    for i in range(1,8):
        if i is 1 or i is 3 or i is 5:
            # get top rated interest recommendation
            while top_interest_counter < len(top_interests) and check_already_in_list(top_interests[top_interest_counter], amalgamated_reco):
                top_interest_counter += 1
            if top_interest_counter < len(top_interests):
                amalgamated_reco.append(top_interests[top_interest_counter])
                top_interest_counter += 1
        elif i is 2 or i is 6:
            # get top rated activity for user in cf recommendation
            reco_flag = False
            while activity_counter < len(top_activties):
                activity = top_activties[activity_counter]
                for recommendation in cf_recommendations:
                    if activity in recommendation and not check_already_in_list(recommendation, amalgamated_reco):
                        reco_flag = True
                        amalgamated_reco.append(recommendation)
                        break
                if reco_flag:
                    break
                activity_counter += 1
        elif i is 4 or i is 7:
            # get outlier activities
            for recommendation in cf_recommendations:
                activity = recommendation[:recommendation.rindex(" ")]
                if not check_already_in_list(activity, amalgamated_reco) and not check_already_in_list(recommendation,
                                                                                                   amalgamated_reco):
                    amalgamated_reco.append(recommendation)
                    break
    return amalgamated_reco

# Test this individual component here
# if __name__ == '__main__':
#     load_datasets()
#     initialize_models()
#     for user in USERS:
#         recos = get_user_recommendations(user)
#         print("for user {}".format(user))
#         print(recos)
#         break
