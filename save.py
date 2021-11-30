import main
import sys

if len(sys.argv) < 3:
    print("Usage: python3 save.py <image in> <text out>")
    sys.exit(1)

with open(sys.argv[2], 'w') as f:
    f.write(main.render(sys.argv[1]))
