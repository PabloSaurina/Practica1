"""

"""

from multiprocessing import Process, BoundedSemaphore, Manager
import random

K = 10
N = 3
M = 3

def productor_numeros():
    vec = [-1]*(K+M)
    vec[0] = random.randrange(1,11)
    for i in range(K-1):
        vec[i+1] = vec[i] + random.randrange(1,11)
    return vec

def minimo_merge(vec):
    m = max(vec)
    j = vec.index(m)
    if m != -1:
        for i in range(N*M):
            if vec[i] >= 0 and vec[i] < m:
                m = vec[i]
                j = i
    return (m,j)
    

def productor_task(semaforo_e,semaforo_n,buffer,buffer_prod,numeros,ide):
    i = 0
    while i < K+M:
        semaforo_e.acquire()
        print(ide,"close e")
        m = ide*M
        while m < (ide+1)*M:
            if i < K+M and buffer_prod[m]:
                buffer[m] = numeros[i]
                buffer_prod[m] = False
                i += 1
            m += 1
        semaforo_n.release()
        print(ide,"open n")

def merger_task(semaforos_e,semaforos_n,buffer,buffer_prod,merged_numeros):
    z = True
    while z:
        for j in range(N):
            semaforos_n[j].acquire()
            print(j,"close n")
        (a,pos) = minimo_merge(buffer)
        ide = pos // M
        buffer_prod[pos] = True
        if a != -1:
            merged_numeros.append(a)
            print("from prod",ide,"pos",pos % M,':',a)
        else:
            z = False
        for j in range(N):
            if j == ide:
                semaforos_e[j].release()
                print(j,"open e")
            else:
                semaforos_n[j].release()
                print(j,"open n")
        
    

def main():
    lp = []
    manager = Manager()
    buffer = manager.list()
    buffer_prod = manager.list()
    semaforos_e = [None]*N
    semaforos_n = [None]*N
    for i in range(N):
        for j in range(M):
            buffer.append(-2)
            buffer_prod.append(True)
        semaforos_e[i] = BoundedSemaphore(1)
        semaforos_n[i] = BoundedSemaphore(1)
        semaforos_n[i].acquire()
       	pr = productor_numeros()
       	print(i,":",pr)
        lp.append(Process(target=productor_task, 
                args = (semaforos_e[i],semaforos_n[i],buffer,buffer_prod,pr,i)))
    res = manager.list()
    lp.append(Process(target=merger_task, args=(semaforos_e,semaforos_n,buffer,buffer_prod,res)))
    for p in lp:
        p.start()
    for p in lp:
        p.join()
    print(res)

if __name__ == '__main__':
    main()
