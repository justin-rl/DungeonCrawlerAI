from geralt.path_finding import a_star

def optimal_path(start, end, objectives, maze):
    traveling_path = [start]
    for o in objectives:
        traveling_path.append(o)
    traveling_path.append(end) 
    return traveling_path