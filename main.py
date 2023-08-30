import gurobipy
from gurobipy import GRB

from data_extraction import Data

# Model
model = gurobipy.Model("Energy optimisation")

# Variables
X = model.addVars(
    Data.months, Data.energies, name="Amount supplied", ub=Data.production_limit
)
Y = model.addVars(Data.months, Data.energies, name="Amount remained")
Z = model.addVars(Data.months, Data.energies, name="Amount used")

# Constraints
# Energy balance
model.addConstrs(
    (
        Y[Data.months[m_ind - 1], energy] + X[month, energy]
        == Z[month, energy] + Y[month, energy]
        for energy in Data.energies
        for m_ind, month in enumerate(Data.months)
        if month != Data.months[0]
    ),
    name="Energy balance",
)
model.addConstrs(
    (
        X[Data.months[0], energy]
        == Z[Data.months[0], energy] + Y[Data.months[0], energy]
        for energy in Data.energies
    ),
    name="Energy balance",
)

# Demand
model.addConstrs(
    (
        gurobipy.quicksum(
            Y[Data.months[m_ind - 1], energy] + X[month, energy]
            for energy in Data.energies
        )
        >= Data.demand[month]
        for m_ind, month in enumerate(Data.months)
        if month != Data.months[0]
    ),
    name="Demand",
)
model.addConstr(
    (
        gurobipy.quicksum(X[Data.months[0], energy] for energy in Data.energies)
        >= Data.demand[Data.months[0]]
    ),
    name="Demand",
)

# Storage
model.addConstrs(
    (
        Y[month, energy] <= Data.storage_limit[energy]
        for month in Data.months
        for energy in Data.energies
    ),
    name="Storage",
)

# Objective function
obj = gurobipy.quicksum(
    (Data.production_cost[energy] * X[month, energy])
    + (Data.storage_cost[energy] * Y[month, energy])
    for energy in Data.energies
    for month in Data.months
)
model.setObjective(obj, GRB.MINIMIZE)

# Run
model.optimize()
model.printAttr("X")

model.write("out.json")
