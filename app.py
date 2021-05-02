from flask import Flask, render_template, redirect, request as flask_request
import apiai
import json
import sys
import os
from framingham_predict import model_prediction

import cv2
import tkinter as tk
from tkinter import filedialog
from landmark_predict import model_predict


#APIAI_CLIENT_ACCESS_TOKEN = "3013744b31ff4b7ba94f8aed23194df0"
APIAI_CLIENT_ACCESS_TOKEN ="5dec7be2c7754c0e85f730cb518981d0"

app = Flask(__name__)

api_ai = apiai.ApiAI(APIAI_CLIENT_ACCESS_TOKEN)

lmrk=['atm','bridge','petrol pump','temple','others']

def __parse_input_params(params): 

    data = { 
        'trigger':0,
    }
    
    if params.get('number'):
        data['trigger'] = 1
    return data


@app.route("/")
def root():
    return render_template('index.html')


@app.route('/api_ai_test', methods=['POST'])
def apiAiTEst():

    requestData = flask_request.json

    if requestData["query"]:
        session_id = "1234567890"
        if requestData["session_id"]:
            session_id = str(requestData["session_id"])

        request = api_ai.text_request()
        request.session_id = session_id

        request.query = requestData["query"]

        response = request.getresponse()
        response = json.loads(response.read().decode('utf-8'))

        # print(json.dumps(response, indent=2))

        print("~" * 30)

        if response.get("result").get("parameters").get("number"):
            data = __parse_input_params(response.get("result").get("parameters"))
            print(data)
            
            application_window = tk.Tk()
            my_filetypes = [('all files', '.*'), ('Image file', '.jpg')]

            answer = filedialog.askopenfilename(parent=application_window,
                                    initialdir=os.getcwd(),
                                    title="Please select a file:",
                                    filetypes=my_filetypes)

            test_image = cv2.imread(answer)


            #return_message = 'The class is  atm'

            result = model_predict(answer)
            print(type(result))
            print('result =', result)
            
            if result:
                return_message = 'The landmark is '+lmrk[int(result)]+'.'
            

            returnData = {
                "status": True,
                "message": return_message,
                "session_refresh": True
            }

            return json.dumps(returnData)
        else:
            responseValue = response.get("result").get(
                "fulfillment").get("speech")

            returnData = {
                "status": True,
                "message": responseValue
            }

            return json.dumps(returnData)
    else:

        returnData = {
            "status": False,
            "message": ""
        }

    return json.dumps(returnData)


if __name__ == '__main__':
    app.debug = True
    app.run(port=9067)
