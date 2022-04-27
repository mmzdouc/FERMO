
import pandas as pd


def display_metrics(samples: str, feature_objects: str, topn = int):
    """Display sample scores and topn of features
    
    Parameters
    ----------
    samples : `dict`
        Sample_names(keys):pandas.core.frame.DataFrame(values)
    feature_objects : `dict`
        Feature_ID(keys):Feature_Objects(values)
    topn : `int`
    
    Notes
    -----
    Calculates topN samples by summing the combined_score of 
    its features.
    Determines the topN features across all samples.
    """
    
    #for each sample, its score
    #create a list of sample names and a list of their overall scores
    sample_scores = dict()
    for sample in samples:
        sample_scores[sample] = samples[sample].loc[:,
        "combined_score"].sum(axis=0)
    topn_samples = sorted(
    sample_scores, key=sample_scores.get, reverse=True)[:topn]
    
    print(
    f"""
            These are the top {topn} scoring samples.
    """ )
    #use topn_samples to print intensities from sample_scores
    for sample in topn_samples:
        print(f"""Sample {sample} has a score of {sample_scores[sample]}.
            From convolutedness_score: {samples[sample].loc[:,
            "convolutedness_score"].sum(axis=0)}
            From bioactivity_score: {samples[sample].loc[:,
            "bioactivity_score"].sum(axis=0)}
            From novelty_score: {samples[sample].loc[:,
            "novelty_score"].sum(axis=0)}
            From diversity_score: {samples[sample].loc[:,
            "diversity_score"].sum(axis=0)}
            Total number of features: {len(samples[sample])}""")
        print(f"""Top {topn} highest scoring features for sample {sample}:""", end='')
        for i in range(topn):
            print(f"""
            {i+1}) Feature_ID: {samples[sample].at[i, "feature_ID"]}, precursor_mz: {samples[sample].at[i, "precursor_mz"]}, retention_time: {samples[sample].at[i, "retention_time"]}, 
                intensity: {samples[sample].at[i, "intensity"]}, peak_overlap: {samples[sample].at[i, "feature_collision"]}, bioactivity_linked: {feature_objects[samples[sample].at[i, "feature_ID"]].bioactivity_associated},
                putative adducts: {*samples[sample].at[i, "putative_adduct_detection"],},
                possible duplicates: {*samples[sample].at[i, "possible_duplicate_detection"],}""", end='')
        print("""
        """)
        
    #print topn features from total
    all_features = dict()
    for sample in samples:
        for index, row in samples[sample].iterrows():
            all_features["".join(
            [sample, " " ,str(row["feature_ID"])])] = row["combined_score"]
    topn_features = sorted(
    all_features, key=all_features.get, reverse=True)[:topn]
    counter = 0
    print(
    f"""
            These are the top {topn} overall scoring features.
    """ )
    for top_features in topn_features:
        counter = counter + 1
        sample = top_features.split()[0]
        feature_ID = int(top_features.split()[1])
        row = samples[sample].loc[samples[sample]["feature_ID"] == feature_ID]
        print(f"""{counter}) From sample {sample}, feature_ID {feature_ID}""")
        print(f"""(m/z {row.iloc[0]["precursor_mz"]}, rt {row.iloc[0]["retention_time"]}, intensity {row.iloc[0]["intensity"]}, combined_score {round(row.iloc[0]["combined_score"], 3)},
putative adducts: {*row.iloc[0]["putative_adduct_detection"],},
ossible duplicates: {*row.iloc[0]["possible_duplicate_detection"],})""")

