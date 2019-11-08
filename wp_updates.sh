#!/bin/bash

sites = (wptest)

for site in ${sites[@]}; do

  /usr/bin/lxc snapshot $site 'pre_update_check_and_run'

  /usr/bin/lxc exec $site -- /usr/local/python/wp_updates/wp_updates_pkg/wp_updates.py -s $site 2>&1 | logger -s

    echo Updates complete for $site.

done

exit 0
