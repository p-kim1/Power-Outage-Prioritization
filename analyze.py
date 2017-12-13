import sys
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

def main():
    resultFile = open(sys.argv[1],"r")
    county = []
    norm = open("norm_countyData.arff","r")
    for line in norm:
        if(line[0] not in ["@","\n"]):
            county.append(line.split(",")[-1][:-1])
    norm.close()

    index = 0
    clusterDict = {} #Key: cluster; #Value: county
    priorityDict = {} #Key: cluster; #Value: list of sums of each feature value
    for line in resultFile:
        if(line[0] not in ["@","\n","{"]):
            attValues = list(map(float,line.split(",")[:4]))
            cluster = line.split(",")[-1][:-1]
            if(cluster not in clusterDict.keys()):
                clusterDict[cluster] = []
            if(cluster not in priorityDict.keys()):
                priorityDict[cluster] = [[0]*4,0]
            clusterDict[cluster].append(county[index])
            for i in range(0,4):
                priorityDict[cluster][0][i] += attValues[i]
            priorityDict[cluster][1] += 1
            index += 1
    resultFile.close()

    #Obtain magnitudes of cluster centers
    for k in priorityDict.keys():
        priorityDict[k][0] = [i / priorityDict[k][1] for i in priorityDict[k][0]]
        priorityDict[k] = (sum(i**2 for i in priorityDict[k][0]))**.5

    #Set cluster bar colors by priority
    cBins = []
    colors = [[1,0,0]]
    acc = 0
    pSort, keySort = zip(*sorted(zip(priorityDict.values(), priorityDict.keys()),reverse = True))
    for k in keySort:
        cBins.append(len(clusterDict[k])*[int(k[-1:])])
        if(len(keySort) < 5):
            colors.append([1,0.2*(acc+1),0.2*(acc+1)])
        acc += 1 

    #Make histogram
    colors = colors[:-1]
    plt.title(sys.argv[1][:-5])
    plt.hist(cBins,color = colors,label = keySort)
    plt.legend(bbox_to_anchor=(1.04,1), loc='upper left', ncol=1)
    fig = plt.gcf()
    plt.text(len(keySort)*1.05,10,"Note: Darker red\nindicates higher\npriority. Clusters\nare arranged\nfrom highest to\nlowest priority.")
    fig.subplots_adjust(right=0.7)
    plt.show()

main()
