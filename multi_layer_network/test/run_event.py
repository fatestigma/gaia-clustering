from baseline2_exe import run_with_file_io

output = "/Users/dongyuli/isi/data/jl_1003r1nl/"
entity_edgelist = output + "entity.edgelist"
entity_json = output + "entity.json"
event_json = output + "event.json"

run_with_file_io(entity_edgelist, entity_json, event_json, output)
