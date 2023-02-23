import pandas as pd


def read_from_metadata_table(
    metadata_table,
    metadata_name,
):
    """Read a metadata table and create groupings

    Parameters
    ----------
    metadata_table : `pandas.core.frame.DataFrame`
        df containing metadata information
    metadata_name : `str` or `None`

    Returns
    -------
    groups_samples : `dict`
        Dict of sets of samples in different groups.

    Notes
    -------
    Tests if (optional) metadata table was provided
    """
    if metadata_name is None:
        groups_samples = dict()
        groups_samples['GENERAL'] = set()
        return groups_samples
    else:
        groups_samples = dict()
        groups_set = set()
        groups_set.add('GENERAL')
        groups_samples['GENERAL'] = set()

        for id, row in metadata_table.iterrows():
            if pd.isnull(row['attribute']):
                groups_samples['GENERAL'].add(row['sample_name'])
            else:
                if row['attribute'] not in groups_set:
                    groups_set.add(row['attribute'])
                    groups_samples[row['attribute']] = set()
                    groups_samples[row['attribute']].add(row['sample_name'])
                else:
                    groups_samples[row['attribute']].add(row['sample_name'])

        return groups_samples
