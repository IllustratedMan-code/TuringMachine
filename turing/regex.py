import re
# convert automata regexes to normal regex


def regex(automata_regex):
    # remove whitespace
    automata_regex = automata_regex.replace(" ", "")
    # dots do something else in normal regex
    automata_regex = automata_regex.replace(".", "")
    # replace plus with pipe
    automata_regex = automata_regex.replace("+", "|")
    # remove lambda (implied in automata style)
    automata_regex = automata_regex.replace("lambda", "")
    # add beginning and end of line (implied in automata style)
    automata_regex = "^" + automata_regex + "$"
    # kleene stars are the same, 1 and 0 are the same, parenthesis are the same
    # return fullmatch function to ensure it matches entire string
    return re.compile(automata_regex).fullmatch
