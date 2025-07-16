import React, { useState, useEffect, useCallback } from 'react';
import { CanvasRenderer } from './CanvasRenderer';
import { ScriptEditor } from './ScriptEditor';
import { ScriptEngine } from '../../services/scriptEngine';
import { RenderingService } from '../../services/renderingService';
import { Drawing, Shape, Point, ScriptError, ExecutionResult } from '../../types';
import { v4 as uuidv4 } from 'uuid';
import './CADEngine.css';

const CADEngine: React.FC = () => {
  const [drawing, setDrawing] = useState<Drawing>({
    id: uuidv4(),
    name: 'New Drawing',
    shapes: [],
    templates: [],
    metadata: {
      scale: 1,
      units: 'mm',
      bounds: { min: { x: 0, y: 0 }, max: { x: 1000, y: 1000 } },
      layers: [
        {
          id: 'default',
          name: 'Default',
          visible: true,
          locked: false,
          shapes: [],
        },
      ],
    },
    createdAt: new Date(),
    updatedAt: new Date(),
  });

  const [script, setScript] = useState<string>(`# Welcome to CAD Script Engine
# Draw a simple store layout

# Create the store perimeter
cad.draw_wall((0, 0), (2000, 0), 100)      # Front wall
cad.draw_wall((2000, 0), (2000, 1500), 100) # Right wall
cad.draw_wall((2000, 1500), (0, 1500), 100) # Back wall
cad.draw_wall((0, 1500), (0, 0), 100)      # Left wall

# Add entrance
cad.draw_door((900, 0), 800, "right")

# Place checkout counters
cad.place_fixture((200, 200), 400, 100, "checkout counter")
cad.place_fixture((200, 350), 400, 100, "checkout counter")

# Place shelves
cad.place_fixture((800, 400), 300, 100, "shelf")
cad.place_fixture((1200, 400), 300, 100, "shelf")
cad.place_fixture((800, 600), 300, 100, "shelf")
cad.place_fixture((1200, 600), 300, 100, "shelf")

# Create storage area
cad.create_area([(1600, 1000), (1900, 1000), (1900, 1400), (1600, 1400)], "storage")

# Log completion
cad.log("Store layout created successfully!")
`);

  const [selectedShape, setSelectedShape] = useState<Shape | null>(null);
  const [isExecuting, setIsExecuting] = useState(false);
  const [errors, setErrors] = useState<ScriptError[]>([]);
  const [logs, setLogs] = useState<string[]>([]);
  const [scriptEngine] = useState(() => new ScriptEngine());
  const [isEngineReady, setIsEngineReady] = useState(false);

  // Initialize script engine
  useEffect(() => {
    const initEngine = async () => {
      try {
        await scriptEngine.initialize();
        setIsEngineReady(true);
      } catch (error) {
        console.error('Failed to initialize script engine:', error);
        setErrors([
          {
            type: 'runtime',
            message: 'Failed to initialize Python script engine. Please refresh the page.',
            details: error instanceof Error ? error.message : String(error),
          },
        ]);
      }
    };

    initEngine();
  }, [scriptEngine]);

  // Update drawing bounds when shapes change
  useEffect(() => {
    if (drawing.shapes.length > 0) {
      const bounds = RenderingService.calculateDrawingBounds(drawing);
      setDrawing(prev => ({
        ...prev,
        metadata: {
          ...prev.metadata,
          bounds,
        },
      }));
    }
  }, [drawing.shapes]);

  const handleScriptExecute = useCallback(async () => {
    if (!isEngineReady) {
      setErrors([
        {
          type: 'runtime',
          message: 'Script engine is not ready. Please wait...',
        },
      ]);
      return;
    }

    setIsExecuting(true);
    setErrors([]);
    setLogs([]);

    try {
      const result: ExecutionResult = await scriptEngine.execute(script, {
        drawing,
        variables: {},
        selectedShapes: selectedShape ? [selectedShape.id] : [],
      });

      if (result.success && result.drawing) {
        setDrawing(result.drawing);
        setLogs(result.logs || []);
      } else if (result.error) {
        setErrors([result.error]);
      }
    } catch (error) {
      setErrors([
        {
          type: 'runtime',
          message: 'Script execution failed',
          details: error instanceof Error ? error.message : String(error),
        },
      ]);
    } finally {
      setIsExecuting(false);
    }
  }, [script, drawing, selectedShape, scriptEngine, isEngineReady]);

  const handleShapeSelect = useCallback((shape: Shape) => {
    setSelectedShape(shape);
  }, []);

  const handleCoordinateClick = useCallback((point: Point) => {
    console.log('Clicked at:', point);
    // Could add point info to logs or status
  }, []);

  const handleClearDrawing = () => {
    setDrawing(prev => ({
      ...prev,
      shapes: [],
      updatedAt: new Date(),
    }));
    setSelectedShape(null);
    setLogs([]);
  };

  const handleSaveDrawing = () => {
    const dataStr = JSON.stringify(drawing, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
    
    const exportFileDefaultName = `${drawing.name}_${new Date().toISOString().split('T')[0]}.json`;
    
    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
  };

  const availableCommands = scriptEngine.getAvailableCommands();

  return (
    <div className="cad-engine">
      <div className="cad-header">
        <h1>CAD Script Engine</h1>
        <div className="cad-controls">
          <button onClick={handleClearDrawing} className="clear-button">
            Clear Drawing
          </button>
          <button onClick={handleSaveDrawing} className="save-button">
            Save Drawing
          </button>
        </div>
      </div>

      <div className="cad-content">
        <div className="left-panel">
          <ScriptEditor
            code={script}
            onCodeChange={setScript}
            onExecute={handleScriptExecute}
            errors={errors}
            isExecuting={isExecuting}
            availableCommands={availableCommands}
          />
        </div>

        <div className="right-panel">
          <div className="canvas-section">
            <CanvasRenderer
              drawing={drawing}
              onShapeSelect={handleShapeSelect}
              onCoordinateClick={handleCoordinateClick}
              width={800}
              height={600}
            />
          </div>

          <div className="info-section">
            <div className="shape-info">
              <h4>Selected Shape</h4>
              {selectedShape ? (
                <div className="shape-details">
                  <p><strong>ID:</strong> {selectedShape.id}</p>
                  <p><strong>Type:</strong> {selectedShape.type}</p>
                  <p><strong>Name:</strong> {selectedShape.properties.name || 'Unnamed'}</p>
                  {selectedShape.label && (
                    <p><strong>Label:</strong> {selectedShape.label}</p>
                  )}
                </div>
              ) : (
                <p>No shape selected</p>
              )}
            </div>

            <div className="logs-section">
              <h4>Execution Logs</h4>
              <div className="logs-container">
                {logs.length > 0 ? (
                  logs.map((log, index) => (
                    <div key={index} className="log-item">
                      {log}
                    </div>
                  ))
                ) : (
                  <p>No logs yet</p>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="cad-status">
        <div className="status-item">
          <span>Engine: {isEngineReady ? 'Ready' : 'Loading...'}</span>
        </div>
        <div className="status-item">
          <span>Shapes: {drawing.shapes.length}</span>
        </div>
        <div className="status-item">
          <span>Scale: {drawing.metadata.scale}x</span>
        </div>
        <div className="status-item">
          <span>Units: {drawing.metadata.units}</span>
        </div>
      </div>
    </div>
  );
};

export default CADEngine;