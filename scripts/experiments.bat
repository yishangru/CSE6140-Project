for /l %%x in (117, 2, 135) do (
    python main.py -inst ./data/DATA/dummy1.graph -alg LS2 -time 600 -seed %%x -ba -rc 5 -params '{\"T\":0.95,\"steps\":100000,\"alpha\":0.999}'
    ::python main.py -inst ./data/DATA/dummy1.graph -alg LS1 -time 600 -seed %%x -ba -rc 
)