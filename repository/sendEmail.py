import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


def getDate(dateString):
    """
    Change the format of the inputted date
    @param dateString: date as a string in YYYY-MM-DD format
    @rtype: String
    @return: date in DD/MM/YYYY format
    """
    return f'{dateString[5:7]}/{dateString[8:10]}/{dateString[0:4]}'


def getDateString(startDate, endDate):
    """
    Helper function that creates the string to show on the PDF. It determines if the start and end date are the same.

    @param startDate: string that is a date in YYYY-MM-DD format (the
    @param endDate: string that is a date in YYYY-MM-DD format
    @rtype: String
    @return:
        If dates are the same then the PDF will show that the measurements were done in 1 day.
        If dates are different, then the PDF will show the start and end date timeframe.
    """
    if startDate == endDate:
        return f"on {getDate(startDate)}"
    return f"from {getDate(startDate)} - {getDate(endDate)}"


def sendEmail(recipientEmail, partNum, startDate, endDate):
    """
    This function will take the PDF analytics report, sign into the measurement device's email account and
    send the report with a message to the inputted email address.

    @param recipientEmail: string that is the email address to send the report to
    @param partNum: the part number of mirror that was queried for this report
    @param startDate: the start date of when the measurements have to be between
    @param endDate: the end date of when the measurements have to be between

    @rtype: Boolean
    @return: True if the email was successfully sent, False otherwise

    """
    body = (f"Hello,\n\nHere is the report for the Mirror Distortion Measurements done for the {partNum} mirror!\n"
            f"These measurements were done {getDateString(startDate, endDate)}.\n\nSincerely yours,\nTeam 24012")

    sender = 'distortionmeasurementsystem@gmail.com'
    password = 'rdng mrrn aysi hgyz'
    receiver = recipientEmail

    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = receiver
    message['Subject'] = f'{partNum} Mirror Distortion Measurements Report'

    message.attach(MIMEText(body, 'plain'))

    pdfname = 'report.pdf'

    # open the file in binary
    binary_pdf = open(pdfname, 'rb')

    payload = MIMEBase('application', 'octate-stream', Name=pdfname)
    # payload = MIMEBase('application', 'pdf', Name=pdfname)
    payload.set_payload((binary_pdf).read())

    # enconding the binary into base64
    encoders.encode_base64(payload)

    # add header with pdf name
    payload.add_header('Content-Decomposition', 'attachment', filename=pdfname)
    message.attach(payload)

    # use gmail with port
    session = smtplib.SMTP('smtp.gmail.com', 587)

    # enable security
    session.starttls()

    # login with mail_id and password
    session.login(sender, password)

    text = message.as_string()
    wasSent = None
    try:
        session.sendmail(sender, receiver, text)
        wasSent = True
    except:
        wasSent = False

    session.quit()
    return wasSent
