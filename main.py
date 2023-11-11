import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import defaultdict

class TuringMachine:
    def __init__(self):
        self.tape = []
        self.head_position = 0
        self.state = 'q1'
        self.transitions = {
            ('q1', 'a'): ('q1', 'a', 'R'),
            ('q1', 'b'): ('q1', 'a', 'R'),
            ('q1', ' '): ('q_accept', ' ', 'S')
        }

        # Inicializar el grafo
        self.graph = nx.DiGraph()

        # Agregar nodos y transiciones al grafo
        for state, symbol in self.transitions.keys():
            self.graph.add_node(state, pos=(0, 0))  # Agregar posición inicial a cada nodo
            self.graph.add_node(self.transitions[(state, symbol)][0], pos=(0, 0))
            self.graph.add_edge(state, self.transitions[(state, symbol)][0], label=symbol)

    def set_tape(self, input_word):
        self.tape = list(input_word)
        self.head_position = 0
        self.state = 'q1'

    def step(self):
        current_symbol = self.tape[self.head_position] if 0 <= self.head_position < len(self.tape) else ' '
        if (self.state, current_symbol) in self.transitions:
            new_state, write_symbol, move_direction = self.transitions[(self.state, current_symbol)]
            if current_symbol != ' ':
                self.tape[self.head_position] = write_symbol

            if move_direction == 'R':
                self.head_position += 1
            elif move_direction == 'L':
                self.head_position -= 1

            self.state = new_state

    def run(self):
        while self.state != 'q_accept':
            self.step()

    def get_tape_content(self):
        return ''.join(self.tape)

    def visualize(self):
        pos = nx.get_node_attributes(self.graph, 'pos')
        labels = nx.get_edge_attributes(self.graph, 'label')
        nx.draw(self.graph, pos, with_labels=True, font_weight='bold')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=labels)
        plt.pause(0.5)  # Pausa para visualizar la transición
        plt.clf()  # Limpia el gráfico para la próxima iteración
