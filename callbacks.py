from dash import Input, Output, callback, dcc
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import pickle

@callback(
    Output('url', 'pathname'),
    Input('start_button', 'n_clicks'),
)
def start_calculation(n_clicks):
    if n_clicks == 0:
        raise PreventUpdate
    else:
        
        storage_input = 'Hakuna matata'
        
        outfile = open('temp', 'wb')
        pickle.dump(storage_input, outfile)
        outfile.close()
        print("ALERT: Saved to session (cache) file.")
        
        
        
        return '/dashboard'


# ~ @callback(
    # ~ Output('params_loading', 'children'),
    # ~ Input('url', 'pathname'),
# ~ )
# ~ def display_params(pathname):
    # ~ if pathname == '/dashboard':
        # ~ try:
            # ~ infile = open('temp', 'rb')
            # ~ session_FERMO = pickle.load(infile) 
            # ~ infile.close()
            # ~ return session_FERMO
        # ~ except:
            # ~ return 'NO file temp found'
