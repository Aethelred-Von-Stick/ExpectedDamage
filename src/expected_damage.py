#!/usr/bin/env python3

## Program to estimate the cost of flooding on a risk in a
## specific postcode using depth data and a vulnerability curve.

import argparse
import errno
import os
import sys
from numpy import genfromtxt, logical_and

def get_args():
    # Create parser to read input paths.
    path_parser = argparse.ArgumentParser(prog='expected_damge',
                                          description = 'Calculate the expected damage to a risk in a specific postcode')

    # Add the arguments to be read in
    path_parser.add_argument('depth', type = str, help = 'Path to the file containing depth data')
    path_parser.add_argument('vulnerability', type = str, help = 'Path to the file containing the vulnerability curve')
    path_parser.add_argument('innundated', type = float, help = 'The fraction of the postcode innundated with water. Must be a value between 0 and 1')

    # Read the arguments to variablies
    args = path_parser.parse_args()
    depth_path = args.depth
    vulnerability_path = args.vulnerability
    innundated = args.innundated

    # Check whether the paths given exist
    depth_exists = os.path.isfile(depth_path)
    vulnerability_exists = os.path.isfile(vulnerability_path)
    if not depth_exists: 
        raise FileNotFoundError(
                os.strerror(errno.ENOENT), depth_path)
        sys.exit()
    elif not vulnerability_exists:
        raise FileNotFoundError(
                os.strerror(errno.ENOENT), vulnerability_path)
        sys.exit()

    # Check that the fraction innundated is between 0 and 1
    if not 0 <= innundated <= 1:
        raise ValueError('innundated must be between 0 and 1, not', innundated)
        sys.exit()

    return depth_path, vulnerability_path, innundated

def read_files(depths_f, vuln_curve_f):
    # Generate numpy arrays from the depth and vulnerability curve files.
    depths = genfromtxt(depths_f, skip_header = 1)
    vuln_curve = genfromtxt(vuln_curve_f, delimiter = ',', skip_header = 1)
    return depths, vuln_curve

def find_depth(depth_arr, fraction):
    # The depth data only contains non zero data points so
    # we need to account for areas which have no flooding to
    # estimate the depth of water at the risk.
    return depth_arr.mean() * fraction

def find_damage(exp_depth, vuln_curve, quiet = True):
    # first check that the expected depth lies within the vulnerability curve's validity
    if exp_depth <= vuln_curve[-1,1]:
        # Find the damage bin that the estimated depth lies in.
        Damage_index = logical_and(vuln_curve[:,0] < exp_depth, vuln_curve[:,1] >= exp_depth).nonzero()
        # Output the amount of damage corresponding to the estimated depth.
        Damage = vuln_curve[Damage_index,2].item()
        if quiet == False:
            print('The expected damage is £' + format(Damage, ".2f") + '.')
        return vuln_curve[Damage_index,2].item()
    else:
        Damage = vuln_curve[-1,2].item()
        if quiet == False:
            print("The expected depth lies outwith the validity of the vulnerability curve. Using highest estimate of £" + format(Damage, "2f") + ".")
        return Damage

def main():
    # Obtain the paths to the data and the fraction of the postcode innundated from the command line arguments.
    depths_file, vulnerability_curve_file, fraction_inundated = get_args() 

    depths, vulnerability_curve = read_files(depths_file, vulnerability_curve_file)
    expected_depth = find_depth(depths, fraction_inundated)
    Damage = find_damage(expected_depth, vulnerability_curve, quiet = False)

if __name__ == "__main__":
    main()    
