import os
import pandas as pd

# Directory containing the CSV files
directory = './data/company-wise'

# Iterate through each file in the directory
for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        # Read the CSV file
        filepath = os.path.join(directory, filename)
        data = pd.read_csv(filepath)

        # Convert NaN values to 0.0
        data.fillna(0.0, inplace=True)

        # Filter the data based on the published_date condition
        filtered_data = data[data['published_date'] <= '2018-02-18'].copy()

        # Calculate the percentage change based on previous day's close price
        filtered_data['per_change'] = (filtered_data['close'] - filtered_data['close'].shift(1)) / filtered_data['close'].shift(1) * 100

        # Format 'per_change' column to display two decimal places
        filtered_data['per_change'] = filtered_data['per_change'].apply(lambda x: '{:.2f}'.format(x))

        # Convert '0.00' values to 0.0
        filtered_data['per_change'] = filtered_data['per_change'].replace('0.00', '0.0')

        # Save the modified 'per_change' values back to the original data
        data.loc[filtered_data.index, 'per_change'] = filtered_data['per_change']

        # Save the modified data back to the same file
        data.to_csv(filepath, index=False)
