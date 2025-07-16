import React, { useState, useRef, useEffect } from 'react';
import { ScriptError } from '../../types';
import './ScriptEditor.css';

interface ScriptEditorProps {
  code: string;
  onCodeChange: (code: string) => void;
  onExecute: () => void;
  errors: ScriptError[];
  isExecuting: boolean;
  availableCommands: string[];
}

export const ScriptEditor: React.FC<ScriptEditorProps> = ({
  code,
  onCodeChange,
  onExecute,
  errors,
  isExecuting,
  availableCommands,
}) => {
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const [showHelp, setShowHelp] = useState(false);
  const [lineNumbers, setLineNumbers] = useState<number[]>([]);

  // Update line numbers when code changes
  useEffect(() => {
    const lines = code.split('\n');
    setLineNumbers(lines.map((_, index) => index + 1));
  }, [code]);

  // Handle keyboard shortcuts
  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Tab') {
      e.preventDefault();
      insertAtCursor('    '); // 4 spaces for indentation
    } else if (e.ctrlKey && e.key === 'Enter') {
      e.preventDefault();
      onExecute();
    }
  };

  const insertAtCursor = (text: string) => {
    const textarea = textareaRef.current;
    if (!textarea) return;

    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const newCode = code.substring(0, start) + text + code.substring(end);
    
    onCodeChange(newCode);
    
    // Set cursor position after insertion
    setTimeout(() => {
      textarea.focus();
      textarea.setSelectionRange(start + text.length, start + text.length);
    }, 0);
  };

  const insertCommand = (command: string) => {
    insertAtCursor(command + '\n');
  };

  const getErrorForLine = (lineNumber: number): ScriptError | undefined => {
    return errors.find(error => error.line === lineNumber);
  };

  return (
    <div className="script-editor">
      <div className="editor-header">
        <h3>Python Script Editor</h3>
        <div className="editor-controls">
          <button
            onClick={() => setShowHelp(!showHelp)}
            className="help-button"
            title="Show/Hide Commands"
          >
            ?
          </button>
          <button
            onClick={onExecute}
            disabled={isExecuting}
            className="execute-button"
            title="Execute Script (Ctrl+Enter)"
          >
            {isExecuting ? 'Executing...' : 'Execute'}
          </button>
        </div>
      </div>

      <div className="editor-content">
        <div className="editor-main">
          <div className="line-numbers">
            {lineNumbers.map((lineNumber) => {
              const error = getErrorForLine(lineNumber);
              return (
                <div
                  key={lineNumber}
                  className={`line-number ${error ? 'error' : ''}`}
                  title={error ? error.message : ''}
                >
                  {lineNumber}
                </div>
              );
            })}
          </div>
          
          <textarea
            ref={textareaRef}
            value={code}
            onChange={(e) => onCodeChange(e.target.value)}
            onKeyDown={handleKeyDown}
            className="code-input"
            placeholder="# Enter your Python script here
# Example:
# cad.draw_wall((0, 0), (1000, 0), 100)
# cad.place_fixture((200, 200), 300, 100, 'shelf')
"
            spellCheck={false}
          />
        </div>

        {showHelp && (
          <div className="commands-panel">
            <h4>Available Commands</h4>
            <div className="commands-list">
              {availableCommands.map((command, index) => (
                <div key={index} className="command-item">
                  <button
                    onClick={() => insertCommand(command)}
                    className="command-button"
                    title="Click to insert"
                  >
                    {command}
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {errors.length > 0 && (
        <div className="error-panel">
          <h4>Errors</h4>
          {errors.map((error, index) => (
            <div key={index} className={`error-item ${error.type}`}>
              <div className="error-header">
                <span className="error-type">{error.type}</span>
                {error.line && <span className="error-line">Line {error.line}</span>}
              </div>
              <div className="error-message">{error.message}</div>
              {error.details && (
                <div className="error-details">{error.details}</div>
              )}
            </div>
          ))}
        </div>
      )}

      <div className="editor-footer">
        <small>
          Shortcuts: Tab for indentation, Ctrl+Enter to execute
        </small>
      </div>
    </div>
  );
};