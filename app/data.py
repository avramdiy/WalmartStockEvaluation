import os
from flask import Flask, render_template
import pandas as pd
import plotly.express as px
import plotly.io as pio

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

@app.route("/average-open-weekly")
def average_open_weekly():

    data_path = r"C:\Users\Ev\Desktop\TRG Week 13\walmart_stock_prices.csv"

    df = pd.read_csv(data_path)

    df['Date'] = pd.to_datetime(df['Date'], errors='coerce', utc=True)

    print("After conversion, first few rows of the 'Date' column:", df['Date'].head())
    
    df = df.dropna(subset=['Date'])

    df['Date'] = df['Date'].dt.tz_localize(None)

    df.set_index('Date', inplace=True)

    if not isinstance(df.index, pd.DatetimeIndex):
        raise ValueError("The index is not a DatetimeIndex. Ensure that the 'Date' column is correctly converted.")

    weekly_avg_open = df['Open'].resample('W').mean().reset_index()

    fig = px.line(weekly_avg_open, x='Date', y='Open', title="Weekly Average 'Open' Prices")

    graph_html = pio.to_html(fig, full_html=False)

    return render_template("graph.html", graph=graph_html)

if __name__ == "__main__":
    app.run(debug=True)
