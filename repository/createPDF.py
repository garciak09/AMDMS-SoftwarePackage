from fpdf import FPDF


# Extract date into a new format from what's stored in database.
# Database has entire time stamp stored. We just want to show month, day, and year
# Date Format: MM/DD/YYYY
def getDate(s):
    return f'{s[5:7]}/{s[8:10]}/{s[0:4]}'

def getAverages(results):
    distortionResultTotal = 0
    passCount = 0
    runtimeTotal = 0
    for result in results:
        distortionResultTotal += result[3]
        runtimeTotal += float(result[6])
        if result[5] == "Pass":
            passCount += 1

    totalMeasurements = len(results)
    distortionAvg = distortionResultTotal / totalMeasurements
    averagePassRate = passCount / totalMeasurements
    runtimeAvg = runtimeTotal / totalMeasurements

    return round(distortionAvg, 5), round(averagePassRate, 2), round(runtimeAvg, 3), totalMeasurements


def createPDF(partNum, startDate, endDate, results):
    distortionAvg, averagePassRate, runtimeAvg, totalMeasurements = getAverages(results)

    # Used to reduce redundancy if the query is made to see measurements of only day
    if startDate == endDate:
        dateString = f"Measurements Date: {getDate(startDate)}"
    else:
        dateString = f"Measurements Timeframe: {getDate(startDate)} - {getDate(endDate)}"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_xy(0, 5)
    pdf.set_font("arial", 'B', 15)
    pdf.cell(70)
    pdf.cell(75, 10, f"Measurement Results For {partNum}", 0, 2, 'C')
    pdf.cell(75, 10, dateString, 0, 2, 'C')
    pdf.cell(-50)
    pdf.set_y(40)
    pdf.set_font("arial", 'I', 10)
    pdf.multi_cell(40, 10, 'Average Runtime' + '\n' + str(runtimeAvg) + ' sec', border=1, align='C')
    pdf.set_xy(60, 40)
    pdf.multi_cell(40, 10, 'Average Distortion' + '\n' + str(distortionAvg), border=1, align='C')
    pdf.set_xy(110, 40)
    pdf.multi_cell(40, 10, 'Total Mirrors Measured' + '\n' + str(totalMeasurements), border=1, align='C')
    pdf.set_xy(160, 40)
    pdf.multi_cell(40, 10, 'Average Pass Rate' + '\n' + f'{int(averagePassRate * 100)}%', border=1, align='C')
    pdf.image("heatmap.png", w=250, h=200, x=-10, y=70)
    # pdf.image("repository/heatmap.png", w=250, h=200, x=-10, y=70)
    pdf.output('report.pdf')
