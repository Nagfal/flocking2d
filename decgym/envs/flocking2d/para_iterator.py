
def next_parameters(best_samples=[],parameters_range={}):
    for p in parameters_range:
        p_list = []
        for example in best_samples:
            p_list.append(example[p])
        parameters_range[p][0] = min(p_list) *0.3 + parameters_range[p][0]*0.7
        parameters_range[p][1] = max(p_list) *0.3 + parameters_range[p][1]*0.7
    return parameters_range