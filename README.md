# 🏎️ fastf1_livetiming
`fastf1_livetiming` is an in-progress Python project designed to interface with the raw live timing data provided by the FastF1 library. The tool captures the live stream of timing packets from Formula 1 sessions and decodes the raw data into structured, usable information.

![GitHub License](https://img.shields.io/github/license/kmschang/fastf1_livetiming)
![GitHub Release](https://img.shields.io/github/v/release/kmschang/fastf1_livetiming)
![GitHub commit activity](https://img.shields.io/github/commit-activity/t/kmschang/fastf1_livetiming)
![GitHub last commit](https://img.shields.io/github/last-commit/kmschang/fastf1_livetiming)

---

## Table of Contents  
- [Overview](#Overview)
- [Features](#features)
- [Tech Stack](#Tech-Stack)
- [Setup](#setup)
- [Usage](#usage)
- [License](#License)

---

## Overview  

`fastf1_livetiming` is an in-progress Python project focused on capturing, decoding, and parsing the raw live timing data provided by the FastF1 library during Formula 1 sessions. The project aims to take the unstructured stream of timing packets and transform them into meaningful, structured information, including lap times, sector times, car positions, and status indicators. Beyond parsing, it also organizes and stores the data efficiently, allowing for real-time analysis, logging, or further processing. A key feature of the project is its ability to present this live data in the terminal in a clear, dynamic format, updating continuously as new packets arrive, making it easier to follow sessions as they unfold. While still under active development, the project provides a foundation for building more advanced live timing tools, visualizations, and telemetry analysis for Formula 1 enthusiasts and developers.

---

## Features  

- **Data Capture:** Connects to the FastF1 live timing service and continuously receives real-time timing packets for all cars on track.
- **Decoding & Parsing:** Translates raw timing data into structured formats, extracting key details such as sector times, lap times, car status, and telemetry markers.
- **Data Storage:** Organizes the parsed data for easy access, enabling further analysis, logging, or visualization.
- **Terminal Representation:** Displays live session data in a clean, readable format directly in the terminal, updating dynamically as new packets arrive.

---

## Tech Stack  

- **Frontend**: HTML (*Future Update*)
- **Backend**: Python
- **Database**: SQL (*Future Update*)
- **Other Tools**: FastF1

---

## Setup

1. **Install uv**
	Download and install [uv](https://github.com/astral-sh/uv) from the official repository or use:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv self update
uv python install 3.13
```

2. **Create a virtual environment**
```bash
uv venv
```

3. **Install dependencies**
```bash
uv pip install -e .
```

---

## Usage

1. Start fastf1 livtiming
```bash
uv run python -m fastf1.livetiming save --append cache.txt
```
- Still working on how the data goes into the program, but the command above will add the info into the `cache.txt` file which can be used later for working on the project

---

## License

This project is licensed under the MIT License, which means you are free to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the software, as long as you include the original copyright and license notice in any copy of the software. The software is provided "as is," without warranty of any kind.

