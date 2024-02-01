# Scan Settings Documentation

This document outlines the various scan strategies and their corresponding settings.
The strategy is a str while the corresponding settings should be in the form of a dictionary

## Infill strategies
The following scan strategies are supported:
- `line_snake`: Simple line scanning left-right-left-.., with constant speed.
- `line_left_right`: Simple line scanning left-right,left-right,.., with constant speed.
- `line_right_left`: Simple line scanning right-left,right-left,.., with constant speed.
- `line_spiral` : Moving in a spiral a point_distance distance between each line, with constant speed.
- `line_concentric` : Moving in full circles along the contour with a point_distance distance between each line, with constant speed.
- `point_random`: Spot melting with random order of spots.
- `point_ordered`: Spot melting jumping along the lines with some predefined distance.

### line_snake
no additional settings

### line_left_right
no additional settings

### line_right_left
no additional settings

### line_spiral
| Setting Key | Data Type | Description                                         | Example Value   |
|-------------|-----------|-----------------------------------------------------|-----------------|
| direction   | str       | Starting from center out or from outer in (standard)| inward/ outward |

### line_concentric
| Setting Key | Data Type | Description                                         | Example Value   |
|-------------|-----------|-----------------------------------------------------|-----------------|
| direction   | str       | Starting from center out or from outer in (standard)| inward/ outward |

### point_random
no additional settings

### point_ordered
| Setting Key | Data Type | Description                                           | Example Value |
|-------------|-----------|-------------------------------------------------------|---------------|
| x_jump      | int       | Number of points that should be jumped in x direction | 2             |
| y_jump      | int       | Number of points that should be jumped in x direction | 5             |


## Contour strategies
The following scan strategies are supported:
- `line_simple`: Simple line scanning, with constant speed.
- `point_simple`: Simple spot scanning.

### line_simple
no additional settings

### point_simple
| Setting Key | Data Type | Description                                           | Example Value |
|-------------|-----------|-------------------------------------------------------|---------------|
| step        | float     | mm distance between points                            | 0.1           |
| jump        | int       | Jumps done between each circulation (standard = 1)    | 5             |


Please ensure you use the correct settings for the selected scan strategy. Providing incorrect or invalid settings may result in unexpected behavior or errors.
