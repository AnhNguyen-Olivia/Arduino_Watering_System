import serial
import json
import paho.mqtt.client as mqtt
import threading
import time

SERIAL_PORT = 'COM4'
BAUD_RATE = 9600
BROKER = "test.mosquitto.org"
TELEMETRY_TOPIC = "arduino/soil_moisture"
COMMAND_TOPIC = "arduino/relay_control"

# Global variables for watering control
watering_active = False
watering_lock = threading.Lock()

def on_message(client, userdata, message):
    global serial_connection  # Global declaration for serial_connection
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

def control_relay():
    global watering_active, serial_connection  # Declare watering_active as global here
    try:
        # Turn relay ON
        serial_connection.write(b"RELAY_ON\n")
        print("Relay activated - watering started")
        time.sleep(5)  # Watering duration
        
        # Turn relay OFF
        serial_connection.write(b"RELAY_OFF\n")
        print("Relay deactivated - watering stopped")
        time.sleep(20)  # Stabilization period
        
    except Exception as e:
        print(f"Error in relay control: {e}")
    finally:
        with watering_lock:
            watering_active = False

def main():
    global serial_connection, watering_active  # Declare watering_active as global here
    watering_active = False  # Initialize watering_active
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

if __name__ == "__main__":
    main()
