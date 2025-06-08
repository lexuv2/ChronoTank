FILENAME = "pico_w5500_results.csv"

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from plotly.subplots import make_subplots

def main():
    # Read the CSV file
    df = pd.read_csv(FILENAME)

    # Display the first few rows of the DataFrame
    print(df.head())

    # Display basic statistics about the DataFrame
    print(df.describe())


    fig = go.Figure()

    ### simple plot all times for every input
    for input_name in df['input'].unique():
        data = df[df['input'] == input_name]['time_taken']
        fig.add_trace(go.Scatter(
            x=np.arange(len(data)),  # Use the index as x-axis
            y=data,
            mode='lines+markers',
            name=input_name
        ))
    fig.update_layout(
        title="Time Taken for Each Input",
        xaxis_title="Index",
        yaxis_title="Time Taken (ns)",
        legend_title="Input"
    )
    fig.show()

        

if __name__ == "__main__":
    main()