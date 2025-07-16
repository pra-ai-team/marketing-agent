import { Request, Response } from 'express';
import { ScriptExecutionService } from '../services/ScriptExecutionService';
import { ScriptExecutionRequest, ScriptExecutionResponse } from '../types';

export class ScriptController {
  private scriptService: ScriptExecutionService;

  constructor() {
    this.scriptService = new ScriptExecutionService();
  }

  executeScript = async (req: Request, res: Response) => {
    try {
      const { script, drawingId, variables }: ScriptExecutionRequest = req.body;

      if (!script) {
        return res.status(400).json({
          success: false,
          error: 'Script is required',
        });
      }

      const result = await this.scriptService.executeScript(script, {
        drawingId,
        variables: variables || {},
      });

      const response: ScriptExecutionResponse = {
        success: result.success,
        data: result.success ? {
          drawing: result.drawing!,
          logs: result.logs,
        } : undefined,
        error: result.error?.message,
      };

      res.json(response);
    } catch (error) {
      console.error('Script execution error:', error);
      res.status(500).json({
        success: false,
        error: 'Internal server error',
      });
    }
  };

  validateScript = async (req: Request, res: Response) => {
    try {
      const { script } = req.body;

      if (!script) {
        return res.status(400).json({
          success: false,
          error: 'Script is required',
        });
      }

      const validationResult = await this.scriptService.validateScript(script);

      res.json({
        success: !validationResult,
        error: validationResult?.message,
        details: validationResult?.details,
      });
    } catch (error) {
      console.error('Script validation error:', error);
      res.status(500).json({
        success: false,
        error: 'Internal server error',
      });
    }
  };

  getCommands = async (req: Request, res: Response) => {
    try {
      const commands = await this.scriptService.getAvailableCommands();
      
      res.json({
        success: true,
        data: commands,
      });
    } catch (error) {
      console.error('Get commands error:', error);
      res.status(500).json({
        success: false,
        error: 'Internal server error',
      });
    }
  };
}