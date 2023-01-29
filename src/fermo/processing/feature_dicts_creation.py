import pandas as pd
import matchms

def extract_from_peaktable(
    row,
    ):
    """Creates sorted pandas df with sample info for each feature
    
    Parameters
    ----------
    row : `pandas.core.series.Series`
    
    Returns
    -------
    samples_intensities : `pandas.core.series.DataFrame`
    """ 
    samples_presence = []
    samples_intens = []
    samples_fwhm = []
    samples_rt = []
    
    #extract sample names in which feature was detected
    for label in row[row=="DETECTED"].index:
        samples_presence.append(label.split(":")[1])

    for sample in samples_presence:
        samples_intens.append(float(
            row["".join(["datafile:", sample, ":intensity_range:max"])]))
        samples_fwhm.append(float(
            row["".join(["datafile:", sample, ":fwhm"])]))
        samples_rt.append(float(
            row["".join(["datafile:", sample, ":rt"])]))

    #constructs dataframe to return values
    sample_specific_data = pd.DataFrame({
        "presence" : samples_presence,
        "intens" : samples_intens,
        "fwhm" : samples_fwhm,
        "rt" : samples_rt,
        })
    
    #sort data after intensity and reset index
    sample_specific_data.sort_values(
        by=["intens",], 
        inplace=True, 
        ascending=[False,]
        )
    sample_specific_data.reset_index(drop=True, inplace=True)
    
    return sample_specific_data


def calc_fold_diff(
    set_groups,
    list_presence,
    samples_intens,
    sample_stats,
    ):
    '''Calculate fold differences between groups
    
    Parameters
    ----------
    set_groups : `set`
        Set of groups associated to feature
    list_presence : `list`
        List of samples feature was detected in
    samples_intens : `dict`
        Dict of samples : intensity (associated to feature)
    sample_stats : `dict`
        Info on samples
        
    Returns
    -------
    dict_fold_diff : `dict`
        group1/group2 : fold-diff
    sorted_fold_diff : `list`
        sorted list of fold difference keys
        
    Parameters
    ----------
    For each group associated to feature, intensities detected over 
    samples are extracted and appended to a list. The maximum value 
    from each of these lists is used to calculate the fold-difference
    between groups, in a pairwise fashion. 
    The results are stored in dict_fold_diff, and sorted_fold_diff 
    holds the keys of dict_fold_diff, sorted after maximum intensity.
    '''

    dict_group_int = dict()
    dict_fold_diff = dict()
    sorted_fold_diff = []
    #fold diff makes only sense if 2 or more groups
    if len(set_groups) > 1:
        for group in set_groups:
            dict_group_int[group] = []

        for sample in list_presence:
            dict_group_int[sample_stats['samples_dict'][sample]].append(
            samples_intens[sample])
        
        #pairwise comparison of group combinations
        list_keys_group = list(dict_group_int.keys())
        for A in range(len(list_keys_group)): 
            for B in range(A+1, len(list_keys_group)):
                dict_fold_diff[
                    "".join([
                        list_keys_group[A],
                        '/',
                        list_keys_group[B],
                    ])] = round(
                    (max(dict_group_int[list_keys_group[A]])
                    /
                    max(dict_group_int[list_keys_group[B]])
                    ), 2
                    )
                dict_fold_diff[
                    "".join([
                        list_keys_group[B],
                        '/',
                        list_keys_group[A],
                    ])] = round(
                    (max(dict_group_int[list_keys_group[B]])
                    /
                    max(dict_group_int[list_keys_group[A]])
                    ), 2
                    )
        #sort after highest fold difference
        sorted_fold_diff.extend(sorted(
            dict_fold_diff,
            key=dict_fold_diff.get,
            reverse=True,))
        
        return dict_fold_diff, sorted_fold_diff
    else: 
        return None, []

        
        
def create_ms2_object(
    ms2_frag, 
    ms2_int, 
    precursor_mz,
    feature_ID,
    min_ms2_peaks,
    ):
    '''Helper function to create matchms.Spectrum objects
    
    Parameters
    ----------
    ms2_frag : `list`
    ms2_int : `list`
    precursor_mz : `float`
    feature_ID : `int`
    min_ms2_peaks : `int`
    
    Returns
    -------
    spectrum : `matchms.Spectrum.object` or `None`
    
    Notes
    -----
    Apart from creating matchms objects, function also fulfils a 
    filtering task: only fragmentation pattern with a minimum number
    of ions (e.g., 8, user-specified) are considered
    further. This removes low quality spectra.
    '''
    if (ms2_frag is None) or (len(ms2_frag) < min_ms2_peaks):
        return None
    else:
        spectrum = matchms.Spectrum(
            mz=ms2_frag,
            intensities=ms2_int,
            metadata={
                'precursor_mz': precursor_mz,
                'id': feature_ID,
                }
            )
        spectrum = matchms.filtering.add_precursor_mz(spectrum)
        spectrum = matchms.filtering.normalize_intensities(spectrum)
        spectrum = matchms.filtering.select_by_intensity(
            spectrum, 
            intensity_from=0.01
            )
        return spectrum

def feature_dicts_creation(
    peaktable, 
    ms2spectra,
    min_ms2_peaks,
    sample_stats,
    detected_features,
    ):
    """Scrape data, create feature dicts, store in dict.
    
    Parameters
    ----------
    peaktable : `pandas.core.frame.DataFrame`
    ms2spectra : `dict`
        Feature_ID(keys):[fragments,intensities](values)
    min_ms2_peaks : `int`
        Quality control parameter. MS2 spectra <= nr peaks are discarded
    sample_stats : `dict`
    detected_features : `set`
        Set of all features detected in samples; used to filter out
        features if an intensity threshold was set
    
    Returns
    -------
    feature_dicts : `dict`
        Feature_ID(keys):feature_dict(dict)
    """
    feature_dicts = dict()
    
    for id, row in peaktable.iterrows():
        if int(row["feature_ID"]) not in detected_features:
            pass
        else:
            #returns a pandas dataframe sorted after intensity
            df_samples = extract_from_peaktable(row)
            
            #Df easier to sort than lists
            list_presence = df_samples.loc[:,'presence'].to_list()
            list_intens = df_samples.loc[:,'intens'].to_list()
            list_rt = df_samples.loc[:,'rt'].to_list()
            fwhm = df_samples.loc[:,'fwhm'].to_list()
            
            #construct dict from lists
            samples_fwhm = dict(zip(list_presence, fwhm))
            samples_rt = dict(zip(list_presence, list_rt))
            samples_intens = dict(zip(list_presence, list_intens))
            
            #retrieve groups 
            set_groups = set()
            for sample in list_presence:
                set_groups.add(sample_stats['samples_dict'][sample])
            
            #calculate fold differences between groups
            dict_fold_diff, sorted_fold_diff = calc_fold_diff(
                set_groups,
                list_presence,
                samples_intens,
                sample_stats
                )
            
            #retrieve MS2 spectra per feature
            try:
                ms2_frag = ms2spectra[int(row["feature_ID"])][0]
                ms2_int = ms2spectra[int(row["feature_ID"])][1]
            except KeyError:
                ms2_frag = None
                ms2_int = None
            
            ms2spectrum = create_ms2_object(
                ms2_frag,
                ms2_int,
                float(row["precursor_mz"]),
                int(row["feature_ID"]),
                int(min_ms2_peaks,))
            
            ms1_bool = False
            if ms2spectrum is None:
                ms1_bool = True
            
            #Dict assignment
            feature_dicts[int(row["feature_ID"])] = {
                'feature_ID' : int(row["feature_ID"]),
                'precursor_mz' : float(row["precursor_mz"]),
                'average_retention_time' : float(row["retention_time"]),
                'rt_in_samples' : samples_rt,
                'presence_samples' : list_presence,
                'intensities_samples' : list_intens,
                'median_fwhm' : round(df_samples.loc[:,'fwhm'].median(), 2),
                'fwhm_samples' : samples_fwhm,
                'feature_max_int' : list_intens[0],
                'ms2spectrum' : ms2spectrum,
                'ms1_bool' : ms1_bool,
                #Dummy values - assigned downstream
                'bioactivity_associated' : False,
                'bioactivity_trend' : False,
                'bioactivity_samples' : [],
                'blank_associated' : False,
                'similarity_clique' : False,
                'similarity_clique_number' : "",
                'similarity_clique_list' : [],
                'cosine_annotation' : False,
                'cosine_annotation_list' : [],
                'ms2query' : False,
                'ms2query_results' : '',
                'novelty_score' : '',
                'set_groups' : set_groups,
                'set_groups_clique' : set(),
                'dict_fold_diff' : dict_fold_diff,
                'sorted_fold_diff' : sorted_fold_diff,
                'ann_adduct_isotop': [],
                }
    
    return feature_dicts
