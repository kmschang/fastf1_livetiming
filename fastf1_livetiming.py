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

    print("------------------------------------------------------------------------------------")
    ic(payloadType)
    ic(payloadData)
    ic(payloadTimestamp)

    if payloadType == "TimingData":

        driverNumber = None
        sector = None
        sectorSegment = None
        status = None
        previousValue = None
        value = None
        pitOut = None
        personalFastest = None
        speedTrap = None
        speed = None

        
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
                        status = int(status)

                        # 0 - Driver not on track (Unknown)
                        # 1 - On Track
                        # 2 - Out Lap
                        # 4 - In Pit
                        # 8 - Entering Pit
                        # 16 - Exiting Pit
                        # 32 - Sector 1 Complete
                        # 64 - Sector 2 Complete
                        # 128 - Sector 3 Complete
                        # 256 - Lap Complete
                        # 512 - Sector timing valid (segment valid)
                        # 1024 - Lap timing valid
                        # 2048 - Segment Completed

                # Gets the data from the value
                value = sectorData.get("Value")  # None if missing
                if value is not None:
                    value = str(value)

                # Gets the data from the previousValue
                previousValue = sectorData.get("PreviousValue")  # None if missing
                if previousValue is not None:
                    previousValue = float(previousValue)

                # Personal Best data
                personalFastest = sectorData.get("PersonalFastest") # None if missing
                if personalFastest is not None:
                    personalFastest = bool(personalFastest)

            # Gets the data from pitOut
            pitOut = driverData.get("PitOut")  # None if missing
            if pitOut is not None:
                pitOut = bool(pitOut)

            # Gets the data from Status
            if status == None:
                status = driverData.get("Status")  # None if missing
                if status is not None:
                    status = int(status)
            
            # Speed Data from Sectors
            speedTraps = driverData.get("Speeds", {})
            for speedTrapStr, speedTrapData in speedTraps.items():
                speedTrap = str(speedTrapStr)

                # I1 - First Speed Trap
                # I2 - Second Speed Trap
                # S1 - Sector 1 Speed (Less Common)
                # S2 - Sector 2 Speed (Less Common)
                # ST - Speed Trap

                speed = speedTrapData.get("Value")
                if speed is not None and speed != "":
                    speed = int(speed)

            # Prints Data

            driverNumber is not None and ic(driverNumber)
            sector is not None and ic(sector)
            sectorSegment is not None and ic(sectorSegment)
            status is not None and ic(status)
            previousValue is not None and ic(previousValue)
            value is not None and ic(value)
            pitOut is not None and ic(pitOut)
            personalFastest is not None and ic(personalFastest)
            speedTrap is not None and ic(speedTrap)
            speed is not None and ic(speed)
            
            # Get driver from driverInfo
            ic(driverInfo[str(driverNumber)]["full_name"])

            


    elif payloadType == "TimingAppData":
        pass
    elif payloadType == "WeatherData":
        
        AirTemp = None
        Humidity = None
        Pressure = None
        Rainfall = None
        TrackTemp = None
        WindDirection = None
        WindSpeed = None

        AirTemp = payloadData.get("AirTemp")
        if AirTemp is not None:
            AirTemp = float(AirTemp)
            ic(AirTemp)

        Humidity = payloadData.get("Humidity")
        if Humidity is not None:
            Humidity = float(Humidity)
            ic(Humidity)

        Pressure = payloadData.get("Pressure")
        if Pressure is not None:
            Pressure = float(Pressure)
            ic(Pressure)

        Rainfall = payloadData.get("Rainfall")
        if Rainfall is not None:
            Rainfall = float(Rainfall)
            ic(Rainfall)

        TrackTemp = payloadData.get("TrackTemp")
        if TrackTemp is not None:
            TrackTemp = float(TrackTemp)
            ic(TrackTemp)

        WindDirection = payloadData.get("WindDirection")
        if WindDirection is not None:
            WindDirection = float(WindDirection)
            ic(WindDirection)

        WindSpeed = payloadData.get("WindSpeed")
        if WindSpeed is not None:
            WindSpeed = float(WindSpeed)
            ic(WindSpeed)

    elif payloadType == "SessionData":
        pass
    elif payloadType == "Heartbeat":
        pass
    else:
        pass
            

with open("driverInformation.json", "r") as f:
    driverInfo = json.load(f)

with open("cache.txt", "r") as f:
    for i in range(16):
        parse_line(f)
