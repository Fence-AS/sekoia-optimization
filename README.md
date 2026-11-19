# Sekoia Optimization Rules

Python CLI for managing Sekoia.io Optimization Rules (filters that drop or reduce noisy events at the intake level) through Sekoia's REST API.

## Usage

Set the API key in a `.env` file next to `main.py`: `SEKOIA_API_TOKEN="API-TOKEN-123-HERE"`.

```Text
usage: main.py [-h] [-l | -c [PATH] | -a | -g UUID | -r UUID | -d UUID |
               -e UUID] [--community UUID] [--intake UUID] [--agent UUID]
               [--limit N] [--offset N] [--all] [--raw] [-y]

options:
  -h, --help           show this help message and exit
  --raw                Print raw JSON instead of formatted text.
  -y, --yes            Skip y/N confirmation prompts.

Arguments:
  -l, --list           List optimization rules (50 by default, see --limit and --all)
  -c, --create [PATH]  Create an optimization rule from JSON payload. Default: ./payload.json
  -a, --actions        List all supported optimization actions
  -g, --get UUID       Get the given rule UUID
  -r, --remove UUID    Remove the given rule UUID
  -d, --disable UUID   Disable the given rule UUID
  -e, --enable UUID    Enable the given rule UUID

List options (only with --list):
  --community UUID     Filter by community UUID
  --intake UUID        Filter by intake UUID
  --agent UUID         Filter by agent ID
  --limit N            Rules to show, 1 to 100 (default: 50)
  --offset N           Page offset (default: 0)
  --all                Show every rule, ignoring --limit
```

Run `python main.py` with no flags for an interactive menu. Rule listing there pages 50 at a time (`n`/`p`/`q`). The list options above are only available with `-l`.

## Creating a rule

Copy `payload.example.json` to `payload.json` (gitignored) and edit it.

- **`community_uuid`** (required): the community the rule applies to. If it's left out or `null`, the rule goes on the workspace and doesn't apply to any community.
- **`format_uuid`** (recommended): limits the rule to intakes of this format (Sekoia's docs call it "dialect"). The API ignores `dialect_uuid`. Required for Sekoia Endpoint Agent intakes, or set `agent_id`, which sets it automatically.
- **`intake_uuid`** (optional): limits the rule to one intake.
- **`filters`** (optional): every filter must match. Only parsed fields work, not enriched ones like `sekoiaio.tags.*`.
- **`action`**: a bitmask, values combine (`3` = Ignore Event + Delete Message Field). Run `python main.py -a` for the current list. Only Ignore Event (`1`) shows as reduced volume on the usage page.

### Filters

Each filter is `{"field", "operator", "value"}`. The value's JSON type must match the field: `"netflow"` is a string, `4624` is a number. A quoted number fails silently.

Operators: `==`, `!=`, `>`, `<`, `>=`, `<=`, `in`, `not in`, `contains`, `not contains`, `exists`, `not exists` (no `value` for the last two).
