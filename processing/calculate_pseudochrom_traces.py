import pandas as pd
import numpy as np


def calculate_pseudochrom_traces(
    samples,):
    """Calculate pseuco-chromatogram traces for each peak in each sample
    
    Parameters
    ----------
    samples : `dict`
        sample_names(keys):pandas.core.frame.DataFrame(values)

    Returns
    -------
    samples : `dict`
        sample_names(keys):pandas.core.frame.DataFrame(values)
    
    Notes
    -----
    Pre-calculate pseudo-chromatogram traces to speed up visualization
    in the later dashboard view. 
    
    Returns nested list of x (retention time) and y (relative intensity)
    datapoints
    """
    
    
    for sample in samples:
        trace = []
        for id, row in samples[sample].iterrows():
            rt_start = float(row["rt_start"])
            rt_stop = float(row["rt_stop"])
            rt = float(row["retention_time"])
            rt_range = float(row["rt_stop"]) - float(row["rt_start"])
            fwhm = float(row["fwhm"])
            norm_int = float(row["norm_intensity"])

            #fwhm cannot be larger than the rt_range. If so, set to rt_range
            if fwhm > rt_range:
                fwhm = rt_range

            #calculate start of fwhm. if fwhm_start would be less than
            #rt_start, set fwhm_start to rt_start and add fwhm
            fwhm_start = rt - (0.5 * fwhm)
            if fwhm_start < rt_start:
                fwhm_start = rt_start

            #calculate start of fwhm. if stop would be greater than
            #rt_stop, set to fwhm_stop to rt_stop and move the fwhm_start
            fwhm_stop = fwhm_start + fwhm
            if fwhm_stop > rt_stop:
                fwhm_stop = rt_stop
                fwhm_start = fwhm_stop - fwhm

            #additional data point (left) to make chrom look nicer
            xG = fwhm_start - (0.5 * (fwhm_start - rt_start))
            if xG < rt_start:
                xG = rt_start

            #additional data point (right) to make chrom look nicer
            xK = fwhm_stop + (0.5 * (rt_stop - fwhm_stop))
            if xK > rt_stop:
                xK = rt_stop
            elif xK <= fwhm_stop:
                xK = fwhm_stop + (0.5 * (rt_stop - fwhm_stop))

            trace.append([
                [rt_start,
                xG,
                fwhm_start,
                rt,
                fwhm_stop,
                xK,
                rt_stop,
                ],
                [0,
                (norm_int * 0.15),
                (norm_int * 0.5),
                norm_int,
                (norm_int * 0.5),
                (norm_int * 0.15),
                0,],
            ])
        
        #append to dataframe
        samples[sample]['pseudo_chrom_trace'] = trace
    
    return samples
            
    
