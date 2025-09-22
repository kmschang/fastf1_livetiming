import ast
import json
import re
from icecream import ic

landoNorris = []

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

        driverNumber = None
        sector = None
        sectorSegment = None
        segmentStatus = None
        previousValue = None
        
        # Gets the data from the drivers
        drivers = payloadData.get("Lines", {})
        for driverNumberStr, driverData in drivers.items():
            driverNumber = int(driverNumberStr)
            
            # Gets the data from the sectprs
            sectors = driverData.get("Sectors", {})
            for sectorStr, sectorData in sectors.items():
                sector = int(sectorStr)

                # Gets the data from the segments
                segments = sectorData.get("Segments", {})
                for segmentStr, segmentData in segments.items():
                    sectorSegment = int(segmentStr)

                    # Gets the data from the status
                    status = segmentData.get("Status")
                    if status is not None:
                        segmentStatus = int(status)

                # Gets the data from the previousValue
                previousValue = sectorData.get("PreviousValue")  # None if missing
                if previousValue is not None:
                    previousValue = float(previousValue)
                
            # Prints Data
            ic(driverNumber)
            ic(sector)
            ic(sectorSegment)
            ic(segmentStatus)
            ic(previousValue)



    else:
        ic("N/A")
            

with open("driverInformation.json", "r") as f:
    driverInfo = json.load(f)

with open("cache.txt", "r") as f:
    for i in range(10):
        parse_line(f)
        print("\n")
