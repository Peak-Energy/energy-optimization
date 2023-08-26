import gurobipy
from gurobipy import GRB

energies = [1,2,3]
quarters = [1,2,3,4]

# Such structure for variable limits
production_upper_lim = {
    (1,1): 10000, (1,2): 8000, (1,3): 6000,
    (2,1): 9000, (2,2): 5000, (2,3): 10000,
    (3,1): 10000, (3,2): 5000, (3,3): 11000,
    (4,1): 9000, (4,2): 7000, (4,3): 7000,
}
storage_lim = 15000

# Such structure for parameters
demand = {
    1: 20000, 2: 30000, 3: 18000, 4: 22000
}

storage_cost = {
    1: 2, 2: 0, 3: 5
}

production_cost = {
    (1,1): 5, (1,2): 5, (1,3): 3,
    (2,1): 10, (2,2): 7, (2,3): 5,
    (3,1): 6, (3,2): 5, (3,3): 2,
    (4,1): 5, (4,2): 6, (4,3): 2,
}

# Model
model = gurobipy.Model('Energy optimisation')

# Variables
X = model.addVars(quarters, energies, name='Amount supplied', ub=production_upper_lim)
Y = model.addVars(quarters, energies, name='Amount remained')
Z = model.addVars(quarters, energies, name='Amount used')

# Constraints
# Energy balance
model.addConstrs(
    (
        Y[quarters[q_ind - 1], energy] + X[quarter, energy]
        == Z[quarter, energy] + Y[quarter, energy]
        for energy in energies for q_ind, quarter in enumerate(quarters)
        if quarter != quarters[0]
    ),
    name="Energy balance"
)
model.addConstrs(
    (
        X[quarters[0], energy]
        == Z[quarters[0], energy] + Y[quarters[0], energy]
        for energy in energies
    ),
    name="Energy balance"
)

# Demand
model.addConstrs(
    (
        gurobipy.quicksum(
        Y[quarters[q_ind - 1], energy] + X[quarter, energy] for energy in energies
        ) >= demand[quarter] 
        for q_ind, quarter in enumerate(quarters) 
        if quarter != quarters[0]
    ),
    name='Demand'
)
model.addConstr(
    (
        gurobipy.quicksum(
        X[quarters[0], energy] for energy in energies
        ) >= demand[quarters[0]] 
    ),
    name='Demand'
)

# Storage 
model.addConstrs(
    (
        gurobipy.quicksum(
            Y[quarter, energy] for energy in energies
        ) <= storage_lim for quarter in quarters
    ),
    name='Storage'
)

# Objective function
obj = gurobipy.quicksum(
    (production_cost[quarter, energy]*X[quarter, energy])
    + (storage_cost[energy]*Y[quarter, energy])
    for energy in energies 
    for quarter in quarters 
)
model.setObjective(obj, GRB.MINIMIZE)

# Run
model.optimize()
model.printAttr('X')

