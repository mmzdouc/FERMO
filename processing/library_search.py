import matchms 
import os
import networkx as nx

def library_search(
    feature_dicts,
    ref_library,
    spec_sim_tol,
    spec_sim_score_cutoff,
    spec_sim_min_matched,
    ):
    """Compare features against reference spectral library
    
    Parameters
    ----------
    feature_dicts : `dict`
        Feature_ID(keys):feature_dict(values).
    infile : `str`
        path to reference spectral library mgf file.
    spec_sim_tol : `float`
        specifies the max tolerance between two fragments to match them
    spec_sim_score_cutoff : `float`
        minimal score to keep connection between two spectra (mod.cosine)
    spec_sim_min_matched : `int`
        minimal number of matched peaks for a match between spectra to 
        be considered
    
    Returns
    -------
    feature_dicts : `dict`
    
    Notes
    -----
    Inspired by the tutorial of Florian Huber
    (https://blog.esciencecenter.nl/build-your-own-mass-spectrometry-
    analysis-pipeline-in-python-using-matchms-part-i-d96c718c68ee)
    
    Function to perform spectral library matching of feature objects
    against a user-provided spectral library 
    (currently the cleaned GNPS library of user-submitted entries,
    downloaded on 26.06.2022).
    
    Cleaning procedure: matchms returns a generic error if the provided 
    library file contains malformed entries. By trial-and-error, these
    entries were pinpointed and removed. 
    Therefore, mgf file entries:
    -must not have pepmass=0.0
    -must not have pepmass=1.0
    
    The similarity measure is a ModifiedCosine due to its recently
    reported better performace than other similarity measures (see
    https://doi.org/10.1101/2022.06.01.494370).
    
    Matched against the library are only features that:
    -have a MS2 spectrum (i.e. not MS1 only)
    -are not medium components
    
    Matches of features against library entries are appended to 
    feature objects provided that:
    -the score of the match was >= user-set parameter
    -the number of matched peaks was  > user-set parameter
    This restricts the number of matches that are reported.
    """
    if ref_library is not None:
        #Create subset of features for comparisons:
        #-must have a MS2 spectrum
        #-must not be blank associated
        spectra = list()
        for i in feature_dicts:
            if (feature_dicts[i]['ms2spectrum'] is not None
            and not feature_dicts[i]['blank_associated']):
                spectra.append(feature_dicts[i]['ms2spectrum'])            
            else:
                pass

        #initializes modified-cosine-based spectral similarity calculation
        similarity_measure = matchms.similarity.ModifiedCosine(
            tolerance=spec_sim_tol)
        
        #calcuate scores
        scores = matchms.calculate_scores(
            ref_library,
            spectra,
            similarity_measure,
            )
        
        #adds annotation to feature dicts
        for i in range(len(spectra)):
            
            #sort matches after score, from high to low
            sorted_matches = scores.scores_by_query(spectra[i], sort=True)
            #filter out matches which do not reach user-set thresholds
            best_matches = [
                x for x in sorted_matches 
                if (
                    x[1]["score"] >= spec_sim_score_cutoff
                and 
                    x[1]["matches"] >= spec_sim_min_matched )
                ]
            
            if len(best_matches) >= 1: 
                
                #set annotation attribute to True
                feature_dicts[spectra[i].get('id')][
                    'cosine_annotation'] = True
                
                #adds reference library matches to feature object
                feature_dicts[spectra[i].get('id')][
                    'cosine_annotation_list'] = (
                        [{
                            'name' : x[0].metadata.get('compound_name') or "",
                            'smiles' : x[0].metadata.get('smiles') or "",
                            'inchi' : x[0].metadata.get('inchi') or "",
                            'score' : float(x[1]['score'].round(2)), 
                            'nr_matches' : int(x[1]['matches']), 
                        }
                        for x in best_matches]
                    )
        return feature_dicts
    else:
        return feature_dicts
