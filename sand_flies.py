import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
from aux.functions import functions
import pandas as pd
import numpy as np
import base64
import planar


### Create a instance of Dash class
app = dash.Dash(__name__,
                meta_tags=[{'name': 'viewport',
                           'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}],
                external_stylesheets = ["https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css",
                                        "https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500&display=swap"])
app.title = "Sand_flies_DB"

server = app.server

df = pd.read_csv("data/DATASET_SAND_FLY_RO_MAPS.csv", sep =";", encoding = "ISO-8859-1", low_memory=False)


#remove some useless columns
df.drop(labels = ["Leishmania Detection", "Subtribes"], inplace = True, axis = 1)


species_list = df["Species"].values
species_list = list(set(species_list))


#get colnames for dash table
col_names = [{"name": i, "id": i} for i in df.columns]


def determine_zoom_level(latitudes, longitudes):
    ###This function return zoom, long and lat
    all_pairs=[]
    for lon, lat in zip(longitudes, latitudes):
        all_pairs.append((lon,lat))
    b_box = planar.BoundingBox(all_pairs)
    area = b_box.height * b_box.width
    zoom = np.interp(area, [0, 5**-10, 4**-10, 3**-10, 2**-10, 1**-10, 1**-5], 
                           [20, 17,   16,     15,     14,     7,      5])
    return zoom, b_box.center



df["Lat"].values
#set map box token
mapbox_access_token = px.set_mapbox_access_token(open("assets/.mapbox_token").read())

def plotHB(df):
    bar = go.Bar(
        y = df["Municipality"],
        x = df["count"],
        orientation = "h"
    )
    data = [bar]
    layout = go.Layout(xaxis = {"title": "Abundance"}, margin = {"t": 10})
    return {"data": data, "layout": layout}



def plotMap(lat, long, text, marker, zoom, box):
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
                lat = box[1],
                lon = box[0]
            ),
            pitch = 0,
            zoom = zoom
        ),
        margin = {"t": 5, "l": 5, "r": 5, "b": 0}
    )
    return fig

### Create dash layout
app.layout = html.Div(

    children = [
    
    #create a div with header conf

    ###Header
        html.Div(
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
                    className = "header-container"
                    )
            ],
            className = "header"
        ),

    #using second row and columns 1/6 to draw a dropdown
    html.Div(

        children = [
            #create the first row
            dcc.Dropdown(species_list,
                        id = "species_selector", 
                        value = "No species"),
            ],
            className = "species-selector"
    ),


    #plot map on thrid row and columns 1/6
    html.Div(
            children = [
                dcc.Graph(id = "map", 
                          config = {'displayModeBar': False})
            ],
            className = "map"
            ),
             

    #last plot inline-block
    html.Div(
        children = [
            dcc.Graph(id = "hor_plot",
                     config = {'displayModeBar': False},
                     style = {'display': 'grid', 
                              "margin-left": "50px",
                              "margin-right": "20px"})
            
        ],
        className = "card-3"
    ),

    
    html.Div(
        children = [
            dash_table.DataTable(columns = col_names,
                                 data = [],
                                 export_format = "csv", 
                                 id = "dash_table",
                                 page_size = 8)
        ],
        className = "card-4"
    )

    ],
    className = "container"
)




#update map
@app.callback(Output(component_id = "map", component_property = "figure"),
              [Input(component_id = "species_selector", component_property = "value")])
def update_map(species):
    if species == "No species":
        _, coord = determine_zoom_level(latitudes = df["Lat"].values, longitudes = df["Long"].values)
        return plotMap(lat = ["-11"], 
                       long = ["-63"], 
                       text = [""], 
                       marker = dict(symbol = "college"),
                       zoom = 0,
                       box = coord)
    else:
        new_df = df[df["Species"] == species]
        new_df = new_df.groupby(["Lat", "Long", "Municipality"]).size().reset_index(name = "count")
        lat = new_df["Lat"].values
        lon = new_df["Long"].values
        text = new_df["Municipality"].values
        zoom, coord = determine_zoom_level(latitudes = new_df["Lat"].values, longitudes = new_df["Long"].values)
        return plotMap(lat = lat,
                       long = lon,
                       text = text,
                       marker = {"size": 15, "symbol": "circle"},
                       zoom = zoom,
                       box = coord
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
    app.run_server(debug=True)