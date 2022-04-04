import dash
import os
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash_leaflet as dl
from dash_leaflet import express as dlx
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


df = pd.read_csv("data/Dataset_cons.csv")
species_list = df["Species"].values
species_list = list(set(species_list))

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
                    dcc.Dropdown(species_list, id = "species_selector", style ={"color": "rgb(229 231 235)",
                                                                                "backgroundColor": "rgb(229 231 235)",
                                                                                "border-radius": "10px"}),
                ],
                className = "species-selector",
            )

        ],
        className = "card-1"
    ),

    #last plot
    html.Div(
        children = [],
        className = "card-2"
    )
    ],
    className = "container"
)


#run app
if __name__ == '__main__':
    app.run_server()