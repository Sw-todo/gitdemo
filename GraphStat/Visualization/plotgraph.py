import matplotlib.pyplot as plt
import numpy as np
def plotdegree_distribution(graph,range=-1):
    '''

    :param graph:图结构
    :param range:范围，默认为-1，即全部的分布
    :return:
    '''
    dicdata =sum(list(map(list,graph['edges'].keys())),[])
    edge_array=np.asarray(dicdata)
    #print(dicdata)
    #print(edge_array)
    key=np.unique(edge_array)
    print(key)
    degree={}
    for i in key:
        mask = (edge_array == i)
        arr_new=edge_array[mask]
        value = arr_new.size
        degree[i]=value

    degrees=np.array(list(degree.values()))
    key = np.unique(degrees)
    static={}
    for i in key:
        mask = (degrees == i)
        arr_new=degrees[mask]
        value = arr_new.size
        static[i]=value
    by_key = sorted(static.items(), key=lambda item: item[0], reverse=True)
    x = []
    y = []
    plt.yticks(fontsize=7)
    for d in by_key:
        x.append(d[0])
        y.append(d[1])
    #if heng == 0:
    #figure = plt.bar(x[0:range], y[0:range])
    figure2=plt.plot(x[0:range], y[0:range],'-')
    plt.xlabel('Degree')
    plt.ylabel('Frequence')
    #plt.savefig(file)
    plt.show()
    return



