import serial
import json
import paho.mqtt.client as mqtt

# Configure your Arduino's serial port
SERIAL_PORT = 'COM4'  # Replace with your port (e.g., '/dev/ttyUSB0' on Linux/macOS)
BAUD_RATE = 9600

# MQTT Configuration
BROKER = "test.mosquitto.org"
TELEMETRY_TOPIC = "arduino/soil_moisture"
COMMAND_TOPIC = "arduino/relay_control"

def on_message(client, userdata, msg):
    if msg.topic == COMMAND_TOPIC:
        payload = json.loads(msg.payload.decode())
        if payload["relay_on"]:
            serial_connection.write(b"RELAY_ON\n")  # Send command to Arduino
        else:
            serial_connection.write(b"RELAY_OFF\n")

def main():
    try:
        # Initialize Serial
        global serial_connection
        serial_connection = serial.Serial(SERIAL_PORT, BAUD_RATE)
        
        # Initialize MQTT
        client = mqtt.Client("arduino_bridge", callback_api_version=mqtt.CallbackAPIVersion.VERSION1)
        client.connect(BROKER)
        client.subscribe(COMMAND_TOPIC)
        client.on_message = on_message
        client.loop_start()

        print("Bridge running. Press Ctrl+C to exit.")
        
        # Main loop
        while True:
            if serial_connection.in_waiting:
                line = serial_connection.readline().decode().strip()
                if line.startswith("SOIL:"):
                    moisture = int(line.split(":")[1])
                    client.publish(TELEMETRY_TOPIC, json.dumps({"soil_moisture": moisture}))
    except serial.SerialException as e:
        print(f"Error initializing serial connection on {SERIAL_PORT}: {e}")
        print("Ensure the port is correct and not in use by another application.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Cleanup resources
        try:
            serial_connection.close()
        except NameError:
            pass
        try:
            client.disconnect()
        except NameError:
            pass

if __name__ == "__main__":
    main()