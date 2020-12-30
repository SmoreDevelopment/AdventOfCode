import argparse


# ------------------------------------------------------------------------------
def tree_collisions(filename: str, alt_route: bool, verbose: bool) -> int:

  tree_collisions = 0
  map_width       = 0
  right_advance   = 3
  position        = 0


  with open(filename, 'r') as f:
    for line_num, line in enumerate(f):
      obstacle_map = line.rstrip('\n')

      # ------------------------------------------------------------------------
      if not map_width:
        map_width = len(obstacle_map)

      # ------------------------------------------------------------------------
      if '#' == obstacle_map[position]:
        tree_collisions += 1

      # ------------------------------------------------------------------------
      if verbose:
        collision_map = []
        for i, char in enumerate(obstacle_map):
          if i == position:
            collision_map.append('X' if '#' == obstacle_map[position] else 'O')
          else:
            collision_map.append(char)

        print('{:03d},{:03d}: {}'.format(line_num+1, position, ''.join(collision_map)))

      # ------------------------------------------------------------------------
      position += right_advance - (map_width if (position + right_advance >= map_width) else 0)

  print('Tree collisions:', tree_collisions)

# ------------------------------------------------------------------------------
if __name__ == '__main__':

  parser = argparse.ArgumentParser(description='Advent Of Code Challenge 2020 - Day 3, Calculate number of tree collisions for Toboggan run.')
  parser.add_argument('file_in', type=str, metavar='input_filename', help='Name of input file.')
  parser.add_argument('--alt', '-a', action='store_true', help='Use alternate password schema.')
  parser.add_argument('--verbose', '-v', action='store_true', help='Display the collision map.')

  args = parser.parse_args()

  tree_collisions(args.file_in, args.alt, args.verbose)