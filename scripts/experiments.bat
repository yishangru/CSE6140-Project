for /l %%x in (117, 2, 135) do (
    python main.py -inst ./data/DATA/dummy1.graph -alg LS1 -time 600 -seed %%x -ba -rc 5
)