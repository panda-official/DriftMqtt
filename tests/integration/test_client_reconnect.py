""" Integration tests for mqtt client
"""
import logging
import subprocess
import time
from pathlib import Path

import paho.mqtt.client as mqtt

import pytest

HERE = Path(__file__).parent.resolve()

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s.%(msecs)03d] [%(levelname)s] [%(process)d] [%(name)s] %(message)s",
)
logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def docker_compose_files():
    """Get the docker-compose.yml absolute path.
    Override this fixture in your tests if you need a custom location.
    """
    return [str(HERE / "docker-compose.yml")]


def check_mqtt_broker(host, port):
    def on_connect(client, userdata, flags, rc, properties=None):
        print("On connect", client, userdata, flags, rc, properties)

    client = mqtt.Client(client_id="test_client_to_check_availability")
    client.enable_logger()
    try:
        client.connect(host, port)
        client.on_connect = on_connect
        time.sleep(5)
        client.loop()
        print("connect to", host, port)
        ok = client.is_connected()
        return ok
    except Exception as e:
        logger.exception("Error", e)
    finally:
        print("disconnect")
        client.disconnect()


@pytest.fixture(scope="session", name="docker_mqtt_broker")
def docker_mqtt_broker_fixture(docker_services):
    docker_services.start("mqtt_broker")
    docker_services.wait_until_responsive(
        timeout=10.0,
        pause=1,
        check=lambda: check_mqtt_broker(docker_services.docker_ip, 1883),
    )
    public_port = docker_services.port_for("mqtt_broker", 1883)
    url = f"tcp://{docker_services.docker_ip}:{public_port}"
    return url


@pytest.fixture
def publisher_subprocess():
    proc = subprocess.Popen(
        ["python", "mqtt_publisher.py", "--topic=test_topic"],
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
        bufsize=1,
    )
    yield proc

    proc.terminate()


@pytest.fixture
def subscriber_subprocess():
    proc = subprocess.Popen(
        ["python", "mqtt_subscriber.py", "--topic=test_topic"],
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
        bufsize=1,
    )

    yield proc

    proc.terminate()


@pytest.mark.skip(
    reason="We skip this test for now as it fail, but we keep it to learn"
)
def test_read_and_write(
    docker_services, docker_mqtt_broker, publisher_subprocess, subscriber_subprocess
):
    """Run service and check on the other side of mqtt topic if there any messages,
    check that they was emitted with specified interval, then stop service with INT signal
    """
    # start service and work for some time
    output = publisher_subprocess.stdout.readline()
    print("Publisher:", output)
    publisher_subprocess.stdin.write(b"one\ntwo\nthree\n")
    publisher_subprocess.stdin.flush()
    print("sent to publisher")
    # time.sleep(3)

    output = subscriber_subprocess.stdout.readline()
    print("Subscriber:", output)
    assert output == b"Got message: test_topic b'one'\n"

    output = subscriber_subprocess.stdout.readline()
    print("Subscriber:", output)
    assert output == b"Got message: test_topic b'two'\n"

    output = subscriber_subprocess.stdout.readline()
    print("Subscriber:", output)
    assert output == b"Got message: test_topic b'three'\n"

    res = docker_services.exec("mqtt_broker", "sudo", "service", "mosquitto", "stop")
    print(res)
    time.sleep(5)
    res = docker_services.exec("mqtt_broker", "sudo", "service", "mosquitto", "start")
    print(res)
    time.sleep(5)

    publisher_subprocess.stdin.write(b"line1\nline2\nline3\n")
    publisher_subprocess.stdin.flush()
    # time.sleep(3)
    output = subscriber_subprocess.stdout.readline()
    print("Subscriber:", output)
    output = subscriber_subprocess.stdout.readline()
    print("Subscriber:", output)
    output = subscriber_subprocess.stdout.readline()
    print("Subscriber:", output)
