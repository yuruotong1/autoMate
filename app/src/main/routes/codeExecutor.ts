const { Router } = require('express');
const bodyParser = require('body-parser');
const { spawn } = require('child_process');

const router = Router();

// Parse incoming JSON
router.use(bodyParser.json());

// Define the '/execute' route to run Python code
router.post('/', (req, res) => {
    const code = req.body.code;  // The Python code to execute

    // Spawn a Python subprocess to execute the code
    const pyProcess = spawn('python', ['-c', code]);

    let output = '';
    let errorOutput = '';

    // Capture the Python process output (stdout)
    pyProcess.stdout.on('data', (data) => {
        output += data.toString();
    });

    // Capture any errors (stderr)
    pyProcess.stderr.on('data', (data) => {
        errorOutput += data.toString();
    });

    // When the Python process finishes
    pyProcess.on('close', (code) => {
        if (code === 0) {
            res.json({ status: 'success', result: output });
        } else {
            res.json({ status: 'error', result: errorOutput });
        }
    });
});

module.exports = router;
