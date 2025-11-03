Contains brains that exhibit specific behavior for demonstative purposes.

=====================
CREATING NEW EXAMPLES
=====================

To create a new example, copy the "template" folder into a new folder, copy the brain to demo into "example.brn", then adjust "settings.json" and "_demo.sh" as appropriate.

If the brain was tested on and/or demonstrates the desired behavior on a specific seed, remember to adjust the "PREDETERMINED_SEEDS" value in settings.json.

================
DEMOING EXAMPLES
================

To demo an example, execute the example's "_demo.sh" script from the project's root directory, for example:
$ ./examples/simple/_demo.sh
