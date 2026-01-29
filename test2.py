from sys import argv
import copy
import heapq

#TODO: the tree still needs to be implemented, but this can be done with one of two  


#ACTIONS: get preformed with a single function call to parameters
#functions dont return as Python passes value by obj ref 
#this handes the mod math so everything will go in a loop

    
    

class State:
    def __init__(self, board_state, shift_values, size):
        #inited both and can be shuffeled 
        self.board_state = list(map(int, board_state))
        self.shift_values = list(map(int, shift_values))
        self.cost=0
        self.size=int(size)
        self.inversions=self.getInversions()
        self.parent=None

    # needed for checking membership in frontier
    def __eq__(self, other):
        if other is None or not isinstance(other, State):
            return False
        return self.board_state == other.board_state

    # needed to pass object in heapq
    def __lt__(self, other):
        return self.cost+self.inversions < other.cost+other.inversions
        
    #gets the index of null
    def getNullIndex(self):
        return self.board_state.index(0)

    # gets a normalized board
    def normalizeBoard(self):
        null = self.getNullIndex()
        return self.board_state[null:] + self.board_state[:null]
    
    # gets the number of inversions needed to reach goal state
    def getInversions(self):
        normalized = self.normalizeBoard()
        inversions=0
        for i in range(1, self.size):
            for j in range(i+1, self.size):
                if normalized[i] > normalized[j]:
                    inversions += 1
        return inversions
    
    #get the current shift value 
    def getShiftValue(self):
        return self.shift_values[self.getNullIndex()]
    
    #moved the empty space to the left 
    def shiftLeft(self):
        null= self.getNullIndex()
        self.board_state[null], self.board_state[(null-1)%10] = self.board_state[(null-1)%10], self.board_state[null]
     
    #moves the empty space to the right and time to to the left   
    def shiftRight(self):
        null= self.getNullIndex()
        self.board_state[null], self.board_state[(null+1)%10] = self.board_state[(null+1)%10], self.board_state[null]
        
    #swaps the space and tile to the right by the shift vaule of the space  
    def rightShiftByValue(self):
        null = self.getNullIndex()
        shiftValue = self.shift_values[null]
        self.board_state[null], self.board_state[(null+shiftValue)%10] = self.board_state[(null+shiftValue)%10], self.board_state[null]
        
        
     ##swaps the space and tile to the left by the shift vaule of the space
    def leftShiftByValue(self):
        null = self.getNullIndex()
        shiftValue= self.shift_values[null]
        self.board_state[null], self.board_state[(null-shiftValue)%10] = self.board_state[(null-shiftValue)%10], self.board_state[null]
    
    #checks the game state to see if it is a solution
    #return bool 
    def checker(self):
        null = self.getNullIndex()
        temp = self.normalizeBoard()
        goal = [0,1,1,1,2,2,2,3,3,3]
        return temp == goal

    # gets children of given state
    def getSuccessors(self):
        successors=[]

        # create child 1
        child = copy.deepcopy(self)
        child.parent=self
        child.cost += 1
        child.shiftLeft()
        child.inversions=child.getInversions()
        successors.append(child)

        # create child 2
        child = copy.deepcopy(self)
        child.parent=self
        child.cost += 1
        child.shiftRight()
        child.inversions=child.getInversions()
        successors.append(child)

        # check if shift value is 1
        if (self.getShiftValue() != 1):
            # create child 3
            child = copy.deepcopy(self)
            child.parent=self
            child.cost += 1
            child.leftShiftByValue()
            child.inversions=child.getInversions()
            successors.append(child)

            # create child 4
            child = copy.deepcopy(self)
            child.parent=self
            child.cost += 1
            child.rightShiftByValue()
            child.inversions=child.getInversions()
            successors.append(child)

        return successors
    
    # gets path of states from initial to self
    def getPath(self):
        path=[]
        current=self
        while current != None:
            path.append(current)
            current = current.parent
        path.reverse()
        return path

    # solves puzzle
    def solve(self):
        # create frontier and closed
        # frontier is a priority queue using a heap
        frontier=[]
        closed=set()

        # push initial state to frontier
        # heapq selects for smallest first is smallest f, second is smallest h
        heapq.heappush(frontier, (self, self.inversions))

        # start search
        while frontier:
            current, h = heapq.heappop(frontier)

            # check if current is solution
            if current.checker():
                return current

            # add current to closed
            closed.add(tuple(current.board_state))

            # add children to frontier if not in closed
            for child in current.getSuccessors():
                if (tuple(child.board_state) not in closed) and (child, child.inversions) not in frontier:
                    heapq.heappush(frontier, (child, child.inversions))
        
        # no solution
        return None



if __name__ == "__main__":
    shift_values=input().split()
    board_state=input().split()
    start = State(board_state, shift_values, argv[1])
    solution = start.solve()
    if (solution != None):
        path = solution.getPath()
        for node in path:
            print(node.board_state)
    else:
        print("No solution")
