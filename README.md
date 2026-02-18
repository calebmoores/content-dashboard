# Content Dashboard

A clean, lightweight content dashboard for reading and managing markdown articles with Mermaid diagram support.

## Features

- 📖 **Clean Reading Interface** - Medium-style article reading experience
- 📊 **Mermaid Diagrams** - Renders flowcharts, charts, and diagrams from ```mermaid blocks
- 🌙 **Dark Mode** - Toggle between light and dark themes
- 📋 **Copy to Clipboard** - Easy copying of raw markdown content
- 📱 **Mobile Responsive** - Works great on all device sizes
- ⚡ **Live Server** - Python server with API endpoints for article management

## Quick Start

```bash
# Clone the repository
git clone https://github.com/calebmoores/content-dashboard.git
cd content-dashboard

# Run the server
python3 server.py

# Open your browser
open http://localhost:3003
```

## Server Configuration

- **Port**: 3003 (configurable in server.py)
- **Drafts Directory**: `../drafts/` (configurable)
- **API Endpoints**:
  - `GET /api/articles` - List all articles
  - `GET /api/articles/:id` - Get specific article content

## Article Format

Place your markdown files in the `drafts/` directory. Supports:

- Standard markdown formatting
- Mermaid diagrams in ```mermaid code blocks
- Word count and reading time calculation
- Article metadata and status tracking

## Mermaid Support

Create diagrams directly in your markdown:

\`\`\`mermaid
graph LR
    A[Start] --> B[Process]
    B --> C[End]
\`\`\`

Supports flowcharts, sequence diagrams, gantt charts, and more.

## Tech Stack

- **Frontend**: Vanilla HTML/CSS/JavaScript
- **Backend**: Python HTTP server
- **Diagrams**: Mermaid.js
- **Styling**: Custom CSS with dark mode support

## License

MIT License