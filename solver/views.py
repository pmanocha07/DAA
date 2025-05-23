import random
from collections import deque
import heapq
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Generate a random maze
def generate_maze(size):
    while True:
        maze = [[1] * size for _ in range(size)]
        for i in range(size):
            for j in range(size):
                if random.random() > 0.3:
                    maze[i][j] = 0  
        maze[0][0] = 0
        maze[size - 1][size - 1] = 0

        _, path = bfs(maze)
        if path:
            return maze


# BFS Algorithm (Shortest Path)
def bfs(maze):
    size = len(maze)
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    queue = deque([(0, 0, [])])
    visited = set()
    steps = []

    while queue:
        x, y, path = queue.popleft()
        if (x, y) in visited:
            continue
        visited.add((x, y))
        new_path = path + [(x, y)]
        steps.append((x, y))

        if (x, y) == (size - 1, size - 1):
            return steps, new_path  # Return full steps and final path

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < size and 0 <= ny < size and maze[nx][ny] == 0:
                queue.append((nx, ny, new_path))

    return steps, []  # No solution found

# DFS Algorithm (May not find shortest path)
def dfs(maze):
    size = len(maze)
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    stack = [(0, 0, [])]
    visited = set()
    steps = []

    while stack:
        x, y, path = stack.pop()
        if (x, y) in visited:
            continue
        visited.add((x, y))
        new_path = path + [(x, y)]
        steps.append((x, y))

        if (x, y) == (size - 1, size - 1):
            return steps, new_path

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < size and 0 <= ny < size and maze[nx][ny] == 0:
                stack.append((nx, ny, new_path))

    return steps, []

# Dijkstra's Algorithm (Guaranteed Shortest Path)
def dijkstra(maze):
    size = len(maze)
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    pq = [(0, 0, 0, [])]  # (cost, x, y, path)
    visited = set()
    steps = []

    while pq:
        cost, x, y, path = heapq.heappop(pq)
        if (x, y) in visited:
            continue
        visited.add((x, y))
        new_path = path + [(x, y)]
        steps.append((x, y))

        if (x, y) == (size - 1, size - 1):
            return steps, new_path

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < size and 0 <= ny < size and maze[nx][ny] == 0:
                heapq.heappush(pq, (cost + 1, nx, ny, new_path))

    return steps, []

# A* Algorithm (Fastest for Shortest Path)
def a_star(maze):
    size = len(maze)
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    pq = [(0, 0, 0, [])]  # (f-cost, x, y, path)
    visited = set()
    steps = []

    def heuristic(x, y):
        return abs(size - 1 - x) + abs(size - 1 - y)

    while pq:
        f, x, y, path = heapq.heappop(pq)
        if (x, y) in visited:
            continue
        visited.add((x, y))
        new_path = path + [(x, y)]
        steps.append((x, y))

        if (x, y) == (size - 1, size - 1):
            return steps, new_path

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < size and 0 <= ny < size and maze[nx][ny] == 0:
                g = len(new_path)
                h = heuristic(nx, ny)
                heapq.heappush(pq, (g + h, nx, ny, new_path))

    return steps, []

# API to generate maze
@csrf_exempt
def generate_maze_api(request):
    data = json.loads(request.body)
    size = data.get('size', 30)
    maze = generate_maze(size)
    return JsonResponse({'maze': maze})

# API to solve the maze
@csrf_exempt
def solve_maze_api(request):
    try:
        data = json.loads(request.body)
        
        maze = data.get('maze')
        algorithm = data.get('algorithm')

        if maze is None:
            return JsonResponse({"error": "Maze data is missing"}, status=400)
        if algorithm == 'bfs':
            steps, shortest_path = bfs(maze)
        elif algorithm == 'dfs':
            steps, shortest_path = dfs(maze)
        elif algorithm == 'dijkstra':
            steps, shortest_path = dijkstra(maze)
        elif algorithm == 'a_star':
            steps, shortest_path = a_star(maze)
        else:
            return JsonResponse({"error": "Invalid algorithm"}, status=400)

        if not shortest_path:
            return JsonResponse({"error": "No solution found, Generate New Maze"}, status=400)

        return JsonResponse({'steps': steps, 'shortest_path': shortest_path})

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)
