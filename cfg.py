import copy

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
    if data.get("type") == "declaration":
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

#traverse through json AST and create nodes for CFG
def create_cfg (data, cfg, next, variables):
    valid_types = ["function_definition",
        "declaration",
        "expression_statement",
        "jump_statement",
        "selection_statement"]
    variables = handle_type(data, cfg, next, variables)
    children = data.get("children")
    if isinstance(children, list):
        for i, subtree in enumerate(children, 0):
            if isinstance(subtree, dict):
                if data.get("type") == "block_item_list" and not i+1 == len(children):
                    new_next = next
                    for j in range(len(children))[(i+1):]:
                        if children[j].get("type") in valid_types:
                            new_next = get_id(children[j])
                            break 
                    create_cfg (subtree, cfg, new_next, variables) 
                else:
                    create_cfg (subtree, cfg, next, variables)


#find all routes in CFG
def find_routes (cfg, routes):
    for name, node in cfg.items():
        if node.get("type") == "function":
            routes.append([])
            find_routes_inner(cfg, routes, routes[-1], name)
    
    
def find_routes_inner (cfg, routes, current_route, current_node_name):
    current_route.append({"id": current_node_name})
    current_node = cfg.get(current_node_name)
    if current_node.get("next") == "end":
        return
    if current_node.get("type") == "condition":
        routes.append(copy.deepcopy(current_route))
        false_route = routes[-1]
        find_routes_inner(cfg, routes, current_route, current_node.get("true"))
        find_routes_inner(cfg, routes, false_route, current_node.get("false"))
    else:
        find_routes_inner(cfg, routes, current_route, current_node.get("next"))