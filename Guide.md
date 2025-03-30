# Arduino MQTT Bridge - Code Explanation

This document provides a detailed breakdown of how each part of the Python code works to create a bridge between an Arduino soil moisture sensor and an MQTT broker.

## Importing Required Modules

```python
import serial
import json
import paho.mqtt.client as mqtt
import threading
import time
```

- `serial`: Handles communication with the Arduino via a serial port.
- `json`: Used to encode and decode JSON messages for MQTT communication.
- `paho.mqtt.client`: Provides MQTT client functionality for sending and receiving messages.
- `threading`: Allows running tasks concurrently, preventing blocking operations.
- `time`: Used for delays and sleep functions in the relay control.

## Configuration Variables

```python
SERIAL_PORT = 'COM4'
BAUD_RATE = 9600
BROKER = "test.mosquitto.org"
TELEMETRY_TOPIC = "arduino/soil_moisture"
COMMAND_TOPIC = "arduino/relay_control"
```

- `SERIAL_PORT`: Defines the serial port where the Arduino is connected.
- `BAUD_RATE`: Communication speed between the Arduino and the computer.
- `BROKER`: The MQTT broker's address (using a public Mosquitto broker for testing).
- `TELEMETRY_TOPIC`: The topic where soil moisture data will be published.
- `COMMAND_TOPIC`: The topic where relay control commands will be received.

## Global Variables for Watering Control

```python
watering_active = False
watering_lock = threading.Lock()
```

- `watering_active`: A flag to prevent multiple watering processes from running simultaneously.
- `watering_lock`: A threading lock to synchronize access to `watering_active`.

## MQTT Message Handling

```python
def on_message(client, userdata, message):
    global serial_connection
    try:
        if message.topic == COMMAND_TOPIC:
            raw_payload = message.payload.decode()
            print(f"Received raw payload: {raw_payload}")
            
            payload = json.loads(raw_payload)
            
            if payload["relay_on"]:
                serial_connection.write(b"RELAY_ON\n")
            else:
                serial_connection.write(b"RELAY_OFF\n")
                
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}")
    except KeyError as e:
        print(f"Missing key 'relay_on' in payload")
    except Exception as e:
        print(f"Error handling message: {e}")
```

- This function listens for incomi
ng MQTT messages on `COMMAND_TOPIC`.
- Decodes the message and extracts the JSON payload.
- If `relay_on` is `true`, it sends the `RELAY_ON` command to the Arduino.
- If `relay_on` is `false`, it sends the `RELAY_OFF` command.
- Error handling ensures invalid messages don’t crash the program.

## Controlling the Relay Automatically

```python
def control_relay():
    global watering_active, serial_connection
    try:
        serial_connection.write(b"RELAY_ON\n")
        print("Relay activated - watering started")
        time.sleep(5)
        
        serial_connection.write(b"RELAY_OFF\n")
        print("Relay deactivated - watering stopped")
        time.sleep(20)
        
    except Exception as e:
        print(f"Error in relay control: {e}")
    finally:
        with watering_lock:
            watering_active = False
```

- Turns the relay on for **5 seconds**.
- Turns it off and waits **20 seconds** before another cycle can start.
- Uses a `try-except-finally` block to ensure `watering_active` is reset even if an error occurs.

## Main Function

```python
def main():
    global serial_connection, watering_active
    watering_active = False
    serial_connection = None
    client = None
    
    try:
        serial_connection = serial.Serial(SERIAL_PORT, BAUD_RATE)
        client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2,
            client_id="arduino_bridge"
        )
        client.on_message = on_message
        client.connect(BROKER)
        client.subscribe(COMMAND_TOPIC)
        client.loop_start()

        print("Bridge running. Press Ctrl+C to exit")
        while True:
            if serial_connection.in_waiting:
                line = serial_connection.readline().decode().strip()
                if line.startswith("SOIL:"):
                    moisture = int(line.split(":")[1])
                    client.publish(TELEMETRY_TOPIC, json.dumps({"soil_moisture": moisture}))
                    
                    # Automatic control logic
                    if moisture > 450:
                        with watering_lock:
                            if not watering_active:
                                watering_active = True
                                threading.Thread(target=control_relay).start()
                                print(f"Low moisture detected ({moisture}), starting watering cycle")
                    else:
                        with watering_lock:
                            if watering_active:
                                watering_active = False
                                print(f"Moisture level sufficient ({moisture}), stopping watering cycle")    
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if client:
            client.loop_stop()
            if client.is_connected():
                client.disconnect()
        if serial_connection and serial_connection.is_open:
            serial_connection.close()
```

### **Breakdown:**

- Establishes a serial connection with the Arduino.
- Creates an MQTT client and connects to the broker.
- Subscribes to `COMMAND_TOPIC` for receiving manual commands.
- Enters a loop to constantly check for **incoming sensor data**.
- Extracts **moisture readings** from serial input.
- If moisture is **too low (> 450)**, starts watering using `control_relay()`.
- Ensures safe shutdown by closing MQTT and serial connections if an error occurs.

## Entry Point

```python
if __name__ == "__main__":
    main()
```

- Ensures the script only runs when executed directly, not when imported as a module.

---

### Summary

This Python script acts as a **bridge** between an Arduino and an MQTT broker, allowing:
✅ **Real-time soil moisture monitoring**
✅ **Automatic watering based on moisture levels**
✅ **Manual relay control via MQTT commands**
