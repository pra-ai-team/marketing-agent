import { ScriptCommand, ScriptExecutionContext, ScriptExecutionResult } from '../types';

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