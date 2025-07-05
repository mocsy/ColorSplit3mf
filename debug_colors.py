#!/usr/bin/env python3
"""
Debug script to examine color information in 3MF files.
"""

import trimesh
import numpy as np
import argparse
import sys

def debug_3mf_colors(filename):
    """Debug color information in a 3MF file."""
    print(f"Analyzing colors in: {filename}")
    print("=" * 50)
    
    # Load the 3MF file
    scene = trimesh.load(filename)
    # Handle both scene and single mesh cases
    if hasattr(scene, 'geometry'):
        mesh = list(scene.geometry.values())[0]
    else:
        mesh = scene
    
    print(f"Mesh vertices: {len(mesh.vertices)}")  # type: ignore
    print(f"Mesh faces: {len(mesh.faces)}")  # type: ignore
    print(f"Visual type: {type(mesh.visual)}")  # type: ignore
    
    # Check vertex colors
    if hasattr(mesh.visual, 'vertex_colors') and mesh.visual.vertex_colors is not None:  # type: ignore
        vertex_colors = mesh.visual.vertex_colors  # type: ignore
        print(f"\nVertex Colors:")
        print(f"  Shape: {vertex_colors.shape}")  # type: ignore
        print(f"  Unique colors: {len(np.unique(vertex_colors, axis=0))}")  # type: ignore
        unique_vertex_colors = np.unique(vertex_colors, axis=0)  # type: ignore
        for i, color in enumerate(unique_vertex_colors):  # type: ignore
            print(f"  Color {i+1}: RGB({color[0]}, {color[1]}, {color[2]}) Alpha({color[3]})")
    else:
        print("\nNo vertex colors found")
    
    # Check face colors
    if hasattr(mesh.visual, 'face_colors') and mesh.visual.face_colors is not None:  # type: ignore
        face_colors = mesh.visual.face_colors  # type: ignore
        print(f"\nFace Colors:")
        print(f"  Shape: {face_colors.shape}")  # type: ignore
        print(f"  Unique colors: {len(np.unique(face_colors, axis=0))}")  # type: ignore
        unique_face_colors = np.unique(face_colors, axis=0)  # type: ignore
        for i, color in enumerate(unique_face_colors):  # type: ignore
            print(f"  Color {i+1}: RGB({color[0]}, {color[1]}, {color[2]}) Alpha({color[3]})")
    else:
        print("\nNo face colors found")
    
    # Check for texture coordinates
    if hasattr(mesh, 'visual') and hasattr(mesh.visual, 'uv'):  # type: ignore
        print(f"\nTexture Coordinates (UV):")
        print(f"  Shape: {mesh.visual.uv.shape}")  # type: ignore
        print(f"  Sample values: {mesh.visual.uv[:5]}")  # type: ignore
    else:
        print("\nNo texture coordinates found")
    
    # Check for materials
    if hasattr(mesh, 'visual') and hasattr(mesh.visual, 'material'):  # type: ignore
        print(f"\nMaterial:")
        print(f"  Type: {type(mesh.visual.material)}")  # type: ignore
        print(f"  Attributes: {dir(mesh.visual.material)}")  # type: ignore
        if hasattr(mesh.visual.material, 'diffuse'):  # type: ignore
            print(f"  Diffuse: {mesh.visual.material.diffuse}")  # type: ignore
        if hasattr(mesh.visual.material, 'baseColorTexture'):  # type: ignore
            print(f"  Base Color Texture: {mesh.visual.material.baseColorTexture}")  # type: ignore
    else:
        print("\nNo material found")
    
    # Check scene metadata
    print(f"\nScene metadata:")
    if hasattr(scene, 'metadata'):
        for key, value in scene.metadata.items():
            print(f"  {key}: {value}")
    
    # Check if there are any other color-related attributes
    print(f"\nAll visual attributes:")
    for attr in dir(mesh.visual):  # type: ignore
        if not attr.startswith('_'):
            try:
                value = getattr(mesh.visual, attr)  # type: ignore
                if value is not None:
                    print(f"  {attr}: {type(value)} - {value if not hasattr(value, 'shape') else value.shape}")
            except:
                pass
    
    # Check for any differences between vertex and face colors
    if (hasattr(mesh.visual, 'vertex_colors') and mesh.visual.vertex_colors is not None and  # type: ignore
        hasattr(mesh.visual, 'face_colors') and mesh.visual.face_colors is not None):  # type: ignore
        print(f"\nComparing vertex vs face colors:")
        vertex_colors = mesh.visual.vertex_colors  # type: ignore
        face_colors = mesh.visual.face_colors  # type: ignore
        
        # Check if they're identical
        if np.array_equal(vertex_colors, face_colors):  # type: ignore
            print("  Vertex and face colors are identical")
        else:
            print("  Vertex and face colors are different")
            print(f"  Vertex colors unique: {len(np.unique(vertex_colors, axis=0))}")  # type: ignore
            print(f"  Face colors unique: {len(np.unique(face_colors, axis=0))}")  # type: ignore

def main():
    """Main function with command line argument parsing."""
    parser = argparse.ArgumentParser(description='Debug color information in 3MF files')
    parser.add_argument('input_file', nargs='?', default='Hinged-Locked-Chest_MultiColor.3mf',
                       help='Input 3MF file path (default: Hinged-Locked-Chest_MultiColor.3mf)')
    
    args = parser.parse_args()
    
    try:
        debug_3mf_colors(args.input_file)
    except FileNotFoundError:
        print(f"Error: File '{args.input_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error analyzing file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 