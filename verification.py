from z3 import *

def declare_invariant(i, variables):
    invariant_name = trim_whitespace(i.split('(')[0])
    invariant = invariant_name + "= Function('"+invariant_name+"', "
    for variable in variables:
        type = variable.get("type")
        name = variable.get("name")
        name = trim_whitespace(name)
        if type == " int ":
            if name.endswith("[ ]"):
                invariant += "ArraySort(IntSort(), IntSort()), "
            else:    
                invariant += "IntSort(), "
        else:
            if name.endswith("[ ]"):
                invariant += "ArraySort(IntSort(), RealSort()), "
            else:    
                invariant += "RealSort(), "
    invariant += "BoolSort())"
    return invariant
                
def add_assert_rule(r, first_t, last_t, first_i, last_i, variables_string, variables):
    first_t_list = list(trim_whitespace(first_t)[1:-1].split(","))
    last_t_list = list(trim_whitespace(last_t)[1:-1].split(","))
    rule = "ForAll(["+variables_string[1:-1]+"], Implies (And ("
    for i in range(len(first_t_list)):
        if first_t_list[i] != last_t_list[i]:
            rule += trim_whitespace(last_t_list[i])+"_last == " + first_t_list[i] + ", "
    rule += first_i + ", "
    rule += r + ", "
    rule += "Not(" + last_i + ")), "
    rule += "False))"
    return rule
    
def add_rule(r, first_t, last_t, first_i, last_i, variables_string, variables):
    first_t_list = list(trim_whitespace(first_t)[1:-1].split(","))
    last_t_list = list(trim_whitespace(last_t)[1:-1].split(","))
    rule = "ForAll(["+variables_string[1:-1]+"], Implies (And ("
    for i in range(len(first_t_list)):
        if first_t_list[i] != last_t_list[i]:
            rule += trim_whitespace(last_t_list[i])+"_last == " + first_t_list[i] + ", "
            last_i = last_i.replace(" "+trim_whitespace(last_t_list[i])+" ", " "+trim_whitespace(last_t_list[i])+"_last " )
    rule += first_i + ", "
    rule += r + "), "
    rule += last_i+"))"
    return rule
    

def add_route (route, cfg, s):
    first = route[0]
    last = route[len(route)-1]
    variables = cfg[first.get("id")].get("variables")
    for variable in variables: #declare functions variables
        type = variable.get("type")
        name = variable.get("name")
        name = trim_whitespace(name)
        if type == " int ":
            if name.endswith("[ ]"):
                name = name[:-4]
                exec(name+" = Array('"+name+"', IntSort(), IntSort())")
                exec(name+"_last = Array('"+name+"_last', IntSort(), IntSort())")
            else:
                exec(name+" = Int('"+name+"')")
                exec(name+"_last = Int('"+name+"_last')")
        else:
            if type == " double ":
                if name.endswith("[ ]"):
                    name = name[:-4]
                    exec(name+" = Array('"+name+"', IntSort(), RealSort())")
                    exec(name+"_last = Array('"+name+"_last', IntSort(), RealSort())")
                else:
                    exec(name+" = Real('"+name+"')")
                    exec(name+"_last = Real('"+name+"_last')")
    r = " "+trim_whitespace(first.get("R"))+" "
    first_t = " "+trim_whitespace(first.get("T"))+" "
    last_t = " "+trim_whitespace(last.get("T"))+" "
    variables_string = " "+trim_whitespace(last.get("T"))+" "               
    first_i = " "+trim_whitespace(first.get("I"))+" "
    if first_i.startswith(" Invr"): 
        exec(declare_invariant(first_i, variables))
    last_i = " "+trim_whitespace(last.get("I"))+" "
    if last_i.startswith(" Invr"): 
        exec(declare_invariant(last_i, variables))
    if cfg[last.get("id")].get("type") == "assert":
        exec(add_assert_rule(r, first_t, last_t, first_i, last_i, variables_string, variables))
    else:
        exec(add_rule(r, first_t, last_t, first_i, last_i, variables_string, variables))
    
def verify_function (function, cfg):
    s = SolverFor("HORN")
    function_id =  function[0][0].get("id")
    function_name = cfg[function_id].get("label")
    for route in function:
        add_route(route, cfg, s)
    if s.check() != sat:
        print ("Failed to verify function:" + function_name)
    else:
        print ("Invariants for function: " + function_name)
        print(s.model())
        
def verify_program (routes, cfg):
    print("Attempting to verify program...")
    for function in routes:
        verify_function (function, cfg)
    print ("Done!") 
    
def trim_whitespace (string):
    string = " ".join(string.split())
    return string
