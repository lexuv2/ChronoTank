import pandas as pd
import plotly.graph_objects as go
from scipy.stats import mannwhitneyu

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

    # mannwhitneyu test for each pair of inputs

    unique_inputs = df['input'].unique()
    results = []
    for i in range(len(unique_inputs)):
        print(f"Processing input {i + 1}/{len(unique_inputs)}: {unique_inputs[i]}")
        for j in range(i + 1, len(unique_inputs)):
            input1 = unique_inputs[i]
            input2 = unique_inputs[j]
            data1 = df[df['input'] == input1]['time_taken']
            data2 = df[df['input'] == input2]['time_taken']
            stat, p_value = mannwhitneyu(data1, data2)
            results.append({
                'input1': input1,
                'input2': input2,
                'statistic': stat,
                'p_value': p_value
            })
    results_df = pd.DataFrame(results)
    ## sort by p_value
    results_df = results_df.sort_values(by='p_value')
    print(results_df)

if __name__ == "__main__":
    main()
