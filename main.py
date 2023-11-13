import networkx as nx

class TuringMachine:
    def __init__(self):
        self.tape = []
        self.head_position = 0
        self.state = 'q1'
        self.transitions = {
            ('q1', 'a'): ('q1', 'a', 'R'),
            ('q1', 'b'): ('q2', 'a', 'R'),  
            ('q1', ' '): ('q_accept', ' ', 'S'),
            ('q2', 'a'): ('q2', 'a', 'R'),
            ('q2', 'b'): ('q2', 'a', 'R'),  
            ('q2', ' '): ('q3', ' ', 'R'),  
            ('q3', 'a'): ('q3', 'a', 'R'),
            ('q3', 'b'): ('q3', 'a', 'R'),  
            ('q3', ' '): ('q_accept', ' ', 'S')
        }

        self.graph = nx.DiGraph()

        for state, symbol in self.transitions.keys():
            self.graph.add_node(state, pos=(0, 0), color='blue')
            self.graph.add_node(self.transitions[(state, symbol)][0], pos=(0, 0), color='blue')
            self.graph.add_edge(state, self.transitions[(state, symbol)][0], label=symbol)

    def set_tape(self, input_word):
        self.tape = list(input_word + ' ')
        self.head_position = 0
        self.state = 'q1'

    def step(self):
        if 0 <= self.head_position < len(self.tape):
            current_symbol = self.tape[self.head_position]
            if (self.state, current_symbol) in self.transitions:
                new_state, write_symbol, move_direction = self.transitions[(self.state, current_symbol)]
                self.tape[self.head_position] = write_symbol

                if move_direction == 'R':
                    self.head_position += 1
                elif move_direction == 'L':
                    self.head_position -= 1

                self.state = new_state
            else:
                self.state = 'q_accept'
        else:
            self.state = 'q_accept'

    def run(self):
        visited_nodes = []
        while self.state != 'q_accept':
            visited_nodes.append(self.state)
            self.step()

        for node in self.graph.nodes:
            if node in visited_nodes:
                self.graph.nodes[node]['color'] = 'red'
            else:
                self.graph.nodes[node]['color'] = 'blue'

    def get_tape_content(self):
        return ''.join(self.tape)

    def get_graph(self):
        return self.graph
