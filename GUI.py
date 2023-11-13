import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
from main import TuringMachine
import time

def get_figure_canvas(window):
    figure, ax = plt.subplots(figsize=(3, 3))  
    canvas = FigureCanvasTkAgg(figure, window['-CANVAS-'].TKCanvas)
    canvas.draw()
    canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure, canvas

def draw_graph(graph, canvas, figure):
    pos = nx.spring_layout(graph)
    node_colors = [graph.nodes[node]['color'] for node in graph.nodes]
    nx.draw(graph, pos, with_labels=True, font_weight='bold', ax=figure.gca(), node_color=node_colors)

    canvas.draw()

def update_tape_display(window, tape_content, head_position):
    tape_display = '| ' + ' '.join(tape_content) + ' |'
    window['-TAPE-'].update(tape_display)
    window['-HEAD-'].update(head_position * 2 + 2)  

def main():
    tm = TuringMachine()

    layout = [
        [sg.Text("Ingrese la palabra (a, b, espacio en blanco):")],
        [sg.Multiline(key='-INPUT-', size=(20, 5))],  
        [sg.Button('Ejecutar'), sg.Button('Siguiente Paso'), sg.Button('Salir')],
        [sg.Canvas(key='-CANVAS-', size=(300, 300))],  
        [sg.Text('', key='-TAPE-', size=(30, 1))],  
        [sg.Text('', key='-HEAD-', size=(30, 1))],  
        [sg.Text(size=(30, 1), key='-OUTPUT-')],  
        [sg.Slider((1, 10), default_value=5, orientation='h', key='-SPEED-', enable_events=True),
         sg.Text('Velocidad')],
    ]

    window = sg.Window('Máquina de Turing', layout, finalize=True)
    figure, canvas = get_figure_canvas(window)

    while True:
        event, values = window.read(timeout=0)

        if event in (sg.WINDOW_CLOSED, 'Salir'):
            break

        elif event == 'Ejecutar':
            input_text = values['-INPUT-'].strip()
            input_words = [word.strip() for word in input_text.split('\n') if word.strip()]

            all_results = []

            if input_words:
                for input_word in input_words:
                    tm.set_tape(input_word)
                    tm.run()
                    final_configuration = tm.get_tape_content()
                    all_results.append(f"Palabra: {input_word}, Configuración final: {final_configuration}")

                window['-OUTPUT-'].update('\n'.join(all_results))
                draw_graph(tm.get_graph(), canvas, figure)

        elif event == 'Siguiente Paso':
            input_text = values['-INPUT-'].strip()
            input_words = [word.strip() for word in input_text.split('\n') if word.strip()]

            all_results = []

            if input_words:
                for input_word in input_words:
                    tm.set_tape(input_word)
                    tm.step()  
                    current_configuration = tm.get_tape_content()
                    all_results.append(f"Palabra: {input_word}, Configuración actual: {current_configuration}")

                    update_tape_display(window, tm.tape, tm.head_position)
                    draw_graph(tm.get_graph(), canvas, figure)

        speed = values['-SPEED-']
        time.sleep(1 / speed)

    window.close()

if __name__ == "__main__":
    main()
