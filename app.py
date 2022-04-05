import dash
import os
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import dash_leaflet as dl
from dash.dependencies import Input, Output, State
from dash_extensions.javascript import Namespace, arrow_function
import plotly.express as px
import plotly.graph_objects as go
from aux.functions import functions
import pandas as pd
import json
import numpy as np
import base64


### Create a instance of Dash class
app = dash.Dash(__name__, 
external_stylesheets = ["https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css",
                        "https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500&display=swap"])
app.title = "Sand_flies_DB"


df = pd.read_csv("data/DATASET_SAND_FLY_RO_MAPS.csv", sep =";", encoding = "ISO-8859-1", low_memory=False)


df.drop(labels = ["Leishmania Detection"], inplace = True, axis = 1)


species_list = df["Species"].values
species_list = list(set(species_list))


#get colnames for dash table
col_names = [{"name": i, "id": i} for i in df.columns]

markers = [dl.Marker(position = [[-63.13,-8.33],[-63.14,-8.34]])]


def plotHB(df):
    bar = go.Bar(
        y = df["Municipality"],
        x = df["count"],
        orientation = "h"
    )
    data = [bar]
    layout = go.Layout(xaxis = {"title": "Abundance"}, margin = {"t": 10})
    return {"data": data, "layout": layout}




### Create dash layout
app.layout = html.Div(

    
    children = [
    
    #create a div with header conf

    ###Header
        html.Div(
            id = "header",
            children = [
                html.Div(
                    children = [

                        #insert sf img
                        html.Img(
                            src = functions.encode_image("assets/sf.png"), className = "header-img"),
                        
                        #inster paper name
                        html.H1(
                            "Updating the knowledge of phlebotomine sand flies in Rondônia State",
                            className = "header-title"
                        ),
                    ],
                    className = "header-cotainer"
                    )
            ],
            className = "header"
        ),

    #create two card template
     #first two plots
    html.Div(

        children = [

            #create the first row
            html.Div(
                children = [
                    dcc.Dropdown(species_list, 
                                id = "species_selector", 
                                style ={"color": "rgb(229 231 235)",
                                         "backgroundColor": "rgb(229 231 235)",
                                         "border-radius": "10px"},
                                value = "No species"),
                ],
                className = "species-selector",
            ),
            html.Div(
                children = [
                    #plot map
                    dl.Map(center = [-11, -63],
                           zoom = 7,
                           children = [
                                dl.TileLayer()
                           ])
                ],
                className = "leaflet-map"
            )

        ],
        className = "card-1"
    ),

    #last plot inline-block
    html.Div(
        children = [
            dcc.Graph(id = "hor_plot",
                     style = {'display': 'grid', 
                              "margin-left": "50px"}),
            dash_table.DataTable(columns = col_names,
                                 data = [],
                                 export_format = "csv", 
                                 id = "dash_table",
                                 page_size=10)
        ],
        className = "card-2"
    )
    ],
    className = "container"
)



#update horizontal plot
@app.callback(Output(component_id = "hor_plot", component_property = "figure"),
              [Input(component_id = "species_selector", component_property = "value")])
def update_graph(species):
    if species == "No species":
        return {"data":[] , "layout": go.Layout(xaxis = {"title": "Abundance"}, margin = {"t": 10})}
    else:
        new_df = df[df["Species"] == species]
        new_df = new_df.groupby(["Municipality"]).size().reset_index(name = "count")
        new_df = new_df.sort_values(by = ["count"], ascending = False)[0:5]
        return plotHB(new_df.sort_values(by = ["count"]))
        
#update table
@app.callback(Output(component_id = "dash_table", component_property = "data"),
              [Input(component_id = "species_selector", component_property = "value")])
def update_table(species):
    if species == "No species":
        pass
    else:
        new_df = df[df["Species"] == species]
        new_df = new_df.to_dict('records')
        return new_df
#run app
if __name__ == '__main__':
    app.run_server(debug = True)