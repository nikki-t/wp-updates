# wp-updates
First iteration, still in testing phase: Python program to update WordPress installation themes and plugins for use with LXD containers; bash script is used to loop through containers on host machine and then run python program local to the container.



Used with venv and requires wget and requests libraries.

Composed of several modules: Check for updates, apply updates, print reports, cleanup, and custom exceptions.
