from connect import  VideoGameSales
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

#-------- Import and clean our Dataframe ------------

# LAPTOPPATH = "/home/zacharygilliom/pythonProjects/video-game-sales/backend/database/vgsales.db"
DESKTOPPATH= "/mnt/c/Users/zacha/Documents/pythonProjects/video-game-sales/backend/database/vgsales.db"
salesData = VideoGameSales(DESKTOPPATH)

salesData.makeDataframe()
salesData.cleanDataframe()

df_grouped_year = salesData.byYearDataframe()
df_melted = salesData.meltDataframe(df_grouped_year)

#-------- Create and set defaults for our app ------------
external_stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheet)

colors = {'background': '#336699',
            'text': '#000000'}

fig_bar = px.bar(df_melted, x='Year', y='Total_Sales', color='Sales_Region', barmode='group')

fig_bar.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

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
    dcc.Graph(
        id='bar-graph',
        figure=fig_bar,
    )

])

if __name__ == '__main__':
    app.run_server(debug=True)
