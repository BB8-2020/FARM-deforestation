"""Dashboard and entry point of the gui."""
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

nav_bar = html.Div(
    children=[
        html.Nav(
            className="nav nav-pills",
            children=[
                html.Img(
                    src="https://d2kta6kx4236p6.cloudfront.net/img/logo.56e22df1.png",
                    height="30px",
                )
            ],
            style={"padding": "10px 10px 10px 10px"},
        )
    ]
)

bot_bar = html.Div(
    children=[
        html.Img(
            src="https://d2kta6kx4236p6.cloudfront.net/img/capgemini-logo.dd5491a8.png",
            height="30px",
        )
    ],
    style={"padding": "10px 10px 10px 10px"},
)

content = html.Div(
    id="page-content",
    children=[
        html.Iframe(
            id="map",
            srcDoc=open("folium_test//application//index.html", "r").read(),
            width="100%",
            height="730",
        )
    ],
)

app.layout = html.Div([nav_bar, content, bot_bar])

if __name__ == "__main__":
    app.run_server(debug=True)
