
# Sekoia Optimization Rules

Python CLI for managing Sekoia.io Optimization Rules (filters that drop or reduce noisy events at the intake level) through Sekoia's REST API.

- [Usage](#usage)
  - [Options](#options)
  - [Interactive Mode](#interactive-mode)
- [Create Rule Optimization](#create-rule-optimization)
  - [Rule Definition](#rule-definition)
    - [Supported Actions](#supported-actions)
  - [Filters](#filters)
    - [Supported Operations](#supported-operations)

---

## Usage

```Bash
python main.py --help
```

Set the API key in a `.env` file next to `main.py`: `SEKOIA_API_TOKEN="API-TOKEN-123-HERE"`.

### Options

```Text
usage: main.py [-h] [-l | -c [PATH] | -a | -g UUID | -r UUID | -d UUID |
               -e UUID] [--community UUID] [--intake UUID] [--agent UUID]
               [--limit N] [--offset N] [--raw] [-y]

Sekoia.io Optimization Rules.
A CLI tool to simplify the management of Optimization Rules in the Sekoia API.

options:
  -h, --help           show this help message and exit
  --raw                Print raw JSON instead of formatted text.
  -y, --yes            Skip y/N confirmation prompts.

Arguments:
  Mutually exclusive arguments reflecting Sekoia's API Scheme.

  -l, --list           List all optimization rules
  -c, --create [PATH]  Create an optimization rule from JSON payload. Default: ./payload.json
  -a, --actions        List all supported optimization actions
  -g, --get UUID       Get the given rule UUID
  -r, --remove UUID    Remove the given rule UUID
  -d, --disable UUID   Disable the given rule UUID
  -e, --enable UUID    Enable the given rule UUID

List options:
  Only apply with --list.

  --community UUID     Filter by community UUID
  --intake UUID        Filter by intake UUID
  --agent UUID         Filter by agent ID
  --limit N            Page limit (default: 100)
  --offset N           Page offset (default: 0)
```

Running `python main.py` with no flags enters an interactive menu instead of the usage message above. See [Interactive Mode](#interactive-mode).

### Interactive Mode

```Bash
python main.py
```

Enters a numbered menu (list/create/actions/get/remove/disable/enable/quit) that prompts for whatever each action needs: a UUID, a payload path. Useful for exploring rules without retyping UUIDs into new commands. The `--list` filters (`--community`/`--intake`/`--agent`/`--limit`/`--offset`) aren't available here, use the one-shot `-l` form for those.

---

## Create Rule Optimization

Copy `payload.example.json` to `payload.json` and edit it to match the event you want to drop. `payload.json` is gitignored, so your local rule, which may reference real intake or community UUIDs, is never committed.

### Rule Definition

A rule has:

- **Community UUID** (optional): restricts the rule to intakes in this community.
- **Dialect UUID** (optional): restricts the rule to intakes using this dialect.
- **Intake UUID** (optional): restricts the rule to this specific intake.
- **Agent ID / Format UUID** (optional): only relevant for intakes collected by the Sekoia Endpoint
  Agent. The agent applies rules on itself and only applies rules matching its format. A rule on an
  agent-collected intake without `format_uuid` (or `agent_id`, which sets it automatically) silently
  never applies on the agent.
- **Filters** (optional): restricts the rule to events matching every filter. Filters only support
  parsed fields; enriched fields like `sekoiaio.tags.*` don't work here.
- **Action**: a bitmask of one or more actions to execute, see [Supported Actions](#supported-actions).
  Only `Ignore Event` (`1`) shows up as reduced volume on the platform's usage page. The other actions
  still run, they just aren't reflected there.

#### Supported Actions

A rule's `action` value is a bitmask, so values combine (e.g. `3` = `Ignore Event` + `Delete Message Field`).

| Value | Action | Description |
| :--- | :--- | :--- |
| `1` | Ignore Event | Prevents the event from being analyzed or stored. |
| `2` | Delete Message Field | Removes the `message` field from the event. |
| `4` | Shrink Event | Retains only the minimum fields required for processing. |
| `8` | Ignore Useless Event | Discards the event if the parser extracted nothing from it. Self-filtering, no filters needed. |
| `16` | Delete Non-Standard Fields | Deletes fields not part of the official ECS/Sekoia Taxonomy. |

### Filters

Each filter has:

- **Key**: the field in the event to evaluate.
- **Operator**: the condition to apply (equals, contains, etc).
- **Value** (optional): the value to compare against. Its JSON type must match the field's type:
  quote string values (`"value": "netflow"`), don't quote numbers (`"value": 4624`). A quoted number
  makes the filter fail silently.

#### Supported Operations

- `==` equal
- `!=` not equal
- `>` greater than
- `<` less than
- `>=` greater than or equal to
- `<=` less than or equal to
- `in` left value is in the right collection
- `not in` left value is not in the right collection
- `contains` left value contains the right value
- `not contains` left value does not contain the right value
- `exists` the key exists
- `not exists` the key does not exist
