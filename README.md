<div align="center">
  <h1>⇋&nbsp;&nbsp;chat-completion-md&nbsp;&nbsp;⌗</h1>
  <p><em>Convert OpenAI chat completion request to markdown and vice versa </em></p>
</div>

______________________________________________________________________

For a couple of projects I needed to work with OpenAI chat completion requests (which format, btw, is compatible with a lot of other LLM's providers and open source solutions). I need to inspect those requests, maybe modify the content of the messages. It makes sense to convert the not-human-friendly JSON format (typically used to store these requests) into markdown files so they can be nicely visualized (highlighted with markdown treesitter in editor) and easily modified.

This lib is so simple that it barely makes sense to create a standalone package to do that. The main reason is to guarantee consistency and tested conversion across projects.

`chat-completion-md` is hosted on [PyPI](https://pypi.org/project/chat-completion-md), so you can install with `uv` (recommended), `pip`, `pipx`...

### CLI

- Convert requests stored as JSON files to markdown files

```
chat_completion_md --json pattern/to/*.json
```

- Convert markdown files to chat completion requests and save them as JSON

```
chat_completion_md --md pattern/to/*.md
```

### API

```python
from chat_completion_md import json_to_md, md_to_json

json_str = ...
md_str = json_to_md(json_str)

md_str = ...
json_str = md_to_json(md_str)
```
