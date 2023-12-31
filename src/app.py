import joblib 
import pandas as pd
import gradio as gr
import warnings

warnings.filterwarnings("ignore")

model= joblib.load("model\LR.joblib")

model

data= pd.read_csv("data\Vodafone_churn.csv")
data

##testing our model
model.predict(data)

##creating a function to return a string depending on the output of the model

def classify(num):
    if num == 0:
        return "Customer will not Churn"
    else:
        return "Customer will churn"



def predict_churn(SeniorCitizen, Partner, Dependents, tenure, InternetService,
                  OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport,
                  StreamingTV, StreamingMovies, Contract, PaperlessBilling,
                  PaymentMethod, MonthlyCharges, TotalCharges): 

     
##create a list of my input features

    input_data = [
        SeniorCitizen, Partner, Dependents, tenure, InternetService,
        OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport,
        StreamingTV, StreamingMovies, Contract, PaperlessBilling,
        PaymentMethod, MonthlyCharges, TotalCharges
    ]    
##changing features into a dataframe

    input_df = pd.DataFrame([input_data], columns=[
        "SeniorCitizen", "Partner", "Dependents", "tenure", "InternetService",
        "OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport",
        "StreamingTV", "StreamingMovies", "Contract", "PaperlessBilling",
        "PaymentMethod", "MonthlyCharges", "TotalCharges"
    ])


    pred = model.predict(input_df) ## prediction on the input data.

    output = classify(pred[0]) 

    if output == "Customer will not Churn":
        return [(0, output)]
    else:
        return [(1, output)]   
    
output = gr.outputs.HighlightedText(color_map={
    "Customer will not Churn": "green",
    "Customer will churn": "red"
}) ##assigning colors to output 

##building my interface and wrapping my model in the function

gui= gr.Blocks() ##instatiating my blocks class

with gui:
    gr.Markdown(""" # Welcome to My Customer Churn Prediction App""")
    
    input=[gr.inputs.Slider(minimum=0, maximum= 1, step=1, label="SeniorCitizen: Select 1 for Yes and 0 for No"),
        gr.inputs.Radio(["Yes", "No"], label="Partner: Do You Have a Partner?"),
        gr.inputs.Radio(["Yes", "No"], label="Dependents: Do You Have a Dependent?"),
        gr.inputs.Number(label="tenure: How Long Have You Been with Vodafone in Months?"),
        gr.inputs.Radio(["DSL", "Fiber optic", "No"], label="What Internet Service Do You Use?"),
        gr.inputs.Radio(["Yes", "No", "No internet service"], label="Do You Have Online Security?"),
        gr.inputs.Radio(["Yes", "No", "No internet service"], label="Do You Have Any Online Backup Service?"),
        gr.inputs.Radio(["Yes", "No", "No internet service"], label="Do You Use Any Device Protection?"),
        gr.inputs.Radio(["Yes", "No", "No internet service"], label="Do You Use TechSupport?"),
        gr.inputs.Radio(["Yes", "No", "No internet service"], label="Do You Stream TV?"),
        gr.inputs.Radio(["Yes", "No", "No internet service"], label="Do You Stream Movies?"),
        gr.inputs.Radio(["Month-to-month", "One year", "Two year"], label="What Is Your Contract Type?"),
        gr.inputs.Radio(["Yes", "No"], label=" Do You Use Paperless Billing?"),
        gr.inputs.Radio([
            "Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"
        ], label="What Payment Method Do You Use?"),
        gr.inputs.Number(label="What is you Monthly Charges?"),
        gr.inputs.Number(label="How Much Is Your Total Charges?")]
     
    output= gr.outputs.HighlightedText(color_map={
     "Customer will not Churn": "green",
     "Customer will churn": "red"}, label= "Your Output")     
    predict_btn= gr.Button("Predict")
     
    predict_btn.click(fn= predict_churn, inputs= input, outputs=output)

gui.launch(share=True)
    

