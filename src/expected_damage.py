## Program to estimate the cost of flooding on a risk in a
## specific postcode using depth data and a vulnerability curve.

from numpy import genfromtxt, logical_and

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
    # The paths to the data.
    depths_file = '../data/depths.csv'
    vulnerability_curve_file = '../data/vulnerability_curve.csv'

    # The fraction of the postcode area inundated by water.
    fraction_inundated = 0.75
    
    depths, vulnerability_curve = read_files(depths_file, vulnerability_curve_file)
    expected_depth = find_depth(depths, fraction_inundated)
    Damage = find_damage(expected_depth, vulnerability_curve, quiet = False)

if __name__ == "__main__":
    main()    
