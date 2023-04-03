import plotly
import plotly.express as px
import json


def placeholder_graph():
    df = px.data.gapminder().query("continent=='Oceania'")
    fig = px.line(
        df,
        x='year',
        y='lifeExp',
        color='country',
        title="Placeholder for main Chromatogram"
    )
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


def empty_feature_info_df() -> list:
    '''Generate placeholder table for feature info

    Returns
    -------
    `list`
        List of lists: empty feature info table
    '''
    data = [
        ['Feature ID', None],
        ['Precursor <i>m/z</i>', None],
        ['Retention time (min)', None],
        ['Feature intensity (absolute)', None],
        ['Feature intensity (relative)', None],
        ['-----', '-----'],
        ['Blank-associated', None],
        ['Novelty score', None],
        ['QuantData-associated', None],
        ['QuantData-trend', None],
        ['Peak overlap (%)', None],
        ['-----', '-----'],
        ['Spectral library: best match', None],
        ['''<a href="https://github.com/iomega/ms2query" target="_blank">
         MS2Query</a>: best match/analog''', None],
        ['''<a href="https://github.com/iomega/ms2query" target="_blank">
         MS2Query</a>: <i>m/z</i> difference to best match/analog''', None],
        ['''<a href="https://github.com/iomega/ms2query" target="_blank">
         MS2Query</a>: predicted class of best match/analog''', None],
        ['''<a href="https://github.com/iomega/ms2query" target="_blank">
         MS2Query</a>:predicted superclass of best match/analog''', None],
        ['-----', '-----'],
        ['Feature found in groups', None],
        ['Fold-differences across groups', None],
        ['Intensity per sample (highest to lowest)', None],
        ['QuantData per sample (highest to lowest)', None],
        ['Original QuantData (highest to lowest)', None],
        ['Putative adducts', None],
        ['-----', '-----'],
        ['Spectral similarity network ID', None],
        ['Groups in network', None],
        ['Number of features in network', None],
        ['IDs of features in network', None],
    ]
    return data
