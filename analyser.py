#!/usr/bin/env python3

from mkbsc import MultiplayerGame, iterate_until_isomorphic, \
                  export, to_string, from_string, to_file, from_file
import signal

def signal_handler(signum, frame):
    raise Exception("Timed out!")


def partition(states):
    if len(states) == 1:
        yield [ states ]
        return
        

    first = states[0]
    for subpartition in partition(states[1:]):
        for n, subset in enumerate(subpartition):
            yield subpartition[:n] + [[ first ] + subset] + subpartition[n+1:]

        yield [[ first ]] + subpartition

def IsHierarchical(obsPlayer1, obsPlayer2):
    for obs1 in obsPlayer1:
        if len(obs1) > 1:
            obsSubset = False

            for obs2 in obsPlayer2:
                if (set(obs1) <= set(obs2)):
                    obsSubset = True
            if obsSubset == False:
                return False
    return True

#Helper function for generating rows into a LaTeX table
def genLatex(observation):
    obs1 = str(observation[0]).replace('[','\{').replace(']','\}').replace("'start'", "start")
    obs2 = str(observation[1]).replace('[','\{').replace(']','\}').replace("'start'", "start")

    lat = '$' + obs1 + '$ & $' + obs2 + '$ \\\\'
    print(lat)
        

# States
L = ["start", 1, 2, 3, 4]

# Initial state
L0 = "start"

# Action alphabet
Sigma = (("init", "wait", "push"), ("init", "wait", "push"))

# Action-labeled transitions
Delta = [
    ("start", ("init", "init"), 1), ("start", ("init", "init"), 2),
    ("start", ("init", "init"), 3), ("start", ("init", "init"), 4),

    (1, ("push", "push"), 1), (1, ("wait", "wait"), 1),
    (1, ("wait", "push"),  1), (1, ("push", "wait"), 2),

    (2, ("push", "push"), 2), (2, ("wait", "wait"), 2),
    (2, ("wait", "push"),  1), (2, ("push", "wait"), 3),

    (3, ("push", "push"), 3), (3, ("wait", "wait"), 3),
    (3, ("wait", "push"),  2), (3, ("push", "wait"), 4),

    (4, ("push", "push"), 4), (4, ("wait", "wait"), 4),
    (4, ("wait", "push"),  3), (4, ("push", "wait"), 4)
]


parts = partition(L[1:])

retlist = []
for i in parts:
    retlist.append(i)

for i in range(len(retlist)):
    for j in range(i, len(retlist)):
        if IsHierarchical(retlist[j], retlist[i]) or IsHierarchical(retlist[i], retlist[j]):
            Obs = [[["start"]] + retlist[j], [["start"]] + retlist[i]]
            G = MultiplayerGame.create(L, L0, Sigma, Delta, Obs)

            signal.signal(signal.SIGALRM, signal_handler)
            signal.alarm(5)   
            try:
                (log, GK, _) = iterate_until_isomorphic(G, -1, False, True)
            except Exception:
                #Enable for unisomorphic observations
                genLatex(Obs)
                
            #Enable for isomorphic observations
            #genLatex(Obs)



    
