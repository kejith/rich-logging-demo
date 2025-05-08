# Rich Logging Demo

This project demonstrates the capabilities of the [Rich](https://github.com/Textualize/rich) Python package, particularly for enhancing logging output and terminal presentations.

## Features Demonstrated

- Colorful and formatted logging
- Progress bars
- Tables
- Panels
- Traceback formatting
- Live updates
- Syntax highlighting
- Multi-threaded logging

## Setup

1. Install the requirements:

```bash
pip install -r requirements.txt
```

## Development Container

This project includes a dev container configuration, making it easy to get started with a consistent development environment:

1. Open the project in VS Code with the Dev Containers extension installed
2. When prompted, click "Reopen in Container"
3. The container will be built with all necessary dependencies installed

## Running the Demos

The project includes two main demonstration scripts:

### grid.py

Run the grid demo with:

```bash
python grid.py
```

This script demonstrates Rich's layout capabilities by displaying a grid of panels with different formatting options and styles.

### demo.py

Run the comprehensive demo with:

```bash
python demo.py
```

This script showcases multiple Rich features including:
- Colorful console logging
- Progress bars for tracking operations
- Tables for structured data display
- Formatted error tracebacks
- Live updating displays
- Syntax highlighting of code snippets

## Key Concepts

- **Rich Logging**: The `RichHandler` integrates with Python's standard logging module to provide enhanced visual output
- **Formatting**: Use markup syntax like `[bold red]text[/]` to format your log messages
- **Progress Tracking**: Visual indicators for long-running tasks
- **Tables and Panels**: Structured information display
- **Traceback Handling**: More readable error traces with syntax highlighting

## Learn More

- [Rich Documentation](https://rich.readthedocs.io/)
- [Rich GitHub Repository](https://github.com/Textualize/rich)

Happy logging!
