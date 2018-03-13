import unittest
import socket

from owlenergy.client import OWLClient
from owlenergy.owl import OWLEnergyReading, OWLDevice


class OWLDeviceTestCase(unittest.TestCase):

    def setUp(self):
        self.test_data = ("<electricity id='4437190077C6'>"
                          "<timestamp>1520612469</timestamp>"
                          "<signal rssi='-65' lqi='98'/>"
                          "<battery level='100%'/>"
                          "<chan id='0'>"
                          "<curr units='w'>2431.00</curr>"
                          "<day units='wh'>5307.82</day>"
                          "</chan>"
                          "<chan id='1'>"
                          "<curr units='w'>0.00</curr>"
                          "<day units='wh'>0.00</day>"
                          "</chan>"
                          "<chan id='2'>"
                          "<curr units='w'>0.00</curr>"
                          "<day units='wh'>0.00</day>"
                          "</chan>"
                          "</electricity>")

    def tearDown(self):
        pass

    def test_process_xml_normal_input(self):
        """Test for normal execution when data is passed to process_xml

        Returns:
            None
        """
        device = OWLDevice()
        device.process_xml(self.test_data)
        self.assertEqual(device.last_update, 1520612469)
        self.assertEqual(device.signal_strength, -65.0)
        self.assertEqual(device.link_quality, 98.0)
        self.assertEqual(device.battery_level, 100.0)

    def test_process_xml_no_input(self):
        """Test for when no data is passed

        Returns:
            None
        """
        device = OWLDevice()
        device.process_xml(None)
        self.assertEqual(device.last_update, None)
        self.assertEqual(device.signal_strength, None)
        self.assertEqual(device.link_quality, None)
        self.assertEqual(device.battery_level, None)

    def test_process_xml_no_match(self):
        """Test for when no matches are found.

        Returns:
            None
        """
        device = OWLDevice()
        device.process_xml("this text will not match.")
        self.assertEqual(device.last_update, None)
        self.assertEqual(device.signal_strength, None)
        self.assertEqual(device.link_quality, None)
        self.assertEqual(device.battery_level, None)

    def test_process_xml_auto(self):
        """Test for when xml is passed when device is created.

        Returns:
            None
        """
        device = OWLDevice(xml_string=self.test_data)
        self.assertEqual(device.last_update, 1520612469)
        self.assertEqual(device.signal_strength, -65.0)
        self.assertEqual(device.link_quality, 98.0)
        self.assertEqual(device.battery_level, 100.0)


class OWLEnergyReadingTestCase(unittest.TestCase):
    def setUp(self):
        self.test_data = ("<electricity id='4437190077C6'>"
                          "<timestamp>1520612469</timestamp>"
                          "<signal rssi='-65' lqi='98'/>"
                          "<battery level='100%'/>"
                          "<chan id='0'>"
                          "<curr units='w'>2431.00</curr>"
                          "<day units='wh'>5307.82</day>"
                          "</chan>"
                          "<chan id='1'>"
                          "<curr units='w'>0.00</curr>"
                          "<day units='wh'>0.00</day>"
                          "</chan>"
                          "<chan id='2'>"
                          "<curr units='w'>0.00</curr>"
                          "<day units='wh'>0.00</day>"
                          "</chan>"
                          "</electricity>")

    def tearDown(self):
        pass

    def test_process_xml_normal(self):
        """Test normal execution with no channel specified.

        Returns:
            None
        """
        energy_reading_0 = OWLEnergyReading()
        energy_reading_0.process_xml(self.test_data)
        self.assertEqual(energy_reading_0.channel, 0)
        self.assertEqual(energy_reading_0.owl_id, '4437190077C6')
        self.assertEqual(energy_reading_0.current, 2431.00)
        self.assertEqual(energy_reading_0.total_current, 5307.82)

    def test_process_xml_normal_specified_channel(self):
        """Test normal execution when channel is specified.

        Returns:

        """
        reading = OWLEnergyReading(channel=1)
        reading.process_xml(self.test_data)
        self.assertEqual(reading.channel, 1)
        self.assertEqual(reading.owl_id, '4437190077C6')
        self.assertEqual(reading.current, 0.0)
        self.assertEqual(reading.total_current, 0.0)

    def test_process_xml_no_input(self):
        """

        Returns:

        """
        reading = OWLEnergyReading()
        reading.process_xml(None)
        self.assertEqual(reading.channel, 0)
        self.assertEqual(reading.owl_id, None)
        self.assertEqual(reading.current, None)
        self.assertEqual(reading.total_current, None)

    def test_process_xml_auto(self):
        """

        Returns:

        """
        reading = OWLEnergyReading(xml_string=self.test_data)
        self.assertEqual(reading.channel, 0)
        self.assertEqual(reading.owl_id, '4437190077C6')
        self.assertEqual(reading.current, 2431.00)
        self.assertEqual(reading.total_current, 5307.82)

    def test_process_xml_no_match(self):
        """

        Returns:

        """
        reading = OWLEnergyReading()
        reading.process_xml("This will not match")
        self.assertEqual(reading.channel, 0)
        self.assertEqual(reading.owl_id, None)
        self.assertEqual(reading.current, None)
        self.assertEqual(reading.total_current, None)


class OWLClientTestCase(unittest.TestCase):

    def setUp(self):
        self.client = OWLClient()

    def tearDown(self):
        self.client._destroy_socket()

    def test_destroy_socket(self):
        self.client._destroy_socket()
        self.assertEqual(self.client.socket, None)

    def test_create_socket(self):
        self.client.initialise_socket()
        self.assertIsInstance(self.client.socket, socket.socket)


if __name__ == '__main__':
    unittest.main()
