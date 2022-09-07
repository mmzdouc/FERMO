from dash import Dash, html, dcc, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate
import pickle

#local modules
from pages_header_footer import footer_row, header_row
from pages_header_footer import footer_row, header_row
from pages_landing import landing
from pages_dashboard import dashboard

import callbacks



app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.GRID],
    suppress_callback_exceptions=True,
    title='FERMO',
    )
server = app.server

app.layout = dbc.Container([
        #header row
        header_row,
        #content row
        html.Div([
            # represents the browser address bar, invisible
            dcc.Location(id='url', refresh=False), 
            #variable page content rendered in this element
            html.Div(id='page-content')
            ]),
        #footer row
        footer_row,
    ], 
    id="bounding_box",
    fluid="True", 
)



@callback(
    Output('page-content', 'children'),
    Input('url', 'pathname'),
)
def display_page(pathname, ):
    
    #has to be adapted to individual pages; + a 404 for wrong entries
    
    if pathname == '/dashboard':
        return dashboard
    else:
        return landing


if __name__ == '__main__':
    app.run_server(debug=True)












#####LAYOUT - USE LATER

# ~ dbc.Container([
        # ~ ###header row###
        # ~ dbc.Row([
                # ~ #header
                # ~ dbc.Col([
                        # ~ html.Div(
                            # ~ html.A([
                                # ~ html.Img(
                                    # ~ src=app.get_asset_url('Fermo_logo.svg'),
                                    # ~ style={'height':'7.5vh'},
                                    # ~ ),
                                # ~ ],
                                # ~ href='https://github.com/mmzdouc/fermo',
                                # ~ target="_blank",
                            # ~ ),
                        # ~ ),
                    # ~ ],
                # ~ id="header_col",
                # ~ width="True",
                # ~ style={'display': 'inline-block'},
                # ~ ),
            # ~ ],
        # ~ id="header_row",
        # ~ ),
        # ~ html.Div([




            # ~ ]),
        # ~ ###footer row###
        # ~ dbc.Row([
            # ~ dbc.Col([
                # ~ html.Div([
                    # ~ html.A([
                        # ~ html.Img(
                            # ~ src=app.get_asset_url('WUR_logo.png'),
                            # ~ style={'height': '7.5vh'},
                            # ~ ),
                        # ~ ],
                        # ~ href='https://www.wur.nl/en/research-results/chair-groups/plant-sciences/bioinformatics/people.htm',
                        # ~ target="_blank",
                        # ~ ),
                    # ~ html.A([
                        # ~ html.Img(
                            # ~ src=app.get_asset_url('Marbles_logo.svg'),
                            # ~ style={'height': '7vh', 'margin': '10px 10px 0px'},
                            # ~ ),
                        # ~ ],
                        # ~ href='https://marblesproject.eu/',
                        # ~ target="_blank",
                        # ~ ),
                    # ~ ],
                # ~ ),
            # ~ ],
            # ~ id="footer_col",
            # ~ width="True",
            # ~ style={'display': 'inline-block'},
            # ~ ),
        # ~ ],
        # ~ id="footer_row",
        # ~ ),
    # ~ ], 
    # ~ id="bounding_box",
    # ~ fluid="True", 
# ~ )

# ~ if __name__ == '__main__':
    # ~ app.run_server(debug=True)



