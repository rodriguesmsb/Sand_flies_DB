library("shiny")
library("shinyWidgets")
library("leaflet")
library("highcharter")
library("shinyalert")
library("rintrojs")



shinyUI(shiny::bootstrapPage(
      
      useShinydashboard(),
      useShinyalert(),
      introjsUI(),
      
      fluidPage(
            
            #create a fluid row to hold article name
            fluidRow(
                  column(2),
                  column(8,
                         HTML("<br><br><center> <h1>Article Name</h1> </center><br>")
                  ),
                  column(2)
            ),
            fluidRow(
                  style = "height:50px;"),
            tags$hr(),
            
            #add explanation about paper
            fluidRow(
                  column(2),
                  column(8,
                         h4("Lorem Ipsum is simply dummy text of the printing and typesetting industry.
                            Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, 
                            when an unknown printer took a galley of type and scrambled it to make a type 
                            specimen book. It has survived not only five centuries, but also the leap 
                            into electronic typesetting, remaining essentially unchanged. It was 
                            popularised in the 1960s with the release of Letraset sheets containing 
                            Lorem Ipsum passages, and more recently with desktop publishing software 
                            like Aldus PageMaker including versions of Lorem Ipsum.", 
                            style="text-align: justify;"),
                         br(),
                         column(width = 3, offset = 5,actionBttn(inputId = "geral_tour", label = "Tour"))
                  ),
                  column(2)
            ),
            
            
            
            
            )
      
      )
      )
      
     
      
     
