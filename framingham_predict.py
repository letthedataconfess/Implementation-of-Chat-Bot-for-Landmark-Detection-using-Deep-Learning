import pandas as pd
import pickle



filename = 'notebook/finalized_model.sav'

loaded_model = pickle.load(open(filename, 'rb'))


def model_prediction(data):

    # data = { 
    #     'male': 1,
    #     'age': 39,
    #     'cigsPerDay': 19,
    #     'BPMeds': 0,
    #     'prevalentStroke': 0,
    #     'prevalentHyp': 0,
    #     'diabetes': 0,
    #     'totChol': 195,
    #     'BMI': 26.97,
    #     'heartRate': 80
    # }

    # data.values()


    response = loaded_model.predict([list(data.values())])

    return response[0]

