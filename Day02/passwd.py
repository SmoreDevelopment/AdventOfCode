import argparse
import re


# ------------------------------------------------------------------------------
def passwd(filename: str, alt_schema: bool) -> None:
  """Find all the valid passwords within a file according to the defined policy.

  Example passwords:

  1-3 a: abcde
  1-3 b: cdefg
  2-9 c: ccccccccc

  1st Policy:

  Each line gives the password policy and then the password. The password policy
  indicates the lowest and highest number of times a given letter must appear
  for the password to be valid. For example, 1-3 a means that the password must
  contain a at least 1 time and at most 3 times.

  In the above example, 2 passwords are valid. The middle password, cdefg, is
  not; it contains no instances of b, but needs at least 1. The first and third
  passwords are valid: they contain one a or nine c, both within the limits of
  their respective policies.


  2nd Policy:

  Each policy describes two positions in the password, where 1 means the first
  character, 2 means the second character, and so on. Exactly one of these
  positions must contain the given letter. Other occurrences of the letter are
  irrelevant for the purposes of policy enforcement.

  Given the same example list from above:

    1-3 a: abcde is valid: position 1 contains a and position 3 does not.
    1-3 b: cdefg is invalid: neither position 1 nor position 3 contains b.
    2-9 c: ccccccccc is invalid: both position 2 and position 9 contain c.

  Inputs:

    filename: str - Name of the password file to be processed

  Outputs:

    None
  """

  regex = r'(\d*)-(\d*) (\w): (\w*)'
  valid_passwords = 0

  with open(filename, 'r') as f:
    for line in f:

      entry = re.search(regex, line)

      required_min  = int(entry.group(1))
      required_max  = int(entry.group(2))
      required_char = entry.group(3)
      password      = entry.group(4)

      # ------------------------------------------------------------------------
      if alt_schema:

        if (password[required_min-1] == required_char) ^ \
           (password[required_max-1] == required_char):
          print(line.rstrip('\n'))
          valid_passwords += 1

      # ------------------------------------------------------------------------
      else:

        count = password.count(required_char)
        if required_min <= count and count <= required_max:
          print(line.rstrip('\n'))
          valid_passwords += 1

  print(valid_passwords)



# ------------------------------------------------------------------------------
if __name__ == '__main__':

  parser = argparse.ArgumentParser(description='Advent Of Code Challenge 2020 - Day 2, Find valid passwords.')
  parser.add_argument('file_in', type=str, metavar='input_filename', help='Name of input file.')
  parser.add_argument('--alt', '-a', action='store_true', help='Use alternate password schema.')

  args = parser.parse_args()

  passwd(args.file_in, args.alt)