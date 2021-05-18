import dash
import dash_html_components as html
import os

app = dash.Dash()

app.layout = html.Div([
    html.H1('Title'),
    html.Iframe(id = 'map', srcDoc= open('folium_test//index.html', 'r').read(), width='100%', height='600')
]
)

if __name__ == '__main__':
    app.run_server(debug=True)