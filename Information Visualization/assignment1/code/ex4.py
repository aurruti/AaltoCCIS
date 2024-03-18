import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Read the CSV file into a DataFrame
df = pd.read_csv('Penguins.csv')
df = df.drop(df.columns[0], axis=1)
df = df.replace('NA', pd.NA)

# Convert the relevant columns to numeric
numeric_cols = ['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g','year']
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

# Create a pairplot for the DataFrame
pair_grid = sns.pairplot(df, diag_kind='hist',diag_kws=dict(fill=False))

# Tweak and display the plot
pair_grid.map_offdiag(sns.scatterplot, size=df["island"])
pair_grid.map_upper(sns.scatterplot, hue=df['sex'], markers=['o','s'])
pair_grid.map_lower(sns.scatterplot, hue=df["species"], palette=["red", "blue", "green"])
pair_grid.add_legend(title="", adjust_subtitles=True)
plt.show()

