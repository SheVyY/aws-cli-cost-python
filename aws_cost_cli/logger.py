import sys

def print_fatal_error(error: str):
    sys.stderr.write(f"Error:\n{error}\n")
    sys.exit(1)

# We can expand this module with more logging utilities as needed.
