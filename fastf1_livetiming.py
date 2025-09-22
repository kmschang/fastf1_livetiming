from icecream import ic
import ast
import json
import re

cacheFile: str = "cache.txt"
driverInfoFile: str = "driverInformation.json"

with open(driverInfoFile) as f:
    driverInfo = json.load(f)

with open(cacheFile, "r") as f:
    data = ast.literal_eval(f.readline().strip())

    payloadType = data[0]
    payloadData = data[1]
    payloadTimestamp = data[2]

    ic(payloadType)
    ic(payloadData)
    ic(payloadTimestamp)

    # extract all numbers from the payloadData
    payloadDataNumbers = re.findall(r"\d+", json.dumps(payloadData))

    # set variables from the payloadDataNumbers list
    driverNumber, sector, sectorSegment, segmentStatus = map(int, payloadDataNumbers)



