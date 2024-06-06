from flask import Flask, request, render_template
import joblib
import pandas as pd
from sql import insert_client, insert_result, create_tables
import traceback

app = Flask(__name__)

# Load the trained model
model = joblib.load('model.pkl')
model_columns = [' no_of_dependents',' income_annum',' loan_amount',' loan_term',' cibil_score',
                 ' residential_assets_value',' commercial_assets_value',' luxury_assets_value',' bank_asset_value',' education_ Not Graduate',' self_employed_ Yes']

def initialize():
    create_tables()
    
initialize()

@app.route('/')
def home():
    return render_template('index.html', form_data={})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Retrieve input values from the form
        form_data = request.form
        print("Form Data:", form_data)  # Debugging
        
        # Create a DataFrame with the input values
        input_data = pd.DataFrame([{
            ' no_of_dependents': int(form_data[' no_of_dependents']),
            ' income_annum': int(form_data[' income_annum']),
            ' loan_amount': int(form_data[' loan_amount']),
            ' loan_term': int(form_data[' loan_term']),
            ' cibil_score': int(form_data[' cibil_score']),
            ' residential_assets_value': int(form_data[' residential_assets_value']),
            ' commercial_assets_value': int(form_data[' commercial_assets_value']),
            ' luxury_assets_value': int(form_data[' luxury_assets_value']),
            ' bank_asset_value': int(form_data[' bank_asset_value']),
            ' education_ Not Graduate': int(form_data[' education_ Not Graduate']),
            ' self_employed_ Yes': int(form_data[' self_employed_ Yes']),
            
        }])
        
        print("Input Data DataFrame:", input_data)  # Debug: Print DataFrame

        input_data = pd.get_dummies(input_data)
        input_data = input_data.reindex(columns=model_columns, fill_value=0)
        
        print("Input Data for Prediction:", input_data)  # Debugging

        # Make prediction
        prediction = model.predict(input_data)

        # Interpret the result
        result = 'Approved' if prediction[0] == 1 else 'Rejected'
        
        client_id = insert_client(form_data)
        
        
        # Insert into results table
        insert_result(client_id, result)

        return render_template('index.html', form_data=form_data, result=result)
    except Exception as e:
        print("Exception occurred:", e)  # Print the exception traceback for debugging
        traceback.print_exc()
        return render_template('index.html', form_data=form_data, result='Error')


if __name__ == '__main__':
    app.run(debug=True)
