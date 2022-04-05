import pandas as pd


def samples_listing(peaktable):
    """Gets sample names + feature precence from peaktable:
    
    Scrapes sample names from MzMine2/3 style peak table.
    Extracts feature IDs of features that were found in each sample.
    Returns a dict with samplename:list of features
    """
    samples = dict()
    for entry in peaktable.filter(regex=".mzML|.mzXML").columns:
        features_in_sample = list()
        for index, row in peaktable[["row ID", entry]].iterrows():
            if int(row[entry]) != 0:
                features_in_sample.append(int(row["row ID"]))
        samples[entry] = features_in_sample
    return samples

