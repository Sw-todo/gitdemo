import matplotlib.pyplot as plt
from GraphStat.Graph import stat
def plot_nodes_weight(graph,file,RANGE=-1,heng=0):#dicdata：字典的数据。
    #RANGE：截取显示的字典的长度。
    #heng=0，代表条状图的柱子是竖直向上的。heng=1，代表柱子是横向的。考虑到文字是从左到右的，让柱子横向排列更容易观察坐标轴。
    dicdata=stat.get_weight_distribution(graph)
    by_value = sorted(dicdata.items(),key = lambda item:item[1],reverse=True)
    x = []
    y = []
    plt.yticks( fontsize=7)
    for d in by_value:
        x.append(d[0])
        y.append(d[1])
    if heng == 0:
        figure=plt.bar(x[0:RANGE], y[0:RANGE])
        plt.savefig(file)
        plt.show()
        return
    elif heng == 1:
        figure=plt.barh(x[0:RANGE],y[0:RANGE] )
        plt.savefig(file)
        plt.show()
        return
    else:
        return "heng的值仅为0或1！"
