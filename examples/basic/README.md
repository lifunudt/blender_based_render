# Basic scene

## Usage

Execute in the Blender-Pipeline main directory:

```
python run.py examples/basic/config.yaml examples/basic/camera_positions examples/basic/scene.obj examples/basic/output
```

Here `examples/basic/config.yaml` is the config file which defines the structure and properties of the pipeline.
The three arguments afterwards are used to fill placeholders like `<args:0>` inside this config file. 

## Steps

* Loads `scene.obj`
* Creates a point light
* Loads camera positions from `camera_positions`
* Renders normals
* Renders rgb

## Explanation of the config file

### Setup
```yaml
  "setup": {
    "blender_install_path": "/home_local/<env:USER>/blender/",
    "blender_version": "blender-2.81-linux-glibc217-x86_64",
    "pip": [
      "h5py",
      "imageio"
    ]
  }
```

* blender is installed into `/home_local/<env:USER>/blender/` where `<env:USER>` is automatically replaced by the username
* we want to use blender 2.8 (installation is done automatically on the first run)
* inside the blender python environment the python packages `h5py` and `imageio` should be automatically installed. These are not provided per default, but are required in order to make the `writer.Hdf5Writer` module work.

### Global

```yaml
  "global": {
    "all": {
      "output_dir": "<args:2>"
    }
  }
```

* In the global section, we just specify the `output_dir` which defines where the final files should be stored.
* As this configuration is defined in `global/all`, it is inherited by all modules. This is equivalent to just putting the `output_dir` configuration into the `config` block of each single module.
* As we don't want to hardcode this path here, the `output_dir` is automatically replaced by the third argument given when running the pipeline. In the upper command the output path is set to `examples/basic/output`.

### Modules

Under `modules` we list all modules we want the pipeline to execute. The order also defines the order in which they are executed.
Every module has a name which specifies the python path to the corresponding class starting from the `src` directory and a `config` dict where we can configure the module to our needs.

#### Initalizer

```yaml
 {
  "name": "main.Initializer",
  "config": {}
}
```

* This module does some basic initialization of the blender project (e.q. sets background color, configures computing device, creates camera)
* We are using the default parameters here, so `config` is empty

#### ObjectLoader

```yaml
{
  "name": "loader.ObjectLoader",
  "config": {
    "path": "<args:1>"
  }
}
```

* This module imports an .obj file into the scene
* The path of the .obj file should be configured via the parameter `path`
* Here we are using the second argument given, in the upper command the output path is set to `examples/basic/scene.obj`


#### LightLoader

```yaml
{
  "name": "lighting.LightLoader",
  "config": {
    "lights": [
      {
        "type": "POINT",
        "location": [5, -5, 5],
        "energy": 1000
      }
    ]
  }
}
```

* This module creates a point light
* The properties of this light are configured via the parameter `lights`


#### CameraLoader

```yaml
{
  "name": "camera.CameraLoader",
  "config": {
    "path": "<args:0>",
    "file_format": "location rotation/value",
    "default_cam_param": {
      "fov": 1
    }
  }
}
```

* This module imports the camera poses which defines from where the renderings should be taken
* The camera positions are defined in a file whose path is again given via the command line (`examples/basic/camera_positions` - contains 2 cam poses)
* The file uses the following format which is defined at `file_format`
```
location_x location_y location_z  rotation_euler_x rotation_euler_y rotation_euler_z
```
* The FOV is the same for all cameras and is therefore set inside `default_cam_param`
* This module also writes the cam poses into extra `.npy` files located inside the `temp_dir` (default: /dev/shm/blender_proc_$pid). This is just some meta information, so we can later clearly say which image had been taken using which cam pose.

=> Creates the files `campose_0001.npy` and `campose_0002.npy` 

#### NormalRenderer

```yaml
{
  "name": "renderer.NormalRenderer",
  "config": {
      "output_key": "normals"
  }
}
```

* This module just goes through all cam poses which were defined in the previous model and renders a normal image for each of them
* The images are rendered using the `.exr` format which allows linear colorspace and higher precision
* The output files are stored in the defined output directory (see [Global](#Global)) and are named like `i.exr` where `i` is the cam pose index
* The `output_key` config is relevant for the last module, as it defines the key at which the normal rendering should be stored inside the `.hdf5` files.

=> Creates the files `normal_0001.exr` and `normal_0002.exr` 

#### RgbRenderer

```yaml
{
  "name": "renderer.RgbRenderer",
  "config": {
     "output_key": "colors",
     "samples": 350
  }
}
```

* This module just goes through all cam poses and renders a rgb image for each of them
* In this case we increase the number of samples used for raytracing which increases the rendering quality
* We again set the `output_key`, here to `colors`

=> Creates the files `rgb_0001.png` and `rgb_0002.png`

#### Hdf5Writer

```yaml
{
  "name": "writer.Hdf5Writer",
  "config": {
  }
}
```

* The last module now merges all the single temporary files created by the two rendering modules into one `.hdf5` file per cam pose
* A `.hdf5` file can be seen as a dict of numpy arrays, where the keys correspond to the `output_key` defined before

The file `1.h5py` would therefore look like the following:
```yaml
{
  "normals": #<numpy array with pixel values read in from normal_0001.exr>,
  "colors": #<numpy array with pixel values read in from rgb_0001.png>,
  "campose": #<numpy array with cam pose read in from campose_0001.npy>
}
``` 

* At the end of the hdf5 writer all temporary files are deleted

=> Creates the files `1.h5py` and `2.h5py`