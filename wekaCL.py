import os
import subprocess
import shlex
import sys

def main():
    #NOTE: If environment variable not set manually, must choose 'y' every time wekaCL.py is run
    env = dict(os.environ)
    setPath = input("Add weka.jar to CLASSPATH environment variable? [y/n]: ") 
    if(setPath == "y"):
        print("Adding weka.jar to CLASSPATH...")
        os.system("find /home -name weka.jar 2>&1 | grep -v 'Permission denied' > log.txt")
        log = open("log.txt","r")
        wekaPath = log.readline()
        log.close()
        env['CLASSPATH'] = '.:' + wekaPath[:-1] + ':.:'        
        os.remove("log.txt")
    print("Initializing input file...")
    cmd = shlex.split("java weka.filters.unsupervised.attribute.Remove -R 5 -i norm_countyData.arff -o temp.arff")
    cmdTemp = subprocess.call(cmd,env=env)
    
    #Check if weka.jar added to CLASSPATH
    if(cmdTemp):
        print("Error: Weka could not be run. Please add weka.jar to the CLASSPATH environment variable.")
        sys.exit()
    

    #Run K-means, Expectation Maximization, or Hierarchical
    loop = "y"
    while(loop == "y"):
        print("Choose a clustering algorithm: ")
        print("1) K-means")
        print("2) Expectation Maximization")
        print("3) Hierarchical")
        cluster = input("[1/2/3]: ")
        while(cluster not in ['1','2','3']):
            cluster = input("Please choose 1, 2, or 3: ")

        #K-means with either Euclidean or Manhattan distance
        if(cluster == "1"):
            print("Choose a distance function: ")
            print("1) Euclidean")
            print("2) Manhattan")
            dist = input("[1/2]: ")
            while(dist not in ['1','2']):
                dist = input("Please choose 1 or 2: ")
            print("Running K-means for K = 2, 3 and 4...")
            for i in range(2,5):
                if(dist == '1'):
                    kfile = "kmeansEuclid"+str(i)+".arff"
                    cmd = shlex.split('java weka.filters.unsupervised.attribute.AddCluster -W "weka.clusterers.SimpleKMeans -N ' + str(i) + '" -i temp.arff -o ' + kfile)
                    subprocess.call(cmd,env=env)
                if(dist == '2'):
                    kfile = "kmeansMan"+str(i)+".arff"
                    cmd = shlex.split('java weka.filters.unsupervised.attribute.AddCluster -W "weka.clusterers.SimpleKMeans -N ' + str(i) + ' -A weka.core.ManhattanDistance" -i temp.arff -o ' + kfile)
                    subprocess.call(cmd,env=env)

        #Expectation Maximization
        if(cluster == "2"):
            print("Running Expectation Maximization...")
            cmd = shlex.split('java weka.filters.unsupervised.attribute.AddCluster -W "weka.clusterers.EM" -i temp.arff -o EM.arff')
            subprocess.call(cmd,env=env)

        #Hierarchical with either Euclidean or Manhattan distance
        if(cluster == "3"):
            print("Choose a distance function: ")
            print("1) Euclidean")
            print("2) Manhattan")
            dist = input("[1/2]: ")
            while(dist not in ['1','2']):
                dist = input("Please choose 1 or 2: ")
            print("Running Hierarchical Clustering for K = 2, 3 and 4...")
            for i in range(2,5):
                if(dist == '1'):
                    hfile = "hierarchicalEuclid"+str(i)+".arff"
                    cmd = shlex.split('java weka.filters.unsupervised.attribute.AddCluster -W "weka.clusterers.HierarchicalClusterer -L AVERAGE -N ' + str(i) + '" -i temp.arff -o ' + hfile)
                    subprocess.call(cmd,env=env)
                if(dist == '2'):
                    hfile = "hierarchicalMan"+str(i)+".arff"
                    cmd = shlex.split('java weka.filters.unsupervised.attribute.AddCluster -W "weka.clusterers.HierarchicalClusterer -A weka.core.ManhattanDistance -L AVERAGE -N ' + str(i) + '" -i temp.arff -o ' + hfile)
                    subprocess.call(cmd,env=env)

        loop = input("Result files written. Run another algorithm? [y/n]: ")
    os.remove("temp.arff")
main()
