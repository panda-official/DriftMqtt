import logging
import sys

from drift_mqtt import Client


logging.basicConfig(level=logging.INFO)


def message_handler(message):
    print("Got message ", message.payload, message.topic)


def main():
    client = Client("tcp://0.0.0.0:1883", client_id="test_subscriber")
    client.connect()
    client.subscribe("test_topic", message_handler)
    client.loop_forever()


if __name__ == "__main__":
    sys.exit(main())
