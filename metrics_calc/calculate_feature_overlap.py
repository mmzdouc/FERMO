import pandas as pd


def calculate_feature_overlap(samples: str, strictness_ppm: float
) -> dict:
    """Detects feature collision (overlap of peaks) based on 
    retention time.
    
    Parameters
    ----------
    samples : `dict`
        dict of pandas dataframes of sample-specific features, with
        key=sample_name : value=pandas.df
    strictness_ppm : `float`
        Tolerable mass deviation in ppm. Allows to tweak precision of
        matching. Should be matched to precision of instrument. E.g.
        20 ppm is still tolerable
    
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
    In mass spectrometry analysis, different ions for the same analyte
    are commonly observed (e.g. [M+H]+, [Na+H]+, [M+2H]2+). Since 
    the [M+H]+ ion is the most common one in ESI, all other adducts 
    can be considered artefacts. Feature collisions of such adducts 
    originating from the same analyte can therefore be ignored (not
    really present in sample). The same is true for duplicate peaks
    due to retention time drifts that arise from the data preprocessing.
    Therefore, detected overlaps are checked if they are I) duplicates
    of each other (same m/z inside mass tolerance); II) are adducts
    of each other (checked for most common adducts: [M+Na]+, [M+2H]2+,
    [2M+H]+, [M+3H]3+). If they are duplicates or adducts, this is 
    noted and the collision is not registered. 
    """
    returned_samples  = dict()
    for sample in samples:
        #Column "feature_collision": most peaks won't overlap
        samples[sample]["feature_collision"] = False
        
        #Column "feature_collision_list" - register overlapping features
        #Must be written that way bc "df['lists'] = [[]]* len(df)"
        #leads to broadcasted assignment when a single field is assigned
        #"df.at[1, "lists"].append("1")". See also:
        #stackoverflow.com/questions/38307489/
        #set-list-as-value-in-a-column-of-a-pandas-dataframe
        samples[sample]["feature_collision_list"] = [
        [] for r in range(len(samples[sample]))]
        
        #Column "duplicate_detection": stores duplicates in list. 
        #For code explanation, see above 
        samples[sample]["possible_duplicate_detection"] = [
        [] for r in range(len(samples[sample]))]
        
        #Column "putative_adduct_detection": stores adducts in list. 
        #For code explanation, see above
        samples[sample]["putative_adduct_detection"] = [
        [] for r in range(len(samples[sample]))]
        
        #make all against all comparison of contained features
        for i in range(len(samples[sample])): 
            for j in range(i+1, len(samples[sample])):
                #readability
                A_left = samples[sample]["rt_start"][i]
                A_right = samples[sample]["rt_stop"][i]
                B_left = samples[sample]["rt_start"][j]
                B_right = samples[sample]["rt_stop"][j]
                A_mz = samples[sample]["precursor_mz"][i]
                B_mz = samples[sample]["precursor_mz"][j]
                #Check for peak overlap: abstraction to fwhm. Peak 
                #defined as (x1,x2) on directional vector (retention
                #time). If any of "A_right < B_left or B_right < A_left"
                #evaluates to True, peaks A and B do not overlap.
                #For readability of flow logic, "not" is prefixed
                #This way, condition evaluates to true if peaks
                #DO overlap.
                if not (A_right < B_left or B_right < A_left):
                    #DUPLICATE
                    #True if duplicate peak (mass error < strictness)
                    if calc_mass_deviation(
                    A_mz, B_mz) < strictness_ppm:
                        #registers possible duplicates
                        samples[sample].at[i,
                        "possible_duplicate_detection"].append(
                        samples[sample]["feature_ID"][j])
                        samples[sample].at[j,
                        "possible_duplicate_detection"].append(
                        samples[sample]["feature_ID"][i])
                    #ADDUCTS
                    #True if any of the common adducts.
                    #"Walrus operator" := needs python 3.8 but allows
                    #to use one function call for condictional and 
                    #for variable assignment
                    elif True in (adducts := detect_adducts(
                    A_mz, B_mz, strictness_ppm)):
                        #determines which adduct relative to [M+H]+
                        if "[M+Na]+" in adducts:
                            #find which one is the adduct + assignment
                            if A_mz > B_mz:
                                samples[sample].at[i,
                                "putative_adduct_detection"].append(
                                "".join([
                                adducts[1],
                                " of ",
                                str(samples[sample]["feature_ID"][j] 
                                )]))
                            else:
                                samples[sample].at[j,
                                "putative_adduct_detection"].append(
                                "".join([
                                adducts[1],
                                " of ",
                                str(samples[sample]["feature_ID"][i] 
                                )]))
                        elif "[M+2H]2+" in adducts:
                            #Find which one is the adduct + assignment.
                            #Consider two overlapping peaks A and B:
                            #peak A with m/z 1648.47;
                            #peak B with m/z 824.74.
                            #If A is assumed [M+H]+, B would be [M+2H]2+
                            #If B is assumed [M+H]+, A would be [2M+H]+
                            #Thus, assignment is performed for both 
                            #[M+2H]2+ and [2M+H]+ in parallel
                            if A_mz < B_mz:
                                #peak A is putatively [M+2H]2+
                                samples[sample].at[i,
                                "putative_adduct_detection"].append(
                                "".join([
                                adducts[1],
                                " of ",
                                str(samples[sample]["feature_ID"][j] 
                                )]))
                                #peak B is putatively [2M+H]+
                                samples[sample].at[j,
                                "putative_adduct_detection"].append(
                                "".join([
                                adducts[2],
                                " of ",
                                str(samples[sample]["feature_ID"][i] 
                                )]))
                            else:
                                #peak B is putatively [M+2H]2+
                                samples[sample].at[j,
                                "putative_adduct_detection"].append(
                                "".join([
                                adducts[1],
                                " of ",
                                str(samples[sample]["feature_ID"][i] 
                                )]))
                                #peak A is putatively [2M+H]+
                                samples[sample].at[i,
                                "putative_adduct_detection"].append(
                                "".join([
                                adducts[2],
                                " of ",
                                str(samples[sample]["feature_ID"][j] 
                                )]))
                        elif "[M+3H]3+" in adducts:
                            #find which one is the adduct + assignment
                            if A_mz < B_mz:
                                samples[sample].at[i,
                                "putative_adduct_detection"].append(
                                "".join([
                                adducts[1],
                                " of ",
                                str(samples[sample]["feature_ID"][j] 
                                )]))
                            else:
                                samples[sample].at[j,
                                "putative_adduct_detection"].append(
                                "".join([
                                adducts[1],
                                " of ",
                                str(samples[sample]["feature_ID"][i] 
                                )]))
                    #Peak collision is registered
                    else: 
                        #Adds peak collision status to feature
                        samples[sample].at[i,
                        "feature_collision"] = True
                        samples[sample].at[j,
                        "feature_collision"] = True
                        #Adds Feature IDs of colliding peaks
                        samples[sample].at[i,
                        "feature_collision_list"].append(
                        samples[sample]["feature_ID"][j])
                        samples[sample].at[j,
                        "feature_collision_list"].append(
                        samples[sample]["feature_ID"][i])
                #peaks do not overlap
                else:
                    pass
        #assign manipulated dataframes to dictionary
        returned_samples[sample] = samples[sample]
    return returned_samples


def calc_mass_deviation(A_mz: float, B_mz: float
) -> float:
    """Calculates mass deviation in ppm between two precursor m/z:
    
    Parameters
    ----------
    A_mz : `float`
    B_mz : `float`
    
    Returns
    -------
    mass_deviation : `float`
        
    Notes
    -----
    "Mass measurement error" taken from publication:
    doi.org/10.1016/j.jasms.2010.06.006 
    """
    mass_deviation = (
    ((A_mz - B_mz) / B_mz)
    * 10**6
    )
    #pos/neg values possible -> make absolute
    return abs(mass_deviation)

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
    ESI. Adducts are calculated from [M+H]+, e.g. [M-H+Na]+ = 21.981942.
    Data taken from:
    https://fiehnlab.ucdavis.edu/
    staff/kind/Metabolomics/MS-Adduct-Calculator/
    and
    doi.org/10.1021/acs.jcim.1c00579 
    """
    Na = 21.981942 #[M-H+Na]
    H = 1.007276
    #Assumes that A and B are different kinds of adducts.
    #If any comparison of peaks A and B returns a mass error of 
    # < n ppm (default 20), an adduct was found.
    
    #M+Na (Sodium)
    if (
    calc_mass_deviation((A_mz + Na), B_mz) < strictness_ppm
    ) or (
    calc_mass_deviation((B_mz + Na), A_mz) < strictness_ppm
    ):
        return [True, "[M+Na]+"]
    #M+2H and 2M+H
    elif (
    calc_mass_deviation((((A_mz + H)/2)), B_mz) < strictness_ppm
    ) or (
    calc_mass_deviation(((B_mz + H)/2), A_mz) < strictness_ppm
    ):
        return [True, "[M+2H]2+", "[2M+H]+"]
    #M+3H
    elif (
    calc_mass_deviation(((A_mz + (2 * H))/3), B_mz) < strictness_ppm
    ) or (
    calc_mass_deviation(((B_mz + (2 * H))/3), A_mz) < strictness_ppm
    ):
        return [True, "[M+3H]3+"]
    else:
        return [False]
