# Pixi Quick Reference

> Full docs: https://pixi.sh | [Getting Started](https://prefix-dev.github.io/pixi/latest/getting_started/)

## Essential Commands

```bash
# Workspace & Dependencies
pixi init                 # Initialize new pixi project
pixi install              # Install dependencies from lock file
pixi add <package>        # Add dependency
pixi remove <package>     # Remove dependency
pixi update               # Update lock file
pixi upgrade              # Upgrade all dependencies to latest versions
pixi lock                 # Create/update lockfile
pixi list                 # List installed packages
pixi tree                 # Show dependency tree
pixi info                 # Show environment info
pixi clean                # Remove environments from machine

# Execution
pixi run <task>           # Run a defined task
pixi run <command>        # Run arbitrary command in environment
pixi shell                # Start interactive shell in environment
pixi exec <command>       # Run command in temporary environment
pixi exec --spec "python=3.12" python  # Run with specific spec
```

## Task Management

```bash
# Adding tasks
pixi task add <name> "<cmd>"                    # Add simple task
pixi task add <name> "<cmd>" --depends-on task2 # With dependencies
pixi task add <name> "<cmd>" --feature feat     # For specific feature

# Managing tasks
pixi task list                # List all tasks
pixi task remove <name>       # Remove task

# Task definition in pyproject.toml/pixi.toml
[tasks]
build = "make build"
test = "pytest"
serve = "python -m http.server"

[tasks.test]
cmd = "pytest tests/"
depends-on = ["build"]
```

## Multiple Environments

```bash
# Add feature/environment
pixi add --feature dev pytest              # Add to dev feature
pixi add --feature test coverage           # Add to test feature

# Environment management
pixi workspace environment add test         # Add environment to workspace
pixi run -e dev pytest                     # Run task in specific environment
pixi shell -e test                         # Activate specific environment
pixi list -e dev                           # List packages in environment

# Configuration
[tool.pixi.environments]
default = {solve-group = "default"}
dev = {features = ["dev"], solve-group = "dev"}
test = {features = ["test"], solve-group = "test"}

[tool.pixi.features]
dev = {dependencies = {pytest = "*", black = "*"}}
test = {dependencies = {coverage = "*"}}
```

## Global Tools

```bash
# Install tools globally
pixi global install ruff              # Install tool in its own environment
pixi global install mypy --version "*" # Specify version
pixi global add ruff black            # Add to existing global environment

# Managing global tools
pixi global list                      # List all global environments
pixi global update                    # Update global environments
pixi global uninstall ruff            # Remove global tool
pixi global sync                      # Sync with global manifest
pixi global edit                      # Edit global manifest
```

## Multi-Platform Support

```bash
# Add platform-specific dependencies
pixi add --platform win-64 pywin32    # Windows only
pixi add --platform linux-64 patchelf  # Linux only

# Configuration
[tool.pixi.workspace]
channels = ["conda-forge"]
platforms = ["linux-64", "osx-arm64", "win-64"]
```

## Configuration (pyproject.toml / pixi.toml)

```toml
[tool.pixi.workspace]
channels = ["conda-forge", "pytorch"]
platforms = ["linux-64", "osx-arm64"]

[tool.pixi.dependencies]
python = ">=3.11"
numpy = ">=1.21"
scipy = "*"

# Platform-specific dependencies
[tool.pixi.dependencies.win-64]
pywin32 = "*"

# Feature-based dependencies
[tool.pixi.features]
dev = {dependencies = {pytest = "*", black = "*"}}
docs = {dependencies = {sphinx = "*"}}

[tool.pixi.tasks]
test = "pytest"
sim = "python simulation/run_simulation.py"
format = "black ."
lint = "ruff check ."
```

## Common Flags

| Flag | Use |
|------|-----|
| `--frozen` | Use exact lock file, don't update |
| `--locked` | Fail if lock file is outdated |
| `--environment <name>` / `-e` | Select specific environment |
| `--platform <plat>` / `-p` | Target specific platform |
| `--feature <feat>` | Work with specific feature |

## Useful Commands

```bash
pixi search <package>     # Search for package
pixi auth login           # Authenticate with conda channels
pixi completion <shell>   # Generate shell completions
pixi help                 # Show all commands
pixi help <command>       # Show help for specific command
```

## Environment Variables

- `PIXI_HOME`: Override pixi installation directory
- `PIXI_FROZEN=true`: Always use frozen mode
- `PIXI_LOCKED=true`: Always use locked mode
- `PIXI_VERBOSE`: Enable verbose output
