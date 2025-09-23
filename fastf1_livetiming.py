# IMPORTS
import ast
import json
import re
from icecream import ic
from datetime import datetime, timezone, timedelta


# VARIABLES
drivers_data = {}
track_data = {"track_status": None}
weather_data = {"AirTemp" : None, "Humidity" : None, "Pressure" : None, "Rainfall" : None, "TrackTemp" : None, "WindDirection" : None, "WindSpeed" : None}


# FUNCTIONS
# Adds the ordinal to the date
def ordinal(n: int) -> str:
    """Adds the ordinal to the date for better looking dates

    Args:
        n (int): takes in the number you want to add the ordinal to

    Returns:
        str: returns the number with the ordinal as string
    """
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return str(n) + suffix


# Adjusts for a timezone, Takes in the raw time and then adds timezone offset
def adjustTimezone(timestamp_str: str, offset_hours: int) -> str:
    """ Adjusts the date to the date in a certain time zone

    Args:
        timestamp_str (str): Unicode date format recieved by FastF1 payload
        offset_hours (int): hours offset from UTC (takes positive and negative)

    Returns:
        str: returns the updated time with timezone offset along with formatting the date to be more human like
    """
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


# Gets the time between two dates
def time_between(ts1: str, ts2: str) -> float:
    """ Gets the time between two dates

    Args:
        ts1 (str): Date #1
        ts2 (str): Date #2

    Returns:
        float: returns the time in seconds between the dates
    """
    def parse_timestamp(ts: str) -> datetime:
        """ Gets the time from the timestamp

        Args:
            ts (str): Unicde format of a date

        Returns:
            datetime: formatted date for easier computing
        """
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


# Reads data from the file
def parse_line(f, previousTimestamp):
    line = f.readline()
    if not line: 
        return None

    # Get data from line on file
    data = ast.literal_eval(line.strip())

    # Seperate data into categories
    payloadType = data[0]
    payloadData = data[1]
    payloadTimestamp = data[2]

    # Print divider for starting new set of data
    print("------------------------------------------------------------------------------------")

    # Print time from last message
    if previousTimestamp is not None:
       ic(f'{time_between(previousTimestamp, payloadTimestamp)} seconds')

    # Print Raw Data form stream
    ic(payloadType)
    ic(payloadData)
    ic(payloadTimestamp)

    if payloadType == "TimingData":

        # Timing Data
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

            # Get driver from driverInformation.json
            try:
                ic(driverInfo[str(driverNumber)]["full_name"])
                ic(driverNumber)

                # Sets up driver in drivers_data if doesn't exist
                if driverNumber not in drivers_data:
                    drivers_data[driverNumber]  = {"current_sector": None, "current_segment": None, "current_status": None, "current_tire": None, "sector_times": [], "speed": None, "pit_out": None}
                
                # Sets current driver to active for adding variables later
                driver_entry = drivers_data[driverNumber]

            except KeyError as e:
                print(f"\033[91m{e}\033[0m")
                print(f"\033[91mERROR: Driver number {driverNumber} not found in driverInformation.json\033[0m")
            
            # Gets the data from the sectprs
            sectors = driverData.get("Sectors", {})
            for sectorStr, sectorData in sectors.items():
                sector = int(sectorStr)
                driver_entry["current_sector"] = sector

                # Gets the data from the segments
                segments = sectorData.get("Segments", {})
                for segmentStr, segmentData in segments.items():
                    sectorSegment = int(segmentStr)
                    driver_entry["current_segment"] = sectorSegment

                    # Gets the data from the status
                    status = segmentData.get("Status")
                    if status is not None:
                        status = int(status)
                        driver_entry["current_status"] = status

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
                    ic(value)

                # Gets the data from the previousValue
                previousValue = sectorData.get("PreviousValue")  # None if missing
                if previousValue is not None:
                    previousValue = float(previousValue)
                    ic(previousValue)

                # Personal Best data
                personalFastest = sectorData.get("PersonalFastest") # None if missing
                if personalFastest is not None:
                    personalFastest = bool(personalFastest)
                    ic(personalFastest)

            # Gets the data from pitOut
            pitOut = driverData.get("PitOut")  # None if missing
            if pitOut is not None:
                pitOut = bool(pitOut)
                ic(pitOut)

            # Gets the data from Status
            if status == None:
                status = driverData.get("Status")  # None if missing
                if status is not None:
                    status = int(status)
                    ic(status)
            
            # Speed Data from Sectors
            speedTraps = driverData.get("Speeds", {})
            for speedTrapStr, speedTrapData in speedTraps.items():
                speedTrap = str(speedTrapStr)
                ic(speedTrap)

                # I1 - First Speed Trap
                # I2 - Second Speed Trap
                # S1 - Sector 1 Speed (Less Common)
                # S2 - Sector 2 Speed (Less Common)
                # ST - Speed Trap

                # If speed, get speed value
                speed = speedTrapData.get("Value")
                if speed is not None and speed != "":
                    speed = int(speed)
                    ic(speed)

        ic(drivers_data)
        ic(drivers_data[driverNumber])
            

    elif payloadType == "TimingAppData":
        pass
    elif payloadType == "WeatherData":
        
        # Weather Vairables
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
            weather_data["AirTemp"] = AirTemp

        Humidity = payloadData.get("Humidity")
        if Humidity is not None:
            Humidity = float(Humidity)
            weather_data["Humidity"] = Humidity

        Pressure = payloadData.get("Pressure")
        if Pressure is not None:
            Pressure = float(Pressure)
            weather_data["Pressure"] = Pressure

        Rainfall = payloadData.get("Rainfall")
        if Rainfall is not None:
            Rainfall = float(Rainfall)
            weather_data["Rainfall"] = Rainfall

        TrackTemp = payloadData.get("TrackTemp")
        if TrackTemp is not None:
            TrackTemp = float(TrackTemp)
            weather_data["TrackTemp"] = TrackTemp

        WindDirection = payloadData.get("WindDirection")
        if WindDirection is not None:
            WindDirection = float(WindDirection)
            weather_data["WindDirection"] = WindDirection

        WindSpeed = payloadData.get("WindSpeed")
        if WindSpeed is not None:
            WindSpeed = float(WindSpeed)
            weather_data["WindSpeed"] = WindSpeed

        ic(weather_data)

    elif payloadType == "SessionData":
        pass
    elif payloadType == "Heartbeat":
        
        sentTime = None

        sentTime = payloadData.get("Utc")
        if sentTime is not None:
            ic(adjustTimezone(sentTime, 0))
            ic(adjustTimezone(sentTime, -5))

    elif payloadType == "RaceControlMessages":
        
        # General variables
        messageNumber = None
        messageCategory = None

        # Flag variables
        flagType = None
        flagScope = None
        flagSector = None

        # Other variables
        messageText = None

        # Get messages
        messages = payloadData.get("Messages", {})
        for messageNumberStr, messageData in messages.items():
            messageNumber = int(messageNumberStr)
            ic(messageNumber)

            #Get message category (Flag, Other)
            messageCategory = messageData.get("Category")
            if messageCategory is not None:
                messageCategory = str(messageCategory)
                ic(messageCategory)

            # If flag, get flag info
            if messageCategory == ("Flag"):
                
                # Get flag type (Green, Yellow, Double Yellow, Red)
                flagType = messageData.get("Flag")
                if flagType is not None:
                    flagType = str(flagType)
                    ic(flagType)

                # Get flag scope (Sector, Track)
                flagScope = messageData.get("Scope")
                if flagScope is not None:
                    flagScope = str(flagScope)
                    ic(flagScope)

                    # If sector flag, get sector
                    flagSector = messageData.get("Sector")
                    if flagSector is not None:
                        flagSector = int(flagSector)
                        ic(flagSector)
                
            # Get message
            messageText = messageData.get("Message")
            if messageText is not None:
                messageText = str(messageText)
                ic(messageText)

    else:
        ic("ERROR: Failure to parse data")
    
    return payloadTimestamp
            
# Get driver information from file
with open("driverInformation.json", "r") as f:
    driverInfo = json.load(f)

# Open and parse data
with open("cache.txt", "r") as f:
    previousTimestamp = None
    for i in range(16):
        previousTimestamp = parse_line(f, previousTimestamp)
