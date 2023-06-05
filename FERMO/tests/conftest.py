import pytest
import pandas as pd
import numpy as np


@pytest.fixture
def example_dict_params():
    return {
        'mass_dev_ppm': 20,
        'min_nr_ms2': 8,
        'bioact_fact': 10,
        'column_ret_fact': 10,
        'spectral_sim_tol': 0.1,
        'spec_sim_score_cutoff': 0.8,
        'max_nr_links_ss': 10,
        'min_nr_matched_peaks': 8,
        'ms2query': False,
        'spec_sim_net_alg': 'modified_cosine',
        'ms2query_blank_annotation': False,
        'relative_intensity_filter_range': [0, 1],
        'ms2query_filter_range': [0, 1]
        }

@pytest.fixture
def example_peaktable_mzmine3():
    return pd.DataFrame(
        {
        'feature_ID' : [1,2,],
        'intensity_range:min' : [1200,1200,],
        'intensity_range:max' : [48000,16000,],
        'height' : [48000,16000,],
        'area' : [16000,3600,],
        'mz_range:min' : [824.7352,1648.4495,],
        'mz_range:max' : [824.7404,1648.4598,],
        'fragment_scans' : [19,5,],
        'rt_range:min' : [14.87,14.93,],
        'rt_range:max' : [15.65,15.38,],
        'charge' : [2,2,],
        'precursor_mz' : [824.7379,1648.4547,],
        'retention_time' : [15.26,15.16,],
        'datafile:file1.mzXML:fwhm' : [0.32,0.2,],
        'datafile:file1.mzXML:intensity_range:min' : [1200,1200,],
        'datafile:file1.mzXML:intensity_range:max' : [48000,16000,],
        'datafile:file1.mzXML:fragment_scans' : [19,5,],
        'datafile:file1.mzXML:rt_range:min' : [14.87,14.93,],
        'datafile:file1.mzXML:rt_range:max' : [15.65,15.38,],
        'datafile:file1.mzXML:feature_state' : ['DETECTED','DETECTED',],
        'datafile:file1.mzXML:rt' : [15.26,15.16,],
        'datafile:file1.mzXML:mz' : [824.7379,1648.4547,],
        'datafile:file1.mzXML:tailing_factor' : [1.54,1.92,],
        'datafile:file1.mzXML:height' : [48000,16000,],
        'datafile:file1.mzXML:area' : [16000,3600,],
        'datafile:file1.mzXML:mz_range:min' : [824.7352,1648.4495,],
        'datafile:file1.mzXML:mz_range:max' : [824.7404,1648.4598,],
        'datafile:file1.mzXML:asymmetry_factor' : [2.03,2.07,],
        'datafile:file1.mzXML:charge' : [2,2,],
        'datafile:file1.mzXML:isotopes' : [5,5,],
        }
    )

@pytest.fixture
def example_ms2_dict():
    mgf = {'1': [[440.0516, 442.0856, 445.5853, 453.1776, 459.0728, 481.0847, 503.0941, 529.1122, 530.1174, 782.2146, 815.0875], [220, 100, 110, 100, 1800, 110, 160, 740, 170, 180, 100]], '2': [[440.0516, 442.0856, 445.5853, 453.1776, 459.0728, 481.0847, 503.0941, 529.1122, 530.1174, 782.2146, 815.0875], [220, 100, 110, 100, 1800, 110, 160, 740, 170, 180, 100]]}
    ms2_dict = dict()
    for ID in mgf:
        ms2_dict[int(ID)] = [
            np.array(mgf[ID][0], dtype=float),
            np.array(mgf[ID][1], dtype=float),
            ]
    return ms2_dict

@pytest.fixture
def example_metadata():
    return pd.DataFrame({
        'sample_name' : ['file1.mzXML',],
        'attribute' : ['group1',],
    })

@pytest.fixture
def example_quant_bio():
    return pd.DataFrame({
        'sample_name' : ['file1.mzXML',],
        'quant_data' : [1],
    })

@pytest.fixture
def example_quant_bio_orig():
    return pd.DataFrame({
        'sample_name' : ['file1.mzXML',],
        'quant_data' : [100],
    })
