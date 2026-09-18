
import math

from mirrorAPI import *
import random
import uuid
from datetime import datetime


def deleteAllData():
    c, conn = connect()
    c.execute("DELETE FROM mirrorData;", )
    conn.commit()
    conn.close()


def roundup(x):
    return int(math.ceil(x / 10.0)) * 10

partNumbers = ["221-9264 / 153-4010", "5P-6879", "8T-2287"]
# deleteAllData()

coordinates = []
for i in range(301):
    x = random.randint(0, 1000)
    y = random.randint(0, 2000)
    coordinates.append(tuple([x + 1, y + 1]))
    coordinates.append(tuple([x - 1, y - 1]))
    coordinates.append(tuple([x + 1, y + 1]))
    coordinates.append(tuple([x - 1, y - 1]))
    coordinates.append(tuple([x + 1, y + 1]))
    coordinates.append(tuple([x - 1, y - 1]))
    coordinates.append(tuple([x + 1, y + 1]))
    coordinates.append(tuple([x - 1, y - 1]))
    x = random.randint(5000 - 1000, 5000)
    y = random.randint(5000 - 2000, 5000)
    coordinates.append(tuple([x + 1, y + 1]))
    coordinates.append(tuple([x - 1, y - 1]))
    coordinates.append(tuple([x + 1, y + 1]))
    coordinates.append(tuple([x - 1, y - 1]))
    coordinates.append(tuple([x + 1, y + 1]))
    coordinates.append(tuple([x - 1, y - 1]))
    coordinates.append(tuple([x + 1, y + 1]))
    coordinates.append(tuple([x - 1, y - 1]))
    x = random.randint(1000, 2000)
    y = random.randint(0, 1000)
    coordinates.append(tuple([x + 1, y + 1]))
    coordinates.append(tuple([x - 1, y - 1]))
    coordinates.append(tuple([x + 1, y + 1]))
    coordinates.append(tuple([x - 1, y - 1]))
    coordinates.append(tuple([x + 1, y + 1]))
    coordinates.append(tuple([x - 1, y - 1]))
    coordinates.append(tuple([x + 1, y + 1]))
    coordinates.append(tuple([x - 1, y - 1]))
    x = random.randint(5000 - 2000, 4000)
    y = random.randint(5000 - 1000, 5000)
    coordinates.append(tuple([x + 1, y + 1]))
    coordinates.append(tuple([x - 1, y - 1]))
    coordinates.append(tuple([x + 1, y + 1]))
    coordinates.append(tuple([x - 1, y - 1]))
    coordinates.append(tuple([x + 1, y + 1]))
    coordinates.append(tuple([x - 1, y - 1]))
    coordinates.append(tuple([x + 1, y + 1]))
    coordinates.append(tuple([x - 1, y - 1]))

# for i in range(301):
#     x = random.randint(5000 - 250, 5000 - 150)
#     y = random.randint(5000 - 2500, 5000 - 2200)
#     coordinates.append(tuple([x, y]))
#     x = random.randint(5000 - 500, 5000 - 250)
#     y = random.randint(5000 - 2400, 5000 - 1800)
#     coordinates.append(tuple([x, y]))
#     x = random.randint(5000 - 600, 5000 - 200)
#     y = random.randint(5000 - 4250, 5000 - 4000)
#     coordinates.append(tuple([x, y]))
#     coordinates.append(tuple([x + 1, y + 1]))
#     coordinates.append(tuple([x - 1, y - 1]))
#     x = random.randint(5000 - 4500, 5000 - 3000)
#     y = random.randint(5000 - 2500, 5000 - 2000)
#     coordinates.append(tuple([x, y]))
#     coordinates.append(tuple([x + 1, y + 1]))
#     coordinates.append(tuple([x - 1, y - 1]))
#     coordinates.append(tuple([x + 1, y + 1]))
#     coordinates.append(tuple([x - 1, y - 1]))
#     coordinates.append(tuple([x + 1, y + 1]))
#     coordinates.append(tuple([x - 1, y - 1]))
#     coordinates.append(tuple([x + 1, y + 1]))
#     coordinates.append(tuple([x - 1, y - 1]))
#     x = random.randint(150, 250)
#     y = random.randint(2200, 2500)
#     coordinates.append(tuple([x, y]))
#     x = random.randint(250, 500)
#     y = random.randint(1800, 2400)
#     coordinates.append(tuple([x, y]))
#     x = random.randint(200, 600)
#     y = random.randint(4000, 4250)
#     coordinates.append(tuple([x, y]))
#     coordinates.append(tuple([x + 1, y + 1]))
#     coordinates.append(tuple([x - 1, y - 1]))
#     x = random.randint(3000, 4500)
#     y = random.randint(2000, 2500)
#     coordinates.append(tuple([x, y]))
#     coordinates.append(tuple([x + 1, y + 1]))
#     coordinates.append(tuple([x - 1, y - 1]))
#     coordinates.append(tuple([x + 1, y + 1]))
#     coordinates.append(tuple([x - 1, y - 1]))
#     coordinates.append(tuple([x + 1, y + 1]))
#     coordinates.append(tuple([x - 1, y - 1]))
#     coordinates.append(tuple([x + 1, y + 1]))
#     coordinates.append(tuple([x - 1, y - 1]))


print(coordinates)

for i in range(20):
    result = "Fail"
    data = {"id": uuid.uuid4(),
            "coordinates": coordinates,
            "mirrorPartNum": "8T-2287",
            "runDate": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "distortionLevel": round(random.uniform(0, 1), 5),
            "result": result,
            "runTime": round(random.uniform(0, 1), 3)
            }

    POST(data)
# deleteAllData()

# partNum = partNumbers[random.randint(0, 2)]
# print("querying for part number: " + partNum)
# query = GET("2023-12-20 00:00:00", "2023-12-31 23:59:59", partNum)
# createHeatmap(query)
# createReport(GETALL())


#query = GETALL()
#### Create PDF ####
# createHeatmap(query)
# createPDF(partNum, "2023-12-20", "2023-12-31", query)
# sendEmail("kevinagarcia.az@gmail.com", partNum, "2023-12-20", "2023-12-20")

# deleteAllData()
