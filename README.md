
# Sekoia Optimization Rules

Python script for handling SEKOIA optimization rules.

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

> ***NOTE:* Set the API key in a `.env` file located along side the `main.py` file.**
> 
> *Set the value as `SEKOIA_API_TOKEN="API-TOKEN-123-HERE"`.*



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
  --limit N            Page limit (default: 20)
  --offset N           Page offset (default: 0)
```

Running `python main.py` with no flags at all enters an interactive menu
instead of the usage message above — see [Interactive Mode](#interactive-mode).

### Interactive Mode

```Bash
python main.py
```

Enters a numbered menu (list/create/actions/get/remove/disable/enable/quit)
that prompts for whatever each action needs (a UUID, a payload path) instead
of a one-shot `-x` flag. Useful for exploring rules without re-typing UUIDs
into new commands each time. `--list`'s `--community`/`--intake`/`--agent`/
`--limit`/`--offset` filters aren't available in this mode — use the one-shot
`-l` form for those.

---

## Create Rule Optimization

> *Modify the `payload.json` file to match the event to drop.*

### Rule Definition

A rule is defined with the following components:

- **Optional Community UUID:** If specified, only intakes belonging to this community will be optimized.
- **Optional Dialect UUID:** If specified, only intakes that use this specific dialect will be optimized.
- **Optional Intake UUID:** If specified, only this specific intake will be optimized.
- **Optional Agent ID / Format UUID:** Only relevant for intakes collected by the Sekoia Endpoint
  Agent. The agent applies rules on itself, and only applies rules matching its format — a rule on
  an agent-collected intake **without** `format_uuid` (or `agent_id`, which sets it automatically)
  will silently never be applied on the agent.
- **Optional Set of Filters** If specified, only events that match the defined filters will be optimized.
  Filters only support parsed fields — enriched fields (e.g. `sekoiaio.tags.*`) can't be used here.
- **Action:** A bitmask of one or more actions to execute (see [Supported Actions](#supported-actions)
  below). Only the `Ignore Event` action (`1`) shows up as reduced volume on the platform's usage page —
  the other actions still run, they just aren't reflected there.

#### Supported Actions

A rule's `action` value is a bitmask, so values can be combined (e.g. `3` = `Ignore Event` + `Delete Message Field`).

| Value | Action | Description |
| :--- | :--- | :--- |
| `1` | Ignore Event | Prevents the event from being analyzed or stored. |
| `2` | Delete Message Field | Removes the `message` field from the event. |
| `4` | Shrink Event | Retains only the minimum fields required for processing. |
| `8` | Ignore Useless Event | Discards the event if the parser extracted nothing from it. No filters needed — this is self-filtering. |
| `16` | Delete Non-Standard Fields | Deletes fields not part of the official ECS/Sekoia Taxonomy. |

### Filters

Each filter consists of:

- **Key:** The field in the event that you want to evaluate.
- **Operator:** The condition to apply for the evaluation (e.g., equals, contains).
- **Optional Value:** The value against which the key will be compared. Its JSON type must match the
  field's type — quote string values (`"value": "netflow"`), don't quote numeric values
  (`"value": 4624`). A quoted number will make the filter fail.

#### Supported Operations

- `==` Checks if two values are equal
- `!=` Checks if two values are not equal
- `>` Checks if the left value is greater than the right
- `<` Checks if the left value is less than the right
- `>=` Checks if the left value is greater than or equal to the right
- `<=` Checks if the left value is less than or equal to the right
- `in` Checks if the left value is in the right collection
- `not in`Checks if the left value is not in the right collection
- `contains` Checks if the left value contains the right value
- `not contains` Checks if the left value does not contain the right value
- `exists`Checks if the specified key exists
- `not exists` Checks if the specified key does not exist


---

