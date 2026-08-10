# Build & Setup

## Prerequisites

- Node.js 18+ (for the Claude Code CLI)
- npm
- git

## Install Claude Code

```bash
npm install -g @anthropic-ai/claude-code
```

Verify the install:

```bash
claude --version
```

## Authentication

```bash
claude
```

Follow the prompts to log in with your Anthropic account on first run.

## Running

From this directory, start Claude Code:

```bash
cd class-01
claude
```

## Troubleshooting

- If `claude` is not found, confirm your global npm bin directory is on `PATH`.
- Run `/doctor` inside an interactive `claude` session to check for configuration issues.
