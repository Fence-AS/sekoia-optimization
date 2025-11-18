# sekoia-optimization
Python script for handling SEKOIA optimization rules.

**Start with:**
```Python
python main.py --help
```

Modify `payload.json` to match the event to drop.


### Options
```Text
usage: main.py [-h] [-c [PATH] | -d UUID | -l]

SEKOIA API.
SEKOIA API CLI Tool.

options:
  -h, --help           show this help message and exit

Optional arguments:
  Yippi yapp.

  -c, --create [PATH]  Create an optimization rule from JSON payload. Default: ./payload.json
  -d, --delete UUID    The rule UUID to delete
  -l, --list           List all optimization rules
```
