import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
from matplotlib.animation import FuncAnimation
from main import TuringMachine
import time

def get_figure_canvas(window):
    figure, ax = plt.subplots(figsize=(3, 3))
    canvas = FigureCanvasTkAgg(figure, window['-CANVAS-'].TKCanvas)
    canvas.draw()
    canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure, canvas

def get_tape_canvas(window):
    figure, ax = plt.subplots(figsize=(3, 0.5))  # Tamaño más pequeño para la cinta
    canvas = FigureCanvasTkAgg(figure, window['-TAPE-CANVAS-'].TKCanvas)
    canvas.draw()
    canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure, canvas

def draw_graph(graph, canvas, figure):
    pos = nx.spring_layout(graph)
    node_colors = [graph.nodes[node]['color'] for node in graph.nodes]

    figure.gca().clear()

    nx.draw(graph, pos, with_labels=True, font_weight='bold', ax=figure.gca(), node_color=node_colors)
    canvas.draw()

def animate_tape(ax, tape_content, head_position, color):
    ax.clear()

    ax.set_xlim(0, len(tape_content))
    ax.set_ylim(0, 1)

    for i, char in enumerate(tape_content):
        ax.add_patch(plt.Rectangle((i, 0), 1, 1, facecolor=color if i == head_position else 'white', edgecolor='black'))

def main():
    tm = TuringMachine()

    layout = [
        [sg.Text('Input:'), sg.Text('Output:', pad=((190, 0), 0))],
        [sg.Multiline(size=(30, 5), key='-INPUT-'), sg.Output(size=(30, 5), key='-OUTPUT-')],
        [sg.Button('Ejecutar'), sg.Button('Siguiente Paso')],
        [sg.Canvas(key='-CANVAS-', size=(300, 300))],
        [sg.Text('', key='-TAPE-', size=(30, 1))],
        [sg.Text('', key='-HEAD-', size=(30, 1))],
        [sg.Canvas(key='-TAPE-CANVAS-', size=(300, 50))],  # Nuevo Canvas para la cinta
        [sg.Text('Speed:'), sg.Slider(range=(1, 10), default_value=5, orientation='h', size=(15, 20), key='-SPEED-')],
        [sg.Button('Salir')]
    ]

    window = sg.Window('Máquina de Turing', layout, finalize=True)
    figure, canvas = get_figure_canvas(window)
    tape_figure, tape_canvas = get_tape_canvas(window)

    ax_tape = tape_figure.add_subplot(111)
    tape_content = []
    head_position = 0
    color = 'green'  # Color de la cinta cuando la cabeza está encima

    def update_animation(frame):
        nonlocal tape_content, head_position, color
        tm.step()
        tape_content = tm.tape
        head_position = tm.head_position
    
        if len(tape_content) > 0:
            ax_tape.clear()
            ax_tape.set_xlim(0, len(tape_content))
            ax_tape.set_ylim(0, 1)
            animate_tape(ax_tape, tape_content, head_position, color)

            figure.gca().clear()
            try:
                draw_graph(tm.get_graph(), canvas, figure)
            except Exception as e:
                print(f"Error updating graph: {e}")

    ani = FuncAnimation(tape_figure, update_animation, interval=100, repeat=False)

    while True:
        event, values = window.read(timeout=0)

        if event == sg.WIN_CLOSED or event == 'Salir':
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
                    all_results.append(f"Palabra: {input_word}, Resultado: {final_configuration}")

                window['-OUTPUT-'].update('\n'.join(all_results))

        elif event == 'Siguiente Paso':
            ani.event_source.stop()
            input_text = values['-INPUT-'].strip()
            input_words = [word.strip() for word in input_text.split('\n') if word.strip()]

            all_results = []

            if input_words:
                for input_word in input_words:
                    tm.set_tape(input_word)
                    tm.step()
                    current_configuration = tm.get_tape_content()
                    all_results.append(f"Palabra: {input_word}, Configuración actual: {current_configuration}")

                window['-OUTPUT-'].update('\n'.join(all_results))

            ani.event_source.start()

        speed = values['-SPEED-']
        time.sleep(1 / speed)

    ani.event_source.stop()
    window.close()

if __name__ == "__main__":
    main()
