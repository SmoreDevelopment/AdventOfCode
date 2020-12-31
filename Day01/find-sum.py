#!/bin/python3
import argparse
import numpy as np
import itertools

# ------------------------------------------------------------------------------
def find_sum(filename: str, target_sum: int, num_to_total: int) -> None:
  """ Find a specified number of values that sum to the total provided and calculate the product of them.

  Description:  This function will open a file and scan it, looking for a pair
                of numbers whose sum is equal to target_sum.  It will then return
                the product of those two numbers.

  Input:        filename: str - Input filename

                target_sum: int - Sum total that we are searching for in the report.

                num_to_total: int - The number of values to use in calculating the sum.

  Outputs:      None
  """

  # Load the inputs

  if 2 == num_to_total:

    data = np.loadtxt(filename)
    compliment = target_sum - data

    combo = np.intersect1d(data, compliment)


  else:

    data = []

    with open(filename, 'r') as f:
      for line in f:
        data.append(int(line))

    for combo in itertools.combinations(data, num_to_total):
      if target_sum == sum(combo):
        break


  print('Combination = ', combo, 'Product = ', np.prod(combo))




# ------------------------------------------------------------------------------
def validate_num(value: int) -> int:
  """ Validate the value passed in with the --num option.

  Description:  Validates the --num option values.  The value must be between
                2 and 10 (arbitrarily bounded upper limit.

  Input:        value: int - Value to be validated.

  Outputs:      int - Validated value
  """

  ivalue = int(value)
  if 2 > ivalue or 10 < ivalue:
    raise argparse.ArgumentTypeError(value, 'is an invalid option.  Must be an integer between 2 and 10')
  return ivalue


# ------------------------------------------------------------------------------
if __name__ == '__main__':

  parser = argparse.ArgumentParser(description='Advent Of Code Challenge 2020 - Day 1, Find 2 numbers that sum 2020 and output the product of the two.')
  parser.add_argument('file_in', type=str, metavar='input_filename', help='Name of input file.')
  parser.add_argument('--sum', '-s', type=int, metavar='sum', default='2020', help='Alternate sum value (default is 2020).')
  parser.add_argument('--num', '-n', type=validate_num, metavar='number', default='2', help='Number of values to sum`')

  args = parser.parse_args()

  find_sum(args.file_in, args.sum, args.num)