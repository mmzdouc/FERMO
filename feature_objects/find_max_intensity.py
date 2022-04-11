import pandas as pd


def find_max_intensity(row: str) -> float:
    '''Extract feature maximum intensity.
    
    Parameters
    ----------
    row : `pandas.core.series.Series`
        Row from MZmine3 peaktable
    
    Returns
    -------
    feature_maximum_intensity : `float`
    
    Notes
    -------
    Covers two kind of MzMine3 tables (ALL and SIMPLE); in case 
    of SIMPLE, finds maximum value across samples.
    '''
    max_int_table_all = 0
    max_int_table_simple = 0
    feature_maximum_intensity = 0
    #tests for table ALL
    try:
        max_int_table_all = row["intensity_range:max"]
    except:
        pass
    #tests for table SIMPLE
    try: 
        max_int_table_simple = row[row!=0].filter(regex="Peak").max()
    except:
        pass
    
    if max_int_table_all > 0:
        feature_maximum_intensity = float(max_int_table_all)
        return feature_maximum_intensity
    elif max_int_table_simple > 0:
        feature_maximum_intensity = float(max_int_table_simple)
        return feature_maximum_intensity
    else:
        print("WARNING: Max feature intensity could not be determined.")
        print("WARNING: Only MzMine3-style peaktables are supported")
        print("WARNING: A value of 0 for the maximum feature int is set.")
        return feature_maximum_intensity


#max intensity; 


#switch for type of table: SIMPLE or ALL

#SIMPLE: collect all columns thaat are not null, extract values, find max
#ALL: query 



#scrape table with regex 
#if dataframe not empty; calc averaged etc
#else
#set fwhm to fake 0.2 min
#return a float to store in Feature Objects
#edit Feature Object class
#edit feature_object_creation 
