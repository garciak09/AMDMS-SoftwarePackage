#!/usr/bin/python
import math
import random
import uuid
from datetime import timedelta

import PySimpleGUI as sg
from PySimpleGUI import theme

from repository.createHeatmap import createHeatmap
from repository.mirrorAPI import *
from measurementAlgorithm.main2 import main2
from repository.createPDF import *
import re


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

            if not isValidEmail(values["-email-"]):
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
    mirrorPartNumbers = ["221-9264 / 153-4010", "5P-6879", "8T-2287"]
    sg.set_options(font=("Arial Bold", 18))
    layout = [
        # Mirror Part Number Selection
        [sg.Text('Choose the Mirror to create the report for')],
        [sg.Radio("221-9264 / 153-4010", "mirror", enable_events=True, key="-221-9264 / 153-4010-")],
        [sg.Radio("5P-6879", "mirror", enable_events=True, key="-5P-6879-")],
        [sg.Radio("8T-2287", "mirror", enable_events=True, key="-8T-2287-")],

        [  # Start Date and End Date Calendar Selection
            [sg.Input(key='-startDate-', size=(20, 1), readonly=True, disabled_readonly_background_color='white'),
             sg.CalendarButton('Start Date', target='-startDate-', format='%Y-%m-%d',
                               default_date_m_d_y=(12, None, 2023))],
            [sg.Input(key='-endDate-', size=(20, 1), readonly=True, disabled_readonly_background_color='white'),
             sg.CalendarButton('End Date', target='-endDate-', format='%Y-%m-%d',
                               default_date_m_d_y=(12, None, 2023))]
        ],

        # Email Address input box
        [sg.Text("Enter Target Email: "), sg.Input(key='-email-'), ],

        # 'OK' and 'Cancel' Buttons
        [sg.Button('OK'), sg.Cancel()]
    ]

    window = sg.Window("Generate Report", layout, modal=True, size=(500, 300))
    return showGenerateReportWindow(window)


def windowLayout():
    theme('Black')
    return [

        [
            sg.pin(sg.Button("Start measurement", key="start", size=(20, 2), visible=True, font=('Arial Bold', 20),
                             button_color="black on yellow")),
            sg.pin(sg.Button("Emergency Stop", key="EStop", size=(20, 2), visible=True, font=('Arial Bold', 20),
                             button_color="white on red")),
            sg.Image("whiteCATlogo.png", size=(250, 123), background_color="white"),

        ],
        # [sg.Text(f'Last Run: \nLast Calibration: ', key='-TIME-', size=(20, 4), font=('Arial', 20),
        #          background_color='white',
        #          text_color='black', pad=(0, 0))],
        [sg.pin(sg.Text("\nLast Hour Summary", size=(200, 3), font=('Arial Bold', 20), justification="center",
                        background_color="yellow", text_color="black"))],
        # [sg.Text(background_color="white")],

        [
            sg.Text('Mirror Part Number', size=(20, 3), font=('Arial', 20, "bold"), justification="center",
                    auto_size_text=True, text_color="yellow", background_color="black"),
            sg.Text('Average Pass Rate ', size=(14, 3), font=('Arial', 20, "bold"), justification="center",
                    text_color="yellow", background_color="black"),
            sg.Text('Total Passed', size=(14, 3), font=('Arial', 20, "bold"), justification="center",
                    text_color="yellow", background_color="black"),
            sg.Text('Total Failed', size=(14, 3), font=('Arial', 20, "bold"), justification="center",
                    text_color="yellow", background_color="black"),
            sg.Text('Average Distortion Percentage', size=(14, 3), font=('Arial', 20, "bold"), justification="center",
                    text_color="yellow", background_color="black")
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

        [sg.Text(background_color="white")],
        [sg.pin(sg.Text("\nMost Recent Run", size=(200, 3), font=('Arial Bold', 20), justification="center",
                        background_color="yellow", text_color="black"))],
        # [sg.Text(background_color="white")],

        [
            sg.ProgressBar(max_value=100, orientation='h', key="-PROG-", size=(130, 5), bar_color="black on yellow")
        ],

        [
            sg.Text("Part Num:", size=(20, 2), font=('Arial', 20), text_color="yellow", justification="right"),
            sg.Text("", key='-PART-NUM-', size=(20, 2), font=('Arial', 20), text_color="yellow")],

        [
            sg.Text("Results:", size=(20, 2), font=('Arial', 20), text_color="yellow", justification="right"),
            sg.Text("", key='-RESULTS-', size=(20, 2), font=('Arial', 20), text_color="yellow")],

        # [
        #     sg.Text("Run Time:", size=(20, 2), font=('Arial', 20), text_color="yellow"),
        #     sg.Text("", key='-TIMERESULTS-', size=(20, 2), font=('Arial', 20), text_color="yellow")],

        [
            sg.Text("Distortion Percentage:", size=(20, 2), font=('Arial', 20), text_color="yellow", justification="right"),
            sg.Text("", key='-DISTORTION-', size=(20, 2), font=('Arial', 20), text_color="yellow")
        ],
        [sg.Text("", background_color="white")],

        [sg.Text("Last Run:", text_color="yellow",size=(20, 2), font=('Arial', 20), justification="right"),
         sg.Text("", key="LastRun", size=(20, 2), font=('Arial', 20), text_color="yellow")
         ],
        [sg.Text("Last Calibration:", text_color="yellow",size=(20, 2), font=('Arial', 20), justification="right"),
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
            # sg.Image("catLogo.png", size=(786,555), background_color="black")
        ],
        # [
        #     sg.Text("", justification="right", background_color="black", size=(125, 2)),
        #     sg.Image("catLogo.png", size=(500,500), background_color="black")
        # ]

    ]


def isAcceptable(results, runTime):
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
    window[f"-{partNum}-AVG-DISTORTION-"].update(str(avgDistortion * 100) + "%")

    #### Most Recent Measurement Section ####
    window['-PART-NUM-'].update(partNum)
    window['-RESULTS-'].update(result, background_color=resultsColor, text_color="black")
    # window['-TIMERESULTS-'].update(str(runtime) + " seconds", background_color=timeColor)
    window['-DISTORTION-'].update(str(distortionLevel * 100) + "%")


def roundup(x):
    return int(math.ceil(x / 10.0)) * 10


def main():
    ## Used to display last time a measurement was run and last time a camera calibration was done.
    lastRunTime = ""
    lastCalibrationTime = ""

    layout = windowLayout()
    window = sg.Window("Mirror Distortion Measurement", layout, background_color="white", size=(1000, 1000))

    while True:
        event, values = window.read(timeout=1)

        # if the 'x' is selected the GUI will quit
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        if event == "Calibrate Camera":
            # TODO: Add Calibration Function
            lastCalibrationTime = datetime.now().strftime("%b-%d %I:%M %p")
            window['LastCalibration'].update(lastCalibrationTime)

        # if the start button is pushed main2 is called and runs the entire distortion algorithm
        if event == "start":
            result, runtime, distortionLevel = main2(random.choice(["1", "2"]))
            timeOfRun = datetime.now()
            partNum = random.choice(["221-9264 / 153-4010", "5P-6879", "8T-2287"])

            data = {"id": uuid.uuid4(),
                    "coordinates": f"[({roundup(random.randint(4500, 5000))}, {roundup(random.randint(4500, 5000))}), "
                                   f" ({roundup(random.randint(2000, 2500))}, {roundup(random.randint(2000, 2500))})]",
                    "mirrorPartNum": partNum,
                    "runDate": timeOfRun.strftime("%Y-%m-%d %H:%M:%S"),
                    "distortionLevel": distortionLevel,
                    "result": result,
                    "runTime": runtime
                    }
            lastRunTime = timeOfRun.strftime("%b-%d %I:%M %p")
            POST(data)
            updateGUI(partNum, result, runtime, distortionLevel, window)
            window['LastRun'].update(lastRunTime)

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
