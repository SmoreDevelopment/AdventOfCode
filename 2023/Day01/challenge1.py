# Read in the input file
with open('input.txt', 'r') as file_in:

  lines = file_in.readlines()

numbers = []

# Loop over each line in the file.
for line in lines:

  found_numbers = []
  number_as_string = []

  # Loop over each character in a line.
  for character in line:

    # If the character is a digit, add to our list of found numbers
    if character.isdigit():

      found_numbers.append(character)

  number_as_string = found_numbers[0] + found_numbers[len(found_numbers) - 1]

  numbers.append(int(number_as_string))

our_sum = sum(numbers)

print(numbers)
print(our_sum)

