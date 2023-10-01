from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

# Load the trained model from the pickle file
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

# Render the index.html template for the home page
@app.route('/')
def index():
    return render_template('index2.html')

# Handle the form submission and make predictions
@app.route('/predict', methods=['POST'])
def predict():
    # Get the user inputs from the form
    unit_number = int(request.form['unit_number'])
    time_cycles = int(request.form['time_cycles'])

    # Load the column values from the form and align them with the dataset columns
    columns = ['unit_number', 'time_cycles']
    values = [unit_number, time_cycles]

    dataset_columns = ['unit_number', 'time_cycles', 'setting_1', 'setting_2',
       '(LPC outlet temperature) (◦R)', '(HPC outlet temperature) (◦R)',
       '(LPT outlet temperature) (◦R)', '(bypass-duct pressure) (psia)',
       '(HPC outlet pressure) (psia)', '(Physical fan speed) (rpm)',
       '(Physical core speed) (rpm)', '(HPC outlet Static pressure) (psia)',
       '(Ratio of fuel flow to Ps30) (pps/psia)',
       '(Corrected fan speed) (rpm)', '(Corrected core speed) (rpm)',
       '(Bypass Ratio) ', '(Bleed Enthalpy)',
       '(High-pressure turbines Cool air flow)',
       '(Low-pressure turbines Cool air flow)']

    for column in dataset_columns:
        if column not in columns:
            try:
                column_value = float(request.form[column])
            except KeyError:
                column_value = 0.0  # Set a default value for missing keys
            columns.append(column)
            values.append(column_value)

    # Make predictions using the aligned data
    prediction = model.predict([values])[0]

    # Render the result.html template with the prediction
    return render_template("result.html", prediction_text = "The RUL is {}".format(prediction))

if __name__ == '__main__':
    app.run(debug=True)