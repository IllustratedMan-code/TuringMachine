# A Turing Machine in Python

This project is a simple Turing machine that I
originally wrote to check my homework.

# Usage

States are defined using a Json syntax (you can actually use Json!).

```python
import turing

states = { "S": {
        "transitions": [
            ["1", "3", "->", "S"],
            [" ", " ", "->", "F"],
        ],
    },
    "F": {
        "transitions": [],
        "final": True
    },
}
T = turing.machine(states, debug=True)
T.test("11111011")
T.plot("state_diagram")
T.animate("usage.gif")
```

# GCD

A common function one might want to implement is the greatest common denominator (GCD) function.

This is the recursive python version:

```python
def gcd(n, m):
    if m != 0:
        return gcd(m, n % m)
    else:
        return n
gcd(8, 12)
# outputs 4
```

The following Turing machine takes 2 numbers in unary 111111110111111111111 (8,12) and calculates the gcd using a turing machine.

![](gcd.pdf)
![](gcd.gif)
