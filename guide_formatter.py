#!/usr/bin/env python3
"""
FFIX Excalibur II Perfect Game Guide - HTML Generator (v3)
Reads guide_content.txt and produces a styled, interactive HTML file.
Improvements: ability tables, Gil totals, info box sub-tables,
preliminaries ToC, credits ASCII art preservation.
"""

import re
import html as html_lib

INPUT_FILENAME = "guide_content.txt"
OUTPUT_FILENAME = "ff9_completeguide.html"

# ============================================================================
# HTML TEMPLATE
# ============================================================================

HTML_HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FFIX - Excalibur II & Perfect Game Guide</title>
    <meta name="description" content="Interactive HTML guide for the Final Fantasy IX Excalibur II & Perfect Game Challenge, based on Atomos199's legendary walkthrough.">
    <meta name="author" content="Atomos199 (original guide), formatted for the web">
    <meta property="og:title" content="FFIX Excalibur II & Perfect Game Guide">
    <meta property="og:description" content="The definitive interactive guide for FFIX's ultimate challenge — get the Excalibur II while completing a perfect game.">
    <meta property="og:type" content="website">
    <meta name="theme-color" content="#c8a84b">
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>⚔️</text></svg>">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Macondo&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        :root {
            --bg-main: #080d1a; --bg-secondary: #0d1428; --bg-tertiary: #0a1020;
            --border-color: #1c2840; --text-main: #e8dfc4; --text-secondary: #7a96b2;
            --accent-primary: #c8a84b; --accent-secondary: #8a6c20; --accent-danger: #b84040;
            --accent-danger-light: #d88070; --accent-warn: #c49a32; --accent-info: #3888a8;
            --accent-green: #3a8a68; --accent-green-dim: #24614a;
            --glow-primary: rgba(200, 168, 75, 0.14); --glow-danger: rgba(184, 64, 64, 0.1);
            --glow-warn: rgba(196, 154, 50, 0.1); --glow-green: rgba(58, 138, 104, 0.1);
        }
        * { box-sizing: border-box; }
        html { scroll-behavior: smooth; }
        body { font-family: 'Inter', system-ui, sans-serif; background-color: var(--bg-main); color: var(--text-main); line-height: 1.7; }
        ::selection { background: var(--accent-secondary); color: white; }
        ::-webkit-scrollbar { width: 8px; height: 8px; }
        ::-webkit-scrollbar-track { background: var(--bg-main); }
        ::-webkit-scrollbar-thumb { background: var(--border-color); border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: var(--accent-secondary); }

        .guide-container { max-width: 1100px; margin: auto; padding: 1rem 2rem 4rem 2rem; }

        /* --- HEADER --- */
        .guide-header { text-align: center; padding: 2rem 0 1.5rem; position: relative; }
        .guide-header::after { content: '\u25c6 \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 \u25c6'; display: block; color: var(--accent-primary); opacity: 0.6; font-size: 0.85rem; letter-spacing: 0.15em; margin: 1.25rem auto 0; text-align: center; }
        .guide-header h1 { font-family: 'Macondo', Georgia, serif; font-size: 2.8rem; font-weight: 400; background: linear-gradient(135deg, #ffe08a 0%, #c8a84b 45%, #8a6c20 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; letter-spacing: 0.06em; text-shadow: none; }
        .guide-header .subtitle { font-size: 1.25rem; color: var(--text-secondary); font-weight: 400; margin-top: 0.25rem; }
        .guide-header .credit { font-size: 0.8rem; color: #64748b; margin-top: 0.5rem; }
        .guide-header .credit a { color: var(--accent-primary); text-decoration: none; }
        .guide-header .credit a:hover { text-decoration: underline; }

        /* --- PROGRESS BAR --- */
        .progress-bar { position: fixed; top: 0; left: 0; width: 0%; height: 3px; background: linear-gradient(90deg, var(--accent-secondary), var(--accent-primary)); z-index: 100; transition: width 0.1s; }

        /* --- TABS --- */
        .tabs { display: flex; border-bottom: 2px solid var(--accent-secondary); position: sticky; top: 0; background-color: rgba(8,13,26,0.97); backdrop-filter: blur(16px); z-index: 50; flex-wrap: wrap; gap: 0; padding: 0 0.5rem; }
        .tab-button { background-color: transparent; border: none; padding: 0.875rem 1.25rem; color: var(--text-secondary); cursor: pointer; font-size: 1rem; font-weight: 400; font-family: 'Macondo', Georgia, serif; letter-spacing: 0.04em; position: relative; transition: color 0.2s; }
        .tab-button:hover { color: var(--text-main); }
        .tab-button.active { color: var(--accent-primary); }
        .tab-button.active::after { content: ''; position: absolute; bottom: -2px; left: 0.5rem; right: 0.5rem; height: 2px; background: var(--accent-primary); border-radius: 1px 1px 0 0; }
        .tab-content { display: none; padding-top: 1rem; animation: fadeIn 0.3s ease; }
        .tab-content.active { display: block; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }

        /* --- SEGMENTS --- */
        .segment-box { background-color: var(--bg-secondary); border: 1px solid var(--border-color); margin-top: 1rem; border-radius: 0.75rem; overflow: hidden; transition: border-color 0.2s, box-shadow 0.2s; }
        .segment-box:hover { border-color: #3a4060; box-shadow: 0 0 0 1px rgba(200,168,75,0.10); }
        .foldable-header { width: 100%; display: flex; justify-content: space-between; align-items: center; padding: 1rem 1.5rem; cursor: pointer; background-color: transparent; border: none; color: var(--text-secondary); text-align: left; transition: background-color 0.15s; font-family: 'Macondo', Georgia, serif; }
        .foldable-header:hover { background-color: rgba(200,168,75,0.05); }
        .segment-title-container { display: flex; align-items: center; gap: 0.75rem; }
        .segment-title-container input[type="checkbox"] { width: 1.15rem; height: 1.15rem; flex-shrink: 0; accent-color: var(--accent-primary); cursor: pointer; }
        .segment-title { font-family: 'Macondo', Georgia, serif; font-size: 1.2rem; font-weight: 400; color: var(--text-main); letter-spacing: 0.03em; }
        .segment-code { font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; color: var(--accent-primary); opacity: 0.7; }
        .foldable-content { padding: 0 1.5rem 1.5rem 1.5rem; border-top: 1px solid var(--border-color); max-height: 10000px; transition: max-height 0.35s ease-in-out, padding 0.2s, visibility 0.2s; visibility: visible; }
        .foldable-content.collapsed { max-height: 0; padding-top: 0; padding-bottom: 0; overflow: hidden; visibility: hidden; }
        .arrow-icon { transition: transform 0.25s ease; flex-shrink: 0; opacity: 0.5; }
        .foldable-header:hover .arrow-icon { opacity: 0.8; }
        .foldable-header.collapsed .arrow-icon { transform: rotate(-90deg); }

        /* --- IN-SECTION FOCUS DIMMING --- */
        .foldable-content > *,
        .foldable-content > .mt-4 > *,
        .foldable-content .instruction-list > li,
        .battle-box > *, .battle-box ul > li { transition: opacity 0.18s, filter 0.18s; }
        .foldable-content:has(> *:hover) > *:not(:hover) { opacity: 0.38; filter: brightness(0.6); }
        .foldable-content > .mt-4:has(> *:hover) > *:not(:hover) { opacity: 0.38; filter: brightness(0.6); }
        .foldable-content .instruction-list:has(> li:hover) > li:not(:hover) { opacity: 0.38; filter: brightness(0.6); }
        .battle-box ul:has(> li:hover) > li:not(:hover) { opacity: 0.38; filter: brightness(0.6); }
        .foldable-content .instruction-list > li:hover,
        .battle-box ul > li:hover { background: rgba(200,168,75,0.06); border-radius: 0.3rem; padding-left: 0.3rem; margin-left: -0.3rem; }

        /* --- TREASURE CHECKLIST --- */
        .treasure-list { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 0.4rem; background-color: var(--bg-tertiary); padding: 1rem; border-radius: 0.5rem; margin: 1.5rem 0; border: 1px solid var(--border-color); }
        .checklist-item { display: flex; align-items: flex-start; padding: 0.2rem 0.4rem; border-radius: 0.25rem; transition: background 0.15s; }
        .checklist-item:hover { background: rgba(200,168,75,0.07); }
        .checklist-item input { margin-top: 0.3rem; margin-right: 0.6rem; width: 0.9rem; height: 0.9rem; flex-shrink: 0; accent-color: var(--accent-green); cursor: pointer; }
        .checklist-item span { font-size: 0.875rem; }

        /* --- INSTRUCTIONS --- */
        .instruction-list { padding-left: 1.5rem; margin: 0.5rem 0; }
        .instruction-list > li { list-style: disc; margin-bottom: 0.6rem; line-height: 1.55; }

        /* --- BATTLE BOX --- */
        .battle-box { background: linear-gradient(135deg, rgba(180,60,60,0.06) 0%, var(--bg-tertiary) 100%); padding: 1rem 1.25rem; margin: 1.25rem 0; border-radius: 0.5rem; border-left: 3px solid var(--accent-danger); }
        .battle-title { font-family: 'Macondo', Georgia, serif; font-weight: 400; color: var(--accent-danger-light); font-size: 1.15rem; letter-spacing: 0.04em; display: flex; align-items: center; gap: 0.5rem; }
        .battle-title::before { content: '⚔'; font-size: 0.9rem; }

        /* --- DETOUR / INFO BOX --- */
        .detour-box { background: linear-gradient(135deg, rgba(180,150,50,0.06) 0%, var(--bg-tertiary) 100%); padding: 1rem 1.25rem; margin: 1.25rem 0; border-radius: 0.5rem; border-left: 3px solid var(--accent-warn); }
        .detour-title { font-family: 'Macondo', Georgia, serif; font-weight: 400; color: var(--accent-warn); font-size: 1.15rem; letter-spacing: 0.04em; display: flex; align-items: center; gap: 0.5rem; }
        .detour-title::before { content: '💡'; font-size: 0.85rem; }

        /* --- PATH BOX --- */
        .path-box { background: linear-gradient(135deg, rgba(40,140,100,0.06) 0%, var(--bg-tertiary) 100%); padding: 1rem 1.25rem; margin: 1.25rem 0; border-radius: 0.5rem; border-left: 3px solid var(--accent-green); }
        .path-label { display: inline-block; margin: 1.25rem 0 0.5rem; padding: 0.2rem 0.75rem; border-radius: 0.3rem; background: rgba(58,138,104,0.15); border: 1px solid var(--accent-green); color: var(--accent-green); font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase; }

        /* --- PERFECT STATS CARDS --- */
        .stat-path-card { border: 1px solid rgba(255,255,255,0.09); border-radius: 0.45rem; margin: 0.85rem 0 1.4rem; overflow: hidden; }
        .stat-path-header { display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 0.4rem; padding: 0.55rem 0.9rem; background: rgba(255,255,255,0.04); border-bottom: 1px solid rgba(255,255,255,0.07); }
        .stat-path-name { font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; font-weight: 700; letter-spacing: 0.07em; text-transform: uppercase; color: var(--accent-green); }
        .stat-badges { display: flex; gap: 0.35rem; flex-wrap: wrap; }
        .stat-badge { font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; font-weight: 700; padding: 0.1rem 0.42rem; border-radius: 0.2rem; }
        .stat-badge.spr { background: rgba(58,138,104,0.18); color: #6fcca0; border: 1px solid rgba(58,138,104,0.4); }
        .stat-badge.str { background: rgba(200,75,75,0.15); color: #e88a8a; border: 1px solid rgba(200,75,75,0.35); }
        .stat-badge.mag { background: rgba(130,88,200,0.15); color: #b89ae8; border: 1px solid rgba(130,88,200,0.35); }
        .stat-badge.spd { background: rgba(196,154,50,0.15); color: #e8cc7a; border: 1px solid rgba(196,154,50,0.35); }
        .stat-equip-table { width: 100%; border-collapse: collapse; }
        .stat-equip-table thead th { padding: 0.3rem 0.75rem; font-size: 0.62rem; letter-spacing: 0.08em; text-transform: uppercase; color: #4a5568; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.06); }
        .stat-equip-table tbody td { padding: 0.28rem 0.75rem; font-size: 0.8rem; color: #9aa5b4; border-bottom: 1px solid rgba(255,255,255,0.04); }
        .stat-equip-table tbody tr:last-child td { border-bottom: none; }
        .stat-equip-table tbody tr:hover td { background: rgba(255,255,255,0.02); }
        .stat-equip-table td.lvl-badge { font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; font-weight: 700; color: var(--accent-green); white-space: nowrap; min-width: 2.5rem; }
        .char-section-header { font-family: 'Macondo', Georgia, serif; font-size: 1.3rem; font-weight: 400; letter-spacing: 0.1em; text-transform: uppercase; color: var(--accent-green); margin: 2.2rem 0 0.5rem; padding-bottom: 0.4rem; border-bottom: 1px solid rgba(58,138,104,0.3); }

        /* --- CONFIG BOX --- */
        .config-box { background: linear-gradient(135deg, rgba(50,140,170,0.06) 0%, var(--bg-tertiary) 100%); padding: 1rem 1.25rem; margin: 1.25rem 0; border-radius: 0.5rem; border-left: 3px solid var(--accent-info); }
        .config-title { font-family: 'Macondo', Georgia, serif; font-weight: 400; color: var(--accent-info); font-size: 1.15rem; letter-spacing: 0.04em; }

        /* --- SHOP BOX --- */
        .shop-box { background: linear-gradient(135deg, rgba(40,140,100,0.06) 0%, var(--bg-tertiary) 100%); padding: 1rem 1.25rem; margin: 0.75rem 0; border-radius: 0.5rem; border-left: 3px solid var(--accent-green); }
        .shop-title { font-family: 'Macondo', Georgia, serif; font-weight: 400; color: var(--accent-green); font-size: 1.15rem; letter-spacing: 0.04em; }

        /* --- TABLES --- */
        .shop-table {
            width: 100%; border-collapse: separate; border-spacing: 0;
            border-radius: 0.5rem; overflow: hidden;
            background: var(--bg-tertiary);
        }
        .shop-table th {
            background: rgba(28,40,64,0.9);
            color: #c8c0a8; font-weight: 600; font-size: 0.8rem;
            text-transform: uppercase; letter-spacing: 0.05em;
            padding: 0.6rem 0.875rem; border-bottom: 1px solid var(--border-color);
            text-align: left;
        }
        .shop-table td {
            padding: 0.5rem 0.875rem; border-bottom: 1px solid rgba(28,40,64,0.6);
            color: #c8c0a8; font-size: 0.85rem;
        }
        .shop-table tr:hover td { background-color: rgba(200,168,75,0.06); }
        .shop-table tr:last-child td { border-bottom: none; }

        /* --- TARGET MARKERS --- */
        .target-marker { background-color: var(--bg-tertiary); border: 1px solid var(--border-color); border-radius: 0.375rem; padding: 0.5rem 1rem; margin: 1rem 0; text-align: center; font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; color: var(--accent-info); }
        .target-summary { background: linear-gradient(135deg, rgba(200,168,75,0.08) 0%, var(--bg-tertiary) 100%); border-top: 2px solid var(--accent-secondary); padding: 1rem; display: flex; justify-content: space-around; font-family: 'JetBrains Mono', monospace; text-align: center; border-radius: 0 0 0.75rem 0.75rem; }

        /* --- TOC --- */
        .toc { background-color: var(--bg-secondary); border: 1px solid var(--border-color); padding: 2rem; border-radius: 0.75rem; margin-top: 1.5rem; }
        .toc h4 { font-family: 'Macondo', Georgia, serif; color: var(--accent-primary); font-weight: 400; font-size: 1.2rem; letter-spacing: 0.04em; margin-top: 1.25rem; margin-bottom: 0.5rem; }
        .toc ul { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 0.5rem; list-style: none; padding: 0; }
        .toc a { text-decoration: none; color: var(--text-secondary); transition: all 0.15s; display: block; padding: 0.3rem 0.5rem; border-radius: 0.25rem; font-size: 0.9rem; }
        .toc a:hover { color: var(--accent-primary); background: var(--glow-primary); }

        /* --- SECTION HEADERS --- */
        .section-header { font-family: 'Macondo', Georgia, serif; color: var(--accent-primary); font-weight: 400; font-size: 1.5rem; letter-spacing: 0.05em; margin-top: 2rem; margin-bottom: 1rem; border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem; }
        .subsection-header { font-family: 'Macondo', Georgia, serif; color: var(--accent-warn); font-weight: 400; font-size: 1.2rem; letter-spacing: 0.04em; margin-top: 1.5rem; margin-bottom: 0.75rem; }

        /* --- EXTRAS --- */
        .extras-box { background-color: var(--bg-secondary); border: 1px solid var(--border-color); padding: 1.5rem; border-radius: 0.5rem; margin: 1rem 0; }

        /* --- ASCII ART --- */
        pre.ascii-art { font-family: 'Courier New', Courier, monospace; white-space: pre; overflow-x: auto; color: var(--accent-primary); background-color: var(--bg-tertiary); padding: 1.5rem; border-radius: 0.75rem; margin: 1rem auto; font-size: 0.7rem; line-height: 1.25; text-align: left; max-width: 100%; border: 1px solid var(--border-color); }

        /* --- ABILITY TABLE --- */
        .ability-table { width: 100%; border-collapse: collapse; margin-top: 0.25rem; }
        .ability-table td { padding: 3px 8px; font-size: 0.8rem; font-family: 'JetBrains Mono', monospace; vertical-align: top; }
        .ability-table .char-cell { font-weight: 700; color: #e2e8f0; width: 30px; text-align: center; border-right: 1px solid var(--border-color); }
        .ability-cell { color: var(--text-secondary); }
        .ability-mastered { color: var(--accent-green); font-weight: 600; }
        .ability-learning { color: var(--accent-warn); font-family: 'JetBrains Mono', monospace; }

        /* --- GIL AMOUNTS --- */
        .gil-amount { font-family: 'JetBrains Mono', monospace; text-align: right; font-size: 0.85rem; padding: 0.35rem 1rem; border-radius: 0.25rem; }
        .gil-amount .label { color: var(--text-secondary); }
        .gil-amount .value { color: var(--accent-warn); font-weight: 600; }

        /* --- INFO SUBTITLES --- */
        .info-subtitle { font-weight: 700; color: var(--accent-warn); font-size: 0.95rem; margin: 0.75rem 0 0.25rem; text-align: center; text-transform: uppercase; letter-spacing: 0.03em; }

        /* --- TOC NAV (in preliminaries) --- */
        .toc-nav { list-style: none; padding: 0; margin: 1.5rem 0; }
        .toc-nav li { padding: 0.45rem 0.75rem; font-size: 0.95rem; border-bottom: 1px solid rgba(42,53,80,0.4); display: flex; justify-content: space-between; transition: background 0.15s; }
        .toc-nav li:hover { background: var(--glow-primary); border-radius: 0.25rem; }
        .toc-nav .toc-num { color: var(--accent-primary); min-width: 2.5rem; font-weight: 500; }
        .toc-nav .toc-title { color: var(--text-main); flex: 1; }
        .toc-nav .toc-code { color: var(--accent-info); font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; opacity: 0.7; }
        .toc-nav .toc-sub { padding-left: 2.5rem; font-size: 0.9rem; }

        /* --- EXAMPLE SEGMENT --- */
        .example-segment { margin: 1.5rem 0; border-radius: 0.75rem; border: 1px solid var(--accent-warn); overflow: hidden; background: linear-gradient(180deg, rgba(251,191,36,0.03) 0%, var(--bg-secondary) 100%); }
        .example-segment-label { padding: 0.5rem 1.25rem; background: linear-gradient(135deg, rgba(251,191,36,0.15) 0%, rgba(251,191,36,0.05) 100%); border-bottom: 1px solid var(--accent-warn); color: var(--accent-warn); font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; }
        .example-segment-body { padding: 1.25rem; }
        .example-segment-header { font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; color: var(--text-main); background: var(--bg-tertiary); border: 1px solid var(--border-color); border-radius: 0.5rem; padding: 0.75rem 1rem; margin-bottom: 1rem; text-align: center; font-weight: 600; }
        .example-annotation { font-size: 0.8rem; color: var(--accent-warn); font-style: italic; padding: 0.25rem 0 0.5rem 2rem; opacity: 0.85; }

        /* --- CREDITS --- */
        .credit-tribute { margin: 1.5rem 0; padding: 1.25rem; background: var(--bg-tertiary); border-radius: 0.75rem; border: 1px solid var(--border-color); overflow-x: auto; }
        .credit-tribute pre { margin: 0; font-family: 'Courier New', monospace; white-space: pre; font-size: 0.72rem; line-height: 1.3; color: var(--text-secondary); }
        .credit-tribute .tribute-name { color: var(--accent-primary); font-weight: 700; font-size: 1rem; margin-top: 0.5rem; text-align: center; }
        .credit-separator { border: none; border-top: 1px solid var(--border-color); margin: 1.5rem 0; }

        /* --- BACK TO TOP --- */
        .back-to-top { position: fixed; bottom: 2rem; right: 2rem; width: 2.5rem; height: 2.5rem; border-radius: 50%; background: var(--accent-secondary); color: var(--text-main); border: 1px solid var(--accent-primary); cursor: pointer; display: flex; align-items: center; justify-content: center; opacity: 0; visibility: hidden; transition: all 0.3s; z-index: 60; box-shadow: 0 4px 12px rgba(200,168,75,0.35); }
        .back-to-top.visible { opacity: 1; visibility: visible; }
        .back-to-top:hover { background: var(--accent-primary); transform: translateY(-2px); }

        /* --- SEARCH --- */
        .search-bar { position: relative; margin-bottom: 0.5rem; }
        .search-bar input { width: 100%; padding: 0.6rem 1rem 0.6rem 2.5rem; background: var(--bg-tertiary); border: 1px solid var(--border-color); border-radius: 0.5rem; color: var(--text-main); font-size: 0.9rem; font-family: 'Inter', system-ui, sans-serif; outline: none; transition: border-color 0.2s; }
        .search-bar input::placeholder { color: #475569; }
        .search-bar input:focus { border-color: var(--accent-primary); box-shadow: 0 0 0 2px var(--glow-primary); }
        .search-bar svg { position: absolute; left: 0.75rem; top: 50%; transform: translateY(-50%); color: #475569; pointer-events: none; }
        .search-highlight { background: rgba(251,191,36,0.25); border-radius: 2px; }
        .segment-box.search-hidden { display: none; }

        /* --- MISC --- */
        p { margin-top: 0.4rem; margin-bottom: 0.4rem; }

        /* --- RESPONSIVE --- */
        @media (max-width: 768px) {
            .guide-container { padding: 0.5rem 1rem 3rem; }
            .guide-header h1 { font-size: 1.75rem; }
            .guide-header .subtitle { font-size: 1rem; }
            .tab-button { padding: 0.7rem 0.75rem; font-size: 0.8rem; }
            .treasure-list { grid-template-columns: 1fr; }
            .toc ul { grid-template-columns: 1fr; }
            .target-summary { flex-direction: column; gap: 0.5rem; }
            .foldable-header { padding: 0.875rem 1rem; }
            .foldable-content { padding: 0 1rem 1rem 1rem; }
        }

        /* --- PRINT --- */
        @media print {
            body { background: white; color: black; }
            .tabs, .back-to-top, .search-bar, .progress-bar { display: none !important; }
            .tab-content { display: block !important; }
            .foldable-content { max-height: none !important; visibility: visible !important; padding: 1rem !important; }
            .foldable-header.collapsed .arrow-icon { transform: none; }
            .segment-box { page-break-inside: avoid; border-color: #ccc; }
        }
    </style>
    <script data-goatcounter="https://matthvephd.goatcounter.com/count"
            async src="//gc.zgo.at/count.js"></script>
</head>
<body>
<div class="progress-bar" id="progress-bar"></div>
<div class="guide-container">
    <header class="guide-header">
        <h1>Final Fantasy IX</h1>
        <div class="subtitle">Excalibur II &amp; Perfect Game Challenge</div>
        <div class="credit">Interactive guide based on <a href="https://gamefaqs.gamespot.com/ps/197338-final-fantasy-ix/faqs/41181" target="_blank" rel="noopener">Atomos199's v.X walkthrough</a></div>
    </header>
    <div style="background:rgba(200,168,75,0.06); border:1px solid rgba(200,168,75,0.22); border-radius:0.75rem; padding:1rem 1.25rem; margin:0 auto 1.5rem; max-width:52rem; font-size:0.85rem; color:#8ba0be; line-height:1.6; text-align:center;">
        <strong style="color:#e8c96a;">Fan Reformatting &mdash; Not for Commercial Use</strong><br>
        All guide content is the intellectual property of <strong style="color:var(--accent-primary)">Atomos199</strong> (© 2005-2015).
        This interactive HTML version is an unofficial, non-commercial fan reformatting made for personal use and ease of reading.
        Final Fantasy IX is a trademark of <strong style="color:#94a3b8">Square Enix Co., Ltd.</strong>
        No copyright infringement is intended. For the original guide, visit
        <a href="https://gamefaqs.gamespot.com/ps/197338-final-fantasy-ix/faqs/41181" target="_blank" rel="noopener" style="color:var(--accent-primary);text-decoration:underline;">GameFAQs</a>.
    </div>
"""

HTML_TABS = """
    <div class="search-bar">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg>
        <input type="text" id="search-input" placeholder="Search segments... (e.g. 'Burmecia', 'Disc 3', 'shop')">
    </div>
    <nav class="tabs" id="disc-tabs">
        <button class="tab-button active" data-tab="preliminaries">Preliminaries</button>
        <button class="tab-button" data-tab="contents">Contents</button>
        <button class="tab-button" data-tab="disc1">Disc 1</button>
        <button class="tab-button" data-tab="disc2">Disc 2</button>
        <button class="tab-button" data-tab="disc3">Disc 3</button>
        <button class="tab-button" data-tab="disc4">Disc 4</button>
        <button class="tab-button" data-tab="extras">Extras</button>
    </nav>
    <main>
"""

HTML_FOOTER = """
    </main>
    <footer style="text-align:center; padding:3rem 1.5rem 1.5rem; color:#475569; font-size:0.75rem; border-top:1px solid var(--border-color); margin-top:3rem; line-height:1.8;">
        <p style="font-size:0.85rem; color:#94a3b8; margin-bottom:0.5rem;">
            Original guide by <strong style="color:var(--accent-primary)">Atomos199</strong> · Version X · © 2005-2015
        </p>
        <p>
            Interactive HTML reformatting &mdash; unofficial, non-commercial fan project for personal use.<br>
            <a href="https://gamefaqs.gamespot.com/ps/197338-final-fantasy-ix/faqs/41181" target="_blank" rel="noopener" style="color:var(--accent-primary);text-decoration:none;">View original guide on GameFAQs</a>
        </p>
        <p style="margin-top:0.75rem; color:#334155; font-size:0.7rem;">
            Final Fantasy IX™ is a registered trademark of Square Enix Co., Ltd. All game content, characters, and imagery are © Square Enix.<br>
            Guide content remains the sole property of its author. This page is provided as-is with no warranty. No affiliation with Square Enix or GameFAQs is implied.
        </p>
    </footer>
</div>

<button class="back-to-top" id="back-to-top" title="Back to top">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 15l-6-6-6 6"/></svg>
</button>

<script>
document.addEventListener('DOMContentLoaded', function () {
    // === TAB SWITCHING ===
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');

    function switchTab(tabId) {
        tabButtons.forEach(btn => btn.classList.toggle('active', btn.dataset.tab === tabId));
        tabContents.forEach(content => content.classList.toggle('active', content.id === tabId));
        try { localStorage.setItem('ffix_active_tab', tabId); } catch(e) {}
    }

    // Restore last active tab on load
    const savedTab = (() => { try { return localStorage.getItem('ffix_active_tab'); } catch(e) { return null; } })();
    if (savedTab && document.getElementById(savedTab)) switchTab(savedTab);

    tabButtons.forEach(button => {
        button.addEventListener('click', () => switchTab(button.dataset.tab));
    });

    // === FOLDABLE SECTIONS ===
    const foldableHeaders = document.querySelectorAll('.foldable-header');
    foldableHeaders.forEach(header => {
        header.addEventListener('click', (e) => {
            if (e.target.tagName === 'INPUT') return;
            header.classList.toggle('collapsed');
            header.nextElementSibling.classList.toggle('collapsed');
            saveFolded();
        });
    });

    // === TOC NAVIGATION ===
    document.querySelectorAll('.toc a').forEach(link => {
        link.addEventListener('click', (event) => {
            event.preventDefault();
            const targetTab = link.getAttribute('data-target-tab');
            const targetId = link.getAttribute('href');
            if (targetTab) {
                switchTab(targetTab);
                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    const header = targetElement.querySelector('.foldable-header');
                    if (header && header.classList.contains('collapsed')) {
                        header.click();
                    }
                    setTimeout(() => targetElement.scrollIntoView({ behavior: 'smooth', block: 'start' }), 150);
                }
            }
        });
    });

    // === PROGRESS BAR ===
    const progressBar = document.getElementById('progress-bar');
    function updateProgress() {
        const scrollTop = window.scrollY;
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
        const progress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
        progressBar.style.width = progress + '%';
    }
    window.addEventListener('scroll', updateProgress, { passive: true });

    // === BACK TO TOP ===
    const backToTop = document.getElementById('back-to-top');
    window.addEventListener('scroll', () => {
        backToTop.classList.toggle('visible', window.scrollY > 400);
    }, { passive: true });
    backToTop.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    // === SEARCH ===
    const searchInput = document.getElementById('search-input');
    let searchTimeout;
    searchInput.addEventListener('input', () => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(doSearch, 200);
    });

    function doSearch() {
        const query = searchInput.value.trim().toLowerCase();
        const segments = document.querySelectorAll('.segment-box');
        if (!query) {
            segments.forEach(s => s.classList.remove('search-hidden'));
            return;
        }
        // Switch to the tab with the best results, or show all
        let anyVisible = false;
        segments.forEach(seg => {
            const title = seg.querySelector('.segment-title');
            const text = (title ? title.textContent : '') + ' ' + seg.id;
            const match = text.toLowerCase().includes(query);
            seg.classList.toggle('search-hidden', !match);
            if (match) anyVisible = true;
        });
        // If no title matches, try full text
        if (!anyVisible) {
            segments.forEach(seg => {
                const content = seg.textContent.toLowerCase();
                const match = content.includes(query);
                seg.classList.toggle('search-hidden', !match);
            });
        }
    }

    // === KEYBOARD SHORTCUTS ===
    document.addEventListener('keydown', (e) => {
        // Ctrl/Cmd + K = focus search
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            searchInput.focus();
            searchInput.select();
        }
        // Escape = clear search
        if (e.key === 'Escape' && document.activeElement === searchInput) {
            searchInput.value = '';
            doSearch();
            searchInput.blur();
        }
    });

    // === CHECKBOX PERSISTENCE (localStorage) ===
    const STORAGE_KEY = 'ffix_guide_checked';
    function loadChecked() {
        try {
            const data = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}');
            document.querySelectorAll('.segment-box').forEach(box => {
                const id = box.id;
                if (!id) return;
                // Segment completion checkbox
                const headerCb = box.querySelector('.segment-title-container input[type="checkbox"]');
                if (headerCb && data[id + '_done']) {
                    headerCb.checked = true;
                    box.style.opacity = '0.6';
                }
                // Treasure checkboxes
                box.querySelectorAll('.checklist-item input[type="checkbox"]').forEach((cb, idx) => {
                    if (data[id + '_t' + idx]) cb.checked = true;
                });
                // Restore expanded state
                if (data[id + '_open']) {
                    const h = box.querySelector('.foldable-header');
                    const c = box.querySelector('.foldable-content');
                    if (h && c) {
                        h.classList.remove('collapsed');
                        c.classList.remove('collapsed');
                    }
                }
            });
            // Auction checklist
            document.querySelectorAll('.auction-checklist input[data-auction-item]').forEach(cb => {
                if (data['auction_' + cb.dataset.auctionItem]) cb.checked = true;
            });
        } catch(e) {}
    }

    function saveChecked() {
        try {
            const data = {};
            document.querySelectorAll('.segment-box').forEach(box => {
                const id = box.id;
                if (!id) return;
                const headerCb = box.querySelector('.segment-title-container input[type="checkbox"]');
                if (headerCb && headerCb.checked) data[id + '_done'] = true;
                box.querySelectorAll('.checklist-item input[type="checkbox"]').forEach((cb, idx) => {
                    if (cb.checked) data[id + '_t' + idx] = true;
                });
                // Persist expanded state
                const h = box.querySelector('.foldable-header');
                if (h && !h.classList.contains('collapsed')) data[id + '_open'] = true;
            });
            // Auction checklist
            document.querySelectorAll('.auction-checklist input[data-auction-item]').forEach(cb => {
                if (cb.checked) data['auction_' + cb.dataset.auctionItem] = true;
            });
            localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
        } catch(e) {}
    }

    function saveFolded() { saveChecked(); }

    loadChecked();

    // Listen for checkbox changes
    document.addEventListener('change', (e) => {
        if (e.target.type === 'checkbox') {
            // Dim completed segments
            const box = e.target.closest('.segment-box');
            if (box) {
                const headerCb = box.querySelector('.segment-title-container input[type="checkbox"]');
                if (e.target === headerCb) {
                    box.style.opacity = headerCb.checked ? '0.6' : '1';
                }
            }
            saveChecked();
        }
    });

    // === EXPAND / COLLAPSE ALL (double-click tab) ===
    tabButtons.forEach(button => {
        button.addEventListener('dblclick', () => {
            const tabId = button.dataset.tab;
            const content = document.getElementById(tabId);
            if (!content) return;
            const headers = content.querySelectorAll('.foldable-header');
            const allExpanded = Array.from(headers).every(h => !h.classList.contains('collapsed'));
            headers.forEach(h => {
                const shouldCollapse = allExpanded;
                if (shouldCollapse && !h.classList.contains('collapsed')) {
                    h.classList.add('collapsed');
                    h.nextElementSibling.classList.add('collapsed');
                } else if (!shouldCollapse && h.classList.contains('collapsed')) {
                    h.classList.remove('collapsed');
                    h.nextElementSibling.classList.remove('collapsed');
                }
            });
            saveFolded();
        });
    });

});
</script>
</body>
</html>
"""

# ============================================================================
# UTILITIES
# ============================================================================

def esc(text):
    """HTML-escape text."""
    return html_lib.escape(str(text))

def is_pure_decoration(stripped):
    """True if line has no meaningful text (no letters, digits, or [] brackets)."""
    if not stripped:
        return True
    return not re.search(r'[a-zA-Z0-9\[\]]', stripped)

def is_block_start(lines, i):
    """Check if line i starts a recognized block (battle, info, config, shop, table)."""
    if i >= len(lines):
        return False
    s = lines[i].strip()
    if re.search(r'BATTLE:\s*.*?\|.*?\(\s*\d+\s*AP\s*\)', s):
        return True
    if re.match(r'.*\.--.*?/.+/.*--\.', s) and 'BATTLE' not in s:
        return True
    if re.match(r'^\s*\.[-]+\.\s*$', s):
        j = i + 1
        while j < len(lines) and not lines[j].strip():
            j += 1
        if j < len(lines) and '|' in lines[j] and '>' in lines[j]:
            return True
    if re.match(r'^-{5,}(\s+-{5,})?$', s) and _has_shop_ahead(lines, i):
        return True
    if re.match(r'^\s*\.=+\.=+\.', s):
        return True
    if re.search(r'(?:SELL|BUY)\s*:', s):
        return True
    if re.match(r'^\s*\|[^|]*>[^|]*\|\s*$', s):
        return True
    if s.lstrip().startswith('|') and s.rstrip().endswith('|') and s.count('|') >= 4:
        return True
    return False

def _has_shop_ahead(lines, idx):
    """Check if SELL/BUY content appears within 12 lines after idx."""
    for j in range(idx + 1, min(idx + 12, len(lines))):
        s = lines[j].strip()
        if re.search(r'(?:SELL|BUY)\s*:', s):
            return True
        if s.startswith('o ') and '|' not in s:
            return False
        if re.search(r'BATTLE:', s):
            return False
        if re.match(r'.*\.--.*?/.+/.*--\.', s):
            return False
    return False

def _strip_box_borders(line):
    """Strip outer |...| borders of an info/battle box line, preserving inner content."""
    first_pipe = line.find('|')
    last_pipe = line.rfind('|')
    if first_pipe >= 0 and last_pipe > first_pipe:
        return line[first_pipe + 1:last_pipe]
    return line.strip()

def _has_real_text(s):
    """Check if line has meaningful text beyond table junction chars like 'o'."""
    # Replace 'o'/'O' used as table junctions (surrounded by dashes/pipes)
    cleaned = re.sub(r'(?<=[-|+])o(?=[-|+])', '+', s)
    return bool(re.search(r'[a-zA-Z0-9\[\]]', cleaned))

def _is_table_separator(s):
    """Check if line is a table border/separator (only structural chars)."""
    if not s or len(s.strip()) < 3:
        return False
    # Replace 'o' used as junction markers
    cleaned = re.sub(r'(?<=[-|+])o(?=[-|+])', '+', s)
    return bool(re.match(r'^[-+|=.\'\`\s\\/]+$', cleaned))

# ============================================================================
# BOX COLLECTORS
# ============================================================================

def collect_battle_box(lines, start):
    """Collect and format a battle box. Returns (html, next_index)."""
    s = lines[start].strip()
    m = re.search(r'BATTLE:\s*(.*?)\s*\|.*?\(\s*(\d+)\s*AP\s*\)', s)
    name = m.group(1).strip() if m else 'Unknown'
    ap = m.group(2).strip() if m else '?'

    content = []
    abilities = []
    in_abilities = False
    i = start + 1
    close_i = None

    while i < len(lines):
        stripped = lines[i].strip()
        if re.match(r"^['\`][-=]+", stripped):
            close_i = i
            break
        if re.match(r'^\s*>[-=]+<', stripped):
            in_abilities = True
            i += 1
            continue
        clean = re.sub(r'^\s*\|\s*', '', lines[i])
        clean = re.sub(r'\s*\|\s*$', '', clean).strip()
        if in_abilities:
            if clean and re.search(r'[a-zA-Z0-9]', clean):
                abilities.append(clean)
        else:
            is_new_bullet = bool(re.match(r'^[•\*]\s*', clean))
            clean = re.sub(r'^[•\*]\s*', '', clean)
            if clean and re.search(r'[a-zA-Z0-9]', clean):
                if is_new_bullet or not content:
                    content.append(clean)
                else:
                    content[-1] = content[-1] + ' ' + clean
        i += 1

    i = (close_i + 1) if close_i is not None else i
    while i < len(lines) and is_pure_decoration(lines[i].strip()):
        i += 1

    html = '<div class="battle-box">'
    html += f'<div class="battle-title">{esc(name)} <span class="font-normal text-sm text-gray-400">({esc(ap)} AP)</span></div>'
    if content:
        html += '<ul class="list-disc list-inside mt-2 text-sm space-y-1">'
        for line in content:
            html += f'<li>{esc(line)}</li>'
        html += '</ul>'

    # === ABILITY TABLE (structured rendering) ===
    if abilities:
        # Merge continuation rows (empty char cell) into the previous character's row
        grouped = []  # list of [char_init, [raw_cell_strings]]
        for aline in abilities:
            cells = aline.split('|')
            char_init = cells[0].strip() if cells else ''
            ability_cells = cells[1:] if len(cells) > 1 else [aline]
            if not char_init and grouped:
                grouped[-1][1].extend(ability_cells)
            else:
                grouped.append([char_init, list(ability_cells)])

        html += '<div class="mt-3 border-t border-gray-600 pt-2">'
        html += '<table class="ability-table">'
        for char_init, ability_cells in grouped:
            # Remove trailing empty cells
            while ability_cells and not ability_cells[-1].strip():
                ability_cells.pop()
            html += '<tr>'
            html += f'<td class="char-cell">{esc(char_init)}</td>'
            for ac in ability_cells:
                ac = ac.strip()
                if not ac:
                    html += '<td class="ability-cell"></td>'
                elif '* * *' in ac:
                    aname = ac.replace('* * *', '').strip()
                    html += f'<td class="ability-cell ability-mastered">{esc(aname)} ★</td>'
                else:
                    am = re.match(r'(.+?)\s+(\d+)/(\d+)', ac)
                    if am:
                        aname = am.group(1).strip()
                        cur, tot = am.group(2), am.group(3)
                        pct = int(cur) / int(tot) * 100 if int(tot) > 0 else 0
                        if pct >= 100:
                            html += f'<td class="ability-cell ability-mastered">{esc(aname)} {cur}/{tot} ★</td>'
                        else:
                            html += f'<td class="ability-cell">{esc(aname)} <span class="ability-learning">{cur}/{tot}</span></td>'
                    else:
                        html += f'<td class="ability-cell">{esc(ac)}</td>'
            html += '</tr>'
        html += '</table></div>'

    html += '</div>'
    return html, i


def collect_info_box(lines, start):
    """Collect and format an info/detour box. Returns (html, next_index)."""
    s = lines[start].strip()
    m = re.search(r'/\s*(.+?)\s*/', s)
    title = m.group(1).strip() if m else 'Information'

    raw_content = []
    i = start + 1
    close_i = None
    time_cost = None

    while i < len(lines):
        stripped = lines[i].strip()
        if re.match(r"^['\`][-=]+", stripped):
            close_i = i
            tc_parts = re.findall(r'/\s*([^/]+?)\s*/', stripped)
            if tc_parts:
                time_cost = ' / '.join(t.strip() for t in tc_parts)
            break
        # Strip outer box borders, preserving inner structure
        inner = _strip_box_borders(lines[i])
        raw_content.append(inner)
        i += 1

    i = (close_i + 1) if close_i is not None else i
    while i < len(lines) and is_pure_decoration(lines[i].strip()):
        i += 1

    is_path = any(kw in title.upper() for kw in ['PATH', 'COMBINED', 'ORDERED', 'LV 1', 'LV1'])
    box_class = 'path-box' if is_path else 'detour-box'

    html = f'<div class="{box_class}">'
    html += f'<div class="detour-title">{esc(title)}</div>'
    html += _format_info_content(raw_content)

    # Auction house shopping checklist
    if 'AUCTION' in title.upper():
        html += _build_auction_checklist(raw_content)

    if time_cost:
        html += f'<div class="mt-2 text-right text-xs text-gray-400 font-mono border-t border-gray-600 pt-1">{esc(time_cost)}</div>'
    html += '</div>'
    return html, i


def _build_auction_checklist(raw_content):
    """Build a shopping checklist for auction house items based on box content."""
    # Extract item names from colon-delimited table rows
    table_items = []
    for line in raw_content:
        s = line.strip()
        if s.count(':') >= 3 and re.search(r'\d', s):
            data = re.sub(r'^\[\d+\]\s*', '', s)
            data = re.sub(r'^\|\s*', '', data)
            cols = [p.strip() for p in data.split(':')]
            if len(cols) >= 4:
                table_items.append(cols[0].strip())

    if not table_items:
        return ''

    # Join text lines into paragraphs for context analysis
    paragraphs = []
    current = []
    for line in raw_content:
        s = line.strip()
        if not s:
            if current:
                joined = ' '.join(current)
                joined = re.sub(r'(\w)- -(\w)', r'\1\2', joined)
                paragraphs.append(joined)
                current = []
        elif not _is_table_separator(s) and s.count(':') < 3:
            text = re.sub(r'^\*\s*', '', s)
            if text:
                current.append(text)
    if current:
        joined = ' '.join(current)
        joined = re.sub(r'(\w)- -(\w)', r'\1\2', joined)
        paragraphs.append(joined)

    # Classify items by context
    checklist = []
    for item in table_items:
        mentioned = False
        skip = False
        label = 'optional'
        for para in paragraphs:
            if item.lower() not in para.lower():
                continue
            mentioned = True
            lower = para.lower()
            if 'avoid' in lower or 'skip' in lower:
                skip = True
                break
            if 'need to win' in lower or 'need' in lower and 'win' in lower:
                label = 'required'
            elif any(kw in lower for kw in ['bid on', 'profit', 'selling them']):
                label = 'sell for profit'
        if mentioned and not skip:
            checklist.append((item, label))

    if not checklist:
        return ''

    slug = lambda s: re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')
    html = '<div class="auction-checklist mt-3 pt-3 border-t border-gray-600">'
    html += '<h4 class="font-bold text-amber-400 mb-2 text-sm">🛒 Shopping List:</h4>'
    html += '<div class="treasure-list">'
    for item, label in checklist:
        note = f' <span class="text-xs text-gray-500">({label})</span>' if label != 'optional' else ''
        html += (f'<div class="checklist-item">'
                 f'<input type="checkbox" data-auction-item="{esc(slug(item))}">'
                 f'<span>{esc(item)}{note}</span></div>')
    html += '</div></div>'
    return html


def _format_info_content(lines):
    """Format content inside an info/detour box, handling sub-tables and text."""
    parts = []
    pending_bullets = []    # completed bullet strings ready to emit as <ul>
    current_lines = []      # lines being accumulated (bullet or para)
    current_is_bullet = False
    in_pipe_table = False
    in_colon_table = False
    i = 0

    def fix_hyphens(s):
        return re.sub(r'(\w)- -(\w)', r'\1\2', s)

    def complete_current():
        """Finish the current accumulation, adding it to pending_bullets or emitting a <p>."""
        nonlocal current_is_bullet
        if not current_lines:
            return
        joined = fix_hyphens(' '.join(current_lines))
        current_lines.clear()
        if current_is_bullet:
            pending_bullets.append(joined)
        else:
            flush_bullets()
            parts.append(f'<p class="text-sm my-1">{esc(joined)}</p>')

    def flush_bullets():
        if pending_bullets:
            parts.append('<ul class="instruction-list">')
            for b in pending_bullets:
                parts.append(f'<li>{esc(b)}</li>')
            parts.append('</ul>')
            pending_bullets.clear()

    def flush_all():
        complete_current()
        flush_bullets()

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Empty line - complete current item; don't flush <ul> yet (next bullet may follow)
        if not stripped:
            complete_current()
            if in_pipe_table:
                parts.append('</table></div>')
                in_pipe_table = False
            if in_colon_table:
                parts.append('</table></div>')
                in_colon_table = False
            i += 1
            continue

        # Sub-section title: / TITLE \ pattern (all caps title inside slashes)
        subtitle_m = re.search(r'/\s+([A-Z][A-Z\s]{3,}[A-Z])\s+\\', stripped)
        if subtitle_m:
            flush_all()
            if in_pipe_table:
                parts.append('</table></div>')
                in_pipe_table = False
            if in_colon_table:
                parts.append('</table></div>')
                in_colon_table = False
            parts.append(f'<div class="info-subtitle">{esc(subtitle_m.group(1).strip())}</div>')
            i += 1
            continue

        # Table separator/border line
        if _is_table_separator(stripped):
            i += 1
            continue

        # All-caps column header (e.g., "ITEM  PRICE RANGE  AVERAGE  VALUE")
        # Check if followed by colon-delimited data
        if re.match(r'^[A-Z\s]+$', stripped) and len(stripped.split()) >= 3 and stripped.count('  ') >= 2:
            j = i + 1
            while j < len(lines) and (not lines[j].strip() or _is_table_separator(lines[j].strip())):
                j += 1
            if j < len(lines) and lines[j].strip().count(':') >= 3 and re.search(r'\d', lines[j].strip()):
                flush_all()
                if in_pipe_table:
                    parts.append('</table></div>')
                    in_pipe_table = False
                if in_colon_table:
                    parts.append('</table></div>')
                    in_colon_table = False
                cols = re.split(r'\s{2,}', stripped.strip())
                parts.append('<div class="overflow-x-auto my-2"><table class="shop-table">')
                parts.append('<tr><th></th>' + ''.join(f'<th>{esc(c)}</th>' for c in cols) + '</tr>')
                in_colon_table = True
                i += 1
                continue

        # Pipe-delimited table row (2+ pipes with real text)
        pipe_count = stripped.count('|')
        if pipe_count >= 2 and _has_real_text(stripped):
            flush_all()
            if in_colon_table:
                parts.append('</table></div>')
                in_colon_table = False
            if not in_pipe_table:
                parts.append('<div class="overflow-x-auto my-2"><table class="shop-table">')
                in_pipe_table = True
            cells = stripped.split('|')
            cells = [c.strip() for c in cells]
            # Remove outer padding empty cells
            while cells and not cells[-1]:
                cells.pop()
            while cells and not cells[0]:
                cells.pop(0)
            if cells:
                is_header = all(c.isupper() or not re.search(r'[a-zA-Z]', c) for c in cells if c.strip())
                tag = 'th' if is_header else 'td'
                parts.append('<tr>' + ''.join(f'<{tag}>{esc(c)}</{tag}>' for c in cells) + '</tr>')
            i += 1
            continue

        # Colon-delimited data row (3+ colons with digits) - auction house style
        if stripped.count(':') >= 3 and re.search(r'\d', stripped):
            flush_all()
            if in_pipe_table:
                parts.append('</table></div>')
                in_pipe_table = False
            if not in_colon_table:
                parts.append('<div class="overflow-x-auto my-2"><table class="shop-table">')
                parts.append('<tr><th></th><th>Item</th><th>Price Range</th><th>Average</th><th>Value</th></tr>')
                in_colon_table = True
            data = stripped
            group = ''
            gm = re.match(r'^(\[\d+\])\s*', data)
            if gm:
                group = gm.group(1)
                data = data[gm.end():]
            data = re.sub(r'^\|\s*', '', data)
            col_parts = [p.strip() for p in data.split(':')]
            if len(col_parts) >= 4:
                parts.append(f'<tr><td class="text-xs text-gray-500">{esc(group)}</td>'
                             f'<td>{esc(col_parts[0])}</td>'
                             f'<td>{esc(col_parts[1])}</td>'
                             f'<td>{esc(col_parts[2])}</td>'
                             f'<td>{esc(col_parts[3])}</td></tr>')
            i += 1
            continue

        # Regular text - accumulate, detecting bullet (* prefix) vs plain paragraph
        if in_pipe_table:
            parts.append('</table></div>')
            in_pipe_table = False
        if in_colon_table:
            parts.append('</table></div>')
            in_colon_table = False

        is_bullet = stripped.startswith('*')
        text = re.sub(r'^\*\s*', '', stripped)
        if not (text and re.search(r'[a-zA-Z]', text)):
            i += 1
            continue

        if is_bullet:
            # New bullet: complete any prior content first
            complete_current()
            current_is_bullet = True
            current_lines.append(text)
        elif current_lines:
            # Continuation of the current bullet (no blank line between)
            current_lines.append(text)
        else:
            # Stand-alone paragraph line
            flush_bullets()
            current_is_bullet = False
            current_lines.append(text)
        i += 1

    flush_all()
    if in_pipe_table:
        parts.append('</table></div>')
    if in_colon_table:
        parts.append('</table></div>')

    if parts:
        return '<div class="mt-2 space-y-1">' + '\n'.join(parts) + '</div>'
    return ''


def collect_config_box(lines, start):
    """Collect and format a config settings box. Returns (html, next_index)."""
    settings = []
    i = start + 1
    while i < len(lines):
        stripped = lines[i].strip()
        if re.match(r"^['\`][-]+", stripped):
            i += 1
            break
        clean = stripped.strip('|').strip()
        if clean and '>' in clean:
            settings.append(clean)
        i += 1

    html = '<div class="config-box">'
    html += '<div class="config-title">Configuration Settings</div>'
    html += '<ul class="list-disc list-inside mt-2 text-sm">'
    for setting in settings:
        html += f'<li>{esc(setting)}</li>'
    html += '</ul></div>'
    return html, i


# ============================================================================
# SHOP TABLE PARSER
# ============================================================================

def collect_shop_table(lines, start):
    """Collect and format a shop table block with Gil totals. Returns (html, next_index)."""
    block = []
    i = start
    seen_shop = False

    while i < len(lines):
        stripped = lines[i].strip()
        if stripped.startswith('o ') and '|' not in stripped and ':' not in stripped:
            break
        if re.search(r'BATTLE:\s*.*?\|.*?\(\s*\d+\s*AP\s*\)', stripped):
            break
        if re.match(r'.*\.--.*?/.+/.*--\.', stripped) and 'BATTLE' not in stripped:
            break
        if re.match(r'\s*\[TARGET', stripped):
            break
        # Only break on full-width segment borders (60+ =), not shop-width (30-40)
        if re.match(r'^={60,}$', stripped):
            break
        block.append(lines[i])
        # Track when we've seen SELL/BUY items
        if re.search(r'(?:SELL|BUY)\s*:', stripped):
            seen_shop = True
        # After shop items, stop at the closing --- line
        if seen_shop and re.match(r'^-{20,}(\s+-{20,})?$', stripped):
            # Verify we've actually passed through items (not the opening ---)
            items_before = any(re.search(r'(?:SELL|BUY)', b) for b in block[:-1])
            if items_before:
                i += 1
                break
        i += 1

    sell_items, buy_items = _parse_shop_items(block)

    # Extract Gil totals - pure number lines before/after items
    starting_gil = None
    remaining_gil = None
    first_item_idx = None
    last_item_idx = None
    for idx_b, bline in enumerate(block):
        bs = bline.strip()
        if re.search(r'(?:SELL|BUY)\s*:|^\s*:', bs) and re.search(r'[a-zA-Z]', bs):
            if first_item_idx is None:
                first_item_idx = idx_b
            last_item_idx = idx_b

    if first_item_idx is not None:
        # Look for number before first item
        for idx_b in range(first_item_idx):
            bs = block[idx_b].strip()
            if re.match(r'^[\d,]+$', bs):
                starting_gil = bs
        # Look for number after last item
        for idx_b in range(last_item_idx + 1, len(block)):
            bs = block[idx_b].strip()
            if re.match(r'^[\d,]+$', bs):
                remaining_gil = bs

    html = '<div class="my-4">'
    if starting_gil:
        html += f'<div class="gil-amount"><span class="label">Starting Gil: </span><span class="value">{esc(starting_gil)}</span></div>'
    if sell_items:
        html += '<div class="shop-box mb-3">'
        html += '<div class="shop-title mb-2">SELL</div>'
        html += '<table class="shop-table"><tr><th>Item</th><th>Gil</th></tr>'
        for item, price in sell_items:
            html += f'<tr><td>{esc(item)}</td><td>{esc(price)}</td></tr>'
        html += '</table></div>'
    if buy_items:
        html += '<div class="shop-box">'
        html += '<div class="shop-title mb-2">BUY</div>'
        html += '<table class="shop-table"><tr><th>Item</th><th>Gil</th></tr>'
        for item, price in buy_items:
            html += f'<tr><td>{esc(item)}</td><td>{esc(price)}</td></tr>'
        html += '</table></div>'
    if not sell_items and not buy_items:
        text = '\n'.join(l.rstrip() for l in block if l.strip())
        if text.strip():
            html += f'<pre class="text-sm text-gray-400 my-2">{esc(text)}</pre>'
    if remaining_gil:
        html += f'<div class="gil-amount"><span class="label">Remaining Gil: </span><span class="value">{esc(remaining_gil)}</span></div>'
    html += '</div>'
    return html, i


def _parse_shop_items(block):
    """Parse shop block into sell_items and buy_items lists of (name, price)."""
    sell_items = []
    buy_items = []
    # Track current mode for continuation lines (": item  price" without SELL/BUY)
    current_mode = None  # 'sell' or 'buy' — driven by the LEFT column in dual-col blocks
    left_col_mode = None   # mode for the left column of a dual-column block
    right_col_mode = None  # mode for the right column of a dual-column block

    for line in block:
        stripped = line.strip()
        if not re.search(r'[a-zA-Z]', stripped):
            continue

        if '|' in line:
            parts = re.split(r'\s+\|\s+', line, maxsplit=1)
            if len(parts) == 2:
                left, right = parts
            else:
                parts = line.split('|', 1)
                left, right = parts[0], parts[1] if len(parts) > 1 else ''
            # Dual-column: track each column's mode independently so the right
            # column (BUY) never corrupts the left column's (SELL) mode.
            for side, is_left in ((left, True), (right, False)):
                side_s = side.strip()
                if re.match(r'(?:SELL)\s*:', side_s, re.IGNORECASE):
                    _extract_shop_item(side_s, sell_items)
                    if is_left:
                        left_col_mode = 'sell'
                        current_mode = 'sell'
                    else:
                        right_col_mode = 'sell'
                elif re.match(r'(?:BUY)\s*:', side_s, re.IGNORECASE):
                    _extract_shop_item(side_s, buy_items)
                    if is_left:
                        left_col_mode = 'buy'
                        current_mode = 'buy'
                    else:
                        right_col_mode = 'buy'
                elif re.match(r'\s*:', side_s):
                    col_mode = left_col_mode if is_left else right_col_mode
                    target = buy_items if col_mode == 'buy' else sell_items
                    _extract_shop_item(side_s, target)
        else:
            # Single-column: detect mode from SELL/BUY keyword
            if re.match(r'(?:SELL)\s*:', stripped, re.IGNORECASE):
                _extract_shop_item(stripped, sell_items)
                current_mode = 'sell'
            elif re.match(r'(?:BUY)\s*:', stripped, re.IGNORECASE):
                _extract_shop_item(stripped, buy_items)
                current_mode = 'buy'
            elif re.match(r'\s*:', stripped):
                # Continuation line - use current mode
                target = buy_items if current_mode == 'buy' else sell_items
                _extract_shop_item(stripped, target)

    return sell_items, buy_items


def _extract_shop_item(text, items):
    """Extract a single shop item from one side of a table line."""
    if not text or not re.search(r'[a-zA-Z]', text):
        return
    if re.match(r'^[-=\s]+$', text):
        return
    text_clean = re.sub(r'^(?:SELL|BUY)\s*', '', text, flags=re.IGNORECASE).strip()
    # Match ": N Item Name   price" with optional trailing notes/decoration
    item_match = re.match(r':\s*(\d+\s+.+?)\s{2,}(\d[\d,]+)', text_clean)
    if item_match:
        item_text, price = item_match.groups()
        items.append((item_text.strip(), price.strip()))


# ============================================================================
# TABLE FORMATTER
# ============================================================================

def collect_bordered_table(lines, start):
    """Collect and format a bordered table (.===. style). Returns (html, next_index)."""
    table_lines = []
    i = start
    found_close = False
    while i < len(lines):
        table_lines.append(lines[i])
        stripped = lines[i].strip()
        if i > start and re.match(r"^['\`][-=]+", stripped):
            i += 1
            found_close = True
            break
        i += 1
        if len(table_lines) > 500:
            break

    all_rows = []
    num_cols = 0
    for line in table_lines:
        stripped = line.strip()
        if not re.search(r'[a-zA-Z0-9]', stripped):
            continue
        if '|' in stripped:
            cells = stripped.split('|')
            cells = [c.strip() for c in cells]
            # Remove exactly the outer empty cells from leading/trailing |
            if cells and not cells[0]:
                cells.pop(0)
            if cells and not cells[-1]:
                cells.pop()
            if cells:
                if num_cols == 0:
                    num_cols = len(cells)
                # Pad short rows (continuation rows with empty leading cells)
                while len(cells) < num_cols:
                    cells.insert(0, '')
                all_rows.append(cells)

    if not all_rows:
        return '', i

    html = '<div class="overflow-x-auto my-3"><table class="shop-table">'
    for idx, row in enumerate(all_rows):
        tag = 'th' if idx == 0 else 'td'
        html += '<tr>'
        for cell in row:
            html += f'<{tag}>{esc(cell)}</{tag}>'
        html += '</tr>'
    html += '</table></div>'
    return html, i


# ============================================================================
# SEGMENT CONTENT PARSER
# ============================================================================

def extract_treasures(lines):
    """Extract treasure items from the beginning of segment content."""
    treasures = []
    remaining = []
    treasure_re = re.compile(r'\[\]\s*([^[\]\n]+)')
    past_treasures = False

    for line in lines:
        stripped = line.strip()

        if not past_treasures:
            if re.match(r'^-{5,}$', stripped):
                continue
            if treasure_re.search(line):
                items = treasure_re.findall(line)
                for item in items:
                    item = item.strip()
                    if item and not re.match(r'^Item \d+$', item):
                        treasures.append(item)
                continue
            if stripped and not is_pure_decoration(stripped):
                past_treasures = True

        remaining.append(line)

    return treasures, remaining


def collect_pipe_table(lines, start):
    """Collect consecutive pipe-bordered rows into an HTML table. Returns (html, next_index)."""
    rows = []
    num_cols = 0
    i = start
    while i < len(lines):
        stripped = lines[i].strip()
        if re.match(r'^\s*\|', stripped) and stripped.rstrip().endswith('|'):
            # Skip separator rows (no letters or digits)
            if not re.search(r'[a-zA-Z0-9]', stripped):
                i += 1
                continue
            cells = stripped.split('|')
            cells = [c.strip() for c in cells]
            # Remove exactly the outer empty cells from leading/trailing |
            if cells and not cells[0]:
                cells.pop(0)
            if cells and not cells[-1]:
                cells.pop()
            if cells:
                if num_cols == 0:
                    num_cols = len(cells)
                # Pad short rows (continuation rows with empty leading cells)
                while len(cells) < num_cols:
                    cells.insert(0, '')
                rows.append(cells)
            i += 1
        elif not stripped:
            # Stop at blank lines to avoid bridging into next section
            break
        elif is_pure_decoration(stripped):
            i += 1
        else:
            break
    if not rows:
        return '', i
    html = '<div class="overflow-x-auto my-3"><table class="shop-table">'
    for idx, row in enumerate(rows):
        tag = 'th' if idx == 0 else 'td'
        html += '<tr>' + ''.join(f'<{tag}>{esc(c)}</{tag}>' for c in row) + '</tr>'
    html += '</table></div>'
    return html, i


def collect_config_inline(lines, start):
    """Collect consecutive | setting > value | lines. Returns (html, next_index)."""
    settings = []
    i = start
    while i < len(lines):
        stripped = lines[i].strip()
        if re.match(r'^\s*\|[^|]*>[^|]*\|\s*$', stripped):
            clean = stripped.strip('|').strip()
            if clean:
                settings.append(clean)
            i += 1
        elif is_pure_decoration(stripped) or not stripped:
            i += 1
        else:
            break
    if not settings:
        return '', i
    html = '<div class="config-box">'
    html += '<div class="config-title">Configuration Settings</div>'
    html += '<ul class="list-disc list-inside mt-2 text-sm">'
    for s in settings:
        html += f'<li>{esc(s)}</li>'
    html += '</ul></div>'
    return html, i


def _is_continuation(ns, lines, idx, in_list):
    """Check if a line is a continuation of current paragraph/instruction."""
    if not ns:
        return False
    if ns.startswith('o '):
        return False
    if is_pure_decoration(ns):
        return False
    if is_block_start(lines, idx):
        return False
    if re.match(r'\s*\[TARGET', ns):
        return False
    if 'TARGET TIME' in ns and 'TARGET GIL' in ns:
        return False
    if re.search(r'(?:SELL|BUY)\s*:', ns):
        return False
    if re.match(r'^\s*\|[^|]*>[^|]*\|\s*$', ns):
        return False
    if re.match(r'^\s*\|.*\|.*\|.*\|\s*$', ns) and ns.strip().startswith('|') and ns.strip().endswith('|'):
        return False
    return True


def _strip_side_panel(lines):
    """Detect and strip side-by-side equipment panels from instruction lines.

    Some sections have an ASCII art equipment box floating to the right of
    instruction text.  This pre-processor separates the two, returning cleaned
    instruction lines and an HTML snippet for the equipment table (inserted
    just before the first affected instruction).
    """
    # Detect the pattern: a .===. border appearing far to the right of a
    # content line (column > 40), indicating a side panel.
    panel_start = None
    panel_col = None
    for idx, line in enumerate(lines):
        m = re.search(r'\.\={5,}\.', line)
        if m and m.start() > 40:
            panel_start = idx
            panel_col = m.start()
            break

    if panel_start is None:
        return lines, '', -1

    # Walk forward from the detected panel start and collect the right-side
    # panel text while stripping it from the instruction lines.
    panel_right = []       # raw right-side strings (between pipes)
    cleaned = list(lines)  # will be mutated
    panel_end = None
    header_name = None

    for idx in range(panel_start, len(lines)):
        line = lines[idx]
        # Only process lines that are long enough to contain the panel
        if len(line) < panel_col:
            if panel_end is not None:
                break
            continue

        right = line[panel_col:]

        # Top/bottom borders or separator
        if re.match(r"^[\.\'\`\s>][-=]+[\.\'\`<>\s]*$", right.strip()):
            cleaned[idx] = line[:panel_col].rstrip()
            if re.match(r"^['\`]", right.strip()):
                panel_end = idx
                # clean this line and stop
                break
            continue

        # Content row: | text |
        rm = re.match(r'\|\s*(.*?)\s*\|', right.strip())
        if rm:
            cell = rm.group(1).strip()
            if header_name is None and cell:
                header_name = cell        # first row is the name/title
            elif cell:
                panel_right.append(cell)
            cleaned[idx] = line[:panel_col].rstrip()
            continue

        # If we already started and hit something that doesn't match, stop
        if panel_right:
            break

    if panel_end is not None:
        # Also strip the remaining line after panel_end
        cleaned[panel_end] = lines[panel_end][:panel_col].rstrip() if panel_end < len(lines) and len(lines[panel_end]) > panel_col else cleaned[panel_end]

    if not panel_right and not header_name:
        return lines, '', -1

    # Build a small equipment table
    equip_html = '<div class="overflow-x-auto my-3"><table class="shop-table">'
    if header_name:
        equip_html += f'<tr><th>{esc(header_name)}</th></tr>'
    for item in panel_right:
        equip_html += f'<tr><td>{esc(item)}</td></tr>'
    equip_html += '</table></div>'

    end = panel_end if panel_end is not None else (panel_start + len(panel_right) + 2)
    return cleaned, equip_html, end


def parse_segment_content(lines):
    """Parse segment content lines into HTML."""
    # Pre-process: strip any side-by-side equipment panels
    lines, side_panel_html, panel_end_idx = _strip_side_panel(lines)
    side_panel_emitted = not side_panel_html  # True if nothing to emit

    parts = []
    in_list = False
    i = 0

    while i < len(lines):
        stripped = lines[i].strip()

        # Inject side panel equipment table once we pass the affected lines
        if not side_panel_emitted and i > panel_end_idx:
            if in_list:
                parts.append('</ul>')
                in_list = False
            parts.append(side_panel_html)
            side_panel_emitted = True

        # ===== BLOCK DETECTIONS THAT LOOK LIKE DECORATION (must come first) =====

        # === BORDERED TABLE (.===.===. multi-section style) ===
        if re.match(r'^\s*\.=+\.=+\.', stripped):
            if in_list:
                parts.append('</ul>')
                in_list = False
            table_html, i = collect_bordered_table(lines, i)
            if table_html:
                parts.append(table_html)
            continue

        # === SHOP TABLE (--- line with SELL/BUY ahead) ===
        if re.match(r'^-{5,}(\s+-{5,})?$', stripped):
            if _has_shop_ahead(lines, i):
                if in_list:
                    parts.append('</ul>')
                    in_list = False
                shop_html, i = collect_shop_table(lines, i)
                parts.append(shop_html)
                continue

        # === CONFIG BOX (.----. opener) ===
        if re.match(r'^\s*\.[-]+\.\s*$', stripped):
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines) and '|' in lines[j] and '>' in lines[j]:
                if in_list:
                    parts.append('</ul>')
                    in_list = False
                box_html, i = collect_config_box(lines, i)
                parts.append(box_html)
                continue

        # ===== NOW FILTER PURE DECORATION =====
        if is_pure_decoration(stripped):
            # Before skipping, check if this is a single-column table border (.====.)
            if re.match(r'^\s*\.[=]+\.\s*$', stripped):
                j = i + 1
                while j < len(lines) and not lines[j].strip():
                    j += 1
                if j < len(lines) and re.match(r'^\s*\|', lines[j].strip()) and lines[j].strip().rstrip().endswith('|'):
                    if not re.search(r'BATTLE:', lines[j]) and not re.search(r'\.--', lines[j]):
                        if in_list:
                            parts.append('</ul>')
                            in_list = False
                        table_html, i = collect_bordered_table(lines, i)
                        if table_html:
                            parts.append(table_html)
                        continue
            i += 1
            continue

        # ===== CONTENT DETECTION =====

        # === BATTLE BOX ===
        if re.search(r'BATTLE:\s*.*?\|.*?\(\s*\d+\s*AP\s*\)', stripped):
            if in_list:
                parts.append('</ul>')
                in_list = False
            box_html, i = collect_battle_box(lines, i)
            parts.append(box_html)
            continue

        # === INFO/DETOUR BOX ===
        if re.match(r'.*\.--.*?/.+/.*--\.', stripped) and 'BATTLE' not in stripped:
            if in_list:
                parts.append('</ul>')
                in_list = False
            box_html, i = collect_info_box(lines, i)
            parts.append(box_html)
            continue

        # === DIRECT SHOP (SELL/BUY lines) ===
        if re.search(r'(?:SELL|BUY)\s*:', stripped):
            if in_list:
                parts.append('</ul>')
                in_list = False
            shop_html, i = collect_shop_table(lines, i)
            parts.append(shop_html)
            continue

        # === INLINE CONFIG (| setting > value |) ===
        if re.match(r'^\s*\|[^|]*>[^|]*\|\s*$', stripped):
            if in_list:
                parts.append('</ul>')
                in_list = False
            cfg_html, i = collect_config_inline(lines, i)
            if cfg_html:
                parts.append(cfg_html)
            continue

        # === PIPE-BORDERED TABLE (| col | col | col |) ===
        if re.match(r'^\s*\|.*\|.*\|.*\|\s*$', stripped) and stripped.startswith('|') or (stripped.lstrip().startswith('|') and stripped.rstrip().endswith('|') and stripped.count('|') >= 4):
            if in_list:
                parts.append('</ul>')
                in_list = False
            tbl_html, i = collect_pipe_table(lines, i)
            if tbl_html:
                parts.append(tbl_html)
            continue

        # === PATH LABEL (----( PATH A )----) ===
        path_label_match = re.match(r'^[-\s]*\(\s*(.+?)\s*\)[-\s]*$', stripped)
        if path_label_match and re.search(r'^[-]+', stripped):
            label = path_label_match.group(1).strip()
            if in_list:
                parts.append('</ul>')
                in_list = False
            parts.append(f'<div class="path-label">{esc(label)}</div>')
            i += 1
            # Skip following ¯¯¯¯ underline if present
            if i < len(lines) and re.match(r'^[¯\s]+$', lines[i].strip() or ' '):
                i += 1
            continue

        # === TARGET TIME MARKER ===
        target_match = re.match(r'\s*\[TARGET TIME:\s*([\d:]+)\]', stripped)
        if target_match:
            if in_list:
                parts.append('</ul>')
                in_list = False
            parts.append(f'<div class="target-marker">TARGET TIME: {target_match.group(1)}</div>')
            i += 1
            continue

        # === TARGET SUMMARY (skip, rendered in segment wrapper) ===
        if 'TARGET TIME' in stripped and 'TARGET GIL' in stripped:
            i += 1
            continue

        # === INSTRUCTION LINE (o ...) ===
        if stripped.startswith('o '):
            if not in_list:
                parts.append('<ul class="instruction-list">')
                in_list = True
            text = stripped[2:]
            i += 1
            while i < len(lines):
                ns = lines[i].strip()
                if not _is_continuation(ns, lines, i, in_list):
                    break
                text += ' ' + ns
                i += 1
            parts.append(f'<li>{esc(text)}</li>')
            continue

        # === REGULAR PARAGRAPH ===
        if in_list:
            parts.append('</ul>')
            in_list = False

        para = [stripped]
        i += 1
        while i < len(lines):
            ns = lines[i].strip()
            if not _is_continuation(ns, lines, i, in_list):
                break
            para.append(ns)
            i += 1
        parts.append(f'<p>{esc(" ".join(para))}</p>')

    if in_list:
        parts.append('</ul>')

    if not side_panel_emitted:
        parts.append(side_panel_html)

    return '\n'.join(parts)


# ============================================================================
# SEGMENT BUILDER
# ============================================================================

def build_segment_html(segment):
    """Build complete HTML for a walkthrough segment."""
    segment_id = segment['id']
    title = segment['title']
    raw_lines = segment['content']

    treasures, content_lines = extract_treasures(raw_lines)

    html = f'<div id="{segment_id}" class="segment-box">'
    html += '<button class="foldable-header collapsed">'
    html += '<div class="segment-title-container"><input type="checkbox" onclick="event.stopPropagation()">'
    html += f'<span class="segment-title">{esc(title)} <span class="segment-code">({segment_id})</span></span></div>'
    html += '<svg class="arrow-icon w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"></path></svg></button>'
    html += '<div class="foldable-content collapsed">'

    if treasures:
        html += '<h4 class="font-bold text-gray-400 mt-4 mb-2">Treasure Checklist:</h4>'
        html += '<div class="treasure-list">'
        for item in treasures:
            html += f'<div class="checklist-item"><input type="checkbox"><span>{esc(item)}</span></div>'
        html += '</div>'

    html += '<div class="mt-4">'
    html += parse_segment_content(content_lines)
    html += '</div>'
    html += '</div>'  # foldable-content

    summary = segment.get('summary')
    if summary and summary.get('time'):
        html += '<div class="target-summary">'
        html += f'<div><span class="text-gray-400">TARGET TIME:</span><br>{esc(summary.get("time", "N/A"))}</div>'
        html += f'<div><span class="text-gray-400">TARGET GIL:</span><br>{esc(summary.get("gil", "N/A"))}</div>'
        html += f'<div><span class="text-gray-400">ENCOUNTERS:</span><br>{esc(summary.get("encounters", "N/A"))}</div>'
        html += '</div>'

    html += '</div>'  # segment-box
    return html


# ============================================================================
# PRELIMINARIES FORMATTER
# ============================================================================

def format_preliminaries(text):
    """Format the introductory sections before the walkthrough."""
    lines = text.split('\n')
    html = '<div class="preliminaries-content">'

    # Find ASCII art end (after author info)
    ascii_end = 0
    for idx, line in enumerate(lines):
        if 'Atomos199' in line and idx > 10:
            for j in range(idx, min(idx + 10, len(lines))):
                if re.search(r'Version\s+X', lines[j]):
                    ascii_end = j + 3
                    break
            if ascii_end > 0:
                break

    if ascii_end > 0:
        ascii_block = '\n'.join(lines[:ascii_end])
        html += f'<pre class="ascii-art">{esc(ascii_block)}</pre>'

    i = ascii_end
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        # === SLASH-TITLED INFO/DETOUR BOX (.--/ Title /...--.) ===
        if re.match(r'.*\.--.*?/.+/.*--\.', stripped) and 'BATTLE' not in stripped:
            box_html, i = collect_info_box(lines, i)
            html += box_html
            continue

        # === SHOP BLOCK (SELL/BUY lines) ===
        if re.search(r'(?:SELL|BUY)\s*:', stripped):
            shop_html, i = collect_shop_table(lines, i)
            html += shop_html
            continue

        # === QUESTION HEADER (text followed by ¯¯¯ underline) ===
        if i + 1 < len(lines) and stripped.endswith('?') and re.match(r'^[¯]+\s*$', lines[i+1].strip()):
            html += f'<h4 class="text-gray-300 font-semibold mt-4 mb-2">{esc(stripped)}</h4>'
            i += 2  # skip the ¯¯¯ underline
            continue

        # === BORDERED TEXT BOX (Version notice, PAL notice, titled boxes) ===
        if re.match(r'^\s*\.[-]+[\(\[]', stripped) or (re.match(r'^\s*\.[-]+\.\s*$', stripped) and i + 1 < len(lines) and lines[i+1].strip().startswith('|')):
            # Extract title if present: .--( Title )----.
            box_title = ''
            title_m = re.search(r'\(\s*(.+?)\s*\)', stripped)
            if title_m and not re.match(r'^\s*\.[-]+\.\s*$', stripped):
                box_title = title_m.group(1).strip()
            box_content = []
            i += 1
            while i < len(lines):
                bs = lines[i].strip()
                if re.match(r"^['\`][-]+['\`\.]$", bs):
                    i += 1
                    break
                clean = re.sub(r'^\s*\|\s*', '', lines[i])
                clean = re.sub(r'\s*\|\s*$', '', clean).strip()
                # Skip decoration/underlines (¯¯¯ lines, etc.)
                if clean and not is_pure_decoration(clean) and not re.match(r'^[¯_~\-=]+$', clean):
                    box_content.append(clean)
                i += 1
            if box_content:
                # Join consecutive lines into paragraphs (split on empty-ish gaps)
                paragraphs = []
                current = []
                for bc in box_content:
                    if not bc:
                        if current:
                            paragraphs.append(' '.join(current))
                            current = []
                    else:
                        current.append(bc)
                if current:
                    paragraphs.append(' '.join(current))
                html += '<div class="extras-box">'
                if box_title:
                    html += f'<div class="font-semibold text-gray-300 mb-2">{esc(box_title)}</div>'
                for para in paragraphs:
                    html += f'<p class="text-sm">{esc(para)}</p>'
                html += '</div>'
            continue

        # === TABLE OF CONTENTS DETECTION ===
        # Detect the decorated ToC banner: .===. / ==='...| TABLE OF CONTENTS |...'=== / .===.
        if 'TABLE OF CONTENTS' in stripped:
            html += '<h2 class="section-header text-center">Table of Contents</h2>'
            # Skip past any remaining decoration on this line and the close decoration
            i += 1
            while i < len(lines) and is_pure_decoration(lines[i].strip()):
                i += 1
            # Now collect ToC entries (roman numeral + title + code)
            toc_entries = []
            while i < len(lines):
                ts = lines[i].strip()
                # ToC entry: "I. Introduction . . . . . . .(A00)" — dots can be space-separated
                toc_m = re.match(r'^([IVXL]+)\.\s+(.+?)[\s.]+\(([A-Z]\d\d)\)\s*$', ts)
                if toc_m:
                    num, title_raw, code = toc_m.groups()
                    toc_entries.append({'num': num, 'title': title_raw.strip().rstrip('.').strip(), 'code': code, 'sub': False})
                    i += 1
                    continue
                # Sub-entries: "1. Disc 1....(F01)"
                sub_m = re.match(r'^(\d+)\.\s+(.+?)[\s.]+\(([A-Z]\d\d)\)\s*$', ts)
                if sub_m:
                    snum, stitle, scode = sub_m.groups()
                    toc_entries.append({'num': snum, 'title': stitle.strip(), 'code': scode, 'sub': True})
                    i += 1
                    continue
                if not ts or is_pure_decoration(ts):
                    i += 1
                    # Check if we've passed all ToC entries
                    if toc_entries and i < len(lines):
                        next_ts = lines[i].strip() if i < len(lines) else ''
                        if next_ts and not re.match(r'^[IVXL]+\.', next_ts) and not re.match(r'^\d+\.', next_ts) and not is_pure_decoration(next_ts) and next_ts:
                            break
                    continue
                break
            if toc_entries:
                html += '<ul class="toc-nav">'
                for entry in toc_entries:
                    sub_class = ' toc-sub' if entry['sub'] else ''
                    prefix = f'{entry["num"]}.' if not entry['sub'] else f'&nbsp;&nbsp;{entry["num"]}.'
                    html += f'<li class="{sub_class.strip()}">'
                    html += f'<span class="toc-num">{prefix}</span>'
                    html += f'<span class="toc-title">{esc(entry["title"])}</span>'
                    html += f'<span class="toc-code">({entry["code"]})</span>'
                    html += '</li>'
                html += '</ul>'
            continue

        # === EXAMPLE WALKTHROUGH SEGMENT (illustrative pre-formatted block) ===
        # The "USING THIS GUIDE" section has a sample segment showing readers
        # what walkthrough content looks like.  Detect it by the (DX-XX) dummy
        # code and render the whole block as <pre> so none of the example
        # content triggers real formatters.
        if re.match(r'^=+$', stripped) and stripped.count('=') >= 10:
            is_example = False
            for look in range(1, 4):
                if i + look < len(lines) and '(DX-XX)' in lines[i + look]:
                    is_example = True
                    break
            if is_example:
                # Collect all example lines up to the final annotation
                example_lines = []
                j = i
                while j < len(lines):
                    example_lines.append(lines[j])
                    if '[time needed for this segment]' in lines[j]:
                        j += 1
                        break
                    j += 1
                while example_lines and not example_lines[-1].strip():
                    example_lines.pop()
                while j < len(lines) and not lines[j].strip():
                    j += 1
                i = j

                # --- Parse the example block into structured HTML ---
                ex_i = 0
                while ex_i < len(example_lines) and not example_lines[ex_i].strip():
                    ex_i += 1

                # Extract header from === / * TITLE * / ===
                header_title = ''
                while ex_i < len(example_lines):
                    s = example_lines[ex_i].strip()
                    if re.match(r'^=+$', s):
                        ex_i += 1
                        continue
                    tm = re.match(r'^\*\s*(.*?)\s*\*$', s)
                    if tm:
                        header_title = tm.group(1).strip()
                        ex_i += 1
                        continue
                    break
                while ex_i < len(example_lines) and not example_lines[ex_i].strip():
                    ex_i += 1

                # Extract checklist items from --- / [] Item rows / ---
                checklist_items = []
                while ex_i < len(example_lines):
                    s = example_lines[ex_i].strip()
                    if re.match(r'^-+$', s):
                        ex_i += 1
                        continue
                    if '[] ' in s:
                        items = re.findall(r'\[\]\s+(\S+(?:\s+\S+)*?)(?=\s{2,}\[\]|$)', s)
                        checklist_items.extend(items)
                        ex_i += 1
                        continue
                    break

                # Remaining lines -> content
                content_lines = list(example_lines[ex_i:])

                # Pre-process: make placeholder values parseable
                processed = []
                for cline in content_lines:
                    cline = cline.replace('(X AP)', '(0 AP)')
                    if '[TARGET TIME:' in cline and 'xx:xx:xx' in cline:
                        cline = cline.replace('xx:xx:xx', '00:00:00')
                        if '<-' in cline:
                            parts = cline.split('<-', 1)
                            processed.append(parts[0].rstrip())
                            processed.append('  ← ' + parts[1].strip())
                            continue
                    processed.append(cline)
                content_lines = processed

                # Parse content through the segment parser
                inner_html = parse_segment_content(content_lines)

                # Post-process: style annotation callouts
                # '-- [text]  (apostrophe escaped to &#x27;)
                inner_html = re.sub(
                    r"<p>&#x27;-- (.+?)</p>",
                    '<div class="example-annotation">← \\1</div>',
                    inner_html
                )
                # <- [text]  (angle bracket escaped to &lt;)
                inner_html = re.sub(
                    r"<p>\s*&lt;- (.+?)</p>",
                    '<div class="example-annotation">← \\1</div>',
                    inner_html
                )
                # ← [text]  (from our pre-processing)
                inner_html = re.sub(
                    r'<p>\s*← (.+?)</p>',
                    '<div class="example-annotation">← \\1</div>',
                    inner_html
                )
                # Remove orphaned ^ paragraphs (annotation arrows)
                inner_html = re.sub(r'<p>\^</p>', '', inner_html)

                # Build example container
                html += '<div class="example-segment">'
                html += '<div class="example-segment-label">Sample Walkthrough Segment</div>'
                html += '<div class="example-segment-body">'

                # Segment-style header
                if header_title:
                    html += f'<div class="example-segment-header">{esc(header_title)}</div>'

                # Treasure checklist
                if checklist_items:
                    html += '<div class="treasure-list mb-4">'
                    for ci in checklist_items:
                        html += f'<div class="checklist-item"><input type="checkbox" disabled><span>{esc(ci)}</span></div>'
                    html += '</div>'

                # Parsed content
                html += '<div class="mt-4">'
                html += inner_html
                html += '</div>'

                html += '</div></div>'
                continue

        # === DECORATED SECTION HEADER ===
        # Pattern: .=====. / ==='...'=== / * | TITLE | (A00) * / ==='.  .'=== / '====='
        # The === lines may contain apostrophes, dots, spaces
        # Exclude multi-column table borders like .===.===.===. (3+ dots)
        if re.match(r'^[=\s\'.\.]+$', stripped) and stripped.count('=') >= 10 and stripped.count('.') <= 2:
            # Scan ahead for the * | TITLE | (code) * line within 3 lines
            found_header = False
            for look in range(1, 4):
                if i + look >= len(lines):
                    break
                next_s = lines[i + look].strip()
                title_m = re.match(r'^\s*[\*o]\s*(.*?)\s*\(([A-Z]\d\d)\)\s*[\*o]$', next_s)
                if title_m:
                    title_text = title_m.group(1).strip()
                    pipe_m = re.search(r'\|\s*(.+?)\s*\|', title_text)
                    if pipe_m:
                        title_text = pipe_m.group(1).strip()
                    html += f'<h2 class="section-header">{esc(title_text)}</h2>'
                    i += look + 1
                    while i < len(lines) and (re.match(r'^[=\s\'.\.]+$', lines[i].strip()) or is_pure_decoration(lines[i].strip())):
                        i += 1
                    found_header = True
                    break
                # Skip decoration lines while looking
                if is_pure_decoration(next_s) or re.match(r'^[=\s\'.\.]+$', next_s):
                    continue
                break
            if found_header:
                continue
            i += 1
            continue

        # === SECTION HEADER LINE: * | TITLE | (A00) * (standalone, no === before) ===
        standalone_m = re.match(r'^\s*[\*o]\s*(.*?)\s*\(([A-Z]\d\d)\)\s*[\*o]$', stripped)
        if standalone_m:
            title_text = standalone_m.group(1).strip()
            pipe_m = re.search(r'\|\s*(.+?)\s*\|', title_text)
            if pipe_m:
                title_text = pipe_m.group(1).strip()
            html += f'<h2 class="section-header">{esc(title_text)}</h2>'
            i += 1
            while i < len(lines) and (re.match(r'^[=\s\'.\.]+$', lines[i].strip()) or is_pure_decoration(lines[i].strip())):
                i += 1
            continue

        # === MAJOR SECTION HEADER (* TITLE *) ===
        section_match = re.match(r'^\s*\*\s*(.*?)\s*\*\s*$', stripped)
        if section_match and not re.search(r'\([A-Z]\d\d\)', stripped) and not re.search(r'\(D\d-\d\d\)', stripped):
            title_text = section_match.group(1).strip()
            # strip pipe decoration from title
            pipe_m = re.search(r'\|\s*(.+?)\s*\|', title_text)
            if pipe_m:
                title_text = pipe_m.group(1).strip()
            if title_text and len(title_text) > 3:
                html += f'<h2 class="section-header">{esc(title_text)}</h2>'
                i += 1
                while i < len(lines) and re.match(r'^[=\s]+$', lines[i].strip()):
                    i += 1
                continue

        # === NUMBERED RULE: .===.----. | N | Title | '==='.----' ===
        if re.match(r"^\s*\.===\.", stripped):
            if i + 1 < len(lines) and '|' in lines[i+1]:
                header_line = lines[i+1].strip()
                header_parts = [p.strip() for p in header_line.split('|') if p.strip()]
                if len(header_parts) >= 2:
                    num = header_parts[0]
                    title_text = header_parts[1]
                    html += f'<h3 class="subsection-header">{esc(num)}. {esc(title_text)}</h3>'
                elif header_parts:
                    html += f'<h3 class="subsection-header">{esc(header_parts[0])}</h3>'
                i += 2
                while i < len(lines) and (re.match(r"^[\s'\`=\-\.]+$", lines[i].strip()) or not lines[i].strip()):
                    i += 1
                continue

        # === LINK TABLE (.===.----.) ===
        if re.match(r'^\s*\.=+\.[-]+\.\s*$', stripped):
            links = []
            i += 1
            while i < len(lines):
                ls = lines[i].strip()
                if '|' in ls and re.search(r'[a-zA-Z]', ls):
                    link_parts = [p.strip() for p in ls.split('|') if p.strip()]
                    if len(link_parts) >= 2:
                        links.append((link_parts[0], link_parts[1]))
                    i += 1
                elif re.match(r"^[\s'\`=\-\.]+$", ls) or not ls:
                    i += 1
                    if re.match(r"^\s*\.=+\.", ls if ls else ''):
                        continue
                    if not ls:
                        continue
                    if i < len(lines) and re.match(r'^\s*\.=+\.', lines[i].strip()):
                        i += 1
                        continue
                    break
                else:
                    break
            if links:
                html += '<div class="overflow-x-auto my-4"><table class="shop-table">'
                html += '<tr><th>Name</th><th>Link</th></tr>'
                for name, url in links:
                    html += f'<tr><td>{esc(name)}</td><td><a href="{esc(url)}" class="text-blue-400 hover:underline" target="_blank">{esc(url)}</a></td></tr>'
                html += '</table></div>'
            continue

        # === TABLE with | separators and . borders ===
        if re.match(r'^\s*\.[=\-]+\.', stripped) and i + 1 < len(lines) and '|' in lines[i+1]:
            table_html, i = collect_bordered_table(lines, i)
            if table_html:
                html += table_html
            continue

        # === PURE DECORATION ===
        if is_pure_decoration(stripped):
            i += 1
            continue

        # === INLINE CONFIG (| setting > value |) ===
        if re.match(r'^\s*\|[^|]*>[^|]*\|\s*$', stripped):
            cfg_html, i = collect_config_inline(lines, i)
            if cfg_html:
                html += cfg_html
            continue

        # === PIPE-BORDERED TABLE (| col | col | col |) ===
        if stripped.lstrip().startswith('|') and stripped.rstrip().endswith('|') and stripped.count('|') >= 4:
            tbl_html, i = collect_pipe_table(lines, i)
            if tbl_html:
                html += tbl_html
            continue

        # === BULLET LIST ===
        if stripped.startswith('•') or stripped.startswith('o ') or (stripped.startswith('- ') and len(stripped) > 2):
            html += '<ul class="list-disc list-inside my-2 space-y-1">'
            while i < len(lines):
                bs = lines[i].strip()
                if bs.startswith('•') or bs.startswith('o ') or (bs.startswith('- ') and len(bs) > 2):
                    item_text = re.sub(r'^[•o\-]\s*', '', bs)
                    html += f'<li class="text-sm">{esc(item_text)}</li>'
                    i += 1
                elif not bs:
                    i += 1
                    break
                elif is_pure_decoration(bs):
                    i += 1
                    continue
                else:
                    break
            html += '</ul>'
            continue

        # === NUMBERED LIST ===
        if re.match(r'^\d+\.', stripped):
            html += '<ol class="list-decimal list-inside my-2 space-y-1">'
            while i < len(lines):
                ns = lines[i].strip()
                if re.match(r'^\d+\.', ns):
                    item_text = re.sub(r'^\d+\.\s*', '', ns)
                    i += 1
                    while i < len(lines) and lines[i].strip() and not re.match(r'^\d+\.', lines[i].strip()) and not is_pure_decoration(lines[i].strip()):
                        item_text += ' ' + lines[i].strip()
                        i += 1
                    html += f'<li class="text-sm">{esc(item_text)}</li>'
                elif not ns:
                    i += 1
                    break
                else:
                    break
            html += '</ol>'
            continue

        # === QUOTATION ===
        if stripped.startswith('"'):
            quote_lines = [stripped]
            i += 1
            while i < len(lines) and lines[i].strip():
                quote_lines.append(lines[i].strip())
                i += 1
            html += f'<blockquote class="border-l-4 border-gray-600 pl-4 my-3 italic text-gray-400">{esc(" ".join(quote_lines))}</blockquote>'
            continue

        # === REGULAR PARAGRAPH ===
        para = [stripped]
        i += 1
        while i < len(lines):
            ns = lines[i].strip()
            if not ns:
                break
            if is_pure_decoration(ns):
                break
            if re.match(r'^\s*\*\s*.+\s*\*\s*$', ns):
                break
            if re.match(r'^\s*\.===', ns):
                break
            if re.match(r'^=+$', ns):
                break
            if re.match(r'.*\.--.*?/.+/.*--\.', ns):
                break
            if re.search(r'(?:SELL|BUY)\s*:', ns):
                break
            if ns.startswith('•') or ns.startswith('o ') or ns.startswith('- '):
                break
            if re.match(r'^\d+\.', ns):
                break
            if ns.startswith('"'):
                break
            if ns.lstrip().startswith('|') and ns.rstrip().endswith('|'):
                break
            if re.match(r'^\s*\.[-]+', ns):
                break
            if re.match(r'^¯+\s*$', ns):
                break
            para.append(ns)
            i += 1
        html += f'<p class="mb-3">{esc(" ".join(para))}</p>'

    html += '</div>'
    return html


# ============================================================================
# EXTRAS (POST-WALKTHROUGH) FORMATTER
# ============================================================================

def format_extras(sections):
    """Format post-walkthrough sections."""
    html = ''
    for section in sections:
        code = section['code']
        title = section['title']
        content_lines = section['content']

        html += f'<div class="segment-box" id="section-{code}">'
        html += '<button class="foldable-header collapsed">'
        html += '<div class="segment-title-container">'
        html += f'<span class="segment-title">{esc(title)} <span class="segment-code">({code})</span></span></div>'
        html += '<svg class="arrow-icon w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"></path></svg></button>'
        html += '<div class="foldable-content collapsed">'
        if code == 'K00':
            html += _format_credits(content_lines)
        else:
            html += _format_extras_content(content_lines)
        html += '</div></div>'

    return html


def _format_credits(lines):
    """Format the Credits section, preserving ASCII art tribute blocks."""
    parts = []
    i = 0

    while i < len(lines):
        stripped = lines[i].strip()

        if not stripped:
            i += 1
            continue

        # === PURE DECORATION ===
        # Don't skip yet — check if a tribute block follows immediately
        if is_pure_decoration(stripped):
            # But if this IS a multi-column table border, don't treat as pre-tribute
            if re.match(r'^\s*\.[=\-]+[\.\|]', stripped) and stripped.count('.') >= 3:
                # Let it fall through to the bordered table handler below
                pass
            else:
                # Look ahead: if a tribute line follows within 3 lines, include this as part of that block
                is_pre_tribute = False
                for look in range(1, 4):
                    if i + look < len(lines):
                        ls = lines[i + look].strip()
                        if not ls or is_pure_decoration(ls):
                            continue
                        if _is_tribute_line(lines[i + look]):
                            is_pre_tribute = True
                        break
                if not is_pre_tribute:
                    i += 1
                    continue
                # Fall through to the tribute collector below

        # === CREDIT SEPARATOR (- - - - - - -) ===
        if re.match(r'^[\-\s]+$', stripped) and stripped.count('-') >= 10 and stripped.count(' ') >= 5:
            parts.append('<hr class="credit-separator">')
            i += 1
            continue

        # === SUBHEADING with underline (Title + ¯¯¯) ===
        if i + 1 < len(lines) and re.match(r'^\s*¯+\s*$', lines[i + 1].strip()) and re.search(r'[a-zA-Z]', stripped):
            parts.append(f'<h4 class="text-lg font-semibold text-gray-300 mt-4 mb-2">{esc(stripped)}</h4>')
            i += 2
            continue

        # === ASCII ART TRIBUTE BLOCK ===
        # Detect side-by-side layout: lines with art on left + text on right
        # Once we find a tribute line, collect everything up to the next
        # credit separator (- - - -) or bordered table, since single-line
        # heuristic misses art-only lines inside a tribute.
        # Also enters here when is_pure_decoration fell through (pre-tribute art).
        is_table_border = re.match(r'^\s*\.[=\-]+[\.\|]', stripped) and stripped.count('.') >= 3
        if _is_tribute_line(lines[i]) or (is_pure_decoration(stripped) and not stripped.startswith('•') and not is_table_border):
            tribute_lines = []
            while i < len(lines):
                raw = lines[i]
                rs = raw.strip()
                # Stop at credit separator
                if re.match(r'^[\-\s]+$', rs) and rs.count('-') >= 10 and rs.count(' ') >= 5:
                    break
                # Stop at multi-column bordered table (3+ dots = column separators)
                if re.match(r'^\s*\.[=\-]+[\.\|]', rs) and rs.count('.') >= 3 and i + 1 < len(lines) and '|' in lines[i + 1]:
                    break
                # Stop at bullet list
                if rs.startswith('•'):
                    break
                # Include any line (tribute, art-only, blanks, decoration — all part of the block)
                tribute_lines.append(raw.rstrip())
                i += 1

            # Extract name from the tribute lines (look for ( • Name • ) pattern)
            tribute_name = ''
            for tl in tribute_lines:
                nm = re.search(r'\(\s*•\s*(.+?)\s*•?\s*\)', tl)
                if nm:
                    tribute_name = nm.group(1).strip()
                    break

            # Trim leading/trailing blank lines
            while tribute_lines and not tribute_lines[0].strip():
                tribute_lines.pop(0)
            while tribute_lines and not tribute_lines[-1].strip():
                tribute_lines.pop()

            if tribute_lines:
                parts.append('<div class="credit-tribute">')
                parts.append(f'<pre>{esc(chr(10).join(tribute_lines))}</pre>')
                if tribute_name:
                    parts.append(f'<div class="tribute-name">{esc(tribute_name)}</div>')
                parts.append('</div>')
            else:
                # Nothing collected — skip the current line to avoid infinite loop
                i += 1
            continue

        # === BORDERED TABLE (contributor names) ===
        if re.match(r'^\s*\.[=\-]+[\.\|]', stripped) and i + 1 < len(lines) and '|' in lines[i + 1]:
            table_html, i = collect_bordered_table(lines, i)
            if table_html:
                parts.append(table_html)
            continue

        # === BULLET LIST (• credits) ===
        if stripped.startswith('•') or (stripped.startswith('- ') and not re.search(r'\[[FCR\*]\]', stripped)):
            items = []
            while i < len(lines):
                ls = lines[i].strip()
                if ls.startswith('•') or (ls.startswith('- ') and not re.search(r'\[[FCR\*]\]', ls)):
                    item_text = re.sub(r'^[•\-]\s*', '', ls)
                    i += 1
                    while i < len(lines) and lines[i].strip() and not lines[i].strip().startswith('•') and not lines[i].strip().startswith('- ') and not is_pure_decoration(lines[i].strip()) and not re.match(r'^[\-\s]+$', lines[i].strip()):
                        item_text += ' ' + lines[i].strip()
                        i += 1
                    items.append(item_text)
                elif not ls:
                    i += 1
                    # Check if more bullets follow
                    if i < len(lines) and (lines[i].strip().startswith('•') or lines[i].strip().startswith('- ')):
                        continue
                    break
                elif is_pure_decoration(ls):
                    i += 1
                    continue
                else:
                    break
            if items:
                parts.append('<ul class="list-disc list-inside my-2 space-y-1">')
                for item in items:
                    parts.append(f'<li class="text-sm">{esc(item)}</li>')
                parts.append('</ul>')
            continue

        # === REGULAR PARAGRAPH ===
        para = [stripped]
        i += 1
        while i < len(lines):
            ns = lines[i].strip()
            if not ns:
                break
            if is_pure_decoration(ns):
                break
            if ns.startswith('•') or ns.startswith('- '):
                break
            if re.match(r'^[\-\s]+$', ns) and ns.count('-') >= 10:
                break
            if re.match(r'^\s*\.[=\-]+', ns):
                break
            if _is_tribute_line(lines[i]):
                break
            para.append(ns)
            i += 1
        parts.append(f'<p class="mb-3">{esc(" ".join(para))}</p>')

    return '\n'.join(parts)


def _is_tribute_line(line):
    """Check if a line is part of a side-by-side ASCII art tribute block."""
    raw = line.rstrip()
    if len(raw) < 30:
        return False
    # Must have a gap of 4+ spaces between non-space segments
    if not re.search(r'\S\s{4,}\S', raw):
        return False
    # Must have some special characters (art) AND some letters (text)
    has_special = bool(re.search(r'[|/\\_()\[\]#\*\.\'`{}~<>^]', raw))
    has_text = bool(re.search(r'[a-zA-Z]{2,}', raw))
    return has_special and has_text


def _collect_stat_table(lines, start):
    """Parse a Perfect Stats equipment table block.

    Expected format:
      .==========.
      | PATH A           | SPR  :   50 | STR  :   77 | MAG  :   61 | SPD  :   34 |
      .==========.
      | *T | -      : Ritual Hat  : Bone Wrist  : Survival V. : Black Belt  |
      ...
      '----------'

    Returns (html, next_index).
    """
    i = start
    path_name = ''
    stats = {}
    equip_rows = []

    # Skip opening .====. border
    while i < len(lines) and is_pure_decoration(lines[i].strip()):
        i += 1

    # Parse header row: | PATH X | SPR : N | STR : N | MAG : N | SPD : N |
    if i < len(lines):
        header = lines[i].strip()
        cells = [c.strip() for c in header.split('|')]
        cells = [c for c in cells if c]  # remove empty edge pieces
        if cells:
            path_name = cells[0]
            for cell in cells[1:]:
                m = re.match(r'(SPR|STR|MAG|SPD)\s*:\s*([\d\?]+)', cell)
                if m:
                    stats[m.group(1)] = m.group(2)
        i += 1

    # Skip middle .====. border
    while i < len(lines) and is_pure_decoration(lines[i].strip()):
        i += 1

    # Collect equipment rows until closing ' border
    while i < len(lines):
        s = lines[i].strip()
        if re.match(r"^['\`][-=]+", s):
            i += 1
            break
        if not s or is_pure_decoration(s):
            i += 1
            continue
        if s.startswith('|') and s.endswith('|'):
            inner = s[1:-1]  # strip outer | chars
            if '|' in inner:
                lvl_raw, equip_raw = inner.split('|', 1)
                lvl_code = lvl_raw.strip()
                equip_items = [e.strip() for e in equip_raw.split(':')]
            else:
                lvl_code = ''
                equip_items = [e.strip() for e in inner.split(':')]
            equip_rows.append((lvl_code, equip_items))
        i += 1

    if not path_name:
        return '', i

    stat_cls = {'SPR': 'spr', 'STR': 'str', 'MAG': 'mag', 'SPD': 'spd'}
    html = '<div class="stat-path-card">'
    html += '<div class="stat-path-header">'
    html += f'<span class="stat-path-name">{esc(path_name)}</span>'
    html += '<div class="stat-badges">'
    for stat in ('SPR', 'STR', 'MAG', 'SPD'):
        val = stats.get(stat, '??')
        html += f'<span class="stat-badge {stat_cls[stat]}">{stat} {esc(val)}</span>'
    html += '</div></div>'

    if equip_rows:
        html += '<table class="stat-equip-table">'
        html += '<thead><tr><th>Lvl</th><th>Weapon</th><th>Head</th><th>Arm</th><th>Armor</th><th>Add-On</th></tr></thead>'
        html += '<tbody>'
        for lvl_code, items in equip_rows:
            html += '<tr>'
            html += f'<td class="lvl-badge">{esc(lvl_code) if lvl_code else "—"}</td>'
            for j in range(5):
                val = items[j].strip() if j < len(items) else ''
                if val in ('-', ''):
                    val = '—'
                html += f'<td>{esc(val)}</td>'
            html += '</tr>'
        html += '</tbody></table>'

    html += '</div>'
    return html, i


def _format_extras_content(lines):
    """Format content of a post-walkthrough section."""
    parts = []
    i = 0

    while i < len(lines):
        stripped = lines[i].strip()

        if not stripped:
            i += 1
            continue

        # === PERFECT STATS TABLE: .====. | PATH X | SPR : N | STR : N | MAG : N | SPD : N | ===
        if re.match(r'^\s*\.[=]+\.\s*$', stripped) and i + 1 < len(lines):
            if re.search(r'SPR\s*:', lines[i + 1]):
                stat_html, i = _collect_stat_table(lines, i)
                if stat_html:
                    parts.append(stat_html)
                continue

        # === CHARACTER SECTION HEADER: .----. | CHARNAME | '----' ===
        # (dash-only box → character section divider in Perfect Stats)
        if re.match(r'^\s*\.-+\.\s*$', stripped) and i + 1 < len(lines) and '|' in lines[i + 1]:
            header_line = lines[i + 1].strip()
            title_match = re.search(r'\|\s*(.+?)\s*\|', header_line)
            if title_match:
                parts.append(f'<h3 class="char-section-header">{esc(title_match.group(1).strip())}</h3>')
                i += 2
                while i < len(lines) and re.match(r"^[\s'\`=\-\.]+$", lines[i].strip()):
                    i += 1
                continue

        # === SUBSECTION HEADER: .===. | TITLE | '===' ===
        if re.match(r'^\s*\.[-=]+\.\s*$', stripped):
            if i + 1 < len(lines) and '|' in lines[i+1]:
                header_line = lines[i+1].strip()
                title_match = re.search(r'\|\s*(.+?)\s*\|', header_line)
                if title_match:
                    parts.append(f'<h3 class="subsection-header">{esc(title_match.group(1).strip())}</h3>')
                    i += 2
                    while i < len(lines) and re.match(r"^[\s'\`=\-\.]+$", lines[i].strip()):
                        i += 1
                    continue

        # === FAQ-STYLE: .===.---. | N | Question | '==='.---' ===
        if re.match(r"^\s*\.===\.", stripped):
            if i + 1 < len(lines) and '|' in lines[i+1]:
                header_line = lines[i+1].strip()
                header_parts = [p.strip() for p in header_line.split('|') if p.strip()]
                if len(header_parts) >= 2:
                    num = header_parts[0]
                    title_text = header_parts[1]
                    parts.append(f'<h3 class="subsection-header">{esc(num)}. {esc(title_text)}</h3>')
                elif header_parts:
                    parts.append(f'<h3 class="subsection-header">{esc(header_parts[0])}</h3>')
                i += 2
                while i < len(lines) and re.match(r"^[\s'\`=\-\.]+$", lines[i].strip()):
                    i += 1
                continue

        # === BORDERED TABLE ===
        if re.match(r'^\s*\.[=\-]+\.', stripped) and i + 1 < len(lines) and '|' in lines[i+1]:
            table_html, i = collect_bordered_table(lines, i)
            if table_html:
                parts.append(table_html)
            continue

        # === SUBHEADING with underline (Title + ¯¯¯) ===
        if i + 1 < len(lines) and re.match(r'^\s*¯+\s*$', lines[i+1].strip()) and re.search(r'[a-zA-Z]', stripped):
            parts.append(f'<h4 class="text-lg font-semibold text-gray-300 mt-4 mb-2">{esc(stripped)}</h4>')
            i += 2
            continue

        # === PURE DECORATION ===
        if is_pure_decoration(stripped):
            i += 1
            continue

        # === TREASURE LIST (- Item [F/C/R] description) ===
        if re.match(r'^[\-\*]\s+\S', stripped) and re.search(r'\[([FCR\*])\]', stripped):
            items = []
            while i < len(lines):
                ls = lines[i].strip()
                if re.match(r'^[\-\*]\s+\S', ls) and re.search(r'[a-zA-Z]', ls):
                    items.append(ls.lstrip('-* '))
                    i += 1
                elif not ls:
                    break
                elif is_pure_decoration(ls):
                    i += 1
                    continue
                else:
                    break
            if items:
                parts.append('<ul class="list-disc list-inside my-2 space-y-1 text-sm">')
                for item in items:
                    escaped_item = esc(item)
                    escaped_item = re.sub(r'\[([FCR\*])\]', r'<span class="text-blue-400 font-bold">[\1]</span>', escaped_item)
                    parts.append(f'<li>{escaped_item}</li>')
                parts.append('</ul>')
            continue

        # === BULLET LIST (•, -) ===
        if stripped.startswith('•') or (stripped.startswith('- ') and not re.search(r'\[[FCR\*]\]', stripped)):
            items = []
            while i < len(lines):
                ls = lines[i].strip()
                if ls.startswith('•') or (ls.startswith('- ') and not re.search(r'\[[FCR\*]\]', ls)):
                    item_text = re.sub(r'^[•\-]\s*', '', ls)
                    i += 1
                    while i < len(lines) and lines[i].strip() and not lines[i].strip().startswith('•') and not lines[i].strip().startswith('- ') and not is_pure_decoration(lines[i].strip()) and not re.match(r'^\s*\.[-=]+', lines[i].strip()):
                        item_text += ' ' + lines[i].strip()
                        i += 1
                    items.append(item_text)
                elif not ls:
                    break
                else:
                    break
            if items:
                parts.append('<ul class="list-disc list-inside my-2 space-y-1">')
                for item in items:
                    parts.append(f'<li class="text-sm">{esc(item)}</li>')
                parts.append('</ul>')
            continue

        # === NUMBERED LIST ===
        if re.match(r'^\d+\.', stripped):
            items = []
            while i < len(lines):
                ls = lines[i].strip()
                if re.match(r'^\d+\.', ls):
                    item_text = re.sub(r'^\d+\.\s*', '', ls)
                    i += 1
                    while i < len(lines) and lines[i].strip() and not re.match(r'^\d+\.', lines[i].strip()) and not is_pure_decoration(lines[i].strip()):
                        item_text += ' ' + lines[i].strip()
                        i += 1
                    items.append(item_text)
                elif not ls:
                    break
                else:
                    break
            if items:
                parts.append('<ol class="list-decimal list-inside my-2 space-y-1">')
                for item in items:
                    parts.append(f'<li class="text-sm">{esc(item)}</li>')
                parts.append('</ol>')
            continue

        # === INSTRUCTION (o ...) ===
        if stripped.startswith('o '):
            parts.append('<ul class="instruction-list">')
            while i < len(lines):
                ns = lines[i].strip()
                if ns.startswith('o '):
                    text = ns[2:]
                    i += 1
                    while i < len(lines):
                        cs = lines[i].strip()
                        if not cs or cs.startswith('o ') or is_pure_decoration(cs) or re.match(r'^\s*\.[-=]+', cs):
                            break
                        text += ' ' + cs
                        i += 1
                    parts.append(f'<li>{esc(text)}</li>')
                elif not ns:
                    i += 1
                    break
                else:
                    break
            parts.append('</ul>')
            continue

        # === REGULAR PARAGRAPH ===
        para = [stripped]
        i += 1
        while i < len(lines):
            ns = lines[i].strip()
            if not ns:
                break
            if is_pure_decoration(ns):
                break
            if re.match(r'^\s*\.[-=]+\.', ns):
                break
            if re.match(r'^\s*\.===', ns):
                break
            if ns.startswith('•') or ns.startswith('- ') or ns.startswith('o '):
                break
            if re.match(r'^\d+\.', ns):
                break
            if ns.count('|') > 3 and len(ns) > 30:
                break
            para.append(ns)
            i += 1
        parts.append(f'<p class="mb-3">{esc(" ".join(para))}</p>')

    return '\n'.join(parts)


# ============================================================================
# MAIN
# ============================================================================

def main():
    print(f"Reading guide from '{INPUT_FILENAME}'...")
    try:
        with open(INPUT_FILENAME, "r", encoding="utf-8") as f:
            raw_text = f.read()
    except FileNotFoundError:
        print(f"Error: '{INPUT_FILENAME}' not found. Run the downloader first.")
        return

    all_lines = raw_text.split('\n')

    # Find walkthrough start (F00)
    walkthrough_start = -1
    for idx, line in enumerate(all_lines):
        if "(F00)" in line and "*" in line:
            walkthrough_start = idx
            break
    if walkthrough_start == -1:
        print("Could not find walkthrough start (F00).")
        return

    preliminaries_text = "\n".join(all_lines[:walkthrough_start])

    segment_pattern = re.compile(r'^\s*\*\s*(.*?)\s*\(D(\d)-(\d\d)\)\s*\*')
    summary_pattern = re.compile(
        r'TARGET TIME\s*:\s*([\d:]+).*?TARGET GIL\s*:\s*([\d,\-]+).*?ENCOUNTERS\s*:\s*(\d+|N/A)'
    )
    post_section_pattern = re.compile(r'\(([A-Z]\d\d)\)\s*\*')

    guide_lines = all_lines[walkthrough_start:]
    segments = []
    post_sections = []
    current_segment = None
    current_post = None
    in_post_walkthrough = False

    for line in guide_lines:
        seg_match = segment_pattern.match(line.strip())
        if seg_match:
            if current_segment:
                segments.append(current_segment)
            if current_post:
                post_sections.append(current_post)
                current_post = None
            in_post_walkthrough = False
            full_title = seg_match.group(1).strip().rstrip(':').strip()
            disc = seg_match.group(2)
            num = seg_match.group(3)
            seg_id = f'D{disc}-{num}'
            current_segment = {
                'id': seg_id, 'title': full_title,
                'content': [], 'summary': {}
            }
            continue

        post_match = post_section_pattern.search(line)
        if post_match and not seg_match:
            code = post_match.group(1)
            if code[0] in 'GHIJKLM' and code not in ('F00', 'F01'):
                if current_segment:
                    segments.append(current_segment)
                    current_segment = None
                if current_post:
                    post_sections.append(current_post)
                in_post_walkthrough = True
                title_match = re.search(r'\|\s*(.+?)\s*\|', line)
                title = title_match.group(1).strip() if title_match else code
                current_post = {'code': code, 'title': title, 'content': []}
                continue

        if in_post_walkthrough and current_post is not None:
            if re.match(r'^=+$', line.strip()):
                continue
            current_post['content'].append(line)
        elif current_segment is not None:
            clean_line = line.replace('|', ' ')
            summary_match = summary_pattern.search(clean_line)
            if summary_match:
                t, g, e = summary_match.groups()
                current_segment['summary'] = {
                    'time': t.strip(), 'gil': g.strip(), 'encounters': e.strip()
                }
            else:
                current_segment['content'].append(line)

    if current_segment:
        segments.append(current_segment)
    if current_post:
        post_sections.append(current_post)

    print(f"Found {len(segments)} walkthrough segments and {len(post_sections)} extra sections.")

    discs = {'disc1': [], 'disc2': [], 'disc3': [], 'disc4': []}
    for seg in segments:
        if seg['id'].startswith('D1'):
            discs['disc1'].append(seg)
        elif seg['id'].startswith('D2'):
            discs['disc2'].append(seg)
        elif seg['id'].startswith('D3'):
            discs['disc3'].append(seg)
        elif seg['id'].startswith('D4'):
            discs['disc4'].append(seg)

    print("Building HTML...")
    final_html = HTML_HEAD + HTML_TABS

    # Preliminaries
    final_html += f'<div id="preliminaries" class="tab-content active">{format_preliminaries(preliminaries_text)}</div>'

    # TOC
    toc_html = '<div id="contents" class="tab-content"><div class="toc">'
    toc_html += '<h3 class="section-header">Table of Contents</h3>'
    for di in range(1, 5):
        disc_key = f'disc{di}'
        toc_html += f'<h4>Disc {di}</h4><ul>'
        for seg in discs[disc_key]:
            toc_html += f'<li><a href="#{seg["id"]}" data-target-tab="{disc_key}">{seg["id"]}: {seg["title"]}</a></li>'
        toc_html += '</ul>'
    if post_sections:
        toc_html += '<h4>Extras</h4><ul>'
        for sec in post_sections:
            toc_html += f'<li><a href="#section-{sec["code"]}" data-target-tab="extras">{sec["code"]}: {sec["title"]}</a></li>'
        toc_html += '</ul>'
    toc_html += '</div></div>'
    final_html += toc_html

    # Disc tabs
    for di in range(1, 5):
        disc_key = f"disc{di}"
        final_html += f'<div id="{disc_key}" class="tab-content">'
        if not discs[disc_key]:
            final_html += '<p class="p-8 text-center text-gray-400">No content for this disc.</p>'
        for seg in discs[disc_key]:
            print(f"  Building segment: {seg['id']}")
            final_html += build_segment_html(seg)
        final_html += '</div>'

    # Extras
    final_html += '<div id="extras" class="tab-content">'
    if post_sections:
        final_html += format_extras(post_sections)
    else:
        final_html += '<p class="p-8 text-center text-gray-400">No extra content found.</p>'
    final_html += '</div>'

    final_html += HTML_FOOTER

    with open(OUTPUT_FILENAME, "w", encoding="utf-8") as f:
        f.write(final_html)

    print(f"\nSuccessfully generated: {OUTPUT_FILENAME}")
    print(f"  Walkthrough segments: {len(segments)}")
    for di in range(1, 5):
        print(f"    Disc {di}: {len(discs[f'disc{di}'])} segments")
    print(f"  Extra sections: {len(post_sections)}")


if __name__ == "__main__":
    main()
