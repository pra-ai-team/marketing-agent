import express from 'express';
import { ScriptController } from '../controllers/ScriptController';

const router = express.Router();
const scriptController = new ScriptController();

// Script execution endpoint
router.post('/execute', scriptController.executeScript);

// Script validation endpoint
router.post('/validate', scriptController.validateScript);

// Get available commands
router.get('/commands', scriptController.getCommands);

export { router as scriptRoutes };