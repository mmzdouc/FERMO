import json
import plotly
import plotly.express as px


def placeholder_graph():
    '''Load data from plotly express package and create simple graph'''
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
