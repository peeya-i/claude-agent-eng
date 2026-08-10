# Claude Agent Eng

This is the Claude Code class working directory. It contains lab modules used to teach and practice working with [Claude Code](https://docs.claude.com/en/docs/claude-code), Anthropic's agentic coding CLI.

## What is Claude Code?

Claude Code is a command-line tool that lets Claude work directly in your terminal and codebase as an agentic collaborator. Instead of just answering questions, it can read your project, make changes, run commands, and verify its own work — end to end.

## Capabilities

- **Codebase understanding** — reads and searches across a project to build context before making changes, without requiring manual file selection.
- **Editing & refactoring** — makes multi-file edits, renames, and refactors directly in your working tree.
- **Shell & tooling access** — runs shell commands, package managers, linters, formatters, and test suites, and iterates based on the results.
- **Git & GitHub workflows** — stages changes, writes commit messages, opens pull requests, and can review PRs and CI output.
- **Debugging** — reproduces failures, inspects logs/stack traces, and proposes and applies fixes.
- **Test-driven work** — writes and runs tests, and checks its own changes against them before reporting completion.
- **Web & browser tools** — fetches documentation, searches the web, and can drive a browser to test UI changes or interact with web apps.
- **MCP (Model Context Protocol)** — connects to external tools and services (databases, issue trackers, APIs) through MCP servers.
- **Subagents** — delegates focused sub-tasks (e.g., broad code search, planning, review) to specialized agents to keep the main context efficient.
- **Custom commands & hooks** — supports project-specific slash commands and hooks that run automatically on events like tool calls.
- **Extended/plan mode** — can propose a step-by-step plan for approval before making larger or riskier changes.
- **Memory** — can persist useful context (preferences, project facts) across sessions when configured to do so.

## Repository Structure

```
claude-agent-eng/
└── class-01/
    ├── README.md   # class-01 overview and objectives
    └── BUILD.md    # setup and run instructions
```

Each `class-NN/` folder is a self-contained lab module with its own `README.md` (objectives) and `BUILD.md` (setup/run instructions).

## Getting Started

Start with [class-01/README.md](class-01/README.md).
