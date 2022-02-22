import expected_damage
from numpy import array

def test_read_files():
    test_depths, test_vuln_curve = expected_damage.read_files(
    assert expected_damage.read_files(

def test_find_depth():
    depth_arr = array([0.1,6.5,3,8.4])
    frac = 0.5
    assert expected_damage.find_depth(depth_arr, frac) == 2.25
