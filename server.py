#!/usr/bin/env python3
"""
Vodouizan Writing Style MCP Server

Provides reference articles and style guidance to help an AI write
in the distinctive voice of the Vodouizan articles.
"""

import json
import os
import sys
from pathlib import Path

# MCP protocol over stdio
def send_response(response: dict):
    line = json.dumps(response) + "\n"
    sys.stdout.write(line)
    sys.stdout.flush()

def send_error(id, code: int, message: str):
    send_response({
        "jsonrpc": "2.0",
        "id": id,
        "error": {"code": code, "message": message}
    })

ARTICLES_DIR = Path(__file__).parent / "articles"

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

def get_articles() -> list[dict]:
    articles = []
    for path in sorted(ARTICLES_DIR.glob("*.txt")):
        articles.append({
            "id": path.stem,
            "filename": path.name,
            "content": path.read_text(encoding="utf-8")
        })
    return articles

def handle_request(request: dict) -> dict | None:
    method = request.get("method")
    req_id = request.get("id")
    params = request.get("params", {})

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {},
                    "resources": {}
                },
                "serverInfo": {
                    "name": "vodouizan-writing-style-mcp",
                    "version": "1.0.0"
                }
            }
        }

    elif method == "notifications/initialized":
        return None  # no response needed

    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "get_style_guide",
                        "description": "Returns the comprehensive Vodouizan writing style guide. Call this first before writing anything to understand the voice, structure, and conventions of this writing style.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {},
                            "required": []
                        }
                    },
                    {
                        "name": "list_articles",
                        "description": "Lists all available reference articles by the Vodouizan author. Returns article IDs and their titles.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {},
                            "required": []
                        }
                    },
                    {
                        "name": "get_article",
                        "description": "Returns the full text of a specific Vodouizan reference article by its ID. Use this to study a particular article's structure and prose before writing on a related topic.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "article_id": {
                                    "type": "string",
                                    "description": "The article ID as returned by list_articles"
                                }
                            },
                            "required": ["article_id"]
                        }
                    },
                    {
                        "name": "get_all_articles",
                        "description": "Returns the full text of all Vodouizan reference articles. Use this when you need comprehensive immersion in the writing style before producing a new piece.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {},
                            "required": []
                        }
                    },
                    {
                        "name": "get_writing_prompt",
                        "description": "Generates a style-locked writing prompt for a given topic. Embeds the Vodouizan voice constraints directly into the instruction so you write in the correct style.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "topic": {
                                    "type": "string",
                                    "description": "The topic or subject you want to write about in the Vodouizan style"
                                }
                            },
                            "required": ["topic"]
                        }
                    }
                ]
            }
        }

    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})

        if tool_name == "get_style_guide":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": STYLE_GUIDE
                        }
                    ]
                }
            }

        elif tool_name == "list_articles":
            articles = get_articles()
            listing = "\n".join([
                f"- ID: {a['id']}\n  Title: {a['id'].replace('-', ' ')}"
                for a in articles
            ])
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Available Vodouizan articles ({len(articles)} total):\n\n{listing}"
                        }
                    ]
                }
            }

        elif tool_name == "get_article":
            article_id = args.get("article_id", "")
            articles = get_articles()
            match = next((a for a in articles if a["id"] == article_id), None)
            if not match:
                # try partial match
                match = next((a for a in articles if article_id.lower() in a["id"].lower()), None)
            if not match:
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": f"Article '{article_id}' not found. Use list_articles to see available IDs."
                            }
                        ]
                    }
                }
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": f"# {match['id']}\n\n{match['content']}"
                        }
                    ]
                }
            }

        elif tool_name == "get_all_articles":
            articles = get_articles()
            combined = "\n\n---\n\n".join([
                f"# {a['id']}\n\n{a['content']}"
                for a in articles
            ])
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": combined
                        }
                    ]
                }
            }

        elif tool_name == "get_writing_prompt":
            topic = args.get("topic", "")
            prompt = f"""You are writing in the exact voice of the Vodouizan author. Study the style guide and reference articles provided by this MCP server before writing.

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

            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            }

        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Unknown tool: {tool_name}"}
            }

    elif method == "resources/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {"resources": []}
        }

    else:
        if req_id is not None:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Method not found: {method}"}
            }
        return None


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
        except json.JSONDecodeError:
            continue

        response = handle_request(request)
        if response is not None:
            send_response(response)


if __name__ == "__main__":
    main()
