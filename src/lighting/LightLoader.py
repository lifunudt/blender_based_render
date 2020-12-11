import mathutils
import bpy

from src.lighting.LightModule import LightModule
from src.utility.Utility import Utility


class LightLoader(LightModule):
    """ Loads light source\'s settings and sets them.

    Settings can be defined in the config file in the corresponding section or in the external file.
    
    **Configuration**:

    .. csv-table::
       :header: "Parameter", "Description"
    
       "lights", "A list of dicts, where each entry describes one light. See next table for which properties can be used."
       "path", "Optionally, a path to a file which specifies one light source position, type, etc. per line. The lines has to be formatted as specified in 'file_format'."
       "file_format", "A string which specifies how each line of the given file is formatted. The string should contain the keywords of the corresponding properties separated by a space. See LightModule for allowed properties."
    """

    def __init__(self, config):
        LightModule.__init__(self, config)
        # A dict specifying the length of parameters that require more than one argument. If not specified, 1 is assumed.
        self.number_of_arguments_per_parameter = {
            "location": 3,
            "rotation": 3,
            "color": 3
        }

    def run(self):
        """ Sets light sources from config and loads them from file. """
        self.light_source_collection.add_items_from_dicts(self.config.get_list("lights", []))
        self.light_source_collection.add_items_from_file(self.config.get_string("path", ""), self.config.get_string("file_format", ""), self.number_of_arguments_per_parameter)