import pandas as pd

class df_test():
    def __init__(self):
        pass

    def create_df(self):
        self.my_df = pd.DataFrame({
            'col_a': [1, 2, 3],
            'col_b': [4, 5, 6],
            'col_c': [7, 8, 9],
            'col_d': [10, 11, 12],
        })

    def append_row(self):
        self.list_row = [4, 7, 10, 13]
        self.my_df.loc[len(self.my_df)] = self.list_row

if __name__ == '__main__':
    o_df = df_test()
    o_df.create_df()
    o_df.append_row()
    print(o_df.my_df.to_string())
