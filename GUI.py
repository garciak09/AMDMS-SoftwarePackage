#!/usr/bin/python

import PySimpleGUI as sg

print(sg)
from measurementAlgorithm.main2 import main2


# variable definitions
# layout = this contains all the elements on the GUI
# window = the window is the actual popup that holds all the elements
# mirrorType = defined by a button click, gets stored in this variable and used in the main2 function


def main():
    layout = [
        [sg.Text('Mirror Part Number:', size=(20, 2), font=('Arial Bold', 20))],
        [sg.Button('Larger Mirror', size=(20, 2), font=('Arial Bold', 20), key='MirrorType1')],
        [sg.Button('Smaller Mirror', size=(20, 2), font=('Arial Bold', 20), key='MirrorType2')],
        [sg.Button("Start measurement", key="start", size=(20, 2), font=('Arial Bold', 20))],
        [sg.ProgressBar(max_value=100, orientation='h', key="-PROG-", size=(80, 5))],
        [sg.Text("Results:", size=(20, 2), font=('Arial Bold', 20))],
        [sg.Text("", key='-RESULTS-', size=(20, 2), font=('Arial Bold', 20))],
        [sg.Text("Run Time:", size=(20, 2), font=('Arial Bold', 20))],
        [sg.Text("", key='-TIMERESULTS-', size=(20, 2), font=('Arial Bold', 20))],
        [sg.Text("Distortion Percentage:", size=(20, 2), font=('Arial Bold', 20))],
        [sg.Text("", key='-DISTORTION-', size=(20, 2), font=('Arial Bold', 20))],
        [sg.Button("Emergency Stop", key="EStop", size=(20, 2), font=('Arial Bold', 20))],
    ]

    window = sg.Window("Mirror Distortion Measurement", layout, background_color="#FFFFFF", size=(1000, 1000))

    while True:
        event, values = window.read(timeout=1)
        # if the 'x' is selected the GUI will quit
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        # if the smaller mirror or larger mirror buttons are clicked the mirror type gets sent to the variable mirrortype
        if event == "MirrorType1":
            mirrorType = "1"
        if event == "MirrorType2":
            mirrorType = "2"
        # if the start button is pushed main2 is called and runs the entire distortion algorithm

        if event == "start":
            results, time, distortionLevel = main2(mirrorType)
            # progress bar gets updated
            for i in range(100):
                window["-PROG-"].UpdateBar(i + 1)
            # results are output with corresponding colors
            if results == "Pass":
                color = "#00FF00"
            else:
                color = "#FF0000"
            if time < 20:
                color2 = "#00FF00"
            else:
                color2 = "#FF0000"
            window['-RESULTS-'].update(results)
            window['-RESULTS-'].update(background_color=color)
            window['-TIMERESULTS-'].update(time)
            window['-TIMERESULTS-'].update(background_color=color2)
            window['-DISTORTION-'].update(distortionLevel * 100)
        # GUI will stop if this button is pushed
        if event == "EStop":
            break

    window.close()


if __name__ == "__main__":
    main()
