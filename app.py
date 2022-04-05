import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
from aux.functions import functions
import pandas as pd
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


#set map box token
mapbox_access_token = px.set_mapbox_access_token(open(".mapbox_token").read())


def plotHB(df):
    bar = go.Bar(
        y = df["Municipality"],
        x = df["count"],
        orientation = "h"
    )
    data = [bar]
    layout = go.Layout(xaxis = {"title": "Abundance"}, margin = {"t": 10})
    return {"data": data, "layout": layout}



def plotMap(lat, long, text, marker):
    fig = go.Figure(go.Scattermapbox(
        lat = lat, 
        lon = long,
        mode = 'markers',
        marker = marker,
        text = text
        )
    )

    fig.update_layout(
        hovermode = 'closest',
        mapbox_style = "open-street-map",
        mapbox = dict(
            accesstoken = mapbox_access_token,
            bearing = 0,
            center = go.layout.mapbox.Center(
                lat = -11,
                lon = -63
            ),
            pitch = 0,
            zoom = 6
        )
    )
    return fig

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
                    # dl.Map(center = [-11, -63],
                    #        zoom = 7,
                    #        children = [
                    #             dl.TileLayer()
                    #        ])
                    dcc.Graph(id = "map", config = {'displayModeBar': False})
                    
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




#update map
@app.callback(Output(component_id = "map", component_property = "figure"),
              [Input(component_id = "species_selector", component_property = "value")])
def update_map(species):
    if species == "No species":
        return plotMap(lat = ["-11"], 
                       long = ["-63"], 
                       text = [""], 
                       marker = dict(symbol = "college", size = 0))
    else:
        new_df = df[df["Species"] == species]
        new_df = new_df.groupby(["Lat", "Long", "Municipality"]).size().reset_index(name = "count")
        lat = new_df["Lat"].values
        lon = new_df["Long"].values
        text = new_df["Municipality"].values
        return plotMap(lat = lat,
                       long = lon,
                       text = text,
                       marker = go.scattermapbox.Marker(size = 9)
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
    app.run_server()