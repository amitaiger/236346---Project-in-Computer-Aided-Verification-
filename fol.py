#produce FOL formula for condition node
def produce_condition_fol(cfg, route, i):
    id = route[i].get("id")
    node = cfg.get(id)
    label = node.get("label")
    if len(route) == i+1:
        route[i]["R"] = label
        route[i]["T"] = get_initial_t(node.get("variables"))
    else:
        route[i]["T"] = route[i+1].get("T")
        if route[i+1].get("id") == node.get("true"):
            route[i]["R"] = route[i+1].get("R") + "&" + label
        else: #next node is false
            route[i]["R"] = route[i+1].get("R") + "& !" + label

#produce FOL formula for a declaration, assignment or assert node
def produce_static_fol(cfg, route, i):
    id = route[i].get("id")
    node = cfg.get(id)
    label = node.get("label")
    if node.get("type") == "declaration" or node.get("type") == "assert": #TODO: change assert here to fit
        if len(route) == i+1:
            route[i]["R"] = "true "
            route[i]["T"] = get_initial_t(node.get("variables"))
        else:
            route[i]["T"] = route[i+1].get("T")
            route[i]["R"] = route[i+1].get("R")
        return
    variable = label.split("=", 1)[0]
    value = label[label.find("="):]
    value = value[1:]
    if len(route) == i+1:
        route[i]["R"] = "true "
        route[i]["T"] = get_initial_t(node.get("variables"))
        route[i]["T"] = route[i]["T"].replace(variable, value)
    else:
        route[i]["R"] = route[i+1].get("R")
        route[i]["R"] = route[i]["R"].replace(variable, value)
        route[i]["T"] = route[i+1].get("T")
        route[i]["T"] = route[i]["T"].replace(variable, value)

#produce FOL formula for return node
def produce_return_fol(cfg, route, i):
    id = route[i].get("id")
    node = cfg.get(id)
    label = node.get("label")
    route[i]["R"] = "true "
    route[i]["T"] = get_initial_t(node.get("variables"))

#produce FOL formula for function decleration node
def produce_function_fol(cfg, route, i):
    route[i]["T"] = route[i+1].get("T")
    route[i]["R"] = route[i+1].get("R")
    
#get the t for an end label    
def get_initial_t(variables):
    initial_t = "("
    for variable in variables:
        initial_t = initial_t + variable +","
    initial_t = initial_t[:-1]
    initial_t = initial_t+")"
    return initial_t

#produce FOL formula for a route in CFG. route is represtended by a list of dicts,
#with each dict having an id entry representing its node
def produce_fol (cfg, route):
    id = route[0].get("id")
    produce_fol_inner(cfg, route, 0)
            
def produce_fol_inner(cfg, route, i):
    id = route[i].get("id")
    node = cfg.get(id)
    if node.get("next") != "end":
        produce_fol_inner(cfg, route, i+1)
    switch = {
        "condition": produce_condition_fol,
        "declaration": produce_static_fol,
        "assignment": produce_static_fol,
        "assert": produce_static_fol,
        "return": produce_return_fol,
        "function": produce_function_fol
    }
    func = switch.get(node.get("type"))
    func(cfg, route, i)

#produce FOL formula for a list containing all routes in CFG
def produce_fol_routes (cfg, routes):
    for route in routes:
        produce_fol (cfg, route)
