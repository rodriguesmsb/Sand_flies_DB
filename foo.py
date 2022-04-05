from dash import Dash, dash_table
import pandas as pd

df = pd.read_csv("data/DATASET_SAND_FLY_RO_MAPS.csv", sep =";", encoding = "ISO-8859-1", low_memory=False)


app = Dash(__name__)

col_names = [{"name": i, "id": i} for i in df.columns]
table_data = df.to_dict('records')



app.layout = dash_table.DataTable(columns = col_names, 
                                  data = table_data,
                                  export_format = 'csv', 
                                  id = "dash_table")

if __name__ == '__main__':
    app.run_server(debug=True)