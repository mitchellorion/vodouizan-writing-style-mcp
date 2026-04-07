#!/usr/bin/env python3
"""
Vodouizan Writing Style MCP Server

Provides reference articles and style guidance to help an AI write
in the distinctive voice of the Vodouizan articles.

Supports both stdio (local) and SSE (hosted) transports.
"""

import os
import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP

ARTICLES_DIR = Path(__file__).parent / "articles"

mcp = FastMCP("vodouizan-writing-style")

STYLE_GUIDE = """
# Vodouizan Writing Style Guide

## Voice and Stance
- Write from a position of deep, insider knowledge — not as an outside observer
- Assert directly. Do not hedge with "some believe" or "it is said." State things as they are
- Open each piece with a single definitive sentence that reframes a common misconception or flattens a reductive assumption
- The sentence structure is: "[Subject] is not [common misunderstanding]" or "[Subject] is not merely [reductive description]"
- Example openers: "In Haitian Vodou, ritual practice is never a casual or symbolic act." / "In Haitian Vodou, alcohol is not merely an offering, nor is it symbolic refreshment."

## Paragraph Structure
- Each paragraph advances exactly one idea, thoroughly, before moving to the next
- Short declarative sentences anchor paragraphs — followed by longer elaborations
- Return frequently to the negative frame: establish what something is NOT before or alongside what it IS
- Paragraphs typically run 4–8 sentences

## Conceptual Approach
- Treat everything as functional, relational, and operational — never symbolic or decorative
- Refuse binaries that Western frameworks impose (sacred/secular, belief/practice, art/ritual)
- Locate the political and historical stakes of every concept — colonial pressure, Catholic suppression, American occupation are recurring contexts
- Use precision about material details: specific ritual objects, specific Kreyòl terms, specific historical events
- Cite mechanisms, not just meanings — explain HOW things work, not just WHAT they mean

## Language and Register
- Academic but grounded: conceptual density delivered in plain sentences
- Use Haitian Kreyòl terms naturally, without over-explaining: lwa, tèt, kòylé, vévé, ounfò, kanzo, asogwe, peristil, ounsi, manbo, houngan, met tèt, djevo, pwen, naition, hounjeniokan, chante pwen, wonble, yanvalou
- Vocabulary leans toward: juridical, ontology, liminality, conduit, relational, regulatory, material, structural, administrative, interface, threshold, sovereignty
- Analogies are concrete and sometimes unexpected: "like unlocking a warehouse full of heavy machinery," "like taking powerful medication without knowing the illness"
- Never use spiritual or mystical language to describe something that can be described functionally

## Rhythm and Syntax
- Comma splices are acceptable and used intentionally for flow
- Sentences can end abruptly for emphasis
- Repetition of key nouns is intentional — do not substitute pronouns to avoid repetition; restate the noun
- Long analytical sentences are acceptable but follow with a short clarifying sentence
- Colons and em-dashes used to introduce elaborations

## What to Avoid
- Do NOT romanticize or exoticize — Vodou is described as a working system, not a mysterious tradition
- Do NOT use words like "spiritual journey," "mystical," "magical thinking," or "exotic"
- Do NOT frame practitioners as believing something so much as doing something
- Do NOT center the Western observer's perspective or reaction
- Do NOT reduce complexity to takeaways or lessons
- Do NOT use subheadings or bullet points in the writing itself
- Do NOT use passive constructions when active is possible

## Structural Patterns Observed Across Articles
1. Open with the corrective frame (what it is NOT)
2. Establish the functional/operational definition
3. Situate within Vodou cosmology or relational network
4. Address the political/historical context of misunderstanding
5. Return to the material specifics
6. Close by expanding the concept outward — implications, related structures, what this reveals about Vodou as a whole system

## Tone on Difficult Topics
- Animal sacrifice, possession, alcohol, sexuality: addressed directly, without euphemism, and without apology
- Poverty, colonialism, slavery: stated plainly as historical forces that shaped practice
- The dead, decomposition, the afterlife: treated as administrative and relational problems, not metaphysical mysteries
"""


def _load_articles() -> list[dict]:
    articles = []
    for path in sorted(ARTICLES_DIR.glob("*.txt")):
        articles.append({
            "id": path.stem,
            "content": path.read_text(encoding="utf-8")
        })
    return articles


@mcp.tool()
def get_style_guide() -> str:
    """Returns the comprehensive Vodouizan writing style guide. Call this first before writing anything to understand the voice, structure, and conventions of this writing style."""
    return STYLE_GUIDE


@mcp.tool()
def list_articles() -> str:
    """Lists all available reference articles by the Vodouizan author. Returns article IDs and their titles."""
    articles = _load_articles()
    listing = "\n".join([f"- {a['id']}" for a in articles])
    return f"Available Vodouizan articles ({len(articles)} total):\n\n{listing}"


@mcp.tool()
def get_article(article_id: str) -> str:
    """Returns the full text of a specific Vodouizan reference article by its ID. Use list_articles first to get valid IDs."""
    articles = _load_articles()
    match = next((a for a in articles if a["id"] == article_id), None)
    if not match:
        match = next((a for a in articles if article_id.lower() in a["id"].lower()), None)
    if not match:
        return f"Article '{article_id}' not found. Use list_articles to see available IDs."
    return f"# {match['id']}\n\n{match['content']}"


@mcp.tool()
def get_all_articles() -> str:
    """Returns the full text of all Vodouizan reference articles. Use this for full immersion in the writing style before producing a new piece."""
    articles = _load_articles()
    return "\n\n---\n\n".join([f"# {a['id']}\n\n{a['content']}" for a in articles])


@mcp.tool()
def get_writing_prompt(topic: str) -> str:
    """Generates a style-locked writing prompt for a given topic. Embeds the Vodouizan voice constraints directly into the instruction."""
    return f"""You are writing in the exact voice of the Vodouizan author. Study the style guide and reference articles provided by this MCP server before writing.

TOPIC: {topic}

MANDATORY STYLE REQUIREMENTS:
1. Open with a single definitive sentence using the pattern: "[Topic] is not [common reductive understanding]." or "[Topic] is not merely [simplified version]."
2. Write in dense, declarative paragraphs — no subheadings, no bullet points, no numbered lists
3. Treat the subject as functional and operational, never merely symbolic or decorative
4. Use relevant Haitian Kreyòl terms naturally where appropriate
5. Address the political, historical, or colonial context of any misconception you are correcting
6. Each paragraph advances exactly one idea; short declarative sentences anchor the paragraph; longer elaborations follow
7. Do NOT hedge, romanticize, or center the outsider's perspective
8. Close by opening the concept outward — what this reveals about the larger system

Before writing, call get_style_guide and get_all_articles from this MCP server to fully immerse yourself in the voice."""


if __name__ == "__main__":
    transport = os.environ.get("MCP_TRANSPORT", "stdio")
    host = os.environ.get("MCP_HOST", "0.0.0.0")
    port = int(os.environ.get("MCP_PORT", "8000"))

    if transport == "sse":
        mcp.run(transport="sse", host=host, port=port)
    elif transport == "streamable-http":
        mcp.run(transport="streamable-http", host=host, port=port)
    else:
        mcp.run(transport="stdio")
