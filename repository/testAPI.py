import math

from mirrorAPI import *
import random
import uuid
from datetime import datetime


def deleteAllData():
    c, conn = connect()
    c.execute("DELETE FROM mirrorData;", )
    # c.execute("ALTER TABLE mirrorData ADD COLUMN runDate TIMESTAMP")
    # c.execute("ALTER TABLE mirrorData ADD COLUMN result VARCHAR(4)")
    conn.commit()
    conn.close()


def roundup(x):
    return int(math.ceil(x / 10.0)) * 10

partNumbers = ["221-9264 / 153-4010", "5P-6879", "8T-2287"]
# deleteAllData()
# for i in range(10000):
#     result = random.choice(["Pass", "Fail"])
#     data = {"id": uuid.uuid4(),
#             "coordinates": f"[({roundup(random.randint(4500, 5000))}, {roundup(random.randint(4500, 5000))}), "
#                            f" ({roundup(random.randint(2000, 2500))}, {roundup(random.randint(2000, 2500))})]",
#             "mirrorPartNum": partNumbers[random.randint(0, 2)],
#             "runDate": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#             "distortionLevel": round(random.uniform(0, 1), 5),
#             "result": result,
#             "runTime": round(random.uniform(0, 1), 3)
#             }
#
#     POST(data)
# deleteAllData()

# c.execute('''
#
#             SELECT coordinates FROM mirrorData
#             WHERE id = "ae003071-75b8-4b30-a8b7-9fddfefa7232"
#
#           ''')

# coordinates = c.fetchall()
# conn.close()
# coord = [i[::-1] for i in eval(coordinates[0][0])]
# for i in range(len(coord)):
#     coord[i] = (4000 - coord[i][0], 4000 - coord[i][1])
#
# print(coord)
# data = {"id": uuid.uuid4(),
#         "coordinates": coord,
#         "mirrorPartNum": partNumbers[2],
#         "runDate": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#         "distortionLevel": round(random.uniform(0, 1), 5),
#         "result": "Fail",
#         "runTime": round(random.uniform(0, 1), 3)
#         }
# for i in range(2):
#     POST(data)

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
