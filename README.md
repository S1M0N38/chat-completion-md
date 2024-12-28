<div align="center">
  <h1>⇋&nbsp;&nbsp;chat-completion-md&nbsp;&nbsp;⌗</h1>
  <p><em>Convert OpenAI chat completion request to markdown and vice versa</em></p>
</div>

______________________________________________________________________

For a couple of projects I needed to work with OpenAI chat completion requests (which format, btw, is compatible with a lot of other LLM's providers and open source solutions). I need to inspect those requests, maybe modify the content of the messages. It makes sense to convert the not-human-friendly JSON format (typically used to store these requests) into markdown files so they can be nicely visualized (highlighted with markdown treesitter in editor) and easily modified.

This lib is so simple that it barely makes sense to create a standalone package to do that. The main reason is to guarantee consistency and tested conversion across projects.

`chat-completion-md` is hosted on [PyPI](https://pypi.org/project/chat-completion-md), so you can install with `uv` (recommended), `pip`, `pipx`...

### CLI

- Print request stored as JSON files to markdown representation to stdout

```
chat_completion_md path/to/json/file.json
```

- Print request stored as markdown files to JSON representation to stdout

```
chat_completion_md path/to/md/file.md
```

### API

```python
from chat_completion_md import json_to_md, md_to_json

json_str = ...
md_str = json_to_md(json_str)

md_str = ...
json_str = md_to_json(md_str)
```

______________________________________________________________________

### Specification

This simple library/application supports only a subset of the available parameters of the OpenAI chat completion endpoint (arguably the most important ones). Inference engine offering OpenAI compatible API (vLLM, Ollama, TGI, llama.cpp, LMStudio, ...) guarantees supports for a similar subsets of parameters.

#### Supported parameters

> [!NOTE]
> To guarantee consistency, the parameters are alphabetically sorted in JSON and in the Markdown representation.

- `frequency_penalty: float` - Penalizes new tokens based on their frequency in the text so far.
- `logit_bias: dict[str, int]` - Modifies the likelihood of specified tokens appearing in the completion.
- `max_tokens: int` - The maximum number of tokens that can be generated in the chat completion.
- `messages: list[str]` - List of messages in the ChatML format.
- `model: str` - ID of the model to use
- `presence_penalty: float` - Penalizes new tokens based on their presence in the text so far.
- `stream: bool` - If set, partial message deltas will be sent as they become available.
- `temperature: float` - Sampling temperature to use, between 0 and 2.
- `top_p: float` - Nucleus sampling, where the model considers the results of the tokens with top_p probability mass.

> [!IMPORTANT]
> `model` and `messages` are the only required parameters.

#### Markdown representation

- The Markdown front matter contains the parameters in YAML format except for the `messages`.
- Message list is unrolled after the front matter where each message has the following format:

```txt
                     <- empty line
# {message role}     <- H1 header with message role
                     <- empty line
{message content}    <- message body spanning multiple lines
                     <- empty line
---                  <- three dashes
```

#### Conversion recipes

***JSON to Markdown***

1. Parse JSON string into a dictionary.
1. Pop the `messages` key from the dictionary.
1. Convert the dictionary to YAML and add as front matter to the markdown file.
1. Convert each message to its markdown representation and add sequentially to the markdown file.

***Markdown to JSON***

1. Use regex to extract the front matter and the content after the front matter.
1. Use YAML to parse the front matter into a dictionary.
1. Parse the content after the front matter into a list of messages.
1. Add messages to the dictionary and convert to JSON string.
