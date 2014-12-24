import copy
import os 
        
### The map itself ###
class map_map():
    def __init__(self,map_matrix):
        self.matrix = map_matrix
        self.placeholders = []
        self.messages = []
        
        # Casts input characters to their respective objects
        for x in range(0,len(self.matrix)):
            for y in range(0,len(self.matrix[x])):
                # Wall
                if(self.matrix[x][y] == "#"):
                    #print("Wall found at " + str(x) + "," + str(y))
                    self.matrix[x][y] = wall([x,y])
                # Space
                if(self.matrix[x][y] == " "):
                    #print("Space found at " + str(x) + "," + str(y))
                    self.matrix[x][y] = space([x,y])
                #Hazard
                if(self.matrix[x][y] == "%"):
                    #print("Hazard found at " + str(x) + "," + str(y))
                    self.matrix[x][y] = hazard([x,y],5)
                
    '''
    # Prints out the indices and objects at them
    def print_matrix_info():
        for x in range(0,len(self.matrix)):
            for y in range(0,len(self.matrix[x])):
                print(str(x) + "," + str(y) + ": " + str(self.matrix[x][y]))
    '''
    # Places an object into the map grid, storing the location's previous occupant
    def place_object(self,to_place):
        #self.placeholders.append(self.matrix[to_place.location[0]][to_place.location[1]])                   
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

    # Updates location where player was
    def update_placeholders(self):
         for item in self.placeholders:
             print(item.location)
             self.matrix[item.location[0]][item.location[1]] = item
         self.placeholders = []

    # Returns the player object on the map
    def player(self):
        result = False
        for row in self.matrix:
            for item in row:
                if(item.object_type == "player"):
                    result = item
        return result

    # Calculates hazard damage
    def environmental_damage(self):
        for row in self.matrix:
            for item in row:
                if(item.object_type == "player" or item.object_type == "enemy"):
                    if(item.beneath.object_type == "hazard"):
                        self.add_message(item.name + " stepped on a hazard!")
                        self.add_message(item.name + " lost " + str(item.beneath.damage) + " hp!")
                        item.hp -= item.beneath.damage

    # Adds message to messages array, to print later
    def add_message(self,to_add):
        self.messages.append(to_add)

    # Prints messages
    def print_messages(self):
        [print(message) for message in self.messages]
        self.messages = []
             
### Things on a map ###
class map_object():
    def __init__(self,name,icon,location):
        self.icon = icon
        self.location = location
        self.prev_location = location
        self.name = name
        self.passable = False

    def __str__(self):
        return self.icon

    def take_damage(self,attack):
        return "There is nothing to attack!"
    
# Subclass of map_object: space
class space(map_object):
    def __init__(self,location):
        map_object.__init__(self,"thin air"," ",location)
        self.passable = True
        self.object_type = "space"
        
# Subclass of map_object: wall
class wall(map_object):
    def __init__(self,location):
        map_object.__init__(self,"a wall","#",location)
        self.object_type = "wall"

    def take_damage(self,atk):
        return "The wall is not effected"

# Subclass of map_object: hazard
class hazard(map_object):
    def __init__(self,location,damage):
        map_object.__init__(self,"thin air","%",location)
        self.damage = damage
        self.passable = True
        self.object_type = "hazard"
        
# Subclass of map_object: character
class character(map_object):
    def __init__(self,name,icon,location,hp,atk):
        map_object.__init__(self,name,icon,location)
        self.hp = hp
        self.atk = atk

    def take_damage(self,atk):
        self.hp -= atk
        return (self.name + " lost " + str(atk) + " hp!")

    def print_stats(self):
        print(self.name + " HP: " + str(self.hp))

# Subclass of map_object: enemy
class enemy(character):
    def __init__(self,name,location,hp,atk):
        character.__init__(self,name,"$",location,hp,atk)
        self.object_type = "enemy"
        self.prev_location = copy.deepcopy(location)
        self.beneath = space(location)
        
        
# Subclass of character: player character      
class player(character):
    def __init__(self,name,location,hp,atk):
        character.__init__(self,name,"@",location,hp,atk)
        self.object_type = "player"
        self.prev_location = copy.deepcopy(location)
        self.beneath = space(location)
        
    #Waits for input; updates prev_location and location accordingly
    def action(self,map_map):
        user_input = input("")

        map_map.add_message("Beneath: " + str(self.beneath.object_type))

        #Movement
        
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
            if(map_map.matrix[self.location[0]][self.location[1]]):
                pass
        except:
            self.location = copy.deepcopy(self.prev_location)

        # Canceling move if contacting something
        if(map_map.matrix[self.location[0]][self.location[1]].passable == False):
            self.location = copy.deepcopy(self.prev_location)

        if(self.prev_location != self.location):
            map_map.matrix[self.prev_location[0]][self.prev_location[1]] = self.beneath
            self.beneath = map_map.matrix[self.location[0]][self.location[1]]
            self.prev_location = copy.deepcopy(self.location)
            
        # Attacking
        if(user_input == "z"):
            if(self.icon == "<"): target_loc = [self.location[0],self.location[1]-1]
            elif(self.icon == ">"): target_loc = [self.location[0],self.location[1]+1]
            elif(self.icon == "^"): target_loc = [self.location[0]-1,self.location[1]]
            elif(self.icon == "v"): target_loc = [self.location[0]+1,self.location[1]]
            else: target_loc = None
            target = map_map.matrix[target_loc[0]][target_loc[1]]

            map_map.add_message(self.name + " struck " + target.name)
            map_map.add_message(target.take_damage(self.atk))

        # Resting
        if(user_input == "r"):
            pass
       
this_map = map_map([["#","#"," "," "," "],
            [" "," "," "," "," "],
            [" "," "," ","%"," "],
            [" "," "," "," ","#"],
            [" "," "," "," "," "],
            [" "," "," "," "," "]])


this_player = player("Hero",[4,1],20,2)
this_map.place_object(this_player)

this_enemy = enemy("Baddy",[2,2],6,1)
this_map.place_object(this_enemy)
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
    this_map.print_messages()
    this_player.action(this_map) # Takes player input
    this_map.place_object(this_player) # Updates spot player moved to
    this_map.environmental_damage()
print("You lost!")
