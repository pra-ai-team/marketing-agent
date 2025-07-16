import { Drawing, Shape, ExecutionResult, ScriptError, ScriptExecutionContext } from '../types';
import { ShapeUtils } from '../utils/shapeUtils';

declare global {
  interface Window {
    pyodide: any;
    loadPyodide: (config: any) => Promise<any>;
  }
}

export class ScriptEngine {
  private pyodide: any = null;
  private isLoading = false;
  private loadPromise: Promise<void> | null = null;

  /**
   * Initialize Pyodide
   */
  async initialize(): Promise<void> {
    if (this.pyodide) return;
    if (this.isLoading && this.loadPromise) return this.loadPromise;

    this.isLoading = true;
    this.loadPromise = this.loadPyodideInstance();
    
    try {
      await this.loadPromise;
    } finally {
      this.isLoading = false;
    }
  }

  private async loadPyodideInstance(): Promise<void> {
    // Load Pyodide
    this.pyodide = await window.loadPyodide({
      indexURL: "https://cdn.jsdelivr.net/pyodide/v0.24.1/full/",
    });

    // Set up the Python environment
    await this.setupPythonEnvironment();
  }

  private async setupPythonEnvironment(): Promise<void> {
    // Define the CAD API in Python
    const pythonCode = `
import json
from typing import List, Dict, Any, Tuple

class CADEngine:
    def __init__(self):
        self.shapes = []
        self.logs = []
        self.selected_shapes = []
        
    def log(self, message: str):
        """Add a log message"""
        self.logs.append(str(message))
        
    def draw_wall(self, start: Tuple[float, float], end: Tuple[float, float], thickness: float = 100):
        """Draw a wall from start to end point"""
        self.log(f"Drawing wall from {start} to {end} with thickness {thickness}")
        shape_data = {
            "type": "wall",
            "start": {"x": start[0], "y": start[1]},
            "end": {"x": end[0], "y": end[1]},
            "thickness": thickness
        }
        self.shapes.append(("create_wall", shape_data))
        
    def draw_column(self, center: Tuple[float, float], width: float, height: float, shape_type: str = "rectangular"):
        """Draw a column at the specified position"""
        self.log(f"Drawing {shape_type} column at {center} with dimensions {width}x{height}")
        shape_data = {
            "type": "column",
            "center": {"x": center[0], "y": center[1]},
            "dimensions": {"width": width, "height": height},
            "shape_type": shape_type
        }
        self.shapes.append(("create_column", shape_data))
        
    def draw_door(self, position: Tuple[float, float], width: float = 800, direction: str = "left"):
        """Draw a door at the specified position"""
        self.log(f"Drawing door at {position} with width {width}, opening {direction}")
        shape_data = {
            "type": "door",
            "position": {"x": position[0], "y": position[1]},
            "width": width,
            "direction": direction
        }
        self.shapes.append(("create_door", shape_data))
        
    def place_fixture(self, position: Tuple[float, float], width: float, height: float, fixture_type: str):
        """Place a fixture (shelf, counter, etc.) at the specified position"""
        self.log(f"Placing {fixture_type} at {position} with dimensions {width}x{height}")
        shape_data = {
            "type": "fixture",
            "position": {"x": position[0], "y": position[1]},
            "dimensions": {"width": width, "height": height},
            "fixture_type": fixture_type
        }
        self.shapes.append(("create_fixture", shape_data))
        
    def place_equipment(self, position: Tuple[float, float], width: float, height: float, equipment_type: str):
        """Place equipment at the specified position"""
        self.log(f"Placing {equipment_type} at {position} with dimensions {width}x{height}")
        shape_data = {
            "type": "equipment",
            "position": {"x": position[0], "y": position[1]},
            "dimensions": {"width": width, "height": height},
            "equipment_type": equipment_type
        }
        self.shapes.append(("create_equipment", shape_data))
        
    def create_area(self, vertices: List[Tuple[float, float]], area_type: str):
        """Create an area with the specified vertices"""
        self.log(f"Creating {area_type} area with {len(vertices)} vertices")
        shape_data = {
            "type": "area",
            "vertices": [{"x": v[0], "y": v[1]} for v in vertices],
            "area_type": area_type
        }
        self.shapes.append(("create_area", shape_data))
        
    def move_shape(self, shape_id: str, delta_x: float, delta_y: float):
        """Move a shape by the specified delta"""
        self.log(f"Moving shape {shape_id} by ({delta_x}, {delta_y})")
        self.shapes.append(("move_shape", {"shape_id": shape_id, "delta": {"x": delta_x, "y": delta_y}}))
        
    def delete_shape(self, shape_id: str):
        """Delete a shape"""
        self.log(f"Deleting shape {shape_id}")
        self.shapes.append(("delete_shape", {"shape_id": shape_id}))
        
    def copy_shape(self, shape_id: str, offset_x: float = 50, offset_y: float = 50):
        """Copy a shape with an offset"""
        self.log(f"Copying shape {shape_id} with offset ({offset_x}, {offset_y})")
        self.shapes.append(("copy_shape", {"shape_id": shape_id, "offset": {"x": offset_x, "y": offset_y}}))
        
    def add_label(self, shape_id: str, text: str):
        """Add a label to a shape"""
        self.log(f"Adding label '{text}' to shape {shape_id}")
        self.shapes.append(("add_label", {"shape_id": shape_id, "text": text}))
        
    def get_results(self):
        """Get the execution results"""
        return {
            "shapes": self.shapes,
            "logs": self.logs
        }

# Create global CAD engine instance
cad = CADEngine()
`;

    await this.pyodide.runPython(pythonCode);
  }

  /**
   * Execute Python script
   */
  async execute(script: string, context: ScriptExecutionContext): Promise<ExecutionResult> {
    if (!this.pyodide) {
      await this.initialize();
    }

    try {
      // Reset the CAD engine state
      await this.pyodide.runPython(`
cad = CADEngine()
cad.selected_shapes = ${JSON.stringify(context.selectedShapes)}
`);

      // Execute the user script
      await this.pyodide.runPython(script);

      // Get the results
      const results = await this.pyodide.runPython(`
import json
json.dumps(cad.get_results())
`);

      const parsedResults = JSON.parse(results);
      
      // Process the shape commands
      const updatedDrawing = await this.processShapeCommands(
        context.drawing,
        parsedResults.shapes
      );

      return {
        success: true,
        drawing: updatedDrawing,
        logs: parsedResults.logs,
      };
    } catch (error: any) {
      return {
        success: false,
        error: this.parseError(error),
        logs: [],
      };
    }
  }

  /**
   * Process shape commands and update the drawing
   */
  private async processShapeCommands(
    drawing: Drawing,
    commands: Array<[string, any]>
  ): Promise<Drawing> {
    let updatedShapes = [...drawing.shapes];

    for (const [command, data] of commands) {
      switch (command) {
        case 'create_wall':
          const wall = ShapeUtils.createWall(
            data.start,
            data.end,
            data.thickness
          );
          updatedShapes.push(wall);
          break;

        case 'create_column':
          const column = ShapeUtils.createColumn(
            data.center,
            data.dimensions,
            data.shape_type
          );
          updatedShapes.push(column);
          break;

        case 'create_door':
          const door = ShapeUtils.createDoor(
            data.position,
            data.width,
            data.direction
          );
          updatedShapes.push(door);
          break;

        case 'create_fixture':
          const fixture = ShapeUtils.createFixture(
            data.position,
            data.dimensions,
            data.fixture_type
          );
          updatedShapes.push(fixture);
          break;

        case 'create_equipment':
          const equipment = ShapeUtils.createEquipment(
            data.position,
            data.dimensions,
            data.equipment_type
          );
          updatedShapes.push(equipment);
          break;

        case 'create_area':
          const area = ShapeUtils.createArea(
            data.vertices,
            data.area_type
          );
          updatedShapes.push(area);
          break;

        case 'move_shape':
          updatedShapes = updatedShapes.map(shape =>
            shape.id === data.shape_id
              ? ShapeUtils.moveShape(shape, data.delta)
              : shape
          );
          break;

        case 'delete_shape':
          updatedShapes = updatedShapes.filter(
            shape => shape.id !== data.shape_id
          );
          break;

        case 'copy_shape':
          const shapeToCopy = updatedShapes.find(
            shape => shape.id === data.shape_id
          );
          if (shapeToCopy) {
            const copiedShape = ShapeUtils.copyShape(shapeToCopy, data.offset);
            updatedShapes.push(copiedShape);
          }
          break;

        case 'add_label':
          updatedShapes = updatedShapes.map(shape =>
            shape.id === data.shape_id
              ? { ...shape, label: data.text }
              : shape
          );
          break;
      }
    }

    return {
      ...drawing,
      shapes: updatedShapes,
      updatedAt: new Date(),
    };
  }

  /**
   * Parse Python error to ScriptError
   */
  private parseError(error: any): ScriptError {
    const errorString = error.toString();
    let type: ScriptError['type'] = 'runtime';
    let line: number | undefined;
    let column: number | undefined;

    // Try to extract line number from Python traceback
    const lineMatch = errorString.match(/line (\d+)/);
    if (lineMatch) {
      line = parseInt(lineMatch[1], 10);
    }

    // Determine error type
    if (errorString.includes('SyntaxError')) {
      type = 'syntax';
    } else if (errorString.includes('NameError') || errorString.includes('AttributeError')) {
      type = 'validation';
    }

    return {
      type,
      message: error.message || errorString,
      line,
      column,
      details: errorString,
    };
  }

  /**
   * Validate script syntax
   */
  async validateScript(script: string): Promise<ScriptError | null> {
    if (!this.pyodide) {
      await this.initialize();
    }

    try {
      // Try to compile the script
      await this.pyodide.runPython(`
compile('''${script.replace(/'/g, "\\'")}''', '<string>', 'exec')
`);
      return null;
    } catch (error: any) {
      return this.parseError(error);
    }
  }

  /**
   * Get available commands
   */
  getAvailableCommands(): string[] {
    return [
      'cad.draw_wall(start, end, thickness=100)',
      'cad.draw_column(center, width, height, shape_type="rectangular")',
      'cad.draw_door(position, width=800, direction="left")',
      'cad.place_fixture(position, width, height, fixture_type)',
      'cad.place_equipment(position, width, height, equipment_type)',
      'cad.create_area(vertices, area_type)',
      'cad.move_shape(shape_id, delta_x, delta_y)',
      'cad.delete_shape(shape_id)',
      'cad.copy_shape(shape_id, offset_x=50, offset_y=50)',
      'cad.add_label(shape_id, text)',
    ];
  }
}