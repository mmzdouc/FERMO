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
    Output('storage_feature_dicts', 'data'),
    Output('storage_samples_JSON', 'data'),
    Output('storage_sample_stats', 'data'),
    Input('data_processing_FERMO', 'data'),
)
def FERMO_data_loading(contents):
    '''Loading function: contents contains the following data (from utils)
    '''
    if contents is None:
        raise PreventUpdate
    else:  
        return (
            contents['feature_dicts'],
            contents['samples_JSON'],
            contents['sample_stats'],
            )

@callback(
    Output(component_id='threshold_values', component_property='data'),
    Input(component_id='rel_intensity_threshold', component_property='value'),
    Input(component_id='convolutedness_threshold', component_property='value'),
    Input(component_id='bioactivity_threshold', component_property='value'),
    Input(component_id='novelty_threshold', component_property='value'),
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
        Output(component_id='table_sample_names', component_property='data'),
        Input(component_id='threshold_values', component_property='data'),
        Input(component_id='storage_feature_dicts', component_property='data'),
        Input(component_id='storage_samples_JSON', component_property='data'),
        Input(component_id='storage_sample_stats', component_property='data'),
        )
def calculate_feature_score(
        thresholds,
        feature_dicts,
        samples_JSON,
        sample_stats,):
    '''Test if over threshold; calculate diversity score'''

    #temporarily convert from JSON to pandas DF
    samples = dict()
    for sample in samples_JSON:
        samples[sample] = pd.read_json(
            samples_JSON[sample], orient='split')
    
    
    #for each sample, extract rows that corresponds to thresholds
    samples_filtered_dfs = dict()
    for sample in samples:
        #all features per sample
        all_feature_set = set(samples[sample]['feature_ID'])


        #determine which features are detected in group BLANK
        features_blanks_set = set()
        for feature_ID in all_feature_set:
            if 'BLANK' in feature_dicts[str(feature_ID)]['set_groups']:
                features_blanks_set.add(feature_ID)
        
        #filter for ms1 only
        ms1_only_df = samples[sample].loc[
            samples[sample]['ms1_only'] == True
            ]
        ms1_only_set = set(ms1_only_df['feature_ID'])
        
        #filter for numeric thresholds
        filtered_thrsh_df = samples[sample].loc[
            (samples[sample]['rel_intensity_score'] >= thresholds['rel_int']) &
            (samples[sample]['convolutedness_score'] >= thresholds['conv']) &
            (samples[sample]['bioactivity_score'] >= thresholds['bioact']) &
            (samples[sample]['novelty_score'] >= thresholds['nov']) 
            ]
        filtered_thrsh_set = set(filtered_thrsh_df['feature_ID'])
        
        #combine ms1 and blank features
        blank_ms1_set = features_blanks_set.union(ms1_only_set)
        
        #subtract ms1 and blanks from features over threshold
        selected_features_set = filtered_thrsh_set.difference(blank_ms1_set)
        
        print(sample)
        print(len(all_feature_set))
        print(all_feature_set)
        print(len(filtered_thrsh_set))
        print(filtered_thrsh_set)
        print(len(blank_ms1_set))
        print(blank_ms1_set)
        print(len(selected_features_set))
        print(selected_features_set)
        
        
        
        
        # ~ samples_filtered_dfs[sample] = set(filtered_df['feature_ID'])
        
        #create dict per sample {
        #list of feature IDs over threshold
        #list of features in medium + ms1 (
        #list of features below threshold (but filtered for medium and ms1) -> subtract from all features per sample in sample stats)
        #}
        
    
    
    # ~ ms1_bool
    
        
        #extract numbers instead of whole row
        #take into account possible len of 0
    
    
    #build if conditional that checks if BLANK in groups of feature dict
    
    
    #can be further filtered down by querying feature dicts for true/false etc
    
    
        # ~ print(sample)
        # ~ print(samples_over[sample])
        # ~ .query(
            # ~ 'rel_intensity_score >= thresholds['rel_int']'
        # ~ )
        

# ~ feature_scoring[sample]['rel_intensity_score'].ge(thresholds[0]) &
        # ~ feature_scoring[sample]['convolutedness_score'].ge(thresholds[1]) &
        # ~ feature_scoring[sample]['bioactivity_score'].ge(thresholds[2]) &
        # ~ feature_scoring[sample]['novelty_score'].ge(thresholds[3]) &
        # ~ #tilde (~) negates expression
        # ~ ~feature_scoring[sample]['in_blank'] &
        # ~ ~feature_scoring[sample]['ms1_only']



    
    return

        # ~ #extract list of sample ids that are over threshold/filters (for each row...?)
        
        # ~ #use this list and stuff from sample stats to calculate metrics
        
        # ~ #make list of samples over threshold, below, medium-components, unique to samples, unique to group...
        
        # ~ #use set with differece for fast calculation
        
        # ~ #store the numbers in dataframe plus a storage container for later plotting of chromatogram
        
        
        
         # ~ #Update over_threshold value in feature_scoring
        # ~ for sample in feature_scoring:

            # ~ #condition C:
    # ~ elif args.bioactivity and args.metadata:
        # ~ feature_scoring[sample]['over_threshold'] = np.select(
            # ~ utilities.threshold_condition_C(
                # ~ feature_scoring, 
                # ~ sample, 
                # ~ thresholds
                # ~ ), 
            # ~ [True], 
            # ~ default=False
        # ~ )
        
        
    # ~ return [
        # ~ feature_scoring[sample]['rel_intensity_score'].ge(thresholds[0]) &
        # ~ feature_scoring[sample]['convolutedness_score'].ge(thresholds[1]) &
        # ~ feature_scoring[sample]['bioactivity_score'].ge(thresholds[2]) &
        # ~ feature_scoring[sample]['novelty_score'].ge(thresholds[3]) &
        # ~ #tilde (~) negates expression
        # ~ ~feature_scoring[sample]['in_blank'] &
        # ~ ~feature_scoring[sample]['ms1_only']
        # ~ ]
        
        
        
        
                        
       
            # ~ #condition B:
            # ~ elif not args.bioactivity and args.metadata:
                # ~ feature_scoring[sample]['over_threshold'] = np.select(
                    # ~ utilities.threshold_condition_B(
                        # ~ feature_scoring, 
                        # ~ sample, 
                        # ~ thresholds
                        # ~ ), 
                    # ~ [True], 
                    # ~ default=False
                # ~ )

            # ~ #condition D:
            # ~ else:
                # ~ feature_scoring[sample]['over_threshold'] = np.select(
                    # ~ utilities.threshold_condition_D(
                        # ~ feature_scoring, 
                        # ~ sample, 
                        # ~ thresholds
                        # ~ ), 
                    # ~ [True], 
                    # ~ default=False
                # ~ )
            # ~ #Sort df, reset index
            # ~ feature_scoring[sample].sort_values(
                # ~ by=["rel_intensity_score",], 
                # ~ inplace=True, 
                # ~ ascending=[False,]
                # ~ )
            # ~ feature_scoring[sample].reset_index(drop=True, inplace=True)

        
        # ~ #Calculate diversity score and check nr features over threshold,
        # ~ for id, row in sample_scores.iterrows():
            
            # ~ #In which group is sample
            # ~ sample_scores.at[id, 'Group'] = (
                # ~ sample_stats['samples_dict'][row['Filename']]
                # ~ )

            # ~ #Total number of features
            # ~ sample_scores.at[id, 'Total'] = (
                # ~ np.count_nonzero(feature_scoring[
                    # ~ row['Filename']].loc[:,"feature_ID"]) 
                # ~ )
            
            # ~ #Nr of features not blank/ms1 associated
            # ~ set_blnk_ms1 = set()
            # ~ set_blnk_ms1.update(
                # ~ list(feature_scoring[row['Filename']].loc[
                    # ~ :,"in_blank"].to_numpy().nonzero()[0]))
            # ~ set_blnk_ms1.update(
                # ~ list(feature_scoring[row['Filename']].loc[
                    # ~ :,"ms1_only"].to_numpy().nonzero()[0]))
            
            # ~ sample_scores.at[id, 'Non-blank'] = (
                # ~ np.count_nonzero(feature_scoring[
                    # ~ row['Filename']].loc[:,"feature_ID"])
                # ~ -
                # ~ len(set_blnk_ms1)
                # ~ )
            
            
            # ~ #Features over thresholds
            # ~ sample_scores.at[id, 'Over cutoff'] = (
                # ~ np.count_nonzero(feature_scoring[
                    # ~ row['Filename']].loc[:,"over_threshold"])
                # ~ )
            
            # ~ #Diversity score: how much of the chemistry of sample set 
            # ~ #is contained in this sample?
            # ~ #Calculated as nr of cliques per sample/all cliques
            # ~ sample_scores.at[id, 'Diversity score'] = round(
                # ~ (
                # ~ len(
                    # ~ set(sample_stats["cliques_per_sample"][row['Filename']]
                        # ~ ).difference(sample_stats["set_blank_cliques"])
                    # ~ )
                # ~ / 
                # ~ (len(
                    # ~ set(sample_stats["set_all_cliques"]
                        # ~ ).difference(sample_stats["set_blank_cliques"])
                    # ~ ))
                # ~ ),
            # ~ 2)
            
            # ~ #Specificity score: detect which mol networks are unique to the
            # ~ #group the sample is part of
            # ~ #report proportion to all mol networks
            # ~ set_unique_cliques = set()
            # ~ for index, line in feature_scoring[row['Filename']].iterrows():
                # ~ feature_ID = line['feature_ID']
                # ~ if (
                    # ~ (row['Filename'] in feature_objects[feature_ID].presence_samples)
                # ~ and not
                    # ~ (line['in_blank'] == True)
                # ~ and not
                    # ~ (line['ms1_only'] == True)
                # ~ and 
                    # ~ (len(feature_objects[feature_ID].set_groups_clique) == 1)
                # ~ ):
                    # ~ set_unique_cliques.add(
                        # ~ feature_objects[feature_ID].similarity_clique_number)

            # ~ sample_scores.at[id, 'Specificity score'] = round(
                # ~ ((len(set_unique_cliques))
                # ~ / 
                # ~ (len(
                    # ~ set(sample_stats["set_all_cliques"]
                        # ~ ).difference(sample_stats["set_blank_cliques"])
                    # ~ ))
                # ~ ),
            # ~ 2)   

        # ~ #Sort df, reset index
        # ~ sample_scores.sort_values(
            # ~ by=[
                # ~ 'Over cutoff',
                # ~ 'Diversity score',
                # ~ 'Total',
                # ~ 'Non-blank',
                # ~ ], 
            # ~ inplace=True, 
            # ~ ascending=[False, False, False, True]
            # ~ )
        # ~ sample_scores.reset_index(drop=True, inplace=True)

        # ~ return sample_scores.to_dict('records')































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
        
        
        
        
