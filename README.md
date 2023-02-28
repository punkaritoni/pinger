# pinger
Linux of Mac preferred because of Make :)  

How to run:  
1. run "make venv" to create python virtual environment
2. run "source venv/bin/activate" to acces the venv

3. utilize CLI commands to operate the testing tool

How to get started?: ->  
  
"pinger-add-target"  
add new Target for testing  
Args (positional):  
name (str): used to identify the target  
url (str): URL to perform testing, correct format e.g. "https://google.com"  
limit (int): RTT time limit in milliseconds. Tests fail if RTT over limit.  
include (str): string that has to be found in URL response.  
  
"pinger-list-targets"  
prints all saved Targets on console  
Args: None  
  
"pinger-monitor"  
Start periodic monitoring for targets. RTT time and content is checked.  
  
"pigner-show-results"  
List results from one target  
Args (positional):  
name (str): to specify which target's result will be listed  
Args (optional):  
--Failed (switch): only print failed test results  
