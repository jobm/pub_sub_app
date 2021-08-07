from ortools.constraint_solver import pywrapcp, routing_enums_pb2


def run_route_optimizer(data):
    manager = pywrapcp.RoutingIndexManager(
        len(data['distance_matrix']),
        data['num_vehicles'], data['depot'])
    routing = pywrapcp.RoutingModel(manager)
    transit_callback_index = routing.RegisterTransitCallback(
        lambda x, y:
        data["distance_matrix"][manager.IndexToNode(x)][manager.IndexToNode(y)]
    )
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    solution = routing.SolveWithParameters(search_parameters)
    solution_data = []
    if solution:
        idx = routing.Start(0)
        route_distance = 0
        while not routing.IsEnd(idx):
            solution_data.append(manager.IndexToNode(idx))
            prev_idx = idx
            idx = solution.Value(routing.NextVar(idx))
            route_distance += routing.GetArcCostForVehicle(prev_idx, idx, 0)
    return solution_data
