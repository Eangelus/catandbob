# Deep Dive: Tool-Plugin-System

Bob soll Tools ausführen können — sowohl fest eingebaute als auch später
hinzugefügte — ohne dass der Rest der Plattform wissen muss, wie ein einzelnes
Tool intern funktioniert. Dafür ein einheitliches Interface statt Sonderfällen
pro Tool:

```python
# Auszug aus runtime/tool_system.py

@dataclass
class ToolResult:
    """Ergebnis der Tool-Ausführung."""
    success: bool
    data: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    duration_ms: float = 0.0
    tool_name: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class BaseTool(ABC):
    """
    Abstrakte Basisklasse für alle Tools.

    Jedes Tool muss diese Klasse implementieren und
    die abstrakten Methoden definieren.
    """

    def __init__(self, name: str = "", description: str = "", version: str = "1.0.0"):
        caps = self._get_capabilities() if name and hasattr(self, "_get_capabilities") else []
        self.metadata: Optional[ToolMetadata] = ToolMetadata(
            name=name, version=version, description=description,
            author="Cat & Bob", capabilities=caps,
        ) if name else None
        self.inputs: Dict[str, ToolInput] = {}
        self.outputs: Dict[str, ToolOutput] = {}

    @abstractmethod
    def validate_inputs(self, **kwargs) -> tuple[bool, Optional[str]]:
        """Validiere Input-Parameter vor der Ausführung."""
        raise NotImplementedError

    @abstractmethod
    def execute(self, **kwargs) -> ToolResult:
        """Führe das Tool aus."""
        raise NotImplementedError
```

Jedes Tool deklariert seine Capabilities (statt Typ-Checks im Aufrufer) und muss
`validate_inputs()` implementieren, bevor `execute()` überhaupt erreichbar ist —
Validierung ist damit kein optionaler Zusatzschritt, sondern Teil des Interfaces.

Die Registry macht Tools über ihre Capability statt über ihren Namen auffindbar
und ist bewusst thread-safe, weil mehrere Anfragen parallel dieselbe Registry
nutzen:

```python
# Auszug aus runtime/tool_system.py

class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}
        self._lock = threading.Lock()

    def register(self, tool: BaseTool) -> None:
        with self._lock:
            self._tools[tool.metadata.name] = tool

    def find_by_capability(self, capability: str) -> List[BaseTool]:
        with self._lock:
            return [
                tool for tool in self._tools.values()
                if capability in tool.metadata.capabilities
            ]
```

**Warum das zählt:** Die eigentliche Sicherheitslogik (Sandbox-Validierung,
Prompt-Injection-Erkennung, Daten-Sanitizing, Audit-Logging) sitzt bewusst
*außerhalb* dieser Klassen als eigene, austauschbare Komponenten, die vor bzw.
nach `execute()` greifen — `BaseTool` selbst kennt sie nicht. Neue Tools erben
diese Absicherung automatisch, ohne sie kennen oder reimplementieren zu müssen.

---

*Teil der [Cat & Bob](README.md) Projektübersicht — der vollständige
Sicherheits-/Sandbox-Code ist bewusst nicht Teil dieses Repos.*
