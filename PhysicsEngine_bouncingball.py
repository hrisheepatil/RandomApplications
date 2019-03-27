from vpython import *
import numpy as np
import matplotlib.pyplot as plt

def make_spring (start, end):
    spring = cylinder()
    spring.pos = start
    spring.axis = end - start
    spring.radius = 0.1
    spring.color = color.blue
    spring.end = end
    return spring
        
def make_mass (pos):
    ball = sphere()
    ball.color = color.orange
    ball.radius = 0.4
    ball.pos = pos
    ball.mass = 1
    return ball


bvec = []
svec = []
orglen = [] 

floor = box(length=25, height=0.5, width=25, color=color.green)
h = 10



count = 0
for j in (-1,1):
    for i in (-1,1):
        for k in (-1,1):
            a = make_mass(vector(i,h+j,k))
            count += 1
            if count < 5:
                a.color = color.orange
            else:
                a.color = color.red
            bvec.append(a)
           

            
for i in range (0,8):
    for j in range (i+1,8):
        a = make_spring(bvec[i].pos, bvec[j].pos);
        orglen.append(a.length)
        svec.append(a)

dt = 0.0
ts = 0.001
k = 1000
g = vector(0.0, -9.81, 0.0)
fc = 0.0
sc = 0.0
for m in range(0,8):
    bvec[m].velocity = vector(0.0,0.0,0.0)

    
forspg = []
for m in range(0,8):
    if m < 4: 
        forspg.append(vector(3000,0.0,0.0))
    else:
        forspg.append(vector(-3000,0.0,0.0))

kmat = []
pmat = []
vmat = []
dtmat = []
temat = []

#time.sleep(10)
while dt < 10:
    rate(100)
    acc = []
    a = 0
    ke = 0
    for m in range(0,8):
        for i in range (m + 1,8):
            svec[a].pos = bvec[i].pos
            svec[a].axis = bvec[m].pos - bvec[i].pos
            defx = (orglen[a] - svec[a].length)
            """
            if a==4:
                defx = ((orglen[a] * (0.5 + sin(1000*dt))) - svec[a].length)
            else:
                defx = (orglen[a] - svec[a].length)
            """
            #print(orglen[a])
            #print(defx)
            ke += 0.5 * (k * defx * defx)
            forspg[m] += np.dot(svec[a].axis, (defx * k)/(bvec[m].pos - bvec[i].pos).mag)            
            forspg[i] -= np.dot(svec[a].axis, (defx * k)/(bvec[m].pos - bvec[i].pos).mag)
            if dt > ts:
                if defx < 0:
                    forspg[m] = forspg[m] + np.dot((bvec[m].velocity - vel_store[m]),sc)
                    forspg[i] = forspg[i] - np.dot((bvec[i].velocity - vel_store[i]),sc)
                elif defx > 0:
                    forspg[m] = forspg[m] - np.dot((bvec[m].velocity - vel_store[m]),sc)
                    forspg[i] = forspg[i] + np.dot((bvec[i].velocity - vel_store[i]),sc)
            a = a + 1
        frc = (forspg[m]/bvec[m].mass) + g
        fh = ((frc.x)**2 + (frc.z)**2)**0.5
        if fh > abs(frc.y)*fc:
            if frc.x < 0:
                frc.x = frc.x + (frc.y * fc)
            elif frc.x > 0:
                frc.x = frc.x - (frc.y * fc)
            elif frc.z < 0:
                frc.z = frc.z + (frc.y * fc)
            elif frc.z > 0:
                frc.z = frc.z - (frc.y * fc)
        acc.append(frc)
        
    vel_store = []
    pos_store = []
    ve = 0
    pe = 0
    for m in range (0,8):
        if bvec[m].pos.y < 0.7:
            bvec[m].velocity = np.dot((bvec[m].velocity),-0.5)            
            bvec[m].pos = bvec[m].pos + np.dot(bvec[m].velocity,ts)
            vel_store.append(bvec[m].velocity)
            pos_store.append(bvec[m].pos)
            pe += bvec[m].mass * 9.81 * abs(bvec[m].pos.y)
            ve += 0.5 * (bvec[m].mass * bvec[m].velocity.mag * bvec[m].velocity.mag)
                
        else:
            bvec[m].velocity = bvec[m].velocity + np.dot(acc[m],ts)
            vel_store.append(bvec[m].velocity)
            pos_store.append(bvec[m].pos)
            ve += 0.5 * (bvec[m].mass * bvec[m].velocity.mag * bvec[m].velocity.mag)

        bvec[m].pos = bvec[m].pos + np.dot(bvec[m].velocity,ts)
        pe += bvec[m].mass * 9.81 * bvec[m].pos.y

    forspg = []    
    for m in range(0,8):
        forspg.append(vector(0.0,0.0,0.0))
    kmat.append(ke)
    #print(ke)
    pmat.append(pe)
    #print(pe)
    vmat.append(ve)
    #print(ve)
    te = pe + ve + ke
    temat.append(te)
    #print(te)
    dtmat.append(dt)
    dt = dt + ts

#print(kmat)
#print(pmat)
#print(vmat)
#print(kmat + pmat + vmat)
plt.figure()
plt.plot(dtmat,temat)
plt.title('Total Energy v/s Time')
plt.ylabel('Total Energy')
plt.xlabel('Time')
plt.ylim((0,1000))
plt.show()

plt.figure()
plt.plot(dtmat,pmat)
plt.title('Potential Energy v/s Time')
plt.ylabel('Potential Energy')
plt.xlabel('Time')
plt.ylim((0,1000))
plt.show()

plt.figure()
plt.plot(dtmat,vmat)
plt.title('Kinetic Energy v/s Time')
plt.ylabel('Kinetic Energy')
plt.xlabel('Time')
plt.ylim((0,1000))
plt.show()

plt.figure()
plt.plot(dtmat,kmat)
plt.title('Spring Energy v/s Time')
plt.ylabel('Spring Energy')
plt.xlabel('Time')
plt.ylim((0,1000))
plt.show()
