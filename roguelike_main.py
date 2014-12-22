import copy
import os

# Checks if there is a location conflict
def contact(self,map_object,map_map):
    if(object1.location == object2.location):
        return true
    else:
        return false
        
### The map itself ###
class map_map():
    def __init__(self,map_matrix):
        self.matrix = map_matrix
    # Places an object into the map grid, updating its previous location
    def place_object(self,to_place):
        self.matrix[to_place.prev_location[1]][to_place.prev_location[0]] = " "
        self.matrix[to_place.location[1]][to_place.location[0]] = to_place.icon
    # Draws the map
    def draw(self):
        [print(row) for row in self.matrix]
        #No borders
        '''
        for row in self.matrix:
            row_string = ""
            for x in range(0,len(row)):
                row_string += str(row[x]) + " "
            print(row_string)
        '''

### Things on a map ###
class map_object():
    def __init__(self,icon,location):
        self.icon = icon
        self.location = location
        self.prev_location = location
        
# Subclass of map_object: wall
class wall(map_object):
    def __init__(self,location):
        map_object.__init__(self,"#",location)
        
# Subclass of map_object: player character      
class player(map_object):
    def __init__(self,location):
        map_object.__init__(self,"@",location)
    #Waits for input; updates prev_location and location accordingly
    def move(self,map_map):
        self.prev_location = copy.deepcopy(self.location)
        user_input = input("")
        if(user_input == "a"):
            self.location[0] -= 1
        elif(user_input == "d"):
            self.location[0] += 1
        elif(user_input == "w"):
            self.location[1] -= 1
        elif(user_input == "s"):
            self.location[1] += 1
        if(map_map.matrix[self.location[1]][self.location[0]] != " "):
            self.location = copy.deepcopy(self.prev_location)


       
this_map = map_map([[" "," "," "," "," "],
            [" "," "," "," "," "],
            [" "," "," "," "," "],
            [" "," "," "," "," "],
            [" "," "," "," "," "],
            [" "," "," "," "," "]])


this_player = player([1,4])
this_map.place_object(this_player)

this_wall = wall([3,3])
this_map.place_object(this_wall)
    
while(True):
    clear = lambda: os.system('cls')
    clear()
    this_map.draw()
    this_player.move(this_map)
    this_map.place_object(this_player)

