import argparse
import os
import hashlib

def pair_finder(map, index):
    keys = map.keys()
    final = []
    list = []
    for x in keys:
        list.append(x)
    n = len(list)
    for i in range(0,n-1):
        if final == []:
            final.append([(list[i],map.get(list[i])[2])])
            continue
        for j in final:
            if map.get(list[i])[index] == map.get(j[0][0])[index]:
                j.append((list[i],map.get(list[i])[2]))
                break
        else:
            final.append([(list[i],map.get(list[i])[2])])
    
    result = []
    for y in final:
        if len(y) > 1:
            result.append(sorted(y, key = lambda x : x[0]))
                
    
    return result
def ult_pair_finder(map):
    keys = map.keys()
    final = []
    list = []
    for x in keys:
        list.append(x)
    n = len(list)
    for i in range(0,n-1):
        if final == []:
            final.append([(list[i],map.get(list[i])[2])])
            continue
        for j in final:
            if map.get(list[i])[0] == map.get(j[0][0])[0] and map.get(list[i])[1] == map.get(j[0][0])[1]:
                j.append((list[i],map.get(list[i])[2]))
                break
        else:
            final.append([(list[i],map.get(list[i])[2])])
    
    result = []
    for y in final:
        if len(y) > 1:
            result.append(sorted(y, key = lambda x : x[0]))
                
    
    return result    
    

parser = argparse.ArgumentParser(prog = 'dene')
parser.add_argument("-d", action="store_true", default = False)
parser.add_argument("-f", action="store_true",default= False)
parser.add_argument("-c",action="store_true",default= False)
parser.add_argument("-n",action="store_true",default=False)
parser.add_argument("-cn", action="store_true",default=False)
parser.add_argument("-s",action="store_true",default=False)
parser.add_argument("strings",nargs = '*',default=".")
args = parser.parse_args()

if args.d and args.f is True:
    print("cannot call both -d and -f")
    exit()
   
isDir = False
isFile = True
if args.d is True:
    isDir= True
    isFile= False
isContent = True
isName = False
isSize = args.s
if args.n is True:
    if args.c or args.cn is True:
        print("error")
        exit()
    isName = True
    isContent = False
    isSize = False
elif args.cn is True:
    if args.c or args.n is True:
        print("error")
        exit()
    isName = True
    isContent = True

for currPath in args.strings:
    dirMap = dict()
    fileMap = dict()

    for root, dirs, files in os.walk(currPath,topdown = False):
        alist = os.path.split(root)# os.path.split kullanilabilir
        dirName = alist[1]
        hashList = []
        nameHashList=[]
        dirSize = 0
        nameHash = hashlib.sha256(dirName.encode()).hexdigest()
        if dirs == [] and files == []:
            emptyCont = hashlib.sha256("".encode()).hexdigest()
            dirMap[root] = [emptyCont, nameHash,dirSize]
            continue #continue for empty directory 
        
            
        for direct in dirs:
            x = os.path.join(root, direct)
            hashList.append(dirMap.get(x)[0])
            nameHashList.append(dirMap.get(x)[1])
            dirSize += dirMap.get(x)[2]
            
        for file in files:
            y = os.path.join(root,file)
            content = open(y).read()
            sHash = hashlib.sha256(content.encode()).hexdigest()
            size = os.path.getsize(y)
            fnameHash = hashlib.sha256(file.encode()).hexdigest()
            fileMap[y] = [sHash, fnameHash, size]
            hashList.append(sHash)
            nameHashList.append(fnameHash)
            dirSize += size
            
        hashList.sort()
        nameHashList.sort()
        str = ""
        nameStr = nameHash
        for hshs in hashList:
            str += hshs
        for kmkm in nameHashList:
            nameStr += kmkm
        dirHash = hashlib.sha256(str.encode()).hexdigest()
        dirNameHash = hashlib.sha256(nameStr.encode()).hexdigest()
        dirMap[root] = [dirHash, dirNameHash,dirSize] 

    #now processing part
    #choosing the map
    finalMap = {}
    if isDir:
        finalMap = dirMap
    else:
        finalMap = fileMap
    theList = []
    if isContent and isName:
        theList = ult_pair_finder(finalMap)
    elif isContent:
        theList = pair_finder(finalMap,0)
    else:
        theList = pair_finder(finalMap,1)
    if isSize:
        theList = sorted(theList, key = lambda x : x[0][1], reverse = True)    #this is a problem

    for paths in theList:
        ch = ""
        for x in paths:
            if isSize:
                ch = x[1]
            print(x[0] , "  ", ch)
        print()    
    







