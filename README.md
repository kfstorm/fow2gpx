# fow2gpx
Export your Fog of World track data to GPX files

Inspired by https://github.com/CaviarChen/fog-machine.

## Usage

```
usage: main.py [-h] --fow-path FOW_PATH --output-file OUTPUT_FILE
               [--sample-level [0-6]]

Export your Fog of World track data to GPX files.

optional arguments:
  -h, --help            show this help message and exit
  --fow-path FOW_PATH, -i FOW_PATH
                        The path of Fog of World data folder. Note that this
                        folder must contains the 'Sync' folder.
  --output-file OUTPUT_FILE, -o OUTPUT_FILE
                        The path of exported GPX file.
  --sample-level [0-6], -s [0-6]
                        The optional sample level to reduce the amount of
                        waypoints and the size of output file. Must be between
                        0 - 6. 0 means no sampling. 1 means resolution of
                        ~19m. 2 means resolution of ~38m. 3 means resolution
                        of ~76m. 4 means resolution of ~152m. 5 means
                        resolution of ~305m. 6 means resolution of ~611m.

Example: python main.py -i "/path/to/Fog of World" -o "/path/to/output.gpx"
```
