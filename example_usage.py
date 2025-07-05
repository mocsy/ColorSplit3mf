#!/usr/bin/env python3
"""
Example usage of the EnhancedColorSplitter class.

This script demonstrates how to use the EnhancedColorSplitter programmatically
to split 3MF files by paint color/material.
"""

from color_split_enhanced import EnhancedColorSplitter
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def example_basic_usage():
    """Basic example of using EnhancedColorSplitter."""
    
    # Initialize the splitter with your 3MF file
    input_file = "Hinged-Locked-Chest_MultiColor.3mf"
    splitter = EnhancedColorSplitter(input_file)
    
    try:
        # Load the 3MF file
        splitter.load_3mf()
        
        # Get information about the colors
        color_info = splitter.get_color_info()
        print(f"\nFound {color_info['total_color_groups']} color groups:")
        
        for color_key, info in color_info['colors'].items():
            print(f"  {color_key}: {info['mesh_count']} meshes")
            if 'paint_info' in info and info['paint_info']:
                paint_info = info['paint_info']
                if 'paint_color_id' in paint_info:
                    print(f"    Paint color ID: {paint_info['paint_color_id']}")
        
        # Split the mesh by color
        split_meshes = splitter.split_by_color()
        print(f"\nSplit into {len(split_meshes)} separate meshes")
        
        # Export each color group to separate files
        exported_files = splitter.export_split_meshes("output_enhanced", "stl")
        print(f"\nExported files:")
        for file_path in exported_files:
            print(f"  {file_path}")
            
    except Exception as e:
        logger.error(f"Error: {e}")

def example_custom_processing():
    """Example of custom processing with the split meshes."""
    
    input_file = "Hinged-Locked-Chest_MultiColor.3mf"
    splitter = EnhancedColorSplitter(input_file)
    
    try:
        splitter.load_3mf()
        split_meshes = splitter.split_by_color()
        
        # Process each color group individually
        for color_key, mesh in split_meshes.items():
            print(f"\nProcessing {color_key}:")
            print(f"  Vertices: {len(mesh.vertices)}")
            print(f"  Faces: {len(mesh.faces)}")
            print(f"  Volume: {mesh.volume:.2f}")
            print(f"  Surface area: {mesh.area:.2f}")
            
            # You can perform additional operations here
            # For example, check if the mesh is watertight
            if mesh.is_watertight:
                print(f"  Watertight: Yes")
            else:
                print(f"  Watertight: No")
                
    except Exception as e:
        logger.error(f"Error: {e}")

def example_export_different_formats():
    """Example of exporting in different formats."""
    
    input_file = "Hinged-Locked-Chest_MultiColor.3mf"
    splitter = EnhancedColorSplitter(input_file)
    
    try:
        splitter.load_3mf()
        
        # Export as STL
        stl_files = splitter.export_split_meshes("output_stl", "stl")
        print(f"Exported {len(stl_files)} STL files")
        
        # Export as OBJ
        obj_files = splitter.export_split_meshes("output_obj", "obj")
        print(f"Exported {len(obj_files)} OBJ files")
        
        # Export as PLY
        ply_files = splitter.export_split_meshes("output_ply", "ply")
        print(f"Exported {len(ply_files)} PLY files")
        
    except Exception as e:
        logger.error(f"Error: {e}")

if __name__ == "__main__":
    print("Enhanced ColorSplit Example Usage")
    print("=" * 50)
    
    print("\n1. Basic Usage:")
    example_basic_usage()
    
    print("\n" + "=" * 50)
    print("\n2. Custom Processing:")
    example_custom_processing()
    
    print("\n" + "=" * 50)
    print("\n3. Export Different Formats:")
    example_export_different_formats() 