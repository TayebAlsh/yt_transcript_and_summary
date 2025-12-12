# Create Plugin System

You are a plugin architecture specialist for the YouTube Transcript & Summary app.

## Your Mission
Design and implement a plugin/extension system to allow users to extend the app's functionality without modifying core code.

## Plugin System Goals
1. **Extensibility**: Easy to add new features
2. **Modularity**: Plugins are self-contained
3. **Discoverability**: Auto-detect and load plugins
4. **Configuration**: Plugins can have their own settings
5. **Safety**: Isolated execution, error handling
6. **Documentation**: Clear plugin API and examples

## Plugin Types

### 1. Export Format Plugins
Add new output formats:
- Plugin provides format name and export function
- Receives content_dict, returns formatted output
- Handles own dependencies

### 2. Summarization Style Plugins
Custom summarization approaches:
- Bullet points, chapters, Q&A format, etc.
- Receives transcript segments
- Returns custom summary structure

### 3. Analysis Plugins
Custom content analysis:
- Topic extraction, sentiment, etc.
- Receives transcript, returns analysis results
- Integrated into output

### 4. Transcription Enhancement Plugins
Post-process transcriptions:
- Punctuation correction
- Formatting improvements
- Error correction
- Capitalization fixes

### 5. Integration Plugins
Connect to external services:
- Export to Notion, Obsidian, Anki
- Post to social media
- Send to read-it-later services
- Cloud storage upload

### 6. UI Plugins (Streamlit)
Add UI components:
- Custom visualizations
- Interactive widgets
- Additional controls
- Custom dashboards

## Plugin Architecture

### Directory Structure
```
plugins/
  __init__.py
  base.py              # Base plugin classes
  registry.py          # Plugin discovery and loading
  builtin/
    __init__.py
    bullet_summary.py
    srt_export.py
  user/
    __init__.py
    my_custom_plugin.py
```

### Base Plugin Class
```python
# plugins/base.py
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class Plugin(ABC):
    """Base class for all plugins."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Plugin name."""
        pass

    @property
    @abstractmethod
    def version(self) -> str:
        """Plugin version."""
        pass

    @property
    def description(self) -> str:
        """Plugin description."""
        return ""

    @property
    def author(self) -> str:
        """Plugin author."""
        return "Unknown"

    def initialize(self, config: Optional[Dict[str, Any]] = None):
        """Initialize plugin with config."""
        pass

    def cleanup(self):
        """Cleanup plugin resources."""
        pass


class ExportPlugin(Plugin):
    """Plugin for custom export formats."""

    @property
    @abstractmethod
    def format_extension(self) -> str:
        """File extension (e.g., 'docx', 'epub')."""
        pass

    @abstractmethod
    def export(self, content_dict: Dict[str, Any], output_path: Path) -> None:
        """Export content to format."""
        pass

    def get_mime_type(self) -> str:
        """Return MIME type for downloads."""
        return "application/octet-stream"


class SummaryPlugin(Plugin):
    """Plugin for custom summary styles."""

    @property
    @abstractmethod
    def style_name(self) -> str:
        """Summary style name (e.g., 'bullets', 'chapters')."""
        pass

    @abstractmethod
    def summarize(self, segments: List[Segment], **kwargs) -> Dict[str, Any]:
        """Generate custom summary."""
        pass


class AnalysisPlugin(Plugin):
    """Plugin for content analysis."""

    @property
    @abstractmethod
    def analysis_type(self) -> str:
        """Analysis type (e.g., 'sentiment', 'topics')."""
        pass

    @abstractmethod
    def analyze(self, segments: List[Segment]) -> Dict[str, Any]:
        """Analyze content and return results."""
        pass
```

### Plugin Registry
```python
# plugins/registry.py
import importlib
import pkgutil
from pathlib import Path
from typing import Dict, List, Type

class PluginRegistry:
    """Discovers and manages plugins."""

    def __init__(self):
        self._plugins: Dict[str, Plugin] = {}

    def discover_plugins(self, plugin_dir: Path):
        """Auto-discover plugins in directory."""
        for _, name, _ in pkgutil.iter_modules([str(plugin_dir)]):
            try:
                module = importlib.import_module(f"plugins.user.{name}")
                # Find Plugin subclasses in module
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if (isinstance(attr, type) and
                        issubclass(attr, Plugin) and
                        attr is not Plugin):
                        plugin = attr()
                        self._plugins[plugin.name] = plugin
            except Exception as e:
                print(f"Failed to load plugin {name}: {e}")

    def get_plugin(self, name: str) -> Optional[Plugin]:
        """Get plugin by name."""
        return self._plugins.get(name)

    def list_plugins(self, plugin_type: Type[Plugin] = Plugin) -> List[Plugin]:
        """List all plugins of given type."""
        return [p for p in self._plugins.values()
                if isinstance(p, plugin_type)]


# Global registry
registry = PluginRegistry()
```

### Example Plugin: DOCX Export
```python
# plugins/user/docx_export.py
from pathlib import Path
from typing import Dict, Any
from plugins.base import ExportPlugin

try:
    from docx import Document
    from docx.shared import Pt, Inches
except ImportError:
    Document = None


class DocxExportPlugin(ExportPlugin):
    """Export to Microsoft Word format."""

    @property
    def name(self) -> str:
        return "DOCX Export"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def description(self) -> str:
        return "Export summaries as Microsoft Word documents"

    @property
    def author(self) -> str:
        return "Your Name"

    @property
    def format_extension(self) -> str:
        return "docx"

    def export(self, content_dict: Dict[str, Any], output_path: Path) -> None:
        """Export to DOCX format."""
        if Document is None:
            raise ImportError("python-docx not installed")

        doc = Document()

        # Title
        doc.add_heading(content_dict['title'], 0)

        # Source
        doc.add_paragraph(f"Source: {content_dict['url']}")

        # TLDR
        doc.add_heading("TLDR", 1)
        doc.add_paragraph(content_dict['tldr'])

        # Detailed Summary
        doc.add_heading("Detailed Summary", 1)
        doc.add_paragraph(content_dict['detailed'])

        # Full Transcript
        doc.add_heading("Full Transcript", 1)
        doc.add_paragraph(content_dict['transcript'])

        # Timestamped Transcript
        if content_dict.get('segments'):
            doc.add_heading("Timestamped Transcript", 1)
            for seg in content_dict['segments']:
                start = seg.get('start', 0.0)
                timestamp = f"{int(start // 60):02d}:{start % 60:05.2f}"
                speaker = f"[{seg.get('speaker')}] " if seg.get('speaker') else ""
                doc.add_paragraph(
                    f"{timestamp} {speaker}{seg.get('text', '')}",
                    style='List Bullet'
                )

        doc.save(str(output_path))

    def get_mime_type(self) -> str:
        return "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
```

## Integration into App

### Load Plugins at Startup
```python
# In yt_transcribe_and_summarize.py
from plugins.registry import registry

def load_plugins():
    """Load all plugins."""
    plugin_dir = Path(__file__).parent / "plugins" / "user"
    plugin_dir.mkdir(exist_ok=True)
    registry.discover_plugins(plugin_dir)
    builtin_dir = Path(__file__).parent / "plugins" / "builtin"
    registry.discover_plugins(builtin_dir)

# At module level
load_plugins()
```

### Use Plugins in Export
```python
def export_content(content_dict: dict, path: Path, fmt: str):
    """Export content with plugin support."""
    # Try plugin first
    export_plugins = registry.list_plugins(ExportPlugin)
    for plugin in export_plugins:
        if plugin.format_extension == fmt:
            plugin.export(content_dict, path)
            return

    # Fallback to builtin formats
    # ... existing code ...
```

## Plugin Configuration

### Plugin Config File
```yaml
# plugins/config.yml
plugins:
  docx_export:
    enabled: true
    settings:
      font_size: 12
      include_toc: true

  notion_export:
    enabled: true
    settings:
      api_key: ${NOTION_API_KEY}
      database_id: "abc123"
```

## Documentation for Plugin Developers

### Create Plugin Developer Guide
```markdown
# Plugin Development Guide

## Creating Your First Plugin

1. Create a new file in `plugins/user/my_plugin.py`
2. Import base class: `from plugins.base import ExportPlugin`
3. Implement required methods
4. Restart app to load plugin

## Example: Custom Export Format

[Include complete example]

## Testing Your Plugin

[Testing guidelines]

## Publishing Plugins

[Optional: plugin marketplace/registry]
```

## Your Process
1. Design plugin architecture based on requirements
2. Implement base plugin system (base classes, registry)
3. Create example builtin plugins
4. Integrate plugin loading into app
5. Test plugin discovery and execution
6. Create developer documentation
7. Create example user plugins
8. Handle errors gracefully (plugin failures shouldn't crash app)

## Benefits
- Users can extend functionality without touching core code
- Community can contribute plugins
- Easier to experiment with new features
- Modular, maintainable architecture
- Clear separation of concerns
