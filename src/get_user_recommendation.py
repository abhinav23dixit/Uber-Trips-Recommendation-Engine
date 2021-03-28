from Recommendation.amalgamated_recommendation import initialize_models, get_user_recommendations, convert_user_idx_to_users
from constants import USERS

def run_user_choices():
    while True:
        choice = input("Enter 1 for getting recommendations for user names\t "
                       "Enter 2 for getting recommendations for user indexes\t "
                       "Enter 3 for viewing available users\t "
                       "Enter 4 for exiting out of system:\t")
        try:
            if int(choice) is 1:
                users_list = input("Enter user names separated by , to see their recommendations:\t")
                user_names = users_list.split(",")
                for name in user_names:
                    print("Running for user {}".format(name))
                    print(get_user_recommendations(user_name=name))
                    print()
            elif int(choice) is 2:
                users_list = input("Enter user indexes separated by , to see their recommendations:\t")
                user_indexes = users_list.split(",")
                user_names = convert_user_idx_to_users(user_indexes)
                for name in user_names:
                    print("Running for user {}".format(name))
                    print(get_user_recommendations(user_name=name))
                    print()
            elif int(choice) is 3:
                counter = 0
                for user in USERS:
                    print(counter, user)
                    counter += 1
            elif int(choice) is 4:
                break
            else:
                print("Invalid option")
            print()
        except ValueError as v:
            print("Invalid choice type entered {}".format(v))


if __name__ == '__main__':
    print("Welcome to Uber Trips recommendation engine")
    print("-------------------------------------------")
    print("Initializing models")
    initialize_models()
    run_user_choices()
