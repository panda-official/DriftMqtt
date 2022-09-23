""" Test MQTT client that subscribes to topic and prints received messages
"""
import argparse
import logging
import sys

from drift_mqtt import Client


logging.basicConfig(level=logging.INFO)


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Subscribe and print messages")
    parser.add_argument(
        "--uri", type=str, default="tcp://0.0.0.0:1883", help="protocol://host:port"
    )
    parser.add_argument("--topic", type=str, help="topic")
    args = parser.parse_args()

    # The callback for when a PUBLISH message is received from the server.
    def on_message(msg):
        print("Got message:", msg.topic, msg.payload)

    client = Client(uri=args.uri, client_id="test_subscriber")
    client.subscribe(args.topic, on_message)
    client.connect()

    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("Exiting...")
        client.disconnect()
        client.loop_stop()


if __name__ == "__main__":
    sys.exit(main())
