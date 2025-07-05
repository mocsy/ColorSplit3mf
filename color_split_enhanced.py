#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced ColorSplit - 3MF Mesh Color-Based Splitting Tool with Paint Color Support

This script loads a 3MF file and splits the mesh by paint color information,
exporting each colored component as a separate file.
"""

import os
import sys
import argparse
import numpy as np
import trimesh
import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
import logging
from collections import defaultdict
from typing import Dict, List, Any, Optional, Union

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EnhancedColorSplitter:
    """Enhanced class to handle splitting 3MF meshes by paint color."""
    
    def __init__(self, input_file: str) -> None:
        """Initialize the EnhancedColorSplitter with an input 3MF file."""
        self.input_file = Path(input_file)
        self.mesh: Optional[Any] = None  # trimesh.Trimesh or trimesh.Scene
        self.paint_colors: Dict[str, Dict[str, Any]] = {}
        self.color_groups: Dict[str, List[Dict[str, Any]]] = {}
        self.face_paint_colors: Optional[Dict[int, int]] = None
        self.face_lookup: Dict[tuple, int] = {}
        
    def load_3mf(self) -> None:
        """Load the 3MF file and extract mesh and paint color information."""
        try:
            logger.info(f"Loading 3MF file: {self.input_file}")
            
            # Load the 3MF file with trimesh
            self.mesh = trimesh.load(str(self.input_file))
            
            # Extract paint color information from the 3MF file
            self._extract_paint_colors()
            
            # Check if we have a scene (multiple objects) or single mesh
            if hasattr(self.mesh, 'geometry'):
                # Scene with multiple objects
                logger.info("Detected multi-object scene")
                self._process_scene_with_paint()
            else:
                # Single mesh
                logger.info("Detected single mesh")
                self._process_single_mesh_with_paint()
                
            logger.info(f"Successfully loaded mesh with {len(self.color_groups)} color groups")
            
        except Exception as e:
            logger.error(f"Error loading 3MF file: {e}")
            raise
    
    def _extract_paint_colors(self) -> None:
        """Extract paint color information from the 3MF file."""
        logger.info("Extracting paint color information...")
        
        # Extract the 3MF file to a temporary directory
        with zipfile.ZipFile(self.input_file, 'r') as zip_ref:
            # Find the object file
            object_files = [f for f in zip_ref.namelist() if f.endswith('.model') and 'Objects' in f]
            
            if not object_files:
                logger.warning("No object files found in 3MF")
                return
            
            # Read the first object file
            object_file = object_files[0]
            with zip_ref.open(object_file) as f:
                content = f.read().decode('utf-8')
            
            # Parse paint colors
            self._parse_paint_colors(content)
    
    def _parse_paint_colors(self, content: str) -> None:
        """Parse paint colors from the XML content."""
        # Find all triangles with paint colors
        paint_color_pattern = r'<triangle v1="(\d+)" v2="(\d+)" v3="(\d+)" paint_color="(\d+)"'
        paint_triangles = re.findall(paint_color_pattern, content)
        
        # Find all triangles without paint colors
        no_paint_pattern = r'<triangle v1="(\d+)" v2="(\d+)" v3="(\d+)"(?!.*paint_color)'
        no_paint_triangles = re.findall(no_paint_pattern, content)
        
        logger.info(f"Found {len(paint_triangles)} triangles with paint colors")
        logger.info(f"Found {len(no_paint_triangles)} triangles without paint colors")
        
        # Create a mapping from triangle index to paint color
        self.face_paint_colors = {}
        
        # Create a fast lookup table for faces
        self._create_face_lookup()
        
        # Process triangles with paint colors
        for v1, v2, v3, paint_color in paint_triangles:
            # Find the face index in the mesh
            face_idx = self._find_face_index_fast(int(v1), int(v2), int(v3))
            if face_idx is not None and self.face_paint_colors is not None:
                self.face_paint_colors[face_idx] = int(paint_color)
        
        # Process triangles without paint colors (assign default color 0)
        for v1, v2, v3 in no_paint_triangles:
            face_idx = self._find_face_index_fast(int(v1), int(v2), int(v3))
            if face_idx is not None and self.face_paint_colors is not None:
                self.face_paint_colors[face_idx] = 0  # Default color
        
        # Count paint colors - use int keys for paint color IDs
        color_counts: Dict[int, int] = defaultdict(int)
        if self.face_paint_colors is not None:
            for paint_color in self.face_paint_colors.values():
                color_counts[paint_color] += 1
        
        logger.info("Paint color distribution:")
        for color_id, count in sorted(color_counts.items()):
            logger.info(f"  Paint color {color_id}: {count} faces")
    
    def _create_face_lookup(self) -> None:
        """Create a fast lookup table for faces."""
        if self.mesh is None:
            logger.error("Mesh is None, cannot create face lookup")
            return
            
        if hasattr(self.mesh, 'geometry'):
            # For scenes, use the first mesh
            mesh = list(self.mesh.geometry.values())[0]
        else:
            mesh = self.mesh
        
        # Create a lookup table: (sorted_vertices) -> face_index
        self.face_lookup = {}
        for i, face in enumerate(mesh.faces):
            # Create a sorted tuple of vertex indices for consistent lookup
            sorted_vertices = tuple(sorted(face))
            self.face_lookup[sorted_vertices] = i
    
    def _find_face_index_fast(self, v1: int, v2: int, v3: int) -> Optional[int]:
        """Find the face index using the fast lookup table."""
        # Create a sorted tuple of vertex indices
        sorted_vertices = tuple(sorted([v1, v2, v3]))
        return self.face_lookup.get(sorted_vertices)
    
    def _find_face_index(self, v1: int, v2: int, v3: int) -> Optional[int]:
        """Find the face index in the mesh that matches the given vertices (slow method, kept for compatibility)."""
        if self.mesh is None:
            return None
            
        if hasattr(self.mesh, 'geometry'):
            # For scenes, use the first mesh
            mesh = list(self.mesh.geometry.values())[0]
        else:
            mesh = self.mesh
        
        # Look for the face with these vertices (in any order)
        for i, face in enumerate(mesh.faces):
            if set(face) == {v1, v2, v3}:
                return i
        
        return None
    
    def _process_scene_with_paint(self) -> None:
        """Process a scene with multiple objects using paint colors."""
        if self.mesh is None:
            logger.error("Mesh is None, cannot process scene")
            return
            
        for name, mesh in self.mesh.geometry.items():
            logger.info(f"Processing object: {name}")
            self._extract_materials_from_mesh_with_paint(mesh, name)
    
    def _process_single_mesh_with_paint(self) -> None:
        """Process a single mesh object using paint colors."""
        if self.mesh is None:
            logger.error("Mesh is None, cannot process single mesh")
            return
            
        self._extract_materials_from_mesh_with_paint(self.mesh, "main")
    
    def _extract_materials_from_mesh_with_paint(self, mesh: trimesh.Trimesh, object_name: str) -> None:
        """Extract material and paint color information from a mesh."""
        if self.face_paint_colors is not None:
            # Use paint colors for splitting
            self._handle_paint_coloring(mesh, object_name)
        elif hasattr(mesh, 'visual') and hasattr(mesh.visual, 'material'):
            # Fallback to material-based coloring
            self._handle_material_coloring(mesh, object_name)
        elif hasattr(mesh, 'visual') and hasattr(mesh.visual, 'vertex_colors'):
            # Fallback to vertex-based coloring
            self._handle_vertex_coloring(mesh, object_name)
        else:
            # No color information found
            logger.warning(f"No color information found in {object_name}")
            self._add_to_color_group(mesh, "default", object_name)
    
    def _handle_paint_coloring(self, mesh: trimesh.Trimesh, object_name: str) -> None:
        """Handle paint-based coloring."""
        if self.face_paint_colors is None:
            logger.warning("No paint color information available")
            return
        
        # Group faces by paint color - use int keys for paint color IDs
        paint_color_groups: Dict[int, List[int]] = defaultdict(list)
        
        for face_idx, paint_color in self.face_paint_colors.items():
            if face_idx < len(mesh.faces):
                paint_color_groups[paint_color].append(face_idx)
        
        # Create submeshes for each paint color
        for paint_color, face_indices in paint_color_groups.items():
            if face_indices:
                color_key = f"paint_color_{paint_color}"
                
                # Create a submesh for this paint color
                submeshes = mesh.submesh([face_indices])
                # submesh can return either a single Trimesh or a list of Trimesh
                if isinstance(submeshes, list) and len(submeshes) > 0:
                    self._add_to_color_group(submeshes[0], color_key, f"{object_name}_{color_key}")
                    self.paint_colors[color_key] = {'paint_color_id': paint_color}
                elif not isinstance(submeshes, list) and submeshes is not None:
                    # Single Trimesh object
                    self._add_to_color_group(submeshes, color_key, f"{object_name}_{color_key}")
                    self.paint_colors[color_key] = {'paint_color_id': paint_color}
    
    def _handle_material_coloring(self, mesh: trimesh.Trimesh, object_name: str) -> None:
        """Handle material-based coloring (fallback)."""
        if not hasattr(mesh, 'visual') or mesh.visual is None:
            logger.warning(f"No visual information found in {object_name}")
            self._add_to_color_group(mesh, "default", object_name)
            return
            
        material = mesh.visual.material
        
        if hasattr(material, 'diffuse'):
            color = material.diffuse
            color_key = self._color_to_key(color)
            self._add_to_color_group(mesh, color_key, object_name)
        else:
            logger.warning(f"No diffuse color found in material for {object_name}")
            self._add_to_color_group(mesh, "default", object_name)
    
    def _handle_vertex_coloring(self, mesh: trimesh.Trimesh, object_name: str) -> None:
        """Handle vertex-based coloring (fallback)."""
        if not hasattr(mesh, 'visual') or mesh.visual is None:
            logger.warning(f"No visual information found in {object_name}")
            self._add_to_color_group(mesh, "default", object_name)
            return
            
        vertex_colors = mesh.visual.vertex_colors
        
        if vertex_colors is not None and len(vertex_colors) > 0:
            # Convert vertex colors to face colors
            face_colors = []
            for face in mesh.faces:
                face_vertex_colors = vertex_colors[face]
                face_color = np.mean(face_vertex_colors, axis=0)
                face_colors.append(face_color)
            
            face_colors_array = np.array(face_colors, dtype=np.float64)
            # Use proper typing for numpy operations
            unique_colors = np.unique(face_colors_array, axis=0)  # type: ignore
            
            for color in unique_colors:
                color_key = self._color_to_key(color)
                color_mask = np.all(np.isclose(face_colors_array, color, atol=1e-6), axis=1)  # type: ignore
                if np.any(color_mask):
                    submeshes = mesh.submesh([color_mask])
                    # Handle both single Trimesh and list of Trimesh
                    if isinstance(submeshes, list) and len(submeshes) > 0:
                        self._add_to_color_group(submeshes[0], color_key, f"{object_name}_{color_key}")
                    elif not isinstance(submeshes, list) and submeshes is not None:
                        self._add_to_color_group(submeshes, color_key, f"{object_name}_{color_key}")
        else:
            logger.warning(f"No valid vertex colors found in {object_name}")
            self._add_to_color_group(mesh, "default", object_name)
    
    def _color_to_key(self, color: Union[List[float], np.ndarray]) -> str:
        """Convert color array to a string key."""
        if isinstance(color, (list, np.ndarray)):
            rgb = [int(c * 255) if c <= 1 else int(c) for c in color[:3]]
            return f"color_{rgb[0]}_{rgb[1]}_{rgb[2]}"
        else:
            return "unknown_color"
    
    def _add_to_color_group(self, mesh: trimesh.Trimesh, color_key: str, object_name: str) -> None:
        """Add a mesh to a color group."""
        if color_key not in self.color_groups:
            self.color_groups[color_key] = []
        
        self.color_groups[color_key].append({
            'mesh': mesh,
            'name': object_name
        })
    
    def split_by_color(self) -> Dict[str, trimesh.Trimesh]:
        """Split the mesh by color and return separate meshes."""
        if not self.color_groups:
            logger.error("No color groups found. Load the 3MF file first.")
            return {}
        
        split_meshes = {}
        
        for color_key, meshes in self.color_groups.items():
            logger.info(f"Processing color group: {color_key} with {len(meshes)} meshes")
            
            if len(meshes) == 1:
                split_meshes[color_key] = meshes[0]['mesh']
            else:
                combined_mesh = trimesh.util.concatenate([m['mesh'] for m in meshes])
                split_meshes[color_key] = combined_mesh
        
        return split_meshes
    
    def export_split_meshes(self, output_dir: str = "output", format: str = "stl") -> List[str]:
        """Export split meshes to separate files."""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        split_meshes = self.split_by_color()
        
        exported_files = []
        
        for color_key, mesh in split_meshes.items():
            base_name = self.input_file.stem
            filename = f"{base_name}_{color_key}.{format}"
            filepath = output_path / filename
            
            try:
                mesh.export(str(filepath))
                logger.info(f"Exported: {filepath}")
                exported_files.append(str(filepath))
                
            except Exception as e:
                logger.error(f"Error exporting {color_key}: {e}")
        
        return exported_files
    
    def get_color_info(self) -> Dict[str, Any]:
        """Get information about the colors found in the mesh."""
        info: Dict[str, Any] = {
            'total_color_groups': len(self.color_groups),
            'colors': {}
        }
        
        for color_key, meshes in self.color_groups.items():
            info['colors'][color_key] = {
                'mesh_count': len(meshes),
                'paint_info': self.paint_colors.get(color_key, {})
            }
        
        return info

def main():
    """Main function to run the enhanced color splitting tool."""
    parser = argparse.ArgumentParser(description='Split 3MF mesh by paint color')
    parser.add_argument('input_file', help='Input 3MF file path')
    parser.add_argument('-o', '--output', default='output', help='Output directory')
    parser.add_argument('-f', '--format', default='stl', choices=['stl', 'obj', 'ply'], 
                       help='Output format')
    parser.add_argument('--info', action='store_true', help='Show color information only')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input_file):
        logger.error(f"Input file not found: {args.input_file}")
        sys.exit(1)
    
    splitter = EnhancedColorSplitter(args.input_file)
    
    try:
        splitter.load_3mf()
        
        color_info = splitter.get_color_info()
        logger.info(f"Found {color_info['total_color_groups']} color groups:")
        
        for color_key, info in color_info['colors'].items():
            logger.info(f"  {color_key}: {info['mesh_count']} meshes")
            if 'paint_info' in info and info['paint_info']:
                paint_info = info['paint_info']
                if 'paint_color_id' in paint_info:
                    logger.info(f"    Paint color ID: {paint_info['paint_color_id']}")
        
        if args.info:
            return
        
        exported_files = splitter.export_split_meshes(args.output, args.format)
        logger.info(f"Successfully exported {len(exported_files)} files to {args.output}/")
        
    except Exception as e:
        logger.error(f"Error processing file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 