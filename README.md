# IoT University Project [ID: 06]

## Overview
This project is based on ["IoT for Beginners"](https://aka.ms/iot-beginners) and follows the lessons from [Microsoft's IoT-For-Beginners](https://github.com/microsoft/IoT-For-Beginners/tree/main/2-farm/lessons/3-automated-plant-watering). It involves developing applications using virtual hardware to simulate sensor interactions. The project is conducted as a group activity, culminating in a presentation and demonstration.

## Environment Setup
We will use virtual hardware, such as CounterFit, to simulate IoT devices and sensors.

### Required Software
- **Python 3.9.1** (Do not download from the website; install via the Microsoft Store)
- **Flask 2.1.2** (`pip install Flask==2.1.2`)
- **Werkzeug 2.1.2** (`pip install Werkzeug==2.1.2`)
- **CounterFit** (launch with `counterfit` and open [http://127.0.0.1:5000/](http://127.0.0.1:5000/))

### Running CounterFit
1. Open VS Code Terminal and launch CounterFit:
   ```sh
   counterfit
   ```
2. Open the web interface at [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
3. Run the Python script (`app.py`):
   ```python
   from counterfit_connection import CounterFitConnection
   CounterFitConnection.init('127.0.0.1', 5000)
   ```
## Assignment and Presentation
### Group Work Requirements
- Prepare slides summarizing key concepts and assignment results.
- Use instructor-provided preliminary slides ([Google Drive Link](https://drive.google.com/drive/folders/1INXCNAvpfRYMtcLCYrTFmM9IJpNdlFGv?usp=drive_link)).
- No need to detail individual tasks—just list task names.

### Presentation & Demo
- Duration: **30-45 minutes**.
- **Before the seminar**, upload slides to Moodle.
- The first slide should include:
  - Student IDs
  - Names
  - GitHub repository link
- Merge all slides into one **PDF file**.
- **Naming convention:** `Group_[ID_Number]_[TopicName].pdf` (e.g., `Group_06_Automated_Plant_Watering.pdf`).
- One upload per group is sufficient.
- **Each member must present or demo.**

## Additional Instructions
- **Building a Nightlight (Virtual IoT Hardware)**
  - Work on `virtual-device-sensor.md` to add a light sensor before running the code.

## Repository Structure
```
📂 iot-university-project
├── 📂 src
│   ├── app.py
│   ├── sensor_simulation.py
│   ├── ...
├── 📂 docs
│   ├── virtual-device-sensor.md
│   ├── research_topics.md
├── 📂 slides
│   ├── Group_XX_TopicName.pdf
│   ├── ...
├── README.md
└── requirements.txt
```
## Contribution Guidelines
1. **Fork** the repository.
2. **Clone** the repository to your local machine.
3. Create a **feature branch** for your changes.
4. Commit and push your changes.
5. Submit a **pull request** for review.

## License
This project follows the MIT License. See `LICENSE` for details.
