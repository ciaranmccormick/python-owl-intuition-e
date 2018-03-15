"""

"""
import logging
import re

logger = logging.getLogger(__name__)


class OWLDevice(object):
    def __init__(self, owl_id=None, last_update=None, signal_strength=None,
                 link_quality=None, battery_level=None):
        """

        Args:
            owl_id (str):
            last_update (long):
            signal_strength (float):
            link_quality (float):
            battery_level (float):
        """
        self.owl_id = owl_id
        self.last_update = last_update
        self.signal_strength = signal_strength
        self.battery_level = battery_level
        self.link_quality = link_quality

    @classmethod
    def from_string(cls, xml_string):
        """Read the device attributes from the OWL message buffer.

        """
        pattern = (r"<electricity id='(.*)'><timestamp>([0-9]*)<.*"
                   r".*rssi='(-[0-9]+)' lqi='([0-9]+)'.*"
                   r"level='([0-9]+)%.*")
        try:
            result = re.match(pattern, xml_string)
            if result is not None:
                owl_id = result.group(1)
                last_update = int(result.group(2))
                signal_strength = float(result.group(3))
                link_quality = float(result.group(4))
                battery_level = float(result.group(5))
                return cls(owl_id=owl_id, last_update=last_update,
                           signal_strength=signal_strength,
                           link_quality=link_quality,
                           battery_level=battery_level)
            else:
                return OWLDevice()
        except TypeError as error:
            logger.error(error)
            return OWLDevice()


class OWLEnergyReading(object):
    def __init__(self, channel=0, owl_id=None, current=None, total_current=None,
                 xml_string=None):
        """

        Args:
            channel (int):
            owl_id (str):
            current (float):
            total_current (float):
            xml_string (str):
        """
        self.current = current
        self.total_current = total_current
        self.channel = channel
        self.owl_id = owl_id

        if xml_string is not None:
            self.process_xml(xml_string)

    def process_xml(self, raw_data):
        """Extracts data from the OWL data buffer that matches the pattern.

        """
        pattern = (r"<electricity id='(.*)'><timestamp>.*chan id='({})'>"
                   r"<curr units='w'>([0-9]+\.[0-9]+)</curr>"
                   r"<day units='wh'>([0-9]+\.[0-9]+)"
                   r"</day.*").format(self.channel)

        try:
            result = re.match(pattern, raw_data)

            if result is not None:
                self.owl_id = result.group(1)
                self.channel = int(result.group(2))
                self.current = float(result.group(3))
                logger.debug("current: %f", self.current)
                self.total_current = float(result.group(4))
                logger.debug("total current: %f", self.total_current)
            else:
                logger.warning("No data available on channel %s", self.channel)

        except TypeError as error:
            logger.error(error)
