# fow2gpx
Export your Fog of World track data to GPX files

Inspired by https://github.com/CaviarChen/fog-machine.

## Usage

```
usage: main.py [-h] --fow-path FOW_PATH --output-file OUTPUT_FILE

Export your Fog of World track data to GPX files.

optional arguments:
  -h, --help            show this help message and exit
  --fow-path FOW_PATH, -i FOW_PATH
                        The path of Fog of World data folder. Note that this
                        folder must contains the 'Sync' folder.
  --output-file OUTPUT_FILE, -o OUTPUT_FILE
                        The path of exported GPX file.

Example: python main.py -i "/path/to/Fog of World" -o "/path/to/output.gpx"
```
