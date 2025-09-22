import ast
import json
import re
from icecream import ic

def parse_line(f):
    line = f.readline()
    if not line: 
        return None

    data = ast.literal_eval(line.strip())

    payloadType = data[0]
    payloadData = data[1]
    payloadTimestamp = data[2]

    ic(payloadType)
    ic(payloadData)
    ic(payloadTimestamp)

    if payloadType == "TimingData":
        payloadDataNumbers = re.findall(r"\d+", json.dumps(payloadData))
        if len(payloadDataNumbers) >= 4:
            driverNumber, sector, sectorSegment, segmentStatus = map(int, payloadDataNumbers[:4])
            return {
                "type": payloadType,
                "timestamp": payloadTimestamp,
                "driverNumber": driverNumber,
                "sector": sector + 1,
                "sectorSegment": sectorSegment + 1,
                "segmentStatus": segmentStatus
            }

    # fallback if not TimingData or missing numbers
    return {
        "type": payloadType,
        "timestamp": payloadTimestamp,
        "data": payloadData
    }


with open("cache.txt", "r") as f:
    for i in range(10):
        result = parse_line(f)
        if result is None: 
            ic("Error reading file. Could be the end.")
            break
        ic(i, result)
