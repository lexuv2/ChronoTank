FILENAME = "pico_w5500_results.csv"

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

def main():
    # Read the CSV file
    df = pd.read_csv(FILENAME)

    # Display the first few rows of the DataFrame
    print(df.head())

    # Display basic statistics about the DataFrame
    print(df.describe())

    """
                input  time_taken  time_delta
0  admin5AAAAAAAA       29624  1051417177
1  adminsecret123       31782    34710990
2  adminaAAAAAAAA       26702    29948428
3  adminqAAAAAAAA       36705    39942643
4  adminvAAAAAAAA       35053    38415936

    
    """

    # remove outliers in time_taken
    q1 = df['time_taken'].quantile(0.25)
    q3 = df['time_taken'].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    df = df[(df['time_taken'] >= lower_bound) & (df['time_taken'] <= upper_bound)]


    # bin by input
    df_grouped = df.groupby('input')


    # Display statistics for each group
    for name, group in df_grouped:
        print(f"Group: {name}")
        print(group.head())





    ## create overlapping histogram of time_taken for each group
    fig = go.Figure()
    
    # Get unique inputs for creating individual histograms
    unique_inputs = df['input'].unique()
    
    # Create histogram for each input group
    for input_name in unique_inputs:
        data = df[df['input'] == input_name]['time_taken']
        fig.add_trace(go.Histogram(
            x=data,
            name=input_name,
            opacity=0.7,
            nbinsx=100,
            histnorm='probability density'
        ))
    
    # Update layout
    fig.update_layout(
        title='Interactive Histogram of Time Taken by Input (Click legend to toggle)',
        xaxis_title='Time Taken (ms)',
        yaxis_title='Density',
        barmode='overlay',
        width=1200,
        height=600,
        legend=dict(
            x=1.05,
            y=1,
            xanchor='left',
            yanchor='top'
        )
    )
    
    # Save and show
    fig.write_html('interactive_histogram.html')
    fig.show()


if __name__ == "__main__":
    main()