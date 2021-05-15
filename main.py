import json
import cfg
import fol 
import verification   

with open("arraysloops.c.ast.json") as f:
    data = json.load(f)
    
program_cfg = {}  
cfg.create_cfg (data, program_cfg, "end", [])
routes = []
cfg.find_routes (program_cfg, routes)
fol.produce_fol_routes (program_cfg, routes)
print(json.dumps(program_cfg, indent = 4))
print(json.dumps(routes, indent = 4))
verification.verify_program (routes, program_cfg)
