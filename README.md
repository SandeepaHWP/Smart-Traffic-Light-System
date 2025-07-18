

# Smart Traffic Light System 🚦

An intelligent traffic control system designed using LabVIEW, Raspberry Pi 4B, and multiple sensors to dynamically adapt traffic signals based on pedestrian presence, vehicle flow, and weather conditions. The system enhances both safety and efficiency through real-time data processing and control.

## 🔧 Features

* **Custom Rain Detection Sensor with Servo Mechanism**
  A custom-designed moisture sensor detects rain intensity in four levels: No Rain, Normal, Medium, and Heavy. When heavy rain is detected, pedestrian red light duration is extended by 5 seconds for added safety.

  Unlike standard rain sensors that rely on heat sheets or nano-coatings, this system improves accuracy using a **servo motor**. Every 10 seconds during heavy rain, the servo tilts the rain sensor to physically shake off water droplets and then returns it to the horizontal position. This maintains high sensitivity and prevents false readings.

* **Camera-Based Pedestrian Crossing Logic**
  A camera is used to detect human presence at the pedestrian crossing. However, pedestrian detection alone does not trigger the red light. Two conditions must be met:

  1. A pedestrian must be present (detected via the camera).
  2. The pedestrian must press the crossing button.

  Only when both conditions are met does the system begin the red light sequence. The behavior of the red light follows these timing rules:

  * If a pedestrian crosses, a fixed **28-second window** is granted for vehicle traffic.
  * If another pedestrian arrives and presses the button during this window, the system will **not** initiate a new red light until the window completes.
  * If no pedestrian is present initially but someone arrives at t=35s and presses the button, the system checks again in 5 seconds.
  * If the pedestrian is still present at t=40s, a 2-second orange light is activated, followed by a red light.

* **Vehicle Detection and Counting System**
  Basic vehicle detection has been implemented, and camera-based vehicle counting is under development for integration into the final version.

* **Auto Street Light Subsystem**
  A subsystem that automatically turns on streetlights when low-light conditions (e.g., night) are detected, improving visibility and safety.

* **Processing and Control**
  The system was initially designed to use a Raspberry Pi 4B for all sensor interfacing, pedestrian detection via camera input, and traffic light control logic. However, due to performance constraints, the image processing tasks were offloaded to a laptop GPU for faster and more accurate processing, while the Raspberry Pi continues to handle sensor interfacing and control coordination.

## 🛠️ Tech Stack

* **LabVIEW** – Manages sensor logic, control rules, and communication
* **DAQ Card** – Interfaces with physical sensors and control systems
* **Raspberry Pi 4B** – Everything implemented using rapberrypi is implemented using Laptop.
* **Laptop with GPU** – Performs image processing tasks (e.g., pedestrian detection) for better performance
* **TCP/IP Protocol** – Communication between Raspberry Pi and laptop GPU
* **Camera Module** – For detecting both pedestrians and vehicles
* **Servo Motor** – Attached to the rain sensor to ensure clear surface for reliable measurement

## 📦 Folder Structure

```
SmartTrafficLightSystem/
├── LabVIEW/
│   └── smart_traffic_light_system_main.vi
│   └── TrafficLightStates.vi
├── VideoProcessing/
│   ├── status_provider.py
│   ├── phonefeed.py (if applicable)
│   └── vehicle.py (if applicable)
├── FinalProduct/
│   └── DemoVideo
├── README.md
```

## 📋 How to Use

1. Connect the rain sensor (with servo), camera, and other inputs to the DAQ and Raspberry Pi.
2. Launch LabVIEW VI files to handle sensor monitoring and logic control.
3. Run pedestrian and vehicle detection scripts on the laptop GPU.
4. Ensure the button press and human detection logic is functioning for pedestrian red lights.
5. Confirm the 28-second rule, 5-second buffer, orange-to-red transition, and extra 5 seconds in heavy rain.
6. Observe the servo tilting every 10 seconds during heavy rain.
7. Test nighttime conditions to verify auto streetlight activation.

## 🤝 Contributions

Pull requests are welcome. Feel free to open issues for feature suggestions or bug reports.

## 📜 License

MIT License



> Developed by Prbhashana, Chamath, and Sampavi ( Team 23 )

---

If you want me to save this as a file or tweak anything else, just let me know!
