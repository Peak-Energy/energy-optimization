# energy-optimisation
A simple project to explore energy supply and demand optimisation. 

## Problem statement
Imagine a hypothetical scenario in which we are tasked with planning the annual budget for energy production and storage. We have information on the production and storage capabilities of various energy sources for each month. What is the amount of each energy source produced and stored every month in order to minimise the total annual cost?

## Model formulation

### Parameters
Let $e \in E$ be the type of energy source in the set of energy sources $E$, and $t \in T$ be the month in the set of all the months $T$. 

Assuming a simple scenario, we have the following parameters:
- $D_t$ is the total projected energy demand month $t$
- $P_{te}$ is the production upper limit of energy source $e$ in month $t$
- $S_{te}$ is the storage upper limit of energy source $e$ in month $t$
- $A_e$ is the production cost of energy source $e$ 
- $B_e$ is the storage cost of energy source $e$

### Variables

The variables to be optimised are defined as follows:
- $x_{te}$ is the amount of energy source $e$ produced in month $t$
- $y_{te}$ is the amount of energy source $e$ remained in month $t$, which is equivalent to the amount that will be stored in that month
- $z_{te}$ is the amount of energy source $e$ used in month $t$ to meet the energy demand of the month

### Objective function
We want to minimise the total cost for the whole year. Translating to mathematical equation, our objective function is given as

$$ \min \sum_{e\in E} \sum_{t \in T} \Big( A_e x_{te} + B_e y_{te} \Big)$$

### Constraints
Our system is limited by the following constraints:

- **Mass balance constraint**: for each energy source at a given month, the sum of the amount produced and the amount remained from the previous month is equal to the sum of amount used and the amount remained of current month. We assume that in the first month $t_0$, i.e. January, there is no energy in storage yet.

$$ x_{te} + y_{t-1, e} = z_{te} + y_{te} \quad \forall t \in T/t_0, \forall e \in E$$

$$ x_{t_0 e} = z_{t_0 e} + y_{t_0 e} \quad \forall e \in E $$

- **Demand constraint**: In a given month, the sum of energy produced, in addition to the sum of energy stored, must at least meet the demand of the month.

$$ \sum_{e \in E} \Big( x_{te} + y_{t-1, e} \Big) \geq D_t \quad \forall t \in T/t_0$$

$$ \sum_{e \in E} x_{t_0 e} \geq D_{t_0} $$

- **Non-negativity and upper limits**: Production and storage limits will constraint $x_{te}$ and $y_{te}$. It follows that $z_{te}$ will be capped by the mass balance constraint.

$$ 0 \leq x_{te} \leq P_{te} \quad \forall t \in T, \forall e \in E$$

$$ 0 \leq y_{te} \leq S_{te} \quad \forall t \in T, \forall e \in E$$

$$ z_{te} \geq 0 \quad \forall t \in T, \forall e \in E$$
