from connect import  VideoGameSales
import dash
import sqlite3
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

#-------- Import and clean our Dataframe ------------

LAPTOPPATH = "/home/zacharygilliom/pythonProjects/video-game-sales/backend/database/vgsales.db"
#DESKTOPPATH= "/mnt/c/Users/zacha/Documents/pythonProjects/video-game-sales/backend/database/vgsales.db"
COL_NAMES = ['Rank', 'Name', 'Platform', 'Year', 'Genre', 'Publisher', 'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']
 
def connectToDatabase(path):
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute("SELECT * FROM sales")
    rows = cur.fetchall()
    return rows

ROWS = connectToDatabase(LAPTOPPATH)

salesData = VideoGameSales(ROWS, COL_NAMES)

print(salesData.df)
df_grouped_year = salesData.byYearDataframe()


#-------- Create and set defaults for our app ------------
external_stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheet)

colors = {'background': '#336699',
            'text': '#000000'}


app.layout = html.Div(style={'backgroundColor': colors['background']},children=[
    html.Div(style={'backgroundColor': colors['background'], 'color': colors['text']}, children=[
             html.H1(
                 'Video Game Sales Data',
                 style={
                     'textAlign': 'center',
                     'color': colors['text']
                 }
             ),
             html.H4(
                 "Select Sales Region: ",
                 style={
                     'textAlign': 'left',
                     'color': colors['text']
                 }
             ),
            html.H4(
                'Between 1980 and 2016 there has been a lot of fluctuation throughout the gaming industry',
                style={
                    'textAlign': 'center',
                    'color': colors['text']
                }
            ),
    dcc.RadioItems(id='sales_region_input',
        options=[
            {'label': 'North America', 'value': 'NA_Sales'},
            {'label': 'Europe', 'value': 'EU_Sales'},
            {'label': 'Japan', 'value': 'JP_Sales'},
            {'label': 'Other Countries', 'value': 'Other_Sales'},
            {'label': 'Global Total', 'value': 'Global_Sales'}
        ],
        value='NA_Sales'

    )]),
    html.Div(style={'backgroundColor': colors['background'], 'color': colors['text']}, children=[
        html.H2(
            'Top 3 Best Selling Genres by Year',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),
        dcc.Graph(
            id='genre-graph'
        )
    ]),
    html.Div(style={'backgroundColor': colors['background'], 'color': colors['text']}, children=[
       html.H2(
            'Top 3 Best Selling Platforms by Year',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),
        dcc.Graph(id='platform-graph')
        ]
    )
]
)

@app.callback(
    Output('genre-graph', 'figure'),
    Input('sales_region_input', 'value'))
def update_line(region):
    df = salesData.topThreeGenresByYearAndRegion(region)
    fig = px.bar(df, x='Year', y=region, color='Genre', barmode='stack')
    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )
    return fig

@app.callback(
    Output('platform-graph', 'figure'),
    Input('sales_region_input', 'value'))
def update_bar(region):
    df = salesData.topThreePlatformsByYearAndRegion(region)
    fig = px.bar(df, x='Year', y=region, color='Platform', barmode='stack')
    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
