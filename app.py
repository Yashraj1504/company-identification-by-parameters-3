from flask import Flask, render_template, request
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

def get_company_data_structured(df, company_name):
    filtered_data = df[df['Company Name'] == company_name]
    if filtered_data.empty:
        return None
    
    company_name_val = company_name
    logo_names = filtered_data['Logo Name'].dropna().tolist()
    status = filtered_data['Status'].dropna().unique().tolist()

    structured_data = pd.DataFrame({
        'Company Name': [company_name_val] + [''] * (len(logo_names) - 1),
        'Logo Name': logo_names,
        'Status': [', '.join(status)] + [''] * (len(logo_names) - 1)
    })
    return structured_data

@app.route('/', methods=['GET', 'POST'])
def index():
    df = load_data()
    structured_output = None
    not_found = False

    if df.empty:
        return "Error: Unable to load company data."

    if request.method == 'POST':
        company_name = request.form.get("company_name")
        structured_output = get_company_data_structured(df, company_name)
        if structured_output is None:
            not_found = True

    return render_template('index.html', structured_output=structured_output, not_found=not_found)

if __name__ == '__main__':
    app.run(debug=True)
