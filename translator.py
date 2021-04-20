import json

#create node for a function declaration in CFG
def make_function_node(data, cfg, next, variables):
    id = get_id(data)
    label = get_label(data)
    next = data.get("children")[2].get("children")[1].get("children")[0]
    next_id = get_id(next)
    cfg[id] = {
        "type": "function",
        "label": label,
        "next": next_id,
        "variables": []
    }
    get_variables(data, cfg[id].get("variables"))
    return cfg[id].get("variables")

#create node for an assignment in CFG    
def make_assignment_node(data, cfg, next, variables):
    id = get_id(data)
    if data.get("type") == "declartion":
        if isinstance(data.get("children")[1], dict):
            label = get_label(data.get("children")[1])
        else:
            return variables #declaration without initiation, no node needed
    else: #type is expression statement
        label = get_label(data.get("children")[0])       
    cfg[id] = {
        "type": "assignment",
        "label": label,
        "next": next,
        "variables": variables
    }
    return variables

#create node for a conditional (if) in CFG    
def make_selection_node(data, cfg, next, variables):
    id = get_id(data)
    condition = data.get("children")[2]
    label = get_label(condition)
    cfg[id] = {
        "type": "condition",
        "label": label,
        "variables": variables
    }
    if_block = data.get("children")[4];
    if if_block.get("type") == "compound_statement":
        cfg[id]["true"] = get_id(if_block.get("children")[1].get("children")[0])
    else:
        cfg[id]["true"] = get_id(if_block)
    if len(data.get("children")) == 7: #else statement
        else_block = data.get("children")[6]
        if else_block.get("type") == "compound_statement":
            cfg[id]["false"] = get_id(else_block.get("children")[1].get("children")[0])
        else:
            cfg[id]["false"] = get_id(else_block)
    else:
        cfg[id]["false"] = next
    return variables
    
#create node for a return in CFG
def make_return_node(data, cfg, next, variables):
    id = get_id(data)
    label = get_label(data)
    cfg[id] = {
        "type": "return",
        "label": label,
        "next": "end",
        "variables": variables
    }
    return variables

#create a new node in CFG depending on type in json AST
def handle_type(data, cfg, next, variables):
    node_type = data.get("type")
    switch = {
        "function_definition": make_function_node,
        "declaration": make_assignment_node,
        "expression_statement": make_assignment_node,
        "jump_statement": make_return_node,
        "selection_statement": make_selection_node
    }
    func = switch.get(node_type, lambda data, cfg, next, variables : variables)
    return func(data, cfg, next, variables)

#for a node, get the label as a string
def get_label(data):
    label = {"string": " "}
    get_label_inner(data, label)
    return label.get("string")
        
def get_label_inner(data, label):
    if data.get("type") == "compound_statement":
        return
    if data.get("children") is None:
        label[("string")] = label.get("string")+data.get("text")+" "
    if isinstance(data.get("children"), list):
        for subtree in data.get("children"):
            if isinstance(subtree, dict):
                get_label_inner(subtree, label)

#for a node, get its id. A node's id is its row number and column number
def get_id(data):
    line = data.get("range").get("startLineNumber")
    column = data.get("range").get("startColumn")
    return str(line)+", "+str(column)    

#get a list of all variables that will be used in the function
def get_variables(data, variables):
    children = data.get("children")
    if isinstance(children, list):
        for subtree in children:
            if isinstance(subtree, dict):
                if subtree.get("type") == "parameter_declaration" or subtree.get("type") == "declaration":
                    new_variable = get_label(subtree.get("children")[1])
                    new_variable = new_variable.split("=", 1)[0]
                    variables.append(new_variable)
                else:
                    if subtree.get("type") == "assignment_expression":
                        new_variable = get_label(subtree)
                        new_variable = new_variable.split("=", 1)[0]
                        if not new_variable in variables:
                            variables.append(new_variable)
                    else:
                        if subtree.get("type") == "jump_statement":
                            new_variable = get_label(subtree)
                            new_variable = new_variable[len(" return"):]
                            new_variable = new_variable[:-2]
                            if not new_variable in variables:
                                variables.append(new_variable)
                        else:
                            get_variables(subtree, variables)  
                        

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

#produce FOL formula for assignment node
def produce_assignment_fol(cfg, route, i):
    id = route[i].get("id")
    node = cfg.get(id)
    label = node.get("label")
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
     
#traverse through json AST and create nodes for CFG
def create_cfg (data, cfg, next, variables):
    variables = handle_type(data, cfg, next, variables)
    children = data.get("children")
    if isinstance(children, list):
        for i, subtree in enumerate(children, 0):
            if isinstance(subtree, dict):
                if data.get("type") == "block_item_list":
                    if i+1 == len(children):
                        create_cfg (subtree, cfg, next, variables)
                    else:
                        create_cfg (subtree, cfg, get_id(children[i+1]), variables) 
                else:
                    create_cfg (subtree, cfg, next, variables)                        

#produce FOL formula for a route in CFG. route is represtended by a list of dicts,
#with each dict having an id entry representing its node
def produce_fol (cfg, route):
    id = route[0].get("id")
    node = cfg.get(id)
    produce_fol_inner(cfg, route, 0)
            
def produce_fol_inner(cfg, route, i):
    id = route[i].get("id")
    node = cfg.get(id)
    if node.get("next") != "end":
        produce_fol_inner(cfg, route, i+1)
    switch = {
        "condition": produce_condition_fol,
        "assignment": produce_assignment_fol,
        "return": produce_return_fol,
        "function": produce_function_fol
    }
    func = switch.get(node.get("type"))
    func(cfg, route, i)
            
        
    

with open("max3.c.ast.json") as f:
    data = json.load(f)
    
cfg = {}  
create_cfg (data, cfg, "end", [])
route = [{"id": "35, 1"}, {"id": "36, 5"}, {"id": "37, 5"}, {"id": "38, 5"}, {"id": "38, 18"}, {"id": "39, 5"}]
#route = [{"id": "28, 1"}, {"id": "29, 5"}, {"id": "33, 9"}, {"id": "35, 5"}] this is a route for array.c
produce_fol (cfg, route)
print(json.dumps(cfg, indent = 4))
print(json.dumps(route, indent = 4))
