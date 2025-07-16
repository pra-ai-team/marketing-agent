// Core geometry types
export interface Point {
  x: number;
  y: number;
}

export interface Dimensions {
  width: number;
  height: number;
}

export interface Rectangle extends Point, Dimensions {}

export interface BoundingBox {
  min: Point;
  max: Point;
}

// Geometry types for CAD
export type GeometryType = 'line' | 'rectangle' | 'circle' | 'polygon';

export interface Geometry {
  type: GeometryType;
  coordinates: Point[];
  dimensions?: Dimensions;
  radius?: number; // For circles
}

// Shape types
export type ShapeType = 'wall' | 'column' | 'fixture' | 'equipment' | 'area' | 'door';

export interface RenderStyle {
  strokeColor?: string;
  fillColor?: string;
  strokeWidth?: number;
  lineStyle?: 'solid' | 'dashed' | 'dotted';
  opacity?: number;
}

export interface ShapeProperties {
  name?: string;
  category?: string;
  metadata?: Record<string, any>;
}

export interface Shape {
  id: string;
  type: ShapeType;
  geometry: Geometry;
  properties: ShapeProperties;
  label?: string;
  style: RenderStyle;
}

// Drawing types
export interface Layer {
  id: string;
  name: string;
  visible: boolean;
  locked: boolean;
  shapes: string[]; // Shape IDs
}

export interface DrawingMetadata {
  scale: number;
  units: 'mm' | 'cm' | 'm';
  bounds: BoundingBox;
  layers: Layer[];
}

export interface Drawing {
  id: string;
  name: string;
  shapes: Shape[];
  templates: Template[];
  metadata: DrawingMetadata;
  createdAt: Date;
  updatedAt: Date;
}

// Template types
export interface Template {
  id: string;
  name: string;
  description?: string;
  shapes: Shape[];
  thumbnail?: string;
}

// Store layout types (legacy compatibility)
export interface StoreElement {
  id: string;
  type: 'shelf' | 'checkout' | 'entrance' | 'wall' | 'custom';
  position: Point;
  dimensions: Dimensions;
  rotation: number;
  properties: Record<string, any>;
}

export interface StoreLayout {
  id: string;
  name: string;
  dimensions: Dimensions;
  elements: StoreElement[];
  metadata: {
    createdAt: Date;
    updatedAt: Date;
    version: string;
  };
}

// Script engine types
export interface ScriptCommand {
  name: string;
  category: 'drawing' | 'editing' | 'calculation' | 'file';
  parameters: Parameter[];
  description: string;
  examples: string[];
}

export interface Parameter {
  name: string;
  type: 'number' | 'string' | 'point' | 'shape';
  required: boolean;
  description: string;
}

export interface ScriptExecutionContext {
  drawing: Drawing;
  variables: Record<string, any>;
  selectedShapes: string[]; // Shape IDs
}

export interface ExecutionResult {
  success: boolean;
  drawing?: Drawing;
  error?: ScriptError;
  logs: string[];
  generatedScript?: string;
}

export interface ScriptError {
  type: 'syntax' | 'runtime' | 'validation';
  message: string;
  line?: number;
  column?: number;
  details?: string;
}

// AI Integration types
export interface Intent {
  action: string;
  target?: string;
  parameters?: Record<string, any>;
  confidence: number;
}

export interface DrawingContext {
  currentDrawing: Drawing;
  recentCommands: string[];
  availableShapes: Shape[];
}

// File import types
export interface ImportResult {
  success: boolean;
  drawing?: Drawing;
  script?: string;
  errors?: string[];
  warnings?: string[];
}

export interface CADData {
  entities: any[];
  blocks: any[];
  layers: any[];
  header: any;
}

// Error types
export type ErrorType = 'script' | 'file' | 'ai' | 'render';

export interface ErrorResponse {
  type: ErrorType;
  message: string;
  details?: string;
  suggestions?: string[];
  recoverable: boolean;
}

// API types
export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

export interface ScriptExecutionRequest {
  script: string;
  drawingId?: string;
  variables?: Record<string, any>;
}

export interface ScriptExecutionResponse extends ApiResponse {
  data?: {
    drawing: Drawing;
    logs: string[];
  };
}

export interface NaturalLanguageRequest {
  command: string;
  drawingId?: string;
  context?: DrawingContext;
}

export interface NaturalLanguageResponse extends ApiResponse {
  data?: {
    script: string;
    intent: Intent;
    clarifications?: string[];
  };
}

export interface FileImportRequest {
  fileType: 'dxf' | 'dwg';
  fileData: string | Buffer;
}

export interface FileImportResponse extends ApiResponse {
  data?: ImportResult;
}