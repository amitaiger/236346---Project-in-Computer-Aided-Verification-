import copy

#create node for a function declaration in CFG
def make_function_node(data, cfg, next, variables):
    id = get_id(data)
    label = get_label(data)
    next = data.get("children")[2].get("children")[1].get("children")[0]
    next_id = get_id(next)
    if label.startswith(" inline void ensures"): #is only used as implimintation of ensure
        type = "ignore"
    else:
        type = "function"
    cfg[id] = {
        "type": type,
        "label": label,
        "next": next_id,
        "variables": []
    }
    get_variables(data, cfg[id].get("variables"))
    return cfg[id].get("variables")

#create node for a declaration, assignment, assert or assume in CFG    
def make_static_node(data, cfg, next, variables):
    id = get_id(data)
    i = None;
    if data.get("type") == "declaration":
        label = get_label(data.get("children")[1])
        if data.get("children")[1].get("type") == "init_declarator":
            node_type = "assignment"
        else:
            node_type = "declaration"
    else: #type is expression statement
        label = get_label(data.get("children")[0])
        if label.startswith(" assert"):
            node_type = "assert"
            i = label[9:]
            i = i[:-2] #strips assert to its condition
        else:
            if label.startswith(" assume"):
                node_type = "assume"
                i = label[9:]
                i = i[:-2] #strips assume to its condition
            else:
                if label.startswith(" ensures"):
                    node_type = "ensures"
                    i = label[label.find("("):]
                    i = i[1:]
                    i = i[:-2] #strips ensures to its condition
                else:
                    if data.get("children")[0].get("type") == "relational_expression":
                        return variables #for loop condition node, already created
                    else:
                        node_type = "assignment"    
    cfg[id] = {
        "type": node_type,
        "label": label,
        "next": next,
        "variables": variables
    }
    if not i == None:
        cfg[id]["I"] = i
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
    else: #no else statement
        cfg[id]["false"] = next
    return variables
    
#create node for a return in CFG
def make_return_node(data, cfg, next, variables):
    id = get_id(data)
    label = get_label(data)
    cfg[id] = {
        "type": "return",
        "label": label,
        "next": next,
        "variables": variables
    }
    return variables

#create node for a loop in CFG
def make_loop_node(data, cfg, next, variables):
    id = get_id(data)
    loop_type = data.get("children")[0].get("type")
    if loop_type == "WHILE":
        condition = data.get("children")[2]
        loop_block = data.get("children")[4]
    else: #for or do while loop
        do_id = id
        cfg[do_id] = {
            "type": "do",
            "label": "do",
            "variables": variables
            }
        if loop_type == "FOR":
            condition = data.get("children")[3].get("children")[0]
            loop_block = data.get("children")[6]
            advancement = data.get("children")[4]
            initializer = data.get("children")[2]
            id = get_id(data.get("children")[3])
            advancement_id = get_id(advancement)
            advancement_label = get_label(advancement)
            cfg[advancement_id] = {
                "type": "assignment",
                "label": advancement_label,
                "next": id,
                "variables": variables
                }
            initializer_id = get_id(initializer)
            initializer_label = get_label(initializer.get("children")[0])
            cfg[initializer_id] = {
                "type": "assignment",
                "label": initializer_label,
                "next": id,
                "variables": variables
                }
            
        else:
            if loop_type == "DO": #do while loop
                condition = data.get("children")[4]
                loop_block = data.get("children")[1]
                id = get_id(data.get("children")[2])
    cfg[id] = {
        "type": "loop",
        "variables": variables,
        "false": next,
        "label": get_label(condition)
    }
    if loop_block.get("type") == "compound_statement":
        loop_start = get_id(loop_block.get("children")[1].get("children")[0])
    else:
        loop_start = id #empty loop
    if loop_type == "DO":
        cfg[do_id]["next"] = loop_start
    else:
        if loop_type == "FOR":
            cfg[do_id]["next"] = initializer_id
    cfg[id]["true"] = loop_start
    return variables

#create a new node in CFG depending on type in json AST
def handle_type(data, cfg, next, variables):
    node_type = data.get("type")
    node_id = get_id(data)
    if node_id in cfg:
        return variables
    switch = {
        "function_definition": make_function_node,
        "declaration": make_static_node,
        "expression_statement": make_static_node,
        "jump_statement": make_return_node,
        "selection_statement": make_selection_node,
        "iteration_statement": make_loop_node
    }
    func = switch.get(node_type, lambda data, cfg, next, variables : variables)
    return func(data, cfg, next, variables)

#for a node, get the label as a string
def get_label(data):
    label = {"string": ""}
    get_label_inner(data, label)
    return_label = label.get("string")
    return_label = " "+" ".join(return_label.split())+" "
    return return_label
        
def get_label_inner(data, label):
    if data.get("type") == "compound_statement":
        return
    if data.get("children") is None:
        label[("string")] = label.get("string")+" "+data.get("text")+" "
    else:
        if data.get("type") == "unary_expression" and data.get("children")[0].get("text") == "!":
            label["string"] = " Not ("+get_label(data.get("children")[1])+") "
            return
        else:
            if data.get("type") == "logical_and_expression":
                label[("string")] = " And ("+get_label(data.get("children")[0])+","+get_label(data.get("children")[2])+") "
                return
            else:
                if data.get("type") == "logical_or_expression":
                    label[("string")] = " Or ("+get_label(data.get("children")[0])+","+get_label(data.get("children")[2])+") "
                    return
    if isinstance(data.get("children"), list):
        for subtree in data.get("children"):
            if isinstance(subtree, dict):
                label["string"] = label.get("string")+get_label(subtree)

#for a node, get its id. A node's id is its row number and column number
def get_id(data):
    line = data.get("range").get("startLineNumber")
    column = data.get("range").get("startColumn")
    return "r"+str(line)+"c"+str(column)    

#get a list of all variables that will be used in the function
def get_variables(data, variables):
    children = data.get("children")
    if isinstance(children, list):
        for subtree in children:
            if isinstance(subtree, dict):
                if subtree.get("type") == "declaration" or \
                 subtree.get("type") == "parameter_declaration":
                    variable_type = get_label(subtree.get("children")[0])
                    if subtree.get("children")[1].get("type") == "init_declarator":
                        names_node = subtree.get("children")[1].get("children")[0]
                    else:
                        names_node = subtree.get("children")[1]  
                    variable_names = get_label(names_node)
                    variable_list = list(variable_names.split(","))
                    for variable_name in variable_list:
                        if "[" in variable_name:
                            left_index = variable_name.index("[")
                            variable_name = variable_name[:left_index]+"[ ] "
                        variables.append({"type": variable_type,
                                           "name": variable_name})
                get_variables(subtree, variables)

#traverse through json AST and create nodes for CFG
def create_cfg (data, cfg, next_node, variables):
    create_cfg_inner (data, cfg, next_node, variables)
    cfg_iter = iter(cfg.items())
    for name, node in cfg_iter:
        if node.get("type") == "ensures":
            node["function"] = next(cfg_iter)[0]
        else:
            if node.get("type") == "return" and node.get("next") != "end":
                cfg[node.get("next")]["next"] = "end"
                    

def create_cfg_inner (data, cfg, next, variables):
    valid_types = ["function_definition",
        "declaration",
        "expression_statement",
        "jump_statement",
        "selection_statement",
        "iteration_statement"]
    variables = handle_type(data, cfg, next, variables)
    children = data.get("children")
    if data.get("type") == "iteration_statement":
        loop_type = data.get("children")[0].get("type")
        if loop_type == "DO":
            new_next = get_id(data.get("children")[2])
        else:
            if loop_type == "FOR":
                new_next = get_id(data.get("children")[4])
            else: #while loop
                new_next = get_id(data)
    else:
        new_next = next
    if isinstance(children, list):
        for i, subtree in enumerate(children, 0):
            if isinstance(subtree, dict):
                if data.get("type") == "block_item_list" and not i+1 == len(children):
                    for j in range(len(children))[(i+1):]:
                        if children[j].get("type") in valid_types:
                            new_next = get_id(children[j])
                            break 
                    create_cfg_inner (subtree, cfg, new_next, variables) 
                else:
                    if data.get("type") == "iteration_statement":
                        create_cfg_inner (subtree, cfg, new_next, variables)
                    else:
                        create_cfg_inner (subtree, cfg, next, variables)
            
#find all routes in CFG
def find_routes (cfg, routes):
    for name, node in cfg.items():
        if node.get("type") == "function":
            routes.append([])
            current_function = routes[-1]
        if node.get("type") == "function" or node.get("type") == "loop":
            current_function.append([])
            find_routes_inner(cfg, current_function, current_function[-1], name)
    
    
def find_routes_inner (cfg, routes, current_route, current_node_name):
    current_route.append({"id": current_node_name})
    current_node = cfg.get(current_node_name)
    if current_node.get("next") == "end" or \
    (current_node.get("type") == "loop" and len(current_route) > 1):
        return
    if current_node.get("type") == "condition" or \
    current_node.get("type") == "loop":
        routes.append(copy.deepcopy(current_route))
        false_route = routes[-1]
        if current_node.get("true")!='end':
            find_routes_inner(cfg, routes, current_route, current_node.get("true"))
        if current_node.get("false")!='end':
            find_routes_inner(cfg, routes, false_route, current_node.get("false"))
    else:
        if current_node.get("next")!='end':
            find_routes_inner(cfg, routes, current_route, current_node.get("next"))