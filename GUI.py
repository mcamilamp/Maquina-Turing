import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
from main import TuringMachine
import time  

def get_figure_canvas(window):
    figure, ax = plt.subplots(figsize=(5, 5))
    canvas = FigureCanvasTkAgg(figure, window['-CANVAS-'].TKCanvas)
    canvas.draw()
    canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure, canvas

def draw_graph(graph, canvas, figure):
    pos = nx.spring_layout(graph)
    node_colors = [graph.nodes[node]['color'] for node in graph.nodes]
    nx.draw(graph, pos, with_labels=True, font_weight='bold', ax=figure.gca(), node_color=node_colors)

    canvas.draw()

def main():
    tm = TuringMachine()

    layout = [
        [sg.Text("Ingrese la palabra sobre {a, b, espacio en blanco}:")],
        [sg.InputText(key='-INPUT-')],
        [sg.Button('Ejecutar'), sg.Button('Salir')],
        [sg.Canvas(key='-CANVAS-', size=(400, 400))],
        [sg.Text(size=(40, 1), key='-OUTPUT-')],
        [sg.Slider((1, 10), default_value=5, orientation='h', key='-SPEED-', enable_events=True),
         sg.Text('Velocidad')],
    ]
    

    window = sg.Window('Máquina de Turing', layout, finalize=True)
    figure, canvas = get_figure_canvas(window)


    while True:
        event, values = window.read()

        if event in (sg.WINDOW_CLOSED, 'Salir'):
            break

        elif event == 'Ejecutar':
            input_word = values['-INPUT-'].strip()

            if input_word:
                tm.set_tape(input_word)
                tm.run()
                final_configuration = tm.get_tape_content()
                window['-OUTPUT-'].update(f"Configuración final: {final_configuration}")
                draw_graph(tm.get_graph(), canvas, figure)

        
        speed = values['-SPEED-']
        time.sleep(1 / speed)  

    window.close()

if __name__ == "__main__":
    main()
