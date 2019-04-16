import sys
import numpy as np

argnum = len(sys.argv);
arglist = sys.argv[1:];

print(arglist)

if argnum < 3:
    raise Exception('Not enough arguments')

lists = [];
tempf = [];
try:
    for filename in arglist:
        tempf = open(filename,'r');
        templines = tempf.readlines();
        tempf.close();
        list = [(int(node),float(value)) for (node,value) in map(lambda x: x.split(),templines)];
        lists.append(list);
except:
    raise Exception('Could not import lists from files')
    sys.exit(2);

def RBO(r1,r2,p,k):
    #Rank-Biased Overlap.
    #input
    #   A, B: the ranks to be compared. r[i] should be a tuple containing all ties at rank i.
    #   p: stopping probability, an RBO parameter. 0.9 will put 86% of the weight on the first 10 elements, 0.98 on the first 50.
    #   k: the depth up to which compare the lists. 0 will compare the whole lists.
    #
    # the algorithm assumes no doubles
    
    m = min(len(r1),len(r2));
    if (k <= 0) or (k > m):
        #use full lists
        k = m;
    
    A = set([]);
    B = set([]);
    RBO = 0.;
    AG = 0.;
    X = 0.;
    for i in range(k):
        a = set(r1[i]);
        b = set(r2[i]);
        
        #update agreement between lists. Take cares of ties.
        AG += len(A.intersection(b)) + len(B.intersection(a)) + len(a.intersection(b));
        
        #add every element of a and b to the corresponding set.
        A = A.union(a);
        B = B.union(b);
        
        #RBO agreement manipulations
        X = 2*AG/(len(A)+len(B));
        
        #print(a,b,A,B,AG,X,RBO);
        X *= (p**(i+1))/p;
        if i != (k-1):
            X *= (1-p);
        
        RBO += X;
    return RBO;


def list2rank(lista):
    #create rank from disordered name-value list; put ties together.
    
    val = lambda x: x[1];
    ord = sorted(lista,key = val); #sort the list by second column;
    
    ranked = [[ord[0][0],]]; #elements of this list will be ties-tuples
    k = 0;
    for i in range(1,len(ord)):
        if ord[i][1] == ord[i-1][1]:
            #put together equal values
            ranked[k].append(ord[i][0]);
        else:
            #create new tuple for new values
            k +=1;
            ranked.append([ord[i][0],]);
    return ranked;

ranks = [list2rank(l) for l in lists];
for i in range (15):
    print(RBO(ranks[0],ranks[1],0.9,i));


