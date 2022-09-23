import logging
import sys

from drift_mqtt import Client


logging.basicConfig(level=logging.INFO)


def main():
    client = Client("tcp://0.0.0.0:1883", client_id="test_publisher")
    client.connect()
    client.loop_start()
    client.publish("topic", "some message")


if __name__ == "__main__":
    sys.exit(main())
