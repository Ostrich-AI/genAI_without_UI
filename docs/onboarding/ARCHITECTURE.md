# Component architecture

```mermaid
flowchart TD
  I[Synthetic inputs] --> A[Python inference workload]
  A --> M[Local model service]
  M --> A
  A --> O[UI or output files]
```

Conceptual source-oriented view, not a verified deployment diagram. Consult the README code map and configuration catalogue for concrete entrypoints. Provider connections depend on the selected feature and environment.
