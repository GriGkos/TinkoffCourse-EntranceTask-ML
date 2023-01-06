import numpy
import token
import tokenize
import argparse


# remove comments from the file
# and rewrite it to one line
def do_file(fname):
    source = open(fname)
    mod = open(fname + "(strip)", "w")

    prev_toktype = token.INDENT
    last_lineno = -1
    last_col = 0

    tokgen = tokenize.generate_tokens(source.readline)
    for toktype, ttext, (slineno, scol), (elineno, ecol), ltext in tokgen:
        if slineno > last_lineno:
            last_col = 0
        if scol > last_col:
            mod.write(" ")
        if toktype == token.STRING and prev_toktype == token.INDENT:
            mod.write("")
        elif toktype == tokenize.COMMENT:
            mod.write("")
        else:
            if ttext != "\n":
                mod.write(ttext.strip())
        prev_toktype = toktype
        last_col = ecol
        last_lineno = elineno


def levenshtein_distance(token1, token2):
    distances = numpy.zeros((len(token1) + 1, len(token2) + 1))

    for t1 in range(len(token1) + 1):
        distances[t1][0] = t1

    for t2 in range(len(token2) + 1):
        distances[0][t2] = t2

    for t1 in range(1, len(token1) + 1):
        for t2 in range(1, len(token2) + 1):
            if token1[t1 - 1] == token2[t2 - 1]:
                distances[t1][t2] = distances[t1 - 1][t2 - 1]
            else:
                a = distances[t1][t2 - 1]
                b = distances[t1 - 1][t2]
                c = distances[t1 - 1][t2 - 1]

                if a <= b and a <= c:
                    distances[t1][t2] = a + 1
                elif b <= a and b <= c:
                    distances[t1][t2] = b + 1
                else:
                    distances[t1][t2] = c + 1

    return distances[len(token1)][len(token2)]


def do_all():
    parser = argparse.ArgumentParser(description='Compare two texts')
    parser.add_argument('indir', type=str, help='Input dir to texts')
    parser.add_argument('outdir', type=str, help='Output dir for saving result')
    args = parser.parse_args()

    inp = open(args.indir, 'r')
    out = open(args.outdir, 'w')

    for line in inp.readlines():
        do_file(line.split()[0].strip())
        do_file(line.split()[1].strip())

        file1 = open(line.split()[0].strip() + "(strip)", 'r')
        file2 = open(line.split()[1].strip() + "(strip)", 'r')

        file1text = file1.read()
        file2text = file2.read()

        out.write(str(levenshtein_distance(file1text, file2text) / len(file2text)) + "\n")

    inp.close()
    out.close()


if __name__ == '__main__':
    do_all()
