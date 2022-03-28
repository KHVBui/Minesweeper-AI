import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return self.cells

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # If the cell is in the sentence, remove the cell
        if cell in self.cells:
            self.cells.remove(cell)
            
            # Decrease the count of the sentence that had the mine
            self.count -= 1
            
    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # If the cell is in the sentence, remove the cell
        if cell in self.cells:
            self.cells.remove(cell)
        
        

class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        If the cell has already been marked, do nothing
        """
        if cell not in self.mines:
            self.mines.add(cell)
            
        # Check the knowledge to update sentences that only contain neighbors
        for sentence in self.knowledge:
            sentence.mark_mine(cell)
                    

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        If the cell has already been marked, do nothing
        """
        if cell not in self.safes:
            self.safes.add(cell)
            
        # Check each sentence in the knowledge for the safe cell and remove the cell 
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        
        # Used for printing information used for debugging
        DEBUG = False
        
        def generate_new_knowledge(self, new_sentences: list):
            """
            Compare each sentence in the knowledge base to each other to see if they are subsets of each other
            If so, generate a new sentence by the rule: set2 - set1 = count2 - count1
            Store the new sentences in new_sentences
            """
            for s1 in tuple(self.knowledge):
                for s2 in tuple(self.knowledge):
                    if s1 != s2 and s1.count != 0 and s2.count != 0:
                        
                        if ((s2.cells).issubset(s1.cells)):
                            temp = Sentence((s1.cells).difference(s2.cells), (s1.count-s2.count))
                            if temp not in new_sentences and temp not in self.knowledge and temp.cells != set():
                                new_sentences.append(temp) 
                                
                        if ((s1.cells).issubset(s2.cells)):
                            temp = Sentence((s2.cells).difference(s1.cells), (s2.count-s1.count))
                            if temp not in new_sentences and temp not in self.knowledge and temp.cells != set():
                                new_sentences.append(temp)       
               
        # Mark the cell as a move that has been made
        self.moves_made.add(cell)
        
        # Mark the cell as safe
        self.mark_safe(cell)
        
        # Generate a new sentence based on value of 'cell' and 'count'
        # Create count_adjuster to modify our count value based on amount of mines already found around the cell
        count_adjuster = 0
        temp_set = set()
        
        # Generate the neighboring cells from the marked safe cell to create a sentence
        for i in range(-1,2):
            for j in range(-1,2):
                
                # Create a neighboring cell
                new_cell = (cell[0]+i, cell[1]+j)
                
                # Checking if the neighbor is in bounds
                # Add the neighbor, if it is undetermined, to a set that will create a new sentence
                # Adjust the count if the neighbor is already known to be a mine
                if (((new_cell[0] <= self.height-1) and (new_cell[0] >= 0)) and ((new_cell[1] <= self.width-1) and (new_cell[1] >= 0))):
                    if new_cell not in self.safes:
                        if new_cell not in self.mines:
                            temp_set.add(new_cell)
                        else:
                            count_adjuster += 1
                            
        # The new sentence will be used to create newer sentences and will be added to the knwoeldge base         
        new_sentences = [Sentence(temp_set, count-count_adjuster)] 
        
        
        if DEBUG:
            x = 0
        
        # Add any new sentences if they can be inferred
        while True:
            
            # Test one sentence from the new sentences
            test_sentence = new_sentences.pop()
            
            # Check if the test sentence is already in the knowledge base
            # Add the test sentence to the knowledge base 
            # Generate new sentences if they can be inferred form the knowledge base
            if test_sentence not in self.knowledge:
                
                self.knowledge.append(test_sentence)
                
                generate_new_knowledge(self, new_sentences)   
                
                while True:
                    
                    # Mark any additional cells as safe or as mines
                    # while keeping track if there are any new mines or safes detected
                    num_mines = len(self.mines)
                    num_safes = len(self.safes)
                    
                    for s in self.knowledge:    
                        
                        mines = s.known_mines()
                        if mines:
                            for c in tuple(mines):
                                self.mark_mine(c)
                        
                        safes = s.known_safes()
                        if safes:    
                            for c in tuple(safes):
                                self.mark_safe(c)
                    
                    # Remove any sentence that is empty after checking for mines and safes
                    for s in tuple(self.knowledge):   
                        if s.cells == set():
                            self.knowledge.remove(s)
                    
                    for s in tuple(new_sentences):
                        if s.cells == set():
                            new_sentences.remove(s)
                            
                    # Remove any duplicate sentences after checking for mines and safes
                    for s in tuple(self.knowledge):
                        if self.knowledge.count(s) > 1:
                            self.knowledge.remove(s)
                    
                    for s in tuple(new_sentences):
                        if new_sentences.count(s) > 1:
                            new_sentences.remove(s)
                    
                    # If the knowledge base has changed by finding new mines or safes,
                    # add any new sentences if they can be inferred from the changed knowledge base
                    if (num_mines > len(self.mines)) or (num_safes > len(self.safes)):
                        
                        generate_new_knowledge(self, new_sentences)
        
                    else:
                        break
                    
            if DEBUG:               
                x += 1
                print("Temp Knowledge", x)
                for s in self.knowledge:
                    print(s)
                print("New_Sentences", x)
                for s in new_sentences:
                    print(s)
                print("Safes:", self.safes.difference(self.moves_made))
                print("Mines:", self.mines)
                    
            # If no new knowledge has been created, then stop
            if len(new_sentences) == 0:
                break
        
        if DEBUG:  
            print("\nFinal Knowledge Base")
            for s in self.knowledge:
                print(s)
            print("Safes:", self.safes.difference(self.moves_made))
            print("Mines:", self.mines)
            print()            
            

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        
        # Create a set of all moves that haven't been chosen and are safe
        
        available_moves = self.safes.difference(self.moves_made)
        
        # Return a random safe move if there are safe moves available
        return random.choice(list(available_moves)) if available_moves else None
        
        

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # Create a set of all moves that haven't been chosen and aren't mines
        available_moves = [(i,j) for i in range(self.height) for j in range(self.width) if ((i,j) not in self.moves_made and (i,j) not in self.mines)]
        
        # Return a random move if there are moves available
        return random.choice(available_moves) if available_moves else None
