#!/usr/bin/python
import datetime
import math
import random
import uuid
from datetime import timedelta, datetime

import PySimpleGUI as sg
from PySimpleGUI import theme
from repository.createHeatmap import createHeatmap
from repository.mirrorAPI import *
from measurementAlgorithm.main2 import main2
from repository.createPDF import *
import re

from repository.sendEmail import sendEmail


# TODO: Add what part number was just run for 'Most Recent Run'
# TODO: Add 'calibrate' button
# TODO: Add

# variable definitions
# layout = this contains all the elements on the GUI
# window = the window is the actual popup that holds all the elements
# mirrorType = defined by a button click, gets stored in this variable and used in the main2 function


def isValidEmail(recipientEmailAddress):
    """
    @note:  Regular expressions are used to ensure that the entered email has a valid format. This does not validate
            that the email is real.

            'bogusemail@thisisnotreal.net' would technically pass the test.

            So please double-check the email you've inputted before clicking 'OK' to avoid any issues with sending the
            report to the wrong person.

    @param recipientEmailAddress: string of the email address where the report will be sent
    @rtype: Boolean
    @return: True if recipientEmailAddress is of valid format, False otherwise
    """
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if re.match(pattern, recipientEmailAddress) is not None:
        return True
    sg.popup("", "Email must be of valid format.", "e.g example@mail.com", title="Invalid Input")
    return False


def verifyPartNumberSelection(values):
    """
    Function to ensure that one part number has been picked in the 'Generate Report' Window

    @param values: dictionary with the part numbers as keys and a boolean as the value.
                    True boolean value means the part number has been selected. False, otherwise.
                    Only one part number can be selected, so only one key will have True value in dictionary.
    @rtype: String
    @return:  The part number that was selected to query,
        If none of the part numbers were selected then this function will return None (null) and display a popup window
        explaining that a part number must be selected.
    """
    if values["-221-9264 / 153-4010-"]:
        return "221-9264 / 153-4010"
    elif values["-5P-6879-"]:
        return "5P-6879"
    elif values["-8T-2287-"]:
        return "8T-2287"
    sg.popup("", "Must select a part number to query", title="Invalid Input")
    return None


def verifyDates(startDate, endDate):
    """
    This function will check that the start date comes before the end date
    @param startDate: String
    @param endDate: String
    @rtype: Boolean
    @return: True if the startDate is before the endDate. False, otherwise.
        If False, then a popup window is shown explaining that the startDate can't come after the endDate.
    """
    if startDate == "" or endDate == "":
        sg.popup("", "A date range must be selected", title="Invalid Input")
        return False
    if startDate >= endDate:
        sg.popup("", "End Date can't be before Start Date", title="Invalid Input")
        return False

    return True


def showGenerateReportWindow(window):
    """
        This function is called the user selects the "Generate Report" button in the Main GUI display.
        This window captures:
            - partNumToQuery: the mirror part number the report will be about
            - startDate, endDate: the time from of when the measurements were ran
            - email: the email address that the report will be sent to

        This function will call verification functions to ensure that the time frame is valid, and the
        email is of the right format before returning.
    @param window: PySimpleGUI instance
    @return: a dictionary of the values captured through user selection in the window
    """
    while True:  # 'Generate Report' window loop
        event, values = window.read()
        if event == "Cancel" or event is None:
            window.close()
            return None

        partNumToQuery = verifyPartNumberSelection(values)
        if partNumToQuery is None:  # verify that a part number was selected
            continue
        if event == "OK":
            if not verifyDates(values["-startDate-"], values["-endDate-"]):  # verify that dates are good
                continue

            if not isValidEmail(values["-email-"]):  # verify that the email is of right format
                continue
            break

    window.close()

    # time stamp is added to startDate and endDate for corner case of querying for a 1 day timeframe
    # dictionary is used due to better runtime performance compared to List (Array)
    queryValues = {"startDate": values["-startDate-"] + " 00:00:00.000000",
                   "endDate": values["-endDate-"] + " 23:59:59.000000",
                   "recipientEmailAddress": values["-email-"],
                   "mirrorPartNum": partNumToQuery
                   }
    return queryValues


def generateReport(query, values):
    """
        This function uses the query results from the SQLite window to create a heatmap, and generate a pdf
        report with the query results.
    @param query: a list of pixel coordinates showing where distortion was found
    @param values: a list of the inputted values from 'Generate Report' window

    """
    createHeatmap(query)
    createPDF(values["mirrorPartNum"], values["startDate"], values["endDate"], query)

    if sendEmail(values["recipientEmailAddress"], values["mirrorPartNum"], values["startDate"], values["endDate"]):
        sg.popup("",
                 f"Report Successfully Emailed!",
                 f"Recipient Email Address: {values['recipientEmailAddress']}",
                 title="Email Confirmation")
    else:
        sg.popup("",
                 "An error occurred when sending the email.",
                 "Make sure the email address inputted is accurate.",
                 title="Email Delivery Error")


def generateReportWindowFormat():
    """
    This function will display a new window when the "Generate Report" button is pressed in the main
    GUI.
    @rtype: List (Array)
    @return: the values that will be used to query the measurements and the email address to send the report to.
    """
    backgroundColor = "black"
    theme("dark")
    textColor = "yellow"

    sg.set_options(font=("Arial Bold", 18))
    current_month = datetime.now().month
    current_year = datetime.now().year

    layout = [
        # Mirror Part Number Selection
        [sg.Text('Choose the Mirror to create the report for', text_color=textColor, background_color=backgroundColor)],
        [sg.Radio("221-9264 / 153-4010", "mirror", enable_events=True, key="-221-9264 / 153-4010-", background_color=backgroundColor, text_color=textColor)],
        [sg.Radio("5P-6879", "mirror", enable_events=True, key="-5P-6879-", background_color=backgroundColor, text_color=textColor)],
        [sg.Radio("8T-2287", "mirror", enable_events=True, key="-8T-2287-", background_color=backgroundColor, text_color=textColor)],

        [  # Start Date and End Date Calendar Selection
            [sg.Input(key='-startDate-', size=(20, 1), readonly=True, text_color="yellow"),
             sg.CalendarButton('Start Date', target='-startDate-', format='%Y-%m-%d',
                               default_date_m_d_y=(current_month, None, current_year), button_color="black on yellow", location=(850, 600))],
            [sg.Input(key='-endDate-', size=(20, 1), readonly=True, text_color="yellow"),
             sg.CalendarButton('End Date', target='-endDate-', format='%Y-%m-%d',
                               default_date_m_d_y=(current_month, None, current_year), button_color="black on yellow", location=(850, 600))]
        ],

        # Email Address input box
        [sg.Text("Enter Target Email: ", text_color=textColor, background_color=backgroundColor), sg.Input(key='-email-', text_color="yellow"), ],

        # 'OK' and 'Cancel' Buttons
        [sg.Button('OK', button_color="black on yellow"), sg.Cancel(button_color="black on yellow")]
    ]

    window = sg.Window("Generate Report", layout, modal=True, size=(500, 300))
    window.BackgroundColor = backgroundColor
    return showGenerateReportWindow(window)


def windowLayout(backgroundColor):
    """
        This function creates the main GUI layout
    @param backgroundColor: String that may be "black" or "white". This is used to determine what color to make
                            certain boxes and texts according to the background color.
    @return:
    """
    if backgroundColor == "black":
        theme("dark")
        themeButton = "black on yellow"
        progressBarColor = "yellow on black"
    else:
        theme("black")
        themeButton = "yellow on black"
        progressBarColor = "black on yellow"

    CAT_LOGO = f"CAT-Logos/{backgroundColor}CATlogo.png"

    return [

        [
            sg.pin(sg.Button("Start measurement", key="start", size=(20, 2), visible=True, font=('Arial Bold', 20),
                             button_color="black on yellow")),
            sg.pin(sg.Button("Emergency Stop", key="EStop", size=(20, 2), visible=True, font=('Arial Bold', 20),
                             button_color="white on red")),
            sg.Image(CAT_LOGO, size=(250, 123), background_color=backgroundColor),

        ],
        [sg.pin(sg.Text("\nLast Hour Summary", size=(200, 3), font=('Arial Bold', 20), justification="center",
                        background_color="yellow", text_color="black"))],

        [
            sg.Text('Mirror Part Number', size=(20, 3), font=('Arial', 20, "bold"), justification="center",
                    auto_size_text=True, text_color="yellow"),
            sg.Text('Average Pass Rate ', size=(14, 3), font=('Arial', 20, "bold"), justification="center",
                    text_color="yellow"),
            sg.Text('Total Passed', size=(14, 3), font=('Arial', 20, "bold"), justification="center",
                    text_color="yellow"),
            sg.Text('Total Failed', size=(14, 3), font=('Arial', 20, "bold"), justification="center",
                    text_color="yellow"),
            sg.Text('Average Distortion Percentage', size=(14, 3), font=('Arial', 20, "bold"), justification="center",
                    text_color="yellow")
        ],

        [
            sg.Text('221-9264 / 153-4010', size=(20, 2), font=('Arial', 20, "italic"), justification="center",
                    text_color="yellow"),
            sg.Text('', key='-221-9264 / 153-4010-AVG-RESULTS-', size=(14, 2), font=('Arial', 20, "italic"),
                    justification="center", text_color="yellow"),
            sg.Text('', key='-221-9264 / 153-4010-AVG-PASSED-', size=(14, 2), font=('Arial', 20, "italic"),
                    justification="center", text_color="yellow"),
            sg.Text('', key='-221-9264 / 153-4010-AVG-FAILED-', size=(14, 2), font=('Arial', 20, "italic"),
                    justification="center", text_color="yellow"),
            sg.Text('', key='-221-9264 / 153-4010-AVG-DISTORTION-', size=(14, 2), font=('Arial', 20, "italic"),
                    justification="center", text_color="yellow")],

        [
            sg.Text('5P-6879', size=(20, 2), font=('Arial', 20, "italic"), justification="center", text_color="yellow"),
            sg.Text('', key='-5P-6879-AVG-RESULTS-', size=(14, 2), font=('Arial', 20, "italic"),
                    justification="center", text_color="yellow"),
            sg.Text('', key='-5P-6879-AVG-PASSED-', size=(14, 2), font=('Arial', 20, "italic"),
                    justification="center", text_color="yellow"),
            sg.Text('', key='-5P-6879-AVG-FAILED-', size=(14, 2), font=('Arial', 20, "italic"),
                    justification="center", text_color="yellow"),
            sg.Text('', key='-5P-6879-AVG-DISTORTION-', size=(14, 2), font=('Arial', 20, "italic"),
                    justification="center", text_color="yellow")],

        [
            sg.Text('8T-2287', size=(20, 2), font=('Arial', 20, "italic"), justification="center", text_color="yellow"),
            sg.Text('', key='-8T-2287-AVG-RESULTS-', size=(14, 2), font=('Arial', 20, "italic"),
                    justification="center", text_color="yellow"),
            sg.Text('', key='-8T-2287-AVG-PASSED-', size=(14, 2), font=('Arial', 20, "italic"),
                    justification="center", text_color="yellow"),
            sg.Text('', key='-8T-2287-AVG-FAILED-', size=(14, 2), font=('Arial', 20, "italic"),
                    justification="center", text_color="yellow"),
            sg.Text('', key='-8T-2287-AVG-DISTORTION-', size=(14, 2), font=('Arial', 20, "italic"),
                    justification="center", text_color="yellow")],

        [sg.Text(background_color=backgroundColor)],
        [sg.pin(sg.Text("\nMost Recent Run", size=(200, 3), font=('Arial Bold', 20), justification="center",
                        background_color="yellow", text_color="black"))],

        [
            sg.ProgressBar(max_value=100, orientation='h', key="-PROG-", size=(130, 5), bar_color=progressBarColor)
        ],

        [
            sg.Text("Part Num:", size=(20, 2), font=('Arial', 20), text_color="yellow", justification="right"),
            sg.Text("", key='-PART-NUM-', size=(20, 2), font=('Arial', 20), text_color="yellow")],

        [
            sg.Text("Results:", size=(20, 2), font=('Arial', 20), text_color="yellow", justification="right"),
            sg.Text("", key='-RESULTS-', size=(20, 2), font=('Arial', 20), text_color="yellow")],

        [
            sg.Text("Distortion Percentage:", size=(20, 2), font=('Arial', 20), text_color="yellow",
                    justification="right"),
            sg.Text("", key='-DISTORTION-', size=(20, 2), font=('Arial', 20), text_color="yellow")
        ],
        [sg.Text("", background_color=backgroundColor)],

        [sg.Text("Last Run:", text_color="yellow", size=(20, 2), font=('Arial', 20), justification="right"),
         sg.Text("", key="LastRun", size=(20, 2), font=('Arial', 20), text_color="yellow")
         ],
        [sg.Text("Last Calibration:", text_color="yellow", size=(20, 2), font=('Arial', 20), justification="right"),
         sg.Text("", key="LastCalibration", size=(20, 2), font=('Arial', 20), text_color="yellow")
         ],

        [
            sg.pin(
                sg.Button("Generate Report", key="Generate Report", size=(20, 2), visible=True,
                          font=('Arial Bold', 20), button_color="black on yellow")
            ),
            sg.pin(
                sg.Button("Calibrate Camera", key="Calibrate Camera", size=(20, 2), visible=True,
                          font=('Arial Bold', 20), button_color="black on yellow")
            ),
            sg.Button(f"Change Theme", key="-CHANGE-THEME-", size=(5,2), visible=True, button_color=themeButton,
                       pad=((150, 0), 30), font=('Arial', 9))

        ],

    ]


def isAcceptable(results, runTime):
    """
        This function is used to determine the background color for the text boxes with the runtime of the measurement
        and the Pass/Fail result.
    @param results: "Pass" or "Fail"
    @param runTime: float, represents the time it took for a measurement to complete.
    @return: color codes that are used to color the background of the text boxes with the pass/fail result and runtime
    """
    # results are output with corresponding colors
    color = "#FF0000"
    if type(results) is float:
        if results >= .50:
            color = "#00FF00"
    elif results == "Pass":
        color = "#00FF00"

    if runTime < 20:
        color2 = "#00FF00"
    else:
        color2 = "#FF0000"

    return color, color2


def updateGUI(partNum, result, runtime, distortionLevel, window):
    """
        This function is called when the "Start Measurement" button is pressed and a measurement has successfully
        completed. This is used to update the values in the main GUI.
    @param partNum: the part number that was just measured
    @param result: "Pass" or "Fail"
    @param runtime: the time it took for the run to complete
    @param distortionLevel: the percentage of distortion found on the mirror
    @param window: main GUI window

    """

    # progress bar gets updated
    for i in range(100):
        window["-PROG-"].UpdateBar(i + 1)

    # Get the time of run and an hour prior to display the results of the past hour
    timeOfRun = datetime.now()
    now = timeOfRun.strftime("%Y-%m-%d %H:%M:%S")
    hourAgo = (timeOfRun - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")

    query = GET(hourAgo, now, partNum)
    avgDistortion, avgPassRate, avgRuntime, totalMirrors = getAverages(query)
    resultsColor, timeColor = isAcceptable(result, runtime)

    avgPassRateColor, avgTimeColor = isAcceptable(avgPassRate, avgRuntime)

    #### Analytics Section ####
    window[f"-{partNum}-AVG-RESULTS-"].update(str(round(avgPassRate * 100, 2)) + "%")
    window[f"-{partNum}-AVG-PASSED-"].update(round(totalMirrors * avgPassRate))
    window[f"-{partNum}-AVG-FAILED-"].update(round(totalMirrors * (1 - avgPassRate)))
    window[f"-{partNum}-AVG-DISTORTION-"].update(str(round(avgDistortion * 100, 2)) + "%")

    #### Most Recent Measurement Section ####
    window['-PART-NUM-'].update(partNum)
    window['-RESULTS-'].update(result, background_color=resultsColor, text_color="black")
    window['-DISTORTION-'].update(str(distortionLevel * 100) + "%")


def roundup(x):
    return int(math.ceil(x / 10.0)) * 10

def updateTheme(event, window, backgroundColor):
    """
        This function is used to switch the background color of the main GUI window. It is called when the
        "Change Theme" button is pressed.
    """
    newWin = None
    if event == '-CHANGE-THEME-':
        if backgroundColor == "black":
            backgroundColor = "white"
        elif backgroundColor == "white":
            backgroundColor = "black"
        newWin = sg.Window("Mirror Distortion Measurement", windowLayout(backgroundColor), size=(1000, 1000))
        newWin.BackgroundColor = backgroundColor
    return window, newWin

def transferValues(oldWindow, newWindow):
    """

        This function is used to keep the current values displayed in the main GUI window when the theme of the
        window is changed.

    """
    valueToUpdate = ["-221-9264 / 153-4010-AVG-RESULTS-",
                     "-221-9264 / 153-4010-AVG-PASSED-",
                     "-221-9264 / 153-4010-AVG-FAILED-",
                     "-221-9264 / 153-4010-AVG-DISTORTION-",
                     "-5P-6879-AVG-RESULTS-",
                     "-5P-6879-AVG-PASSED-",
                     "-5P-6879-AVG-FAILED-",
                     "-5P-6879-AVG-DISTORTION-",
                     "-8T-2287-AVG-RESULTS-",
                     "-8T-2287-AVG-PASSED-",
                     "-8T-2287-AVG-FAILED-",
                     "-8T-2287-AVG-DISTORTION-",
                     "-PART-NUM-",
                     "-RESULTS-",
                     "-DISTORTION-",
                     "LastRun",
                     "LastCalibration"]
    for key in valueToUpdate:
        newWindow[key].update(oldWindow[key].get())
        if key == "-RESULTS-":  # Used because the background color of the results text box is different from the rest
            backgroundColor, holder = isAcceptable(oldWindow[key].get(), 1)
            if len(newWindow[key].get()) > 0:
                newWindow[key].update(background_color=backgroundColor, text_color="black")
def main():
    layout = windowLayout("black")
    window = sg.Window("Mirror Distortion Measurement", layout, size=(1000, 1000))
    window.BackgroundColor = "black"  # change to 'white' or 'black' for theme change
    while True:
        event, values = window.read()

        # if the 'x' is selected the GUI will quit
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        if event == '-CHANGE-THEME-':
            window, newWin = updateTheme(event, window, window.BackgroundColor)
            newWin.read(timeout=1)
            transferValues(window, newWin)
            window.close()
            window = newWin

        if event == "Calibrate Camera":
            # TODO: Add Calibration Function
            window['LastCalibration'].update(datetime.now().strftime("%b-%d %I:%M %p"))

        # if the start button is pushed main2 is called and runs the entire distortion algorithm
        if event == "start":
            result, runtime, distortionLevel, distortedCoordinates = main2(random.choice(["1", "2"]))
            timeOfRun = datetime.now()
            partNum = random.choice(["221-9264 / 153-4010", "5P-6879", "8T-2287"])
            data = {"id": uuid.uuid4(),
                    "coordinates": distortedCoordinates,
                    "mirrorPartNum": partNum,
                    "runDate": timeOfRun.strftime("%Y-%m-%d %H:%M:%S"),
                    "distortionLevel": distortionLevel,
                    "result": result,
                    "runTime": runtime
                    }
            POST(data)
            updateGUI(partNum, result, runtime, distortionLevel, window)
            window['LastRun'].update(timeOfRun.strftime("%b-%d %I:%M %p"))

        if event == "Generate Report":
            values = generateReportWindowFormat()

            # Avoids errors in creating the HeatMap
            if values is None:
                continue

            query = GET(values["startDate"], values["endDate"], values["mirrorPartNum"])

            # Avoids errors in computing averages for the results
            if len(query) == 0:
                sg.popup("", "Query returned no results", title="Empty Query Exception")
                continue
            generateReport(query, values)

        # GUI will stop if this button is pushed
        if event == "EStop":
            break

    window.close()


if __name__ == "__main__":
    main()
