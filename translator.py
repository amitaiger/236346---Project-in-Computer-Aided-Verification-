import json

#create node for a return in CFG
def make_function_node(data, cfg, next):
    id = get_id(data)
    label = get_label(data)
    next = data.get("children")[2].get("children")[1].get("children")[0]
    next_id = get_id(next)
    cfg[id] = {
        "type": "function",
        "label": label,
        "next": next_id
    }

#create node for an assignment in CFG    
def make_assignment_node(data, cfg, next):
    id = get_id(data)
    if data.get("type") == "declartion":
        if isinstance(data.get("children")[1], dict):
            label = get_label(data.get("children")[1])
        else:
            return #declaration without initiation, no node needed
    else: #type is expression statement
        label = get_label(data.get("children")[0])       
    cfg[id] = {
        "type": "assignment",
        "label": label,
        "next": next
    }

#create node for a conditional (if) in CFG    
def make_selection_node(data, cfg, next):
    id = get_id(data)
    condition = data.get("children")[2]
    label = get_label(condition)
    cfg[id] = {
        "type": "condition",
        "label": label,
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
    

#create node for a return in CFG
def make_return_node(data, cfg, next):
    id = get_id(data)
    label = get_label(data)
    cfg[id] = {
        "type": "return",
        "label": label,
        "next": "end"
    }

#create a new node in CFG depending on type in json AST
def handle_type(data, cfg, next):
    type = data.get("type")
    switch = {
        "function_definition": make_function_node,
        "declaration": make_assignment_node,
        "expression_statement": make_assignment_node,
        "jump_statement": make_return_node,
        "selection_statement": make_selection_node
    }
    func = switch.get(type, lambda data, cfg, next : None)
    func(data, cfg, next)

#for a node, get the label as a string
def get_label(data):
    label = {"string": ""}
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

def get_id(data):
    line = data.get("range").get("startLineNumber")
    column = data.get("range").get("startColumn")
    return str(line)+", "+str(column)            
    
#traverse through json AST and create labels for CFG
def create_cfg (data, cfg, next):
    max = 0
    id = handle_type(data, cfg, next)
    children = data.get("children")
    if isinstance(children, list):
        for i, subtree in enumerate(children, 0):
            if isinstance(subtree, dict):
                if data.get("type") == "block_item_list":
                    if i+1 == len(children):
                        create_cfg (subtree, cfg, next)
                    else:
                        create_cfg (subtree, cfg, get_id(children[i+1])) 
                else:
                    create_cfg (subtree, cfg, next)                        


with open("D:/Projects/20-21 Spring/project in verification/Teaching.Verification.Project-master/\
benchmarks/c/json/max3.c.ast.json") as f:
    data = json.load(f)
    
cfg = {}    
create_cfg (data, cfg, "end")
print (cfg)