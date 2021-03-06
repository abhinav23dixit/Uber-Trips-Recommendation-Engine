import numpy as np
import pandas as pd
import sklearn
from scipy.sparse import csr_matrix
import warnings
import implicit
from scipy.sparse import save_npz
from sklearn.neighbors import NearestNeighbors
from Recommendation.utils import get_interest, read_dataset, get_interest_index, interest_finder, see_user_top_interests
from constants import OTHERS_REGEX
warnings.simplefilter(action='ignore', category=FutureWarning)


def data_analysis(ratings: pd.DataFrame):
    n_ratings = len(ratings)
    n_interests = ratings['INTEREST_ID*'].nunique()
    n_users = ratings['USER_ID*'].nunique()

    print(f"Number of ratings: {n_ratings}")
    print(f"Number of unique interests: {n_interests}")
    print(f"Number of unique users: {n_users}")
    print(f"Average number of ratings per user: {round(n_ratings / n_users, 2)}")
    print(f"Average number of ratings per interests: {round(n_ratings / n_interests, 2)}")

    user_freq = ratings[['USER_ID*', 'INTEREST_ID*']].groupby('USER_ID*').count().reset_index()
    user_freq.columns = ['USER_ID*', 'n_ratings']
    print(user_freq.head())

    print(f"Mean number of ratings for a given user: {user_freq['n_ratings'].mean():.2f}.")


def create_X(df: pd.DataFrame):
    """
    Generates a sparse matrix from ratings dataframe.
    Returns:
        X: sparse matrix
        user_mapper: dict that maps user id's to user indices
        user_inv_mapper: dict that maps user indices to user id's
        interest_mapper: dict that maps interest id's to interest indices
        interest_inv_mapper: dict that maps interest indices to interest id's
    """
    N = df['USER_ID*'].nunique()
    M = df['INTEREST_ID*'].nunique()

    user_mapper = dict(zip(np.unique(df["USER_ID*"]), list(range(N))))
    interest_mapper = dict(zip(np.unique(df["INTEREST_ID*"]), list(range(M))))

    user_inv_mapper = dict(zip(list(range(N)), np.unique(df["USER_ID*"])))
    interest_inv_mapper = dict(zip(list(range(M)), np.unique(df["INTEREST_ID*"])))

    user_index = [user_mapper[i] for i in df['USER_ID*']]
    interest_index = [interest_mapper[i] for i in df['INTEREST_ID*']]

    X = csr_matrix((df["RATING*"], (interest_index, user_index)), shape=(M, N))

    return X, user_mapper, interest_mapper, user_inv_mapper, interest_inv_mapper


def find_similar_movies(interest, X, k, interest_mapper, interest_inv_mapper , metric='cosine',  show_distance=False):
    """
    Finds k-nearest neighbours for a given interest.

    Args:
        interest: interest id
        X: user-item utility matrix
        k: number of similar items to retrieve
        metric: distance metric for kNN calculations

    Returns:
        list of k similar interest's
    """
    neighbour_ids = []

    interest_ind = interest_mapper[interest]
    interest_vec = X[interest_ind]
    k += 1
    kNN = NearestNeighbors(n_neighbors=k, algorithm="brute", metric=metric)
    kNN.fit(X)
    if isinstance(interest_vec, np.ndarray):
        interest_vec = interest_vec.reshape(1, -1)
    neighbour = kNN.kneighbors(interest_vec, return_distance=show_distance)
    for i in range(0, k):
        n = neighbour.item(i)
        neighbour_ids.append(interest_inv_mapper[n])
    neighbour_ids.pop(0)
    return neighbour_ids


def use_alternating_least_squares(factors: int, X):
    model = implicit.als.AlternatingLeastSquares(factors=factors)
    model.fit(X)
    return model


def initialize_cf_model(ratings: pd.DataFrame, interests: pd.DataFrame):
    # interests mapper
    interest_to_id_mapper = dict(zip(interests['INTEREST*'], interests['INTEREST_ID*']))
    interest_id_inv_mapper = dict(zip(interests['INTEREST_ID*'], interests['INTEREST*']))

    X, user_mapper, interest_mapper, user_inv_mapper, interest_inv_mapper = create_X(ratings)
    save_npz('Recommendation/user_interest_matrix.npz', X)
    model = use_alternating_least_squares(factors=24, X=X)
    X_t = X.T.tocsr()
    return {
        "X": X,
        "user_mapper": user_mapper,
        "interest_mapper": interest_mapper,
        "user_inv_mapper": user_inv_mapper,
        "interest_inv_mapper": interest_inv_mapper,
        "X_t": X_t,
        "model": model
    }


def get_cf_user_recommendations(user_id: int, model_details: dict, interest_id_inv_mapper):
    user_idx = model_details['user_mapper'][user_id]
    recommendations = model_details['model'].recommend(user_idx, model_details['X_t'])
    reco_interests = []
    for r in recommendations:
        recommended_interest = get_interest(r[0], model_details['interest_inv_mapper'],
                                            interest_id_inv_mapper)
        if OTHERS_REGEX not in recommended_interest:
            reco_interests.append(recommended_interest)
    return reco_interests

# Test this individual component here
# if __name__ == '__main__':
#     ratings = read_dataset("Dataset/Rated User Interests.csv")
#     interests = read_dataset("Dataset/Interests Dataset.csv")
#     users = read_dataset("Dataset/Users Dataset.csv")
#     interest_id_inv_mapper = dict(zip(interests['INTEREST_ID*'], interests['INTEREST*']))
#
#     model_details = initialize_cf_model(ratings, interests)
#     print(get_cf_user_recommendations(2, model_details, interest_id_inv_mapper))









