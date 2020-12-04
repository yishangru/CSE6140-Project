# CSE6140-Project: Minimum Vertex Cover
*Rao Fu, Huizi Shao, Shangru Yi, Zhe Zhou*
 
Team project repo for **CSE6140 (FALL 2020)** in ***Georgia Institution of Technology***
 
The Minimum Vertex Cover (**MVC**) problem is a typical NP-complete problem that plays a significant role 
in many practical applications such as operation research, network security, computational biology and parallel machine scheduling. 
In this project, four algorithms, i.e. Branch-and-Bound (BnB), Max Degree Greedy Approximation, 
Two Weighting Local Search (Cai, Shaowei, etc. AAAI'15), Simulated Annealing Local Search are implemented to obtain the minimum vertex cover (MVC). 
A dummy solution using **NetworkX** is also included in this project for reference. Please refer to ``/doc/ProjectDescription.pdf`` and ``/doc/report.pdf`` for project details.

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
python main.py -inst <filePath> -alg [BnB|Approx|LS1|LS2] -time <cutoff in seconds> -seed <random seed>
#for bnb, can try:  python <bnb.py> -inst <filePath> -alg BnB -time 600 -seed 100 . Will also works.
# see more usage with -h (batch run, experiment repeat, solution completeness check, etc. 
# filePath example (relative path): ./data/Data/dummy1.graph
```

If you install new package to the environment, **make sure you update `dependencies.txt` with correct package name and version, and commit**. 
Just add the main package with version to `dependencies.txt` should be fine. Refer to `dependencies.txt` for example dependencies. 

Following shell snippet can be used to retrieve installed package lists.
```shell script
pip freeze  # get current installed packages and version info
```


## Paper Reference Lists
### Branch and Bound
- An Exact Algorithm for Minimum Vertex Cover Problem [paper link](https://res.mdpi.com/d_attachment/mathematics/mathematics-07-00603/article_deploy/mathematics-07-00603.pdf)

### Local Search
- Two Weighting Local Search for Minimum Vertex Cover (AAAI 2015) [paper link](https://dl.acm.org/doi/abs/10.5555/2887007.2887161#pill-authors__contentcon)
- Local search with edge weighting and configuration checking heuristics for minimum vertex cover Cover (revised from AAAI 2010, Artificial Intelligence) [paper link](https://www.sciencedirect.com/science/article/pii/S0004370211000427)
- An efficient simulated annealing algorithm for the minimum vertex cover problem [paper link](https://www.sciencedirect.com/science/article/pii/S0925231205003565?casa_token=Dz59rH3pJg8AAAAA:zWMxPM7uYdDMQ7VZ_igKVM4g0oDxapgqPUfwwWNHf9Cx1oZTKp_sZH200uE41lclpRn9ZvmYKg)

### Approximation
- Approximating the minimum vertex cover in sublinear time and a connection to distributed algorithms (Theortical Computer Science) [paper link](https://www.sciencedirect.com/science/article/pii/S0304397507003696)
- Analytical and Experimental Comparison of Six Algorithms for the Vertex Cover Problem [paper link](https://dl.acm.org/doi/pdf/10.1145/1671970.1865971)
- NMVSA Greedy Solution for Vertex Cover Problem [paper link](https://pdfs.semanticscholar.org/e8f5/943ebf4891a782dc8c25944fd71e0276a5bf.pdf)
- Analytical and experimental comparison of six algorithms for the vertex cover problem [paper link](https://www.researchgate.net/publication/238344195_Analytical_and_experimental_comparison_of_six_algorithms_for_the_vertex_cover_problem)
- An Approximation Algorithm for the Minimum Vertex Cover Problem [paper link](https://www.researchgate.net/publication/294139277_An)
 

## Python NetworkX
Bar-Yehuda, R., and Even, S. (1985). "A local-ratio theorem for approximating the weighted vertex cover problem."*Annals of Discrete Mathematics*, 25, 27–46, [MVC Sol](https://networkx.org/documentation/stable/_modules/networkx/algorithms/approximation/vertex_cover.html)
