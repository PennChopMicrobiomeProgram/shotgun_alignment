import sys

for line in sys.stdin:
    if line.startswith(">"):
            desc = line.split()[0]
            sys.stdout.write(desc)
            sys.stdout.write("\n")
    else:
        sys.stdout.write(line)
