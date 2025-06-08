import pandas as pd
import plotly.graph_objects as go

FILENAME = "pico_w5500_results.csv"

def main():
    # Read the CSV file
    df = pd.read_csv(FILENAME)

    # # Remove outliers in time_taken
    # q1 = df['time_taken'].quantile(0.25)
    # q3 = df['time_taken'].quantile(0.75)
    # iqr = q3 - q1
    # lower_bound = q1 - 1.5 * iqr
    # upper_bound = q3 + 1.5 * iqr
    # df = df[(df['time_taken'] >= lower_bound) & (df['time_taken'] <= upper_bound)]

    # Get unique inputs for creating individual CDFs
    unique_inputs = df['input'].unique()

    # Create CDF plot for each input group
    fig = go.Figure()
    for input_name in unique_inputs:
        data = df[df['input'] == input_name]['time_taken'].sort_values()
        yvals = (range(1, len(data) + 1))
        yvals = [y / len(data) for y in yvals]
        fig.add_trace(go.Scatter(
            x=data,
            y=yvals,
            mode='lines',
            name=input_name
        ))

    # Update layout
    fig.update_layout(
        title='Interactive CDF of Time Taken by Input (Click legend to toggle)',
        xaxis_title='Time Taken (ms)',
        yaxis_title='Cumulative Probability',
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
    fig.write_html('interactive_cdf.html')
    fig.show()

if __name__ == "__main__":
    main()
