from src.utility.ItemWriter import ItemWriter
import bpy
import os

from src.writer.StateWriter import StateWriter


class ObjectStateWriter(StateWriter):
    """ Writes the state of all objects for each frame to a file.

    **Attributes per object**:

    .. csv-table::
       :header: "Keyword", "Description"
    """

    def __init__(self, config):
        StateWriter.__init__(self, config)
        self.object_writer = ItemWriter(self._get_attribute)

    def run(self):
        # Collect all mesh objects
        objects = []
        for object in bpy.context.scene.objects:
            if object.type == 'MESH':
                objects.append(object)

        self.write_attributes_to_file(self.object_writer, objects, "object_states_", "object_states", ["id", "location", "rotation_euler"])

    def _get_attribute(self, object, attribute_name):
        """ Returns the value of the requested attribute for the given object.

        :param object: The mesh object.
        :param attribute_name: The attribute name.
        :return: The attribute value.
        """
        return super()._get_attribute(object, attribute_name)
