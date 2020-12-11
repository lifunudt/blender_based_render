# blender --background --python run.py  -- <config> [<args>]
import bpy
import sys
import os

# Make sure the current script directory is in PATH, so we can load other python modules
dir = "."  # From CLI
if not dir in sys.path:
    sys.path.append(dir)

# Add path to custom packages inside the blender main directory
sys.path.append(os.path.join(os.path.dirname(sys.executable), "custom-python-packages"))
from src.utility.ConfigParser import ConfigParser


# Read args
argv = sys.argv
batch_index_file = None

if "--batch-process" in argv:
	batch_index_file = argv[argv.index("--batch-process") + 1]

argv = argv[argv.index("--") + 1:]
working_dir = os.path.dirname(os.path.abspath(__file__))

from src.main.Pipeline import Pipeline

config_path = argv[0]

config_parser = ConfigParser()
config = config_parser.parse(config_path, argv[1:]) # Don't parse placeholder args in batch mode.
setup_config = config["setup"]

if "bop_toolkit_path" in setup_config:
    sys.path.append(setup_config["bop_toolkit_path"])
else:
    print('ERROR: Please download the bop_toolkit package and set bop_toolkit_path in config:')
    print('https://github.com/thodan/bop_toolkit')

if batch_index_file == None:
	pipeline = Pipeline(config_path, argv[1:], working_dir)
	pipeline.run()
else:
	with open(Utility.resolve_path(batch_index_file), "r") as f:
		lines = f.readlines()

		for line in lines:
			args = line.split(" ")
			pipeline = Pipeline(config_path, args, working_dir)
			pipeline.run()
