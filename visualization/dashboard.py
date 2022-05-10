import pandas as pd
from dash import Dash, html, dcc, dash_table
import plotly.express as px

def dashboard(
samples: dict, feature_objects: dict, topn_samples_features: list):
    """Initializes the dashboard

    Parameters
    ----------
    samples : `dict`
        Sample_names(keys):pandas.core.frame.DataFrame(values)
    feature_objects : `dict`
        Feature_ID(keys):Feature_Objects(values)
    topn_samples_features : `list`
        Contains two lists: topn_samples and topn_features
        
    Notes
    -----
    #for visualization of peaks, use bezier curves from wand library
    #(would that work?) Alternatively, also possibleto make bezier  
    #curves in pyplot but less convenient
    #curves must be defined for every peak separately; 
    #look closer into chromatographic peak theory and how fwhm is defined
    # start = (rt-(0.75*fwhm)/0); top = (rt/rel_int); stop = (rt+(0.75*fwhm)/0)
    #the 0.75 could be a bit lower but lets see how it looks like
    #abstraction -> in a real peak, curve is left-leaning; reaches maximum fast
    #and has some more (or lots of ) peak trailing

    """
    
    #initializes Dash Object
    app = Dash(__name__, title='FERMO')
    
    #layout of app
    app.layout = dashboard_layout()
    
    #run server - found on http://127.0.0.1:8050/
    app.run_server(debug=True)



def dashboard_layout():
    """Defines app layout"""
    
    layout_app = html.Div([
    html.Div(
        className="app-header",
        children=[
            html.Div('FERMO', className="app-header--title")
        ]
    ),
    html.Div(
        children=html.Div([
            html.H5('Overview'),
            html.Div('''
                This is a placeholder for the FERMO Dash app with
                local, customized CSS.
            ''')
            ])
        )
    ])
    
    
    return layout_app
