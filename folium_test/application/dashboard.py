import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
import os
from dash_html_components.Content import Content

from dash_html_components.Tr import Tr

FARM_LOGO = "folium_test/application/images/farm_logo.png"
CAPGEMINI_LOGO = "folium_test/application/images/capgemini_logo.png"

# print(os.getcwd())
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# navbar = dbc.Navbar(
#     [
#         html.A(
#             # Use row and col to control vertical alignment of logo / brand
#             dbc.Row(
#                 [
#                     html.Img(src="https://d2kta6kx4236p6.cloudfront.net/img/logo.56e22df1.png", height="30px"),
#                     dbc.Nav(
#                         [
#                             dbc.NavItem(dbc.NavLink("Home", active=True, href="#")),
#                             dbc.NavItem(dbc.NavLink("Interactive Map", href="#"))
#                         ],
#                         pills=True
#                     )
#                 ],
#                 align="center",
#                 no_gutters=True,
#             ),
#             href="https://plot.ly",
#         )
#     ],
#     color="white"
# )

nav_bar = html.Div(children=[
    html.Nav(className="nav nav-pills", children=[
        html.Img(src="https://d2kta6kx4236p6.cloudfront.net/img/logo.56e22df1.png", height="30px")
], style={'padding': '10px 10px 10px 10px'})])

bot_bar = html.Div(children=[
    html.Img(src="https://d2kta6kx4236p6.cloudfront.net/img/capgemini-logo.dd5491a8.png", height="30px")
    ], style={'padding': '10px 10px 10px 10px'})

# content = html.Iframe(id='map', srcDoc=open('folium_test//application//index.html', 'r').read(), width='100%', height='2000', style=CONTENT_STYLE)

content = html.Div(id="page-content", children=[html.Iframe(id='map', srcDoc=open('folium_test//application//index.html', 'r').read(), width='100%', height='730')])

app.layout = html.Div([
    nav_bar,
    content,
    bot_bar
]
)

if __name__ == '__main__':
    app.run_server(debug=True)