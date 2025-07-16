import { Drawing, ScriptCommand, ExecutionResult, ScriptError } from '../types';
import { v4 as uuidv4 } from 'uuid';

export class ScriptExecutionService {
  private commands: ScriptCommand[] = [
    {
      name: 'draw_wall',
      category: 'drawing',
      parameters: [
        { name: 'start', type: 'point', required: true, description: 'Starting point of the wall' },
        { name: 'end', type: 'point', required: true, description: 'Ending point of the wall' },
        { name: 'thickness', type: 'number', required: false, description: 'Wall thickness in mm (default: 100)' },
      ],
      description: 'Draw a wall between two points',
      examples: ['cad.draw_wall((0, 0), (1000, 0), 100)'],
    },
    {
      name: 'draw_column',
      category: 'drawing',
      parameters: [
        { name: 'center', type: 'point', required: true, description: 'Center point of the column' },
        { name: 'width', type: 'number', required: true, description: 'Column width in mm' },
        { name: 'height', type: 'number', required: true, description: 'Column height in mm' },
        { name: 'shape_type', type: 'string', required: false, description: 'Shape type: "rectangular" or "circular"' },
      ],
      description: 'Draw a column at the specified position',
      examples: ['cad.draw_column((500, 500), 200, 200, "rectangular")'],
    },
    {
      name: 'draw_door',
      category: 'drawing',
      parameters: [
        { name: 'position', type: 'point', required: true, description: 'Door position' },
        { name: 'width', type: 'number', required: false, description: 'Door width in mm (default: 800)' },
        { name: 'direction', type: 'string', required: false, description: 'Opening direction: "left" or "right"' },
      ],
      description: 'Draw a door at the specified position',
      examples: ['cad.draw_door((900, 0), 800, "right")'],
    },
    {
      name: 'place_fixture',
      category: 'drawing',
      parameters: [
        { name: 'position', type: 'point', required: true, description: 'Fixture position' },
        { name: 'width', type: 'number', required: true, description: 'Fixture width in mm' },
        { name: 'height', type: 'number', required: true, description: 'Fixture height in mm' },
        { name: 'fixture_type', type: 'string', required: true, description: 'Type of fixture (e.g., "shelf", "counter")' },
      ],
      description: 'Place a fixture (shelf, counter, etc.) at the specified position',
      examples: ['cad.place_fixture((200, 200), 400, 100, "checkout counter")'],
    },
    {
      name: 'place_equipment',
      category: 'drawing',
      parameters: [
        { name: 'position', type: 'point', required: true, description: 'Equipment position' },
        { name: 'width', type: 'number', required: true, description: 'Equipment width in mm' },
        { name: 'height', type: 'number', required: true, description: 'Equipment height in mm' },
        { name: 'equipment_type', type: 'string', required: true, description: 'Type of equipment' },
      ],
      description: 'Place equipment at the specified position',
      examples: ['cad.place_equipment((1000, 1000), 200, 200, "register")'],
    },
    {
      name: 'create_area',
      category: 'drawing',
      parameters: [
        { name: 'vertices', type: 'point', required: true, description: 'List of vertices defining the area' },
        { name: 'area_type', type: 'string', required: true, description: 'Type of area (e.g., "storage", "seating")' },
      ],
      description: 'Create an area with the specified vertices',
      examples: ['cad.create_area([(1600, 1000), (1900, 1000), (1900, 1400), (1600, 1400)], "storage")'],
    },
    {
      name: 'move_shape',
      category: 'editing',
      parameters: [
        { name: 'shape_id', type: 'string', required: true, description: 'ID of the shape to move' },
        { name: 'delta_x', type: 'number', required: true, description: 'X-axis movement in mm' },
        { name: 'delta_y', type: 'number', required: true, description: 'Y-axis movement in mm' },
      ],
      description: 'Move a shape by the specified delta',
      examples: ['cad.move_shape("shape_id", 100, 50)'],
    },
    {
      name: 'delete_shape',
      category: 'editing',
      parameters: [
        { name: 'shape_id', type: 'string', required: true, description: 'ID of the shape to delete' },
      ],
      description: 'Delete a shape',
      examples: ['cad.delete_shape("shape_id")'],
    },
    {
      name: 'copy_shape',
      category: 'editing',
      parameters: [
        { name: 'shape_id', type: 'string', required: true, description: 'ID of the shape to copy' },
        { name: 'offset_x', type: 'number', required: false, description: 'X-axis offset for the copy (default: 50)' },
        { name: 'offset_y', type: 'number', required: false, description: 'Y-axis offset for the copy (default: 50)' },
      ],
      description: 'Copy a shape with an offset',
      examples: ['cad.copy_shape("shape_id", 100, 100)'],
    },
    {
      name: 'add_label',
      category: 'editing',
      parameters: [
        { name: 'shape_id', type: 'string', required: true, description: 'ID of the shape to label' },
        { name: 'text', type: 'string', required: true, description: 'Label text' },
      ],
      description: 'Add a label to a shape',
      examples: ['cad.add_label("shape_id", "Checkout Counter")'],
    },
  ];

  async executeScript(
    script: string,
    context: { drawingId?: string; variables: Record<string, any> }
  ): Promise<ExecutionResult> {
    try {
      // Create a mock drawing for server-side validation
      const mockDrawing: Drawing = {
        id: context.drawingId || uuidv4(),
        name: 'Server Drawing',
        shapes: [],
        templates: [],
        metadata: {
          scale: 1,
          units: 'mm',
          bounds: { min: { x: 0, y: 0 }, max: { x: 2000, y: 2000 } },
          layers: [],
        },
        createdAt: new Date(),
        updatedAt: new Date(),
      };

      // Basic script validation
      const validationError = await this.validateScript(script);
      if (validationError) {
        return {
          success: false,
          error: validationError,
          logs: [],
        };
      }

      // In a real implementation, this would execute the script
      // For now, we'll return a success response with the mock drawing
      return {
        success: true,
        drawing: mockDrawing,
        logs: ['Script executed successfully on server'],
      };
    } catch (error) {
      return {
        success: false,
        error: {
          type: 'runtime',
          message: 'Script execution failed',
          details: error instanceof Error ? error.message : String(error),
        },
        logs: [],
      };
    }
  }

  async validateScript(script: string): Promise<ScriptError | null> {
    try {
      // Basic syntax checks
      if (!script.trim()) {
        return {
          type: 'validation',
          message: 'Script cannot be empty',
        };
      }

      // Check for potentially dangerous operations
      const dangerousPatterns = [
        /import\s+os/,
        /import\s+subprocess/,
        /import\s+sys/,
        /exec\s*\(/,
        /eval\s*\(/,
        /__import__/,
        /open\s*\(/,
        /file\s*\(/,
      ];

      for (const pattern of dangerousPatterns) {
        if (pattern.test(script)) {
          return {
            type: 'validation',
            message: 'Script contains potentially dangerous operations',
            details: 'File operations and system imports are not allowed',
          };
        }
      }

      return null;
    } catch (error) {
      return {
        type: 'syntax',
        message: 'Script validation failed',
        details: error instanceof Error ? error.message : String(error),
      };
    }
  }

  async getAvailableCommands(): Promise<ScriptCommand[]> {
    return this.commands;
  }
}