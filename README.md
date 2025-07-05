# ColorSplit Enhanced

Split 3MF files by paint color/material into separate components.

## Features

- Extract paint color information from 3MF files
- Split multi-color models into individual components
- Export as STL, OBJ, or PLY files
- Command line and programmatic API

## Installation

```bash
uv pip install .
```

## Quick Start

```bash
# Split a 3MF file by color
python color_split_enhanced.py Hinged-Locked-Chest_MultiColor.3mf

# Show color info only
python color_split_enhanced.py input.3mf --info

# Custom output
python color_split_enhanced.py input.3mf -o my_output -f obj
```

## Programmatic Usage

```python
from color_split_enhanced import EnhancedColorSplitter

splitter = EnhancedColorSplitter("input.3mf")
splitter.load_3mf()
splitter.export_split_meshes("output", "stl")
```

## Arguments

- `input_file`: 3MF file to process
- `-o, --output`: Output directory (default: output)
- `-f, --format`: Format: stl, obj, ply (default: stl)
- `--info`: Show info only, don't export

## Output

Files named: `{original_name}_{color_key}.{format}`

Example: `Hinged-Locked-Chest_MultiColor_paint_color_1.stl`

## Dependencies

- trimesh, numpy, matplotlib, open3d
