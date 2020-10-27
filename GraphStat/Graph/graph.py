import pickle
def init_graph(node_list,edges,with_forward=False):
    '''图结构建立

    :param node_list: 字典列表，列表包含各个node的属性字典
    :param edges: 字典，key为元组，存储边，value为int，存储边的权重、
    :param with_forward:类别，默认False，即无向图
    :return:字典，存储节点信息以及边信息
    '''
    return {'nodes':node_list,'edges':edges,'forward': with_forward}

def save_graph(graph,file):
    '''

    :param graph: 图结构，由init_graph生成
    :param file: 字符串，存储路径
    :return: None
    '''
    with open(file,'wb') as f:
        pickle.dump(graph,f)
    return None

def load_graph(file):
    '''

    :param file: 字符串，存储路径
    :return: 图结构
    '''
    with open(file,'rb') as f:
        return pickle.load(f)

