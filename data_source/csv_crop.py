import pandas as pd

# Load the original dataset
# Replace 'your_dataset.csv' with your actual file name
df = pd.read_csv('preprocess_dataset.csv')

# There's a discrepancy in your request - you mentioned both 4k and 6k rows
# I'll create code for both options

# For 4,000 rows
df_4k = df.tail(1000)  # Takes the first 4,000 rows
df_4k.to_csv('dataset_1k_rows_last.csv', index=False)

# For 6,000 rows
# df_6k = df.head(6000)  # Takes the first 6,000 rows
# df_6k.to_csv('dataset_6k_rows.csv', index=False)

# # If you want random rows instead of the first rows:
# df_random_4k = df.sample(n=4000, random_state=42)  # Random 4,000 rows
# df_random_4k.to_csv('dataset_random_4k_rows.csv', index=False)

# df_random_6k = df.sample(n=6000, random_state=42)  # Random 6,000 rows
# df_random_6k.to_csv('dataset_random_6k_rows.csv', index=False)