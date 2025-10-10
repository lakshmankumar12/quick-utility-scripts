import sys
import json
import ast
from pprint import pprint

def parse_input(input_data):
    try:
        # Try parsing as JSON
        return json.loads(input_data)
    except json.JSONDecodeError:
        try:
            # Fallback to literal_eval
            return ast.literal_eval(input_data)
        except (ValueError, SyntaxError) as e:
            raise ValueError(f"Failed to parse input: {e}")

def main():

    if len(sys.argv) > 1:
        # Read from file if filename provided
        filename = sys.argv[1]
        try:
            with open(filename, 'r') as f:
                input_data = f.read()
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found", file=sys.stderr)
            sys.exit(1)
        except IOError as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Fall back to stdin
        input_data = sys.stdin.read()

    try:
        parsed = parse_input(input_data)
        pprint(parsed)
    except Exception as e:
        print(f"Error: {type(e).__name__}:{e}", file=sys.stderr)

if __name__ == "__main__":
    main()
