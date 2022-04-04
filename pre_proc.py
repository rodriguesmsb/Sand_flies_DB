import pandas as pd



data = pd.read_excel("data/DATASET_SAND_FLY_RO_MAPS.xlsx")

data = data.groupby(["Paper", "Subtribes", "Municipality", "Long", "Lat", "Species"])["Species"].size().reset_index(name = "contagem")
print(data)

data.to_csv("data/Dataset_cons.csv", index = False)