from treelib import Node, Tree

#TODO: the tree still needs to be implemented, but this can be done with one of two  


#ACTIONS: get preformed with a single function call to parameters
#functions dont return as Python passes value by obj ref 
#this handes the mod math so everything will go in a loop

    
    

class State:
    def __init__(self):
        #inited both and can be shuffeled 
        self.board_state= [2,2,2,3,3,3,None,1,1,1]
        self.shift_values = [1,2,3,4,4,3,1,2,2,1]
        
    #gets the index of null
    def getNullIndex(self):
        return self.board_state.index(None)
    
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
        temp = self.board_state[null:] + self.board_state[:null]
        goal = [None,1,1,1,2,2,2,3,3,3]
        return temp == goal


if __name__ == "__main__":
    node = State()
    c_state= node.checker()
    # print("correct state: " + str(c_state)+ "\n")
    print("starting state: "+str(node.board_state))
    # node.shiftLeft()
    # print(str(node.board_state)+"\n")
    
    # node.shiftRight()
    # node.shiftRight()
    # node.shiftRight()
    # node.shiftRight()
    # node.shiftRight()
    
    node.leftShiftByValue()
    print("LSBV: "+str(node.board_state))
    node.rightShiftByValue()
    
    print("RSBV: "+str(node.board_state))
