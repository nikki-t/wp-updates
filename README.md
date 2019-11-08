# wp-updates
Python program to automate theme and plugin updates on WordPress installations. For use with LXD containers and includes bash script that loops through WordPress containers on host machine to run python program locally on the container. Requires wqet and requests libraries.

wp_updates is composed of several modules: Check for updates (update_check.py), apply updates (apply_updates.py), print reports (print_reports.py), cleanup (maintenance_cleanup.py), and custom exceptions (cusom_exceptions.py).
