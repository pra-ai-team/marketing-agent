import { Shape, Point, Geometry, BoundingBox, Drawing } from '../types';

export class RenderingService {
  /**
   * Calculate bounding box for a shape
   */
  static calculateShapeBounds(shape: Shape): BoundingBox {
    const points = shape.geometry.coordinates;
    
    if (points.length === 0) {
      return { min: { x: 0, y: 0 }, max: { x: 0, y: 0 } };
    }

    let minX = points[0].x;
    let minY = points[0].y;
    let maxX = points[0].x;
    let maxY = points[0].y;

    // Handle different geometry types
    switch (shape.geometry.type) {
      case 'rectangle':
        if (shape.geometry.dimensions) {
          maxX = minX + shape.geometry.dimensions.width;
          maxY = minY + shape.geometry.dimensions.height;
        }
        break;

      case 'circle':
        if (shape.geometry.radius) {
          const center = points[0];
          minX = center.x - shape.geometry.radius;
          minY = center.y - shape.geometry.radius;
          maxX = center.x + shape.geometry.radius;
          maxY = center.y + shape.geometry.radius;
        }
        break;

      case 'line':
      case 'polygon':
        points.forEach(point => {
          minX = Math.min(minX, point.x);
          minY = Math.min(minY, point.y);
          maxX = Math.max(maxX, point.x);
          maxY = Math.max(maxY, point.y);
        });
        break;
    }

    return { min: { x: minX, y: minY }, max: { x: maxX, y: maxY } };
  }

  /**
   * Calculate bounding box for entire drawing
   */
  static calculateDrawingBounds(drawing: Drawing): BoundingBox {
    if (drawing.shapes.length === 0) {
      return { min: { x: 0, y: 0 }, max: { x: 1000, y: 1000 } };
    }

    const bounds = drawing.shapes.map(shape => this.calculateShapeBounds(shape));
    
    const minX = Math.min(...bounds.map(b => b.min.x));
    const minY = Math.min(...bounds.map(b => b.min.y));
    const maxX = Math.max(...bounds.map(b => b.max.x));
    const maxY = Math.max(...bounds.map(b => b.max.y));

    return { min: { x: minX, y: minY }, max: { x: maxX, y: maxY } };
  }

  /**
   * Check if a point is inside a shape
   */
  static isPointInShape(point: Point, shape: Shape): boolean {
    switch (shape.geometry.type) {
      case 'rectangle':
        return this.isPointInRectangle(point, shape.geometry);
      case 'circle':
        return this.isPointInCircle(point, shape.geometry);
      case 'polygon':
        return this.isPointInPolygon(point, shape.geometry.coordinates);
      default:
        return false;
    }
  }

  private static isPointInRectangle(point: Point, geometry: Geometry): boolean {
    if (!geometry.dimensions || geometry.coordinates.length === 0) return false;
    
    const topLeft = geometry.coordinates[0];
    return (
      point.x >= topLeft.x &&
      point.x <= topLeft.x + geometry.dimensions.width &&
      point.y >= topLeft.y &&
      point.y <= topLeft.y + geometry.dimensions.height
    );
  }

  private static isPointInCircle(point: Point, geometry: Geometry): boolean {
    if (!geometry.radius || geometry.coordinates.length === 0) return false;
    
    const center = geometry.coordinates[0];
    const distance = Math.sqrt(
      Math.pow(point.x - center.x, 2) + Math.pow(point.y - center.y, 2)
    );
    
    return distance <= geometry.radius;
  }

  private static isPointInPolygon(point: Point, vertices: Point[]): boolean {
    let inside = false;
    
    for (let i = 0, j = vertices.length - 1; i < vertices.length; j = i++) {
      const xi = vertices[i].x;
      const yi = vertices[i].y;
      const xj = vertices[j].x;
      const yj = vertices[j].y;
      
      const intersect = ((yi > point.y) !== (yj > point.y)) &&
        (point.x < (xj - xi) * (point.y - yi) / (yj - yi) + xi);
      
      if (intersect) inside = !inside;
    }
    
    return inside;
  }

  /**
   * Calculate distance between two points
   */
  static distance(p1: Point, p2: Point): number {
    return Math.sqrt(Math.pow(p2.x - p1.x, 2) + Math.pow(p2.y - p1.y, 2));
  }

  /**
   * Calculate area of a shape
   */
  static calculateArea(shape: Shape): number {
    switch (shape.geometry.type) {
      case 'rectangle':
        if (shape.geometry.dimensions) {
          return shape.geometry.dimensions.width * shape.geometry.dimensions.height;
        }
        break;
      case 'circle':
        if (shape.geometry.radius) {
          return Math.PI * Math.pow(shape.geometry.radius, 2);
        }
        break;
      case 'polygon':
        return this.calculatePolygonArea(shape.geometry.coordinates);
    }
    return 0;
  }

  private static calculatePolygonArea(vertices: Point[]): number {
    let area = 0;
    const n = vertices.length;
    
    for (let i = 0; i < n; i++) {
      const j = (i + 1) % n;
      area += vertices[i].x * vertices[j].y;
      area -= vertices[j].x * vertices[i].y;
    }
    
    return Math.abs(area) / 2;
  }

  /**
   * Snap point to grid
   */
  static snapToGrid(point: Point, gridSize: number = 10): Point {
    return {
      x: Math.round(point.x / gridSize) * gridSize,
      y: Math.round(point.y / gridSize) * gridSize,
    };
  }

  /**
   * Convert between different units
   */
  static convertUnits(
    value: number,
    fromUnit: 'mm' | 'cm' | 'm',
    toUnit: 'mm' | 'cm' | 'm'
  ): number {
    // Convert to mm first
    let mm = value;
    switch (fromUnit) {
      case 'cm':
        mm = value * 10;
        break;
      case 'm':
        mm = value * 1000;
        break;
    }

    // Convert from mm to target unit
    switch (toUnit) {
      case 'cm':
        return mm / 10;
      case 'm':
        return mm / 1000;
      default:
        return mm;
    }
  }
}