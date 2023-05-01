import turing
states = {
    # copy zero to end
    "S": {
        "transitions": [
            ("1", "1", "->", "S"),
            ("0", "0", "->", "S"),
            (" ", "0", "<-", "COPY 1")
        ],
    },
    # go back to beginning and copy each 1 from the first number to the end
    # go back
    "COPY 1": {
        "transitions": [
            ("1", "1", "<-", "COPY 1"),
            ("0", "0", "<-", "COPY 1"),
            (" ", " ", "->", "COPY 2")
        ],
        "subgraph": "COPY"
    },
    # read 1
    "COPY 2": {
        "transitions": [
            ("1", "X", "->", "COPY 3"),
            ("0", "0", "->", "MOD 1"),
        ],
        "subgraph": "COPY"
    },
    # copy 1 to end
    "COPY 3": {
        "transitions": [
            ("1", "1", "->", "COPY 3"),
            ("0", "0", "->", "COPY 3"),
            (" ", "1", "<-", "COPY 4"),
        ],
        "subgraph": "COPY"
    },
    "COPY 4": {
        "transitions": [
            ("1", "1", "<-", "COPY 4"),
            ("0", "0", "<-", "COPY 4"),
            ("X", "X", "->", "COPY 2"),
        ],
        "subgraph": "COPY"
    },
    # calculate the modulus
    # change 1 to Y
    "MOD 1": {
        "transitions": [
            ("1", "Y", "->", "MOD 2"),
            ("0", "0", "->", "N>M 1"),
        ],
        "subgraph": "MOD"
    },
    # go to end
    "MOD 2": {
        "transitions": [
            ("1", "1", "->", "MOD 2"),
            ("0", "0", "->", "MOD 2"),
            ("X", "X", "->", "MOD 2"),
            (" ", " ", "<-", "MOD 3"),
        ],
        "subgraph": "MOD"
    },
    # change 1 to X
    "MOD 3": {
        "transitions": [
            ("1", "X", "<-", "MOD 4"),
            ("X", "X", "<-", "MOD 3"),
            ("0", "0", "->", "M>N 1"),
        ],
        "subgraph": "MOD"
    },
    # Go to Y
    "MOD 4": {
        "transitions": [
            ("Y", "Y", "->", "MOD 1"),
            ("0", "0", "<-", "MOD 4"),
            ("1", "1", "<-", "MOD 4"),
        ],
        "subgraph": "MOD"
    },
    "N>M 1": {
        "transitions": [
            ("1", "1", "->", "N>M 1"),
            ("X", "X", "->", "N>M 1"),
            (" ", " ", "<-", "N>M 2"),
        ],
        "subgraph": "N>M"
    },
    "N>M 2": {
        "transitions": [
            ("X", " ", "<-", "N>M 2"),
            ("1", "1", "<-", "N>M 3"),
            ("0", " ", "<-", "END 1"),
        ],
        "subgraph": "N>M"
    },
    "N>M 3": {
        "transitions": [
            ("0", "0", "<-", "N>M 3"),
            ("1", "1", "<-", "N>M 3"),
            ("X", "X", "<-", "N>M 3"),
            ("Y", "1", "<-", "N>M 3"),
            (" ", " ", "->", "N>M 4"),
        ],
        "subgraph": "N>M"
    },
    "N>M 4": {
        "transitions": [
            ("X", " ", "->", "N>M 4"),
            ("0", " ", "->", "S"),
        ],
        "subgraph": "N>M"
    },
    "M>N 1": {
        "transitions": [
            ("X", "X", "->", "M>N 1"),
            (" ", " ", "<-", "M>N 2"),

        ],
        "subgraph": "M>N"
    },
    "M>N 2": {
        "transitions": [
            ("X", "1", "<-", "M>N 2"),
            ("Y", "1", "<-", "M>N 2"),
            ("1", "1", "<-", "M>N 2"),
            ("0", "0", "<-", "M>N 2"),
            (" ", " ", "->", "M>N 3"),

        ],
        "subgraph": "M>N"
    },
    "M>N 3": {
        "transitions": [
            ("0", " ", "->", "S"),
            ("1", " ", "->", "M>N 3"),

        ],
        "subgraph": "M>N"
    },
    "END 1": {
        "transitions": [
            ("Y", "1", "<-", "END 1"),
            ("0", "0", "<-", "END 2"),
        ],
        "subgraph": "END"
    },
    "END 2": {
        "transitions": [
            ("X", "X", "<-", "END 2"),
            (" ", " ", "->", "END 3"),
        ],
        "subgraph": "END"
    },
    "END 3": {
        "transitions": [
            ("X", " ", "->", "END 3"),
            ("0", " ", "->", "END 3")
        ],
        "final": True,
        "subgraph": "END"
    },
}
T = turing.machine(states, debug=False)
# lets make a function that returns the same way our gcd python returns, using our turing machine


def GCDturing(n, m):
    s = "1" * n + "0" + "1" * m
    t = T.test(s)
    return s, t, len(t)


G = T.plot("gcd")

GCDturing(8, 12)
T.animate("gcd.gif")
