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


    pairs = {}
    ## go trough each input line by line
    for i in range(len(df)):
        first_input = df.iloc[i]['input']
        if i + 1 >= len(df):
            break
        second_input = df.iloc[i+1]['input']
        if pairs.get(first_input) is None:
            pairs[first_input] = {}
        if pairs.get(first_input).get(second_input) is None:
            pairs[first_input][second_input] = []
        pairs[first_input][second_input].append(abs(df.iloc[i]['time_taken'] - df.iloc[i+1]['time_taken']))
        

    pairs_mean = {}
    for first_input, second_dict in pairs.items():
        num =0 
        suma =0  
        for second_input, values in second_dict.items():
            num += 1
            suma += sum(values) / len(values)
        print(f"Me vs others {first_input} , {suma/num}")

    for mean in pairs_mean:
        print(f"{mean}: {pairs_mean[mean]}")


if __name__ == "__main__":
    main()