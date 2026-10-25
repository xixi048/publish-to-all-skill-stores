#!/usr/bin/env node
/* Launcher for the bundled Python MCP server. Requires Python 3.8+ on PATH. */
const { spawn } = require('node:child_process');
const path = require('node:path');

const server = path.join(__dirname, '..', 'mcp', 'server.py');
const py = process.env.PYTHON || (process.platform === 'win32' ? 'python' : 'python3');

const child = spawn(py, [server], { stdio: 'inherit' });
child.on('error', (err) => {
  console.error(`[publish-to-all-skill-stores-mcp] could not start ${py}: ${err.message}`);
  console.error('Python 3.8+ is required. Set PYTHON=/path/to/python3 to override.');
  process.exit(127);
});
child.on('exit', (code) => process.exit(code ?? 0));
for (const sig of ['SIGINT', 'SIGTERM']) {
  process.on(sig, () => child.kill(sig));
}
