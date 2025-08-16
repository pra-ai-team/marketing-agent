import { Request, Response, NextFunction } from 'express';
import { ErrorResponse } from '../types';

export const errorHandler = (
  error: Error,
  req: Request,
  res: Response,
  next: NextFunction
) => {
  console.error('Error:', error);

  // Default error response
  const errorResponse: ErrorResponse = {
    type: 'script',
    message: 'An unexpected error occurred',
    details: error.message,
    recoverable: false,
  };

  // Determine error type and set appropriate response
  if (error.name === 'ValidationError') {
    errorResponse.type = 'script';
    errorResponse.message = 'Validation failed';
    errorResponse.recoverable = true;
  } else if (error.name === 'SyntaxError') {
    errorResponse.type = 'script';
    errorResponse.message = 'Script syntax error';
    errorResponse.recoverable = true;
  } else if (error.name === 'TypeError') {
    errorResponse.type = 'script';
    errorResponse.message = 'Type error in script';
    errorResponse.recoverable = true;
  }

  // Send error response
  res.status(500).json({
    success: false,
    error: errorResponse,
  });
};