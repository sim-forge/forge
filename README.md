# SimForge

A local-first, production-grade synthetic cognition tool for generating, editing, and visualizing structured data.

## Overview

SimForge enables users to generate, edit, and visualize structured data — such as belief-action sequences — using a smart table interface powered by LLMs. It supports visualized forking, batch generation, and modular prompt authoring.

## Key Features

- **Smart Table Interface**: Edit and manipulate structured data with an intuitive UI
- **Batch Generation**: Generate multiple sequences in parallel
- **Visualized Forking**: Create and visualize alternative paths and decision trees
- **Modular Prompt Authoring**: Create, edit, and reuse prompt templates
- **Local-First Architecture**: Run everything locally with optional cloud sync

## Technology Stack

### Backend
- **Python 3.10+**
- **FastAPI**: High-performance API framework
- **Pydantic**: Data validation and settings management
- **SQLite/SQLAlchemy**: Local data persistence
- **LLM Integrations**: Support for multiple LLM providers

### Frontend
- **Tauri**: Lightweight, secure desktop application framework
- **SvelteKit**: Efficient, component-based UI framework
- **TypeScript**: Type-safe JavaScript
- **Framer Motion**: Smooth, cinematic transitions and animations

## Project Structure

```
SimForge/
├── backend/                # Python FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Core business logic
│   │   │   ├── engine/     # Generation, validation, history
│   │   │   ├── prompts/    # Prompt management
│   │   │   ├── schema/     # Data models
│   │   │   └── utils/      # Utilities
│   │   └── services/       # External services
│   │       ├── llm/        # LLM providers
│   │       ├── memory/     # Storage solutions
│   │       └── visualization/ # Visualization tools
│   └── tests/              # Backend tests
├── frontend/               # Tauri + SvelteKit frontend
│   ├── src/
│   │   ├── app/
│   │   │   ├── components/ # UI components
│   │   │   │   ├── layout/ # Layout components
│   │   │   │   ├── table/  # Table components
│   │   │   │   ├── chat/   # Chat interface
│   │   │   │   ├── context/ # Context panels
│   │   │   │   ├── prompt/ # Prompt editing
│   │   │   │   ├── ribbon/ # Action ribbons
│   │   │   │   └── graph/  # Visualization components
│   │   │   ├── pages/      # Page components
│   │   │   ├── stores/     # Svelte stores
│   │   │   ├── styles/     # Global styles
│   │   │   └── utils/      # Frontend utilities
│   │   └── lib/            # Shared libraries
│   └── public/             # Static assets
├── data/                   # Data storage
│   ├── output/             # Generated outputs
│   ├── schemas/            # Schema definitions
│   └── templates/          # Prompt templates
├── configs/                # Configuration files
│   └── env/                # Environment configs
├── .github/                # GitHub configurations
│   └── workflows/          # CI/CD workflows
└── logs/                   # Application logs
```

## PRISM CODES Design System

SimForge follows the PRISM CODES design system:

- **Performance**: Optimized for speed and responsiveness
- **Resilience**: Robust error handling and recovery
- **Interoperability**: Compatible with various data formats and systems
- **Scalability**: Designed to handle growing data and user needs
- **Modularity**: Component-based architecture for flexibility
- **Creativity**: Enabling creative exploration of possibilities
- **Optimization**: Efficient resource utilization
- **Design**: Intuitive, beautiful user experience
- **Ethics & Security**: Responsible AI use and data protection
- **Sustainability**: Long-term maintainability and evolution

## Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- Rust (for Tauri)

### Installation

1. Clone the repository
2. Set up the backend:
   ```bash
   cd SimForge/backend
   pip install -r requirements.txt
   ```
3. Set up the frontend:
   ```bash
   cd SimForge/frontend
   npm install
   ```

### Running the Application

1. Start the backend:
   ```bash
   cd SimForge/backend
   python main.py
   ```
2. Start the frontend:
   ```bash
   cd SimForge/frontend
   npm run tauri dev
   ```

## License

[MIT License](LICENSE)