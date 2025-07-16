import React, { useEffect, useRef, useState } from 'react';
import { fabric } from 'fabric';
import { Shape, Point, Drawing, RenderStyle } from '../../types';

interface CanvasRendererProps {
  drawing: Drawing;
  onShapeSelect: (shape: Shape) => void;
  onCoordinateClick: (point: Point) => void;
  width?: number;
  height?: number;
}

export const CanvasRenderer: React.FC<CanvasRendererProps> = ({
  drawing,
  onShapeSelect,
  onCoordinateClick,
  width = 800,
  height = 600,
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const fabricCanvasRef = useRef<fabric.Canvas | null>(null);
  const [zoom, setZoom] = useState(1);
  const [pan, setPan] = useState<Point>({ x: 0, y: 0 });

  useEffect(() => {
    if (!canvasRef.current) return;

    // Initialize Fabric.js canvas
    const canvas = new fabric.Canvas(canvasRef.current, {
      width,
      height,
      selection: true,
      backgroundColor: '#f5f5f5',
    });

    fabricCanvasRef.current = canvas;

    // Handle mouse events
    canvas.on('mouse:down', (e) => {
      if (e.e.shiftKey) {
        // Pan mode
        canvas.selection = false;
        canvas.setCursor('move');
      }
    });

    canvas.on('mouse:move', (e) => {
      if (e.e.shiftKey && e.e.buttons === 1) {
        const delta = new fabric.Point(e.e.movementX, e.e.movementY);
        canvas.relativePan(delta);
        setPan({ x: canvas.viewportTransform![4], y: canvas.viewportTransform![5] });
      }
    });

    canvas.on('mouse:up', () => {
      canvas.selection = true;
      canvas.setCursor('default');
    });

    canvas.on('mouse:wheel', (e) => {
      const delta = e.e.deltaY;
      let newZoom = canvas.getZoom();
      newZoom *= 0.999 ** delta;
      newZoom = Math.max(0.1, Math.min(5, newZoom));
      
      canvas.zoomToPoint({ x: e.e.offsetX, y: e.e.offsetY }, newZoom);
      setZoom(newZoom);
      e.e.preventDefault();
      e.e.stopPropagation();
    });

    canvas.on('mouse:dblclick', (e) => {
      const pointer = canvas.getPointer(e.e);
      onCoordinateClick({ x: pointer.x, y: pointer.y });
    });

    canvas.on('selection:created', (e) => {
      const selected = e.selected?.[0];
      if (selected && selected.data) {
        onShapeSelect(selected.data as Shape);
      }
    });

    return () => {
      canvas.dispose();
    };
  }, [width, height, onShapeSelect, onCoordinateClick]);

  useEffect(() => {
    if (!fabricCanvasRef.current) return;

    const canvas = fabricCanvasRef.current;
    canvas.clear();

    // Render shapes
    drawing.shapes.forEach((shape) => {
      const fabricObject = createFabricObject(shape);
      if (fabricObject) {
        fabricObject.data = shape;
        canvas.add(fabricObject);
      }
    });

    canvas.renderAll();
  }, [drawing]);

  const createFabricObject = (shape: Shape): fabric.Object | null => {
    const style = shape.style;
    const commonProps = {
      stroke: style.strokeColor || '#000000',
      strokeWidth: style.strokeWidth || 1,
      fill: style.fillColor || 'transparent',
      opacity: style.opacity || 1,
      strokeDashArray: getStrokeDashArray(style),
      selectable: true,
      hasControls: true,
      hasBorders: true,
    };

    switch (shape.geometry.type) {
      case 'line':
        if (shape.geometry.coordinates.length >= 2) {
          const points = shape.geometry.coordinates;
          return new fabric.Line(
            [points[0].x, points[0].y, points[1].x, points[1].y],
            commonProps
          );
        }
        break;

      case 'rectangle':
        if (shape.geometry.coordinates.length > 0 && shape.geometry.dimensions) {
          return new fabric.Rect({
            left: shape.geometry.coordinates[0].x,
            top: shape.geometry.coordinates[0].y,
            width: shape.geometry.dimensions.width,
            height: shape.geometry.dimensions.height,
            ...commonProps,
          });
        }
        break;

      case 'circle':
        if (shape.geometry.coordinates.length > 0 && shape.geometry.radius) {
          return new fabric.Circle({
            left: shape.geometry.coordinates[0].x - shape.geometry.radius,
            top: shape.geometry.coordinates[0].y - shape.geometry.radius,
            radius: shape.geometry.radius,
            ...commonProps,
          });
        }
        break;

      case 'polygon':
        if (shape.geometry.coordinates.length >= 3) {
          return new fabric.Polygon(
            shape.geometry.coordinates.map(p => ({ x: p.x, y: p.y })),
            commonProps
          );
        }
        break;
    }

    return null;
  };

  const getStrokeDashArray = (style: RenderStyle): number[] | undefined => {
    switch (style.lineStyle) {
      case 'dashed':
        return [10, 5];
      case 'dotted':
        return [2, 2];
      default:
        return undefined;
    }
  };

  const handleZoomIn = () => {
    if (!fabricCanvasRef.current) return;
    const canvas = fabricCanvasRef.current;
    const newZoom = Math.min(canvas.getZoom() * 1.2, 5);
    canvas.setZoom(newZoom);
    setZoom(newZoom);
  };

  const handleZoomOut = () => {
    if (!fabricCanvasRef.current) return;
    const canvas = fabricCanvasRef.current;
    const newZoom = Math.max(canvas.getZoom() / 1.2, 0.1);
    canvas.setZoom(newZoom);
    setZoom(newZoom);
  };

  const handleResetView = () => {
    if (!fabricCanvasRef.current) return;
    const canvas = fabricCanvasRef.current;
    canvas.setZoom(1);
    canvas.setViewportTransform([1, 0, 0, 1, 0, 0]);
    setZoom(1);
    setPan({ x: 0, y: 0 });
  };

  return (
    <div className="canvas-renderer">
      <div className="canvas-toolbar">
        <button onClick={handleZoomIn} title="Zoom In">+</button>
        <button onClick={handleZoomOut} title="Zoom Out">-</button>
        <button onClick={handleResetView} title="Reset View">⟲</button>
        <span className="zoom-level">{(zoom * 100).toFixed(0)}%</span>
        <span className="coordinates">
          Pan: ({pan.x.toFixed(0)}, {pan.y.toFixed(0)})
        </span>
      </div>
      <canvas ref={canvasRef} />
      <div className="canvas-info">
        <p>Shift + Drag: Pan | Scroll: Zoom | Double-click: Get coordinates</p>
      </div>
    </div>
  );
};