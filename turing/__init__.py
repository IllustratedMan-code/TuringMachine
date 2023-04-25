import graphviz
from matplotlib import pyplot as plt, animation
import matplotlib


class transition:

    def __init__(self, symbol, replace, direction, state):
        self.symbol = symbol
        self.replace = replace
        self.direction = direction
        self.state = state


class state:

    def __init__(self, transitions, final=False, subgraph=None, compass=None):
        self.transitions = transitions
        for i, v in enumerate(transitions):
            if type(v) != transition:
                self.transitions[i] = transition(*v)
        self.final = final
        self.subgraph = subgraph
        self.compass = compass


class machine:

    def __init__(self,
                 states: dict,
                 input_tape="",
                 start_state="S",
                 debug=False):
        self.debug = debug
        self.states = states
        self.transition_data = []
        for k, v in states.items():
            if type(v) != state:
                self.states[k] = state(**v)
        self.pointer = 0
        self.start_state = start_state
        self.current_state = states[start_state]
        self.current_state_name = start_state
        self._init_input_tape(input_tape)
        self.max_transitions = 100 * len(self.input_tape)
        self.transition_count = 0

    def _init_input_tape(self, input_tape):
        if input_tape == "":
            self.input_tape = list(" ")
        else:
            self.input_tape = list(input_tape)

    def printif(self, message):
        if self.debug:
            print(message)

    def transition(self):
        transitioned = False
        for t in self.current_state.transitions:
            if self.input_tape[self.pointer] == t.symbol:
                transitioned = True
                self.transition_count += 1
                self.input_tape[self.pointer] = t.replace
                if t.direction == "<-":
                    self.pointer -= 1
                elif t.direction == "->":
                    self.pointer += 1

                if self.pointer == -1:
                    self.input_tape = [" "] + self.input_tape
                    self.pointer = 0
                elif self.pointer == len(self.input_tape):
                    self.input_tape = self.input_tape + [" "]
                self.current_state = self.states[t.state]
                self.current_state_name = t.state
                self.print_info()
                break
        return not transitioned

    def print_info(self):
        s = f"Transition count:{self.transition_count}\nCurrent state:{self.current_state_name}\ncurrent tape:\n"
        tape = "".join(self.input_tape).replace(" ", "󱞟") + "\n" + " " * len(
            (self.input_tape[:self.pointer])) + "^"
        s += tape
        self.printif(s)
        self.transition_data += [s]

    def transition_until_stop(self):
        while (True):
            t = self.transition()
            if t and self.current_state.final:
                self.printif(
                    "The string was accepted by the machine and resulted in the following tape:"
                )
                # output ="".join(self.input_tape[self.pointer:]).rstrip().
                output = "".join(self.input_tape).strip()
                self.printif(output)
                return output
            elif t:
                self.printif(
                    "The string was not accepted by the machine (state was not final) and resulted in the following tape:"
                )
                output = "".join(self.input_tape).strip()
                self.printif(output)
                return "FAILED"
            elif self.transition_count >= self.max_transitions and self.max_transitions != -1:
                self.printif(
                    "Maximum transition count was met, the implies the existance of an infinite loop"
                )
                self.printif(
                    "To set an infinite maximum transition count, set turing_machine.max_transitions to -1"
                )
                return "INFINITE LOOP"

    def test(self, input_tape, max_transitions=0):
        self._init_input_tape(input_tape)
        self.current_state = self.states[self.start_state]
        self.current_state_name = self.start_state
        self.transition_count = 0
        self.pointer = 0
        if max_transitions == 0:
            self.max_transitions = 1000 * len(self.input_tape)
        else:
            self.max_transitions = max_transitions

        return self.transition_until_stop()

    def plot(self, filename, engine="dot", attributes={}):
        DG = graphviz.Digraph(filename=filename)
        DG.engine = engine
        DG.attr(**attributes)
        # nodes
        subgraphs = {}
        for k, v, in self.states.items():
            if v.subgraph and v.subgraph not in subgraphs:
                subgraphs[v.subgraph] = graphviz.Digraph(
                    name=f"cluster_{v.subgraph}")
                subgraphs[v.subgraph].attr(label=v.subgraph)
                subgraphs[v.subgraph].attr(fontcolor="blue")
                subgraphs[v.subgraph].attr(style="dotted")
        for k, v in self.states.items():
            attributes = {"labelfontcolor": "black"}
            if v.subgraph:
                G = subgraphs[v.subgraph]
            else:
                G = DG
            if k == self.start_state:
                G.node("fake", style="invisible")
                G.edge("fake", k)
                attributes["root"] = "true"
            if self.states[k].final:
                attributes["shape"] = "doublecircle"
            else:
                attributes["shape"] = "circle"
            G.node(k, **attributes)
        for v in subgraphs.values():
            DG.subgraph(v)
        # edges
        for k, v in self.states.items():
            labels = {}
            for t in v.transitions:
                symbol = t.symbol.replace(" ", "☐")
                replace = t.replace.replace(" ", "☐")
                direction = t.direction.replace("->", "⟶")
                direction = direction.replace("<-", "⟵")
                if t.state in labels:
                    labels[t.state] += f"{symbol}, {replace}, {direction}\n"
                else:
                    labels[t.state] = f"{symbol}, {replace}, {direction}\n"
            for key, label in labels.items():
                if v.compass:
                    DG.edge(f"{k}:{v.compass}", key, label=label)
                else:
                    DG.edge(k, key, label=label)
        DG.render()
        return DG

    def animate(self, filename=None):
        matplotlib.rcParams['font.family'] = 'monospace'
        fig, ax = plt.subplots()
        label = ax.text(0, 0, "", ha="left", fontsize=30)
        ax.set(ylim=(0, 0.5))

        def animate(i):
            label.set_text(self.transition_data[i])

        anim = animation.FuncAnimation(fig,
                                       animate,
                                       interval=100,
                                       frames=len(self.transition_data))
        ax.axis('off')
        fig.tight_layout()
        if filename:
            writergif = animation.PillowWriter(fps=10)
            anim.save(filename, writer=writergif)
        else:
            plt.show()
        return anim
