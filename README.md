
# Sekoia Optimization Rules

Python script for handling SEKOIA optimization rules.

- [Usage](#usage)
  - [Options](#options)
- [Create Rule Optimization](#create-rule-optimization)
  - [Rule Definition](#rule-definition)
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
usage: main.py [-h] [-l | -c [PATH] | -a | -g UUID | -r UUID | -d UUID | -e UUID]

Sekoia.io Optimization Rules.
A CLI tool to simplify the management of Optimization Rules in the Sekoia API.

options:
  -h, --help           show this help message and exit

Arguments:
  Mutually exclusive arguments reflecting Sekoia's API Scheme.

  -l, --list           List all optimization rules
  -c, --create [PATH]  Create an optimization rule from JSON payload. Default: ./payload.json
  -a, --actions        List all supported optimization actions
  -g, --get UUID       Get the given rule UUID
  -r, --remove UUID    Remove the given rule UUID
  -d, --disable UUID   Disable the given rule UUID
  -e, --enable UUID    Enable the given rule UUID
```

---

## Create Rule Optimization

> *Modify the `payload.json` file to match the event to drop.*

### Rule Definition

A rule is defined with the following components:

- **Optional Community UUID:** If specified, only intakes belonging to this community will be optimized.
- **Optional Dialect UUID:** If specified, only intakes that use this specific dialect will be optimized.
- **Optional Intake UUID:** If specified, only this specific intake will be optimized.
- **Optional Set of Filters** If specified, only events that match the defined filters will be optimized.
- **Action:** This specifies the particular actions that will be executed to optimize the events.

### Filters

Each filter consists of:

- **Key:** The field in the event that you want to evaluate.
- **Operator:** The condition to apply for the evaluation (e.g., equals, contains).
- **Optional Value:** The value against which the key will be compared.

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

