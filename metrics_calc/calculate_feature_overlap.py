import pandas as pd



def calculate_feature_overlap(samples: str, strictness_ppm: float
) -> dict:
    """
    Calculate overlap by checking rectangle x axes
    If overlap, check if they are different adducts (lookat most 
    common one from the paper: sodium, water)
    If overlap, check if they are in the same similarity clique (has
    to be implemented before
    If no and overlap, then set flag overlap to True
    add to column
    add list of features that collided with each other(?)
    
    most common adducts: 
    adduct-check: fiehn-lab website reference
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
        
        #Column "adduct_detection": stores adducts in list. 
        #For code explanation, see above
        samples[sample]["adduct_detection"] = [
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
                    #True if any of the common adducts
                    elif True in (adducts := detect_adducts(
                    A_mz, B_mz, strictness_ppm)):
                        #determines which adduct relative to [M+H]+
                        if "[M+Na]+" in adducts:
                            #find which one is the adduct + assignment
                            if A_mz > B_mz:
                                samples[sample].at[i,
                                "adduct_detection"].append(
                                "".join([
                                adducts[1],
                                " of ",
                                str(samples[sample]["feature_ID"][j] 
                                )]))
                            else:
                                samples[sample].at[j,
                                "adduct_detection"].append(
                                "".join([
                                adducts[1],
                                " of ",
                                str(samples[sample]["feature_ID"][i] 
                                )]))
                        elif "[M+2H]2+" in adducts:
                            #Find which one is the adduct + assignment;
                            #Consider two overlapping peaks A and B:
                            #Peak A with m/z 1648.47;
                            #Peak B with m/z 824.74;
                            #If A is assumed [M+H]+, B would be [M+2H]2+
                            #If B is assumed [M+H]+, A would be [2M+H]+
                            #Thus, assignment is performed for both 
                            #[M+2H]2+ and [2M+H]+ in parallel
                            if A_mz < B_mz:
                                samples[sample].at[i,
                                "adduct_detection"].append(
                                "".join([
                                adducts[1],
                                " of ",
                                str(samples[sample]["feature_ID"][j] 
                                )]))
                                #
                                samples[sample].at[j,
                                "adduct_detection"].append(
                                "".join([
                                adducts[2],
                                " of ",
                                str(samples[sample]["feature_ID"][i] 
                                )]))
                            else:
                                samples[sample].at[j,
                                "adduct_detection"].append(
                                "".join([
                                adducts[1],
                                " of ",
                                str(samples[sample]["feature_ID"][i] 
                                )]))
                                #
                                samples[sample].at[i,
                                "adduct_detection"].append(
                                "".join([
                                adducts[2],
                                " of ",
                                str(samples[sample]["feature_ID"][j] 
                                )]))
                        elif "[M+3H]3+" in adducts:
                            #find which one is the adduct + assignment
                            if A_mz < B_mz:
                                samples[sample].at[i,
                                "adduct_detection"].append(
                                "".join([
                                adducts[1],
                                " of ",
                                str(samples[sample]["feature_ID"][j] 
                                )]))
                            else:
                                samples[sample].at[j,
                                "adduct_detection"].append(
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
    Equation as "mass measurement error" taken from
    doi.org/10.1016/j.jasms.2010.06.006 
    """
    #pos/neg values possible -> make absolute
    mass_deviation = (
    ((A_mz - B_mz) / B_mz)
    * 10**6
    )
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
    Na = 21.981942 # [M-H+Na]
    H = 1.007276
    #assumes that A and B are different kinds of adducts 
    #(the are not both [M+H]+)
    #if any comparison of peaks A and B returns a mass error of 
    # < n ppm (default 20), an adduct was found
    #Na (Sodium)
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
