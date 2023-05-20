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
        
        # Calculate the percentage change based on previous day's close price
        data['per_change'] = (data['close'] - data['close'].shift(1)) / data['close'].shift(1) * 100

        # Format 'per_change' column to display two decimal places
        data['per_change'] = data['per_change'].apply(lambda x: '{:.2f}'.format(x))
        
        # Save the modified data back to the same file
        data.to_csv(filepath, index=False)
