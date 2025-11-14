-To solve path errors:export PYTHONPATH=/home/max/test/base_fast_api/app
shell:
    taskiq worker core:broker --fs-discover --tasks-pattern "**/tasks"
    taskiq worker core:broker --workers 1 --fs-discover --tasks-pattern "**/tasks"
    taskiq worker core:broker --workers 1 --no-configure-logging --fs-discover --tasks-pattern "**/tasks"
     