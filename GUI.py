import PySimpleGUI as sg
from main import TuringMachine

class TuringMachineGUI:
    def __init__(self):
        self.tm = TuringMachine()

        layout = [
            [sg.Text("Ingrese la palabra sobre {a, b}:")],
            [sg.InputText(key='-INPUT-')],
            [sg.Button('Ejecutar'), sg.Button('Salir')],
            [sg.Text(size=(40, 1), key='-OUTPUT-')]
        ]

        self.window = sg.Window('Máquina de Turing', layout)

    def run(self):
        while True:
            event, values = self.window.read()

            if event in (sg.WINDOW_CLOSED, 'Salir'):
                break

            elif event == 'Ejecutar':
                input_word = values['-INPUT-'].strip()

                if input_word:
                    self.tm.set_tape(input_word)
                    self.tm.run()
                    final_configuration = self.tm.get_tape_content()
                    self.window['-OUTPUT-'].update(f"Configuración final: {final_configuration}")

        self.window.close()

if __name__ == "__main__":
    app = TuringMachineGUI()
    app.run()
