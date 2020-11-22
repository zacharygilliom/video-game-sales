from connect import  VideoGameSales
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

#-------- Import and clean our Dataframe ------------

# LAPTOPPATH = "/home/zacharygilliom/pythonProjects/video-game-sales/backend/database/vgsales.db"
DESKTOPPATH= "/mnt/c/Users/zacha/Documents/pythonProjects/video-game-sales/backend/database/vgsales.db"
salesData = VideoGameSales(DESKTOPPATH)

salesData.makeDataframe()
salesData.cleanDataframe()

df_grouped_year = salesData.byYearDataframe()
df_melted = salesData.meltDataframe(df_grouped_year)

df_region_specific_top_sales= salesData.topThreePlatoformsByYearAndRegion('NA_Sales')

#-------- Create and set defaults for our app ------------
external_stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheet)

colors = {'background': '#336699',
            'text': '#000000'}


fig_line = px.line(df_melted, x='Year', y='Total_Sales', color='Sales_Region')

fig_line.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

app.layout = html.Div(style={'backgroundColor': colors['background']},children=[
    html.H1(
        'Video Game Sales Data',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    dcc.Graph(
        id='line-graph',
        figure=fig_line,
    ),
    html.Div(style={'backgroundColor': colors['background'], 'color': colors['text']}, children=[
       html.H2(
            'Top 3 Best Selling Platforms by Year',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),
        html.H5(
            "Select Sales Region: ",
            style={
                'textAlign': 'left',
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

        ),
        dcc.Graph(id='bar-graph')
        ]
    )
]
)
        

@app.callback(
    Output('bar-graph', 'figure'),
    Input('sales_region_input', 'value'))
def update_bar(region):
    df = salesData.topThreePlatoformsByYearAndRegion(region)
    fig = px.bar(df, x='Year', y=region, color='Platform', barmode='stack')
    fig.update_layout()
    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )
    return fig
if __name__ == '__main__':
    app.run_server(debug=True)
