""" Test MQTT client that publishes messages from stdin
"""
import argparse
import logging
import sys

from drift_mqtt import Client


logging.basicConfig(level=logging.INFO)


def main():
    parser = argparse.ArgumentParser(description="Publish messages from stdin")
    parser.add_argument(
        "--uri", type=str, default="tcp://0.0.0.0:1883", help="protocol://host:port"
    )
    parser.add_argument("--topic", type=str, help="topic")
    args = parser.parse_args()

    client = Client(uri=args.uri, client_id="test_publisher")
    client.connect()
    client.loop_start()

    print("Waiting for input...")
    while True:
        line = input()
        client.publish(args.topic, line)
        print("sent to", args.topic)

    print("Exiting...")


if __name__ == "__main__":
    sys.exit(main())
