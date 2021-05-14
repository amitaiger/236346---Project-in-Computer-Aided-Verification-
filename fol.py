#produce FOL formula for condition node
def produce_condition_fol(cfg, route, i):
    id = route[i].get("id")
    node = cfg.get(id)
    label = node.get("label")
    if len(route) == i+1:
        route[i]["R"] = " True "
        route[i]["T"] = get_initial_t(node.get("variables"))
    else:
        route[i]["T"] = route[i+1].get("T")
        if route[i+1].get("id") == node.get("True"):
            route[i]["R"] = " And ("+route[i+1].get("R") + "," + label+")"
        else: #next node is false
            route[i]["R"] = " And ("+route[i+1].get("R") + "," + " Not (" + label +") )"

#produce FOL formula for a declaration or assert node
def produce_static_fol(cfg, route, i):
    id = route[i].get("id")
    node = cfg.get(id)
    label = node.get("label")
    if len(route) == i+1:
        route[i]["R"] = " True "
        route[i]["T"] = get_initial_t(node.get("variables"))
    else:
        route[i]["T"] = route[i+1].get("T")
        route[i]["R"] = route[i+1].get("R")

#produce FOL formula for an assignment node
def produce_assignment_fol(cfg, route, i):
    id = route[i].get("id")
    node = cfg.get(id)
    label = node.get("label")
    if label.endswith("++ "):
        variable = label.split("++", 1)[0]
        value = " ("+variable+"+ 1 "+") "
    else: #"varaible = value" assignment
        variable = label.split("=", 1)[0] #gets variable that is being assigned to
        value = label[label.find("="):]
        value = value[1:] #gets value being assigned
        value = " ("+value+") "
    variable = remove_parentheses(variable)
    if len(route) == i+1:
        route[i]["R"] = " True "
        route[i]["T"] = get_initial_t(node.get("variables"))
    else:
        route[i]["R"] = route[i+1].get("R")
        route[i]["T"] = route[i+1].get("T")
    if "[" in variable:
        left_index = variable.index("[")
        right_index = variable.rindex("]")
        array_name = variable[:left_index]
        array_index = variable[left_index+1:right_index]
        t_list = list(route[i]["T"][1:-1].split(","))
        for t_variable in t_list:
            if t_variable.startswith(array_name):
                left_index = t_variable.index("[")
                right_index = t_variable.rindex("]")
                array_entries =  t_variable[left_index+1:right_index]
                if array_index+"<-" in array_entries:
                    array_list = list(array_entries.split(","))
                    for array_entry in array_list:
                        if array_entry.startswith(array_index+"<-"):
                            array_entries_new = array_entries.replace(array_entry, array_index+"<-"+value)  
                else:
                    if array_entries == " ":
                        t_variable_new = array_name+"[ " +array_index+"<-"+value+"] "
                    else:
                        array_entries_new = array_entries+"| "+array_index+"<-"+value    
                        t_variable_new = t_variable.replace(array_entries, array_entries_new)
                    route[i]["T"] = route[i]["T"].replace(t_variable, t_variable_new)                 
    route[i]["R"] = route[i]["R"].replace(variable, value)  
    route[i]["T"] = route[i]["T"].replace(variable, value)

#produce FOL formula for return node
def produce_return_fol(cfg, route, i):
    id = route[i].get("id")
    node = cfg.get(id)
    label = node.get("label")
    route[i]["R"] = " True "
    route[i]["T"] = get_initial_t(node.get("variables"))

#produce FOL formula for function decleration node
def produce_function_fol(cfg, route, i):
    route[i]["T"] = route[i+1].get("T")
    route[i]["R"] = route[i+1].get("R")

#produce ensures node, goes at the end of every path in given function    
def produce_ensures_fol(cfg, id):
    node = cfg.get(id)
    l = node.get("l")
    new_node = {
        "id": id,
        "l": l
    }
    return new_node
    
#get the t for an end label    
def get_initial_t(variables):
    initial_t = "("
    for variable in variables:
        initial_t = initial_t + variable.get("name") +","
    initial_t = initial_t[:-1]
    initial_t = initial_t+")"
    return initial_t

#removes any parantheses at start or end of string
def remove_parentheses(s):
    while s.startswith(" ("):
        s = s[2:]
    while s.endswith(") "):
        s = s[:-2]
    return s

#produce FOL formula for a route in CFG. route is represtended by a list of dicts,
#with each dict having an id entry representing its node
def produce_fol (cfg, route):
    id = route[0].get("id")
    produce_fol_inner(cfg, route, 0)
            
def produce_fol_inner(cfg, route, i):
    id = route[i].get("id")
    node = cfg.get(id)
    if i < len(route) - 1:
        produce_fol_inner(cfg, route, i+1)
    switch = {
        "condition": produce_condition_fol,
        "loop": produce_condition_fol,
        "assignment": produce_assignment_fol,
        "declaration": produce_static_fol,
        "assert": produce_static_fol,
        "do": produce_static_fol,
        "return": produce_return_fol,
        "function": produce_function_fol
    }
    func = switch.get(node.get("type"), lambda cfg, route, i : None)
    func(cfg, route, i)

#adds ensures to end of every route in case it was defined
def append_ensures (cfg, routes):
    for name, node in cfg.items():
        if node.get("type") == "ensures":
            new_node = produce_ensures_fol(cfg, name)
            for route in routes:
                for subnode in route:
                    if subnode.get("id") != node.get("function") and route.index(subnode) == 0: #route not of current ensures function
                        break
                    if cfg[subnode.get("id")].get("next") == "end":
                        route.append(new_node)
                        break
                        

#adds assertions to start and end of route if it doesn't have one
def add_assertions (cfg, routes):
    for route in routes:
        first_node = route[0]
        last_node = route[len(route)-1]
        first_node["l"] = find_assertion(cfg, first_node)
        last_node["l"] = find_assertion(cfg, last_node)

#find the assertion for node in next node, if it exists.
#otherwise, assertions is just 'True'
def find_assertion (cfg, node):
    if "l" in node:
        return node.get("l")
    if cfg[node.get("id")].get("type") == "loop":
        next = cfg[node.get("id")].get("true")
    else:
        next = cfg[node.get("id")].get("next")
    if next == "end":
        return " True "
    next_node = cfg[next]
    if "l" in next_node:
        return next_node.get("l")
    return " True "
        

#produce FOL formula for a list containing all routes in CFG
def produce_fol_routes (cfg, routes):
    for route in routes:
        produce_fol (cfg, route)
    append_ensures (cfg, routes)
    add_assertions (cfg, routes)
