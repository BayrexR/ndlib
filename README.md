# NDlib - Network Diffusion Library

NDlib provide implementations of several spreading and opinion dynamics models.
It is implemented in Python 2.7 (support for Python 3.x pending).

## Installation

In order to install the library just download (or clone) the current project and copy the ndlib folder in the root of your application (installation via pip will be supported in the near future).

## Example usage

Import the selected diffusion model with
```python
import ndlib.VoterModel as m
```

Generate/load a graph with the [networkx](https://networkx.github.io/) library
```python
import networkx as nx
g = nx.erdos_renyi_graph(1000, 0.1)
```
Initialize the model on the graph
```python
model = m.VoterModel(g)
```
Set the nodel initial status
```python
model.set_initial_status({'model': {'percentage_infected': 0.2}})
```
Request a single iteration of the simulation
```python
it_id, it_status = model.iteration()
```
or a bunch of iterations
```python
it_bunch = model.iteration_bunch(bunch_size=10)
``` 

## Rationale behind the implemented models

- All models inherit from ndlib.DiffusionModel

- Model configuration and parameter settings is generalized by passing configuration dictionaries

- NDlib describe diffusion models as agent-based simulations occurring at discrete time: once configured the desired model and selected the target network, subsequent iterations will provide to the user the current status of each node.

### Model configuration
Every model needs few parameters to be executed, in order to make general the initialization and iterative steps we decided to describe model configuration via dictionaries. In particular to initialize the implemented models you must supply (the chosen values are only examples of possible configurations):
```python
model = m.MSznajdModel(g)
model = m.VoterModel(g) 
model = m.QVoterModel(g, {'q': 5})
model = m.CognitiveOpDynModel(g,{'I':0.15,'B_range_min':0, 'B_range_max':1,'T_range_min':0,'T_range_max':1,'R_fraction_negative':1/3.0,'R_fraction_neutral':1/3.0,'R_fraction_positive':1/3.0})

model = m.IndependentCascadesModel(g)
model = m.ThresholdModel(g)
model = m.ProfileModel(g)
model = m.ProfileThresholdModel(g)
model = m.SIModel(g, {'beta': 0.1})
model = m.SIRModel(g, {'beta': 0.1, 'gamma': 0.1})
model = m.SISModel(g, {'beta': 0.1, 'lambda': 0.1})
```

Moreover, additional parameter can be specified to define the initial configuration of the network by using the set_initial_status method.
In particular it takes as input a (not necessarely full defined) dictionary having the following form:
```python
{
 'nodes': {'threshold': {}, 'profile': {}},
 'edges': {},
 'model': {'percentage_infected': 0, 'infected_nodes': []}
}
```
where:
- the 'nodes' component describes the individual values of (all) node thresholds and/or profiles i.e.
```python
{'nodes':{ 'threshold': {node1: value1, node2: value2, node3: value3},
          'profile': {node1: value1, node2: value2, node3: value3}}
```
- the 'edges' component describes the edge weights i.e.
```python
{'edges': [
            {'source': node1, 'target': node2, 'weight': value},
            {'source': node2, 'target': node3, 'weight': value}
           ]}
```
- the 'model' component define either the percentage of initial nodes (selected at random) or a specific initial set of infected nodes. In case both 'percentage_infected' and 'infected_nodes' are specified the latter is ignored.
