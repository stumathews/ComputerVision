class Room:
    # pass in an array of boolean to indicate presence of wall
    # [top, left, right, bottom] = [True, True, True, True]
    def __init__(self, walls, length = 10, breadth = 3):
        self.walls = walls
        self.length = length
        self.breadth = breadth

    def print_room(self):
        top = self.walls[0]
        right = self.walls[1]
        bottom = self.walls[2]
        left = self.walls[3]
        breadth = self.breadth
        length = self.length

        # print the top
        if top:
            for l in range(length):
                end = length-1
                print('_' if top else '', end='\n' if l == end else '')

        # print the sides
        for b in range(breadth):
            # print left char |
            print('|' if left else ' ', end='')

            # print the middle, discounting the left and right character, i.e '|'
            for i in range(length - 2):
                if b != breadth - 1:
                    print(' ', end='')
                else:
                    if bottom:
                        print('_', end='')

            # print right char |
            print('|' if right else ' ')


room = Room([True, True, False, False])
room.print_room()
