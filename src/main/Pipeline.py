
from src.utility.ConfigParser import ConfigParser
from src.utility.Utility import Utility
import bpy

class Pipeline:

    def __init__(self, config_path, args, working_dir, should_perform_clean_up=True):
        Utility.working_dir = working_dir

        # Clean up example scene or scene created by last run when debugging pipeline inside blender
        if should_perform_clean_up:
            self._cleanup()

        config_parser = ConfigParser(silent=True)
        config = config_parser.parse(Utility.resolve_path(config_path), args)

        self.modules = Utility.initialize_modules(config["modules"], config["global"])

    def _cleanup(self):
        """ Cleanup the scene by removing objects, orphan data and custom properties """
        self._remove_all_objects()
        self._remove_orphan_data()
        self._remove_custom_properties()

    def _remove_all_objects(self):
        """ Removes all objects of the current scene """
        # Select all
        for obj in bpy.context.scene.objects:
            obj.select_set(True)
        # Delete selection
        bpy.ops.object.delete()

    def _remove_orphan_data(self):
        """ Remove all data blocks which are not used anymore. """
        data_structures = [
            bpy.data.meshes,
            bpy.data.materials,
            bpy.data.textures,
            bpy.data.images,
            bpy.data.brushes,
            bpy.data.cameras,
            bpy.data.actions,
            bpy.data.lights
        ]

        for data_structure in data_structures:
            for block in data_structure:
                # If no one uses this block => remove it
                if block.users == 0:
                    data_structure.remove(block)

    def _remove_custom_properties(self):
        """ Remove all custom properties registered at global entities like the scene. """
        for key in bpy.context.scene.keys():
            del bpy.context.scene[key]

    def run(self):
        """ Runs each module and measuring their execution time. """
        with Utility.BlockStopWatch("Running blender pipeline"):
            for module in self.modules:
                with Utility.BlockStopWatch("Running module " + module.__class__.__name__):
                    module.run()

