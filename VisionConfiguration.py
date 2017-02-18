import ConfigParser as cP
import numpy as np

H_LOW_KEY = 'h_low'
H_HIGH_KEY = 'h_high'
S_LOW_KEY = 's_low'
S_HIGH_KEY = 's_high'
V_LOW_KEY = 'v_low'
V_HIGH_KEY = 'v_high'

EXPOSURE_KEY = 'exposure'
WB_BLUE_KEY = 'wb_blue'
WB_RED_KEY = 'wb_red'
BRIGHTNESS_KEY = 'brightness'
CONTRAST_KEY = 'contrast'

FILE_LOCATION = 'config.properties'

RANGE_SECTION = 'color_ranges'
CAMERA_PROP_SECTION = 'camera_props'

class VisionConfiguration(object):
    def __init__(self):
        self.config = cP.RawConfigParser()
        self.config.read(FILE_LOCATION)

    def set_key(self, section, key, value):
        """
        Set a key in the config file
        """
        try:
            self.config.add_section(section)
        except cP.DuplicateSectionError:
            pass

        self.config.set(section, key, value)

    def sync(self):
        """
        Sync configuration changes to the disk
        """
        self.config.write(open(FILE_LOCATION,'w'))

    def get_key(self, section, key, default_value):
        """
        Gets a key from the configuration file
        """
        try:
            return self.config.getint(section, key)
        except cP.NoSectionError:
            pass
        except cP.NoOptionError:
            pass
        except ValueError:
            return self.config.getfloat(section, key)
        return default_value

    @property
    def exposure(self):
        return self.get_key(CAMERA_PROP_SECTION, EXPOSURE_KEY, 0.69)

    @exposure.setter
    def exposure(self, value):
        self.set_key(CAMERA_PROP_SECTION, EXPOSURE_KEY, value)

    @property
    def white_balance_blue(self):
        return self.get_key(CAMERA_PROP_SECTION, WB_BLUE_KEY, 0.69)

    @white_balance_blue.setter
    def white_balance_blue(self, value):
        self.set_key(CAMERA_PROP_SECTION, WB_BLUE_KEY, value)

    @property
    def white_balance_red(self):
        return self.get_key(CAMERA_PROP_SECTION, WB_RED_KEY, 0.69)

    @white_balance_red.setter
    def white_balance_red(self, value):
        return self.set_key(CAMERA_PROP_SECTION, WB_RED_KEY, value)

    @property
    def brightness(self):
        return self.get_key(CAMERA_PROP_SECTION, BRIGHTNESS_KEY, -0.69)

    @brightness.setter
    def brightness(self, value):
        self.set_key(CAMERA_PROP_SECTION, BRIGHTNESS_KEY, value)

    @property
    def contrast(self):
        return self.get_key(CAMERA_PROP_SECTION, CONTRAST_KEY, 0.69)

    @contrast.setter
    def contrast(self, value):
        self.set_key(CAMERA_PROP_SECTION, CONTRAST_KEY, value)
    
    @property
    def low_range(self):
        """
        Low range of the hsv values to process
        """
        h_low = self.get_key(RANGE_SECTION,H_LOW_KEY,0)
        s_low = self.get_key(RANGE_SECTION, S_LOW_KEY,0)
        v_low = self.get_key(RANGE_SECTION, V_LOW_KEY,0)
        return np.array([h_low,s_low,v_low],dtype = np.uint8)
    
    @low_range.setter
    def low_range(self, value):
        self.set_key(RANGE_SECTION, H_LOW_KEY, value[0])
        self.set_key(RANGE_SECTION, S_LOW_KEY, value[1])
        self.set_key(RANGE_SECTION, V_LOW_KEY, value[2])
        
    @property
    def high_range(self) :
        """
        High range of the hsv values to process
        """
        h_high = self.get_key(RANGE_SECTION, H_HIGH_KEY,255)
        s_high = self.get_key(RANGE_SECTION, S_HIGH_KEY, 255)
        v_high = self.get_key(RANGE_SECTION, V_HIGH_KEY,255)
        return np.array([h_high,s_high,v_high],dtype = np.uint8)
    
    @high_range.setter
    def high_range(self, value):
        self.set_key(RANGE_SECTION, H_HIGH_KEY, value[0])
        self.set_key(RANGE_SECTION, S_HIGH_KEY, value[1])
        self.set_key(RANGE_SECTION, V_HIGH_KEY, value[2])
