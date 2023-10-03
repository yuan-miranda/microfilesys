import argparse

parser = argparse.ArgumentParser(description='Example command-line application')

# Required argument
parser.add_argument('required_argument', help='A required argument')

# Optional argument
parser.add_argument('--optional_argument', help='An optional argument')

# Choices for an argument
parser.add_argument('--choice', choices=['option1', 'option2'], help='Pick one of the options')

args = parser.parse_args()

print('Required argument:', args.required_argument)
print('Optional argument:', args.optional_argument)
print('Chosen option:', args.choice)
