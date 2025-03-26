import serial
import json
import paho.mqtt.client as mqtt

SERIAL_PORT = 'COM4'
BAUD_RATE = 9600
BROKER = "test.mosquitto.org"
TELEMETRY_TOPIC = "arduino/soil_moisture"
COMMAND_TOPIC = "arduino/relay_control"

def on_message(client, userdata, message):
    """Updated callback signature for API v2.x"""
    global serial_connection
    try:
        if message.topic == COMMAND_TOPIC:
            payload = json.loads(message.payload.decode())
            if payload["relay_on"]:
                serial_connection.write(b"RELAY_ON\n")
            else:
                serial_connection.write(b"RELAY_OFF\n")
    except Exception as e:
        print(f"Error handling message: {e}")

def main():
    global serial_connection
    serial_connection = None
    client = None
    
    try:
        # Initialize Serial
        serial_connection = serial.Serial(SERIAL_PORT, BAUD_RATE)
        
        # Initialize MQTT with version 2 API
        client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2,  # <-- Key change here
            client_id="arduino_bridge"
        )
        client.on_message = on_message
        client.connect(BROKER)
        client.subscribe(COMMAND_TOPIC)
        client.loop_start()

        print("Bridge running. Press Ctrl+C to exit")
        
        # Main loop
        while True:
            if serial_connection.in_waiting:
                line = serial_connection.readline().decode().strip()
                if line.startswith("SOIL:"):
                    moisture = int(line.split(":")[1])
                    client.publish(TELEMETRY_TOPIC, json.dumps({"soil_moisture": moisture}))
    
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        # Cleanup with proper order and checks
        if client:
            client.loop_stop()
            if client.is_connected():
                client.disconnect()
        if serial_connection and serial_connection.is_open:
            serial_connection.close()

if __name__ == "__main__":
    main()