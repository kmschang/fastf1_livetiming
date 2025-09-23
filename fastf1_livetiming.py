import ast
import json
import re
from icecream import ic
from datetime import datetime, timezone, timedelta


# Functions
def ordinal(n: int) -> str:
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return str(n) + suffix


def adjustTimezone(timestamp_str: str, offset_hours: int) -> str:
    s_fixed = timestamp_str[:-2] + "Z"
    
    # Parse as UTC
    dt_utc = datetime.strptime(s_fixed, "%Y-%m-%dT%H:%M:%S.%fZ")
    dt_utc = dt_utc.replace(tzinfo=timezone.utc)
    
    # Apply offset
    target_tz = timezone(timedelta(hours=offset_hours))
    dt_local = dt_utc.astimezone(target_tz)
    
    # Format with ordinal day
    day_with_suffix = ordinal(dt_local.day)
    formatted = dt_local.strftime(f"%A, %B {day_with_suffix}, %Y %H:%M:%S %Z")
    
    return formatted


def time_between(ts1: str, ts2: str) -> float:
    def parse_timestamp(ts: str) -> datetime:
        ts = ts.rstrip("Z")  # remove trailing Z

        if '.' in ts:
            # fractional seconds present
            dt = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S.%f")
        else:
            # no fractional seconds
            dt = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S")

        return dt.replace(tzinfo=timezone.utc)
    
    dt1 = parse_timestamp(ts1)
    dt2 = parse_timestamp(ts2)
    
    delta = dt2 - dt1
    return abs(delta.total_seconds())


def parse_line(f, previousTimestamp):
    line = f.readline()
    if not line: 
        return None

    data = ast.literal_eval(line.strip())

    payloadType = data[0]
    payloadData = data[1]
    payloadTimestamp = data[2]

    print("------------------------------------------------------------------------------------")

    if previousTimestamp is not None:
       ic(f'{time_between(previousTimestamp, payloadTimestamp)} seconds')

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
            try:
                ic(driverInfo[str(driverNumber)]["full_name"])
            except KeyError as e:
                print(f"\033[91mERROR: Driver number {driverNumber} not found in driverInformation.json\033[0m")


            


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
        
        sentTime = None

        sentTime = payloadData.get("Utc")
        if sentTime is not None:
            ic(adjustTimezone(sentTime, 0))
            ic(adjustTimezone(sentTime, -5))


    else:
        ic("ERROR: Failure to parse data")
    
    return payloadTimestamp
            

with open("driverInformation.json", "r") as f:
    driverInfo = json.load(f)

with open("cache.txt", "r") as f:
    previousTimestamp = None
    for i in range(633):
        previousTimestamp = parse_line(f, previousTimestamp)
