from z3 import *

def verify_route (route, cfg):
    s = Solver()
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
                exec(name+"_last = Array('"+name+"', IntSort(), IntSort())")
            else:
                exec(name+" = Int('"+name+"')")
                exec(name+"_last = Int('"+name+"')")
        else:
            if type == " double ":
                if name.endswith("[ ]"):
                    name = name[:-4]
                    exec(name+" = Array('"+name+"', IntSort(), RealSort())")
                    exec(name+"_last = Array('"+name+"', IntSort(), RealSort())")
                else:
                    exec(name+" = Real('"+name+"')")
                    exec(name+"_last = Real('"+name+"')")
    first_i = trim_whitespace(first.get("I"))
    r = trim_whitespace(first.get("R"))
    t = trim_whitespace(first.get("T"))
    last_i = trim_whitespace(last.get("I"))
    first_t_list = list(trim_whitespace(first.get("T"))[1:-1].split("|"))
    last_t_list = list(trim_whitespace(last.get("T"))[1:-1].split("|"))
    for i in range(len(first_t_list)): #declare variables used with last assert
        exec("s.add("+trim_whitespace(last_t_list[i])+"_last == "+trim_whitespace(first_t_list[i])+")")
        last_i = last_i.replace(last_t_list[i], " "+trim_whitespace(last_t_list[i])+"_last"+" ")
    exec("s.add(Not(Implies(And("+first_i+", "+r+"), "+last_i+")))") #negation of floyd's rule
    if s.check() == sat:
        print("Error in route ("+first.get("id")+") -> ("+last.get("id")+")")
        #print (s.model())

def trim_whitespace (string):
    string = " ".join(string.split())
    return string

def verify_program (routes, cfg):
    print("Attempting to verify program...")
    for route in routes:
        verify_route (route, cfg)
    print ("Done!") 
