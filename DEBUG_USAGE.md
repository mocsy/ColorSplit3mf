# Debug Colors Script Usage

Analyzes color information in 3MF files to diagnose color-related issues.

## Usage

```bash
# Analyze default test file
python debug_colors.py

# Analyze specific 3MF file
python debug_colors.py your_file.3mf

# Show help
python debug_colors.py --help
```

## What it analyzes

- **Mesh properties**: vertices, faces, visual type
- **Vertex colors**: RGB/Alpha values, unique colors
- **Face colors**: RGB/Alpha values, unique colors
- **Materials**: diffuse colors, textures, attributes
- **Textures**: UV coordinates, texture data
- **Scene metadata**: file information
- **Color comparison**: vertex vs face colors

## When to use

- Main color splitting tool doesn't work as expected
- Need to understand 3MF color structure
- Troubleshooting color-related issues
- Before running `color_split_enhanced.py`

## Error handling

- File not found: Clear error message
- Invalid 3MF: Analysis error details
- Missing colors: No color data found

## Integration

```bash
# Step 1: Analyze file
python debug_colors.py my_model.3mf

# Step 2: Split by color
python color_split_enhanced.py my_model.3mf
``` 