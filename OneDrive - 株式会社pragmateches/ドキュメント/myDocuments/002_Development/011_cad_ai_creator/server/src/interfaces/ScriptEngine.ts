import { StoreLayout } from '../types';

export interface ScriptCommand {
  type: string;
  parameters: Record<string, any>;
}

export interface ScriptExecutionContext {
  layout: StoreLayout;
  variables: Record<string, any>;
}

export interface ScriptExecutionResult {
  success: boolean;
  layout?: StoreLayout;
  error?: string;
  logs: string[];
}

export interface IScriptEngine {
  executeScript(script: string, context: ScriptExecutionContext): Promise<ScriptExecutionResult>;
  parseScript(script: string): ScriptCommand[];
  validateScript(script: string): { valid: boolean; errors: string[] };
}

export interface IScriptParser {
  parse(script: string): ScriptCommand[];
  validate(script: string): { valid: boolean; errors: string[] };
}

export interface IScriptExecutor {
  execute(commands: ScriptCommand[], context: ScriptExecutionContext): Promise<ScriptExecutionResult>;
}