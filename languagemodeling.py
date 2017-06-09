import random
def viterbi(obs, states, start_p, trans_p, emit_p):
     V = [{}]
     for st in states:
         V[0][st] = {"prob": start_p[st] * emit_p[st][obs[0]], "prev": None}
     # Run Viterbi when t > 0
     for t in range(1, len(obs)):
         V.append({})
         for st in states:
             max_tr_prob = max(V[t-1][prev_st]["prob"]*trans_p[prev_st][st] for prev_st in states)

             for prev_st in states:
                #print prev_st
                if V[t-1][prev_st]["prob"] * trans_p[prev_st][st] == max_tr_prob:
                    if(obs[t] in emit_p[st]):
                       max_prob = max_tr_prob * emit_p[st][obs[t]]
                       #print max_prob
                    else:
                        max_prob=1
                    V[t][st] = {"prob": max_prob, "prev": prev_st}
                    break
     for line in dptable(V):
        print line
     opt = []
     # The highest probability
     max_prob = max(value["prob"] for value in V[-1].values())
     previous = None
     # Get most probable state and its backtrack
     for st, data in V[-1].items():
         if data["prob"] == max_prob:
             opt.append(st)
             previous = st
             break
     # Follow the backtrack till the first observation
     for t in range(len(V) - 2, -1, -1):
         opt.insert(0, V[t + 1][previous]["prev"])
         previous = V[t + 1][previous]["prev"]
     
     print 'The steps of states are ' + ' '.join(opt) + ' with highest probability of %s' % max_prob
     return opt
 
def dptable(V):
     # Print a table of steps from dictionary
    yield " ".join(("%12d" % i) for i in range(len(V)))
    for state in V[0]:
        yield "%s: " % state + " ".join("%s" % ("%.21f" % (v[state]["prob"]*100.0)) for v in V)

def transfromstartp(states, start_p):
    temp={}
    grandtotal=0.0
    for state in start_p:
        grandtotal+=start_p[state]
    for state in states:
        if state in start_p:
            temp[state]=start_p[state]/grandtotal
        else:
            temp[state]=0.00000000000000000001   # I assume this is good enough?                         
    return temp

def remove_duplicates(l):
   return list(set(l))    
def transfromemitp(states, emit_p, obs):
    temp={}
    for state in states:
        grandtotal=0.0
        temp[state]={}
        for word in obs:
            if word in emit_p[state]:
                temp[state][word]=emit_p[state][word]/float(len(obs))
            else:
                temp[state][word]=0.00000000000000000001   
    return temp    
def transfromtransp(states, transp):
   temp={}
   for state1 in states:
          grandtotal=0.0
          for state2 in states:
              if state2 in transp[state1]:
                 grandtotal+=transp[state1][state2]
              else:
                 transp[state1][state2]=0.00000000000000000001
          temp[state1]={}        
          for state2 in states:
             temp[state1][state2]=transp[state1][state2]/grandtotal
   return temp


infilename="something.txt"
trainingdata=open(infilename).read()
obs=[]
states=[]
start_p={}
transp={}
emit_p={}
start=True
previous=""
for word in trainingdata.split():
   array=word.split('_')
   obs.append(array[0])
   states.append(array[1])
   if start==True:
    if array[1] not in start_p:
      start_p[array[1]]=1
    else:  
      start_p[array[1]]=start_p[array[1]]+1
    start=False
   if array[1]==".":
     start=True
   if previous!="":
     if previous not in transp:
        transp[previous]={}
        transp[previous][array[1]]=1
     elif array[1] not in transp[previous]:
        transp[previous][array[1]]=1
     else: 
        transp[previous][array[1]]=transp[previous][array[1]]+1
   previous=array[1]
   if array[1] not in emit_p:
     emit_p[array[1]]={} 
     emit_p[array[1]][array[0]]=1
   elif array[0] not in emit_p[array[1]]:
     emit_p[array[1]][array[0]] =1
   else:
     emit_p[array[1]][array[0]]=emit_p[array[1]][array[0]]+1
obs=remove_duplicates(obs)
states=remove_duplicates(states)
start_p=transfromstartp(states, start_p)
transp=transfromtransp(states,transp)
emit_p=transfromemitp(states, emit_p, obs)
#print len(transp)
#print len(states)
#print obs
#print states
#print start_p
#print transp
#print transp.keys()
#print transp["PRP$"]['FW']
#print emit_p['.']['a']
infilename="testing.txt"
testingdata=open(infilename).read() 
test=[]
compare=[]
for word in testingdata.split():
  temp=word.split("_")
  #print temp[0]
  test.append(temp[0])
  compare.append(temp[1])

stuff=viterbi(test, states, start_p, transp, emit_p)
i=0
good=0.0
total=len(compare)
for word in stuff:
  if word==compare[i]:
    good+=1.0
  i+=1  
print "my accuracy is this ",good/total    






