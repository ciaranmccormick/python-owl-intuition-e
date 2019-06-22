### OWL Energy by STRETCH


#### Installation

```bash
pip install owl-energy
```

#### Usage

```python
from owlenergy.client import OWLClient
from owlenergy.owl import OWLDevice, OWLEnergyReading

client = OWLClient(host='localhost', port=22600, msg_buffer_size=512,
                   multi_cast_address='224.192.32.19')
client.initialise_socket()
reading = client.get_reading()

if reading is not None:
    device = OWLDevice.from_string(reading)
    energy_reading = OWLEnergyReading.from_string(reading, channel=0)
```


### Example Data

```python
device.__dict__

{'battery_level': 100.0,
 'last_update': 1520612469,
 'link_quality': 98.0,
 'owl_id': '4437191177C6',
 'signal_strength': -65.0}

energy_reading.__dict__

{'channel': 0,
 'current': 2431.0,
 'owl_id': '4437190077C6',
 'total_current': 5307.82}

```
