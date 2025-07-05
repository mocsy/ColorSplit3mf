# Project Setup Instructions

## Prerequisites

```bash
# Install Python 3.8+ if not already installed
python --version
```

## Install Dependencies

```bash
# Install uv package manager
pip install uv

# Install project dependencies
uv pip install .
```

## Verify Installation

```bash
# Test the main script
python color_split_enhanced.py --help

# Test with example file
python color_split_enhanced.py Hinged-Locked-Chest_MultiColor.3mf --info
```

## Run Type Checking

```bash
# Install pyrefly if not already installed
pip install pyrefly

# Check type errors
pyrefly check color_split_enhanced.py
```

## Test Example Usage

```bash
# Run the example script
python example_usage.py
```

## Project Structure

- `color_split_enhanced.py` - Main tool
- `example_usage.py` - Usage examples
- `Hinged-Locked-Chest_MultiColor.3mf` - Test file
- `pyproject.toml` - Project configuration

## Testing Setup with test_setup.py

The `test_setup.py` script verifies that your environment is properly configured and ready to use.

### When to Run test_setup.py

#### 1. **Initial Setup**
After first cloning or downloading the project:
```bash
python test_setup.py
```

#### 2. **After Installing Dependencies**
When you install or update the required packages:
```bash
pip install -r requirements.txt
python test_setup.py
```

#### 3. **Troubleshooting Issues**
When the main scripts aren't working as expected:
```bash
python test_setup.py
```

#### 4. **Before Running Main Scripts**
As a quick sanity check before processing important files:
```bash
python test_setup.py
python color_split_enhanced.py your_file.3mf
```

#### 5. **After Environment Changes**
When you:
- Switch Python environments
- Update Python version
- Install new packages
- Move the project to a different machine

### What the Test Checks

The script verifies:
- ✅ **Dependencies**: `trimesh`, `numpy`, `EnhancedColorSplitter`
- ✅ **3MF File**: Can load the test file `Hinged-Locked-Chest_MultiColor.3mf`
- ✅ **Color Splitting**: Can process and split the mesh by color
- ✅ **Debug Tools**: Optional check for `debug_colors.py` availability

### When NOT to Run

- **During normal operation**: Once you've confirmed everything works, you don't need to run it repeatedly
- **For every file**: The test uses a specific 3MF file, so it won't test your custom files
- **In production**: This is a development/testing tool, not needed for regular use

The test is most valuable during initial setup and troubleshooting, ensuring your environment is properly configured before processing your 3MF files. 