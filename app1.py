"""
from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

def load_data():
    try:
        df = pd.read_excel("static/Yash.xlsx")
        df['Company Name'] = df['Company Name'].fillna(method='ffill')
        return df
    except Exception as e:
        print(f"Error loading file: {e}")
        return pd.DataFrame()

@app.route('/get_logos', methods=['GET'])
def get_logos():
    company_name = request.args.get('company_name')
    df = load_data()
    filtered_data = df[df['Company Name'] == company_name]
    logos = filtered_data['Logo Name'].dropna().unique().tolist()
    return jsonify(logos)

@app.route('/', methods=['GET', 'POST'])
def index():
    df = load_data()
    structured_output = None
    not_found = False
    company_names = df['Company Name'].unique().tolist()

    if df.empty:
        return "Error: Unable to load company data."

    if request.method == 'POST':
        company_name = request.form.get("company_name")
        logo_name = request.form.get("logo_name")
        filtered_data = df[(df['Company Name'] == company_name) & (df['Logo Name'] == logo_name)]
        if filtered_data.empty:
            not_found = True
        else:
            structured_output = filtered_data
        print(filtered_data)
    return render_template('index1.html', structured_output=structured_output, not_found=not_found ,company_names=company_names)

if __name__ == '__main__':
    app.run(debug=True)
"""

from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

def load_data():
    try:
        df = pd.read_excel("static/Yash.xlsx")
        df['Logo Name'] = df['Logo Name'].fillna(method='ffill')
        df["Status"] = df["Status"].fillna(method="ffill")
        df["CIN"] = df["CIN"].fillna(method="ffill")
        #df["ROC"] = df["ROC"].fillna(method="ffill")
        return df
    except Exception as e:
        print(f"Error loading file: {e}")
        return pd.DataFrame()

@app.route('/get_logos', methods=['GET'])
def get_logos():
    company_name = request.args.get('company_name')
    df = load_data()
    filtered_data = df[df['Logo Name'] == company_name]
    logos = filtered_data['Branch Name'].dropna().unique().tolist()
    return jsonify(logos)

@app.route('/', methods=['GET', 'POST'])
def index():
    df = load_data()
    structured_output = None
    not_found = False
    company_names = df['Logo Name'].unique().tolist()

    if df.empty:
        return "Error: Unable to load company data."

    if request.method == 'POST':
        company_name = request.form.get("company_name")
        logo_name = request.form.get("logo_name")
        filtered_data = df[(df['Logo Name'] == company_name) & (df['Branch Name'] == logo_name)]
        if filtered_data.empty:
            not_found = True
        else:
            # Convert DataFrame to list of dictionaries
            structured_output = filtered_data.to_dict(orient='records')

    return render_template('index2.html', structured_output=structured_output, not_found=not_found, company_names=company_names)

if __name__ == '__main__':
    app.run(debug=True)

