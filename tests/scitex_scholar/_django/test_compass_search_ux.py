#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compass 2026-09-10, Scholar search-UX structure.

Regression guards for the search-first rework of the standalone Django GUI
(compass-impl-scitex-scholar-20260910). These assert STRUCTURE, not pixels:

  L303  Search is the primary, default tab (was: Citation Graph).
  L653  Advanced query syntax is collapsed; cache + source controls and the
        CrossRef API status moved out of the always-visible sidebar into the
        Search tab's Advanced section.
  L316  Placeholder tabs (Library, Enrichment) share the same container as the
        content tabs, so switching does not shift the layout.
  L345  Each search result with a DOI offers "Build citation graph" -- the
        graph can be started FROM a search result, not only via the tab.

The style is the same as test_views.py: render the template via views.index
with a RequestFactory, or read the source files directly. No browser needed;
these pin the DOM/CSS the page ships so a future edit that reintroduces the
old layout fails here.
"""

from __future__ import annotations

from pathlib import Path

from django.test import RequestFactory

from scitex_scholar._django import views

_HERE = Path(views.__file__).parent
_TEMPLATE = _HERE / "templates" / "scholar" / "scholar.html"
_SEARCH_CSS = _HERE / "static" / "scholar" / "css" / "_partials" / "_search.css"
_FORMS_CSS = _HERE / "static" / "scholar" / "css" / "_partials" / "_forms.css"
_SEARCH_JS = _HERE / "static" / "scholar" / "js" / "search.js"


def _index_body() -> str:
    return views.index(RequestFactory().get("/")).content.decode()


# ── L303: Search is the primary, default tab ────────────────────────────────


def test_search_is_the_default_active_tab():
    """The default tab must be Search, not Citation Graph (the demotion)."""
    body = _index_body()
    assert 'data-tab="search"' in body
    # Search's button AND panel both carry the active class on load.
    assert 'class="tab-btn active" data-tab="search"' in body
    assert 'id="tab-search" class="tab-panel active"' in body


def test_graph_tab_is_no_longer_active_by_default():
    """Citation Graph remains a tab, but it is not the default one."""
    body = _index_body()
    assert 'data-tab="graph"' in body
    assert 'class="tab-btn active" data-tab="graph"' not in body
    assert 'id="tab-graph" class="tab-panel active"' not in body


# ── L653: advanced details collapsed; CrossRef out of the sidebar ──────────


def test_advanced_section_is_collapsed_by_default():
    """The Advanced <details> is present and not open, so the first screen
    shows a keyword box, not backend API infrastructure."""
    body = _index_body()
    assert "search-advanced" in body
    assert "<details" in body
    # The details element must not carry the open attribute on load.
    assert '<details class="search-advanced">' in body


def test_advanced_hides_query_syntax_until_requested():
    """The advanced query-syntax help lives inside the collapsed details."""
    body = _index_body()
    assert "search-advanced__syntax" in body
    assert "if:&gt;5" in body  # impact-factor syntax, escaped in the template


def test_ignore_cache_control_is_wired_to_the_api():
    """The 'Ignore cache' checkbox exists and search.js forwards no_cache."""
    body = _index_body()
    assert 'id="searchNoCache"' in body
    assert "Ignore cache" in body
    js = _SEARCH_JS.read_text()
    assert 'params.set("no_cache", "true")' in js
    assert 'params.set("mode", modeSelect.value)' in js


def test_crossref_api_status_moved_out_of_the_sidebar():
    """The raw CrossRef endpoint is no longer the default researcher view; it
    sits in the Search tab's Advanced section instead of the always-on sidebar."""
    body = _index_body()
    assert "CrossRef API" in body
    # It must be inside the advanced block, not a top-level sidebar-section.
    assert "search-advanced__api" in body
    # The old sidebar-section header for the API status is gone.
    # (The 'DB Info' comment that introduced it is not in the shipped HTML.)
    assert ">CrossRef API</span>" in body
    # Confirm the sidebar no longer declares its own CrossRef section header
    # as a standalone sidebar-section title.
    assert "sidebar-section__title\">CrossRef API</span>" not in body


# ── L316: placeholder tabs share the stable container ───────────────────────


def test_placeholder_tabs_share_the_stable_container():
    """Library and Enrichment placeholders are wrapped in the same
    citation-graph-container the content tabs use, so switching does not
    shift the horizontal layout."""
    tpl = _TEMPLATE.read_text()
    for tab_id in ("tab-library", "tab-enrichment"):
        idx = tpl.index(f'id="{tab_id}"')
        # The container must open before the placeholder content.
        container_idx = tpl.rindex("citation-graph-container", 0, idx + 400)
        placeholder_idx = tpl.index("tab-placeholder", idx)
        assert container_idx < placeholder_idx


# ── L345: graph can be started from a search result ─────────────────────────


def test_search_results_offer_build_citation_graph():
    """Each DOI result carries a 'Build citation graph' action, and the CSS
    styles it as a quiet secondary button (not another primary)."""
    js = _SEARCH_JS.read_text()
    assert "Build citation graph" in js
    assert "search-result__graph-btn" in js
    css = _SEARCH_CSS.read_text()
    assert ".search-result__graph-btn" in css


# ── L303: touch-target minimum on the search input ──────────────────────────


def test_search_input_has_a_44px_touch_target():
    """The paper-search input and the tab bar carry a 44px+ min-height, with a
    fallback to the shared scitex-ui --input-height token when it lands."""
    forms_css = _FORMS_CSS.read_text()
    assert "min-height: var(--input-height, 44px)" in forms_css
