"""
Unit and regression test for the vasp_postprocess package.
"""

# Import package, test suite, and other packages as needed
import vasp_postprocess
import pytest
import sys

def test_vasp_postprocess_imported():
    """Sample test, will always pass so long as import statement worked"""
    assert "vasp_postprocess" in sys.modules
