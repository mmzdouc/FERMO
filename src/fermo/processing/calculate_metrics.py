def calculate_feature_score(
    row, 
    feature_dicts,
    samples,
    sample,
    sample_stats,
    ):
    """Calculate points for each feature.
    
    Parameters
    ----------
    row : `pandas.core.frame.Series`
    feature_dicts : `dict`
        Feature_ID(keys):feature_dict(values)
    samples : `dict`
    sample : `str`
    sample_stats : `dict`
    """
    return {
        'rel_intensity_p' : float(row["norm_intensity"]),
        'convolutedness_p' : float(convolutedness(row, samples, sample)),
        'bioactivity_p' : float(bioactivity(row, feature_dicts)),
        'novelty_p' : float(novelty_new(row, feature_dicts, sample_stats)),
        'blank_ass' : in_blank(row, feature_dicts),
        }

def novelty_new(
    row, 
    feat_dicts, 
    sample_stats,
    ):
    '''Calculate novelty score
    
    Parameters
    ----------
    row : `pandas.core.frame.Series`
    feat_dicts : `dict`
    sample_stats : `dict`
    
    Returns
    -------
    `int` or `float`
    
    Notes
    -----
    Calculates 'consensus' novelty score from modified cosine 
    library search and ms2query results. 
    Attention: all scores are inverted (good annotation == low novelty
    score and vice versa
    Decision tree:
    if cosine and ms2query score is very high (>0.9), take the better score
    elif one of cosine or ms2query scores are very high (>0.9), take it
    elif 
        get cosine score if any
        get ms2query score if any
        get number of predicted classes for next neighbours of feature in
            similarity clique
        calculate average
    else return 1
    '''
    
    feat_ID = int(row["feature_ID"])
    cos_bool = feat_dicts[feat_ID]['cosine_annotation']
    ms2query_bool = feat_dicts[feat_ID]['ms2query']
    score_thrshld = 0.95
    
    if (cos_bool or ms2query_bool):
        
        #If cosine and ms2query scores very high, return higher score
        if (
            (
                cos_bool
                and
                feat_dicts[feat_ID]['cosine_annotation_list'][0
                    ]['score'] > score_thrshld
            )
            and
            (
                ms2query_bool
                and
                feat_dicts[feat_ID]['ms2query_results'][0
                    ]['ms2query_model_prediction'] > score_thrshld
            )
        ):
            if (
                feat_dicts[feat_ID]['cosine_annotation_list'][0]['score']
                >
                feat_dicts[feat_ID]['ms2query_results'][0
                    ]['ms2query_model_prediction']
            ):
                return (1 - feat_dicts[feat_ID]['cosine_annotation_list'][0
                    ]['score'])
            else:
                return (1 - feat_dicts[feat_ID]['ms2query_results'][0
                    ]['ms2query_model_prediction'])
                    
        #Elif high cosine score, return
        elif (
            cos_bool 
            and
            feat_dicts[feat_ID]['cosine_annotation_list'][0
                ]['score'] > score_thrshld
        ):
            return ( 1 - feat_dicts[feat_ID][
                'cosine_annotation_list'][0]['score'])
        
        #Elif high ms2query score, return
        elif (
            ms2query_bool
            and
            feat_dicts[feat_ID]['ms2query_results'][0
                ]['ms2query_model_prediction'] > score_thrshld
        ):
            return (1 - feat_dicts[feat_ID]['ms2query_results'][0
                ]['ms2query_model_prediction'])
        
        #Else calculate compound score
        else:
            cos_score = None
            if cos_bool:
                cos_score = feat_dicts[feat_ID]['cosine_annotation_list'][0
                    ]['score']
            
            ms2query_score = None
            if ms2query_bool:
                ms2query_score = feat_dicts[feat_ID]['ms2query_results'][0
                    ]['ms2query_model_prediction']
            
            #Calculate diversity of ms2query class annotation for 
            #nearest neighbours in spectral similarity network (should
            #be identical if related compounds). If many different, bad
            next_neigh_score = None
            if ms2query_bool:
                if feat_dicts[feat_ID]['similarity_clique']:
                    set_neighbours = set()
                    #get set of nearest neighbours (direct partners in mn)
                    for clique in sample_stats['cliques']:
                        if feat_ID in sample_stats['cliques'][clique][0]:
                            if len(sample_stats['cliques'][clique][0]) > 1:
                                for pair in sample_stats['cliques'][clique][1]:
                                    if feat_ID in pair:
                                        if feat_ID == pair[0]:
                                            set_neighbours.add(pair[1])
                                        else: 
                                            set_neighbours.add(pair[0])
                    set_neighbours.add(feat_ID)
                    
                    if len(set_neighbours) > 1:
                        set_npc_superclass_results = set()
                        set_cf_superclass = set()
                        for feature in set_neighbours:
                            set_npc_superclass_results.add(
                                feat_dicts[feat_ID]['ms2query_results'][0
                                    ]['npc_superclass_results']
                                )
                            set_cf_superclass.add(
                                feat_dicts[feat_ID]['ms2query_results'][0
                                    ]['cf_superclass']
                                )
                        
                        min_len = ""
                        if (
                            len(set_npc_superclass_results) 
                            <= 
                            len(set_cf_superclass)
                        ):
                            min_len = len(set_npc_superclass_results)
                        else:
                            min_len = len(set_cf_superclass)
                        
                        try:                    
                            next_neigh_score = (1 / min_len)
                        except:
                            next_neigh_score = None
            
            list_scores = [
                cos_score,
                ms2query_score,
                next_neigh_score
                ]
            
            counter = 0
            score = 0
            for i in range(len(list_scores)):
                if list_scores[i] is not None:
                    score = score + list_scores[i]
                    counter = counter + 1
            
            #Prevents division by zero
            if counter == 0:
                counter = 1 
            return (1 - (score / counter))
    else:
        return 1

def bioactivity(
    row, 
    feature_dicts,
    ):
    """Extracts bioactivity information."""
    
    if feature_dicts[int(row["feature_ID"])]['bioactivity_associated'] == True:
        bioactiv = feature_dicts[
            int(row["feature_ID"])]['bioactivity_samples']
        return max(bioactiv)
    else: 
        return 0

def in_blank(
    row,
    feature_dicts,
    ):
    """Extracts blank-associatedness information."""
    
    if feature_dicts[int(row["feature_ID"])]['blank_associated'] == True:
        return True
    else: 
        return False

def convolutedness(
    row, 
    samples, 
    sample,
    ):
    """Calculates convolutedness: how much % of peak remains. Legacy"""
    
    A_s = float(row["rt_start"])
    A_e = float(row["rt_stop"])
    #at beginning of calculation, A_rt_remainder and A_rt_full are equal
    A_rt_remainder = (A_e - A_s)
    A_rt_full = A_rt_remainder
    #if there is a collision, follow up on how much of peak is affected
    if row["feature_collision"] == True:
        X_s_left = []
        X_e_left = []
        X_s_right = []
        X_e_right = []
        X_s_middle = []
        X_e_middle = []
        X_s_covered = []
        X_e_covered = []
        
        #checks for each collision that was registered
        for collision in row["feature_collision_list"]:
            #assigns to variable to make equations easier to read
            entry = samples[sample].loc[
            samples[sample]["feature_ID"] == collision]
            X_s = float(entry["rt_start"])
            X_e = float(entry["rt_stop"])
            #collects data to create "consensus overlaps"
            #if peak X is overlapping A on the left
            if (A_s >= X_s) and (A_e > X_e):
                X_s_left.append(X_s)
                X_e_left.append(X_e)
            #if peak X is overlapping A on the right
            if (A_s < X_s) and (A_e <= X_e):
                X_s_right.append(X_s)
                X_e_right.append(X_e)
            #if peak X is inside peak A (covered)
            if (A_s < X_s) and (A_e > X_e):
                X_s_middle.append(X_s)
                X_e_middle.append(X_e)
            #if peak A is inside peak X or identical(covered)
            if (A_s >= X_s) and (A_e <= X_e):
                X_s_covered.append(X_s)
                X_e_covered.append(X_e)
        
        #determine how much of peak remains
        #left side: check if there were overlaps: if, newly assigns A_s
        if X_e_left:
            A_s = max(X_e_left)
        #right side: check if there were overlaps: ifm newly assigns A_e
        if X_s_right: 
            A_e = min(X_s_right)
        #check if there is any peak rt is left after this step
        if A_s >= A_e:
            A_rt_remainder = 0
            pass
        else:
            A_rt_remainder = (A_e - A_s)
        
        #check if any X inside A
        if X_s_middle and X_e_middle:
            #stretches over both sides of the now reduced peak
            if min(X_s_middle) <= A_s and max(X_e_middle) >= A_e:
                A_rt_remainder = 0
                pass
            #X streches over left side
            elif min(X_s_middle) <= A_s and max(X_e_middle) < A_e:
                A_s = max(X_e_middle)
                A_rt_remainder = (A_e - A_s)
            #X streches over right side
            elif min(X_s_middle) > A_s and max(X_e_middle) >= A_e:
                A_e = min(X_s_middle)
                A_rt_remainder = (A_e - A_s)
            #X still inside A
            elif min(X_s_middle) > A_s and max(X_e_middle) < A_e:
                range_middle = max(X_e_middle) - min(X_s_middle)
                A_rt_remainder = A_rt_remainder - range_middle

        #check if any A inside X:
        if X_s_covered:
            A_rt_remainder = 0
            pass
    
    #makes the remainder of the rt a fraction of orignial rt of peak
    try:
        return (1 - (A_rt_remainder / A_rt_full))
    except ZeroDivisionError:
        return 0


def calculate_metrics(
    samples,
    feature_dicts,
    sample_stats,
    ):
    """Calculate metrics for samples and score them:
    
    Parameters
    ----------
    samples : `samples`
        sample_names(keys):pandas.core.frame.DataFrame(values)
    feature_dicts : `dict`
        Feature_ID(keys):feature_dict(values)
    sample_stats : `dict`

    Returns
    -------
    samples : `dict`
        sample_names(keys):pandas.core.frame.DataFrame(values)
    feature_dicts : `dict`
    
    Notes
    -----
    Extracts sample-specific features
    Filters sample-specific features for topN features
    Calculates feature overlap per sample
    Detects bioactivity-associated features
    Detects blank-associated features
    ...
    Calculates scores for samples
    """

    ###CALCULATION SCORES

    sample_count = dict()
    #for each sample
    for sample in samples:
        #collect feature scores per sample
        feature_list = list()
        rel_intensity = list()
        convolutedness = list()
        bioactivity = list()
        novelty = list()
        diversity = list()
        blank_associatedness = list()
        ms1_only = list()
        
        #for each feature in sample
        for id, row in samples[sample].iterrows():
            feature_list.append(int(row["feature_ID"])) 
            
            #calculation of score per feature
            feature_scores = calculate_feature_score(
                row, 
                feature_dicts, 
                samples, 
                sample,
                sample_stats,
                )

            feature_dicts[int(row["feature_ID"])]['novelty_score'
                ] = round(feature_scores['novelty_p'],3)
            
            #appending to lists
            rel_intensity.append(feature_scores['rel_intensity_p'])
            convolutedness.append(feature_scores['convolutedness_p'])
            bioactivity.append(feature_scores['bioactivity_p'])
            novelty.append(feature_scores['novelty_p'])
            blank_associatedness.append(feature_scores['blank_ass'])
            
            #additional row to append info is ms2 available
            if feature_dicts[int(row["feature_ID"])]['ms2spectrum'] is None: 
                ms1_only.append(True)
            else:
                ms1_only.append(False)
                
        #appends lists to existing dataframe
        samples[sample]['rel_intensity_score'] = rel_intensity
        samples[sample]['convolutedness_score'] = convolutedness
        samples[sample]['bioactivity_score'] = bioactivity
        samples[sample]['novelty_score'] = novelty
        samples[sample]['in_blank'] = blank_associatedness
        samples[sample]['ms1_only'] = ms1_only
        
    return samples, feature_dicts

