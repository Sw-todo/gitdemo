#节点读入、输出
import jieba
import GraphStat.Graph.graph as graph
import GraphStat.Graph.stat as stat
from GraphStat.Visualization import plotnodes
from GraphStat.Visualization import plotgraph
def init_nodes(file,encoding="UTF-8"):
    """实现文件读取，并读取其中的节点信息

    :param file: 字符串，相关节点文件路径
    :param encoding:
    :return:字典列表，列表包含各个node的属性字典
    """
    node_list = []
    with open(file , encoding=encoding ) as f:
        next(f)
        f=f.read().split("\n")
        for nodes in f:
            if(nodes!='*Edges'):
                node_list.append(init_node(nodes))
            else:
                break
    return node_list
def init_node(parmaters):
    '''实现节点信息字典化存储

    :param parmaters: 句子
    :return: 字典，key为各个属性，value为属性值
    '''
    node_contain = ['id', 'name', 'weight', 'class', 'other']
    a = parmaters.split("\t")
    other = a.pop(-1)
    a = a + [list(other.split(';')[:-1])]
    return {node_contain[i]: a[i] for i in range(len(a))}

def _get_attr_(node,key):
    '''读取node的相关key值

    :param node: 节点字典
    :param key: 属性名字
    :return: 字符串
    '''
    return node[key]

def get_id(node):
    '''get_xx皆类似

    :param node: 字典，节点
    :return: 字符串，属性值
    '''
    return _get_attr_(node,'id')

def get_name(node):
    return _get_attr_(node, 'name')
def get_class(node):
    return _get_attr_(node, 'class')
def get_weight(node):
    return _get_attr_(node,'weight')
def edges(file,encoding="UTF-8",with_forward=False):
    """读取文件中的边信息

    :param file: 字符串，相关节点文件路径
    :param encoding:
    :param with_forward: 布尔值，是否为无向图
    :return:字典，key为：turple形式，value为int，表示边的权重，无向图边按照（i,j）的方式存储，i<j
    """
    edge_dict={}
    with open(file , encoding=encoding ) as f:
        edge=f.readline().strip().split("\t")
        while(len(edge)!=3):
            edge = f.readline().strip().split("\t")
        while(edge!=[""]):
            edge = list(map(int, edge))
            if with_forward:
                edge_dict[tuple(edge[0:-1])] = edge_dict.get(tuple(edge[0:-1]), 0) + edge[-1]
            else:
                if (edge[0]<=edge[1]):
                    edge_dict[tuple(edge[0:-1])]=edge_dict.get(tuple(edge[0:-1]),0)+edge[-1]
                else:
                    edge_dict[tuple(edge[0:-1:-1])] = edge_dict.get(tuple(edge[0:-1:-1]), 0) + edge[-1]

            edge =  f.readline().strip().split("\t")

    return edge_dict


def print_node(node):
    '''

    :param node: 字典列表，存储node
    :return:None
    '''
    node_contain = ['id', 'name', 'weight', 'class', 'other']
    for i in node:
        for j in range(len(node_contain)):
            print(f'  {node_contain[j]}: {i[node_contain[j]]}',end='')
        print('\n')
    return None
if __name__=="__main__":
    # a=init_nodes(r'D:\大学资料\大三上资料\现代程序设计\数据\newmovies.txt')
    # print(f'id:{get_id(a[1])}   name:{get_name(a[1])}')
    # b=edges(r'D:\大学资料\大三上资料\现代程序设计\数据\newmovies.txt')
    # print(list(b.items())[:5])
    # c=graph.init_graph(a,b)
    # print(f'图结构组成成分：{c.keys()}')
    # graph.save_graph(c,r'D:\大学资料\大三上资料\现代程序设计\GraphStat\cad')
    # d=graph.load_graph(r'D:\大学资料\大三上资料\现代程序设计\GraphStat\cad')
    # print(f'重载后图结构组成成分：{d.keys()}')
    # d=stat.cal_average_dgree(c)
    # print(f'平均度数：{d}')
    # e=stat.get_weight_distribution(c)
    # print(list(e.items())[:5])
    # plotnodes.plot_nodes_weight(c,r'D:\大学资料\大三上资料\现代程序设计\GraphStat\1.png',heng=1)
    # plotgraph.plotdegree_distribution(c,range=50)
    pass





