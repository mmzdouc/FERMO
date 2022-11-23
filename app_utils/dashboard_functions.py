import copy
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import re

from app_utils.variables import color_dict


def filter_str_regex(
    query,
    annot_str,
    ):
    '''Return bool if query matches annot_str'''
    try:
        if bool(re.search(query, annot_str, re.IGNORECASE,)):
            return True
        else:
            return False
    except:
        return False

def generate_subsets(
    samples, 
    sample,
    thresholds,
    feature_dicts,
    ):
    """Make subsets of features in sample based on thresholds
    
    Parameters
    ----------
    samples : `dict`
    sample : `str`
    thresholds : `dict`
    feature_dicts : `dict`
    
    Returns
    --------
    `dict`
    
    Notes
    ------
    Additional filters can be added with relative ease:
    Add the filter to the FERMO dashboard
    Connect filter to the callback id calculate_feature_score
    Simply add a conditional that adds feature ID to "all_select_no_blank"
    set. the later operations take care of the right group for plotting
    ####
    Example code: extract a row as series using squeeze()
    samples[selected_sample].loc[
        samples[selected_sample]['feature_ID'] == ID].squeeze(),
    """
    ###STATS###
    
    #all features per sample
    all_feature_set = set(samples[sample]['feature_ID'])

    #which of these features blank associated
    features_blanks_set = set()
    for feature_ID in all_feature_set:
        if 'BLANK' in feature_dicts[str(feature_ID)]['set_groups']:
            features_blanks_set.add(feature_ID)
    
    #extract features w ms1 only from samples table
    ms1_only_df = samples[sample].loc[
        samples[sample]['ms1_only'] == True
        ]
    ms1_only_set = set(ms1_only_df['feature_ID'])
    
    #combine ms1 and blank features
    blank_ms1_set = features_blanks_set.union(ms1_only_set)
    
    #from all features, filter blank and features with ms1 only
    all_nonblank_set = all_feature_set.difference(blank_ms1_set)
    
    ###FILTERS###
    
    #filter for numeric thresholds
    filt_df = samples[sample].loc[
        (
            (samples[sample]['rel_intensity_score'] >= thresholds['rel_intensity_threshold'][0]) 
            & 
            (samples[sample]['rel_intensity_score'] <= thresholds['rel_intensity_threshold'][1])
        ) 
        &
        (
            (samples[sample]['novelty_score'] >= thresholds['novelty_threshold'][0]) 
            & 
            (samples[sample]['novelty_score'] <= thresholds['novelty_threshold'][1])
        ) 
        &
        (
            samples[sample]['bioactivity_score'] >= thresholds['quant_biological_value']
        ) 
        ]
    filtered_thrsh_set = set(filt_df['feature_ID'])
    
    if thresholds['filter_adduct_isotopes'] != '':
        temp_set = set()
        for feature in filtered_thrsh_set:
            if filter_str_regex(
                thresholds['filter_adduct_isotopes'],
                ', '.join([i for i in feature_dicts[str(feature)]['ann_adduct_isotop']]),
                ):
                temp_set.add(feature)
        filtered_thrsh_set = filtered_thrsh_set.intersection(temp_set)
    
    
    if thresholds['filter_annotation'] != '':
        temp_set = set()
        for feature in filtered_thrsh_set:
            #construct string to query against
            search_list = ['',]
            if feature_dicts[str(feature)]['ms2query']:
                search_list.append(
                    feature_dicts[str(feature)][
                        'ms2query_results'][0]['analog_compound_name']
                    )
            if feature_dicts[str(feature)]['cosine_annotation']:
                search_list.append(
                    feature_dicts[str(feature)][
                        'cosine_annotation_list'][0]['name']
                    )
            if filter_str_regex(
                thresholds['filter_annotation'],
                ', '.join([i for i in search_list])
                ):
                temp_set.add(feature)
        filtered_thrsh_set = filtered_thrsh_set.intersection(temp_set)


    if thresholds['filter_feature_id'] != '':
        if thresholds['filter_feature_id'] in filtered_thrsh_set:
            filtered_thrsh_set = set([thresholds['filter_feature_id']])
        else:
            filtered_thrsh_set = set()



    #Filter to add:
    ##Feature ID
    ##precursor mz(match from start - modify query with a ^ to search from start
    ##similarity clique number
    ##fold difference larger than n (separately programmed)



    #subtract ms1 and blanks from features over threshold
    all_select_no_blank = filtered_thrsh_set.difference(blank_ms1_set)
    
    
    #subset of selected sample specific features
    select_sample_spec = set()
    for ID in all_select_no_blank:
        if (len(feature_dicts[str(ID)]['presence_samples']) == 1):
            select_sample_spec.add(ID)
    
    #subset of selected group specific features
    select_group_spec = set()
    for ID in all_select_no_blank.difference(select_sample_spec):
        if (
            (len(feature_dicts[str(ID)]['set_groups']) == 1)
            and not
            ('GENERAL' in feature_dicts[str(ID)]['set_groups'])
        ):
            select_group_spec.add(ID)
    
    #subtract sample spec and group spec features from total
    select_remainder = all_select_no_blank.difference(select_sample_spec)
    select_remainder = select_remainder.difference(select_group_spec)
    
    #non-selected features (subtracted blanks+ms1)
    all_nonsel_no_blank = all_nonblank_set.difference(all_select_no_blank)
    
    #subset of nonselected sample specific features
    nonselect_sample_spec = set()
    for ID in all_nonsel_no_blank:
        if (len(feature_dicts[str(ID)]['presence_samples']) == 1):
            nonselect_sample_spec.add(ID)
    
    #subset of nonselected group specific features
    nonselect_group_spec = set()
    for ID in all_nonsel_no_blank.difference(nonselect_sample_spec):
        if (
            (len(feature_dicts[str(ID)]['set_groups']) == 1)
            and not
            ('GENERAL' in feature_dicts[str(ID)]['set_groups'])
        ):
            nonselect_group_spec.add(ID)
    
    #subtract sample spec and group spec features from total
    nonselect_remainder = all_nonsel_no_blank.difference(nonselect_sample_spec)
    nonselect_remainder = nonselect_remainder.difference(nonselect_group_spec)
    
    return {
        ###GENERAL
        'all_features' : list(all_feature_set),
        'blank_ms1' : list(blank_ms1_set),
        'all_nonblank' : list(all_nonblank_set),
        ###SELECTED
        'all_select_no_blank' : list(all_select_no_blank),
        'select_sample_spec' : list(select_sample_spec),
        'select_group_spec' : list(select_group_spec),
        'select_remainder' : list(select_remainder),
        ###NONSELECTED
        'all_nonsel_no_blank' : list(all_nonsel_no_blank),
        'nonselect_sample_spec' : list(nonselect_sample_spec),
        'nonselect_group_spec' : list(nonselect_group_spec),
        'nonselect_remainder' : list(nonselect_remainder),
        }

def calc_diversity_score(sample_stats, samples):
    '''Calculate diversity scores for each sample, return list'''
    list_div_scores = list()
    for sample in samples:
        try:
            list_div_scores.append(round(
                (
                len(
                    set(sample_stats["cliques_per_sample"][sample]).difference(
                        set(sample_stats["set_blank_cliques"])
                        )
                    )
                / 
                len(
                    set(sample_stats["set_all_cliques"]).difference(
                        set(sample_stats["set_blank_cliques"]))
                    )
                ),
            2))
        except:
            list_div_scores.append(0)
    return list_div_scores

def calc_specificity_score(sample_stats, samples, sample_unique_cliques):
    '''Calculate specificity scores for each sample, return list'''
    list_spec_scores = list()
    for sample in samples:
        try:
            list_spec_scores.append(round(
                (
                (len(sample_unique_cliques[sample]))
                / 
                len(
                    set(sample_stats["cliques_per_sample"][sample]).difference(
                        set(sample_stats["set_blank_cliques"]))
                    )
                ),
            2))
        except:
            list_spec_scores.append(0)
    return list_spec_scores

def append_scatter_text(
    row,
    fill,
    line,
    width,
    bordercolor,
    feat_dicts
    ):
    '''Create scatter trace with hoverlabel'''
    ID=str(row["feature_ID"])
    
    cosine_ann = "None"
    if feat_dicts[ID]['cosine_annotation']:
        cosine_ann = ''.join([
            feat_dicts[ID]['cosine_annotation_list'][0]['name'],
            ])
    cosine_ann = (cosine_ann[:75] + '...') if len(cosine_ann) > 75 else cosine_ann
    
    ms2query_ann = "None"
    if feat_dicts[ID]['ms2query']:
        ms2query_ann = ''.join([
            feat_dicts[ID]['ms2query_results'][0]['analog_compound_name'],
            ])
    ms2query_ann = (ms2query_ann[:75] + '...') if len(ms2query_ann) > 75 else ms2query_ann
    
    text = (f'Feature ID <b>{row["feature_ID"]}</b>' +
            '<br>' +
            f'<i>m/z</i> <b>{row["precursor_mz"]}</b>' +
            '<br>' +
            f'RT (min) <b>{row["retention_time"]}</b>' +
            '<br>' +
            f'Lib. annot. <b>{cosine_ann}</b>' +
            '<br>' +
            f'MS2Query <b>{ms2query_ann}</b>' +
            '<br>'
            )
    return go.Scatter(
        x=np.array(row['pseudo_chrom_trace'][0]),
        y=np.array(row['pseudo_chrom_trace'][1]),
        fill='toself',
        fillcolor=fill,
        showlegend=False,
        mode="lines",
        line={
            'color' : line,
            'shape' : 'spline',
            'smoothing' : 0.8,
            'width' : width,
            },
        hoverinfo="text", #change to 'skip' if want to suppress
        text=text,
        hoverlabel={
            'bgcolor' : 'white',
            'bordercolor' : bordercolor}
        )






def plot_central_chrom(
    sel_sample,
    active_feature_index,
    sample_stats,
    samples,
    subsets,
    feature_dicts,
    ):
    '''Plot central chromatogram'''
    fig = go.Figure()
    fig.update_layout(
        margin = dict(t=0,b=0, r=0),
        height = 300,
        )

    fig.update_xaxes(
        autorange=False,
        visible=True,
        range=[
            (sample_stats["rt_min"]-(sample_stats["rt_range"]*0.05)),
            (sample_stats["rt_max"]+(sample_stats["rt_range"]*0.05)),
            ],
        )
    
    fig.update_yaxes(
        autorange=False,
        title_text="Relative Intensity",
        range=[0, 1.05],
        )
    
    for id, row in samples[sel_sample].iterrows():
        if int(row['feature_ID']) in subsets[sel_sample]['blank_ms1']:
            fig.add_trace(
                append_scatter_text(
                    row,
                    color_dict['light_yellow'],
                    color_dict['yellow'],
                    4,
                    color_dict['black'],
                    feature_dicts,
                    )
                )
        elif int(row['feature_ID']) in subsets[sel_sample]['select_sample_spec']:
            fig.add_trace(
                append_scatter_text(
                    row,
                    color_dict['light_green'],
                    color_dict['purple'],
                    4,
                    color_dict['black'],
                    feature_dicts,
                    )
                )
        elif int(row['feature_ID']) in subsets[sel_sample]['select_group_spec']:
            fig.add_trace(
                append_scatter_text(
                    row,
                    color_dict['light_green'],
                    color_dict['black'],
                    4,
                    color_dict['black'],
                    feature_dicts,
                    )
                )
        elif int(row['feature_ID']) in subsets[sel_sample]['select_remainder']:
            fig.add_trace(
                append_scatter_text(
                    row,
                    color_dict['light_green'],
                    color_dict['green'],
                    4,
                    color_dict['black'],
                    feature_dicts,
                    )
                )
        elif int(row['feature_ID']) in subsets[sel_sample]['nonselect_sample_spec']:
            fig.add_trace(
                append_scatter_text(
                    row,
                    color_dict['light_cyan'],
                    color_dict['purple'],
                    4,
                    color_dict['black'],
                    feature_dicts,
                    )
                )
        elif int(row['feature_ID']) in subsets[sel_sample]['nonselect_group_spec']:
            fig.add_trace(
                append_scatter_text(
                    row,
                    color_dict['light_cyan'],
                    color_dict['black'],
                    4,
                    color_dict['black'],
                    feature_dicts,
                    )
                )
        elif int(row['feature_ID']) in subsets[sel_sample]['nonselect_remainder']:
            fig.add_trace(
                append_scatter_text(
                    row,
                    color_dict['light_cyan'],
                    color_dict['cyan'],
                    4,
                    color_dict['black'],
                    feature_dicts,
                    )
                )
        else:
            fig.add_trace(
                append_scatter_text(
                    row,
                    color_dict['black'],
                    color_dict['black'],
                    4,
                    color_dict['black'],
                    feature_dicts,
                    )
                )

    if isinstance(active_feature_index, int):
        fig.add_shape(
            type="rect",
            xref="x", 
            yref="y",
            x0=samples[sel_sample].at[
                active_feature_index, 'rt_start'],
            x1=samples[sel_sample].at[
                active_feature_index, 'rt_stop'], 
            y0=0, 
            y1=(samples[sel_sample].at[
                active_feature_index, 'norm_intensity'] * 1),
            line={
                'color' : color_dict['blue'],
                'width' : 5,
                'dash' : 'dash',}
        )
    
    return fig




def plot_clique_chrom(
    selected_sample,
    active_feature_index,
    active_feature_id,
    sample_stats,
    samples,
    feature_dicts,
    ):
    '''Plot clique chromatogram - overview'''
    fig = go.Figure()
    
    fig.update_layout(
        margin = dict(t=0,b=0,r=0),
        height = 100,
        )
    
    fig.update_yaxes(
        visible=False,
        )
    
    fig.update_xaxes(
        autorange=False,
        title_text="Retention Time (min)",
            range=[
                (sample_stats["rt_min"]-(sample_stats["rt_range"]*0.05)),
                (sample_stats["rt_max"]+(sample_stats["rt_range"]*0.05)),
                ],
            )

    if isinstance(active_feature_index, int):
        if feature_dicts[str(active_feature_id)]['similarity_clique']:
            for clique_member in (
                sample_stats['cliques']
                    [str(feature_dicts[str(active_feature_id)]['similarity_clique_number'])]
                    [0]
                ):
                if clique_member != active_feature_id:
                    try:
                        row = samples[selected_sample].loc[
                            samples[selected_sample]['feature_ID'] 
                            == clique_member].squeeze()
                        fig.add_trace(
                            append_scatter_text(
                                row,
                                color_dict['light_red'],
                                color_dict['red'],
                                3,
                                color_dict['black'],
                                feature_dicts,
                                )
                            )
                    except:
                        pass
        fig.add_trace(
                append_scatter_text(
                    samples[selected_sample].loc[
                        samples[selected_sample]['feature_ID'] 
                        == active_feature_id].squeeze(),
                    color_dict['light_blue'],
                    color_dict['blue'],
                    3,
                    color_dict['black'],
                    feature_dicts,
                    )
                )
    return fig

def plot_mini_chrom(
    selected_sample,
    active_feature_id,
    sample_stats,
    samples,
    feature_dicts,
    ):
    '''Plot mini-chromatogram overview'''
    
    fig = make_subplots(rows=1, cols=1)

    if isinstance(active_feature_id, int):

        try: 
            nr_subplots = len(
                feature_dicts[str(active_feature_id)]['presence_samples'])
        except KeyError:
            nr_subplots = 0
    
        fig = make_subplots(
            rows=nr_subplots, 
            cols=1,
            shared_xaxes=True,
            x_title="Retention Time (min)",
            subplot_titles=[
                x for x in 
                feature_dicts[str(active_feature_id)]['presence_samples']
                ]
            )
        
        fig.update_annotations(
            font_size=12
            )

        fig.update_yaxes(visible=False)
        
        row_counter = 1
        for sample in feature_dicts[str(active_feature_id)]['presence_samples']:
            feature_row = ""
            for id, row in samples[sample].iterrows():
                if row['feature_ID'] == active_feature_id:
                    active_feature_row = copy.deepcopy(row)
                elif row['norm_intensity'] > 0.05:
                    fig.append_trace(append_scatter_text(
                            row,
                            color_dict['light_grey'],
                            color_dict['grey'],
                            2,
                            color_dict['grey'],
                            feature_dicts,
                            ),
                        row=row_counter, 
                        col=1
                        )
            try:
                fig.append_trace(append_scatter_text(
                    active_feature_row,
                    color_dict['blue'],
                    color_dict['black'],
                    2,
                    color_dict['black'],
                    feature_dicts,
                ),
                row=row_counter, 
                col=1
                )
            except TypeError:
                pass

            row_counter = row_counter + 1

    fig.update_xaxes(
        autorange=False,
        range=[
            (sample_stats["rt_min"]-(sample_stats["rt_range"]*0.05)),
            (sample_stats["rt_max"]+(sample_stats["rt_range"]*0.05)),
            ],
        )
    
    fig.update_yaxes(
    autorange=False,
    range=[0, 1],
    visible=False,
    )
    
    fig.update_layout(
    margin = dict(r=0,l=0,b=0,t=50),
    )
    
    return fig


def modify_feature_info_df(
    smpl,
    ID,
    index,
    feat_dicts,
    samples,
    sample_stats,
    ):
    '''Modify feature_info_dataframe for feature info display'''
    #change to str for feature dict querying
    ID = str(ID)
    
    #Intensity per sample
    int_sample = ''.join(
        [str(samples[smpl].at[index, 'intensity']), ' (', smpl,')',]
        )
    
    #best cosine match
    cosine_annotation = None
    if feat_dicts[ID]['cosine_annotation']:
        cosine_annotation = ''.join([
            '(Name: <b>', feat_dicts[ID]['cosine_annotation_list'][0]['name'],
            '</b>;', '<br>', 'Score: ',
            str(feat_dicts[ID]['cosine_annotation_list'][0]['score']), ';',
            '<br>', 'Nr of matched fragments: ',
            str(feat_dicts[ID]['cosine_annotation_list'][0]['nr_matches']),
            ')', ])

    #Best ms2query match
    ann_ms2query = None
    mass_diff_ms2query = None
    class_ms2query = None
    if feat_dicts[ID]['ms2query']:
        ann_ms2query = ''.join([
            'Name: ', feat_dicts[ID]['ms2query_results'][0]['Link'], ';',
            '<br>', 'Score: ', str(round(feat_dicts[ID]['ms2query_results'][0]
                ['ms2query_model_prediction'],3)), ])
        mass_diff_ms2query = ''.join([ 
            'Δ ', str(round(feat_dicts[ID]['ms2query_results'][0]
                ['precursor_mz_difference'],3)),
            ' <i>m/z</i> (',
            str(round(feat_dicts[ID]['ms2query_results'][0]
                ['precursor_mz_analog'],3)), ')',])
        class_ms2query = ''.join([ 
            str(feat_dicts[ID]['ms2query_results'][0]['npc_class_results']),
            ' (NP Classifier);', '<br>',
            str(feat_dicts[ID]['ms2query_results'][0]['cf_subclass']),
            ' (ClassyFire)' ])
    
    fold_diff_list = []
    if feat_dicts[ID]['dict_fold_diff'] is not None:
        for comp in feat_dicts[ID]['sorted_fold_diff']:
            if feat_dicts[ID]['dict_fold_diff'][comp] > 1:
                fold_diff_list.append(''.join([
                    str(feat_dicts[ID]['dict_fold_diff'][comp]),
                    ' (', comp, '),', '<br>',])) 

    combined_list_int = []
    for i in range(len(feat_dicts[ID]['presence_samples'])):
        combined_list_int.append(''.join([
            str(feat_dicts[ID]['intensities_samples'][i]),' (',
            str(feat_dicts[ID]['presence_samples'][i]), '),', '<br>', ]))

    combined_list_bio = []
    if feat_dicts[ID]['bioactivity_associated']:
        for i in range(len(feat_dicts[ID]['presence_samples'])):
            combined_list_bio.append(''.join([
                str(feat_dicts[ID]['bioactivity_samples'][i]), ' (',
                str(feat_dicts[ID]['presence_samples'][i]), '),', '<br>',
                ]))
    else:
        combined_list_bio = [None]
        
    combined_list_adducts = []
    if feat_dicts[ID]['ann_adduct_isotop']:
        for i in range(len(feat_dicts[ID]['ann_adduct_isotop'])):
            combined_list_adducts.append(''.join([
                str(feat_dicts[ID]['ann_adduct_isotop'][i]),
                ',<br>', ]))
    else:
        combined_list_adducts = [None]

    groups_cliques= []
    if feat_dicts[ID]['similarity_clique']:
        for group in feat_dicts[ID]['set_groups_clique']:
            groups_cliques.append(''.join([group, '<br>', ]))
    else:
        groups_cliques = [None]
    
    sim_clique_len = None
    sim_clique_list = None
    if feat_dicts[ID]['similarity_clique']:
        sim_clique_len = len(
            sample_stats['cliques'][
                str(feat_dicts[ID]['similarity_clique_number'])][0]
            )
        sim_clique_list = (', '.join(str(i) for i in 
            sample_stats['cliques'][
                str(feat_dicts[ID]['similarity_clique_number'])][0]))

    placeholder = '-----'
    data = [
        ['Feature ID', ID],
        ['Precursor <i>m/z</i>', feat_dicts[ID]['precursor_mz']],
        ['Retention time (min)', samples[smpl].at[index, 'retention_time']],
        ['Feature intensity (absolute)', int_sample],
        [placeholder, placeholder],
        ['Medium/blank associated', feat_dicts[ID]['blank_associated']],
        ['Relative intensity', round(samples[smpl].at[index, 'rel_intensity_score'],2)], 
        ['QuantData score', round(samples[smpl].at[index, 'bioactivity_score'],2)],
        ['Novelty score', round(samples[smpl].at[index, 'novelty_score'],2)],
        [placeholder, placeholder],
        ['User-library: matches', cosine_annotation],
        ['MS2Query: best analog/match', ann_ms2query],
        ['MS2Query: <i>m/z</i> diff. to best analog/match', mass_diff_ms2query],
        ['MS2Query: pred. class of best analog/match', class_ms2query],
        [placeholder, placeholder],
        ['Found in groups', ("".join(f"{i}<br>" for i in feat_dicts[ID]['set_groups']))],
        ['Fold-differences groups', ("".join(str(i) for i in fold_diff_list))],
        ['Intensity per sample', ("".join(str(i) for i in combined_list_int))],
        ['Bioactivity per sample', ("".join(str(i) for i in combined_list_bio))],
        ['Putative adducts', ("".join(str(i) for i in combined_list_adducts))],
        [placeholder, placeholder],
        ['Molecular network ID', feat_dicts[ID]['similarity_clique_number']],
        ['Groups in molecular network', ("".join(str(i) for i in groups_cliques))],
        ['Number of features in MN', sim_clique_len],
        ['IDs of features in MN', sim_clique_list],
    ]
    
    df = pd.DataFrame(data, columns=['Attribute', 'Description'])
    
    return df.to_dict('records')


def empty_feature_info_df():
    '''Return empty dataframe'''
    placeholder = '-----'
    data = [
        ['Feature ID', None],
        ['Precursor <i>m/z</i>', None],
        ['Retention time (min)', None],
        ['Feature intensity (absolute)', None],
        [placeholder, placeholder],
        ['Medium/blank associated', None],
        ['Relative intensity', None], 
        ['QuantData score', None],
        ['Novelty score', None],
        [placeholder, placeholder],
        ['User-library: matches', None],
        ['MS2Query: best analog/match', None],
        ['MS2Query: <i>m/z</i> diff. to best analog/match', None],
        ['MS2Query: pred. class of best analog/match', None],
        [placeholder, placeholder],
        ['Found in groups', None],
        ['Fold-differences groups', None],
        ['Intensity per sample', None],
        ['Bioactivity per sample', None],
        ['Putative adducts', None],
        [placeholder, placeholder],
        ['Molecular network ID', None],
        ['Groups in molecular network', None],
        ['Number of features in MN', None],
        ['IDs of features in MN', None],
    ]
    
    df = pd.DataFrame(data, columns=['Attribute', 'Description'])
    
    return df.to_dict('records')


def generate_cyto_elements(
    sel_sample,
    active_feature_id,
    feat_dicts,
    sample_stats,
    ):
    '''Generate cytoscape elements.
    
    Notes
    -----
    Creates nested list of cytoscape elements (nodes and edges).
    Using conditional expressions, nodes are colored by applying
    different classes. These classes have stylesheets associated, which 
    are defined in variables.py, and which is 
    called at dashboard startup as "global" variables. 
    
    List comprehension with multiple conditionals:
    do A if condition a
    else do B if condition b
    else do C if condition c
    for i in list
    '''
    ID = str(active_feature_id)

    #tests if currently selected feature is in a similarity clique
    if feat_dicts[ID]['similarity_clique']:
        
        node_list = list(
            sample_stats['cliques'][
                str(feat_dicts[ID]['similarity_clique_number'])][0]
            )
        edges_list = list(
            sample_stats['cliques'][
                str(feat_dicts[ID]['similarity_clique_number'])][1]
            )
        precursor_list = [feat_dicts[str(i)]['precursor_mz'] for i in node_list]
        id_precursor_dict = {
            node_list[i] : [precursor_list[i],
                            feat_dicts[str(node_list[i])]['feature_ID'],]
            for i in range(len(node_list))
            }
        
        if len(node_list) <= 250:
            #Creates list of nodes, with each node as a dictionary.
            nodes = [
            
                #first condition: selected, unique to sample
                {
                'data': {
                    'id': str(i), 
                    'label': "".join([str(id_precursor_dict[i][0])," m/z",]),
                },
                'classes': 'selected_unique_sample',
                }
                if ((id_precursor_dict[i][1] == int(ID))
                and
                (len(feat_dicts[str(i)]['presence_samples']) == 1)
                )
                
                #second condition: selected, unique to group
                else {
                    'data': {
                        'id': str(i), 
                        'label': "".join([str(id_precursor_dict[i][0])," m/z",]),
                    },
                    'classes': 'selected_unique_group',
                }
                if ((id_precursor_dict[i][1] == int(ID))
                and
                (len(feat_dicts[str(i)]['set_groups']) == 1)
                and not 
                ('GENERAL' in feat_dicts[str(i)]['set_groups'])
                )
                
                #third condition: selected - RETAIN
                else {
                    'data': {
                        'id': str(i), 
                        'label': "".join([str(id_precursor_dict[i][0])," m/z",]),
                    },
                    'classes': 'selected',
                }
                if (id_precursor_dict[i][1] == int(ID))
                
                #fourth condition: in sample, unique to sample
                else {
                    'data': {
                        'id': str(i), 
                        'label': "".join([str(id_precursor_dict[i][0])," m/z",]),
                    },
                    'classes': 'sample_unique_sample',
                }
                if (
                    (id_precursor_dict[i][1] in 
                        sample_stats['features_per_sample'][sel_sample])
                and
                    (sel_sample in feat_dicts[str(i)]['presence_samples'])
                and
                    (len(feat_dicts[str(i)]['presence_samples']) == 1)
                    )
                    
                #fifth condition: in sample, unique to group
                else {
                    'data': {
                        'id': str(i), 
                        'label':"".join([str(id_precursor_dict[i][0])," m/z",]),
                    },
                    'classes': 'sample_unique_group',
                }
                if (
                    (id_precursor_dict[i][1] in 
                        sample_stats['features_per_sample'][sel_sample])
                and
                    (sel_sample in feat_dicts[str(i)]['presence_samples'])
                and
                    (len(feat_dicts[str(i)]['set_groups']) == 1)
                and not 
                    ('GENERAL' in feat_dicts[str(i)]['set_groups'])
                )
                
                #sixth condition: in sample, unique to group - RETAIN
                else {
                    'data': {
                        'id': str(i), 
                        'label': "".join([str(id_precursor_dict[i][0])," m/z",]),
                    },
                    'classes': 'sample',
                }
                if (
                    (id_precursor_dict[i][1] in 
                        sample_stats['features_per_sample'][sel_sample])
                )
                
                #seventh condition: not in sample, unique to the group
                #where it is found
                else {
                    'data': {
                        'id': str(i), 
                        'label': "".join([str(id_precursor_dict[i][0])," m/z",]),
                    },
                    'classes': 'default_unique_group',
                }
                if (
                    (len(feat_dicts[str(i)]['set_groups']) == 1)
                and
                    (feat_dicts[str(i)]['set_groups'] == feat_dicts[ID]['set_groups'])
                and not 
                    ('GENERAL' in feat_dicts[str(i)]['set_groups'])
                )
                
                #eight condition: everything else
                else {
                    'data': {
                        'id': str(i), 
                        'label': "".join([str(id_precursor_dict[i][0])," m/z",]),
                    },
                    'classes': 'default',
                }
                for i in id_precursor_dict
            ]
            
            #Create list of edges (one dictionary per edge)
            edges = [
                {'data': {
                    'source': str(edges_list[i][0]),
                    'target': str(edges_list[i][1]),
                    'weight': edges_list[i][2],
                    'mass_diff' : abs(round(
                        (feat_dicts[str(edges_list[i][0])]['precursor_mz'] -
                        feat_dicts[str(edges_list[i][1])]['precursor_mz']), 3
                        )),
                    }
                }
                for i in range(len(edges_list))
            ]
            
            #Concatenate nodes and edges into single list
            elements = nodes + edges
            return elements
        else:
            return []
    else:
        return []

def add_nodedata(
    data,
    feat_dicts,
    ):
    '''Append node data to df'''
    
    annotation = ''.join([
        (feat_dicts[str(data['id'])]['cosine_annotation_list'][0]['name']
            if feat_dicts[str(data['id'])]['cosine_annotation']
            else 'None '),
        '<b>(user-library)</b>, <br>',
        (feat_dicts[str(data['id'])]['ms2query_results'][0]['analog_compound_name']
            if feat_dicts[str(data['id'])]['ms2query'] else "None"),
        '<b>(MS2Query)</b>',
        ])
        
    combined_list_int = []
    for i in range(len(feat_dicts[str(data['id'])]['presence_samples'])):
        combined_list_int.append(''.join([
            str(feat_dicts[str(data['id'])]['presence_samples'][i]),
            '<br>', ]))

    content = [
        ['Feature ID', data['id']],
        ['Precursor <i>m/z</i>', feat_dicts[str(data['id'])]['precursor_mz']],
        ['Retention time (avg)', feat_dicts[str(data['id'])]['average_retention_time']],
        ['Annotation', annotation],
        ['Detected in samples', ("".join(str(i) for i in combined_list_int))],
    ]
    
    df = pd.DataFrame(content, columns=['Node info', 'Description'])
    
    return df.to_dict('records')


def add_edgedata(data, feat_dicts,):
    '''Append edge data to df'''
    
    content = [
        ['Connected nodes (IDs)', ''.join([data['source'],'--', data['target']])],
        ['Weight of edge', data['weight']],
        ['<i>m/z</i> difference between nodes', data['mass_diff']],
        ]
    df = pd.DataFrame(content, columns=['Edge info', 'Description'])

    return df.to_dict('records')


def export_sel_peaktable(samples, sel_sample):
    '''Return columns from pandas df'''
    return samples[sel_sample].loc[:,[
            'feature_ID',
            'precursor_mz',
            'retention_time',
            'fwhm',
            'intensity',
            'norm_intensity',
            'rt_start',
            'rt_stop',
            'putative_adduct_detection',
            'rel_intensity_score',
            'convolutedness_score',
            'bioactivity_score',
            'novelty_score',
            'in_blank',
            'ms1_only',]]

def prepare_log_file(contents):
    '''Concatenate information for logging file'''
    return [
        ''.join(['FERMO_version: ', str(contents['FERMO_version'])]),
        'Input file names:',
        contents['input_filenames'],
        'Processing parameters:',
        contents['params_dict'],
        'Processing log:',
        contents['logging_dict']
        ]

def prepare_log_file_filters(contents, thresholds):
    '''Concatenate information for logging file - include set filters'''
    return [
        ''.join(['FERMO_version: ', str(contents['FERMO_version'])]),
        'Input file names:',
        contents['input_filenames'],
        'Processing parameters:',
        contents['params_dict'],
        'Filters applied',
        thresholds,
        'Processing log:',
        contents['logging_dict']
        ]
    
    


def export_features(feature_dicts):
    '''From feature dicts, create lists, convert to pandas df'''
    t_feature_ID = []
    t_prec_mz = []
    t_avg_ret_time = []
    t_rt_samples = []
    t_presence_samp = []
    t_int_samples = []
    t_bioact = []
    t_blank = []
    t_sim_cliq_bool = []
    t_sim_cliq_nr = []
    t_cos_ann_list = []
    t_ms2query_list = []
    t_set_groups = []
    t_set_groups_clique = []
    t_dict_fold_diff = []
        
    for ID in feature_dicts:
        t_feature_ID.append(feature_dicts[ID]['feature_ID'])
        t_prec_mz.append(feature_dicts[ID]['precursor_mz'])
        t_avg_ret_time.append(feature_dicts[ID]['average_retention_time'])
        t_rt_samples.append(feature_dicts[ID]['rt_in_samples'])
        t_presence_samp.append(feature_dicts[ID]['presence_samples'])
        t_int_samples.append(feature_dicts[ID]['intensities_samples'])
        t_bioact.append(feature_dicts[ID]['bioactivity_associated'])
        t_blank.append(feature_dicts[ID]['blank_associated'])
        t_sim_cliq_bool.append(feature_dicts[ID]['similarity_clique'])
        t_sim_cliq_nr.append(feature_dicts[ID]['similarity_clique_number'])
        t_cos_ann_list.append(feature_dicts[ID]['cosine_annotation_list'])
        t_ms2query_list.append(feature_dicts[ID]['ms2query_results'])
        t_set_groups.append(feature_dicts[ID]['set_groups'])
        t_set_groups_clique.append(feature_dicts[ID]['set_groups_clique'])
        t_dict_fold_diff.append(feature_dicts[ID]['dict_fold_diff'])
        
    return pd.DataFrame({
        'feature_ID': t_feature_ID,
        'precursor_mz': t_prec_mz,
        'avg_ret_time': t_avg_ret_time,
        'presence_samples': t_presence_samp,
        'ret_time_in_samples': t_rt_samples,
        'intensities_samples': t_int_samples,
        'bioact_assoc': t_bioact,
        'blank_assoc': t_blank,
        'annotation_user_lib': t_cos_ann_list,
        'ms2query_results': t_ms2query_list,
        'groups_assoc': t_set_groups,
        'similarity_clique': t_sim_cliq_bool,
        'similarity_clique_number': t_sim_cliq_nr,
        'similarity_clique_groups': t_set_groups_clique,
        'groups_fold_differences': t_dict_fold_diff,
        })


