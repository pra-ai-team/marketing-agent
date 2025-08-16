import { v4 as uuidv4 } from 'uuid';
import { Shape, ShapeType, Point, Dimensions, RenderStyle, Geometry } from '../types';

export class ShapeUtils {
  /**
   * Create a wall shape
   */
  static createWall(
    start: Point,
    end: Point,
    thickness: number = 100,
    style?: Partial<RenderStyle>
  ): Shape {
    return {
      id: uuidv4(),
      type: 'wall',
      geometry: {
        type: 'polygon',
        coordinates: this.calculateWallPolygon(start, end, thickness),
      },
      properties: {
        name: 'Wall',
        category: 'structure',
        metadata: { thickness },
      },
      style: {
        strokeColor: '#333333',
        fillColor: '#cccccc',
        strokeWidth: 2,
        lineStyle: 'solid',
        opacity: 1,
        ...style,
      },
    };
  }

  /**
   * Create a column shape
   */
  static createColumn(
    center: Point,
    dimensions: Dimensions,
    type: 'rectangular' | 'circular' = 'rectangular',
    style?: Partial<RenderStyle>
  ): Shape {
    if (type === 'circular') {
      return {
        id: uuidv4(),
        type: 'column',
        geometry: {
          type: 'circle',
          coordinates: [center],
          radius: dimensions.width / 2,
        },
        properties: {
          name: 'Column',
          category: 'structure',
          metadata: { type: 'circular' },
        },
        style: {
          strokeColor: '#333333',
          fillColor: '#999999',
          strokeWidth: 2,
          lineStyle: 'solid',
          opacity: 1,
          ...style,
        },
      };
    }

    return {
      id: uuidv4(),
      type: 'column',
      geometry: {
        type: 'rectangle',
        coordinates: [
          {
            x: center.x - dimensions.width / 2,
            y: center.y - dimensions.height / 2,
          },
        ],
        dimensions,
      },
      properties: {
        name: 'Column',
        category: 'structure',
        metadata: { type: 'rectangular' },
      },
      style: {
        strokeColor: '#333333',
        fillColor: '#999999',
        strokeWidth: 2,
        lineStyle: 'solid',
        opacity: 1,
        ...style,
      },
    };
  }

  /**
   * Create a door shape
   */
  static createDoor(
    position: Point,
    width: number = 800,
    openingDirection: 'left' | 'right' = 'left',
    style?: Partial<RenderStyle>
  ): Shape {
    const arcRadius = width;
    const arcPoints: Point[] = [];
    const segments = 20;

    // Create arc for door swing
    for (let i = 0; i <= segments; i++) {
      const angle = (i / segments) * (Math.PI / 2);
      const x = openingDirection === 'left' 
        ? position.x + arcRadius * Math.cos(angle)
        : position.x - arcRadius * Math.cos(angle);
      const y = position.y - arcRadius * Math.sin(angle);
      arcPoints.push({ x, y });
    }

    return {
      id: uuidv4(),
      type: 'door',
      geometry: {
        type: 'line',
        coordinates: arcPoints,
      },
      properties: {
        name: 'Door',
        category: 'structure',
        metadata: { width, openingDirection },
      },
      style: {
        strokeColor: '#666666',
        strokeWidth: 2,
        lineStyle: 'solid',
        opacity: 1,
        ...style,
      },
    };
  }

  /**
   * Create a fixture shape (shelf, counter, etc.)
   */
  static createFixture(
    position: Point,
    dimensions: Dimensions,
    fixtureType: string,
    style?: Partial<RenderStyle>
  ): Shape {
    return {
      id: uuidv4(),
      type: 'fixture',
      geometry: {
        type: 'rectangle',
        coordinates: [position],
        dimensions,
      },
      properties: {
        name: fixtureType,
        category: 'fixture',
        metadata: { fixtureType },
      },
      style: {
        strokeColor: '#0066cc',
        fillColor: '#e6f2ff',
        strokeWidth: 2,
        lineStyle: 'solid',
        opacity: 0.8,
        ...style,
      },
    };
  }

  /**
   * Create an equipment shape
   */
  static createEquipment(
    position: Point,
    dimensions: Dimensions,
    equipmentType: string,
    style?: Partial<RenderStyle>
  ): Shape {
    return {
      id: uuidv4(),
      type: 'equipment',
      geometry: {
        type: 'rectangle',
        coordinates: [position],
        dimensions,
      },
      properties: {
        name: equipmentType,
        category: 'equipment',
        metadata: { equipmentType },
      },
      style: {
        strokeColor: '#cc6600',
        fillColor: '#fff2e6',
        strokeWidth: 2,
        lineStyle: 'solid',
        opacity: 0.8,
        ...style,
      },
    };
  }

  /**
   * Create an area shape
   */
  static createArea(
    vertices: Point[],
    areaType: string,
    style?: Partial<RenderStyle>
  ): Shape {
    return {
      id: uuidv4(),
      type: 'area',
      geometry: {
        type: 'polygon',
        coordinates: vertices,
      },
      properties: {
        name: areaType,
        category: 'area',
        metadata: { areaType },
      },
      style: {
        strokeColor: '#009900',
        fillColor: '#e6ffe6',
        strokeWidth: 2,
        lineStyle: 'dashed',
        opacity: 0.3,
        ...style,
      },
    };
  }

  /**
   * Move a shape to a new position
   */
  static moveShape(shape: Shape, delta: Point): Shape {
    const newCoordinates = shape.geometry.coordinates.map(coord => ({
      x: coord.x + delta.x,
      y: coord.y + delta.y,
    }));

    return {
      ...shape,
      geometry: {
        ...shape.geometry,
        coordinates: newCoordinates,
      },
    };
  }

  /**
   * Rotate a shape around a center point
   */
  static rotateShape(shape: Shape, angle: number, center?: Point): Shape {
    const shapeCenter = center || this.getShapeCenter(shape);
    const rad = (angle * Math.PI) / 180;
    const cos = Math.cos(rad);
    const sin = Math.sin(rad);

    const newCoordinates = shape.geometry.coordinates.map(coord => {
      const dx = coord.x - shapeCenter.x;
      const dy = coord.y - shapeCenter.y;
      return {
        x: shapeCenter.x + dx * cos - dy * sin,
        y: shapeCenter.y + dx * sin + dy * cos,
      };
    });

    return {
      ...shape,
      geometry: {
        ...shape.geometry,
        coordinates: newCoordinates,
      },
    };
  }

  /**
   * Create a copy of a shape
   */
  static copyShape(shape: Shape, offset: Point = { x: 50, y: 50 }): Shape {
    const newShape = this.moveShape(shape, offset);
    return {
      ...newShape,
      id: uuidv4(),
    };
  }

  /**
   * Calculate wall polygon from start and end points
   */
  private static calculateWallPolygon(start: Point, end: Point, thickness: number): Point[] {
    const dx = end.x - start.x;
    const dy = end.y - start.y;
    const length = Math.sqrt(dx * dx + dy * dy);
    
    if (length === 0) return [start, start, start, start];

    // Perpendicular vector
    const perpX = (-dy / length) * (thickness / 2);
    const perpY = (dx / length) * (thickness / 2);

    return [
      { x: start.x + perpX, y: start.y + perpY },
      { x: end.x + perpX, y: end.y + perpY },
      { x: end.x - perpX, y: end.y - perpY },
      { x: start.x - perpX, y: start.y - perpY },
    ];
  }

  /**
   * Get the center point of a shape
   */
  private static getShapeCenter(shape: Shape): Point {
    const coords = shape.geometry.coordinates;
    
    if (coords.length === 0) return { x: 0, y: 0 };

    if (shape.geometry.type === 'rectangle' && shape.geometry.dimensions) {
      return {
        x: coords[0].x + shape.geometry.dimensions.width / 2,
        y: coords[0].y + shape.geometry.dimensions.height / 2,
      };
    }

    if (shape.geometry.type === 'circle') {
      return coords[0];
    }

    // Calculate centroid for polygon or line
    const sum = coords.reduce(
      (acc, coord) => ({ x: acc.x + coord.x, y: acc.y + coord.y }),
      { x: 0, y: 0 }
    );

    return {
      x: sum.x / coords.length,
      y: sum.y / coords.length,
    };
  }
}