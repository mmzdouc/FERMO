import pandas as pd

def calculate_feature_overlap(samples, strictness_ppm, feature_dicts):
    """Detects feature collision (overlap of peaks) based on retent time.
    
    Parameters
    ----------
    samples : `dict`
        dict of pandas dataframes of sample-specific features, with
        key=sample_name : value=pandas.df
    strictness_ppm : `float`
        Tolerable mass deviation in ppm. Allows to tweak precision of
        matching. Should be matched to precision of instrument. E.g.
        20 ppm is still tolerable
    feature_dicts : `dict`
        Contains feature 'objects
    
    Returns
    -------
    returned_samples : `dict`
        dict of pandas dataframes of sample-specific features, with
        key=sample_name : value=pandas.df
    
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
                
    [1]: doi.org/10.1021/acs.jcim.1c00579 
    
    Practical notes:
    
    To add new adduct types:
    1) add elif conditions to main function (double loop)
    2) in function "detect_adducts", add calculations (define the kind
    of adduct respective to the [M+H]+
    3) add test case to tests/test_calculate_feature_overlap
    """
    
    
    returned_samples  = dict()
    
    for sample in samples:
        #Column "feature_collision": most peaks won't overlap
        samples[sample]["feature_collision"] = False
        
        #List comprehension to prevent broadcasted assignment.
        #For details, see "stackoverflow.com/questions/38307489/
        #set-list-as-value-in-a-column-of-a-pandas-dataframe"
        samples[sample]["feature_collision_list"] = [
            [] for r in range(len(samples[sample]))]
        samples[sample]["putative_adduct_detection"] = [
            [] for r in range(len(samples[sample]))]        
        
        #make all against all comparison of contained features
        for A in range(len(samples[sample])): 
            for B in range(A+1, len(samples[sample])):
                #readability
                A_left = samples[sample]["rt_start"][A]
                A_right = samples[sample]["rt_stop"][A]
                B_left = samples[sample]["rt_start"][B]
                B_right = samples[sample]["rt_stop"][B]
                A_mz = samples[sample]["precursor_mz"][A]
                B_mz = samples[sample]["precursor_mz"][B]
                
                #If any True, peaks A and B do not overlap.
                #For readability, "not" is prefixed to that true if 
                #peaks DO overlap.
                if not (A_right < B_left or B_right < A_left):

                    #If True, putative adduct was found - no collision
                    #"Walrus operator" := to use one function call 
                    #for condictional and for variable assignment
                    if True in (adduct := detect_adducts(
                    A_mz, B_mz, strictness_ppm)):
                        
                        #sodium
                        if "[M+Na]+" in adduct:
                            if A_mz > B_mz:
                                app_addct_inf(samples,sample,adduct,A,B,
                                feature_dicts)
                            else:
                                app_addct_inf(samples,sample,adduct,B,A,
                                feature_dicts)
                        
                        #dimer plus sodium
                        elif "[2M+Na]+" in adduct:
                            if A_mz > B_mz:
                                app_addct_inf(samples,sample,adduct,A,B,
                                feature_dicts)
                            else:
                                app_addct_inf(samples,sample,adduct,B,A,
                                feature_dicts)
                        
                        #double proton (see app_dimer_dbl() for details)
                        elif "[M+2H]2+" in adduct:
                            if A_mz < B_mz:
                                app_dimer_dbl(samples,sample,adduct,A,B,
                                feature_dicts)
                            else:
                                app_dimer_dbl(samples,sample,adduct,B,A,
                                feature_dicts)
                                    
                        #triple proton
                        elif "[M+3H]3+" in adduct:
                            if A_mz > B_mz:
                                app_addct_inf(samples,sample,adduct,A,B,
                                feature_dicts)
                            else:
                                app_addct_inf(samples,sample,adduct,B,A,
                                feature_dicts)

                        #isotopic +1 peak
                        elif "[M+1+H]+" in adduct:
                            if A_mz > B_mz:
                                app_addct_inf(samples,sample,adduct,A,B,
                                feature_dicts)
                            else:
                                app_addct_inf(samples,sample,adduct,B,A,
                                feature_dicts)
                                
                        #isotopic +2 peak
                        elif "[M+2+H]+" in adduct:
                            if A_mz > B_mz:
                                app_addct_inf(samples,sample,adduct,A,B,
                                feature_dicts)
                            else:
                                app_addct_inf(samples,sample,adduct,B,A,
                                feature_dicts)

                        #isotopic +3 peak
                        elif "[M+3+H]+" in adduct:
                            if A_mz > B_mz:
                                app_addct_inf(samples,sample,adduct,A,B,
                                feature_dicts)
                            else:
                                app_addct_inf(samples,sample,adduct,B,A,
                                feature_dicts)

                        #isotopic +4 peak
                        elif "[M+4+H]+" in adduct:
                            if A_mz > B_mz:
                                app_addct_inf(samples,sample,adduct,A,B,
                                feature_dicts)
                            else:
                                app_addct_inf(samples,sample,adduct,B,A,
                                feature_dicts)
                        
                        #isotopic +5 peak
                        elif "[M+5+H]+" in adduct:
                            if A_mz > B_mz:
                                app_addct_inf(samples,sample,adduct,A,B,
                                feature_dicts)
                            else:
                                app_addct_inf(samples,sample,adduct,B,A,
                                feature_dicts)
                                            
                        #double proton isotopic +1 peak
                        elif "[M+1+2H]2+" in adduct:
                            if A_mz < B_mz:
                                app_addct_inf(samples,sample,adduct,A,B,
                                feature_dicts)
                            else:
                                app_addct_inf(samples,sample,adduct,B,A,
                                feature_dicts)
                        
                        #double proton isotopic +2 peak
                        elif "[M+2+2H]2+" in adduct:
                            if A_mz < B_mz:
                                app_addct_inf(samples,sample,adduct,A,B,
                                feature_dicts)
                            else:
                                app_addct_inf(samples,sample,adduct,B,A,
                                feature_dicts)
                        
                        #double proton isotopic +3 peak
                        elif "[M+3+2H]2+" in adduct:
                            if A_mz < B_mz:
                                app_addct_inf(samples,sample,adduct,A,B,
                                feature_dicts)
                            else:
                                app_addct_inf(samples,sample,adduct,B,A,
                                feature_dicts)
                        
                        #double proton isotopic +4 peak
                        elif "[M+4+2H]2+" in adduct:
                            if A_mz < B_mz:
                                app_addct_inf(samples,sample,adduct,A,B,
                                feature_dicts)
                            else:
                                app_addct_inf(samples,sample,adduct,B,A,
                                feature_dicts)
                        
                        #double proton isotopic +5 peak
                        elif "[M+5+2H]2+" in adduct:
                            if A_mz < B_mz:
                                app_addct_inf(samples,sample,adduct,A,B,
                                feature_dicts)
                            else:
                                app_addct_inf(samples,sample,adduct,B,A,
                                feature_dicts)
                                
                        #+1 isotopic peak of a double charged ion: 
                        #[M+2H] vs [M+1+2H]
                        elif "+1 isotopic peak of [M+2H]2+" in adduct:
                            if A_mz > B_mz:
                                app_addct_inf(samples,sample,adduct,A,B,
                                feature_dicts)
                            else:
                                app_addct_inf(samples,sample,adduct,B,A,
                                feature_dicts)
                                
                    else:
                        #Peak collision is registered
                        #Adds peak collision status to feature
                        samples[sample].at[A,
                        "feature_collision"] = True
                        samples[sample].at[B,
                        "feature_collision"] = True
                        #Adds Feature IDs of colliding peaks
                        samples[sample].at[A,
                        "feature_collision_list"].append(
                        samples[sample]["feature_ID"][B])
                        samples[sample].at[B,
                        "feature_collision_list"].append(
                        samples[sample]["feature_ID"][A])
                        
                else:
                    #peaks do not overlap
                    pass
                    
        #assign manipulated dataframes to dictionary
        returned_samples[sample] = samples[sample]

    return returned_samples


def detect_adducts(A_mz: float, B_mz: float,
strictness_ppm) -> list:
    """Check if features A and B are common adducts of each other.
    
    Parameters
    ----------
    A_mz : `float`
    B_mz : `float`
    
    Returns
    -------
    `list`
    
    Notes
    -----
    Considers [M+H]+ as "base", since it is the most common adduct in 
    ESI. [1] Assumes that A and B are different kinds of adducts.
    If any comparison of peaks A and B returns a mass error of 
     < n ppm (default 20), a putative adduct was found.
    
    Since [M+H]+ is considered the 'base' adduct,
    adducts are calculated from [M+H]+ (e.g. [M-H+Na]+ = 21.981942 diff)
    
    Sources:
    [1] doi.org/10.1021/acs.jcim.1c00579 
    
    monoisotopic masses:    https://fiehnlab.ucdavis.edu/staff
                            /kind/Metabolomics/MS-Adduct-Calculator/
    """
    #Definitions of variables
    Na = 21.981942 #[M-H+Na]: proton already subtracted
    H = 1.007276 #mass of proton
    C13_12 = 1.0033548 #difference between 13C and 12C isotopes 
    
    #M+Na (sodium)
    if (calc_mass_deviation(
        (A_mz + Na), B_mz) < strictness_ppm
    ) or (
    calc_mass_deviation(
        (B_mz + Na), A_mz) < strictness_ppm
    ):
        return [True, "[M+Na]+"]
    
    #2M+Na (dimer + sodium)
    elif (calc_mass_deviation(
        ((2 * (A_mz - H)) + Na + H), B_mz) < strictness_ppm
    ) or (
    calc_mass_deviation(
        ((2 * (B_mz - H)) + Na + H), A_mz) < strictness_ppm
    ):
        return [True, "[2M+Na]+"]

    #M+2H and 2M+H
    elif (calc_mass_deviation(
        ((A_mz + H)/2), B_mz) < strictness_ppm
    ) or (
    calc_mass_deviation(
        ((B_mz + H)/2), A_mz) < strictness_ppm
    ):
        return [True, "[M+2H]2+", "[2M+H]+"]
        
    #M+3H
    elif (calc_mass_deviation(
        ((A_mz + (2 * H))/3), B_mz) < strictness_ppm
    ) or (
    calc_mass_deviation(
        ((B_mz + (2 * H))/3), A_mz) < strictness_ppm
    ):
        return [True, "[M+3H]3+"]
        
    #+1 isotopic peak, addition of 1 neutron
    elif (calc_mass_deviation(
        (A_mz + C13_12), B_mz) < strictness_ppm
    ) or (
    calc_mass_deviation(
        (B_mz + C13_12), A_mz) < strictness_ppm
    ):
        return [True, "[M+1+H]+"]
        
    #+2 isotopic peak, addition of 2 neutrons
    elif (calc_mass_deviation(
        (A_mz + (2 * C13_12)), B_mz) < strictness_ppm
    ) or (
    calc_mass_deviation(
        (B_mz + (2 * C13_12)), A_mz) < strictness_ppm
    ):
        return [True, "[M+2+H]+"]
        
    #+3 isotopic peak, addition of 3 neutrons
    elif (calc_mass_deviation(
        (A_mz + (3 * C13_12)), B_mz) < strictness_ppm
    ) or (
    calc_mass_deviation(
        (B_mz + (3 * C13_12)), A_mz) < strictness_ppm
    ):
        return [True, "[M+3+H]+"]
    
    #+4 isotopic peak, addition of 4 neutrons
    elif (calc_mass_deviation(
        (A_mz + (4 * C13_12)), B_mz) < strictness_ppm
    ) or (
    calc_mass_deviation(
        (B_mz + (4 * C13_12)), A_mz) < strictness_ppm
    ):
        return [True, "[M+4+H]+"]
    
    #+5 isotopic peak, addition of 5 neutrons
    elif (calc_mass_deviation(
        (A_mz + (5 * C13_12)), B_mz) < strictness_ppm
    ) or (
    calc_mass_deviation(
        (B_mz + (5 * C13_12)), A_mz) < strictness_ppm
    ):
        return [True, "[M+5+H]+"]
        
    #double charged +1 isotopic peak, addition of 1 neutron and 1 proton
    elif (calc_mass_deviation(
        ((A_mz + (C13_12 + H)) / 2), B_mz) < strictness_ppm
    ) or (
    calc_mass_deviation(
        ((B_mz + (C13_12 + H)) / 2), A_mz) < strictness_ppm
    ):
        return [True, "[M+1+2H]2+"]
        
    #double charged +2 isotopic peak, addition of 2 neutron and 1 proton
    elif (calc_mass_deviation(
        ((A_mz + ((2 * C13_12) + H)) / 2), B_mz) < strictness_ppm
    ) or (
    calc_mass_deviation(
        ((B_mz + ((2 * C13_12) + H)) / 2), A_mz) < strictness_ppm
    ):
        return [True, "[M+2+2H]2+"]
        
    #double charged +3 isotopic peak, addition of 3 neutron and 1 proton
    elif (
    calc_mass_deviation(
        ((A_mz + ((3 * C13_12) + H)) / 2), B_mz) < strictness_ppm
    ) or (
    calc_mass_deviation(
        ((B_mz + ((3 * C13_12) + H)) / 2), A_mz) < strictness_ppm
    ):
        return [True, "[M+3+2H]2+"]
        
    #double charged +4 isotopic peak, addition of 4 neutron and 1 proton
    elif (
    calc_mass_deviation(
        ((A_mz + ((4 * C13_12) + H)) / 2), B_mz) < strictness_ppm
    ) or (
    calc_mass_deviation(
        ((B_mz + ((4 * C13_12) + H)) / 2), A_mz) < strictness_ppm
    ):
        return [True, "[M+4+2H]2+"]
    
    #double charged +5 isotopic peak, addition of 5 neutron and 1 proton
    elif (
    calc_mass_deviation(
        ((A_mz + ((5 * C13_12) + H)) / 2), B_mz) < strictness_ppm
    ) or (
    calc_mass_deviation(
        ((B_mz + ((5 * C13_12) + H)) / 2), A_mz) < strictness_ppm
    ):
        return [True, "[M+5+2H]2+"]
    
    #+1 isotopic peak of a double protonated ion: [M+2H] vs [M+1+2H]
    elif (
    calc_mass_deviation(
        (A_mz + (C13_12/2)), B_mz) < strictness_ppm
    ) or (
    calc_mass_deviation(
        (B_mz + (C13_12/2)), A_mz) < strictness_ppm
    ):
        return [True, "+1 isotopic peak of [M+2H]2+"]
    
    else:
        return [False]

def calc_mass_deviation(A_mz: float, B_mz: float
) -> float:
    """Calculates mass deviation in ppm between two precursor m/z:
    
    Parameters
    ----------
    A_mz : `float`
    B_mz : `float`
    
    Returns
    -------
    `float`
        
    Notes
    -----
    "Mass measurement error" taken from publication:
    doi.org/10.1016/j.jasms.2010.06.006 
    """
    return abs(
                ((A_mz - B_mz) / B_mz) * (10**6)
            )

def app_addct_inf(
    samples: str, 
    sample: str,
    adduct: list, 
    first: int,
    second: int,
    feature_dicts,
    ):
    """Append info on adducts to table.
    
    Parameters
    ----------
    samples : `dict`
        dict of pandas dataframes of sample-specific features, with
        key=sample_name : value=pandas.df
    sample : `str`
        key to samples dict
    adduct : `list`
        List containing True/False on [0] and a string describing the 
        kind of adduct in [1]
    first : `int`
        Index of feature 'first'
    second : `int`
        Index of feature 'second'
    feature_dicts : `dict`
        
    Notes
    -----
    Function to append adduct information to dataframe.
    'second' is considered the M+H+ ion, while 'first' is considered a different
    adduct. 
    """
    first_str = "".join([
                    adduct[1],
                    "(ID ",
                    str(samples[sample]["feature_ID"][second]),
                    ', ',
                    str(sample),
                    ')',
                    ])
    
    second_str = "".join([
                    "ID ",
                    str(samples[sample]["feature_ID"][first]),
                    ": ",
                    adduct[1],
                    ' (',
                    str(sample),
                    ')',
                ])
    
    samples[sample].at[first,"putative_adduct_detection"].append(first_str)
    samples[sample].at[second,"putative_adduct_detection"].append(second_str)
    
    first_ID = int(samples[sample].at[first,'feature_ID'])
    second_ID = int(samples[sample].at[second,'feature_ID'])
    
    feature_dicts[first_ID]['ann_adduct_isotop'].append(first_str)
    feature_dicts[second_ID]['ann_adduct_isotop'].append(second_str)
    
    

def app_dimer_dbl(
    samples: str, 
    sample: str,
    adduct: list, 
    first: int,
    second: int,
    feature_dicts):
    """Append info on dimer/double charged ion 
    
    Parameters
    ----------
    samples : `dict`
        dict of pandas dataframes of sample-specific features, with
        key=sample_name : value=pandas.df
    sample : `str`
        key to samples dict
    adduct : `list`
        List containing True/False on [0] and a string describing the 
        kinds of adducts in [1] and [2]
    first : `int`
        Index of feature 'first'
    second : `int`
        Index of feature 'second'
    feature_dicts : `dict`
        
    Notes
    -----
    More specific version of app_addct_inf() function, with different 
    annotation to append. Here, one of the ions is the [2M+H]+ ion,
    the other one is the [M+2H]2+ ion. Lack of isotopic pattern makes it
    impossible to say which is which, so both are annotated.
    Consider two overlapping peaks A and B:
        -peak A with m/z 1648.47;
        -peak B with m/z 824.74.
    If A is assumed [M+H]+, B would be [M+2H]2+
    If B is assumed [M+H]+, A would be [2M+H]+
    Thus, assignment is performed for [M+2H]2+ and [2M+H]+ in parallel
    """
    first_str = "".join([
                    adduct[1],
                    "(ID ",
                    str(samples[sample]["feature_ID"][second]),
                    ', ',
                    str(sample),
                    ')',
                    ])
    
    second_str = "".join([
                    adduct[2],
                    "(ID ",
                    str(samples[sample]["feature_ID"][first]),
                    ', ',
                    str(sample),
                    ')',
                    ])
    
    #peak 'first' is putatively [M+2H]2+
    samples[sample].at[first,"putative_adduct_detection"].append(first_str)
    
    #peak 'second' is putatively [2M+H]+
    samples[sample].at[second,"putative_adduct_detection"].append(second_str)

    first_ID = int(samples[sample].at[first,'feature_ID'])
    second_ID = int(samples[sample].at[second,'feature_ID'])
    
    feature_dicts[first_ID]['ann_adduct_isotop'].append(first_str)
    feature_dicts[second_ID]['ann_adduct_isotop'].append(second_str)

