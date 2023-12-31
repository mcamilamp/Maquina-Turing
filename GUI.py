import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
from matplotlib.animation import FuncAnimation
from main import TuringMachine
import gettext
import time
import sys
import os
import pyttsx3
from gtts import gTTS
import pygame


MAX_FRAMES = 100  
localedir = os.path.join(os.path.dirname(__file__), 'locale')

# Inicializar el motor de voz
pygame.mixer.init()

def emitir_mensaje(mensaje):
    tts = gTTS(text=mensaje, lang='es')
    tts.save("mensaje.mp3")

    # Reproducir el archivo de audio con pygame
    pygame.mixer.music.load("mensaje.mp3")
    pygame.mixer.music.play()

    # Esperar a que la reproducción termine antes de continuar
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
def get_figure_canvas(window):
    figure, ax = plt.subplots(figsize=(3, 3))
    canvas = FigureCanvasTkAgg(figure, window['-CANVAS-'].TKCanvas)
    canvas.draw()
    canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure, canvas

def get_tape_canvas(window):
    figure, ax = plt.subplots(figsize=(3, 0.5))  
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

def main(idioma):

    tm = TuringMachine()
    
    translations = gettext.translation('mensajes', localedir, languages=[idioma])
    translations.install()
    _ = translations.gettext

    for node in tm.graph.nodes:
        tm.graph.nodes[node]['color'] = 'blue'
    for u, v in tm.graph.edges:
        tm.graph[u][v]['color'] = 'black'
        
    layout = [
        [sg.Radio(_('Español'),'RADIO1', key='-ES-', enable_events=True),
         sg.Radio(_('Inglés'), "RADIO1", key='-EN-', enable_events=True),
         sg.Radio(_('Francés'), "RADIO1", key='-FR-', enable_events=True)],
        
        [sg.Text(_('Entrada')), sg.Text(_('Salida'), pad=((190, 0), 0))],
        [sg.Multiline(size=(30, 5), key='-INPUT-'), sg.Output(size=(30, 5), key='-OUTPUT-')],
        [sg.Button(_('Ejecutar'), key='-EXECUTE-'), sg.Button(_('Siguiente paso'), key='-NEXT-')],
        [sg.Canvas(key='-CANVAS-', size=(300, 300))],
        [sg.Text('', key='-TAPE-', size=(30, 1))],
        [sg.Text('', key='-HEAD-', size=(30, 1))],
        [sg.Canvas(key='-TAPE-CANVAS-', size=(300, 50))], 
        [sg.Text(_('Velocidad')), sg.Slider(range=(1, 10), default_value=5, orientation='h', size=(15, 20), key='-SPEED-')],
        [sg.Button(_('Salir'), key='-EXIT-')]
    ]

    window = sg.Window(_('Máquina de Turing'), layout, finalize=True)
    figure, canvas = get_figure_canvas(window)
    tape_figure, tape_canvas = get_tape_canvas(window)

    ax_tape = tape_figure.add_subplot(111)
    tape_content = []
    head_position = 0
    color = 'blue'

    def update_animation(frame):
        nonlocal tape_content, head_position, color
        tm.step()
        tape_content = tm.tape
        head_position = tm.head_position

        if len(tape_content) > 0:
            animate_tape(ax_tape, tape_content, head_position, color)
            
            node_colors = [tm.graph.nodes[node]['color'] for node in tm.graph.nodes]
            edge_colors = [tm.graph[u][v]['color'] for u, v in tm.graph.edges]
            nx.set_node_attributes(tm.graph, values=dict(zip(tm.graph.nodes, node_colors)), name='color')
            nx.set_edge_attributes(tm.graph, values=dict(zip(tm.graph.edges, edge_colors)), name='color')

            draw_graph(tm.graph, canvas, figure)
            
    def change_language(idioma):
        if idioma == 'en':
            locale = 'en'
        elif idioma == 'fr':
            locale = 'fr'
        else:
            locale = 'es'
        
        gettext.install('mensajes', localedir, names=("ngettext",))
        gettext.translation('mensajes', localedir, languages=[locale]).install()
        main(locale)

    ani = FuncAnimation(
        tape_figure, 
        update_animation, 
        interval=100, 
        repeat=False, 
        cache_frame_data=False, 
        save_count=MAX_FRAMES
    )

    while True:
        event, values = window.read(timeout=0)

        if event == sg.WIN_CLOSED or event == '-EXIT-':
            break
        
        elif event in ('-ES-', '-EN-', '-FR-'):
            if values['-ES-']:
                change_language('es')
            elif values['-EN-']:
                change_language('en')
            elif values['-FR-']:
                change_language('fr')

        elif event == '-EXECUTE-':
            input_text = values['-INPUT-'].strip()
            input_words = [word.strip() for word in input_text.split('\n') if word.strip()]

            all_results = []

            if input_words:
                for input_word in input_words:
                    tm.set_tape(input_word)
                    tm.run()
                    final_configuration = tm.get_tape_content()
                    all_results.append(f'Palabra: {input_word} Resultado: {final_configuration}')

                    # Agregar mensaje de voz para la aceptación
                    if tm.state == 'q_accept':
                        emitir_mensaje("La máquina de Turing ha aceptado la entrada.")

                window['-OUTPUT-'].update('\n'.join(all_results))

        elif event == '-NEXT-':
            ani.event_source.stop()
            input_text = values['-INPUT-'].strip()
            input_words = [word.strip() for word in input_text.split('\n') if word.strip()]

            all_results = []

            if input_words:
                for input_word in input_words:
                    tm.set_tape(input_word)
                    tm.step()
                    current_configuration = tm.get_tape_content()
                    all_results.append(f"Palabra: {input_word} Configuración actual: {current_configuration}")

                    # Agregar mensaje de voz para la aceptación
                    if tm.state == 'q_accept':
                        emitir_mensaje("La máquina de Turing ha aceptado la entrada.")

                window['-OUTPUT-'].update('\n'.join(all_results))

            ani.event_source.start()

        speed = values['-SPEED-']
        time.sleep(1 / speed)

    ani.event_source.stop()
    window.close()

if __name__ == "__main__":
    main('es')
