from queue import Queue

# a function to read graph from file
def readgraphfromfile(filename):
    with open('dijkstraData.txt') as f:
        line = f.readline()
        adjlist = []
        while line != '':
            praselist = [[int(e.split(',')[0])-1,int(e.split(',')[1])] for e in line.split()[1:]]
            adjlist.append(praselist)
            line = f.readline()
                
    return adjlist


# BFS to identify reachable nodes
def BFS(graph,s=0):
    explored = set([s])
    q = Queue(maxsize = 1000)
    q.put(s)
    while not q.empty():
        v = q.get()
        for w,_ in graph[v]:
            if w in explored:
                continue
            else:
                explored.add(w)
                q.put(w)
    return explored


class min_heap(object):
    def __init__(self,array = [],key = lambda x:x[1]):
        self.array = array
        self.heap = []
        self.key = key
        self.index_finder={}
        
        for i in array:
            self.insert(i)
        
    def _bubble_up(self,heap,index):
        parent_id = (index-1) // 2
        if index == 0 or self.key(self.heap[index]) >= self.key(self.heap[parent_id]):
            self.index_finder[self.heap[index][0]] = index
            return
        else:
            self.heap[index], self.heap[parent_id] = self.heap[parent_id], self.heap[index]
            self.index_finder[self.heap[index][0]] = index
            self.index_finder[self.heap[parent_id][0]] = parent_id
            self._bubble_up(self.heap,parent_id)
    
    def _bubble_down(self,heap,index):
        try:
            child_id = self.heap.index(min(self.heap[index*2+1],self.heap[index*2+2],key=self.key))
        except:
            if index*2+2 == len(self.heap):
                child_id = len(self.heap) - 1
            else:
                return
        if self.key(self.heap[index]) <= self.key(self.heap[child_id]):
            self.index_finder[self.heap[index][0]] = index
            return
        else:
            self.heap[index], self.heap[child_id] = self.heap[child_id], self.heap[index]
            self.index_finder[self.heap[index][0]] = index
            self.index_finder[self.heap[child_id][0]] = child_id
            self._bubble_down(self.heap,child_id)
        
    def insert(self,element):
        self.heap.append(element)
        self._bubble_up(self.heap,len(self.heap)-1)
        
    
    def get(self,index=0):
        self.heap[index], self.heap[-1] = self.heap[-1], self.heap[index]
        self.index_finder[self.heap[index][0]] = index
        element = self.heap.pop()
        self._bubble_down(self.heap,index)
        return element
    
    def delete(self,v):
        index = self.index_finder[v]
        return self.get(index)
        


def dijkstra(graph,s=1,v=[7,37,59,82,99,115,133,165,188,197]):
    s,v,n = s-1,list(map(lambda x:x-1,v)),len(graph)
    A = [1000000] * n
    
    
    X = set([s]) # keep track of processed vertices
    A[s] = 0 # keep track of the shortest(len) to vertices 
    
    V = BFS(graph,s) # extract the reachable vertices
    
    
    
    init_list = [[i,1000000] for i in range(n)]
    
    for x in X:
        for w,l in graph[x]:
            if w not in V-X:
                continue
            else:
                init_list[w]=[w,l]
    init_list.pop(0)
    
    mheap = min_heap(init_list) #heap V-X
    
    while X != V:
        w,l = mheap.get()
        X.add(w)
        for v_,l_wv in graph[w]:
            if v_ in V-X:
                v_, old_l = mheap.delete(v_)
                new_l = min(old_l,l+l_wv)
                mheap.insert([v_,new_l])
            
        A[w] = l
        
        
    for i in v:
        print('The shortest path lenght form {} to {} is {}'.format(s+1,i+1,A[i]))
    
    return A



def main():
    graph = readgraphfromfile('dijkstraData.txt')
    costs = dijkstra(graph)
    
    
if __name__ == '__main__':
    main()

