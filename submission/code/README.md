# CSE6140-Project: Minimum Vertex Cover
*Rao Fu, Huizi Shao, Shangru Yi, Zhe Zhou*
 
**This code for contest. We are signing the contest for **LS** and **BnB** both.**

## Install Python Dependencies for Local Running
This project use Python 3+ (3.7.4 for implementation). We recommend to use python virtual environment to avoid possible dependency conflicts.

Following shell snippet can be used to create a local virtual environment.
```shell script
For windows:
  cmd cd to current directory (../CSE6140-Project/)
  
  python3 -m venv env
  env\Scripts\activate.bat  # activate virtual environment
  pip install -r dependencies.txt

For linux / MacOS:
  terminal cd to current directory (../CSE6140-Project/)
  
  python3 -m venv env
  source env/bin/activate  # activate virtual environment
  pip install -r dependencies.txt
```

After the virtual environment is created and activated, use following command to run scripts.
```shell script
python main.py -inst <filePath> -alg [BnB|LS] -time <cutoff in seconds> -seed <random seed>
# see more usage with -h (batch run, experiment repeat, solution completeness check, etc. 
# filePath example (relative path): ./data/Data/dummy1.graph
```