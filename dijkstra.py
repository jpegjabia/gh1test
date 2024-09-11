'''
Есть список скорейших путей и очередь на проверку
Список = [(Точка, ближайшее расстояние), ...]

Проверяем соседей, добавляем эти точки в список скорейших путей.
Смотрим соседей одной из точек. Обновляем скорейшие пути 
и добовляем в очередь новые точки для изучения их соседей.  
'''
import heapq
import math

graph = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'C': 2, 'D': 5},
    'C': {'A': 4, 'B': 2, 'D': 1},
    'D': {'B': 5, 'C': 1}
}

start_node = 'A'

def dijkstra(graph, start):
    priority_queue = []
    distances = {node: float('infinity') for node in graph}   #all nodes firstly have dist. infinity
    distances[start] = 0  #make the starting node have a distance 0

    heapq.heappush(priority_queue, (0, start))  #put the starting node in the queue 

    while priority_queue: #while queue isn't empty
        #Pop and return the smallest item from the queue
        current_distance, current_node = heapq.heappop(priority_queue) 

        # if the currently analysed distance is larger than the previously found, then we skip it
        if current_distance > distances[current_node]:
            continue 

        # checking the neighbors of the node, which we are currently at
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            # if the newly found path is smaller than the previous, 
            # then we update the smallest distance 
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances 

distances = dijkstra(graph, start_node)
print(f"Distances from {start_node}: {distances}")
