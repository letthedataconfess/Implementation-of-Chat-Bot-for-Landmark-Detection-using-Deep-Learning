import numpy as np
from lightfm.datasets import fetch_movielens
import pickle
from lightfm import LightFM
from lightfm.evaluation import precision_at_k


data = fetch_movielens(min_rating=5.0)


def sample_recommendation(model, data, user_ids):

    n_users, n_items = data['train'].shape

    for user_id in user_ids:
        known_positives = data['item_labels'][
            data['train'].tocsr()[user_id].indices]

        scores = model.predict(user_id, np.arange(n_items))
        top_items = data['item_labels'][np.argsort(-scores)]

        print("User %s" % user_id)
        print("     Known positives:")

        for x in known_positives[:3]:
            print("        %s" % x)

        print("     Recommended:")

        for x in top_items[:3]:
            print("        %s" % x)


with open('model_movielens.pkl', 'rb') as fid:
    model = pickle.load(fid)

    sample_recommendation(model, data, [3, 25, 450])
