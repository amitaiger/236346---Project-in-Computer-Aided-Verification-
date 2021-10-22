import json
import cfg
import fol 
import verification 
import os

with open("../benchmarks/c/json/temp.ast.json") as f:
    data = json.load(f)
    
program_cfg = {}  
cfg.create_cfg (data, program_cfg, "end", [])
routes = []
cfg.find_routes (program_cfg, routes)
fol.produce_fol_routes (program_cfg, routes)
verification.verify_program (routes, program_cfg)