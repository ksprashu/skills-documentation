# Documentation & Visual Portal Engine (`skills-documentation`)

A unified documentation compiler, visual portal builder, report scaffolder/sanitizer, and automated lifecycle archiving engine for Google Antigravity and AI coding assistants.

## Features

1. **Visual-First Interactive Portal Builder**: Compiles project Markdown files with 4 premium Stitch themes (`technical`, `obsidian`, `proscript`, `dynamics`).
2. **HTML Report Scaffolder & Sanitizer**: Scaffolds high-fidelity visual HTML review reports and sweeps them to strip trailing `&nbsp;`, balance container tags (`<div>`), and verify responsive CSS.
3. **Automated Lifecycle Sync Engine**: Hooked into Google Antigravity events to sync brain files (`task.md`, `implementation_plan.md`, `walkthrough.md`) to `docs/`.

## Usage

### Compile Workspace Documentation
```bash
python3 skills/documentation/scripts/compile_docs.py
```

### Watch & Auto-Compile Docs
```bash
python3 skills/documentation/scripts/watch_docs.py
```

## License

Apache License 2.0. See [LICENSE](LICENSE) for details.
