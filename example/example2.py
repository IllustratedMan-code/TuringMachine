import turing
import json

with open("example2.json") as f:
    states = json.load(f)

states = {
    "S": {
        "transitions": [
            ["a", "X", "->", "SUBN 1"],
            ["b", "X", "->", "SUBM 1"],
            ["X", "X", "->", "S"],
            [" ", " ", "->", "F"],
        ]
    },
    "SUBN 1": {
        "transitions": [
            ["X", "X", "->", "SUBN 1"],
            ["a", "a", "->", "SUBN 1"],
            ["b", "X", "->", "SUBN 2"],
        ]
    },
    "SUBN 2": {
        "transitions": [
            ["b", "X", "->", "SUBN 3"],
        ]
    },
    "SUBN 3": {
        "transitions": [
            ["b", "b", "->", "SUBN 3"],
            ["X", "X", "->", "SUBN 3"],
            ["c", "X", "->", "SUBN 4"],
        ]
    },
    "SUBN 4": {
        "transitions": [
            ["c", "X", "->", "SUBN 5"],
        ]
    },
    "SUBN 5": {
        "transitions": [
            ["c", "X", "->", "SUBN 6"],
        ]
    },
    "SUBN 6": {
        "transitions": [
            ["X", "X", "<-", "SUBN 6"],
            ["a", "a", "<-", "SUBN 6"],
            ["b", "b", "<-", "SUBN 6"],
            ["c", "c", "<-", "SUBN 6"],
            [" ", " ", "->", "S"],
        ]
    },
    "SUBM 1": {
        "transitions": [
            ["X", "X", "->", "SUBM 1"],
            ["b", "b", "->", "SUBM 1"],
            ["c", "X", "->", "SUBM 2"],
        ]
    },
    "SUBM 2": {
        "transitions": [
            ["c", "X", "<-", "SUBN 6"],
        ]
    },
    "F": {
        "transitions": [],
        "final": True
    }
}

T = turing.machine(states, debug=True)
T.test("aabbbbbbcccccccccc")
T.plot("machine").view()
T.animate("machine.gif")
