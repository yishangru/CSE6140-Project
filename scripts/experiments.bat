for /l %%x in (40, 2, 138) do (
    python main.py -inst ./data/DATA/dummy1.graph -alg LS1 -time 600 -seed %%x -ba -rc 10
)