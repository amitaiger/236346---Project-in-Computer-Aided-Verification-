import json
import cfg
import fol    

with open("max3.c.ast.json") as f:
    data = json.load(f)
    
program_cfg = {}  
cfg.create_cfg (data, program_cfg, "end", [])
print(json.dumps(program_cfg, indent = 4))
routes = []
cfg.find_routes (program_cfg, routes)
fol.produce_fol_routes (program_cfg, routes)
print(json.dumps(program_cfg, indent = 4))
print(json.dumps(routes, indent = 4))
