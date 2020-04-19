import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from pylab import *         #支持中文

def histogram(labels,quants, xname, yname):
    labels = list(labels)
    quants = list(quants)
    l = len(labels)
    width = 0.4
    ind = np.linspace(0.5, 0.5+l-1, l)
    # make a square figure
    fig = plt.figure(1)
    ax  = fig.add_subplot(111)
    # Bar Plot
    ax.bar(ind-width/2,quants,width,color='green')
    # Set the ticks on x-axis
    ax.set_xticks(ind)
    ax.set_xticklabels(labels)
    # labels
    ax.set_xlabel(xname)
    ax.set_ylabel(yname)
    # title
    # ax.set_title('Top 10 GDP Countries', bbox={'facecolor':'0.8', 'pad':5})
    plt.grid(True)
    plt.show()

def broken_line_chart(x, y, xname, yname):
    import matplotlib.pyplot as plt
    mpl.rcParams['font.sans-serif'] = ['SimHei']

    x = list(x)
    y = list(y)
    plt.plot(x, y, marker='o', mec='r', mfc='w',label='')
    plt.legend() # 让图例生效
    plt.margins(0)
    plt.subplots_adjust(bottom=0.15)
    plt.xlabel(xname) #X轴标签
    plt.ylabel(yname) #Y轴标签
    #plt.title("A simple plot") #标题

    plt.show()




# labels   = ['USA', 'China', 'India', 'Japan', 'Germany', 'Russia', 'Brazil', 'UK', 'France', 'Italy']

# quants   = [15094025.0, 11299967.0, 4457784.0, 4440376.0, 3099080.0, 2383402.0, 2293954.0, 2260803.0, 2217900.0, 1846950.0]

# draw_bar(labels,quants)
