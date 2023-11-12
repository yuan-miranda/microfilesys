import urparser

parser = urparser.Urparser()
parser.add_argument('-i', str, description="input value", default_value=20)

ui = input("enter command: ").split()
parser.parse_argument(ui)

if parser.show_help:
    parser.print_help()

print(parser.get_value('-i'))