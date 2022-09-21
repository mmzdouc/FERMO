import dash
from dash import Input, Output, callback, dcc, dash_table, State, html, ctx, DiskcacheManager, CeleryManager
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import pickle
import matchms
from  matchms.Spectrum import Spectrum

from pyteomics import mgf

import sys
import os
import pandas as pd
import io
import base64
import numpy as np


####LOCAL MODULES AND VARS

import utils

from variables import (
    params_dict,
    input_file_store,
    style_data_table,
    style_data_cond_table,
    style_header_table,
)



##########
#PAGES_PROCESSING
##########

@callback(
    Output('params_cache', 'component'),
    Input('mass_dev_inp', 'value'),
    Input('min_ms2_inpt', 'value'),
    Input('feat_int_filt_inp', 'value'),
    Input('bioact_fact_inp', 'value'),
    Input('column_ret_fact_inp', 'value'),
    Input('spec_sim_tol_inp', 'value'),
    Input('spec_sim_score_cutoff_inp', 'value'),
    Input('spec_sim_max_links_inp', 'value'),
    Input('spec_sim_min_match_inp', 'value'),
    )
def bundle_params_into_cache(
    mass_dev, 
    min_ms2, 
    feat_int_filt,
    bioact_fact,
    column_ret_fact,
    spec_sim_tol,
    spec_sim_score_cutoff,
    spec_sim_max_links,
    spec_sim_min_match,
    ):
    '''Bundle parameter input values'''
    return {
    'mass_dev' : mass_dev,
    'min_ms2' : min_ms2,
    'feat_int_filt' : feat_int_filt,
    'bioact_fact' : bioact_fact,
    'column_ret_fact' : column_ret_fact,
    'spec_sim_tol' : spec_sim_tol,
    'spec_sim_score_cutoff' : spec_sim_score_cutoff,
    'spec_sim_max_links' : spec_sim_max_links,
    'spec_sim_min_match' : spec_sim_min_match,
        }

@callback(
    Output('out_params_assignment', 'children'),
    Input('params_cache', 'component')
)
def update_params_dict(params_cache):
    '''Assign set params to table, with sanity check for None'''

    if params_cache is not None:
        params_dict['mass_dev_ppm'] = (params_cache['mass_dev']
            if params_cache['mass_dev'] is not None
            else 20)
        params_dict['min_nr_ms2'] = (params_cache['min_ms2']
            if params_cache['min_ms2'] is not None
            else 0)
        params_dict['feature_rel_int_fact'] = (params_cache['feat_int_filt']
            if params_cache['feat_int_filt'] is not None
            else 0)
        params_dict['bioact_fact'] = (params_cache['bioact_fact']
            if params_cache['bioact_fact'] is not None
            else 0)
        params_dict['column_ret_fact'] = (params_cache['column_ret_fact']
            if params_cache['column_ret_fact'] is not None
            else 0)
        params_dict['spectral_sim_tol'] = (params_cache['spec_sim_tol']
            if params_cache['spec_sim_tol'] is not None
            else 0)
        params_dict['spec_sim_score_cutoff'] = (params_cache['spec_sim_score_cutoff']
            if params_cache['spec_sim_score_cutoff'] is not None
            else 0)
        params_dict['max_nr_links_ss'] = (params_cache['spec_sim_max_links']
            if params_cache['spec_sim_max_links'] is not None
            else 0)
        params_dict['min_nr_matched_peaks'] = (params_cache['spec_sim_min_match']
            if params_cache['spec_sim_min_match'] is not None
            else 0)
            
        return html.Div()

@callback(
    Output('upload-peaktable-output', 'children'),
    Input('processing-upload-peaktable', 'contents'),
    State('processing-upload-peaktable', 'filename'),
)
def upload_peaktable(contents, filename):
    '''Peaktable parsing and format check'''
    
    if contents is None:
        return html.Div('No peaktable loaded.',)
    else:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)

        try:
            peaktable = pd.read_csv(
                    io.StringIO(decoded.decode('utf-8')))
        except:
            input_file_store['peaktable'] = None
            input_file_store['peaktable_name'] = None
            return html.Div(
                f'''
                ❌ Error: "{filename}" does not seem to be a file in the
                .csv-format. Have you selected the right file?
                ''')
        return_assert = utils.assert_peaktable_format(peaktable, filename)
        
        peaktable.rename(
            columns={
                'id' : 'feature_ID',
                'mz' : "precursor_mz",
                'rt' : "retention_time",
                },
            inplace=True,
            )
            
        if return_assert is not None:
            input_file_store['peaktable'] = None
            input_file_store['peaktable_name'] = None
            return return_assert
        else:
            input_file_store['peaktable'] = peaktable
            input_file_store['peaktable_name'] = filename
            return html.Div(
                f'✅ "{filename}" successfully loaded.',
                style={
                    'color' : 'green',
                    'font-weight' : 'bold',
                })

@callback(
    Output('upload-mgf-output', 'children'),
    Input('processing-upload-mgf', 'contents'),
    State('processing-upload-mgf', 'filename'),
)
def upload_mgf(contents, filename):
    '''mgf file parsing and format check'''
    
    if contents is None:
        return html.Div('No .mgf-file loaded.')
    else:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        
        try:
            ms2spectra = dict()
            for spectrum in mgf.read(
                io.StringIO(decoded.decode('utf-8')),
                use_index=False
            ):
                fragments = spectrum.get('m/z array')
                intensities = spectrum.get('intensity array')
                feature_ID = int(spectrum.get('params').get('feature_id'))
                ms2spectra[feature_ID] = [fragments, intensities]
            
            utils.assert_mgf_format(ms2spectra)
            
            input_file_store['mgf'] = ms2spectra
            input_file_store['mgf_name'] = filename
            return html.Div(
                f'✅ "{filename}" successfully loaded.',
                style={
                    'color' : 'green',
                    'font-weight' : 'bold',
                })
            
        except:
            input_file_store['mgf'] = None
            input_file_store['mgf_name'] = None
            return html.Div(
                f'''
                ❌ Error: "{filename}" is not a mgf or is erroneously formatted.
                 Please check the file and try again.
                ''')

@callback(
    Output('upload-bioactiv-output', 'children'),
    Input('upload-bioactiv', 'contents'),
    State('upload-bioactiv', 'filename'),
    Input('bioact_type', 'value'),
)
def upload_bioactiv(contents, filename, value):
    '''Bioactivity table parsing and format check'''
    if contents is None:
        return html.Div('No bioactivity table loaded.')
    else:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)

        try:
            bioactiv_table = pd.read_csv(
                    io.StringIO(decoded.decode('utf-8')))
        except:
            input_file_store['bioactivity'] = None
            input_file_store['bioactivity_name'] = None
            return html.Div(
                f'''
                ❌ Error: "{filename}" does not seem to be a file in the
                .csv-format. Have you selected the right file?
                ''')
        
        if value is None:
            return html.Div(
                f'''
                ❌ Error: Please specify the bioactivity table format.
                Currently, the value is {value}.
                ''')
        
        return_assert = utils.assert_bioactivity_format(
            bioactiv_table, 
            filename,
            )
        
        if return_assert is not None:
            input_file_store['bioactivity'] = None
            input_file_store['bioactivity_name'] = None
            return return_assert
        else:
            converted_df = utils.parse_bioactiv_conc(bioactiv_table, value)
            input_file_store['bioactivity'] = converted_df
            input_file_store['bioactivity_name'] = filename
            return html.Div(
                f'✅ "{filename}" successfully loaded.',
                style={
                    'color' : 'green',
                    'font-weight' : 'bold',
                })

@callback(
    Output('store_bioact_type', 'children'),
    Input('bioact_type', 'value'),
)
def store_bioactiv_format(value):
    '''Stores the value of bioactivity data format'''
    return html.Div(value)


@callback(
    Output('upload-metadata-output', 'children'),
    Input('upload-metadata', 'contents'),
    State('upload-metadata', 'filename'),
)
def upload_metadata(contents, filename,):
    '''Metadata table parsing and format check'''
    if contents is None:
        return html.Div('No metadata table loaded.')
    else:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
    
        try:
            metadata_table = pd.read_csv(
                    io.StringIO(decoded.decode('utf-8')))
        except:
            input_file_store['metadata'] = None
            input_file_store['metadata_name'] = None
            return html.Div(
                f'''
                ❌ Error: "{filename}" does not seem to be a file in the
                .csv-format. Have you selected the right file?
                ''')
        
        return_assert = utils.assert_metadata_format(
            metadata_table, 
            filename,
            )
        
        if return_assert is not None:
            input_file_store['metadata'] = None
            input_file_store['metadata_name'] = None
            return return_assert
        else:
            input_file_store['metadata'] = metadata_table
            input_file_store['metadata_name'] = filename
            return html.Div(
                f'✅ "{filename}" successfully loaded.',
                style={
                    'color' : 'green',
                    'font-weight' : 'bold',
                })

@callback(
    Output('upload-userlib-output', 'children'),
    Input('upload-userlib', 'contents'),
    State('upload-userlib', 'filename'),
)
def upload_userlib(contents, filename):
    '''mgf file parsing and format check for user-provided spectral lib'''
    
    if contents is None:
        return html.Div('No spectral library loaded.')
    else:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        
        try:
            ref_library = list()
            for spectrum in mgf.read(
                io.StringIO(decoded.decode('utf-8')),
                use_index=False,
            ):
                mz = spectrum.get('m/z array')
                intensities = spectrum.get('intensity array')
                metadata = spectrum.get('params')
                
                if not np.all(mz[:-1] <= mz[1:]):
                    idx_sorted = np.argsort(mz)
                    mz = mz[idx_sorted]
                    intensities = intensities[idx_sorted]
                
                ref_library.append(
                    Spectrum(
                        mz=mz,
                        intensities=intensities,
                        metadata=metadata,
                        )
                    )
            ref_library = [matchms.filtering.add_compound_name(s) 
                for s in ref_library]
            ref_library = [matchms.filtering.normalize_intensities(s) 
                for s in ref_library]
            ref_library = [matchms.filtering.select_by_intensity(s, intensity_from=0.01)
                for s in ref_library]
            ref_library = [matchms.filtering.add_precursor_mz(s)
                for s in ref_library]
            ref_library = [matchms.filtering.require_precursor_mz(s)
                for s in ref_library]
            
            utils.assert_mgf_format(ref_library)

            input_file_store['user_library'] = ref_library
            input_file_store['user_library_name'] = filename
            return html.Div(
                f'✅ "{filename}" successfully loaded.',
                style={
                    'color' : 'green',
                    'font-weight' : 'bold',}
                    )
        except:
            input_file_store['user_library'] = None
            input_file_store['user_library_name'] = None
            return html.Div(
                f'''
                ❌ Error: "{filename}" is not a mgf or is erroneously formatted
                (e.g. 'pepmass' must not be 0.0 or 1.0).
                Please check the file and try again.
                ''')

##########
#PAGES_LOADING
##########

@callback(
    Output('upload-session-output', 'children'),
    Input('upload-session', 'contents'),
    State('upload-session', 'filename'),
)
def upload_sessionfile(contents, filename):
    '''Placeholder'''
    return html.Div(
                f'''
                SESSION FILE UPLOAD NOT YET ACTIVE
                ''')


##########
#PAGES_DASHBOARD
##########

@callback(
    Output('threshold_values', 'data'),
    Input('rel_intensity_threshold', 'value'),
    Input('convolutedness_threshold', 'value'),
    Input('bioactivity_threshold', 'value'),
    Input('novelty_threshold', 'value'),
)
def read_threshold_values_function(rel_int, conv, bioact, nov,):
    '''Bundle input values'''

    if None not in [rel_int, conv, bioact, nov,]:
        return {
            'rel_int' : float(rel_int),
            'conv' : float(conv),
            'bioact' : float(bioact),
            'nov' : float(nov),
            }
    else:
        raise PreventUpdate


@callback(
        Output('table_sample_names', 'data'),
        Output('samples_subsets', 'data'),
        Output('sample_list', 'data'),
        Input('threshold_values', 'data'),
        Input('data_processing_FERMO', 'data'),
        )
def calculate_feature_score(
        thresholds,
        contents,
        ):
    '''For each sample, create subsets of features and calculate scores'''
    feature_dicts = contents['feature_dicts']
    samples_JSON = contents['samples_JSON']
    sample_stats = contents['sample_stats']
    
    #temporarily convert from JSON to pandas DF
    samples = dict()
    for sample in samples_JSON:
        samples[sample] = pd.read_json(
            samples_JSON[sample], orient='split')
    
    #for each sample, extract rows that corresponds to thresholds
    samples_subsets = dict()
    for sample in samples:
        samples_subsets[sample] = utils.generate_subsets(
            samples, 
            sample,
            thresholds,
            feature_dicts,)
    
    #how many cliques in this sample are only found in group
    #extract all features per sample (corrected for blanks)
    sample_unique_cliques = dict()
    for sample in samples:
        unique_cliques = set()
        for ID in samples_subsets[sample]['all_nonblank']:
            if (
                (len(feature_dicts[str(ID)]['set_groups_clique']) == 1)
                and
                (sample in feature_dicts[str(ID)]['presence_samples'])
            ):
                unique_cliques.add(
                    feature_dicts[str(ID)]['similarity_clique_number']
                    )
        sample_unique_cliques[sample] = list(unique_cliques)

    #create dataframe to export to dashboard
    sample_scores = pd.DataFrame({
        'Filename' : [i for i in samples],
        'Group' : [sample_stats['samples_dict'][i] for i in samples],
        'Diversity score' : [
            round(
                (
                len(
                    set(sample_stats["cliques_per_sample"][i]).difference(
                        set(sample_stats["set_blank_cliques"])
                        )
                    )
                / 
                len(
                    set(sample_stats["set_all_cliques"]).difference(
                        set(sample_stats["set_blank_cliques"]))
                    )
                ),
            2) for i in samples],
        'Spec score' : [
            round(
                (
                (len(sample_unique_cliques[i]))
                / 
                len(
                    set(sample_stats["set_all_cliques"]).difference(
                        set(sample_stats["set_blank_cliques"]))
                    )
                ),
            2) for i in samples],
        'Total' : [len(samples_subsets[i]['all_features']) for i in samples],
        'Non-blank' : [len(samples_subsets[i]['all_nonblank']) for i in samples],
        'Over cutoff' : [len(samples_subsets[i]['all_select_no_blank']) for i in samples],
    })

    #Sort df, reset index
    sample_scores.sort_values(
        by=[
            'Diversity score',
            'Spec score',
            'Non-blank',
            ], 
        inplace=True, 
        ascending=[False, False, False]
        )
    sample_scores.reset_index(drop=True, inplace=True)
    
    sample_list = sample_scores['Filename'].tolist()
    
    return sample_scores.to_dict('records'), samples_subsets, sample_list


@callback(
    Output('storage_active_sample', 'data'),
    Input('table_sample_names', 'active_cell'),
    Input('table_sample_names', 'data'),
    Input('sample_list', 'data'),
)
def storage_active_sample(data, update_table, sample_list):
    '''Store active cell in dcc.Storage'''
    #Null coalescing assignment: default value if var not assigned
    data = data or {'row' : 0,}
    
    return sample_list[data["row"]]


@callback(
    Output('title_central_chrom', 'children'),
    Input('storage_active_sample', 'data'),
)
def title_central_chrom(selected_sample,):
    return f"""Chromatogram of Sample {selected_sample}"""


@callback(
    Output('chromat_out', 'figure'),
    Input('storage_active_sample', 'data'),
    Input('storage_active_feature_index', 'data'),
    Input('samples_subsets', 'data'),
    State('data_processing_FERMO', 'data'),
)
def plot_chromatogram(
    selected_sample, 
    active_feature_index,
    samples_subsets,
    contents,
    ):
    '''Plot central chromatogram'''
    samples_JSON = contents['samples_JSON']
    sample_stats = contents['sample_stats']
    
    #temporarily convert from JSON to pandas DF
    samples = dict()
    for sample in samples_JSON:
        samples[sample] = pd.read_json(
            samples_JSON[sample], orient='split')
    
    return utils.plot_central_chrom(
        selected_sample,
        active_feature_index,
        sample_stats,
        samples,
        samples_subsets)

@callback(
    Output('storage_active_feature_index', 'data'),
    Output('storage_active_feature_id', 'data'),
    Input('chromat_out', 'clickData'),
    Input('storage_active_sample', 'data'),
    State('data_processing_FERMO', 'data'),
)
def storage_active_feature(data, selected_sample, contents):
    '''Stores active feature in dcc.Storage'''
    if data is None:
        raise PreventUpdate
    
    if ctx.triggered_id == 'storage_active_sample':
        return None, None
    
    samples_JSON = contents['samples_JSON']
    #temporarily convert from JSON to pandas DF
    samples = dict()
    for sample in samples_JSON:
        samples[sample] = pd.read_json(
            samples_JSON[sample], orient='split')
    
    data_int = int(data["points"][0]['curveNumber'])
    
    feature_ID = int(samples[selected_sample].loc[data_int, 'feature_ID'])
    
    if data_int <= len(samples[selected_sample]):
        return data_int, feature_ID
    else:
        return 0, None


@callback(
    Output('chromat_clique_out', 'figure'),
    Input('storage_active_sample', 'data'),
    Input('storage_active_feature_index', 'data'),
    Input('storage_active_feature_id', 'data'),
    State('data_processing_FERMO', 'data'),
)
def plot_chromatogram_clique(
    selected_sample, 
    active_feature_index,
    active_feature_id,
    contents,
    ):
    '''Plot clique chromatogram'''
    feature_dicts = contents['feature_dicts']
    samples_JSON = contents['samples_JSON']
    sample_stats = contents['sample_stats']
    
    #temporarily convert from JSON to pandas DF
    samples = dict()
    for sample in samples_JSON:
        samples[sample] = pd.read_json(
            samples_JSON[sample], orient='split')

    return utils.plot_clique_chrom(
        selected_sample,
        active_feature_index,
        active_feature_id,
        sample_stats,
        samples,
        feature_dicts,)


@callback(
    Output('title_mini_chrom', 'children'),
    Input('storage_active_feature_id', 'data'),
    State('data_processing_FERMO', 'data'),
)
def title_mini_chrom(
    active_feature_id,
    contents,
    ):
    '''Print title of mini chromatograms'''
    feature_dicts = contents['feature_dicts']
    sample_stats = contents['sample_stats']
    
    
    if active_feature_id is None:
        raise PreventUpdate
    
    return f"""Feature {active_feature_id}: Detected Across 
        {len(feature_dicts[str(active_feature_id)]['presence_samples'])} 
        of {len(sample_stats["samples_list"])} Samples"""

@callback(
    Output('mini_chromatograms', 'figure'),
    Input('storage_active_sample', 'data'),
    Input('storage_active_feature_id', 'data'),
    State('data_processing_FERMO', 'data'),
)
def plot_chrom_overview(
    selected_sample, 
    active_feature_id,
    contents
    ):
    '''Plot mini-chromatograms'''
    
    '''Solution to sample name (subplot titles) problem of 
    stacking on top of the chromatograms is simply to 
    plot separate small chromatograms instead of subplots!
    Questionable how scalable but best solution 
    since more adjustable than subplots'''
    feature_dicts = contents['feature_dicts']
    samples_JSON = contents['samples_JSON']
    sample_stats = contents['sample_stats']
    
    #temporarily convert from JSON to pandas DF
    samples = dict()
    for sample in samples_JSON:
        samples[sample] = pd.read_json(
            samples_JSON[sample], orient='split')
    
    return utils.plot_mini_chrom(
        selected_sample,
        active_feature_id,
        sample_stats,
        samples,
        feature_dicts,)
    

@callback(
    Output('featureinfo_out', 'data'), 
    Input('storage_active_sample', 'data'),
    Input('storage_active_feature_id', 'data'),
    Input('storage_active_feature_index', 'data'),
    State('data_processing_FERMO', 'data'),
    )
def update_selected_feature(
    selected_sample, 
    active_feature_id,
    active_feature_index,
    contents,
    ):
    '''Return info on active feature'''
    feature_dicts = contents['feature_dicts']
    samples_JSON = contents['samples_JSON']
    
    #temporarily convert from JSON to pandas DF
    samples = dict()
    for sample in samples_JSON:
        samples[sample] = pd.read_json(
            samples_JSON[sample], orient='split')
    
    if isinstance(active_feature_index, int):
        return utils.modify_feature_info_df(
            selected_sample,
            active_feature_id,
            active_feature_index,
            feature_dicts,
            samples,
            )
    else:
        return utils.empty_feature_info_df()

@callback(
    Output('cytoscape', 'elements'),
    Input('storage_active_sample', 'data'),
    Input('storage_active_feature_id', 'data'),
    State('data_processing_FERMO', 'data'),
    )
def update_cytoscape(
    selected_sample,
    active_feature_id,
    contents,
    ):
    '''Plot spectral similarity network'''
    feature_dicts = contents['feature_dicts']
    sample_stats = contents['sample_stats']
    
    if active_feature_id is None:
        return []
    else:
        return utils.generate_cyto_elements(
            selected_sample,
            active_feature_id,
            feature_dicts,
            sample_stats,
            )

@callback(
    Output('click-nodedata-output', 'data'),
    Input('cytoscape', 'tapNodeData'),
    Input('storage_active_sample', 'data'),
    Input('storage_active_feature_id', 'data'),
    State('data_processing_FERMO', 'data'),
    )
def displayTapNodeData(
    nodedata, 
    selected_sample, 
    active_feature_id,
    contents
    ):
    '''Display node data after cytoscape click'''
    feature_dicts = contents['feature_dicts']
    
    if (
        ctx.triggered_id == 'storage_active_sample'
    or
        ctx.triggered_id == 'storage_active_feature_id'
    ):
        data = [
        ['Feature ID', None],
        ['Precursor <i>m/z</i>', None],
        ['Retention time (avg)', None],
        ['Annotation', None],
        ['Detected in samples', None],
        ]
        df = pd.DataFrame(data, columns=['Node info', 'Description'])
        return df.to_dict('records')
    
    elif ctx.triggered_id == 'cytoscape':
        return utils.add_nodedata(nodedata, feature_dicts,)

@callback(
    Output('click-edgedata-output', 'data'),
    Input('cytoscape', 'tapEdgeData'),
    Input('storage_active_sample', 'data'),
    Input('storage_active_feature_id', 'data'),
    State('data_processing_FERMO', 'data'),
    )
def displayTapEdgeData(
    edgedata, 
    selected_sample, 
    active_feature_id,
    contents
    ):
    '''Display edge data after cytoscape click'''
    feature_dicts = contents['feature_dicts']
    
    if (
        ctx.triggered_id == 'storage_active_sample'
    or
        ctx.triggered_id == 'storage_active_feature_id'
    ):
        data = [
        ['Connected nodes (IDs)', None],
        ['Weight of edge', None],
        ['<i>m/z</i> difference between nodes', None],
        ]
        df = pd.DataFrame(data, columns=['Node info', 'Description'])
        return df.to_dict('records')
    
    elif ctx.triggered_id == 'cytoscape':
        return utils.add_edgedata(edgedata, feature_dicts,)









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

        
        #get the input files -> input_file_store
        #load in the main -> build step by step
        
        #load in all four files
        
        
        
        #write a catch that prevents running FERMO without any input
        
        

        
        # ~ #READ PRE-SPECIFIED INPUT FOLDER
        # ~ dirname = os.path.dirname(__file__)
        # ~ input_folder = os.path.join(dirname, 'INPUT',)
        
        # ~ assert os.path.exists(input_folder), 'ERROR'
        
        # ~ list_input_files = os.listdir(input_folder)
        
        # ~ print(list_input_files)
        
        
        #STORAGE DATA BY PICKLE DUMP
        # ~ storage_input = 'Hakuna matata'
        # ~ outfile = open('temp', 'wb')
        # ~ pickle.dump(storage_input, outfile)
        # ~ outfile.close()
        # ~ print("ALERT: Saved to session (cache) file.")

        #READ 
        
        
        
        
