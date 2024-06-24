# fastapi as backend service
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# module to load the model
from pickle import load

# pydantic to define the structure of body request
from pydantic import BaseModel

# pandas to create the dataframe
import pandas as pd

# ---

# open the model
with open('./model/iris_model.pkl', 'rb') as model:
    iris_model = load(model)

# instanciate FastAPI APP
app = FastAPI()

# define CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to the specific origins you want to allow
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods, including POST, OPTIONS, etc.
    allow_headers=["*"],
)


# define the Request body Structure
# jadi user harus ngirim data di bodynya dengan struktur kaya gini
class LeafUser(BaseModel):
    sepal_length_cm: float
    sepal_width_cm: float 

def json_to_df(input: LeafUser):
    data =  pd.DataFrame({
        'sepal length (cm)': [input.sepal_length_cm],
        'sepal width (cm)': [input.sepal_width_cm]
    })

    return data

# user/client should request to url '/predict-iris'
@app.post("/predict-iris")
async def root(leaf_data: LeafUser):
    print("user input leaf data: ", leaf_data)
    # print("length: ", leaf_data.sepal_length_cm)
    # print("width: ", leaf_data.sepal_width_cm)
    
    # change user request data to dataframe
    request_df = json_to_df(leaf_data)
    print("dataframe:", request_df)

    # predict the request data
    predict_result = iris_model.predict(request_df)
    print("predict_result:", predict_result)
    print("type predict_result:", type(predict_result))

    # get class classification
    # -> this should be automatically saved by `saving encoding data features`
    target_names = ['setosa', 'versicolor', 'virginica']
    target_result = target_names[predict_result[0]]

    return_data = {
        "class classification": int(predict_result[0]),
        "classification name": target_result
    }
    return return_data

    # return "success"