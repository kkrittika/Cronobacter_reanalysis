#!/bin/python
'''
This script reads in the investigations information
and the pairwise distances created by the perl distance script 
to either retain the pairwise comparisons between samples, get a range of distances
for samples within an investigation or compare samples between two investigations.
Author:Krittika Krishnan; Date: 19th July 2024
'''
import argparse

#Filter pairwise comparisons to those within the same investigation
def filterDist(infofile,distfile):
    investigations = {}
    with open(infofile,'r') as f:
        for line in f:
            line = line.strip()
            strain = line.split("\t")[0]
            info = line.split("\t")[1].replace(" ","_")
            if strain not in investigations.keys():
                investigations[strain] = info
    
    with open(distfile,'r') as f2:
        for line2 in f2:
            line2 = line2.strip()
            tmp = line2.split("\t")
            
            if tmp[0] and tmp[1] in investigations.keys():
                #Checking if sample1 and sample2 belong to the same investigations
                if investigations[tmp[0]] == investigations[tmp[1]]:
                    # print(tmp[0]+"\t"+tmp[1]+"\t"+str(int(tmp[4])-int(tmp[3])))
                    
                    # printout the pairwise comparisons along with investigation info - July 30th
                    print(f'{tmp[0]}\t{investigations[tmp[0]]}\t{tmp[1]}\t{investigations[tmp[1]]}\t{tmp[3]}\t{tmp[4]}')
                    
#  Getting the distance range for samples within the same investigations
def intraCompare(infofile,distfile):
    investigations = {}
    inv_format = {}
    newentry = []

    with open(infofile,'r') as f:
        for line in f:
            line = line.strip()
            strain = line.split("\t")[0]
            info = line.split("\t")[1].replace(" ","_") #Get rid of the space in the investigation name
            if strain not in investigations.keys():
                investigations[strain] = info
            #Creating another dict with a different organization of strain and investigation info
            if not info in inv_format.keys():
                inv_format[info] = []
            inv_format[info].append(strain) #{Investigation:[sample1,sample2,...]}

    with open(distfile,'r') as f2:
        f2.readline()
        for line2 in f2:
            line2 = line2.strip()
            tmp = line2.split("\t")
            #Get the investigation names for each sample
            smpl1 = investigations[tmp[0]]
            smpl2 = investigations[tmp[1]]
            #Calculate the distance
            diff = str(int(tmp[4]) - int(tmp[3]))
            newentry.append([tmp[0],smpl1,tmp[1],smpl2,diff])
            

        investigations_list = list(inv_format.keys())
        #Comparisons within investigations
        for key in range(len(investigations_list)):
            for key2 in range(len(investigations_list)):
               
                distvalue = []
                comp1 = ''
                comp2 = ''
                
                for sample in newentry:
                    if investigations_list[key] == investigations_list[key2]:
                        if sample[1] == investigations_list[key] and sample[3] == investigations_list[key2]:
                            distvalue.append(int(sample[4]))
                            comp1 = investigations_list[key]
                            comp2 = investigations_list[key2]
                
                if distvalue:
                    print(f'{comp1},{comp2},{min(distvalue)},{max(distvalue)}')



def investiCompare(infofile,distfile):
    investigations = {}
    inv_format = {}
    newentry = []

    with open(infofile,'r') as f:
        for line in f:
            line = line.strip()
            strain = line.split("\t")[0]
            info = line.split("\t")[1].replace(" ","_") #Get rid of the space in the investigation name
            if strain not in investigations.keys():
                investigations[strain] = info
            #Creating another dict with a different organization of strain and investigation info
            if not info in inv_format.keys():
                inv_format[info] = []
            inv_format[info].append(strain) #{Investigation:[sample1,sample2,...]}

    with open(distfile,'r') as f2:
        f2.readline()
        for line2 in f2:
            line2 = line2.strip()
            tmp = line2.split("\t")
            #Get the investigation names for each sample
            smpl1 = investigations[tmp[0]]
            smpl2 = investigations[tmp[1]]
            #Calculate the distance
            diff = str(int(tmp[4]) - int(tmp[3]))
            newentry.append([tmp[0],smpl1,tmp[1],smpl2,diff])
            

        investigations_list = list(inv_format.keys())
        #Comparisons across investigations
        for key in range(len(investigations_list)):
            for key2 in range(len(investigations_list)):
               
                distvalue = []
                comp1 = ''
                comp2 = ''
                
                for sample in newentry:
                    if (sample[1] == investigations_list[key] and sample[3] == investigations_list[key2]) or (sample[1] == investigations_list[key2] and sample[3] == investigations_list[key]) :
                        # print(sample)
                        distvalue.append(int(sample[4]))
                        comp1 = investigations_list[key]
                        comp2 = investigations_list[key2]
                
                if distvalue:
                    print(f'{comp1},{comp2},{min(distvalue)},{max(distvalue)}')
                
        

def main():
    parser = argparse.ArgumentParser('Pairwise distance intra cronobacter investigations')
    parser.add_argument('--infofile','-i',help='File containing investigation information per sample')
    parser.add_argument('--distfile','-d',help='File with calculated pairwise distances')
    parser.add_argument('--mode','-m',help='Choose between "filter", "intra" or "inter" for investigation-wise filtering')
    

    args = parser.parse_args()
    infofile = args.infofile
    distfile = args.distfile
    mode = args.mode
    if mode == "intra":
        intraCompare(infofile,distfile)
    elif mode == "inter":
        investiCompare(infofile,distfile)
    elif mode == "filter":
        filterDist(infofile,distfile)
    

if __name__ == '__main__':
    main()
