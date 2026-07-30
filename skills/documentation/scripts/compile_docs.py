# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import re
import sys
import json
import argparse
import html
import shutil
from datetime import datetime

# ==============================================================================
# 4 Stitch Design Systems CSS Configurations (Spacious, Airy, and Visual-First)
# ==============================================================================

THEME_CSS = {
    "technical": """
        /* TECHNICAL DOCUMENTATION THEME (LIGHT DEVPUB PORTAL) */
        :root {
            --bg-canvas: #f6f5fa;
            --bg-surface: #ffffff;
            --bg-surface-alt: #f0edf6;
            --text-primary: #121217;
            --text-secondary: #3e3f48;
            --color-primary: #0a1172;
            --color-secondary: #455a64;
            --color-accent: #0077b6;
            --color-accent-glow: rgba(0, 119, 182, 0.12);
            --border-color: #d1cde0;
            --font-heading: 'Outfit', sans-serif;
            --font-body: 'Inter', sans-serif;
            --font-mono: 'JetBrains Mono', monospace;
            --rounding: 12px;
            --shadow-sm: 0 2px 4px rgba(0,0,0,0.03);
            --shadow-md: 0 10px 30px rgba(10, 17, 114, 0.06);
            --shadow-lg: 0 20px 40px rgba(0,0,0,0.08);
        }
        body {
            background-color: var(--bg-canvas);
            color: var(--text-primary);
            font-family: var(--font-body);
        }
        .main-container {
            display: grid;
            grid-template-columns: 320px minmax(0, 1fr) 280px;
            gap: 40px;
            max-width: 1560px;
            margin: 0 auto;
            padding: 48px 40px;
        }
        @media(max-width: 1200px) {
            .main-container { grid-template-columns: 280px minmax(0, 1fr); }
            .toc-bar { display: none; }
        }
        @media(max-width: 900px) {
            .main-container { grid-template-columns: 1fr; padding: 24px 16px; }
            .sidebar { position: relative; top: 0; height: auto; border-right: none; padding-right: 0; margin-bottom: 24px; }
        }
        .sidebar {
            position: sticky;
            top: 120px;
            height: calc(100vh - 160px);
            overflow-y: auto;
            border-right: 1px solid var(--border-color);
            padding-right: 32px;
        }
        .toc-bar {
            position: sticky;
            top: 120px;
            height: calc(100vh - 160px);
            overflow-y: auto;
            border-left: 1px solid var(--border-color);
            padding-left: 32px;
        }
        .prose-content {
            max-width: 85ch;
            margin: 0 auto;
            line-height: 1.75;
            font-size: 16px;
        }
        .glass-panel {
            background: var(--bg-surface);
            border: 1px solid var(--border-color);
            border-radius: var(--rounding);
            box-shadow: var(--shadow-md);
            padding: 48px;
            margin-bottom: 40px;
            will-change: transform;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .glass-panel:hover {
            box-shadow: var(--shadow-lg);
            transform: translateY(-2px);
        }
    """,
    "obsidian": """
        /* LUMINOUS OBSIDIAN THEME (DARK PRESENTATION KEYNOTE) */
        :root {
            --bg-canvas: #070512;
            --bg-surface: rgba(13, 11, 28, 0.7);
            --bg-surface-alt: #121021;
            --text-primary: #ffffff;
            --text-secondary: #a3a1bc;
            --color-primary: #00f0ff;
            --color-secondary: #ff007f;
            --color-accent: #39ff14;
            --color-accent-glow: rgba(0, 240, 255, 0.2);
            --border-color: rgba(255, 255, 255, 0.08);
            --font-heading: 'Outfit', sans-serif;
            --font-body: 'Inter', sans-serif;
            --font-mono: 'JetBrains Mono', monospace;
            --rounding: 28px;
            --shadow-sm: 0 4px 12px rgba(0,0,0,0.6);
            --shadow-md: 0 16px 48px rgba(0,0,0,0.7);
            --shadow-lg: 0 0 40px rgba(0, 240, 255, 0.15);
        }
        body {
            background: radial-gradient(circle at 50% 0%, #160e34 0%, var(--bg-canvas) 80%);
            color: var(--text-primary);
            font-family: var(--font-body);
        }
        .main-container {
            display: grid;
            grid-template-columns: 320px minmax(0, 1fr);
            gap: 48px;
            max-width: 1560px;
            margin: 0 auto;
            padding: 64px 48px;
        }
        @media(max-width: 1024px) {
            .main-container { grid-template-columns: 1fr; }
        }
        .sidebar {
            position: sticky;
            top: 120px;
            height: calc(100vh - 180px);
            overflow-y: auto;
            background: var(--bg-surface);
            backdrop-filter: blur(32px);
            border: 1px solid var(--border-color);
            border-radius: var(--rounding);
            padding: 32px;
        }
        .prose-content {
            max-width: 90ch;
            line-height: 1.8;
            font-size: 16px;
        }
        .glass-panel {
            background: var(--bg-surface);
            backdrop-filter: blur(32px);
            border: 1px solid var(--border-color);
            border-radius: var(--rounding);
            box-shadow: var(--shadow-md);
            padding: 56px;
            margin-bottom: 48px;
            transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        }
        .glass-panel:hover {
            border-color: rgba(0, 240, 255, 0.3);
            box-shadow: var(--shadow-lg);
            transform: translateY(-4px);
        }
    """,
    "proscript": """
        /* PROSCRIPT SYSTEM THEME (LIGHT ENTERPRISE CHECKLIST) */
        :root {
            --bg-canvas: #f8f9fc;
            --bg-surface: #ffffff;
            --bg-surface-alt: #f1f3f8;
            --text-primary: #121416;
            --text-secondary: #4a4d52;
            --color-primary: #0f1c3f;
            --color-secondary: #1d2a5a;
            --color-accent: #2e438a;
            --color-accent-glow: rgba(46, 67, 138, 0.08);
            --border-color: #dbe0ea;
            --font-heading: 'Outfit', sans-serif;
            --font-body: 'Inter', sans-serif;
            --font-mono: 'Inter', sans-serif;
            --rounding: 8px;
            --shadow-sm: 0 2px 4px rgba(0,0,0,0.03);
            --shadow-md: 0 8px 16px rgba(15, 28, 63, 0.03);
            --shadow-lg: 0 16px 32px rgba(0, 0, 0, 0.05);
        }
        body {
            background-color: var(--bg-canvas);
            color: var(--text-primary);
            font-family: var(--font-body);
        }
        .main-container {
            max-width: 1280px;
            margin: 0 auto;
            padding: 64px 32px;
        }
        .sidebar {
            margin-bottom: 40px;
            padding-bottom: 24px;
            border-bottom: 1px solid var(--border-color);
        }
        .prose-content {
            max-width: 100%;
            line-height: 1.7;
            font-size: 16px;
        }
        .glass-panel {
            background: var(--bg-surface);
            border: 1px solid var(--border-color);
            border-radius: var(--rounding);
            box-shadow: var(--shadow-md);
            padding: 48px;
            margin-bottom: 40px;
        }
    """,
    "dynamics": """
        /* DELHI TRAFFIC DYNAMICS THEME (DARK HIGH-DENSITY ANALYTICAL) */
        :root {
            --bg-canvas: #0f0f10;
            --bg-surface: #18181a;
            --bg-surface-alt: #141416;
            --text-primary: #e6e6ea;
            --text-secondary: #b8b8c2;
            --color-primary: #f0f0f5;
            --color-secondary: #4d4e57;
            --color-accent: #2aff2d;
            --color-accent-glow: rgba(42, 255, 45, 0.15);
            --border-color: #2c2c30;
            --font-heading: 'Outfit', sans-serif;
            --font-body: 'Inter', sans-serif;
            --font-mono: 'JetBrains Mono', monospace;
            --rounding: 6px;
            --shadow-sm: 0 2px 4px rgba(0,0,0,0.4);
            --shadow-md: 0 8px 24px rgba(0,0,0,0.5);
            --shadow-lg: 0 0 24px rgba(42, 255, 45, 0.1);
        }
        body {
            background-color: var(--bg-canvas);
            color: var(--text-primary);
            font-family: var(--font-body);
        }
        .main-container {
            display: grid;
            grid-template-columns: 280px minmax(0, 1fr);
            gap: 32px;
            max-width: 1640px;
            margin: 0 auto;
            padding: 40px 24px;
        }
        .sidebar {
            position: sticky;
            top: 120px;
            height: calc(100vh - 160px);
            overflow-y: auto;
            background: var(--bg-surface);
            border: 1px solid var(--border-color);
            border-radius: var(--rounding);
            padding: 24px;
        }
        .prose-content {
            max-width: 100%;
            line-height: 1.6;
            font-size: 15px;
        }
        .glass-panel {
            background: var(--bg-surface);
            border: 1px solid var(--border-color);
            border-radius: var(--rounding);
            box-shadow: var(--shadow-md);
            padding: 40px;
            margin-bottom: 24px;
        }
    """
}

# ==============================================================================
# Markdown & Container Parser Class
# ==============================================================================

class MarkdownParser:
    def __init__(self, theme_name):
        self.theme = theme_name
        self.headers = []

    def parse_frontmatter(self, md_text):
        frontmatter = {}
        content = md_text
        if md_text.startswith("---"):
            match = re.match(r"^---\s*\n(.*?)\n---\s*\n", md_text, re.DOTALL)
            if match:
                fm_raw = match.group(1)
                content = md_text[match.end():]
                for line in fm_raw.split("\n"):
                    if ":" in line:
                        k, v = line.split(":", 1)
                        frontmatter[k.strip().lower()] = v.strip().strip('"').strip("'")
        return frontmatter, content

    def parse(self, md_content):
        text = md_content

        # 1. Custom Outer Grid Containers :::: grid ... :::: (uses 4 colons)
        def parse_grid_containers(match):
            grid_content = match.group(1)
            # Recursively compile card tags inside the grid first
            grid_content = self.parse_cards(grid_content)
            return f'<div class="grid grid-cols-1 md:grid-cols-2 gap-8 my-10">{grid_content}</div>'
        
        text = re.compile(r"::::\s*grid\n(.*?)\n::::", re.DOTALL).sub(parse_grid_containers, text)

        # Apply card parsing on remaining individual cards (not wrapped in grids)
        text = self.parse_cards(text)

        # Extract fenced code blocks
        code_blocks = []
        def save_code_block(match):
            lang = match.group(1) or "txt"
            code_text = match.group(2)
            code_idx = len(code_blocks)
            code_blocks.append((lang, code_text))
            return f"<!--CODE_BLOCK_{code_idx}-->"
        text = re.compile(r"```+(\w*)\n(.*?)```+", re.DOTALL).sub(save_code_block, text)

        # Protect inline code
        inline_codes = []
        def save_inline_code(match):
            code_idx = len(inline_codes)
            inline_codes.append(match.group(1))
            return f"<!--INLINE_CODE_{code_idx}-->"
        text = re.compile(r"`([^`\n]+)`").sub(save_inline_code, text)

        # Parse GFM Alerts/Quotes
        lines = text.split("\n")
        parsed_lines = []
        in_quote = False
        quote_content = []
        quote_type = "STANDARD"

        def flush_quote():
            nonlocal in_quote, quote_content, quote_type
            if not in_quote:
                return ""
            content_block = "<br/>".join(quote_content)
            content_block = re.sub(r"^\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*", "", content_block, flags=re.IGNORECASE)
            
            icon = ""
            bg_class = ""
            if quote_type == "NOTE":
                icon = '<svg class="w-6 h-6 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"></svg>'
                bg_class = "admonition-note"
            elif quote_type == "TIP":
                icon = '<svg class="w-6 h-6 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .6 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6"/><path d="M10 22h4"></svg>'
                bg_class = "admonition-tip"
            elif quote_type == "IMPORTANT":
                icon = '<svg class="w-6 h-6 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"></svg>'
                bg_class = "admonition-important"
            elif quote_type == "WARNING":
                icon = '<svg class="w-6 h-6 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"></svg>'
                bg_class = "admonition-warning"
            elif quote_type == "CAUTION":
                icon = '<svg class="w-6 h-6 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><octagon points="7.86 2 16.14 2 22 7.86 22 16.14 16.14 22 7.86 22 2 16.14 2 7.86 7.86 2"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"></svg>'
                bg_class = "admonition-caution"
            else:
                icon = '<svg class="w-6 h-6 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></svg>'
                bg_class = "admonition-quote"

            in_quote = False
            quote_content = []
            return f'<div class="admonition {bg_class}">{icon}<div><strong>{quote_type}</strong><p>{content_block}</p></div></div>'

        for line in lines:
            if line.strip().startswith(">"):
                in_quote = True
                cleaned = line.strip().lstrip(">").strip()
                match_alert = re.match(r"^\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]", cleaned, re.IGNORECASE)
                if match_alert:
                    quote_type = match_alert.group(1).upper()
                quote_content.append(cleaned)
            else:
                if in_quote:
                    parsed_lines.append(flush_quote())
                parsed_lines.append(line)
        if in_quote:
            parsed_lines.append(flush_quote())

        text = "\n".join(parsed_lines)

        # Parse Headers (generating Table of Contents list)
        def parse_header(match):
            level = len(match.group(1))
            title = match.group(2).strip()
            h_id = re.sub(r"[^a-zA-Z0-9\-]+", "-", title.lower()).strip("-")
            self.headers.append({"level": level, "title": title, "id": h_id})
            return f'<h{level} id="{h_id}">{title}</h{level}>'
        text = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE).sub(parse_header, text)

        # Parse Badges [badge:color:label]
        def render_badge(match):
            color = match.group(1).lower()
            label = match.group(2)
            return f'<span class="badge badge-{color}">{label}</span>'
        text = re.compile(r"\[badge:(\w+):([^\]]+)\]").sub(render_badge, text)

        # Convert links
        def render_links(match):
            label = match.group(1)
            url = match.group(2)
            if "file:///" in url or url.endswith(".md"):
                filename = os.path.basename(url)
                base, _ = os.path.splitext(filename)
                return f'<a href="{base}.html" class="nav-link-item">{label}</a>'
            return f'<a href="{url}" target="_blank" rel="noopener noreferrer">{label}</a>'
        text = re.compile(r"\[([^\]]+)\]\(([^)]+)\)").sub(render_links, text)

        # Convert checklists, lists, and paragraphs
        html_lines = []
        in_list = False
        in_table = False
        table_rows = []

        def parse_inline_elements(ln):
            ln = re.compile(r"\*\*([^*]+)\*\*").sub(r"<strong>\1</strong>", ln)
            ln = re.compile(r"\*([^*]+)\*").sub(r"<em>\1</em>", ln)
            return ln

        lines = text.split("\n")
        for line in lines:
            stripped = line.strip()

            if "|" in line:
                if stripped.startswith("|") and stripped.endswith("|"):
                    if re.match(r"^\|[\s\-:|]+\|$", stripped):
                        continue
                    in_table = True
                    cells = [c.strip() for c in stripped.split("|")[1:-1]]
                    table_rows.append(cells)
                    continue
            else:
                if in_table:
                    in_table = False
                    html_lines.append('<div class="overflow-x-auto"><table class="rich-table">')
                    if table_rows:
                        html_lines.append('<thead><tr>')
                        for cell in table_rows[0]:
                            html_lines.append(f'<th>{parse_inline_elements(cell)}</th>')
                        html_lines.append('</tr></thead><tbody>')
                        for row in table_rows[1:]:
                            html_lines.append('<tr>')
                            for cell in row:
                                html_lines.append(f'<td>{parse_inline_elements(cell)}</td>')
                            html_lines.append('</tr>')
                    html_lines.append('</tbody></table></div>')
                    table_rows = []

            # Lists
            if stripped.startswith("- ") or stripped.startswith("* "):
                if not in_list:
                    in_list = True
                    html_lines.append('<ul class="list-disc">')
                item_content = stripped[2:]
                if item_content.startswith("[ ]"):
                    html_lines.append(f'<li class="checklist-item"><input type="checkbox" disabled /> <span>{parse_inline_elements(item_content[3:].strip())}</span></li>')
                elif item_content.startswith("[x]") or item_content.startswith("[/]") or item_content.startswith("[X]"):
                    html_lines.append(f'<li class="checklist-item"><input type="checkbox" checked disabled /> <span>{parse_inline_elements(item_content[3:].strip())}</span></li>')
                else:
                    html_lines.append(f'<li>{parse_inline_elements(item_content)}</li>')
                continue
            else:
                if in_list:
                    in_list = False
                    html_lines.append('</ul>')

            if not stripped:
                html_lines.append('<br/>')
                continue

            if stripped.startswith("<h") or stripped.startswith("<!--") or stripped.startswith("<div") or stripped.startswith("</div"):
                html_lines.append(line)
            else:
                html_lines.append(f'<p>{parse_inline_elements(line)}</p>')

        if in_table:
            html_lines.append('<table class="rich-table">')
            if table_rows:
                html_lines.append('<thead><tr>')
                for cell in table_rows[0]:
                    html_lines.append(f'<th>{parse_inline_elements(cell)}</th>')
                html_lines.append('</tr></thead><tbody>')
                for row in table_rows[1:]:
                    html_lines.append('<tr>')
                    for cell in row:
                        html_lines.append(f'<td>{parse_inline_elements(cell)}</td>')
                    html_lines.append('</tr>')
            html_lines.append('</tbody></table>')

        text = "\n".join(html_lines)

        # Restore Protected Inline Code
        for idx, ic in enumerate(inline_codes):
            escaped_code = html.escape(ic)
            text = text.replace(f"<!--INLINE_CODE_{idx}-->", f'<code class="inline-code">{escaped_code}</code>')

        # Restore Protected Fenced Code Blocks
        for idx, (lang, block) in enumerate(code_blocks):
            escaped_block = html.escape(block)
            code_html = f"""
            <div class="code-container">
                <div class="code-header">
                    <span>{lang.upper()}</span>
                    <button class="copy-btn" onclick="copyCode(this)">Copy</button>
                </div>
                <pre><code class="language-{lang}">{escaped_block}</code></pre>
            </div>
            """
            text = text.replace(f"<!--CODE_BLOCK_{idx}-->", code_html)

        return text

    def parse_cards(self, text_content):
        """
        Translates triple-colon ::: card blocks into elegant visual card containers.
        """
        def card_match_handler(match):
            title = match.group(1).strip()
            body = match.group(2)
            header = f'<h4 class="text-xl font-bold mb-4 text-white/95">{title}</h4>' if title else ""
            return f'<div class="glass-panel-card bg-white/5 border border-white/10 p-8 rounded-2xl hover:scale-[1.01] transition-all duration-300">{header}{body}</div>'
        
        return re.compile(r":::\s*card\s*([^\n]*)\n(.*?)\n:::", re.DOTALL).sub(card_match_handler, text_content)

# ==============================================================================
# HTML Assembly Helper (Beautiful, Airy, Dual-View and Premium)
# ==============================================================================

def assemble_html(title, desc, parsed_body, sidebar_nav, toc_html, theme, raw_markdown_src, live_reload=False):
    css_tokens = THEME_CSS.get(theme, THEME_CSS["technical"])
    escaped_markdown = html.escape(raw_markdown_src)
    
    live_reload_js = ""
    if live_reload:
        live_reload_js = """
        <script>
            let failCount = 0;
            function checkReload() {
                fetch('/live-reload')
                    .then(r => r.json())
                    .then(data => {
                        if (data.reload) {
                            window.location.reload();
                        } else {
                            setTimeout(checkReload, 1000);
                        }
                    })
                    .catch(err => {
                        failCount++;
                        if (failCount > 15) return;
                        setTimeout(checkReload, 2000);
                    });
            }
            setTimeout(checkReload, 1000);
        </script>
        """

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title if title else "Project Documentation"}</title>
    <meta name="description" content="{desc if desc else ""}">
    
    <!-- Premium Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;600;700;800&family=Inter:wght@400;500;600;700;900&family=Outfit:wght@400;500;600;700;900&display=swap" rel="stylesheet">
    
    <!-- Tailwind CSS Engine -->
    <script src="https://cdn.tailwindcss.com"></script>
    
    <style>
        {css_tokens}
        
        /* Premium Global Elements */
        body {{
            transition: all 0.3s ease;
            margin: 0;
            padding: 0;
        }}
        
        /* Modern Glass-Morph Header */
        .premium-header {{
            position: sticky;
            top: 0;
            z-index: 50;
            background: rgba(13, 11, 28, 0.45);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid var(--border-color);
            padding: 20px 48px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        /* Dual View Tabs */
        .tab-btn {{
            padding: 8px 24px;
            border-radius: 9999px;
            font-size: 0.9rem;
            font-weight: 600;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            color: var(--text-secondary);
        }}
        .tab-btn:hover {{
            color: var(--text-primary);
        }}
        .tab-btn.tab-active {{
            background: var(--color-accent-glow);
            color: var(--color-accent);
            box-shadow: 0 0 16px rgba(0, 240, 255, 0.1);
            border: 1px solid rgba(0, 240, 255, 0.2);
        }}
        
        /* Spacious Typography Overrides */
        .prose-content h1 {{
            font-family: var(--font-heading);
            font-size: 2.75rem;
            font-weight: 900;
            letter-spacing: -0.02em;
            margin-top: 0rem;
            margin-bottom: 1.5rem;
            line-height: 1.15;
            background: linear-gradient(135deg, var(--text-primary) 0%, var(--color-primary) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .prose-content h2 {{
            font-family: var(--font-heading);
            font-size: 1.85rem;
            font-weight: 700;
            margin-top: 3.5rem;
            margin-bottom: 1.25rem;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 0.75rem;
            color: var(--color-primary);
        }}
        .prose-content h3 {{
            font-family: var(--font-heading);
            font-size: 1.35rem;
            font-weight: 600;
            margin-top: 2.5rem;
            margin-bottom: 1rem;
            color: var(--color-primary);
        }}
        .prose-content p {{
            margin-bottom: 1.75rem;
            color: var(--text-secondary);
            font-size: 1.05rem;
            line-height: 1.8;
        }}
        
        /* Word Wrapping Table Rule (Global Guideline) */
        .rich-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 36px 0;
            font-size: 0.95rem;
            box-shadow: var(--shadow-sm);
            border-radius: var(--rounding);
            overflow: hidden;
        }}
        .rich-table th {{
            background-color: var(--bg-surface-alt);
            color: var(--text-primary);
            font-weight: 700;
            text-align: left;
            padding: 16px 20px;
            border-bottom: 2px solid var(--border-color);
        }}
        .rich-table td {{
            padding: 16px 20px;
            border-bottom: 1px solid var(--border-color);
            color: var(--text-secondary);
        }}
        .rich-table tr:hover {{
            background-color: rgba(255,255,255,0.01);
        }}
        .rich-table th:first-child, .rich-table td:first-child {{
            white-space: nowrap !important;
        }}
        .rich-table td:first-child code {{
            white-space: nowrap !important;
            word-break: normal !important;
        }}
        
        /* Code container */
        .code-container {{
            background-color: #0b0a13;
            border: 1px solid var(--border-color);
            border-radius: var(--rounding);
            margin: 36px 0;
            overflow: hidden;
            box-shadow: var(--shadow-md);
        }}
        .code-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 20px;
            background-color: #06050a;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            font-family: var(--font-mono);
            font-size: 0.8rem;
            color: #859397;
        }}
        .copy-btn {{
            background: transparent;
            border: 1px solid rgba(255,255,255,0.1);
            padding: 6px 14px;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .copy-btn:hover {{
            background-color: rgba(255,255,255,0.05);
            color: white;
        }}
        pre {{
            margin: 0;
            padding: 24px;
            overflow-x: auto;
        }}
        code {{
            font-family: var(--font-mono);
            font-size: 0.925rem;
        }}
        .inline-code {{
            background-color: var(--bg-surface-alt);
            padding: 4px 8px;
            border-radius: 6px;
            font-family: var(--font-mono);
            font-size: 0.85em;
            color: var(--color-accent);
        }}
        
        /* GFM alerts */
        .admonition {{
            display: flex;
            gap: 20px;
            padding: 24px;
            border-radius: var(--rounding);
            border-left: 5px solid;
            margin: 36px 0;
            box-shadow: var(--shadow-sm);
        }}
        .admonition-note {{
            border-left-color: #00d2ff;
            background-color: rgba(0, 210, 255, 0.04);
            color: var(--text-primary);
        }}
        .admonition-tip {{
            border-left-color: #39ff14;
            background-color: rgba(57, 255, 20, 0.04);
            color: var(--text-primary);
        }}
        .admonition-important {{
            border-left-color: #bd00ff;
            background-color: rgba(189, 0, 255, 0.04);
            color: var(--text-primary);
        }}
        .admonition-warning {{
            border-left-color: #ffaa00;
            background-color: rgba(255, 170, 0, 0.04);
            color: var(--text-primary);
        }}
        .admonition-caution {{
            border-left-color: #ff0055;
            background-color: rgba(255, 0, 85, 0.04);
            color: var(--text-primary);
        }}
        
        /* Sidebar layout links */
        .sidebar-link {{
            display: block;
            padding: 10px 16px;
            border-radius: var(--rounding);
            color: var(--text-secondary);
            font-size: 0.95rem;
            font-weight: 500;
            margin-bottom: 6px;
            transition: all 0.3s;
        }}
        .sidebar-link:hover {{
            background-color: var(--bg-surface-alt);
            color: var(--color-primary);
        }}
        .sidebar-link.active {{
            background-color: var(--color-accent-glow);
            color: var(--color-accent);
            font-weight: 600;
        }}
        
        /* Lists */
        .list-disc {{
            list-style-type: none;
            margin-left: 0;
            margin-bottom: 32px;
        }}
        .list-disc li {{
            position: relative;
            padding-left: 28px;
            margin-bottom: 12px;
            color: var(--text-secondary);
            font-size: 1.025rem;
        }}
        .list-disc li::before {{
            content: "•";
            color: var(--color-accent);
            font-weight: bold;
            font-size: 1.5rem;
            position: absolute;
            left: 8px;
            top: -4px;
        }}
        .checklist-item {{
            display: flex;
            align-items: center;
            gap: 12px;
            padding-left: 0 !important;
        }}
        .checklist-item::before {{
            display: none !important;
        }}
        .checklist-item input[type="checkbox"] {{
            accent-color: var(--color-accent);
            width: 18px;
            height: 18px;
        }}
        
        /* Badges */
        .badge {{
            display: inline-flex;
            align-items: center;
            padding: 4px 14px;
            font-size: 0.75rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            border-radius: 9999px;
            border: 1px solid;
            margin-right: 8px;
        }}
        .badge-indigo {{
            background-color: rgba(99, 102, 241, 0.1);
            border-color: rgba(99, 102, 241, 0.2);
            color: #6366f1;
        }}
        .badge-teal {{
            background-color: rgba(20, 184, 166, 0.1);
            border-color: rgba(20, 184, 166, 0.2);
            color: #14b8a6;
        }}
        .badge-green {{
            background-color: rgba(16, 185, 129, 0.1);
            border-color: rgba(16, 185, 129, 0.2);
            color: #10b981;
        }}
        .badge-red {{
            background-color: rgba(239, 68, 68, 0.1);
            border-color: rgba(239, 68, 68, 0.2);
            color: #ef4444;
        }}
        .badge-yellow {{
            background-color: rgba(245, 158, 11, 0.1);
            border-color: rgba(245, 158, 11, 0.2);
            color: #f59e0b;
        }}
    </style>
</head>
<body>

    <!-- Premium Nav Bar with Dual-View Switcher -->
    <header class="premium-header">
        <div class="flex items-center gap-4">
            <span class="w-3 h-3 rounded-full bg-cyan-400 animate-pulse"></span>
            <span class="text-xs font-semibold tracking-widest uppercase opacity-40 text-white/70">Document Portal</span>
        </div>
        <div class="flex gap-2 bg-white/5 border border-white/10 rounded-full p-1">
            <button id="btn-ui-view" onclick="showView('ui')" class="tab-btn tab-active">🖥️ UI View</button>
            <button id="btn-md-view" onclick="showView('md')" class="tab-btn">📄 Markdown Source</button>
        </div>
    </header>

    <!-- Base Layout Container -->
    <div class="main-container">
        
        <!-- Sidebar -->
        <aside class="sidebar flex flex-col space-y-4">
            <div class="pb-6 border-b border-white/5 mb-4">
                <h1 class="text-xl font-black text-white/90">{title if title else "Documentation"}</h1>
                <p class="text-xs text-white/40 mt-1">{desc if desc else ""}</p>
            </div>
            <nav class="flex-1 space-y-1">
                {sidebar_nav}
            </nav>
        </aside>

        <!-- Dynamic View Contents -->
        <main class="prose-content">
            
            <!-- Default UI Presentation View -->
            <div id="ui-view" class="transition-all duration-300">
                <!-- Spacious Hero Banner with SVG Background Art -->
                <div class="relative overflow-hidden bg-gradient-to-br from-violet-950/20 to-cyan-950/10 border border-white/5 rounded-3xl p-12 mb-12 shadow-2xl flex flex-col justify-between min-h-[220px]">
                    <div class="absolute inset-0 opacity-20 pointer-events-none">
                        <!-- Abstract Wave Art -->
                        <svg width="100%" height="100%" viewBox="0 0 1000 300" xmlns="http://www.w3.org/2000/svg">
                            <path d="M 0,150 Q 250,50 500,150 T 1000,150 L 1000,300 L 0,300 Z" fill="url(#wave-grad)"></path>
                            <defs>
                                <linearGradient id="wave-grad" x1="0%" y1="0%" x2="100%" y2="100%">
                                    <stop offset="0%" stop-color="#ff007f"></stop>
                                    <stop offset="100%" stop-color="#00f0ff"></stop>
                                </linearGradient>
                            </defs>
                        </svg>
                    </div>
                    <div class="relative z-10">
                        <span class="text-xs font-black tracking-widest text-cyan-400 uppercase">Interactive Suite</span>
                        <h2 class="text-4xl font-extrabold text-white mt-2 leading-tight">{title}</h2>
                        <p class="text-white/60 mt-3 text-base max-width-[65ch]">{desc}</p>
                    </div>
                </div>

                <!-- Page Content Prose -->
                <article class="glass-panel">
                    {parsed_body}
                </article>
            </div>

            <!-- Alternative Raw Markdown Code View -->
            <div id="markdown-view" class="hidden transition-all duration-300">
                <div class="glass-panel">
                    <div class="flex justify-between items-center pb-4 border-b border-white/5 mb-6">
                        <h2 class="text-2xl font-extrabold text-white/90 m-0 p-0">Raw Markdown Source</h2>
                        <button onclick="copyRawMarkdown(this)" class="copy-btn text-xs">Copy Source</button>
                    </div>
                    <pre class="bg-black/30 border border-white/5 rounded-xl p-6 overflow-x-auto"><code class="language-markdown text-white/80">{escaped_markdown}</code></pre>
                </div>
            </div>

        </main>

        <!-- Right Side TOC (only for 3-column layouts) -->
        {f'<aside class="toc-bar"><div class="sticky-toc"><span class="text-xs font-semibold tracking-widest uppercase opacity-40">On This Page</span><nav class="mt-6 space-y-2">{toc_html}</nav></div></aside>' if theme == "technical" else ""}

    </div>

    <!-- Client-side Tab Switcher and Helpers -->
    <script>
        function showView(view) {{
            const ui = document.getElementById('ui-view');
            const md = document.getElementById('markdown-view');
            const btnUi = document.getElementById('btn-ui-view');
            const btnMd = document.getElementById('btn-md-view');
            
            if (view === 'ui') {{
                ui.classList.remove('hidden');
                md.classList.add('hidden');
                btnUi.classList.add('tab-active');
                btnMd.classList.remove('tab-active');
            }} else {{
                ui.classList.add('hidden');
                md.classList.remove('hidden');
                btnUi.classList.remove('tab-active');
                btnMd.classList.add('tab-active');
            }}
        }}

        function copyCode(btn) {{
            const pre = btn.closest('.code-container').querySelector('code');
            navigator.clipboard.writeText(pre.innerText).then(() => {{
                btn.innerText = "Copied!";
                setTimeout(() => btn.innerText = "Copy", 1500);
            }});
        }}

        function copyRawMarkdown(btn) {{
            const code = document.querySelector('#markdown-view code');
            navigator.clipboard.writeText(code.innerText).then(() => {{
                btn.innerText = "Copied Source!";
                setTimeout(() => btn.innerText = "Copy Source", 1500);
            }});
        }}
    </script>
    {live_reload_js}
</body>
</html>
"""
    return full_html

# ==============================================================================
# Main Compiler Logic
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(description="Standalone Premium Markdown to HTML Compiler")
    parser.add_argument("--file", help="Specific markdown file to compile")
    parser.add_argument("--dir", default="./docs", help="Directory where markdown files live")
    parser.add_argument("--watch", action="store_true", help="Enable live-reload script injection")
    args = parser.parse_args()

    markdown_files = []
    if args.file:
        if os.path.exists(args.file):
            markdown_files.append(args.file)
        else:
            print(f"Error: {args.file} not found.")
            sys.exit(1)
    else:
        if os.path.exists(args.dir):
            for file in os.listdir(args.dir):
                if file.endswith(".md"):
                    markdown_files.append(os.path.join(args.dir, file))
        else:
            print(f"Warning: Directory {args.dir} not found. Creating empty docs folder.")
            os.makedirs(args.dir, exist_ok=True)

    if not markdown_files:
        print("No markdown files discovered to compile.")
        sample_path = os.path.join(args.dir, "user_guide.md")
        with open(sample_path, "w") as f:
            f.write("""---
title: "User & Demo Guide"
theme: "technical"
description: "High-impact developer portal layout"
---

# User & Demo Guide

Welcome to your newly compiled software project documentation guide!

:::: grid

::: card Get Started
Compile your files by running the standard python CLI command:
```bash
python compile_docs.py
```
:::

::: card Custom Themes
Use the frontmatter key `theme` to dynamically toggle layouts!
:::

::::
""")
        markdown_files.append(sample_path)

    sidebar_links = []
    for f_path in sorted(markdown_files):
        basename = os.path.basename(f_path)
        base, _ = os.path.splitext(basename)
        sidebar_links.append(f'<a href="{base}.html" class="sidebar-link">{base.replace("_", " ").title()}</a>')
    sidebar_nav_html = "\n".join(sidebar_links)

    for f_path in markdown_files:
        print(f"Compiling: {f_path}")
        with open(f_path, "r", encoding="utf-8") as f:
            raw_text = f.read()

        basename = os.path.basename(f_path)
        base, _ = os.path.splitext(basename)

        parser_instance = MarkdownParser("technical")
        fm, content = parser_instance.parse_frontmatter(raw_text)

        doc_title = fm.get("title", base.replace("_", " ").title())
        doc_desc = fm.get("description", "")
        doc_theme = fm.get("theme", "technical").lower()

        if doc_theme not in THEME_CSS:
            print(f"  Warning: Theme '{doc_theme}' is unrecognized. Defaulting to 'technical'.")
            doc_theme = "technical"

        parser_instance.theme = doc_theme
        parsed_body = parser_instance.parse(content)

        toc_links = []
        for header in parser_instance.headers:
            if header["level"] == 2:
                toc_links.append(f'<a href="#{header["id"]}" class="sidebar-link text-xs">{header["title"]}</a>')
            elif header["level"] == 3:
                toc_links.append(f'<a href="#{header["id"]}" class="sidebar-link text-xs ml-4">{header["title"]}</a>')
        toc_html = "\n".join(toc_links)

        active_sidebar_nav = sidebar_nav_html.replace(
            f'href="{base}.html" class="sidebar-link"',
            f'href="{base}.html" class="sidebar-link active"'
        )

        final_html = assemble_html(
            doc_title,
            doc_desc,
            parsed_body,
            active_sidebar_nav,
            toc_html,
            doc_theme,
            raw_markdown_src=raw_text,
            live_reload=args.watch
        )

        out_folder = os.path.dirname(f_path)
        out_path = os.path.join(out_folder, f"{base}.html")
        with open(out_path, "w", encoding="utf-8") as f_out:
            f_out.write(final_html)

        print(f"  Compiled Successfully: {out_path}")

if __name__ == "__main__":
    main()
