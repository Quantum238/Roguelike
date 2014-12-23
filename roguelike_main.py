import copy
import os

def environmental_damage(map_map):
    for item in map_map.placeholders:
        if(item.object_type == "hazard"):
            if(item.location == map_map.player().location):
                print("You stepped on a hazard!")
                print("You lost " + str(item.damage) + " hp!")
                map_map.player().hp -= item.damage
    
### The map itself ###
class map_map():
    def __init__(self,map_matrix):
        self.matrix = map_matrix
        self.placeholders = []
        # Casts input characters to their respective objects
        for x in range(0,len(self.matrix)):
            for y in range(0,len(self.matrix[x])):
                # Wall
                if(self.matrix[x][y] == "#"):
                    print("Wall found at " + str(x) + "," + str(y))
                    self.matrix[x][y] = wall([x,y])
                # Space
                if(self.matrix[x][y] == " "):
                    print("Space found at " + str(x) + "," + str(y))
                    self.matrix[x][y] = space([x,y])
                #Hazard
                if(self.matrix[x][y] == "%"):
                    print("Hazard found at " + str(x) + "," + str(y))
                    self.matrix[x][y] = hazard([x,y],5)
    '''
    # Prints out the indices and objects at them
    def print_matrix_info():
        for x in range(0,len(self.matrix)):
            for y in range(0,len(self.matrix[x])):
                print(str(x) + "," + str(y) + ": " + str(self.matrix[x][y]))
    '''
    # Places an object into the map grid, updating its previous location
    def place_object(self,to_place):
        self.placeholders.append(self.matrix[to_place.location[0]][to_place.location[1]])
        #[print(str(type(item)) + " : " + str(item.location)) for item in self.placeholders]                    
        self.matrix[to_place.location[0]][to_place.location[1]] = to_place
        
    # Draws the map
    def draw(self):
        # As arrays
        '''
        [print(row) for row in self.matrix]
        '''
        # As characters
        '''
        for row in self.matrix:
            row_string = ""
            for x in range(0,len(row)):
                row_string += str(row[x]) + " "
            print(row_string)
        '''
        # As characters with borders
        print("-"*(len(self.matrix[0])+2))
        for row in self.matrix:
            row_string = "|"
            for x in range(0,len(row)):
                row_string += str(row[x])
            row_string += "|"
            print(row_string)
        print("-"*(len(self.matrix[0])+2))

    def update_placeholders(self):
         for item in self.placeholders:
             self.matrix[item.location[0]][item.location[1]] = item
         self.placeholders = []

    def player(self):
        result = False
        for row in self.matrix:
            for item in row:
                if(item.object_type == "player"):
                    result = item
        return result
             
### Things on a map ###
class map_object():
    def __init__(self,icon,location):
        self.icon = icon
        self.location = location
        self.prev_location = location
        self.passable = False

    def __str__(self):
        return self.icon
    
# Subclass of map_object: space
class space(map_object):
    def __init__(self,location):
        map_object.__init__(self," ",location)
        self.passable = True
        self.object_type = "space"
        
# Subclass of map_object: wall
class wall(map_object):
    def __init__(self,location):
        map_object.__init__(self,"#",location)
        self.object_type = "wall"

# Subclass of map_object: hazard
class hazard(map_object):
    def __init__(self,location,damage):
        map_object.__init__(self,"%",location)
        self.damage = damage
        self.passable = True
        self.object_type = "hazard"
        
# Subclass of map_object: character
class character(map_object):
    def __init__(self,icon,location,hp,atk):
        map_object.__init__(self,icon,location)
        self.hp = hp
        self.atk = atk
        
# Subclass of character: player character      
class player(character):
    def __init__(self,location,hp,atk):
        character.__init__(self,"@",location,hp,atk)
        self.object_type = "player"
        print(self.location)
    #Waits for input; updates prev_location and location accordingly
    def move(self,map_map):
        self.prev_location = copy.deepcopy(self.location)
        user_input = input("")
        if(user_input == "a"):
            self.location[1] -= 1
            self.icon = "<"
        elif(user_input == "d"):
            self.location[1] += 1
            self.icon = ">"
        elif(user_input == "w"):
            self.location[0] -= 1
            self.icon = "^"
        elif(user_input == "s"):
            self.location[0] += 1
            self.icon = "v"
        # Canceling move if going out of bounds
        try:
            if(map_map.matrix[self.location[1]][self.location[0]]):
                pass
        except:
            self.location = copy.deepcopy(self.prev_location)
        # Canceling move if contacting something
        if(map_map.matrix[self.location[0]][self.location[1]].passable == False):
            self.location = copy.deepcopy(self.prev_location)

    def print_stats(self):
        print("HP: " + str(self.hp))
       
this_map = map_map([["#","#"," "," "," "],
            [" "," "," "," "," "],
            [" "," "," ","%"," "],
            [" "," "," "," ","#"],
            [" "," "," "," "," "],
            [" "," "," "," "," "]])


this_player = player([4,1],20,2)
this_map.place_object(this_player)
'''
#For manually adding things
this_wall = wall([3,3])
this_map.place_object(this_wall)
'''

# A turn
while(this_player.hp > 0):
    # Refreshes screen
    clear = lambda: os.system('cls')
    clear()
    this_map.draw()
    this_player.print_stats()
    this_player.move(this_map) # Takes player input
    this_map.update_placeholders() # Updates spot player was in
    this_map.place_object(this_player) # Updates spot player moved to
    environmental_damage(this_map)
print("You lost!")
