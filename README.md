# Vodouizan Writing Style MCP

An MCP (Model Context Protocol) server that provides writing style guidance and reference articles to help an AI write in the distinctive voice of the Vodouizan articles on Haitian Vodou.

## Overview

This server exposes the full text of 11 reference articles and a detailed style guide derived from them. Feed it to any MCP-compatible AI to produce new writing in the same voice: authoritative, functional, anti-reductive, and grounded in insider knowledge of Haitian Vodou practice.

## Configuration

### Hosted / SSE (ModelScope or any remote deployment)

Set the environment variable `MCP_TRANSPORT=sse` before starting the server. The server listens on `0.0.0.0:8000` by default.

```json
{
  "mcpServers": {
    "vodouizan-writing-style": {
      "type": "sse",
      "url": "http://<your-host>:8000/sse"
    }
  }
}
```

Override host/port with environment variables:

```
MCP_TRANSPORT=sse
MCP_HOST=0.0.0.0
MCP_PORT=8000
```

### Streamable HTTP

```json
{
  "mcpServers": {
    "vodouizan-writing-style": {
      "type": "streamable-http",
      "url": "http://<your-host>:8000/mcp"
    }
  }
}
```

Set `MCP_TRANSPORT=streamable-http` when starting the server.

### Local / Stdio

```json
{
  "mcpServers": {
    "vodouizan-writing-style": {
      "command": "python3",
      "args": ["/FULL/PATH/TO/vodouizan-writing-style-mcp/server.py"]
    }
  }
}
```

Replace `/FULL/PATH/TO/` with the actual path where you cloned this repository.

### Requirements

- Python 3.8+
- `pip install -r requirements.txt` (installs `mcp[cli]`)

## Tools

| Tool | Description |
|------|-------------|
| `get_style_guide` | Returns a comprehensive style guide covering voice, sentence structure, paragraph rhythm, vocabulary, and what to avoid. **Call this first.** |
| `list_articles` | Lists all 11 reference article IDs |
| `get_article` | Returns the full text of a single article by ID |
| `get_all_articles` | Returns all 11 articles concatenated — for full immersion before writing |
| `get_writing_prompt` | Takes a topic string and returns a style-locked prompt with voice constraints embedded |

## Usage

1. Connect the server to your MCP-compatible AI client
2. Tell the AI to call `get_style_guide` and `get_all_articles` before writing
3. Use `get_writing_prompt` with your topic to get a fully constrained writing instruction

## Reference Articles

The server includes 11 articles covering:

- Alcohol as ritual technology
- Animal sacrifice and the food system
- Children and incomplete personhood
- Initiation and spiritual worth
- Post-death as bureaucratic process
- Ritual adornments (kòylé)
- Ritual practice and the danger of unsupervised work
- Sound, drumming, and altered time
- The Gede and their historical transformation
- The tèt as a site of sovereignty
- Design, vévé, and sacred form

## Writing Style Summary

The Vodouizan voice is:

- **Declarative and authoritative** — no hedging, no outsider framing
- **Corrective in structure** — opens by reframing what something is NOT
- **Functional, not symbolic** — everything is described as operational, relational, material
- **Historically grounded** — colonialism, Catholic suppression, and American occupation are recurring contexts
- **Dense but plain** — conceptual precision delivered in direct sentences
- Uses Haitian Kreyòl terms naturally (lwa, tèt, vévé, kòylé, ounfò, etc.)
