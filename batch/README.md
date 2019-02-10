# Batch scripts

## Overview

The idea here is to have write small functional scripts that can be combined via pipes.

For example:

$ python script1.py | python script2.py /dev/stdin
[START SCRIPT]
stdin NOT isatty
['yahoo world\n', '{"price": 1.22, "result": "success"}\n']
STOP
[END SCRIPT]


## Script list

