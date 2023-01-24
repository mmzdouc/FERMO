import pytest
import pandas as pd

from fermo.processing.calculate_feature_overlap import (
    prepare_pandas_tables,
    calc_mass_deviation,
    detect_sodium_adduct,
    detect_dimer_sodium_adduct,
    detect_trimer_adduct,
    detect_frst_isot_adduct,
    detect_scnd_isot_adduct,
    detect_thrd_isot_adduct,
    detect_fourth_isot_adduct,
    detect_fifth_isot_adduct,
    detect_double_first_isot_adduct,
    detect_double_second_isot_adduct,
    detect_double_third_isot_adduct,
    detect_double_fourth_isot_adduct,
    detect_double_fifth_isot_adduct,
    detect_first_isot_double_adduct,
    detect_iron_adduct,
    detect_dimer_dbl,
    calculate_feature_overlap,
    detect_ammonium,
    detect_potassium,
    detect_proton_plus_water,
    detect_proton_minus_water,
    )



# FIXTURES #

@pytest.fixture
def example_samples_dict_input():
    return {
        'sample_1' : pd.DataFrame(
                {
                'feature_ID' : [1,2,],
                'precursor_mz' : [1648.4547, 1510.4198],
                'retention_time' : [12.5, 12.7],
                'fwhm' : [0.1, 0.1],
                'intensity' : [1200, 1200],
                'rt_start' : [12.3, 12.5],
                'rt_stop' : [12.7, 12.9],
                'norm_intensity' : [1, 1],
                }
            )
        }

@pytest.fixture
def example_samples_dict_post_prepare_pandas_tables():
    return {
        'sample_1' : pd.DataFrame(
                {
                'feature_ID' : [1,2,],
                'precursor_mz' : [1648.4547, 1510.4198],
                'retention_time' : [12.5, 12.7],
                'fwhm' : [0.1, 0.1],
                'intensity' : [1200, 1200],
                'rt_start' : [12.3, 12.5],
                'rt_stop' : [12.7, 12.9],
                'norm_intensity' : [1, 1],
                'feature_collision' : [False, False],
                'feature_collision_list' : [[], []],
                'putative_adduct_detection' : [[], []],
                }
            )
        }

@pytest.fixture
def example_samples_dict_output():
    return {
        'sample_1' : pd.DataFrame(
                {
                'feature_ID' : [1,2,],
                'precursor_mz' : [1648.4547, 1510.4198],
                'retention_time' : [12.5, 12.7],
                'fwhm' : [0.1, 0.1],
                'intensity' : [1200, 1200],
                'rt_start' : [12.3, 12.5],
                'rt_stop' : [12.7, 12.9],
                'norm_intensity' : [1, 1],
                'feature_collision' : [True, True],
                'feature_collision_list' : [[2],[1]],
                'putative_adduct_detection' : [[],[]],
                }
            )
        }



# TESTS #


def test_prepare_pandas_tables(
    example_samples_dict_input,
    example_samples_dict_post_prepare_pandas_tables,
    ):
    '''Assert correct pandas table formatting'''
    result = prepare_pandas_tables(example_samples_dict_input)
    assert result['sample_1'].equals(
        example_samples_dict_post_prepare_pandas_tables['sample_1']
        )

def test_calc_mass_deviation():
    '''Assert mass deviation - authentic data'''
    assert calc_mass_deviation(415.2098, 415.2098,) == 0

def test_detect_sodium_adduct():
    '''Assert sodium adduct - authentic data'''
    assert detect_sodium_adduct(415.2098, 437.1912, 20)

def test_detect_dimer_sodium_adduct():
    '''Assert dimer sodium adduct - calculated data'''
    assert detect_dimer_sodium_adduct(415.2098, 851.39427, 20)

def test_detect_trimer_adduct():
    '''Assert trimer adduct - calculated data siomycin B'''
    assert detect_trimer_adduct(1510.4198, 504.1447, 20)

def test_detect_frst_isot_adduct():
    '''Assert single charged +1 isotope - authentic data siomycin A'''
    assert detect_frst_isot_adduct(1648.4547, 1649.4578, 20)

def test_detect_scnd_isot_adduct():
    '''Assert single charged +2 isotope - calculated data siomycin A'''
    assert detect_scnd_isot_adduct(1648.4547, 1650.4653, 20)

def test_detect_thrd_isot_adduct():
    '''Assert single charged +3 isotope - authentic data siomycin A'''
    assert detect_thrd_isot_adduct(1648.4547, 1651.4547, 20)

def test_detect_fourth_isot_adduct():
    '''Assert single charged +4 isotope - authentic data siomycin A'''
    assert detect_fourth_isot_adduct(1648.4547, 1652.4539, 20)

def test_detect_fifth_isot_adduct():
    '''Assert single charged +5 isotope - calculated data siomycin A'''
    assert detect_fifth_isot_adduct(1648.4547, 1653.4754, 20)

def test_detect_double_first_isot_adduct():
    '''Assert double charged +1 isotope - calculated data siomycin A'''
    assert detect_double_first_isot_adduct(1648.4547, 825.2326, 20)

def test_detect_double_second_isot_adduct():
    '''Assert double charged +2 isotope - calculated data siomycin A'''
    assert detect_double_second_isot_adduct(1648.4547, 825.7343, 20)

def test_detect_double_third_isot_adduct():
    '''Assert double charged +3 isotope - calculated data siomycin A'''
    assert detect_double_third_isot_adduct(1648.4547, 826.2360, 20)

def test_detect_double_fourth_isot_adduct():
    '''Assert double charged +4 isotope - calculated data siomycin A'''
    assert detect_double_fourth_isot_adduct(1648.4547, 826.7377, 20)

def test_detect_double_fifth_isot_adduct():
    '''Assert double charged +5 isotope - calculated data siomycin A'''
    assert detect_double_fifth_isot_adduct(1648.4547, 827.2393, 20)

def test_detect_first_isot_double_adduct():
    '''Assert +1 isotope of double protonated ion - calculated data siomycin B'''
    assert detect_first_isot_double_adduct(790.2263, 790.7269, 20)

def test_detect_iron_adduct():
    '''Assert 56^Fe adduct - authentic data siomycin A'''
    assert detect_iron_adduct(843.4772, 896.3883, 20)

def test_detect_dimer_dbl():
    '''Assert dimer and double charged ions - authentic data siomycin A'''
    assert detect_dimer_dbl(1510.4198, 755.7153, 20)

def test_detect_ammonium():
    '''Assert ammonium adduct - authentic data cholic acid (JGI)'''
    assert detect_ammonium(409.29477, 426.321, 20)

def test_detect_potassium():
    '''Assert potassium adduct - authentic data cholic acid (MoNA)'''
    assert detect_potassium(409.29477, 447.251, 20)

def test_detect_proton_plus_water():
    '''Assert proton+water adduct - calculated data cholic acid '''
    assert detect_proton_plus_water(409.29477, 427.30588, 20)

def test_detect_proton_minus_water():
    '''Assert proton-water adduct - authentic data cholic acid (JGI)'''
    assert detect_proton_minus_water(409.29477, 391.284, 20)






def test_calculate_feature_overlap(
    example_samples_dict_post_prepare_pandas_tables,
    example_samples_dict_output,
    example_feature_dict_base,
    ):
    '''Assert overlap calculation. feature_dicts not modified - no assert'''
    samples_mod, feature_dicts = calculate_feature_overlap(
        example_samples_dict_post_prepare_pandas_tables,
        20,
        example_feature_dict_base,
        )
    assert samples_mod['sample_1'].equals(
        example_samples_dict_output['sample_1']
        )

