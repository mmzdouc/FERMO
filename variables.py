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

params_dict = {
    'mass_dev_ppm' : None,
    'min_nr_ms2' : None,
    'feature_rel_int_fact' : None,
    'bioact_fact' : None,
    'column_ret_fact' : None,
    'spectral_sim_tol' : None,
    'spec_sim_score_cutoff' : None,
    'max_nr_links_ss' : None,
    'min_nr_matched_peaks' : None,
    }

input_file_store = {
    'peaktable' : None,
    'peaktable_name' : None,
    'mgf' : None,
    'mgf_name' : None,
    'metadata' : None,
    'metadata_name' : None,
    'bioactivity' : None,
    'bioactivity_name' : None,
    'user_library' : None,
    'user_library_name' : None,
}
