import ConfigParser as cP
import numpy as np

H_LOW_KEY = 'h_low'
H_HIGH_KEY = 'h_high'
S_LOW_KEY = 's_low'
S_HIGH_KEY = 's_high'
V_LOW_KEY = 'v_low'
V_HIGH_KEY = 'v_high'

FILE_LOCATION = 'config.properties'

RANGE_SECTION = 'color_ranges'

class VisionConfiguration(object):
    def __init__(self):
        self.config = cP.RawConfigParser()
        self.config.read(FILE_LOCATION)

    def set_key(self, section, key, value):
        try:
            self.config.add_section(section)
        except cP.DuplicateSectionError:
            pass

        self.config.set(section, key, value)

    def get_key(self, section, key, default_value):
        try:
            return self.config.getint(section, key)
        except cP.NoSectionError:
            pass
        except cP.NoOptionError:
            pass
        return default_value
    
    @property
    def low_range(self):
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
        h_high = self.get_key(RANGE_SECTION, H_HIGH_KEY,255)
        s_high = self.get_key(RANGE_SECTION, S_HIGH_KEY, 255)
        v_high = self.get_key(RANGE_SECTION, V_HIGH_KEY,255)
        return np.array([h_high,s_high,v_high],dtype = np.uint8)
    
    @high_range.setter
    def high_range(self, value):
        self.set_key(RANGE_SECTION, H_HIGH_KEY, value[0])
        self.set_key(RANGE_SECTION, S_HIGH_KEY, value[1])
        self.set_key(RANGE_SECTION, V_HIGH_KEY, value[2])
