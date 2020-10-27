import node
def cal_average_dgree(graph):
    '''平均度数求取

    :param graph: 图结构
    :return: float or int 平均度数
    '''
    if (graph['forward']):
        return len(graph['edges'].keys())/len(graph['nodes'])*2
    else:
        return len(graph['edges'].keys())/len(graph['nodes'])*2
def get_weight_distribution(graph):
    '''节点权重属性的分布分析

    :param graph: 图结构
    :return: 字典，各个权重区间的分布
    '''
    weight_dict={}
    nodes=graph['nodes']
    for i in range(0,25000,1000):
        weight_dict[f'{i}:{i+999}']=sum(1 if ((int( node.get_weight(j)) >=i) & (int(node.get_weight(j))<i+1000)) else 0 for j in nodes)
    weight_dict[f'>=24000'] = sum(1 if (int(node.get_weight(j)) >= 24000 ) else 0 for j in nodes)
    return weight_dict