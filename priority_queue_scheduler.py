# priority_queue_scheduler.py

class Task:
    """
    Represents an individual task in the scheduling system. [cite: 20]
    """
    def __init__(self, task_id, priority, arrival_time, deadline):
        self.task_id = task_id
        self.priority = priority        # Higher number = higher priority
        self.arrival_time = arrival_time
        self.deadline = deadline

    def __str__(self):
        return f"Task(ID: {self.task_id}, Priority: {self.priority}, Deadline: {self.deadline})"

class MaxPriorityQueue:
    """
    A Priority Queue implemented as a Max-Heap using a Python list (dynamic array). [cite: 17, 18, 21]
    """
    def __init__(self):
        self.heap = []
        # A dictionary to track the index of each task_id in the heap array.
        # This is CRUCIAL for achieving O(log n) time in increase/decrease_key operations.
        self.position_map = {}

    def is_empty(self):
        """Checks if the priority queue is empty. [cite: 29]"""
        return len(self.heap) == 0

    def _swap(self, i, j):
        """Helper method to swap two elements and update their positions in the map."""
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        self.position_map[self.heap[i].task_id] = i
        self.position_map[self.heap[j].task_id] = j

    def _heapify_up(self, index):
        """Maintains the max-heap property by moving an element up the tree."""
        parent_index = (index - 1) // 2
        # If the current node has a higher priority than its parent, swap them
        if index > 0 and self.heap[index].priority > self.heap[parent_index].priority:
            self._swap(index, parent_index)
            self._heapify_up(parent_index)

    def _heapify_down(self, index):
        """Maintains the max-heap property by moving an element down the tree."""
        largest = index
        left_child = 2 * index + 1
        right_child = 2 * index + 2
        n = len(self.heap)

        if left_child < n and self.heap[left_child].priority > self.heap[largest].priority:
            largest = left_child
        if right_child < n and self.heap[right_child].priority > self.heap[largest].priority:
            largest = right_child

        if largest != index:
            self._swap(index, largest)
            self._heapify_down(largest)

    def insert(self, task):
        """Inserts a new task into the heap. [cite: 23]"""
        self.heap.append(task)
        index = len(self.heap) - 1
        self.position_map[task.task_id] = index
        self._heapify_up(index)

    def extract_max(self):
        """Removes and returns the task with the highest priority. [cite: 25]"""
        if self.is_empty():
            return None

        max_task = self.heap[0]
        last_task = self.heap.pop()
        del self.position_map[max_task.task_id]

        if not self.is_empty():
            self.heap[0] = last_task
            self.position_map[last_task.task_id] = 0
            self._heapify_down(0)

        return max_task

    def update_priority(self, task_id, new_priority):
        """
        Modifies the priority of an existing task and adjusts its position. 
        Handles both increase_key and decrease_key logic. [cite: 27]
        """
        if task_id not in self.position_map:
            print(f"Task {task_id} not found.")
            return

        index = self.position_map[task_id]
        old_priority = self.heap[index].priority
        self.heap[index].priority = new_priority

        # If priority increased, sift up. If decreased, sift down.
        if new_priority > old_priority:
            self._heapify_up(index)
        elif new_priority < old_priority:
            self._heapify_down(index)


# ==========================================
# Scheduler Simulation [cite: 31]
# ==========================================
def run_scheduler_simulation():
    print("Initializing CPU Scheduler Simulation...")
    pq = MaxPriorityQueue()

    # 1. Arrival of tasks
    tasks = [
        Task("T1", priority=10, arrival_time=0, deadline=100),
        Task("T2", priority=5, arrival_time=1, deadline=50),
        Task("T3", priority=20, arrival_time=2, deadline=30),
        Task("T4", priority=15, arrival_time=3, deadline=80)
    ]

    print("\nInserting tasks into the Priority Queue...")
    for task in tasks:
        pq.insert(task)
        print(f"Inserted: {task}")

    # 2. Updating a task's priority (e.g., aging to prevent starvation)
    print("\nUpdating Priority of Task T2 from 5 to 25 (Priority Inversion/Aging)...")
    pq.update_priority("T2", 25)

    # 3. Executing tasks based on priority
    print("\nExecuting Tasks in Order of Priority:")
    while not pq.is_empty():
        executing_task = pq.extract_max()
        print(f"Processing -> {executing_task}")

if __name__ == "__main__":
    run_scheduler_simulation()