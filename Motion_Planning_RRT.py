import numpy
import random
import sys
import time
import matplotlib.pyplot as plt

def dist_heur(a, b, num_joints, goal):
	d = []
	dist = 0
	for i in range(0, num_joints):
		d.append(((a[i] - b[i]) * (a[i] - b[i])) + ((goal[i] - b[i]) * (goal[i] - b[i])))
	for i in range(0, num_joints):
		dist = dist + d[i]
	dist = dist ** 0.5
	return dist

def random_q(num_joints):
    qc = []
    for i in range(0,num_joints):
        qc.append(random.uniform(0,10))
    return qc

def dist(a, b, num_joints):
    d = []
    dist = 0
    for i in range(0,num_joints):
        d.append((a[i] - b[i]) * (a[i] - b[i]))
    for i in range(0,num_joints):
        dist = dist + d[i]
    dist = dist ** 0.5
    return dist

def close_node(parent, child, a, num_joints, goal):
    mindist = numpy.zeros((len(child), 2))
    for i in range(0, len(child)):
        mindist[i,0] = dist_heur(a, child[i], num_joints, goal)
        mindist[i,1] = i
    for i in range(0, len(child)):
        for j in range(1, len(child)):
                if mindist[j,0] <= mindist[j - 1,0]:
                        mindist[j-1,0], mindist[j,0] = mindist[j,0], mindist[j-1,0]
                        mindist[j-1,1], mindist[j,1] = mindist[j,1], mindist[j-1,1]
    
    return child[int(mindist[0,1])], int(mindist[0,1])

def new_node_func(a,b,n, num_joints):
    nv = []
    for i in range(0,num_joints):
        nv.append(b[i] - a[i])
    mag = 0
    for i in range(0,num_joints):
        mag = mag + (nv[i] * nv[i])
    mag = mag ** 0.5
    new_n = []
    for i in range(0,num_joints):
        new_n.append((nv[i]*n)/mag)

    return new_n

def new_int_node(a,b,n,num_joints):
    nv = []
    for i in range(0,num_joints):
        nv.append((b[i]*n) + (a[i]*(1-n)))
    return nv


num_joints = 2
goal_node = []	
start_node = []
tree = []
parent = []
child = []
goal_node = [10, 10]		
start_node = [5.0, 5.0]
print("start_node:",start_node)
print("goal_node:", goal_node)	
parent.append(None)
child.append(start_node)
#print("Parent:", None)
#print("Child:", start_node)
current_node = start_node
while True:
    print("Node:", len(child))
    random_node = random_q(num_joints)
    #print("random_node:", random_node)
    near_node, nindex = close_node(parent, child, random_node, num_joints, goal_node)
    #print("near_node:", near_node)
    fact = 1
    while True:
        new_node = new_int_node(near_node,random_node,fact,num_joints)
        if dist(near_node, new_node,num_joints) < 0.5:
            break
        fact = fact - 0.05
    print("new_node:", new_node)
    #print("distbetnodes :", dist(near_node, new_node, num_joints, goal_node))
    parent.append(nindex)
    child.append(new_node)
    #print("Parent:", nindex)
    #print("Child:", new_node)
    current_node = new_node
    #print("Dist:", dist(current_node, goal_node,num_joints))
    if dist(current_node, goal_node, num_joints) < 1:
            break
parent.append(len(child) - 1)
child.append(goal_node)

plt.figure(1)
x = []
y = []
for i in range(0,len(child)):
    x.append(child[i][0])
for i in range(0,len(child)):
    y.append(child[i][1])
plt.axis((0,10,0,10))
plt.scatter(x,y)
plt.show()

print(child)
route = []    
ind = len(tree) - 1
while True:
    route.append(child[ind])
    ind = parent[ind]
    if ind == None:
                break
print(route)

plt.figure(2)
x = []
y = []
for i in range(0,len(route)):
    x.append(route[i][0])
for i in range(0,len(route)):
    y.append(route[i][1])
plt.axis((0,10,0,10))
plt.plot(x,y)
plt.show()    

        
