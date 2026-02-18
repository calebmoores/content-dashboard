# Article Writing Haven

A comprehensive article writing platform with editing, scheduling, and publishing workflow management.

![Dashboard Preview](preview.png)

## 🚀 Features

### 1. Full Editing Capabilities
- **Inline editing** - Click any paragraph to edit directly
- **Live markdown preview** - See changes instantly
- **Auto-save** - Content saves on blur
- **Split view** - Edit and preview side by side
- **Dark/Light theme** - Toggle between modes

### 2. Source Management
- **Add sources** - URL + notes per article
- **Inline citations** - Insert citations from sources
- **Source verification** - Click links to verify
- **Research notes** - Keep track of sources

### 3. AI Editing Features
- **Improve selected text** - Enhance clarity and flow
- **Rewrite with tone** - Professional, casual, persuasive
- **Expand sections** - Add more detail
- **Condense content** - Make concise
- **Generate headlines** - Alternative titles
- **Grammar check** - Fix errors

> ⚠️ **Note**: AI features require API configuration. Currently shows placeholders.

### 4. Diagram Editing
- **Mermaid diagrams** - Render directly in editor
- **Live preview** - See diagrams as you type
- **Diagram templates** - Flowcharts, timelines, mindmaps

### 5. Writing Tools
- **Word count tracking** - Real-time updates
- **Word goal progress** - Set targets per article
- **Stats panel** - Words, characters, sentences
- **Export** - Markdown and HTML formats

### 6. Research Integration
- **Web search** - Search within editor
- **Save snippets** - Capture research findings
- **Quote formatting** - Easy citation insertion

### 7. Release Schedule & Publishing Pipeline

#### Calendar View
- **Monthly calendar** - Visual schedule overview
- **Drag-and-drop** - Schedule articles by dragging
- **Publish dates** - Set target dates per article
- **Today highlighting** - Current date highlighted

#### Pipeline View
- **Four stages**: Draft → Review → Scheduled → Published
- **Drag-and-drop** - Move articles between stages
- **Count badges** - See article count per stage
- **Status badges** - Quick visual status

#### Scheduling
- **Target publish dates** - Set exact date/time
- **Reminders** - 1 day or 1 week before alerts
- **Status transitions** - Auto-update on scheduling

### 8. Analytics Dashboard
- **Total articles** - All-time count
- **Published count** - Completed articles
- **Scheduled count** - Upcoming publications
- **Words written** - Total word count

## 🎯 Quick Start

```bash
cd /home/caleb/.openclaw/workspace/content-dashboard
python3 server.py
```

Open **http://localhost:3003**

## 📁 File Structure

```
content-dashboard/
├── index.html        # Complete SPA with all features
├── server.py         # Python HTTP server with REST API
└── README.md         # This file
```

**Drafts location**: `/home/caleb/.openclaw/workspace/drafts/`

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/articles` | GET | List all articles |
| `/api/articles` | POST | Create new article |
| `/api/articles/:id` | GET | Get full article |
| `/api/articles/:id/update` | POST | Update article |
| `/api/articles/:id/status` | POST | Update status |
| `/api/articles/:id/schedule` | POST | Schedule publish date |
| `/api/ai` | POST | AI suggestions |
| `/api/search` | POST | Web search |

### Request/Response Examples

**Create Article:**
```json
POST /api/articles
{"id": "my-article", "title": "My Article", "content": "# My Article\n\n..."}
```

**Update Status:**
```json
POST /api/articles/:id/status
{"status": "scheduled", "publishDate": "2026-03-01T09:00"}
```

## ⌨️ Keyboard Shortcuts

| Key | Action |
|-----|--------|
| Ctrl+S | Save |
| Ctrl+Shift+P | Preview mode |
| Ctrl+Shift+S | Split view |

## 🎨 UI Layout

```
┌─────────────────┬────────────────────┬────────────────────┐
│  NAV            │  Articles List     │  Editor            │
│  ─────────────  │  ────────────────  │  ───────────────   │
│  ✍️ Editor      │  Search            │  [Title]           │
│  📅 Calendar    │  [+] New           │  [Content...]      │
│  🔄 Pipeline    │  ──────────────    │                    │
│  📊 Analytics  │  • Article 1       │  Preview Panel     │
│                │  • Article 2       │  (Split/Preview)   │
│                │  • Article 3       │                    │
├─────────────────┴────────────────────┴────────────────────┤
│  Sources │ AI Tools │ Schedule │ Stats                    │
└───────────────────────────────────────────────────────────┘
```

## ⚙️ Configuration

Edit `server.py` to customize:
- `DRAFTS_DIR` - Change drafts location
- `PORT` - Change server port

## 🔒 Status Workflow

```
Draft → Review → Scheduled → Published
  ↓        ↓         ↓           ↓
[WIP]   [Needs    [Ready]    [Live]
        review]   to publish]
```

## 📅 Calendar Features

- View scheduled articles on calendar
- Drag articles to different dates
- Click date to see scheduled items
- Visual status indicators (color-coded)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Submit pull request

## 📝 License

MIT - Build cool stuff!

---

Built with ❤️ for writers who want to create, schedule, and publish amazing content.