import json
from typing import Tuple

from fermo.app_utils.dashboard.dashboard_functions import color_dict


def generate_cyto_elements(
    sel_sample: str,
    active_feature_id: int,
    feat_dicts: dict,
    sample_stats: dict,
) -> Tuple[list, str]:
    '''Generate cytoscape elements.

    Parameters
    ----------
    sel_sample : `str`\n
    active_feature_id : `int`\n
    feature_dicts : `dict`\n
    sample_stats : `dict`\n

    Returns
    -------
    networkJSON: `list`
        stringified JSON object of the list of nodes and edges (both
        represented as dictionaries)
    error_message: `str`

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

    if not active_feature_id:
        networkJSON = []
        message = '''No network selected - click any feature in the
        chromatogram overview.'''

    # tests if currently selected feature is in a similarity clique
    elif feat_dicts[ID]['similarity_clique']:

        node_list = list(
            sample_stats['cliques'][
                str(feat_dicts[ID]['similarity_clique_number'])][0]
        )
        edges_list = list(
            sample_stats['cliques'][
                str(feat_dicts[ID]['similarity_clique_number'])][1]
        )
        precursor_list = [
            feat_dicts[str(i)]['precursor_mz'] for i in node_list
        ]
        id_precursor_dict = {
            node_list[i]: [
                precursor_list[i],
                feat_dicts[str(node_list[i])]['feature_ID'],
            ]
            for i in range(len(node_list))
        }

        if len(node_list) <= 250:
            # Creates list of nodes, with each node as a dictionary.
            nodes = [
                # first condition: selected, unique to sample
                {'data': {
                    'id': str(i),
                    'label': "".join([str(id_precursor_dict[i][0]), " m/z", ]),
                }, 'classes': 'selected_unique_sample', }
                if ((id_precursor_dict[i][1] == int(ID)) and (
                    len(feat_dicts[str(i)]['presence_samples']) == 1
                ))

                # second condition: selected, unique to group
                else {
                    'data': {
                        'id': str(i),
                        'label': "".join([str(id_precursor_dict[i][0]),
                                          " m/z",]),
                    },
                    'classes': 'selected_unique_group',
                }
                if ((id_precursor_dict[i][1] == int(ID)) and (
                    len(feat_dicts[str(i)]['set_groups']) == 1
                ) and not (
                    'GENERAL' in feat_dicts[str(i)]['set_groups']
                ))

                # third condition: selected - RETAIN
                else {
                    'data': {
                        'id': str(i),
                        'label': "".join([str(id_precursor_dict[i][0]),
                                          " m/z",]),
                    },
                    'classes': 'selected',
                }
                if (id_precursor_dict[i][1] == int(ID))

                # fourth condition: in sample, unique to sample
                else {
                    'data': {
                        'id': str(i),
                        'label': "".join([str(id_precursor_dict[i][0]),
                                          " m/z",]),
                    },
                    'classes': 'sample_unique_sample',
                }
                if ((id_precursor_dict[i][1] in
                     sample_stats['features_per_sample'][sel_sample])
                    and (sel_sample in feat_dicts[str(i)]['presence_samples'])
                    and (len(feat_dicts[str(i)]['presence_samples']) == 1)
                    )

                # fifth condition: in sample, unique to group
                else {
                    'data': {
                        'id': str(i),
                        'label': "".join([str(id_precursor_dict[i][0]),
                                          " m/z",]),
                    },
                    'classes': 'sample_unique_group',
                }
                if ((id_precursor_dict[i][1] in
                     sample_stats['features_per_sample'][sel_sample])
                    and (sel_sample in feat_dicts[str(i)]['presence_samples'])
                    and (len(feat_dicts[str(i)]['set_groups']) == 1)
                    and not ('GENERAL' in feat_dicts[str(i)]['set_groups'])
                    )

                # sixth condition: in sample, unique to group - RETAIN
                else {
                    'data': {
                        'id': str(i),
                        'label': "".join([str(id_precursor_dict[i][0]),
                                          " m/z",]),
                    },
                    'classes': 'sample',
                }
                if (
                    (id_precursor_dict[i][1] in
                     sample_stats['features_per_sample'][sel_sample])
                )

                # seventh condition: not in sample, unique to the group
                # where it is found
                else {
                    'data': {
                        'id': str(i),
                        'label': "".join([str(id_precursor_dict[i][0]),
                                          " m/z",]),
                    },
                    'classes': 'default_unique_group',
                }
                if ((len(feat_dicts[str(i)]['set_groups']) == 1)
                    and (feat_dicts[str(i)]['set_groups']
                         == feat_dicts[ID]['set_groups'])
                    and not ('GENERAL' in feat_dicts[str(i)]['set_groups'])
                    )

                # eight condition: everything else
                else {
                    'data': {
                        'id': str(i),
                        'label': "".join([str(id_precursor_dict[i][0]),
                                          " m/z",]),
                    },
                    'classes': 'default',
                }
                for i in id_precursor_dict
            ]

            # Create list of edges (one dictionary per edge)
            edges = [
                {'data': {
                    'source': str(edges_list[i][0]),
                    'target': str(edges_list[i][1]),
                    'weight': edges_list[i][2],
                    'mass_diff': abs(round(
                        (feat_dicts[str(edges_list[i][0])]['precursor_mz'] -
                         feat_dicts[str(edges_list[i][1])]['precursor_mz']),
                        3
                    )),
                }}
                for i in range(len(edges_list))
            ]

            # Concatenate nodes and edges into single list
            network = nodes + edges
            networkJSON = json.dumps(network)
            message = ''
        else:  # number of Nodes > 250
            networkJSON = []
            message = '''Spectral similarity network has too many elements for
                visualization (>250 features).'''
    else:
        networkJSON = []
        message = '''Selected feature has no associated spectral similarity
            network - MS1 only.'''

    return (networkJSON, message)


def collect_nodedata(
    nodedata: dict,
    feat_dicts: dict,
) -> list:
    '''Collect info of selected node for display in table

    Parameters
    ----------
    nodedata : `dict`
        Should look something like this: {'id': '9', 'label': '364.1614 m/z'}
    feature_dicts : `dict`

    Returns
    -------
    `list`
        List of lists
    '''
    if not nodedata:
        return [[]]

    feature_info = feat_dicts[str(nodedata['id'])]
    annotation = ''.join([
        (feature_info['cosine_annotation_list'][0]['name']
            if feature_info['cosine_annotation'] else 'None '),
        '<b>(user-library)</b>, <br>',
        (feature_info['ms2query_results'][0]['analog_compound_name']
            if feature_info['ms2query'] else "None "),
        '<b>(MS2Query)</b>',
    ])

    superclass_ms2query = ''.join([
        (str(feature_info['ms2query_results'][0]['npc_superclass_results']
             if feature_info['ms2query'] else "None ")),
        '<b>(NPC superclass)</b>, <br>',
        (str(feature_info['ms2query_results'][0]['cf_superclass']
             if feature_info['ms2query'] else "None ")),
        '<b>(CF superclass)</b>',
    ])

    combined_list_int = []
    for i in range(len(feature_info['presence_samples'])):
        combined_list_int.append(''.join([
            str(feature_info['presence_samples'][i]),
            '<br>',
        ]))

    content = [
        ['Feature ID', nodedata['id']],
        ['Precursor <i>m/z</i>', feature_info['precursor_mz']],
        ['Retention time (avg)', feature_info['average_retention_time']],
        ['Annotation', annotation],
        ['MS2Query class pred', superclass_ms2query],
        ['Detected in samples', ("".join(str(i) for i in combined_list_int))],
    ]

    return content


def collect_edgedata(
    edgedata: dict,
) -> list:
    '''Collect info of selected edge for display in table

    Parameters
    ----------
    edgedata : `dict`
        Should look something like this: {
            'source': '93',
            'target': '12',
            'weight': 0.93,
            'mass_diff': 15.994,
            'id': '48ef5707-0580-424e-8e7d-1659c0885856'
        }

    Returns
    -------
    `list`
        List of lists
    '''
    if not edgedata:
        return [[]]

    content = [
        ['Connected nodes (IDs)', ''.join([
            edgedata['source'],
            '--',
            edgedata['target']
        ])],
        ['Weight of edge', edgedata['weight']],
        ['<i>m/z</i> difference between nodes', edgedata['mass_diff']],
    ]

    return content


def stylesheet_cytoscape() -> str:
    '''Return stylesheet for cytoscape graph in JSON format.'''
    colors = color_dict()
    style = [{
        'selector': '.selected',
        'style': {
            'background-color': colors['light_blue'],
            'border-width': 4,
            'border-color': colors['blue'],
            'label': 'data(label)',
        }
    }, {
        'selector': '.selected_unique_sample',
        'style': {
            'background-color': colors['light_blue'],
            'border-width': 4,
            'border-color': colors['purple'],
            'label': 'data(label)',
        }
    }, {
        'selector': '.selected_unique_group',
        'style': {
            'background-color': colors['light_blue'],
            'border-width': 4,
            'border-color': colors['black'],
            'label': 'data(label)',
        }
    }, {
        'selector': '.sample',
        'style': {
            'background-color': colors['light_red'],
            'border-width': 4,
            'border-color': colors['red'],
            'label': 'data(label)',
        }
    }, {
        'selector': '.sample_unique_sample',
        'style': {
            'background-color': colors['light_red'],
            'border-width': 4,
            'border-color': colors['purple'],
            'label': 'data(label)',
        }
    }, {
        'selector': '.sample_unique_group',
        'style': {
            'background-color': colors['light_red'],
            'border-width': 4,
            'border-color': colors['black'],
            'label': 'data(label)',
        }
    }, {
        'selector': '.default',
        'style': {
            'background-color': colors['light_grey'],
            'border-width': 4,
            'border-color': colors['grey'],
            'label': 'data(label)',
        }
    }, {
        'selector': '.default_unique_sample',
        'style': {
            'background-color': colors['light_grey'],
            'border-width': 4,
            'border-color': colors['purple'],
            'label': 'data(label)',
        }
    }, {
        'selector': '.default_unique_group',
        'style': {
            'background-color': colors['light_grey'],
            'border-width': 4,
            'border-color': colors['black'],
            'label': 'data(label)',
        }
    }, {
        'selector': '[weight > 0.8]',
        'style': {
            'width': 2,
        }
    }, {
        'selector': '[weight > 0.85]',
        'style': {
            'width': 3,
        }
    },
        {
        'selector': '[weight > 0.90]',
        'style': {
            'width': 5,
            }
    }, {
        'selector': '[weight > 0.95]',
        'style': {
            'width': 7,
        }
    }, ]
    styleJSON = json.dumps(style)
    return styleJSON
