import json

import numpy
import pandas
from matplotlib import pyplot

from data_extraction import Data

# Load output data
with open("out.json", "r") as file:
    data = json.loads(file.read())

# Separate into amount supplied, amount remained, and amount used
vars = data["Vars"]
supplied = {month: [0] * 4 for month in Data.months}
used = {month: [0] * 4 for month in Data.months}
remained = {month: [0] * 4 for month in Data.months}

for entry in vars:
    parts = entry["VarName"].split("[")
    month = parts[1].split(",")[0]
    energy = parts[1].split(",")[1][:-1]
    idx = Data.energies.index(energy)
    if "Amount supplied" in parts[0]:
        supplied[month][idx] = entry["X"]
    elif "Amount used" in parts[0]:
        used[month][idx] = entry["X"]
    elif "Amount remained" in parts[0]:
        remained[month][idx] = entry["X"]

supplied = pandas.DataFrame.from_dict(supplied, orient="index", columns=Data.energies)
used = pandas.DataFrame.from_dict(used, orient="index", columns=Data.energies)
remained = pandas.DataFrame.from_dict(remained, orient="index", columns=Data.energies)

# Get cost information
energies = pandas.read_excel("energies.xlsx")


def plot_demand(save=False):
    f, ax1 = pyplot.subplots(1, 1, figsize=(8, 5))
    months = list(Data.demand.keys())

    # Barcharts
    supplied_normalised = supplied.apply(lambda row: row / row.sum(), axis=1)
    bottom = numpy.zeros(12)
    colours = ["#FFCACC", "#D4E2D4", "#FCE1FD", "#FAF3F0"]
    for i, e in enumerate(Data.energies):
        ax1.bar(
            months,
            supplied_normalised[e],
            label=e,
            bottom=bottom,
            color=colours[i],
            width=1,
        )
        bottom += supplied_normalised[e]
    ax1.legend()
    ax1.set_ylabel("Proportion of energy supplied")

    # Demand curve
    ax2 = ax1.twinx()
    demand_values = list(Data.demand.values())
    ax2.plot(months, demand_values, "k-", linewidth=2)
    ax2.axis(xmin=-0.5, xmax=11.5, ymin=0, ymax=40000)
    ax2.set_ylabel("Energy demand (GWh)")

    if save:
        pyplot.savefig("demand.png", dpi=500)
    pyplot.show()


def plot_amount_breakdown(save=False):
    f, ax = pyplot.subplots(1, 1, figsize=(8, 5))
    months = list(Data.demand.keys())
    production_costs = supplied * energies.production_cost.tolist()
    ax.plot(months, production_costs.sum(axis=1).values, "k--", label="Production cost")

    storage_costs = remained * energies.storage_cost.tolist()
    ax.plot(months, storage_costs.sum(axis=1).values, "k:", label="Storage cost")

    total_costs = production_costs + storage_costs
    ax.plot(months, total_costs.sum(axis=1).values, "k-", label="Total cost")

    actual_costs = Data.actual_production * energies.production_cost.tolist()
    ax.plot(months, actual_costs.sum(axis=1).values, "r-", label="Actual cost")

    bottom = numpy.zeros(12)
    colours = ["#FFCACC", "#D4E2D4", "#FCE1FD", "#FAF3F0"]
    for i, e in enumerate(Data.energies):
        ax.bar(
            months,
            production_costs[e],
            label=e,
            bottom=bottom,
            color=colours[i],
            width=1,
        )
        bottom += production_costs[e]
    ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", borderaxespad=0)
    ax.axis(xmin=-0.5, xmax=11.5, ymin=0, ymax=3e9)
    ax.set_ylabel("Energy production cost (GBP)")

    if save:
        pyplot.savefig("cost.png", dpi=500, bbox_inches="tight")
    pyplot.show()


