# Drift MQTT tools

![GitHub Workflow Status](https://img.shields.io/github/workflow/status/panda-official/DriftMqtt/ci)
![PyPI](https://img.shields.io/pypi/v/drift-mqtt)
![PyPI - Downloads](https://img.shields.io/pypi/dm/drift-mqtt)


A collection of helpers to work with MQTT:
* `Client` - wrapper around `paho.mqtt.Client` that correctly handles subscriptions after reconnect


## Installation

```bash
pip install drift-mqtt
```

Or get the latest version from GitHub:
```bash
pip install git+https://github.com/panda-official/DriftMqtt.git
```


## Usage

Producer
```python
from drift_mqtt import Client


client = Client('tcp://127.0.0.1:8000', 'client_id')
client.connect()
client.loop_start()
...
client.publish('topic', 'some message')
```
Consumer
```python
from drift_mqtt import Client


def message_handler(message):
    print('Got message ', message.payload, message.topic)


client = Client('tcp://127.0.0.1:8000', client_id='test_subscriber')
client.subscribe('test_topic', message_handler)
client.connect()
client.loop_forever()
```

For more details please check `examples/` folder
