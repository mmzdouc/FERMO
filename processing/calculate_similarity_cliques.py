import matchms 
import os
import networkx as nx

from matchms.similarity.vector_similarity_functions import cosine_similarity_matrix
from ms2deepscore import MS2DeepScore
from ms2deepscore.models import load_model as load_ms2ds_model



def calculate_similarity_cliques(
    feature_dicts,
    sample_stats,
    spec_sim_tol,
    spec_sim_score_cutoff,
    spec_sim_max_links,
    algorithm,
    ):
    """Calculate cliques for features based on spectral similarity
    
    Parameters
    ----------
    feature_dicts : `dict`
        Feature_ID(keys):feature_dict(values)
    sample_stats : `dict`
        Dict holding general information on samples
    spec_sim_tol : `float`
        max m/z tolerance between two peaks to be a match (mod.cosine)
    spec_sim_score_cutoff : `float`
        minimal score to keep connection between two spectra (mod.cosine)
    spec_sim_max_links : `int`
        Max number of links that come from one node.
    algorithm : `str`
        Either 'modified_cosine' or 'ms2deepscore'
    
    Returns
    -------
    algorithm_used : `str`
        Reports algorithm used for logging
    
    Notes
    -----
    For all features with a MS2 fragmentation pattern, their pairwise
    similarity is calculated using matchms. A spectral similarity
    network is created and its output is stored in the feature object
    in a easy accessible way for the later cytoscape plotting. 

    Inspired by the tutorial from Florian Huber
    https://blog.esciencecenter.nl/build-your-own-mass-spectrometry-
    analysis-pipeline-in-python-using-matchms-part-i-d96c718c68ee

    #example code - might be of use in future
    for (u, v, wt) in subnetworks[50].edges.data('weight'):
    print(f"({u}, {v}, {wt:.3})")
    for entry in feature_dicts[205]['similarity_clique_list'][1]:
    print(entry[0],entry[1],entry[2],)
    """
    
    #Create subset of features for comparisons:
    #-must have a MS2 spectrum
    spectral_similarity = []
    for i in feature_dicts:
        if feature_dicts[i]['ms2spectrum'] is not None:
            spectral_similarity.append(feature_dicts[i]['feature_ID'])
    
    algorithm_used = None
    scores = None
    
    if algorithm == 'ms2deepscore':
        input_folder = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'libraries',)
        input_file = None
        for i in os.listdir(input_folder):
            if i.endswith('.hdf5'):
                input_file = os.path.join(input_folder, i)
                break
        
        try:
            ms2ds_model = load_ms2ds_model(input_file)
            scores = matchms.calculate_scores(
                [feature_dicts[i]['ms2spectrum'] for i in spectral_similarity],
                [feature_dicts[i]['ms2spectrum'] for i in spectral_similarity],
            MS2DeepScore(ms2ds_model, progress_bar=False),
            is_symmetric=True,
            )
            algorithm_used = 'ms2deepscore'
        except:
            print('WARNING: MS2DeepScore model file (*.hdf5) not found in folder "libraries".')
            print('WARNING: Fallback to "modified cosine" algorithm.')

    if algorithm == 'modified_cosine' or scores is None:
        modified_cosine = matchms.similarity.ModifiedCosine(
            tolerance=spec_sim_tol,)
        scores = matchms.calculate_scores(
            [feature_dicts[i]['ms2spectrum'] for i in spectral_similarity],
            [feature_dicts[i]['ms2spectrum'] for i in spectral_similarity],
            modified_cosine,
            is_symmetric=True,
            )
        algorithm_used = 'ms2deepscore'

    #sets settings of spectral similarity network 
    network_spec_sim = matchms.networking.SimilarityNetwork(
        identifier_key="id",
        score_cutoff=spec_sim_score_cutoff,
        max_links=spec_sim_max_links,
        top_n=10,
        link_method='mutual',
        )
        
    #calculates spectral similarity network 
    network_spec_sim.create_network(scores)
    
    #creates a networkx-based graph object (multigraph)
    network_graph = network_spec_sim.graph
    
    #creates a list of subgraphs (all cliques) - breaks up multigraph
    subnetworks = [
        network_graph.subgraph(c).copy() 
        for c in nx.connected_components(network_graph)
        ]

    #returns a dict with nonredundant list of nodes for each subgraph 
    #Some unknown error in network calculations creates "duplicate"
    #cliques (with stringified IDs instead of int -> mixed "set").
    #E.g. clique 1 = [169, 170, '171'], clique 2 = ['169', '170', 171],
    #with identical similarity values. 
    #Fixed: remove redundant cliques before storage
    counter_cliques = 0
    clusters = {}
    for i, subnet in enumerate(subnetworks):
        
        clique = list(set([int(j) for j in subnet.nodes]))
        clique = sorted(clique, 
                    key=lambda i: (isinstance(i, int), i), reverse=True)
        
        if not clique in clusters.values():
            clusters[i] = clique
            counter_cliques = counter_cliques + 1
        else:
            pass

    #append number of cliques to dict sample_stats
    sample_stats['nr_all_cliques'] = counter_cliques
    
    #for each subgraph in clusters, retrieve its edges; create
    #nonredundant list of edges (as sets), turn it again into lists
    #(so that they are sort-able), sort them after integers. 
    #This way, there are always the nodes on [0] and [1], while the 
    #weigth (their mod_cosine_similarity) is in [0] 
    for i in clusters:
        nodes = clusters[i]
        edges = []
        for u, v, wt in subnetworks[i].edges.data('weight'):
            edge = set([int(u), int(v), round(float(wt),2)])
            if edge not in edges:
                edges.append(edge)
            else:
                pass
        nr_edges = []
        for edge in edges:
            edge = list(edge)
            edge = sorted(edge, 
                    key=lambda i: (isinstance(i, int), i), reverse=True)
            nr_edges.append(edge)
        
        #add a dict with similarity clique lists to sample stats
        
        sample_stats['cliques'][i] = [nodes, nr_edges]
        
        
        #Append info to feature object
        #Each feature object has:
        #-similarity clique (is in one (True) or none (False)
        #-similarity_clique_number (the clique number in which it is)
        #-similarity_clique_list (list with [0] nodes, [1] edges)
        for j in clusters[i]:
            #add to feature objects
            feature_dicts[j]['similarity_clique'] = True
            feature_dicts[j]['similarity_clique_number'] = i
            feature_dicts[j]['similarity_clique_list'] = [nodes, nr_edges]
            #add to sample stats
            sample_stats['set_all_cliques'].add(i)
            if feature_dicts[j]['blank_associated']:
                sample_stats['set_blank_cliques'].add(i)


    #collect groups associated to a similarity clique
    for ID in feature_dicts:
        if feature_dicts[ID]['similarity_clique']:
            for member in feature_dicts[ID]['similarity_clique_list'][0]:
                for group in feature_dicts[member]['set_groups']:
                    feature_dicts[ID]['set_groups_clique'].add(group)
            feature_dicts[ID]['similarity_clique_list'] = []
        else:
            feature_dicts[ID]['set_groups_clique'] = None
            feature_dicts[ID]['similarity_clique_list'] = []

    #For each sample, create list of cliques that it contains
    for sample in sample_stats["samples_list"]:
        sample_stats["cliques_per_sample"][sample] = {
            feature_dicts[i]['similarity_clique_number']
            for 
            i in sample_stats["features_per_sample"][sample]
            if
            (feature_dicts[i]['similarity_clique'] == True)
            }
        sample_stats["cliques_per_sample"][sample] = list(sample_stats[
            "cliques_per_sample"][sample])
    
    return algorithm_used
    
