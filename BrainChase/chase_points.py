import simplekml
import math
import sys


#-------------------------------------------------------------------------------
def calculate_coordinate(origin: [float, float], range: float, fwd_az) -> [float, float]:
  """Calculate a forward coordinate given a origin, range and forward azimuth

  Forward coordinate calculation is based on Ed William's Aviation Formulary.
  The earth radius is based on the WGS84 mean ellipsoid as defined by
  r = (2a + b)/3, were a is the semi-major axis and b is the semi-minor axis.

  Inputs:

    origin: [float, float] - origin latitude and longitude in radians
    range:  float - range to the destination in meters
    fwd_az: float - forward azimuth in radians

  Outputs:

    [float, float] - Destination coordinate in radians

  """

  # Convert to range to angular distance.
  # angular distance = range / mean earth radius

  ang_dist = range / ((2.0 * 6378137.0 + 6356752.314245) / 3.0)

  # Calculate the forward latitude and longitude

  lat = math.asin(math.sin(origin[0]) * math.cos(ang_dist) + \
                  math.cos(origin[0]) * math.sin(ang_dist) * math.cos(fwd_az))

  lon = origin[1] + math.atan2(math.sin(fwd_az) * math.sin(ang_dist) * math.cos(origin[0]), \
                    math.cos(ang_dist) - math.sin(origin[0]) * math.sin(lat))

  return [lat, lon]


#-------------------------------------------------------------------------------
def chase_points(file_in: str) -> None:
  """ BrainChase support tool, calculates lat/lon coordinates from range and bearing.

  Given an input file containing a lat/lon origin and a series of range, bearing
  pairs, this tool will calculate the coordinates for each of the pairs.  The
  output is dumped to standard out and to a GoogleEarth KML file with the same
  root name as the input file.

  The input file is an ASCII text (.txt) file with the following format.  The
  first line of the file is the start point.  The start point needs to be in
  decimal degrees where N/E are positive and S/W are negative.  Range, bearing
  pairs should be in the form 'range @ bearing'.  Where the range is in
  kilometers and the bearing is in degrees (0-360).   One range, bearing pair
  per line, empty lines are allowed.  A range, bearing pair can be commented out
  by placing a '#' character in the first column of a line.

  Example (NOTE: first range, bearing is commented out):

    30.284491, -97.710238

    #422.50 @  18.92
    526.50 @ 313.68
    341.50 @ 250.27

  Inputs:

    file_in: str - Name of the input file, see format specification above.

  Outputs:

    return: None

    Calculated points are printed to standard out.

    Calculated points are also output to a kml file of the same root name as the
    input file.

  """
  kml = simplekml.Kml()

  coord   = [0.0, 0.0]  # Current lat/lon
  point   = 0           # Way point sequence number
  range   = 0.0         # Range in meters
  bearing = 0.0         # Bearing in radians

  # Read in the file
  with open(file_in,'r') as f:
    lines = f.read().split('\n')

  # Process the file
  for line in lines:

      # The first line in the file is the origin.
      # lat, lon in decimal degrees; +/- for N/S and E/W.

      if point == 0:

        # Convert input from degrees to radians

        origin   = line.split(',')
        coord[0] = math.radians(float(origin[0]))
        coord[1] = math.radians(float(origin[1]))

      else:

        # If the line is empty or starts with a comment ('#')
        # skip the line.

        if not line or line.isspace():
          continue

        if line[0] == '#':
          continue

        range_bearing = line.split('@')

        # Convert range from kilometers to meters and bearing from
        # degrees to radians.

        range   = float(range_bearing[0]) * 1000.0
        bearing = math.radians(float(range_bearing[1]))

        coord = calculate_coordinate(coord, range, bearing)

      print('PT: {:02}: {:10.6f}, {:10.6f}'.format(point, math.degrees(coord[0]), math.degrees(coord[1])))

      kml.newpoint(name='PT: {:02}'.format(point), \
                   coords=[(math.degrees(coord[1]), math.degrees(coord[0]))], \
                   description='{:.2f} km @ {:.2f}\N{DEGREE SIGN} from last point.'.format(range * 0.001, math.degrees(bearing)))
      point += 1

  kml.save(file_in.replace('.txt', '.kml'))


#-------------------------------------------------------------------------------
if __name__ == '__main__':

  if len(sys.argv) != 2:
    print("USAGE: python chase_points.py [input_file]")

  chase_points(sys.argv[1])
