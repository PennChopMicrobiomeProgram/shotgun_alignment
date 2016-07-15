import sys

for line in sys.stdin:
    line = line.rstrip()
    if line.startswith(">"):
        line = line.split()[0]
    sys.stdout.write(line)
    sys.stdout.write("\n")
