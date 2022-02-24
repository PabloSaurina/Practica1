"""

"""

from multiprocessing import Process, BoundedSemaphore, Manager
import random

K = 10
N = 3

def productor_numeros():
    vec = [None]*(K+1)
    vec[0] = random.randrange(1,11)
    for i in range(K-1):
        vec[i+1] = vec[i] + random.randrange(1,11)
    vec[-1] = -1
    return vec

def minimo_merge(vec):
    m = max(vec)
    j = vec.index(m)
    if m != -1:
        for i in range(N):
            if vec[i] >= 0 and vec[i] < m:
                m = vec[i]
                j = i
    return (m,j)
    

def productor_task(semaforo_e,semaforo_n,buffer,numeros,ide):
    for i in range(K+1):
        semaforo_e.acquire()
        print(ide,"close e")
        buffer[ide] = numeros[i]
        semaforo_n.release()
        print(ide,"open n")

def merger_task(semaforos_e,semaforos_n,buffer,merged_numeros):
    z = True
    while z:
        for j in range(N):
            semaforos_n[j].acquire()
            print(j,"close n")
        (a,pos) = minimo_merge(buffer)
        if a != -1:
            merged_numeros.append(a)
            print("from prod",pos,':',a)
        else:
            z = False
        for j in range(N):
            if j == pos:
                semaforos_e[j].release()
                print(j,"open e")
            else:
                semaforos_n[j].release()
                print(j,"open n")
        
    

def main():
    lp = []
    manager = Manager()
    buffer = manager.list()
    semaforos_e = [None]*N
    semaforos_n = [None]*N
    for i in range(N):
        buffer.append(-2)
        semaforos_e[i] = BoundedSemaphore(1)
        semaforos_n[i] = BoundedSemaphore(1)
        semaforos_n[i].acquire()
       	pr = productor_numeros()
       	print(i,":",pr)
        lp.append(Process(target=productor_task, 
                args = (semaforos_e[i],semaforos_n[i],buffer,pr,i)))
    res = manager.list()
    lp.append(Process(target=merger_task, args=(semaforos_e,semaforos_n,buffer,res)))
    for p in lp:
        p.start()
    for p in lp:
        p.join()
    print(res)

if __name__ == '__main__':
    main()
