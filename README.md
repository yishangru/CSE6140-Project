# CSE6140-Project
Team project for CSE6140 Gatech

## Install Python Dependencies for Local Running
This project use Python 3+. We recommend to use python virtual environment to avoid possible dependency conflicts.
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

If you install new package to the environment, **make sure you update `dependencies.txt` with correct package name and version**. 
Following shell snippet can be used to retrieve installed package lists.

```shell script
pip freeze  # get current installed packages and version info
```

## Paper Reference Lists
### Local Search
- Two Weighting Local Search for Minimum Vertex Cover (AAAI 2015) [paper link](https://dl.acm.org/doi/abs/10.5555/2887007.2887161#pill-authors__contentcon)
- Local search with edge weighting and configuration checking heuristics for minimum vertex cover Cover (revised from AAAI 2010, Artificial Intelligence) [paper link](https://www.sciencedirect.com/science/article/pii/S0004370211000427)
- ...

### Approximation
- Approximating the minimum vertex cover in sublinear time and a connection to distributed algorithms (Theortical Computer Science) [paper link](https://www.sciencedirect.com/science/article/pii/S0304397507003696)
- ...

## Python NetworkX
Bar-Yehuda, R., and Even, S. (1985). "A local-ratio theorem for approximating the weighted vertex cover problem."*Annals of Discrete Mathematics*, 25, 27–46, [MVC Sol](https://networkx.org/documentation/stable/_modules/networkx/algorithms/approximation/vertex_cover.html)
