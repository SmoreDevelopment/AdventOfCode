import argparse

# ------------------------------------------------------------------------------
def collision_checker(obstacle_map: list, dx: int, dy: int, verbose: bool) -> int:
  """ Lool for tree collisions along the specified path, return the number of collisions

  Inputs:

    obstacle_map: list - The grid map of obstacles:
                         '.' represents a clear space
                         '#' represents a tree

    dx: int - Amount of right run on the path

    dy: int - Amount of down run on the path

    verbose:  bool - Print the collision map for debugging purposes

  Outputs:

    int - Total number of tree collisions detected along the tobaggon path
  """

  collisions = 0
  width      = len(obstacle_map[0])
  x          = 0

  for line_num, line in enumerate(obstacle_map):

    if line_num % dy:
      continue

    # ------------------------------------------------------------------------
    if '#' == line[x]:
      collisions += 1

    # ------------------------------------------------------------------------
    if verbose:
      collision_map = []
      for i, char in enumerate(line):
        if i == x:
          collision_map.append('X' if '#' == line[x] else 'O')
        else:
          collision_map.append(char)

      print('{:03d},{:03d}: {}'.format(line_num+1, x, ''.join(collision_map)))

    # ------------------------------------------------------------------------
    x = (x + dx) % width

  return collisions


# ------------------------------------------------------------------------------
def traverse_route(filename: str, part_two: bool, verbose: bool) -> None:
  """ Load the input file and traverse the route(s) looking for tree collisions.

  Inputs:

    filename: str - Name of the password file to be processed

    part_two: bool - Calculate the solution for part 2 of the puzzle if true

    verbose:  bool - Print the collision map for debugging purposes

  Outputs:

    None
  """

  with open(filename, 'r') as f:
    data = f.read().splitlines()

  # For some reason we are multiplying instead of summing the collisions
  # for part 2 of the puzzle, so we will default this to 1.
  collisions = 1

  if not part_two:
    collisions = collision_checker(data, 3, 1, verbose)

  else:
    routes = ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2))

    for route in routes:
      collisions *= collision_checker(data, route[0], route[1], verbose)


  print('Tree collisions:', collisions)

# ------------------------------------------------------------------------------
if __name__ == '__main__':

  parser = argparse.ArgumentParser(description='Advent Of Code Challenge 2020 - Day 3, Calculate number of tree collisions for Toboggan run.')
  parser.add_argument('file_in', type=str, metavar='input_filename', help='Name of input file.')
  parser.add_argument('--part_two', '-p', action='store_true', help='Solve for part 2 of the puzzle.')
  parser.add_argument('--verbose', '-v', action='store_true', help='Display the collision map.')

  args = parser.parse_args()

  traverse_route(args.file_in, args.part_two, args.verbose)