import numpy as np
from lightfm.datasets import fetch_movielens
import pickle


data = fetch_movielens(min_rating=5.0)


print(repr(data['train']))
print(repr(data['test']))


from lightfm import LightFM


model = LightFM(loss='warp')
model.fit(data['train'], epochs=30, num_threads=2)


from lightfm.evaluation import precision_at_k


print("Train precision: %.2f" %
      precision_at_k(model, data['train'], k=5).mean())
print("Test precision: %.2f" % precision_at_k(model, data['test'], k=5).mean())


# save the model
with open('model_movielens.pkl', 'wb') as fid:
    pickle.dump(model, fid)
    print("model saved")
