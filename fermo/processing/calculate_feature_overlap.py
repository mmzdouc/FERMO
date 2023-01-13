from copy import deepcopy

def prepare_pandas_tables(
    samples,
    ):
    '''Prepare pandas tables for manipulation
    
    Parameters
    ----------
    samples : `dict`
    
    Returns
    -------
    samples_mod : `dict`
    
    Notes
    -----
    List comprehension to prevent broadcasted assignment 
    (see "stackoverflow.com/questions/38307489/
    set-list-as-value-in-a-column-of-a-pandas-dataframe")
    '''
    samples_mod = deepcopy(samples)
    
    for sample in samples_mod:
        samples_mod[sample]["feature_collision"] = False
        samples_mod[sample]["feature_collision_list"] = [
            [] for r in range(len(samples_mod[sample]))
            ]
        samples_mod[sample]["putative_adduct_detection"] = [
            [] for r in range(len(samples_mod[sample]))
            ]
    
    return samples_mod

def calc_mass_deviation(
    A, 
    B,
    ):
    """Calculates mass deviation in ppm between two precursor m/z:
    
    Parameters
    ----------
    A : `float`
    B : `float`
    
    Returns
    -------
    `float`
        
    Notes
    -----
    "Mass measurement error" taken from publication:
    doi.org/10.1016/j.jasms.2010.06.006 
    """
    return abs(((A - B) / B) * (10**6))

def add_mh_adduct_info(
    feature_dicts,
    samples_mod, 
    sample,
    adduct, 
    mh_ion,
    other_ion,
    ):
    """Append info on adducts
    
    Parameters
    ----------
    feature_dicts : `dict`
    samples_mod : `dict`
    sample : `str`
    adduct : `str`
    mh_ion : `int`
    other_ion : `int`

    Returns
    -------
    samples_mod : `dict`
    feature_dicts : `dict`
    
    Notes
    -----
    mh_ion stands for [M+H]+ (which is taken as reference)
    other_ion is the adduct relative to [M+H]+
    """
    mh_ion_ID = int(samples_mod[sample].at[mh_ion,'feature_ID'])
    other_ion_ID = int(samples_mod[sample].at[other_ion,'feature_ID'])
    
    mh_ion_str = f'ID {other_ion_ID}: {adduct} ({sample}) '
    other_ion_str = f'{adduct} (ID {mh_ion_ID}, {sample})'
    
    samples_mod[sample].at[mh_ion,"putative_adduct_detection"].append(mh_ion_str)
    samples_mod[sample].at[other_ion,"putative_adduct_detection"].append(other_ion_str)
    
    feature_dicts[mh_ion_ID]['ann_adduct_isotop'].append(mh_ion_str)
    feature_dicts[other_ion_ID]['ann_adduct_isotop'].append(other_ion_str)
    
    return samples_mod, feature_dicts

def add_dimer_dbl_info(
    feature_dicts,
    samples_mod, 
    sample,
    adduct, 
    mh_ion,
    other_ion,
    ):
    """Append info on dimer/double charged ion 
    
    Parameters
    ----------
    feature_dicts : `dict`
    samples_mod : `dict`
    sample : `str`
    adduct : `list`
    mh_ion : `int`
    other_ion : `int`
    
    Returns
    -------
    samples_mod : `dict`
    feature_dicts : `dict`
    
    Notes
    -----
    Consider two overlapping peaks A and B:
        -peak A with m/z 1648.47;
        -peak B with m/z 824.74.
    If A is assumed [M+H]+, B would be [M+2H]2+
    If B is assumed [M+H]+, A would be [2M+H]+
    Thus, assignment is performed for [M+2H]2+ and [2M+H]+ in parallel,
    since the the real condition cannot be determined without isotopic
    data.
    """
    mh_ion_ID = int(samples_mod[sample].at[mh_ion,'feature_ID'])
    other_ion_ID = int(samples_mod[sample].at[other_ion,'feature_ID'])
    
    mh_ion_str = f'{adduct[0]} (ID {other_ion_ID}, {sample})'
    other_ion_str = f'{adduct[1]} (ID {mh_ion_ID}, {sample})'
    
    samples_mod[sample].at[mh_ion,"putative_adduct_detection"].append(mh_ion_str)
    samples_mod[sample].at[other_ion,"putative_adduct_detection"].append(other_ion_str)

    feature_dicts[mh_ion_ID]['ann_adduct_isotop'].append(mh_ion_str)
    feature_dicts[other_ion_ID]['ann_adduct_isotop'].append(other_ion_str)

    return samples_mod, feature_dicts

def detect_sodium_adduct(
    mh_ion, 
    adduct, 
    strictness_ppm,
    ):
    '''Detect adduct
    
    Parameters
    ----------
    mh_ion : `float`
    adduct : `float`
    strictness_ppm : `int`
    
    Returns
    -------
    `bool`
    '''
    Na = 22.989218
    H = 1.007276
    
    if (calc_mass_deviation(
        (mh_ion - H + Na), adduct) < strictness_ppm
    ):
        return True
    else:
        return False

def detect_dimer_sodium_adduct(
    mh_ion, 
    adduct, 
    strictness_ppm,
    ):
    '''Detect and append adduct information
    
    Parameters
    ----------
    mh_ion : `float`
    adduct : `float`
    strictness_ppm : `int`
    
    Returns
    -------
    `bool`
    '''
    Na = 22.989218
    H = 1.007276
    
    if (calc_mass_deviation(
        ((2 * (mh_ion - H)) + Na), adduct) < strictness_ppm
    ):
        return True
    else:
        return False
    
def detect_trimer_adduct(
    mh_ion, 
    adduct, 
    strictness_ppm,
    ):
    '''Detect and append adduct information
    
    Parameters
    ----------
    mh_ion : `float`
    adduct : `float`
    strictness_ppm : `int`
    
    Returns
    -------
    `bool`
    '''
    H = 1.007276
    
    if (calc_mass_deviation(
        ((mh_ion + (2 * H))/3), adduct) < strictness_ppm
    ):
        return True
    else:
        return False
    
def detect_frst_isot_adduct(
    mh_ion, 
    adduct, 
    strictness_ppm,
    ):
    '''Detect and append adduct information
    
    Parameters
    ----------
    mh_ion : `float`
    adduct : `float`
    strictness_ppm : `int`
    
    Returns
    -------
    `bool`
    '''
    C13_12 = 1.0033548 #difference between 13C and 12C isotopes 
    
    if (calc_mass_deviation(
        (mh_ion + C13_12), adduct) < strictness_ppm
    ):
        return True
    else:
        return False
    
def detect_scnd_isot_adduct(
    mh_ion, 
    adduct, 
    strictness_ppm,
    ):
    '''Detect and append adduct information
    
    Parameters
    ----------
    mh_ion : `float`
    adduct : `float`
    strictness_ppm : `int`
    
    Returns
    -------
    `bool`
    '''
    C13_12 = 1.0033548 #difference between 13C and 12C isotopes 
    
    if (calc_mass_deviation(
        (mh_ion + (2 * C13_12)), adduct) < strictness_ppm
    ):
        return True
    else:
        return False
    
def detect_thrd_isot_adduct(
    mh_ion, 
    adduct, 
    strictness_ppm,
    ):
    '''Detect and append adduct information
    
    Parameters
    ----------
    mh_ion : `float`
    adduct : `float`
    strictness_ppm : `int`
    
    Returns
    -------
    `bool`
    '''
    C13_12 = 1.0033548 #difference between 13C and 12C isotopes 
    
    if (calc_mass_deviation(
        (mh_ion + (3 * C13_12)), adduct) < strictness_ppm
    ):
        return True
    else:
        return False
    
def detect_fourth_isot_adduct(
    mh_ion, 
    adduct, 
    strictness_ppm,
    ):
    '''Detect and append adduct information
    
    Parameters
    ----------
    mh_ion : `float`
    adduct : `float`
    strictness_ppm : `int`
    
    Returns
    -------
    `bool`
    '''
    C13_12 = 1.0033548 #difference between 13C and 12C isotopes 
    
    if (calc_mass_deviation(
        (mh_ion + (4 * C13_12)), adduct) < strictness_ppm
    ):
        return True
    else:
        return False
    
def detect_fifth_isot_adduct(
    mh_ion, 
    adduct, 
    strictness_ppm,
    ):
    '''Detect and append adduct information
    
    Parameters
    ----------
    mh_ion : `float`
    adduct : `float`
    strictness_ppm : `int`
    
    Returns
    -------
    `bool`
    '''
    C13_12 = 1.0033548 #difference between 13C and 12C isotopes 
    
    if (calc_mass_deviation(
        (mh_ion + (5 * C13_12)), adduct) < strictness_ppm
    ):
        return True
    else:
        return False
    
def detect_double_first_isot_adduct(
    mh_ion, 
    adduct, 
    strictness_ppm,
    ):
    '''Detect and append adduct information
    
    Parameters
    ----------
    mh_ion : `float`
    adduct : `float`
    strictness_ppm : `int`
    
    Returns
    -------
    `bool`
    
    Notes
    -----
    #double charged +1 isotopic peak, addition of 1 neutron and 1 proton
    
    '''
    C13_12 = 1.0033548 #difference between 13C and 12C isotopes
    H = 1.007276
    
    if (calc_mass_deviation(
        ((mh_ion + (C13_12 + H)) / 2), adduct) < strictness_ppm
    ):
        return True
    else:
        return False
    
def detect_double_second_isot_adduct(
    mh_ion, 
    adduct, 
    strictness_ppm,
    ):
    '''Detect and append adduct information
    
    Parameters
    ----------
    mh_ion : `float`
    adduct : `float`
    strictness_ppm : `int`
    
    Returns
    -------
    `bool`
    
    Notes
    -----
    #double charged +2 isotopic peak, addition of 2 neutron and 1 proton
    
    '''
    C13_12 = 1.0033548 #difference between 13C and 12C isotopes
    H = 1.007276
    
    if (calc_mass_deviation(
        ((mh_ion + ((2 * C13_12) + H)) / 2), adduct) < strictness_ppm
    ):
        return True
    else:
        return False
    
def detect_double_third_isot_adduct(
    mh_ion, 
    adduct, 
    strictness_ppm,
    ):
    '''Detect and append adduct information
    
    Parameters
    ----------
    mh_ion : `float`
    adduct : `float`
    strictness_ppm : `int`
    
    Returns
    -------
    `bool`
    
    Notes
    -----
    #double charged +3 isotopic peak, addition of 3 neutron and 1 proton
    
    '''
    C13_12 = 1.0033548 #difference between 13C and 12C isotopes
    H = 1.007276
    
    if (calc_mass_deviation(
        ((mh_ion + ((3 * C13_12) + H)) / 2), adduct) < strictness_ppm
    ):
        return True
    else:
        return False
    
def detect_double_fourth_isot_adduct(
    mh_ion, 
    adduct, 
    strictness_ppm,
    ):
    '''Detect and append adduct information
    
    Parameters
    ----------
    mh_ion : `float`
    adduct : `float`
    strictness_ppm : `int`
    
    Returns
    -------
    `bool`
    
    Notes
    -----
    #double charged +4 isotopic peak, addition of 4 neutron and 1 proton
    
    '''
    C13_12 = 1.0033548 #difference between 13C and 12C isotopes
    H = 1.007276
    
    if (calc_mass_deviation(
        ((mh_ion + ((4 * C13_12) + H)) / 2), adduct) < strictness_ppm
    ):
        return True
    else:
        return False
    
def detect_double_fifth_isot_adduct(
    mh_ion, 
    adduct, 
    strictness_ppm,
    ):
    '''Detect and append adduct information
    
    Parameters
    ----------
    mh_ion : `float`
    adduct : `float`
    strictness_ppm : `int`
    
    Returns
    -------
    `bool`
    
    Notes
    -----
    #double charged +5 isotopic peak, addition of 5 neutron and 1 proton
    
    '''
    C13_12 = 1.0033548 #difference between 13C and 12C isotopes
    H = 1.007276
    
    if (calc_mass_deviation(
        ((mh_ion + ((5 * C13_12) + H)) / 2), adduct) < strictness_ppm
    ):
        return True
    else:
        return False
    
def detect_first_isot_double_adduct(
    mh_ion, 
    adduct, 
    strictness_ppm,
    ):
    '''Detect and append adduct information
    
    Parameters
    ----------
    mh_ion : `float`
    adduct : `float`
    strictness_ppm : `int`
    
    Returns
    -------
    `bool`
    
    Notes
    -----
    #+1 isotopic peak of a double protonated ion: [M+2H] vs [M+1+2H]
    '''
    C13_12 = 1.0033548 #difference between 13C and 12C isotopes
    
    if (calc_mass_deviation(
        (mh_ion + (C13_12/2)), adduct) < strictness_ppm
    ):
        return True
    else:
        return False
    
def detect_iron_adduct(
    mh_ion, 
    adduct, 
    strictness_ppm,
    ):
    '''Detect and append adduct information
    
    Parameters
    ----------
    mh_ion : `float`
    adduct : `float`
    strictness_ppm : `int`
    
    Returns
    -------
    `bool`
    
    Notes
    -----
    #56^Fe adduct
    '''
    H = 1.007276
    Fe56 = 55.934940
    
    if (calc_mass_deviation(
        (mh_ion - (3 * H) + Fe56), adduct) < strictness_ppm
    ):
        return True
    else:
        return False
    
def detect_dimer_dbl(
    mh_ion, 
    adduct, 
    strictness_ppm,
    ):
    '''Detect and append adduct information
    
    Parameters
    ----------
    mh_ion : `float`
    adduct : `float`
    strictness_ppm : `int`
    
    Returns
    -------
    `bool`
    
    Notes
    -----
    #M+2H and 2M+H
    '''
    H = 1.007276
    
    if (calc_mass_deviation(
        ((mh_ion + H)/2), adduct) < strictness_ppm
    ):
        return True
    else:
        return False

def calculate_feature_overlap(
    samples,
    strictness_ppm,
    feature_dicts,
    ):
    '''Detect peak overlaps and differentiate adducts or compounds
    
    Parameters
    ----------
    samples : `dict`
    strictness_ppm : `float`
    feature_dicts : `dict`
    
    Returns
    -------
    samples_mod : `dict`
    feature_dicts : `dict`
    
    Notes
    -----
    Calculates overlap of features (peaks) by simplifying them to
    one-dimensional vectors. Consider two peaks A and B with A(x1,x2)
    and B(x1,x2), where x is a retention time. If any True in
    Ax2 < Bx1 or Bx2 < Ax1, peaks do not overlap.
    
    For overlapping features:
    Several conditions are possible in which features are not registered
    to be colliding even though their retention time windows overlap:
    
        -isotopic peaks: 
            natural isotope distributions can lead to different
            isotopic peaks. In organic compounds, isotopic 
            peaks resulting from 13C atoms are most commonly
            observed, and are shifted 1.00336 mass units.
            Feature collisions between isotopic peaks and
            monoisotopic peaks can be ignored, since they 
            originate from the same analyte.
        -adducts: 
            in mass spectrometry analysis, different ions for the 
            same analyte are commonly observed (e.g. [M+H]+, [Na+H]+,
            [M+2H]2+). Since the [M+H]+ ion is the most common one
            in ESI,[1] all other adducts can be considered 
            artefacts. Feature collisions of such adducts 
            originating from the same analyte can therefore be 
            ignored (not present as compounds in sample). 
    
    If any adduct pair matches, annotation is written and the loop exited
    since there is only one possible adduct identity. Such matches are 
    not registered as overlaps.
    
    [1]: doi.org/10.1021/acs.jcim.1c00579 
    
    monoisotopic masses taken from:    
    - https://fiehnlab.ucdavis.edu/staff/kind/Metabolomics/MS-Adduct-Calculator/
    - http://www.chemspider.com/Chemical-Structure.22368.html
    '''
    samples_mod = prepare_pandas_tables(samples)
    
    for sample in samples_mod:
        for A in range(len(samples_mod[sample])): 
            for B in range(A+1, len(samples_mod[sample])):
                A_left = samples_mod[sample]["rt_start"][A]
                A_right = samples_mod[sample]["rt_stop"][A]
                B_left = samples_mod[sample]["rt_start"][B]
                B_right = samples_mod[sample]["rt_stop"][B]
                A_mz = samples_mod[sample]["precursor_mz"][A]
                B_mz = samples_mod[sample]["precursor_mz"][B]
                
                if not (A_right < B_left or B_right < A_left):
                    
                    if detect_sodium_adduct(A_mz, B_mz, strictness_ppm,):
                        samples_mod, feature_dicts = add_mh_adduct_info(
                            feature_dicts,
                            samples_mod,
                            sample,
                            "[M+Na]+",
                            A,
                            B,
                            )
                        continue
                    
                    elif detect_sodium_adduct(B_mz, A_mz, strictness_ppm,):
                        samples_mod, feature_dicts = add_mh_adduct_info(
                            feature_dicts,
                            samples_mod,
                            sample,
                            "[M+Na]+",
                            B,
                            A,
                            )
                        continue
                    
                    elif detect_dimer_sodium_adduct(A_mz, B_mz, strictness_ppm,):
                        samples_mod, feature_dicts = add_mh_adduct_info(
                            feature_dicts,
                            samples_mod,
                            sample,
                            "[2M+Na]+",
                            A,
                            B,
                            )
                        continue
                    
                    elif detect_dimer_sodium_adduct(B_mz, A_mz, strictness_ppm,):
                        samples_mod, feature_dicts = add_mh_adduct_info(
                            feature_dicts,
                            samples_mod,
                            sample,
                            "[2M+Na]+",
                            B,
                            A,
                            )
                        continue
                    
                    elif detect_trimer_adduct(A_mz, B_mz, strictness_ppm,):
                        samples_mod, feature_dicts = add_mh_adduct_info(
                            feature_dicts,
                            samples_mod,
                            sample,
                            "[M+3H]3+",
                            A,
                            B,
                            )
                        continue
                    
                    elif detect_trimer_adduct(B_mz, A_mz, strictness_ppm,):
                        samples_mod, feature_dicts = add_mh_adduct_info(
                            feature_dicts,
                            samples_mod,
                            sample,
                            "[M+3H]3+",
                            B,
                            A,
                            )
                        continue
                    
                    elif detect_frst_isot_adduct(A_mz, B_mz, strictness_ppm,):
                        samples_mod, feature_dicts = add_mh_adduct_info(
                            feature_dicts,
                            samples_mod,
                            sample,
                            "[M+1+H]+",
                            A,
                            B,
                            )
                        continue
                    
                    elif detect_frst_isot_adduct(B_mz, A_mz, strictness_ppm,):
                        samples_mod, feature_dicts = add_mh_adduct_info(
                            feature_dicts,
                            samples_mod,
                            sample,
                            "[M+1+H]+",
                            B,
                            A,
                            )
                        continue
                    
                    elif detect_scnd_isot_adduct(A_mz, B_mz, strictness_ppm,):
                        samples_mod, feature_dicts = add_mh_adduct_info(
                            feature_dicts,
                            samples_mod,
                            sample,
                            "[M+2+H]+",
                            A,
                            B,
                            )
                        continue
                    
                    elif detect_scnd_isot_adduct(B_mz, A_mz, strictness_ppm,):
                        samples_mod, feature_dicts = add_mh_adduct_info(
                            feature_dicts,
                            samples_mod,
                            sample,
                            "[M+2+H]+",
                            B,
                            A,
                            )
                        continue
                    
                    elif detect_thrd_isot_adduct(A_mz, B_mz, strictness_ppm,):
                        samples_mod, feature_dicts = add_mh_adduct_info(
                            feature_dicts,
                            samples_mod,
                            sample,
                            "[M+3+H]+",
                            A,
                            B,
                            )
                        continue
                    
                    elif detect_thrd_isot_adduct(B_mz, A_mz, strictness_ppm,):
                        samples_mod, feature_dicts = add_mh_adduct_info(
                            feature_dicts,
                            samples_mod,
                            sample,
                            "[M+3+H]+",
                            B,
                            A,
                            )
                        continue
                    
                    elif detect_fourth_isot_adduct(A_mz, B_mz, strictness_ppm,):
                        samples_mod, feature_dicts = add_mh_adduct_info(
                            feature_dicts,
                            samples_mod,
                            sample,
                            "[M+4+H]+",
                            A,
                            B,
                            )
                        continue
                    
                    elif detect_fourth_isot_adduct(B_mz, A_mz, strictness_ppm,):
                        samples_mod, feature_dicts = add_mh_adduct_info(
                            feature_dicts,
                            samples_mod,
                            sample,
                            "[M+4+H]+",
                            B,
                            A,
                            )
                        continue
                    
                    elif detect_fourth_isot_adduct(A_mz, B_mz, strictness_ppm,):
                        samples_mod, feature_dicts = add_mh_adduct_info(
                            feature_dicts,
                            samples_mod,
                            sample,
                            "[M+5+H]+",
                            A,
                            B,
                            )
                        continue
                    
                    elif detect_fourth_isot_adduct(B_mz, A_mz, strictness_ppm,):
                        samples_mod, feature_dicts = add_mh_adduct_info(
                            feature_dicts,
                            samples_mod,
                            sample,
                            "[M+5+H]+",
                            B,
                            A,
                            )
                        continue
                    
                    elif detect_double_first_isot_adduct(A_mz, B_mz, strictness_ppm,):
                        samples_mod, feature_dicts = add_mh_adduct_info(
                            feature_dicts,
                            samples_mod,
                            sample,
                            "[M+1+2H]2+",
                            A,
                            B,
                            )
                        continue
                    
                    elif detect_double_first_isot_adduct(B_mz, A_mz, strictness_ppm,):
                        samples_mod, feature_dicts = add_mh_adduct_info(
                            feature_dicts,
                            samples_mod,
                            sample,
                            "[M+1+2H]2+",
                            B,
                            A,
                            )
                        continue
                    
                    elif detect_double_second_isot_adduct(A_mz, B_mz, strictness_ppm,):
                        samples_mod, feature_dicts = add_mh_adduct_info(
                            feature_dicts,
                            samples_mod,
                            sample,
                            "[M+2+2H]2+",
                            A,
                            B,
                            )
                        continue
                    
                    elif detect_double_second_isot_adduct(B_mz, A_mz, strictness_ppm,):
                        samples_mod, feature_dicts = add_mh_adduct_info(
                            feature_dicts,
                            samples_mod,
                            sample,
                            "[M+2+2H]2+",
                            B,
                            A,
                            )
                        continue
                    
                    elif detect_double_third_isot_adduct(A_mz, B_mz, strictness_ppm,):
                        samples_mod, feature_dicts = add_mh_adduct_info(
                            feature_dicts,
                            samples_mod,
                            sample,
                            "[M+3+2H]2+",
                            A,
                            B,
                            )
                        continue
                    
                    elif detect_double_third_isot_adduct(B_mz, A_mz, strictness_ppm,):
                        samples_mod, feature_dicts = add_mh_adduct_info(
                            feature_dicts,
                            samples_mod,
                            sample,
                            "[M+3+2H]2+",
                            B,
                            A,
                            )
                        continue
                    
                    elif detect_double_fourth_isot_adduct(A_mz, B_mz, strictness_ppm,):
                        samples_mod, feature_dicts = add_mh_adduct_info(
                            feature_dicts,
                            samples_mod,
                            sample,
                            "[M+4+2H]2+",
                            A,
                            B,
                            )
                        continue
                    
                    elif detect_double_fourth_isot_adduct(B_mz, A_mz, strictness_ppm,):
                        samples_mod, feature_dicts = add_mh_adduct_info(
                            feature_dicts,
                            samples_mod,
                            sample,
                            "[M+4+2H]2+",
                            B,
                            A,
                            )
                        continue
                    
                    elif detect_double_fifth_isot_adduct(A_mz, B_mz, strictness_ppm,):
                        samples_mod, feature_dicts = add_mh_adduct_info(
                            feature_dicts,
                            samples_mod,
                            sample,
                            "[M+5+2H]2+",
                            A,
                            B,
                            )
                        continue
                    
                    elif detect_double_fifth_isot_adduct(B_mz, A_mz, strictness_ppm,):
                        samples_mod, feature_dicts = add_mh_adduct_info(
                            feature_dicts,
                            samples_mod,
                            sample,
                            "[M+5+2H]2+",
                            B,
                            A,
                            )
                        continue
                    
                    elif detect_first_isot_double_adduct(A_mz, B_mz, strictness_ppm,):
                        samples_mod, feature_dicts = add_mh_adduct_info(
                            feature_dicts,
                            samples_mod,
                            sample,
                            "+1 isotopic peak of [M+2H]2+",
                            A,
                            B,
                            )
                        continue
                    
                    elif detect_first_isot_double_adduct(B_mz, A_mz, strictness_ppm,):
                        samples_mod, feature_dicts = add_mh_adduct_info(
                            feature_dicts,
                            samples_mod,
                            sample,
                            "+1 isotopic peak of [M+2H]2+",
                            B,
                            A,
                            )
                        continue
                    
                    elif detect_iron_adduct(A_mz, B_mz, strictness_ppm,):
                        samples_mod, feature_dicts = add_mh_adduct_info(
                            feature_dicts,
                            samples_mod,
                            sample,
                            "[M+56Fe-2H]+",
                            A,
                            B,
                            )
                        continue
                    
                    elif detect_iron_adduct(B_mz, A_mz, strictness_ppm,):
                        samples_mod, feature_dicts = add_mh_adduct_info(
                            feature_dicts,
                            samples_mod,
                            sample,
                            "[M+56Fe-2H]+",
                            B,
                            A,
                            )
                        continue
                    
                    elif detect_dimer_dbl(A_mz, B_mz, strictness_ppm,):
                        samples_mod, feature_dicts = add_dimer_dbl_info(
                            feature_dicts,
                            samples_mod,
                            sample,
                            ["[2M+H]+", "[M+2H]2+",],
                            A,
                            B,
                            )
                        continue
                    
                    elif detect_dimer_dbl(B_mz, A_mz, strictness_ppm,):
                        samples_mod, feature_dicts = add_dimer_dbl_info(
                            feature_dicts,
                            samples_mod,
                            sample,
                            ["[2M+H]+", "[M+2H]2+",],
                            B,
                            A,
                            )
                        continue

                    #additional adducts: add here

                    else:
                        #Peak collision registered: not adduct overlap
                        samples_mod[sample].at[A,"feature_collision"] = True
                        samples_mod[sample].at[B,"feature_collision"] = True
                        samples_mod[sample].at[A,
                            "feature_collision_list"].append(
                                samples_mod[sample]["feature_ID"][B])
                        samples_mod[sample].at[B,
                            "feature_collision_list"].append(
                                samples_mod[sample]["feature_ID"][A])
    
    return samples_mod, feature_dicts
