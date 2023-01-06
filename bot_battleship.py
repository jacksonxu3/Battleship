# Player vs Bot Game

from random import randint

# Creates an empty board of 20 columns by 10 rows where the player will place down ships
def defence_board_maker():
    row1 = ['~']*20
    row2 = ['~']*20
    row3 = ['~']*20
    row4 = ['~']*20
    row5 = ['~']*20
    row6 = ['~']*20
    row7 = ['~']*20
    row8 = ['~']*20
    row9 = ['~']*20
    row10 = ['~']*20
    return [row1, row2, row3, row4, row5, row6, row7, row8, row9, row10]

# Creates an empty board of 20 columns by 10 rows where the player will place down ships
def offence_board_maker():
    row1 = ['?']*20
    row2 = ['?']*20
    row3 = ['?']*20
    row4 = ['?']*20
    row5 = ['?']*20
    row6 = ['?']*20
    row7 = ['?']*20
    row8 = ['?']*20
    row9 = ['?']*20
    row10 = ['?']*20
    return [row1, row2, row3, row4, row5, row6, row7, row8, row9, row10]

# Welcome print message
def welcomer():
    print('\n')
    print('---------------------')
    print('Welcome to Bot Battleship!')
    print('It is the board game Battleship,')
    print('but instead of 2 players, it is a player vs a bot.')
    print('It is a 20x10 board and each side gets 8 boats.')
    print('Each side has 8 boats of the following sizes 1, 3, 5, and 7.')

# Places the ships
def ship_placer(defender, size):
        direction = defender.direction_helper(size)
        raw_ship_row, raw_ship_column = defender.center_helper(size, direction)
        ship_row, ship_column = raw_ship_row - 1, raw_ship_column - 1
        if direction == 'horizontal':
            for spot in range(ship_column - (size//2), ship_column + (size//2) + 1):
                defender.defence_board[ship_row][spot] = '#'
        elif direction == 'vertical':
            for spot in range(ship_row - (size//2), ship_row + (size//2) + 1):
                defender.defence_board[spot][ship_column] = '#'

# Checks if the location of the ship will be valid in terms of 
# if it will fit on the board and if it intersects another ship
def ship_center_validity_checker(defender, size, direction, raw_row, raw_column):
    ship_row, ship_column = raw_row - 1, raw_column - 1
    if direction == 'horizontal':
        if (raw_column - size//2) < 1 or (raw_column + size//2) > 20:
            return False
        for spot in range(ship_column - (size//2), ship_column + (size//2) + 1):
            if defender.defence_board[ship_row][spot] != '~':
                return False
    elif direction == 'vertical':
        if (raw_row - size//2) < 1 or (raw_row + size//2) > 10:
            return False
        for spot in range(ship_row - (size//2), ship_row + (size//2) + 1):
            if defender.defence_board[spot][ship_column] != '~':
                return False
    else:
        return True

# Checks if the attack location is a hit or a miss
def attack_validity_checker(defender, raw_row, raw_column):
    if defender.defence_board[raw_row-1][raw_column-1] == '#':
        return True
    elif defender.defence_board[raw_row-1][raw_column-1] == '~':
        return False

# Employs the attack
def attack(defender, attacker):
    raw_row, raw_column = attacker.attack_asker()
    row, column = raw_row - 1, raw_column - 1
    if attack_validity_checker(defender, raw_row, raw_column) == True:
        defender.defence_board[row][column] = 'X'
        attacker.offence_board[row][column] = 'X'
        defender.broken += 1
        attacker.hits += 1
        if type(defender) == Player:
            print(f"\nThe enemy got a hit at ({row+1}, {column+1}).")
        elif type(defender) == Bot:
            print(f"\nYou hit the enemy at ({row+1}, {column+1}).")
    elif attack_validity_checker(defender, raw_row, raw_column) == False:
        defender.defence_board[row][column] = 'O'
        attacker.offence_board[row][column] = 'O'
        if type(defender) == Player:
            print(f"\nThe enemy got a miss at ({row+1}, {column+1}).")
        elif type(defender) == Bot:
            print(f"\nYou missed the enemy at ({row+1}, {column+1}).")

# Checking if the input is a valid row input
def ten_integer_checker(input):
    if input == '1' or input == '2' or input == '3' or \
    input == '4' or input == '5' or input == '6' or \
    input == '7' or input == '8' or input == '9' or \
    input == '10':
        return int(input)
    else:
        return False

# Checking if the input is a valid column input
def twenty_integer_checker(input):
    if input == '1' or input == '2' or input == '3' or \
    input == '4' or input == '5' or input == '6' or \
    input == '7' or input == '8' or input == '9' or \
    input == '10' or input == '11' or input == '12' or \
    input == '13' or input == '14' or input == '15' or \
    input == '16' or input == '17' or input == '18' or \
    input == '19' or input == '20':
        return int(input)
    else:
        return False

# Prints out the board
def board_printer(board):
    for row in board:
        print("".join(row))

# Game winner determiner
def game_winner(player, bot):
    if player.hits == 32 and bot.broken == 32:
        return 'player'
    elif bot.hits == 32 and player.broken == 32:
        return 'bot'
    else:
        return False

# Player Class and methods 
class Player:
    def __init__(self):
        self.defence_board = defence_board_maker()
        self.offence_board = offence_board_maker()
        self.attacks = []
        self.broken = 0
        self.hits = 0

    # Determines the direction that a specific ship will face
    def direction_helper(self, size):
        print(f'\nWould you like your size {size} ship to be "horizontal" or "vertical"?')
        ship_direction = input()
        if ship_direction != 'horizontal' and ship_direction != 'vertical':
            print(f'\nInvalid response! Please enter "horizontal" or "vertical".')
            return self.direction_helper(size)
        return ship_direction

    # Determines the center of a specific ship
    # Returns the center in raw coordinates
    def center_helper(self, size, direction):
        raw_ship_row, raw_ship_column = self.ship_center_asker(size)
        if ship_center_validity_checker(self, size, direction, raw_ship_row, raw_ship_column) == False:
            print('\nInvalid ship location. Please try another location.')
            return self.center_helper(size, direction)
        else:
            return raw_ship_row, raw_ship_column

    # Asks for the desired location of the center of a specific ship
    def ship_center_asker(self, size):
    # Asks about the row number
        print(f'\nWhich row would you like the center of your size {size} ship to be?')
        print(f'Enter an integer from 1 through 10.')
        raw_ship_row = ten_integer_checker(input())
        while raw_ship_row == False:
            print(f'\nInvalid response! Please enter an integer from 1 through 10.')
            raw_ship_row = ten_integer_checker(input())
    
        #Asks about the column number
        print(f'\nWhich column would you like the center of your size {size} ship to be?')
        print(f'Enter an integer from 1 through 20.')
        raw_ship_column = twenty_integer_checker(input())
        while raw_ship_column == False:
            print(f'\nInvalid response! Please enter an integer from 1 through 20.')
            raw_ship_column = twenty_integer_checker(input())
    
        return raw_ship_row, raw_ship_column
    
    # Asks about the desired attack location and 
    # ensures that the targetted location has not been previously attacked
    def attack_asker(self):
        # The row being attacked
        print('\nWhich row would you like to attack')
        print('Enter an integer from 1 through 10.')
        raw_ship_row = ten_integer_checker(input())
        while raw_ship_row == False:
            print(f'\nInvalid response! Please enter an integer from 1 through 10.')
            raw_ship_row = ten_integer_checker(input())
        # The column being attacked
        print('\nWhich column would you like to attack')
        print('Enter an integer from 1 through 20.')
        raw_ship_column = twenty_integer_checker(input())
        while raw_ship_column == False:
            print(f'\nInvalid response! Please enter an integer from 1 through 20.')
            raw_ship_column = twenty_integer_checker(input())
        # Checking if the spot has already been attacked
        combined_attack = str(raw_ship_row) + str(raw_ship_column)
        if combined_attack in self.attacks:
            print('\nYou have already attacked that location. Please attack somewhere else.')
            return self.attack_asker()
        else:
            self.attacks.append(combined_attack)
        return raw_ship_row, raw_ship_column

# Bot Class and methods
class Bot:
    def __init__(self):
        self.defence_board = defence_board_maker()
        self.offence_board = offence_board_maker()
        self.attacks = []
        self.direction = None
        self.broken = 0
        self.hits = 0
    
    # Picks the direction that all the boats will face
    def direction_helper(self, size):
        if self.direction == None:
            number = randint(1, 2)
            if number == 1:
                self.direction = 'vertical'
            elif number == 2:
                self.direction = 'horizontal'
        return self.direction
    
    # Gets a random coordinate to place the center of the ship
    def ship_center_asker(self, size):
        raw_row = randint(1, 10)
        raw_column = randint(1, 20)
        return raw_row, raw_column

    # Determines the random center of a specific ship
    def center_helper(self, size, direction):
        raw_ship_row, raw_ship_column = self.ship_center_asker(size)
        if ship_center_validity_checker(self, size, direction, raw_ship_row, raw_ship_column) == False:
            return self.center_helper(size, direction)
        else:
            return raw_ship_row, raw_ship_column

    # Determines the random attack coordinate of the bot
    def attack_asker(self):
        # The row being attacked
        raw_row = randint(1, 10)
        # The column being attacked
        raw_column = randint(1, 20)
        # Making sure that the spot hasn't been attacked before
        combined_attack = str(raw_row) + str(raw_column)
        if combined_attack in self.attacks:
            return self.attack_asker()
        else:
            self.attacks.append(combined_attack)
        return raw_row, raw_column


# The code that runs the entire game
the_player = Player()
the_bot = Bot()
welcomer()
for size in [1, 1, 3, 3, 5, 5, 7, 7]:
    ship_placer(the_player, size)
    print('\nBoard of Defence')
    board_printer(the_player.defence_board)
    ship_placer(the_bot, size)
while game_winner(the_player, the_bot) == False:
    attack(the_bot, the_player)
    print('\nBoard of Offence')
    board_printer(the_player.offence_board)
    attack(the_player, the_bot)
    print('\nBoard of Defence')
    board_printer(the_player.defence_board)
if game_winner(the_player, the_bot) == 'bot':
    print('\nYou have been defeated...')
elif game_winner(the_player, the_bot) == 'player':
    print('\nYou are victorious!')