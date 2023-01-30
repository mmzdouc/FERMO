import pytest

from fermo.processing.read_from_metadata_table import read_from_metadata_table

def test_read_from_metadata_table(example_metadata):
    '''Assert sample grouping'''
    
    assert (
        read_from_metadata_table(example_metadata, None,)
        ==
        {'GENERAL' : set()}
    )
    
    assert (
        read_from_metadata_table(example_metadata, 'filename',)
        ==
        {
            'GENERAL' : set(),
            'group1' : set(['file1.mzXML']),
        }
    )
