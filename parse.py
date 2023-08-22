num_variables = int()
num_clauses = int()
def parse_file(filename):
    target = open(filename)
    cnf = list()
    cnf.append(list())
    for line in target.readlines(): 
    # faster than to readline() individually. of course this limits the file size. But a file in the range of MBs should be fine
        clause = line.split()
        if len(clause) != 0 and clause[0] != "p" and clause[0] != "c":
            for literal in clause:
                literal_value = int(literal)
                if literal_value == 0:
                    cnf.append(list())
                else:
                    # not at the end, then append variable inside the last list!
                    cnf[-1].append(literal_value)
        elif len(clause) != 0 and clause[0] == "p":
             num_variables = int(clause[2])
             num_clauses = int(clause[3])
    assert len(cnf[-1]) == 0
    cnf.pop()
    return cnf, num_variables, num_clauses