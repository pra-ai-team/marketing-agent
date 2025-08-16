import { StoreLayout, StoreElement } from '../types';

export interface ILayoutRenderer {
  render(layout: StoreLayout): void;
  clear(): void;
  addElement(element: StoreElement): void;
  removeElement(elementId: string): void;
  updateElement(elementId: string, updates: Partial<StoreElement>): void;
  getCanvas(): HTMLCanvasElement | null;
}

export interface IRenderingEngine {
  initialize(canvas: HTMLCanvasElement): void;
  drawElement(element: StoreElement): void;
  clearCanvas(): void;
  setViewport(x: number, y: number, zoom: number): void;
}