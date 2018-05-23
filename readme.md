# Planner

This project is a simple planner, used with this [simulator](https://github.com/LoicGoulefert/Simulateur-robot-lego).

It currently uses the Dijkstra algorithm to search for the best solution in a state graph.

The final objective is to implement the A* algorithm to search the state graph, using graphplan as a heuristic.

## How to install the dependencies

```
pip3 install antlr-python2-runtime
pip3 install antlr-python3-runtime
pip3 install pddlpy
pip3 install bitarray
```

To compile bitarray you must have the python3.5-dev package.


## Inputs

This simulator is meant to be used with a simulator, connected with it via TCP.
The planner send a list of instructions to the simulator, if it finds a solution to the problem it is asked to solve.


## Usage

In a terminal, execute :
`./simulator.py`

This will launch the server, waiting for the planner's instructions

In an other terminal :
`./planner.py`

You can find the **simulator** [here](https://github.com/LoicGoulefert/Simulateur-robot-lego).

