PS_PATH=/U03/psutil
. $PS_PATH/env/bin/activate
wait
python $PS_PATH/execute/run_proc.py
deactivate
