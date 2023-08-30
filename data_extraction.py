import pandas


class Data:
    month_data = pandas.read_excel("months.xlsx")
    energy_data = pandas.read_excel("energies.xlsx")

    # Variables
    months = month_data.month.to_list()
    energies = energy_data.energy.to_list()

    # Parameters
    demand = month_data.set_index("month").demand.to_dict()
    production_cost = energy_data.set_index("energy").production_cost.to_dict()
    storage_cost = energy_data.set_index("energy").storage_cost.to_dict()
    storage_limit = energy_data.set_index("energy").storage_lim.to_dict()
    production_limit = {
        (row["month"], col.replace("_lim", "")): value
        for _, row in month_data.iterrows()
        for col, value in row.items()
        if col not in ["month", "demand"]
    }
