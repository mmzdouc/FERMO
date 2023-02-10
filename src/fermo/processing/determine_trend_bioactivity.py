def determine_trend_bioactivity(
    feature_dicts,
    sample_stats,
    ):
    '''Determine correlation of feature intensity vs bioactivity
    
    Parameters
    ----------
    feature_dicts : `dict`
    sample_stats : `dict`
    
    Returns
    ------
    feature_dicts : `dict`
    
    Note
    ----
    test for downward trend of bioactivity across samples 
    (already sorted after intensity of feature across samples)
    '''
    for ID in feature_dicts:
        if feature_dicts[int(ID)]['bioactivity_associated'] == True:
                bioactiv = feature_dicts[int(ID)]['bioactivity_samples']
                
                counter = 0
                list_trend = []
                
                for i in range(len(bioactiv)):
                    if i == 0:
                        list_trend.append(True)
                    else:
                        if bioactiv[counter] >= bioactiv[i]:
                            list_trend.append(True)
                        else:
                            list_trend.append(False)
                        counter = counter + 1
                
                if (not False in list_trend):
                    feature_dicts[int(ID)]['bioactivity_trend'] = True
    
    return feature_dicts
