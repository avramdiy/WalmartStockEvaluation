import os
from flask import Flask, render_template
import pandas as pd

app = Flask(__name__, template_folder=os.path.abspath("templates"))


@app.route("/")
def load_dataframe():
    # Path to the data file
    data_path = r"C:\Users\Ev\Desktop\TRG Week 13\walmart_stock_prices.csv"
    
    # Load data into a pandas DataFrame
    df = pd.read_csv(data_path)

    df = df.drop(columns=["Dividends", "Stock Splits"], errors="ignore")
    
    # Convert DataFrame to HTML table
    df_html = df.to_html(classes="table table-striped", index=False)
    
    # Pass the HTML table to the template
    return render_template("table.html", table=df_html)

if __name__ == "__main__":
    app.run(debug=True)
