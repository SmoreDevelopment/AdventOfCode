import argparse
import re

# ------------------------------------------------------------------------------
def validate_year(type: str, year: str, part_two: bool) -> bool:
  """ Validate birth year
  """

  schemes = { 'byr': ['(byr:)\s*(\d4)', 1920, 2002],
              'iyr': ['(iyr:)\s*(\d4)', 1920, 2002],
              'eyr': ['(eyr:)\s*(\d4)', 1920, 2002],  }

  valid = False

  result = re.search(rschemes[type][0], year)

  if result.group(1):
    if not part_two:
      valid = True
    else:
      if schemes[type][1] <= year_int int(result.group(2)) <= schemes[type][2]:
        valid = True

  return valid

# ------------------------------------------------------------------------------
def validate_passports(filename: str, part_two: bool) -> None:
  """ Validates a list of pass ports

  The automatic passport scanners are slow because they're having trouble
  detecting which passports have all required fields. The expected fields are as
  follows:

      byr (Birth Year)
      iyr (Issue Year)
      eyr (Expiration Year)
      hgt (Height)
      hcl (Hair Color)
      ecl (Eye Color)
      pid (Passport ID)
      cid (Country ID) (Optional)

  Each passport is represented as a sequence of key:value pairs separated by
  spaces or newlines. Passports are separated by blank lines.

  Inputs:

    filename: str - Name of the input file

    part_two: bool - Boolean flag to enable part two solution to the puzzle

  Outputs:

    None
  """

  with open(filename, 'r') as f:
    data = f.read().split('\n\n')

  valid_passports = 0

  for passport in data:

    required_fields = 0

    if validate_year('byr', passport, part_two):   required_fields += 1  # Birth Year
    if validate_year('iyr', passport, part_two):   required_fields += 1  # Issue Year
    if validate_year('eyr', passport, part_two):   required_fields += 1  # Expiration Year
    if re.search(r'hgt:', passport):   required_fields += 1  # Height
    if re.search(r'hcl:', passport):   required_fields += 1  # Hair Color
    if re.search(r'ecl:', passport):   required_fields += 1  # Eye Color
    if re.search(r'pid:', passport):   required_fields += 1  # Passport ID
    required_fields += 1                                     # Country ID (Don't Care)

    if required_fields == 8:
      valid_passports += 1

  print('Valid Passports:', valid_passports)


# ------------------------------------------------------------------------------
if __name__ == '__main__':

  parser = argparse.ArgumentParser(description='Advent Of Code Challenge 2020 - Day 4, Validate passports.')
  parser.add_argument('file_in', type=str, metavar='input_filename', help='Name of input file.')
  parser.add_argument('--part_two', '-p', action='store_true', help='Solve for part 2 of the puzzle.')

  args = parser.parse_args()

  validate_passports(args.file_in, args.part_two)