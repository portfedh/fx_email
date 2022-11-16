import pandas as pd

df1 = pd.DataFrame({
    'col_a': [1, 2, 3],
    'col_b': [4, 5, 6],
    })
df2 = pd.DataFrame({
    'col_a': [7, 8, 9],
    'col_b': [10, 11, 12],
    })

print(df1)
print(df2)
df3 = pd.concat([df1, df1])
print(df3)

# actual = db.concat_df(df1, df2, type=1)
# result = pd.concat(list, axis=type)
