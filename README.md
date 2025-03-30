# IoT University Project [ID: 06]-Arduino Watering System

## Overview

This project is based on "IoT for Beginners" and follows the lessons from Microsoft's IoT-For-Beginners. It involves developing applications using actual hardware to simulate sensor interactions. The project is conducted as a group activity, culminating in a presentation and demonstration. We use an Arduino Uno to implement the system.

## Features

- **Automatic Mode**: Waters plants based on soil moisture levels.
- **Manual Control**: Control the relay via MQTT commands using the Mosquitto client.
- **MQTT Integration**: Uses a public MQTT broker for remote monitoring and control.
- **Real-Time Monitoring**: Subscribe to soil moisture data from the Arduino.

## Hardware Requirements

- Arduino (e.g., Uno, ESP8266, ESP32)
- Soil moisture sensor
- Relay module
- Water pump
- Jumper wires

## Installation

1. Clone this repository:

   ```sh
   git clone https://github.com/yourusername/Arduino-Watering-System.git
   cd Arduino-Watering-System
   ```

2. Install Mosquitto clients for MQTT communication:

   - **On Debian/Ubuntu**:

     ```sh
     sudo apt-get install mosquitto-clients
     ```

   - **On Windows**:
     1. Download the Mosquitto installer from the [Mosquitto download page](https://mosquitto.org/download/).
     2. Run the installer and ensure the "Mosquitto Command Line Client Tools" option is selected.
     3. Add the installation directory (e.g., `C:\Program Files\Mosquitto`) to your system's PATH environment variable. This allows you to use the `mosquitto_pub` and `mosquitto_sub` commands from the terminal.

3. Install Python dependencies (required if using the Python script):

   ```sh
   pip install -r requirements.txt
   ```

4. Upload the Arduino sketch:

   - Use `auto_watering.ino` for automatic moisture-based watering.
   - Use `manual_watering.ino` for MQTT manual control.

## MQTT Configuration

- **Broker**: `test.mosquitto.org` (public broker)
- **Soil Moisture Topic**: `arduino/soil_moisture` (subscribe)
- **Relay Control Topic**: `arduino/relay_control` (publish)
- **Command Format**: Send JSON payload `{ "relay_on": true }` or `{ "relay_on": false }`

## Usage

### Automatic Mode

The system will water plants automatically when the soil moisture drops below a threshold.

### Manual Control via MQTT

#### Subscribe to Soil Moisture Data

```sh
mosquitto_sub -h test.mosquitto.org -t "arduino/soil_moisture"
```

#### Control the Water Pump

**Turn the relay ON:**

```sh
mosquitto_pub -h test.mosquitto.org -t "arduino/relay_control" -m '{\"relay_on\": true}'
```

**Turn the relay OFF:**

```sh

mosquitto_pub -h test.mosquitto.org -t "arduino/relay_control" -m '{\"relay_on\": false}'
```

## Python MQTT Handler (Optional)

If using the included Python script for relay control:

Run the script:

```sh
python python_control/mqtt_relay_control.py
```

Ensure the script is configured to subscribe to `arduino/relay_control` and parse JSON payloads.

## Contributing

Contributions are welcome! Fork the repository and submit pull requests.

## License

This project is licensed under the MIT License.
