const express = require('express');
const codeExecutorRoutes = require('./routes/codeExecutor.ts');
// const shutdownRoutes = require('./routes/shutdown');
// const llmRoutes = require('./routes/llm');

const app = express();
const PORT = 3000;

// Middleware to parse incoming requests with JSON payloads
app.use(express.json());

// Register routes
app.use('/execute', codeExecutorRoutes);
// app.use('/shutdown', shutdownRoutes);
// app.use('/llm', llmRoutes);

// Start the Express server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});

module.exports = app;
