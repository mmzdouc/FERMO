import json
import numpy as np
import pandas as pd
import plotly
import plotly.graph_objects as go
from fermo.app_utils.dashboard.dashboard_functions import (
    default_filters,
    generate_subsets,
)

from fermo.app_utils.dashboard.dashboard_functions import color_dict


def plot_central_chrom(
    sel_sample: str,
    active_feature_index: int,
    sample_stats: dict,
    samples_json_dict: dict,
    feature_dicts: dict,
    sel_all_vis: str,
    thresholds: dict,
) -> str:
    '''Plot central chromatogram

    Parameters
    ----------
    sel_sample: `str`\n
    active_feature_index: `int`\n
    sample_stats: `dict`\n
    samples_json_dict: `dict`\n
    feature_dicts: `dict`\n
    sel_all_vis: `str`\n
    thresholds: `dict`

    Returns
    -------
    graphJSON: `str`
        stringified JSON object of plotly graph
    '''
    colors = color_dict()
    fig = go.Figure()
    fig.update_layout(
        margin=dict(t=0, b=0, r=0),
        height=300,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    fig.update_xaxes(
        autorange=False,
        showgrid=False,
        visible=True,
        range=[
            (sample_stats["rt_min"]-(sample_stats["rt_range"]*0.05)),
            (sample_stats["rt_max"]+(sample_stats["rt_range"]*0.05)),
        ],
    )
    fig.update_yaxes(
        autorange=False,
        showgrid=False,
        title_text="Relative Intensity",
        range=[0, 1.05],
    )
    filtered_samples = {}
    for sample in samples_json_dict:
        filtered_samples[sample] = generate_subsets(
            samples_json_dict,
            sample,
            thresholds,
            feature_dicts
        )
    for _, row in samples_json_dict[sel_sample].iterrows():
        if (
            int(row['feature_ID']) in filtered_samples[sel_sample]['blank_ms1']
            and sel_all_vis == 'ALL'
        ):
            fig.add_trace(
                append_scatter_text(
                    row,
                    colors['light_yellow'],
                    colors['yellow'],
                    4,
                    colors['black'],
                    feature_dicts,
                )
            )
        elif (
            int(row['feature_ID']) in filtered_samples[sel_sample]['blank_ms1']
            and sel_all_vis == 'HIDDEN'
        ):
            fig.add_trace(append_invis_trace(row))

        elif int(row['feature_ID']) in (
                filtered_samples[sel_sample]['select_sample_spec']
        ):
            fig.add_trace(
                append_scatter_text(
                    row,
                    colors['light_green'],
                    colors['purple'],
                    4,
                    colors['black'],
                    feature_dicts,
                )
            )
        elif int(row['feature_ID']) in (
            filtered_samples[sel_sample]['select_group_spec']
        ):
            fig.add_trace(
                append_scatter_text(
                    row,
                    colors['light_green'],
                    colors['black'],
                    4,
                    colors['black'],
                    feature_dicts,
                )
            )
        elif int(row['feature_ID']) in (
            filtered_samples[sel_sample]['select_remainder']
        ):
            fig.add_trace(
                append_scatter_text(
                    row,
                    colors['light_green'],
                    colors['green'],
                    4,
                    colors['black'],
                    feature_dicts,
                )
            )
        elif (
            int(row['feature_ID']) in (
                filtered_samples[sel_sample]['nonselect_sample_spec']
            )
            and sel_all_vis == 'ALL'
        ):
            fig.add_trace(
                append_scatter_text(
                    row,
                    colors['light_cyan'],
                    colors['purple'],
                    4,
                    colors['black'],
                    feature_dicts,
                )
            )
        elif (
            int(row['feature_ID']) in (
                filtered_samples[sel_sample]['nonselect_sample_spec']
            )
            and sel_all_vis == 'HIDDEN'
        ):
            fig.add_trace(append_invis_trace(row))

        elif (
            int(row['feature_ID']) in (
                filtered_samples[sel_sample]['nonselect_group_spec']
            )
            and sel_all_vis == 'ALL'
        ):
            fig.add_trace(
                append_scatter_text(
                    row,
                    colors['light_cyan'],
                    colors['black'],
                    4,
                    colors['black'],
                    feature_dicts,
                )
            )
        elif (
            int(row['feature_ID']) in (
                filtered_samples[sel_sample]['nonselect_group_spec']
            )
            and sel_all_vis == 'HIDDEN'
        ):
            fig.add_trace(append_invis_trace(row))
        elif (
            int(row['feature_ID']) in (
                filtered_samples[sel_sample]['nonselect_remainder']
            )
            and sel_all_vis == 'ALL'
        ):
            fig.add_trace(
                append_scatter_text(
                    row,
                    colors['light_cyan'],
                    colors['cyan'],
                    4,
                    colors['black'],
                    feature_dicts,
                )
            )
        elif (
            int(row['feature_ID']) in (
                filtered_samples[sel_sample]['nonselect_remainder']
            )
            and sel_all_vis == 'HIDDEN'
        ):
            fig.add_trace(append_invis_trace(row))
        else:
            fig.add_trace(
                append_scatter_text(
                    row,
                    colors['very_light_grey'],
                    colors['very_light_grey'],
                    4,
                    colors['black'],
                    feature_dicts,
                )
            )

    if isinstance(active_feature_index, int):
        fig.add_shape(
            type="rect",
            xref="x",
            yref="y",
            x0=samples_json_dict[sel_sample].at[
                active_feature_index, 'rt_start'],
            x1=samples_json_dict[sel_sample].at[
                active_feature_index, 'rt_stop'],
            y0=0,
            y1=(samples_json_dict[sel_sample].at[
                active_feature_index, 'norm_intensity'] * 1),
            line={
                'color': colors['blue'],
                'width': 5,
                'dash': 'dash',
            }
        )

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


def plot_clique_chrom(
    selected_sample: str,
    active_feature_index: int,
    active_feature_id: int,
    sample_stats: dict,
    samples_json_dict: dict,
    feature_dicts: dict,
) -> str:
    '''Plot clique chromatogram - overview

    Parameters
    ----------
    selected_sample: `str`\n
    active_feature_index: `int`\n
    active_feature_id: `int`\n
    sample_stats: `dict`\n
    samples_json_dict: `dict`\n
    feature_dicts: `dict`\n

    Returns
    -------
    clique_chromatogram: `str`
        stringified JSON object of plotly graph
    '''
    fig = go.Figure()

    fig.update_layout(
        margin=dict(t=0, b=0, r=0),
        height=100,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )

    fig.update_yaxes(
        visible=False,
        showgrid=False,
    )

    fig.update_xaxes(
        autorange=False,
        showgrid=False,
        visible=True,
        title_text="Retention Time (min)",
        range=[
            (sample_stats["rt_min"]-(sample_stats["rt_range"]*0.05)),
            (sample_stats["rt_max"]+(sample_stats["rt_range"]*0.05)),
        ],
    )

    colors = color_dict()
    if isinstance(active_feature_index, int):
        if feature_dicts[str(active_feature_id)]['similarity_clique']:
            for clique_member in (
                sample_stats['cliques']
                    [str(feature_dicts
                         [str(active_feature_id)]
                         ['similarity_clique_number']
                         )]
                    [0]
            ):
                if clique_member != active_feature_id:
                    try:
                        row = samples_json_dict[selected_sample].loc[
                            samples_json_dict[selected_sample]['feature_ID']
                            == clique_member].squeeze()
                        fig.add_trace(
                            append_scatter_text(
                                row,
                                colors['light_red'],
                                colors['red'],
                                3,
                                colors['black'],
                                feature_dicts,
                            )
                        )
                    except:
                        pass
        fig.add_trace(
            append_scatter_text(
                samples_json_dict[selected_sample].loc[
                    samples_json_dict[selected_sample]['feature_ID']
                    == active_feature_id].squeeze(),
                colors['light_blue'],
                colors['blue'],
                3,
                colors['black'],
                feature_dicts,
            )
        )

    clique_chromatogram = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return clique_chromatogram


def append_scatter_text(
    row: pd.Series,
    fill: str,
    line: str,
    width: int,
    bordercolor: str,
    feat_dicts: dict,
) -> go.Scatter:
    '''Create scatter trace with hoverlabel

    Parameters
    ----------
    row : `Pandas.Series`\n
    fill : `str`\n
    line : `str`\n
    width : `int`\n
    bordercolor : `str`\n
    feat_dicts : `dict`

    Returns
    -------
    `Plotly graph object scatter trace`
    '''
    ID = str(row["feature_ID"])

    cosine_ann = "None"
    if feat_dicts[ID]['cosine_annotation']:
        cosine_ann = ''.join([
            feat_dicts[ID]['cosine_annotation_list'][0]['name'],
            ])
    if len(cosine_ann) > 75:
        cosine_ann = (cosine_ann[:75] + '...')  # limit long annotations

    ms2query_ann = "None"
    if feat_dicts[ID]['ms2query']:
        ms2query_ann = ''.join([
            feat_dicts[ID]['ms2query_results'][0]['analog_compound_name'],
            ])
    if len(ms2query_ann) > 75:
        ms2query_ann = (ms2query_ann[:75] + '...')  # limit long annotations

    text = (
        f'Feature ID <b>{row["feature_ID"]}</b>' +
        '<br>' +
        f'<i>m/z</i> <b>{row["precursor_mz"]}</b>' +
        '<br>' +
        f'RT (min) <b>{row["retention_time"]}</b>' +
        '<br>' +
        f'Lib. annot. <b>{cosine_ann}</b>' +
        '<br>' +
        f'MS2Query <b>{ms2query_ann}</b>' +
        '<br>'
    )
    return go.Scatter(
        x=np.array(row['pseudo_chrom_trace'][0]),
        y=np.array(row['pseudo_chrom_trace'][1]),
        fill='toself',
        fillcolor=fill,
        showlegend=False,
        mode="lines",
        line={
            'color': line,
            'shape': 'spline',
            'smoothing': 0.8,
            'width': width,
            },
        hoverinfo="text",  # change to 'skip' if want to suppress
        text=text,
        hoverlabel={
            'bgcolor': 'white',
            'bordercolor': bordercolor}
        )


def append_invis_trace(
    row: pd.Series,
) -> go.Scatter:
    '''Create invisible scatter trace to keep track of peaks

    Parameters
    ----------
    row : `Pandas.Series`

    Returns
    -------
    `Plotly graph object scatter trace`
    '''
    return go.Scatter(
        x=np.array([
            row['pseudo_chrom_trace'][0][0],
            row['pseudo_chrom_trace'][0][6],
        ]),
        y=np.array([0, 0]),
        fill='toself',
        fillcolor='rgba(0,0,0,0)',
        showlegend=False,
        mode="lines",
        line={
            'color': 'rgba(0,0,0,0)',
            'shape': 'spline',
            'smoothing': 0.8,
            'width': 0,
            },
        )
