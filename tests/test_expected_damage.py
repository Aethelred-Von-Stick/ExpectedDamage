import pytest
import os
import numpy as np
import expected_damage

def test_read_files():
    # Test that the outputs of read_files are numpy ndarrays
    path_to_test_dir = os.path.dirname(os.path.realpath(__file__))
    path_to_depths = os.path.join(path_to_test_dir, "data", "depths.csv")
    path_to_vulnerability_curve = os.path.join(path_to_test_dir, "data", "vulnerability_curve.csv")
    test_depths, test_vuln_curve = expected_damage.read_files(path_to_depths,path_to_vulnerability_curve)
    assert str(type(test_depths)) == "<class 'numpy.ndarray'>" 
    assert str(type(test_vuln_curve)) == "<class 'numpy.ndarray'>"

def test_find_depth():
    # Check that find_depth is giving the correct expectation value
    depth_arr = np.array([0.1,6.5,3,8.4])
    frac = 0.5
    assert expected_damage.find_depth(depth_arr, frac) == 2.25

# Parametrize the test inputs to run one test within the limits of the vulnerability curve and one outwith it.
@pytest.mark.parametrize("test_input,expected", [(5.5, 60000), (15.6, 100000)])
def test_find_damage(test_input, expected):
    # Create a vulnerability curve array
    low_edges = np.arange(0,10)
    high_edges = np.arange(1,11)
    Damages = np.linspace(10000,100000,10)
    vuln_curve = np.vstack((low_edges, high_edges, Damages)).T
    
    # Check that the damage value is as expected
    assert expected_damage.find_damage(test_input, vuln_curve, quiet=True) == expected 


