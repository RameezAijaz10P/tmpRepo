import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv("CSVs/even-mega-data.csv")
df = df.drop_duplicates()

df,df_test = train_test_split(df, test_size=0.2, random_state=42)
df.to_csv('CSVs/trainData.csv', index=False)
df_test.to_csv('CSVs/testData.csv', index=False)
