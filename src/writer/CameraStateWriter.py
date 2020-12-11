from src.utility.ItemWriter import ItemWriter
import bpy
import os

from src.writer.StateWriter import StateWriter


class CameraStateWriter(StateWriter):
    """ Writes the state of all camera poses to a file.

    **Attributes per object**:

    .. csv-table::
       :header: "Keyword", "Description"

       "fov_x", "The horizontal FOV."
       "fov_y", "The vertical FOV."
       "half_fov_x", "Half of the horizontal FOV."
       "half_fov_y", "Half of the vertical FOV."
    """

    def __init__(self, config):
        StateWriter.__init__(self, config)
        self.object_writer = ItemWriter(self._get_attribute)

    def run(self):
        # Collect camera and camera object
        cam_ob = bpy.context.scene.camera
        cam = cam_ob.data
        cam_pose = (cam, cam_ob)

        self.write_attributes_to_file(self.object_writer, [cam_pose], "campose_", "campose", ["id", "location", "rotation_euler", "fov_x", "fov_y", "shift_x", "shift_y"])

    def _get_attribute(self, cam_pose, attribute_name):
        """ Returns the value of the requested attribute for the given object.

        :param cam_pose: The mesh object.
        :param attribute_name: The attribute name.
        :return: The attribute value.
        """
        cam, cam_ob = cam_pose

        if attribute_name == "fov_x":
            return cam.angle_x
        elif attribute_name == "fov_y":
            return cam.angle_y
        elif attribute_name == "shift_x":
            return cam.shift_x
        elif attribute_name == "shift_y":
            return cam.shift_y
        elif attribute_name == "half_fov_x":
            return cam.angle_x * 0.5
        elif attribute_name == "half_fov_y":
            return cam.angle_y * 0.5
        else:
            return super()._get_attribute(cam_ob, attribute_name)
