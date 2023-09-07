import matplotlib as plt
import pandas as  pd

df = pd.read_csv("./accidents_statistics2021/honhyo_2021.csv", encoding='cp932')

df_person = df[df["事故類型"]==1].reset_index()
df_person['年齢（当事者A）'].hist(bins=50)
df_person['年齢（当事者B）'].hist(bins=50, alpha=0.5)