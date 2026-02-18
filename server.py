#!/usr/bin/env python3
"""
Article Writing Haven Server
A comprehensive HTTP server that provides API endpoints for the article writing platform.
Supports editing, source management, scheduling, and more.
"""

import http.server
import json
import os
import re
import urllib.parse
from pathlib import Path
from datetime import datetime
import threading

# Configuration
DRAFTS_DIR = Path("/home/caleb/.openclaw/workspace/drafts")
PORT = 3003

# In-memory storage for article metadata
article_metadata = {}
article_content_cache = {}

# Lock for thread-safe operations
cache_lock = threading.Lock()


def extract_title(content):
    """Extract the title from markdown content (first H1)."""
    match = re.search(r'^# (.+)$', content, re.MULTILINE)
    return match.group(1).strip() if match else "Untitled"


def count_words(content):
    """Count words in content."""
    return len(content.split())


def load_article_metadata(article_id):
    """Load article metadata from cache or defaults."""
    with cache_lock:
        if article_id not in article_metadata:
            article_metadata[article_id] = {
                "status": "draft",
                "publishDate": None,
                "sources": [],
                "wordGoal": 1000
            }
        return article_metadata[article_id].copy()


def save_article_metadata(article_id, metadata):
    """Save article metadata."""
    with cache_lock:
        article_metadata[article_id] = metadata


def get_article_info(filepath):
    """Get information about an article."""
    if filepath.exists():
        content = filepath.read_text(encoding='utf-8')
    else:
        content = ""

    filename = filepath.name
    article_id = filename.replace('.md', '')
    metadata = load_article_metadata(article_id)

    return {
        "id": article_id,
        "filename": filename,
        "title": extract_title(content) if content else "Untitled",
        "wordCount": count_words(content) if content else 0,
        "status": metadata.get("status", "draft"),
        "publishDate": metadata.get("publishDate"),
        "sources": metadata.get("sources", []),
        "wordGoal": metadata.get("wordGoal", 1000),
        "content": content
    }


def list_articles():
    """List all articles in the drafts directory."""
    if not DRAFTS_DIR.exists():
        return []

    articles = []
    for filepath in sorted(DRAFTS_DIR.glob("*.md")):
        try:
            info = get_article_info(filepath)
            articles.append({
                "id": info["id"],
                "filename": info["filename"],
                "title": info["title"],
                "wordCount": info["wordCount"],
                "status": info["status"],
                "publishDate": info["publishDate"],
                "wordGoal": info["wordGoal"]
            })
        except Exception as e:
            print(f"Error reading {filepath}: {e}")

    return articles


def get_article(article_id):
    """Get a specific article by ID."""
    filepath = DRAFTS_DIR / f"{article_id}.md"
    if not filepath.exists():
        return None
    return get_article_info(filepath)


def save_article(article_id, title, content, status=None, sources=None, publishDate=None, wordGoal=None):
    """Save an article to disk and update metadata."""
    filepath = DRAFTS_DIR / f"{article_id}.md"

    # Ensure drafts directory exists
    DRAFTS_DIR.mkdir(parents=True, exist_ok=True)

    # Update content if provided
    if content is not None:
        # Update title in content if provided
        if title:
            # Remove existing H1 and add new one
            lines = content.split('\n')
            new_lines = []
            for line in lines:
                if not line.startswith('# '):
                    new_lines.append(line)
            content = f"# {title}\n\n" + '\n'.join(new_lines)

        filepath.write_text(content, encoding='utf-8')

    # Update metadata
    metadata = load_article_metadata(article_id)
    if status is not None:
        metadata["status"] = status
    if sources is not None:
        metadata["sources"] = sources
    if publishDate is not None:
        metadata["publishDate"] = publishDate
    if wordGoal is not None:
        metadata["wordGoal"] = wordGoal
    save_article_metadata(article_id, metadata)

    return get_article_info(filepath)


class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP request handler for the content dashboard."""

    def log_message(self, format, *args):
        """Suppress default logging for cleaner output."""
        pass

    def send_json_response(self, data, status=200):
        """Send a JSON response."""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def send_error_response(self, message, status=404):
        """Send an error response."""
        self.send_json_response({"error": message}, status)

    def do_OPTIONS(self):
        """Handle CORS preflight requests."""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        """Handle GET requests."""
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        query = urllib.parse.parse_qs(parsed_path.query)

        # API endpoints
        if path == '/api/articles':
            articles = list_articles()
            self.send_json_response(articles)
            return

        if path.startswith('/api/articles/'):
            parts = path.split('/')
            if len(parts) == 4:
                article_id = parts[3]
                article = get_article(article_id)
                if article:
                    self.send_json_response(article)
                else:
                    self.send_error_response("Article not found", 404)
                return

            if len(parts) == 5 and parts[3] == 'status':
                # Get article status
                article_id = parts[4]
                metadata = load_article_metadata(article_id)
                self.send_json_response({"status": metadata.get("status", "draft")})
                return

        # Health check
        if path == '/api/health':
            self.send_json_response({"status": "ok", "port": PORT})
            return

        # Serve static files
        if path == '/' or path == '/index.html':
            self.serve_file('index.html', 'text/html')
        elif path.endswith('.css'):
            self.serve_file(path.lstrip('/'), 'text/css')
        elif path.endswith('.js'):
            self.serve_file(path.lstrip('/'), 'application/javascript')
        else:
            self.send_error_response("Not found", 404)

    def do_POST(self):
        """Handle POST requests."""
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path

        # Read request body
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else '{}'

        try:
            data = json.loads(body) if body else {}
        except json.JSONDecodeError:
            self.send_error_response("Invalid JSON", 400)
            return

        # Create article
        if path == '/api/articles':
            article_id = data.get('id')
            title = data.get('title', 'Untitled')
            content = data.get('content', f"# {title}\n\nStart writing...")

            if not article_id:
                self.send_error_response("Article ID required", 400)
                return

            article = save_article(article_id, title, content, status='draft')
            self.send_json_response({"success": True, "article": article}, 201)
            return

        # Update article
        if path.startswith('/api/articles/') and path.endswith('/update'):
            parts = path.split('/')
            if len(parts) == 5:
                article_id = parts[3]
                title = data.get('title')
                content = data.get('content')
                status = data.get('status')
                sources = data.get('sources')
                publishDate = data.get('publishDate')
                wordGoal = data.get('wordGoal')

                article = save_article(article_id, title, content, status, sources, publishDate, wordGoal)
                self.send_json_response({"success": True, "article": article})
                return

        # Update article status
        if path.startswith('/api/articles/') and path.endswith('/status'):
            parts = path.split('/')
            if len(parts) == 5:
                article_id = parts[3]
                new_status = data.get('status')
                publishDate = data.get('publishDate')

                valid_statuses = ['draft', 'review', 'scheduled', 'published']
                if new_status not in valid_statuses:
                    self.send_error_response("Invalid status", 400)
                    return

                metadata = load_article_metadata(article_id)
                metadata['status'] = new_status
                if publishDate:
                    metadata['publishDate'] = publishDate
                save_article_metadata(article_id, metadata)

                self.send_json_response({"success": True, "status": new_status, "publishDate": publishDate})
                return

        # Schedule article
        if path.startswith('/api/articles/') and path.endswith('/schedule'):
            parts = path.split('/')
            if len(parts) == 5:
                article_id = parts[3]
                publishDate = data.get('publishDate')

                metadata = load_article_metadata(article_id)
                metadata['publishDate'] = publishDate
                metadata['status'] = 'scheduled'
                save_article_metadata(article_id, metadata)

                self.send_json_response({"success": True, "publishDate": publishDate})
                return

        # AI endpoint (placeholder - would connect to OpenAI/Anthropic API)
        if path == '/api/ai':
            action = data.get('action')
            text = data.get('text', '')
            options = data.get('options', {})

            # This is a placeholder - actual implementation would call AI API
            suggestions = {
                'improve': f"Suggested improvement for: {text[:100]}...",
                'rewrite': f"Rewritten version with {options.get('tone', 'professional')} tone",
                'expand': f"Expanded content adding more detail and context...",
                'condense': f"Condensed version to make it more concise...",
                'grammar': f"Grammar fixes applied to: {text[:100]}...",
                'headlines': [
                    f"Alternative headline 1 for: {text[:30]}...",
                    f"Alternative headline 2 for: {text[:30]}...",
                    f"Alternative headline 3 for: {text[:30]}..."
                ]
            }

            suggestion = suggestions.get(action, "No suggestion available")
            self.send_json_response({"suggestion": suggestion, "action": action})
            return

        # Search endpoint (placeholder)
        if path == '/api/search':
            query = data.get('query', '')
            # This would connect to a search API
            self.send_json_response({"results": [], "query": query})
            return

        # Bulk schedule endpoint
        if path == '/api/bulk-schedule':
            articles = data.get('articles', [])
            startDate = data.get('startDate')
            intervalDays = data.get('intervalDays', 1)

            if not articles or not startDate:
                self.send_error_response("Articles and start date required", 400)
                return

            results = []
            currentDate = datetime.fromisoformat(startDate)

            for article_id in articles:
                publishDate = currentDate.isoformat()[:16]
                metadata = load_article_metadata(article_id)
                metadata['status'] = 'scheduled'
                metadata['publishDate'] = publishDate
                save_article_metadata(article_id, metadata)
                results.append({"id": article_id, "publishDate": publishDate})
                currentDate = currentDate.replace(day=currentDate.day + intervalDays)

            self.send_json_response({"success": True, "scheduled": results})
            return

        # Milestones endpoint
        if path == '/api/milestones':
            method = self.command
            if method == 'GET':
                milestones = []
                # Would load from storage
                self.send_json_response({"milestones": milestones})
            elif method == 'POST':
                milestone = data
                # Would save to storage
                self.send_json_response({"success": True, "milestone": milestone})
            return

        # Notifications endpoint
        if path == '/api/notifications':
            articles = list_articles()
            now = datetime.now()
            notifications = []

            for article in articles:
                if article.get('publishDate'):
                    publishDate = datetime.fromisoformat(article['publishDate'])
                    daysUntil = (publishDate - now).days

                    if daysUntil == 1:
                        notifications.append({
                            "type": "reminder",
                            "title": "Publishing Tomorrow",
                            "article": article['title'],
                            "date": article['publishDate']
                        })
                    elif daysUntil == 7:
                        notifications.append({
                            "type": "reminder",
                            "title": "Publishing in 1 Week",
                            "article": article['title'],
                            "date": article['publishDate']
                        })

            self.send_json_response({"notifications": notifications})
            return

        self.send_error_response("Not found", 404)

    def do_PUT(self):
        """Handle PUT requests."""
        self.do_POST()

    def do_DELETE(self):
        """Handle DELETE requests."""
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path

        if path.startswith('/api/articles/'):
            parts = path.split('/')
            if len(parts) == 4:
                article_id = parts[3]
                filepath = DRAFTS_DIR / f"{article_id}.md"

                if filepath.exists():
                    filepath.unlink()
                    with cache_lock:
                        article_metadata.pop(article_id, None)
                    self.send_json_response({"success": True, "message": "Article deleted"})
                else:
                    self.send_error_response("Article not found", 404)
                return

        self.send_error_response("Not found", 404)

    def serve_file(self, filepath, content_type):
        """Serve a file from the current directory."""
        try:
            with open(filepath, 'rb') as f:
                content = f.read()

            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_error_response("File not found", 404)


def run_server():
    """Run the HTTP server."""
    server_address = ('', PORT)
    httpd = http.server.HTTPServer(server_address, DashboardHandler)

    print(f"🚀 Article Writing Haven running at http://localhost:{PORT}")
    print(f"📁 Serving drafts from: {DRAFTS_DIR}")
    print("\nFeatures:")
    print("  • Full editing capabilities with live preview")
    print("  • Source management per article")
    print("  • AI tools (placeholder - configure API)")
    print("  • Calendar view with drag-and-drop scheduling")
    print("  • Publishing pipeline (Draft → Review → Scheduled → Published)")
    print("  • Analytics dashboard")
    print("\nPress Ctrl+C to stop")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped")
        httpd.shutdown()


if __name__ == '__main__':
    run_server()