import numpy as np
import sys

def main():
    dataset = open(sys.argv[1],"r")
    matrix = []
    arffFormat = []
    county = []
    for line in dataset:
        if line[0] not in ["\n","@"]:
            matrix.append(list(map(float,line.split(",")[:-1])))
            county.append(line.split(",")[-1])
        else:
            arffFormat.append(line)
    matrix = np.matrix(matrix)
    dataset.close()

    #Normalize features from 0 to 1
    for i in range(0,np.shape(matrix)[1]):
        maxVal = np.max(matrix[:,i])
        minVal = np.min(matrix[:,i])
        matrix[:,i] = (matrix[:,i] - minVal)/(maxVal - minVal)

    #Create new dataset with normalized features
    normData = open("norm_"+sys.argv[1],"w")
    for line in arffFormat:
        normData.write(line)
    for i in range(0,np.shape(matrix)[0]):
        line = np.ndarray.tolist(matrix[i,:])[0]
        line = ",".join(list(map(str,line))) + "," + county[i]
        normData.write(line)
    normData.close()
main()
