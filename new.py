

import pandas as pd
import webbrowser

import dash
import dash_html_components as html
from dash.dependencies import Input, Output 
import dash_core_components as dcc 
import plotly.graph_objects as go  
import plotly.express as px
from dash.exceptions import PreventUpdate

app = dash.Dash()

 
def open_browser():

 webbrowser.open_new('http://127.0.0.1:8050/')


def read_data():
    dataset_name = "globalterror_2.csv"
    global df
    df = pd.read_csv(dataset_name)
    

    global attacktype_list 
    attacktype_list = [{"label": str(i), 'value': str(i)} for i in sorted(df['attacktype1_txt'].unique().tolist())]    
    
    global month_list
    month = {
         "January":1,
         "February": 2,
         "March": 3,
         "April":4,
         "May":5,
         "June":6,
         "July": 7,
         "August":8,
         "September":9,
         "October":10,
         "November":11,
         "December":12
         }
      
    month_list= [{"label":key, "value":values} for key,values in month.items()]
    global date_list
    date_list = [x for x in range(1, 32)]

    global region_list
    region_list = [{"label": str(i), "value": str(i)}  for i in sorted( df['region_txt'].unique().tolist() ) ]
  
    global country_list
    country_list = df.groupby("region_txt")["country_txt"].unique().apply(list).to_dict()
    print(country_list)
    
    global state_list
    state_list = df.groupby("country_txt")["provstate"].unique().apply(list).to_dict()

    global city_list
    city_list  = df.groupby("provstate")["city"].unique().apply(list).to_dict()

    global attack_type_list
    attack_type_list = [{"label": str(i), "value": str(i)}  for i in df['attacktype1_txt'].unique().tolist()]

    global year_list
    year_list = sorted ( df['iyear'].unique().tolist()  )

    global year_dict
    year_dict = {str(year): str(year) for year in year_list}
    global chart_dropdown_values
    chart_dropdown_values = {"Terrorist Organisation":'gname', 
                             "Target Nationality":'natlty1_txt', 
                             "Target Type":'targtype1_txt', 
                             "Type of Attack":'attacktype1_txt', 
                             "Weapon Type":'weaptype1_txt', 
                             "Region":'region_txt', 
                             "Country Attacked":'country_txt'
                          }
                              
    chart_dropdown_values = [{"label":keys, "value":value} for keys, value in chart_dropdown_values.items()]
  

def create_app_ui():


  main_layout = html.Div([
  html.H1('Terrorism Analysis with Insights', id='Main_title'),
  dcc.Tabs(id="Tabs", value="Map",children=[
      dcc.Tab(label="Map tool" ,id="Map tool",value="Map", children=[
          dcc.Tabs(id = "subtabs", value = "WorldMap",children = [
              dcc.Tab(label="World Map tool", id="World", value="WorldMap"),
              dcc.Tab(label="India Map tool", id="India", value="IndiaMap")
              ]),
          dcc.Dropdown(id='dropdown1',
                  options=month_list,
                  placeholder = 'select month',
                  multi = True
                  ),
                    
          dcc.Dropdown(id='dropdown2',
                 placeholder='select Day',
                 multi = True
                 ),
                 
          

        dcc.Dropdown(id='dropdown3',
                  options=region_list,
                  placeholder = 'select region',
                  multi = True
                  ),
          
        dcc.Dropdown(id='dropdown4',
                  options= [{'label': 'All', 'value': 'All'}],
                  placeholder ='select_country',
                  multi = True
                  ),
                  
                  
        dcc.Dropdown(id='dropdown5',
                     options= [{'label': 'All', 'value': 'All'}],
                  placeholder ='select_state',
                  multi = True
                  ),
     
        dcc.Dropdown(
                  id='city-dropdown', 
                  options= [{'label': 'All', 'value': 'All'}],
                  placeholder='select_city',
                  multi = True
                  ),
     
     
     
        dcc.Dropdown(id='dropdown7',
                 options=attacktype_list,
                  placeholder = 'select attack',   
                  multi = True
                  ),
        
     html.Br(),
     html.H5('Select the Year', id='year_title'),
     dcc.RangeSlider(
     id='year-slider',
     min = min(year_list) ,
     max = max(year_list),
     value =[min(year_list),max(year_list)],
     marks = year_dict,
     step=None
     ),                
     
     
     html.Br()
    ]),
      
    dcc.Tab(label = "Chart Tool", id="chart tool", value="Chart", children=[
          dcc.Tabs(id = "subtabs2", value = "WorldChart",children = [
              dcc.Tab(label="World Chart tool", id="WorldC", value="WorldChart", children = [          
                  dcc.Dropdown(id="Chart_Dropdown", options = chart_dropdown_values, placeholder="Select option", value = "region_txt"), 
                  html.Br(),
                  html.Br(),
                  html.Hr(),
                  dcc.Input(id="search", placeholder="Search Filter"),
                  html.Hr(),
                  html.Br(),
                  dcc.RangeSlider(
                    id='cyear_slider',
                    min=min(year_list),
                    max=max(year_list),
                    value=[min(year_list),max(year_list)],
                    marks=year_dict,
                    step=None
                      ),
                  html.Br()
                  ]),
              dcc.Tab(label="India Chart tool", id="IndiaC", value="IndiaChart", children = [])
              ]),
         ])
     ]),
  html.Div(id = "graph-object", children ="Graph will be shown here")
  ])

  return main_layout

@app.callback(
    dash.dependencies.Output('graph-object', 'children'),
    [
     dash.dependencies.Input("Tabs", "value"),
    dash.dependencies.Input('dropdown1', 'value'),
    dash.dependencies.Input('dropdown2', 'value'),
    dash.dependencies.Input('dropdown3', 'value'),
    dash.dependencies.Input('dropdown4', 'value'),
    dash.dependencies.Input('dropdown5', 'value'),
    dash.dependencies.Input('city-dropdown', 'value'),
    dash.dependencies.Input('dropdown7', 'value'),
    dash.dependencies.Input('year-slider', 'value'),
    dash.dependencies.Input('cyear_slider', 'value'),
    dash.dependencies.Input("Chart_Dropdown", "value"),
    dash.dependencies.Input("search", "value"),
    dash.dependencies.Input("subtabs2", "value")     
     ]
    )
def update_app_ui(Tabs, month_value, date_value,region_value,country_value,state_value,city_value,attack_value,year_value, chart_year_selector, chart_dp_value, search,
                   subtabs2):
    fig = None
     
    if Tabs == "Map":
        print("Data Type of month value = " , str(type(month_value)))
        print("Data of month value = " , month_value)
        
        print("Data Type of Day value = " , str(type(date_value)))
        print("Data of Day value = " , date_value)
        
        print("Data Type of region value = " , str(type(region_value)))
        print("Data of region value = " , region_value)
        
        print("Data Type of country value = " , str(type(country_value)))
        print("Data of country value = " , country_value)
        
        print("Data Type of state value = " , str(type(state_value)))
        print("Data of state value = " , state_value)
        
        print("Data Type of city value = " , str(type(city_value)))
        print("Data of city value = " , city_value)
        
        print("Data Type of Attack value = " , str(type(attack_value)))
        print("Data of Attack value = " , attack_value)
        
        print("Data Type of year value = " , str(type(year_value)))
        print("Data of year value = " , year_value)
    
        year_range = range(year_value[0], year_value[1]+1)
        new_df = df[df["iyear"].isin(year_range)]
    
        if month_value==[] or month_value is None:
            pass
        else:
            if date_value==[] or date_value is None:
                new_df = new_df[new_df["imonth"].isin(month_value)]
            else:
                new_df = new_df[new_df["imonth"].isin(month_value)
                                & (new_df["iday"].isin(date_value))]
     
        if region_value==[] or region_value is None:
            pass
        else:
            if country_value==[] or country_value is None :
                new_df = new_df[new_df["region_txt"].isin(region_value)]
            else:
                if state_value == [] or state_value is None:
                    new_df = new_df[(new_df["region_txt"].isin(region_value))&
                                    (new_df["country_txt"].isin(country_value))]
                else:
                    if city_value == [] or city_value is None:
                        new_df = new_df[(new_df["region_txt"].isin(region_value))&
                        (new_df["country_txt"].isin(country_value)) &
                        (new_df["provstate"].isin(state_value))]
                    else:
                        new_df = new_df[(new_df["region_txt"].isin(region_value))&
                        (new_df["country_txt"].isin(country_value)) &
                        (new_df["provstate"].isin(state_value))&
                        (new_df["city"].isin(city_value))]
                        
        if attack_value == [] or attack_value is None:
            pass
        else:
            new_df = new_df[new_df["attacktype1_txt"].isin(attack_value)] 
        
             
        mapFigure = go.Figure()
        
        if new_df.shape[0]:
            pass
        else: 
            new_df = pd.DataFrame(columns = ['iyear', 'imonth', 'iday', 'country_txt', 'region_txt', 'provstate',
               'city', 'latitude', 'longitude', 'attacktype1_txt', 'nkill'])
            
            new_df.loc[0] = [0, 0 ,0, None, None, None, None, None, None, None, None]
            
        
        mapFigure = px.scatter_mapbox(new_df,
          lat="latitude", 
          lon="longitude",
          color="attacktype1_txt",
          hover_name="city", 
          hover_data=["region_txt", "country_txt", "provstate","city", "attacktype1_txt","nkill","iyear","imonth", "iday"],
          zoom=1
          )                       
        mapFigure.update_layout(mapbox_style="open-street-map",
          autosize=True,
          margin=dict(l=0, r=0, t=25, b=20),
          )
          
        fig = mapFigure
        
    elif Tabs=="Chart":
        fig = None

        year_range_c = range(chart_year_selector[0], chart_year_selector[1]+1)
        chart_df = df[df["iyear"].isin(year_range_c)]


        if subtabs2 == "WorldChart":
            pass
        elif subtabs2 == "IndiaChart":
            chart_df = chart_df[(chart_df["region_txt"]=="South Asia") &(chart_df["country_txt"]=="India")]
        if chart_dp_value is not None and chart_df.shape[0]:
            if search is not None:
                chart_df = chart_df.groupby("iyear")[chart_dp_value].value_counts().reset_index(name = "count")
                chart_df  = chart_df[chart_df[chart_dp_value].str.contains(search, case=False)]
            else:
                chart_df = chart_df.groupby("iyear")[chart_dp_value].value_counts().reset_index(name="count")


        if chart_df.shape[0]:
            pass
        else: 
            chart_df = pd.DataFrame(columns = ['iyear', 'count', chart_dp_value])

            chart_df.loc[0] = [0, 0,"No data"]
        fig = px.area(chart_df, x="iyear", y ="count", color = chart_dp_value)                                     
    
    return dcc.Graph(figure = fig)
   


@app.callback(
    Output("dropdown2", "options"),
    [Input("dropdown1", "value")])
def update_date(month_value):
    date_list = [x for x in range(1, 32)]
    option = []
    if month_value:
        option= [{"label":m, "value":m} for m in date_list]
    return option


@app.callback([Output("dropdown3", "value"),
               Output("dropdown3", "disabled"),
               Output("dropdown4", "value"),
               Output("dropdown4", "disabled")],
              [Input("subtabs", "value")])
def update_r(tab):
    region = None
    disabled_r = False
    country = None
    disabled_c = False
    if tab == "WorldMap":
        pass
    elif tab=="IndiaMap":
        region = ["South Asia"]
        disabled_r = True
        country = ["India"]
        disabled_c = True
    return region, disabled_r, country, disabled_c

@app.callback(
    Output('dropdown4', 'options'),
    [Input('dropdown3', 'value')])
def set_country_options(region_value):
    option = []

    if region_value is  None:
        raise PreventUpdate
    else:
        for var in region_value:
            if var in country_list.keys():
                option.extend(country_list[var])
    return [{'label':m , 'value':m} for m in option]


@app.callback(
    Output('dropdown5', 'options'),
    [Input('dropdown4', 'value')])
def set_state_options(country_value):
  # Making the state Dropdown data
    option = []
    if country_value is None :
        raise PreventUpdate
    else:
        for var in country_value:
            if var in state_list.keys():
                option.extend(state_list[var])
    return [{'label':m , 'value':m} for m in option]


@app.callback(
    Output('city-dropdown', 'options'),
    [Input('dropdown5', 'value')])
def set_city_options(state_value):
  # Making the city Dropdown data
    option = []
    if state_value is None:
        raise PreventUpdate
    else:
        for var in state_value:
            if var in city_list.keys():
                option.extend(city_list[var])
    return [{'label':m , 'value':m} for m in option]

def main():
    print('starting main')
    
    read_data()
    open_browser()

    global app 
    app.layout=create_app_ui()
    app.title = 'Terrorism analysis with Insights '
    app.run_server()
    global df
    df=None
    app=None



if __name__ == '__main__':
    print('start the project')
    main()
    print('end the project')
    
