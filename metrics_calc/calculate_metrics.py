
from .get_samplespecific_features import get_samplespecific_features
from .calculate_feature_overlap import calculate_feature_overlap



def calculate_metrics(peaktable, feature_objects):
    """
    """
    samples = get_samplespecific_features(peaktable)
    samples_feature_overlap = calculate_feature_overlap(samples)
    
    
    # ~ for sample in samples:
        # ~ print(sample, type(sample))
        # ~ feature_overlap = calculate_feature_overlap(sample)
        #check for adduct (if m/z matches)
        #make stub for possible check if in same similarity clique
    
    
    
    # ~ return metrics





#call feature_collision for peaks

#change range to len of pandas array
#consider rt k-mers so that no all-against-all needs to be performed?
#more relevant if there are more features
#make calls for rt etc to Feature Objects
# ~ for i in range(1, 10):
    # ~ for j in range(i+1, 10):
        # ~ print(i, j)



# ~ simplyfy to x only!

# ~ if (A_top < B_bottom or B_top < A_bottom):
    # ~ print ("Rectangles A and B do not overlap")
# ~ else:
    # ~ print("Rectangels A and B overlap")


# ~ byt_bottom = [(byt_rt-(byt_fwhm*0.5)), 0]
# ~ byt_top = [(byt_rt+(byt_fwhm*0.5)), (byt_int * 0.5)]




"""NOTES: script to calculate metrics

1) read sample-specific dataframes, calculate overlaps of peaks,
add column of collision true/false, add column with a list of feature IDs which clashed
2)annotation features per sample -> top n most intense;
sample-metric: how many clashes
bioactivity of samples: are features in samples that are also in samples
that are not bioactive: if yes, probably not bioactivity-associated
3)visualize samples by drawing (2d or 3d)
"""
