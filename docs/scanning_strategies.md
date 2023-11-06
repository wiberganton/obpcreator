# Scan Settings Documentation

This document outlines the various scan strategies and their corresponding settings.
The strategy is a str while the corresponding settings should be in the form of a dictionary

## Infill strategies
The following scan strategies are supported:
- `line_snake`: Simple line scanning left-right-left-.., with constant speed.
- `line_left_right`: Simple line scanning left-right,left-right,.., with constant speed.
- `line_right_left`: Simple line scanning right-left,right-left,.., with constant speed.
- `point_random`: Spot melting with random order of spots.

### line_snake
no additional settings

### line_left_right
no additional settings

### line_right_left
no additional settings

### point_random
no additional settings

### Strategy B Settings
| Setting Key | Data Type | Description                              | Example Value |
|-------------|-----------|------------------------------------------|---------------|
| frequency   | int       | The frequency at which the scan operates | 5             |
| resolution  | int       | The resolution of the scan                | 300           |


## Contour strategies
The following scan strategies are supported:
- `line_simple`: Simple line scanning, with constant speed.

### line_simple
no additional settings


Please ensure you use the correct settings for the selected scan strategy. Providing incorrect or invalid settings may result in unexpected behavior or errors.
