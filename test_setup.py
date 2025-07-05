#!/usr/bin/env python3
"""
Test script to verify ColorSplit Enhanced setup works with your 3MF file.
"""

import os
import sys
from pathlib import Path

def test_imports():
    """Test if all required packages can be imported."""
    print("Testing imports...")
    
    try:
        import trimesh
        print("✓ trimesh imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import trimesh: {e}")
        return False
    
    try:
        import numpy as np
        print("✓ numpy imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import numpy: {e}")
        return False
    
    try:
        from color_split_enhanced import EnhancedColorSplitter
        print("✓ EnhancedColorSplitter imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import EnhancedColorSplitter: {e}")
        return False
    
    return True

def test_3mf_file():
    """Test if the 3MF file can be loaded."""
    print("\nTesting 3MF file loading...")
    
    input_file = "Hinged-Locked-Chest_MultiColor.3mf"
    
    if not os.path.exists(input_file):
        print(f"✗ Input file not found: {input_file}")
        return False
    
    print(f"✓ Input file found: {input_file}")
    
    try:
        import trimesh
        mesh = trimesh.load(input_file)
        print(f"✓ 3MF file loaded successfully")
        
        # Check if it's a scene or single mesh
        print(f"  - Mesh loaded successfully")
        
        return True
        
    except Exception as e:
        print(f"✗ Failed to load 3MF file: {e}")
        return False

def test_enhanced_color_splitter():
    """Test the EnhancedColorSplitter with the 3MF file."""
    print("\nTesting EnhancedColorSplitter...")
    
    try:
        from color_split_enhanced import EnhancedColorSplitter
        
        input_file = "Hinged-Locked-Chest_MultiColor.3mf"
        splitter = EnhancedColorSplitter(input_file)
        
        # Load the 3MF file
        splitter.load_3mf()
        print("✓ 3MF file loaded by EnhancedColorSplitter")
        
        # Get color information
        color_info = splitter.get_color_info()
        print(f"✓ Found {color_info['total_color_groups']} color groups")
        
        # Show color details
        for color_key, info in color_info['colors'].items():
            print(f"  - {color_key}: {info['mesh_count']} meshes")
        
        # Test splitting
        split_meshes = splitter.split_by_color()
        print(f"✓ Successfully split into {len(split_meshes)} separate meshes")
        
        return True
        
    except Exception as e:
        print(f"✗ EnhancedColorSplitter test failed: {e}")
        return False

def test_debug_colors():
    """Test if the debug_colors.py script is available."""
    print("\nTesting debug_colors.py availability...")
    
    debug_script = "debug_colors.py"
    
    if not os.path.exists(debug_script):
        print(f"✗ Debug script not found: {debug_script}")
        return False
    
    print(f"✓ Debug script found: {debug_script}")
    
    try:
        # Test if we can import the debug functionality
        import subprocess
        result = subprocess.run([sys.executable, debug_script, "--help"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✓ Debug script runs successfully")
            return True
        else:
            print("✗ Debug script failed to run")
            return False
    except Exception as e:
        print(f"✗ Debug script test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("ColorSplit Enhanced Setup Test")
    print("=" * 40)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import test failed. Please install dependencies:")
        print("   pip install -r requirements.txt")
        return False
    
    # Test 3MF file
    if not test_3mf_file():
        print("\n❌ 3MF file test failed.")
        return False
    
    # Test EnhancedColorSplitter
    if not test_enhanced_color_splitter():
        print("\n❌ EnhancedColorSplitter test failed.")
        return False
    
    # Test debug script
    if not test_debug_colors():
        print("\n⚠️  Debug script test failed (optional)")
    
    print("\n✅ All core tests passed! ColorSplit Enhanced is ready to use.")
    print("\nYou can now run:")
    print("  python color_split_enhanced.py Hinged-Locked-Chest_MultiColor.3mf")
    print("  python example_usage.py")
    print("  python debug_colors.py Hinged-Locked-Chest_MultiColor.3mf")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 