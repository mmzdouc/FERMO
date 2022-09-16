import pandas as pd

##########
#STYLES
##########

style_data_table={
    'color': 'black',
    'backgroundColor': 'white',
    'font-size': '12px'
}

style_data_cond_table=[{
        'if': {'row_index': 'odd'},
        'backgroundColor': 'rgb(220, 220, 220)',
}]

style_header_table={
    'backgroundColor': '#116789',
    'color': 'white',
    'fontWeight': 'bold',
    'textAlign': 'left',
    'font-size': '15px',
    'whiteSpace': 'normal',
    'height': 'auto',
}

##########
#STORAGE
##########

params_df = pd.DataFrame({
    'Parameters' : [
        'Mass deviation (in ppm)',
        'Minimal nr of MS<sup>2</sup> peaks',
        'Feature relative intensity filter',
        'Bioactivity factor',
        'Column retention factor',
        'Spectral similarity tolerance',
        'Spectral similarity score cutoff',
        'Maximal number of links in MN',
        'Min number of matched peaks',
        ],
    'Values' : 'N/A',
    })

input_file_store = {
    'peaktable' : None,
    'peaktable_name' : None,
    'mgf' : None,
    'mgf_name' : None,
    'metadata' : None,
    'metadata_name' : None,
    'bioactivity' : None,
    'bioactivity_name' : None,
}
