from __future__ import annotations


"""
This creates a "tower" of teams to fight against. The tower uses 2 Linkedlists
1 Linkedlist to store each team and another Linkedlist to store the number of lives of the teams
"""



from poke_team import PokeTeam
from battle import Battle
from random_gen import *
from linked_list import LinkedList
from stack_adt import ArrayStack

class BattleTower:
    """
    The goal of this class is to create a series of Poketeams to defeat with each Poketeam having a set amount of lives

    """
    def __init__(self, battle: Battle|None=None) -> None:
        """
        This initialises the BattleTower class.
        """
        self.opponent_teams = LinkedList()   
        self.battle = battle    
        self.team = None
        self.n = None

    def set_my_team(self, team: PokeTeam) -> None:
        """
        Description: 
        "set_my_team" is a method of the class BattleTower, it sets up the team that will be fighting through the tower.

        Complexity: O(1)

        Arguments:
        team: the team that is going to be fighting through the tower 

        Returns: 
        None        
        """
        self.team = team
    
    def generate_teams(self, n: int) -> None:
        """
        Description: 
        "generate_teams" is a method of the class BattleTower, it generates "n" amount of teams that will be used for the battle tower.

        Complexity: O(n*m)

        Arguments:
        n: an integer value that dictates how many teams will be used in the pokemon tower.

        Returns:
        None
        """
        if type(n) != int:
            raise ValueError ("n is not an int")
        self.n = n
        opp_num = 0
        self.num_lives_linked_list = LinkedList(n)
        for _ in range(n):
            # this is used for debugging for later on
            opp_num += 1
            
            battle_mode = RandomGen.randint(0, 1)
            
            team = PokeTeam.random_team(f"Opponent {opp_num}", battle_mode)
            self.opponent_teams.append(team)

            num_lives = RandomGen.randint(2,10)
            self.num_lives_linked_list.append(num_lives)    

    def __iter__(self):
        """
        Description:
        "__iter__" is a magic method of the class BattleTower, it returns an iterator for the given object.

        Complexity: O(1)

        Argument:
        None

        Returns:
        None 
        
        """
        return BattleTowerIterator(self.opponent_teams, self.num_lives_linked_list, self.team, self.battle)

    # def __next__(self):
    #     opp_team = self[self.iindex] # self,iindex is the poketeam we are facing
    #     opp_team.regenerate_team()
    #     self.team.regenerate_team()
    #     battle_result = self.battle.battle(self.team, opp_team)
    #     lives = self.num_linked_list[self.iindex]
    #     if battle_result == 1:
    #         lives -= 1
    #     if lives == 0:
    #         self.delete_at_index(self.iindex)
    #         self.num_linked_list.delete_at_index(self.iindex)
    #     if self.iindex == self.n:    # not sure if the len statement works
    #         self.iindex = 0
    #     else:
    #         self.iindex += 1
    #     return (battle_result, self.team, self.iindex, lives)
        
class BattleTowerIterator:
    """
    This class is used to iterate through the tower where one iteration is one battle completed. 
    """
    def __init__(self, opponent_teams: LinkedList, lives_list: LinkedList, team: PokeTeam, battle: Battle) -> None:
        """
        initiailises the BattleTowerIterator class
        """
        self.current = opponent_teams.head
        self.lives_current = lives_list.head
        self.team = team
        self.battle = battle
        self.opponent_team = opponent_teams
        self.lives = lives_list
        self.battle_result = None

    def __iter__(self):
        """
        Description:
        "__iter__" is a magic method of the class BattleTowerIterator, it returns the the iterator for the given object.

        Complexity: O(1)

        Arguments:
        None 

        Returns:
        Returns the the iterator object itself.
        """
        return self
    
    def __next__(self): ####ADD STUFF FROM DUPLICATES ONTO HERE AND HOPE FOR THE BEST ## Chhnage lives_current to current_lives. add self. to lives_previous later
        """
        Description:
        "__next__" is a magic method of the class BattleTowerIterator, it simulates one battle in the tower.

        Complexity: O(B)

        Arguments:
        None

        Returns:
        Returns a tuple of four elements in the order: battle_result (who won/draw the battle), the players team after the battle, 
        the opposing team after the battle and the remaining lives of the tower team.
        """
        
        if self.battle_result != 2 and self.current is not None:
            opp_team = self.current.item
            opp_team.regenerate_team()
            self.team.regenerate_team()
            self.battle_result = self.battle.battle(self.team, opp_team)

            lives = self.lives_current.item
            if self.battle_result == 1:
                lives -= 1
                self.lives_current.item -= 1
            if lives == 0:
                if self.opponent_team.head == self.current:
                    self.opponent_team.head = self.current.next
                    self.previous_node = self.opponent_team.head
                    self.current = self.opponent_team.head
                    self.opponent_team.length -=1

                    self.lives.head = self.lives_current.next
                    self.lives_previous = self.lives.head
                    self.lives_current = self.lives.head
                    self.lives.length -=1
                elif self.current.next == None:
                    self.previous_node.next = None
                    self.opponent_team.length -=1

                    self.lives_previous.next = None
                    self.lives.length -=1
                else:
                    self.previous_node.next = self.current.next
            if self.current.next == None:
                self.current = self.opponent_team.head
                self.lives_previous = self.lives_current
                self.lives_current  = self.lives.head
            else:       
                self.previous_node = self.current
                self.current = self.current.next
                self.lives_previous = self.lives_current
                self.lives_current = self.lives_current.next
            
            return (self.battle_result, self.team, opp_team, self.lives_previous.item)
        else:
            raise StopIteration
        
    
    def avoid_duplicates(self) -> None:
        """
        Description:
        "avoid_duplicates" is a method of the class BattleTowerIterator that removes all currently alive trainers from the battle tower which 
        have multiple pokemon with the same types.

        Complexity: O(N*P)
        
        Arguments: 
        None 

        Returns:
        None
        """
        self.current = self.opponent_team.head
        self.current_lives = self.lives.head
        for i in range(0,len(self.opponent_team)):
            a = self.current.item.retrieve_pokemon()
            b = self.current.item.retrieve_pokemon()
            for x in range(0, len(self.current.item)+1):
                if a.get_poke_name() == b.get_poke_name():
                    if self.opponent_team.head == self.current:
                        self.opponent_team.head = self.current.next
                        self.previous_node = self.opponent_team.head
                        self.current = self.opponent_team.head
                        self.opponent_team.length -=1

                        self.lives.head = self.current_lives.next
                        self.previous_lives = self.lives.head
                        self.current_lives = self.lives.head
                        self.lives.length -=1
                        break
                    elif self.current.next == None:
                        self.previous_node.next = None
                        self.opponent_team.length -=1

                        self.previous_lives.next = None
                        self.lives.length -=1
                        break
                    else:
                        self.previous_node.next = self.current.next
                        self.current = self.previous_node.next
                        self.opponent_team.length -=1

                        self.previous_lives.next = self.current_lives.next
                        self.current_lives = self.previous_lives.next
                        self.lives.length -=1
                        break
                else:
                    if self.current.item.is_empty():
                        self.previous_node = self.current
                        self.current = self.current.next

                        self.previous_lives = self.current_lives
                        self.current_lives = self.current_lives.next
                        break
                    else:
                        a, b = b, self.current.item.retrieve_pokemon() 


    # def sort_by_lives(self):
    #     # 1054
    #     raise NotImplementedError()
