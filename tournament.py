from __future__ import annotations


"""
This file sets up a tournament in a single elimination style. A pair of Poketeam will fight with each other and the loser is eliminated.
The winner will proceed to fight with another winner until everyone else has been eliminated given that the correct string representation
is presented.
"""
__author__ = "Scaffold by Jackson Goerner, Code by ______________"

from poke_team import PokeTeam
from battle import Battle
from linked_list import LinkedList
from queue_adt import CircularQueue
from stack_adt import ArrayStack, Stack
from bset import BSet

class Tournament:
    """
    This class sets up a tournament for teams of Pokemon to fight against each other
    """
    def __init__(self, battle: Battle|None=None) -> None:
        """
        Initialises the Tournament class. Creates Linkedlists for later use. 
        """
        self.battle= battle
        if battle == None:
            self.battle = Battle(verbosity=0)
        self.conditional = False
        self.lst_plus_sign = LinkedList()       # this is for the + signs 
        self.loser_queue = None
        self.switch_counter = 1

        

    def set_battle_mode(self, battle_mode: int) -> None:
        """
        Description: 
        "set_battle_mode" is a method of the class Tournament, it sets the battle mode for all randomly generated teams. 

        Arguments:
        battle_mode: the selected battle mode 

        Complexity: O(1)

        Returns:
        None
        """
        self.battle_mode = battle_mode

    def is_valid_tournament(self, tournament_str: str) -> bool:
        """
        Description: 
        "is_valid_tournament" is a method of the class Tournament, it returns a boolean value depending on if tournament_str is a valid tournament.

        Complexity: O(n*m)

        Arguments:
        tournament_str: a string representation of a tournament 

        Returns 
        Returns a boolean TRUE if tournament_str was a valid tournament, otherwise returns a boolean FALSE.        
        """
        
        s = tournament_str.split(" ")

        self.lst_plus_sign.clear()
        plus_position = 0
        for i in range(len(s)):
            iter = 1
            if s[i] == "+":     
            
                if i > plus_position:
                    while i > plus_position:

                        if i + iter == len(s):
                            plus_position = len(s)
                            break

                        if s[i + iter] == "+":
                            iter += 1
                            
                        else:
                            plus_position = i + iter 
                    
                    if i < plus_position:
                        self.lst_plus_sign.append(iter)

                        if i + iter == len(s):
                            break

        counter = 0
        counter_plus = 0
        for i in s:
            if i != "+":
                counter += 1
            else:
                counter_plus += 1
        self.lst = CircularQueue(counter)
        self.lst1 = ArrayStack(counter) 
        self.lst2 = ArrayStack(counter)

        if counter % 2 == 0 and (counter - counter_plus) == 1:
            for i in range(len(self.lst_plus_sign)):

                if self.lst_plus_sign[i] > i + 1:
                    self.lst_plus_sign_current = self.lst_plus_sign.head
                    return False
            self.lst_plus_sign_current = self.lst_plus_sign.head
            return True
        else:
            self.lst_plus_sign_current = self.lst_plus_sign.head
            return False
        

    def is_balanced_tournament(self, tournament_str: str) -> bool:
        # 1054 only
        raise NotImplementedError()

    def start_tournament(self, tournament_str: str) -> None:
        """
        Description: 
        "start_tournament" is a method of the class Tournament, it generates teams based on tournament_str but does not intiate any games.

        Complexity: O(n)

        Arguments:
        tournament_str: a string representation of a tournament 

        Returns: 
        None        
        """

        if type(tournament_str) != str:
            raise ValueError 
        # self.lst.clear()
        if self.is_valid_tournament(tournament_str):
            s = tournament_str.split(" ")
            self.loser_stack = ArrayStack(len(s))
            for i in range(len(s)):
                if s[i] != "+":     

                    t = PokeTeam.random_team(f"{s[i]}", self.battle_mode)
                    self.lst.append(t)
                    int1 = 0
                    for char in s[i]:
                        int1 += ord(char)
        else:
            raise ValueError()


    def advance_tournament(self) -> tuple[PokeTeam, PokeTeam, int] | None:
        """
        Description: 
        "advance_tournament" is a method of the class Tournament, it simulates one battle of the tournament, following the order 
        of the previously given tournament string. 

        Complexity: O(B+P)

        Arguents:
        None 

        Returns:
        If there are still games remaining, return a tuple containing (?). Otherwise, return None.
        """
        
        if len(self.lst) == 0 and len(self.lst1) == 1:
            return None
        else:
            if self.conditional:
                player2 = self.lst1.pop()
                player1 = self.lst1.pop()
            else:
                player1 = self.lst.serve()
                player2 = self.lst.serve()

            player1.regenerate_team()
            
            player2.regenerate_team()
            res = self.battle.battle(player1, player2)
            name1 = player1.team_name
            name2 = player2.team_name

            if res == 1:
                player1.matches_played += 1
                self.lst1.push(player1)
                self.lst2.push(player1)
                self.loser_stack.push(player2)
            if res == 2:
                player2.matches_played += 1
                self.lst1.push(player2)
                self.lst2.push(player2)
                self.loser_stack.push(player1)

            self.lst_plus_sign_current.item -= 1
            if self.lst_plus_sign_current.item != 0:
                self.conditional = True
                self.switch_counter +=1
            else:
                self.lst_plus_sign_current = self.lst_plus_sign_current.next
                self.conditional = False

            return name1, name2, res

    def linked_list_of_games(self) -> LinkedList[tuple[PokeTeam, PokeTeam]]:
        """
        Description:
        "linked_list_of_games" is a method of the class Tournament, it (?)

        Arguments:
        None 

        Returns:
        Returns a tuple the names two teams that battle.

        Complexity: : O(M), where M is the total number of matches played
        """
        l = LinkedList()
        while True:
            res = self.advance_tournament()
            if res is None:
                break
            l.insert(0, (res[0], res[1]))
        return l
    
    def linked_list_with_metas(self) -> LinkedList[tuple[PokeTeam, PokeTeam, list[str]]]:
        """
        Description:
        "linked_list_with_metas" is a method of the class Tournament, it returns a linked list, containing a tuple for each match 
        of the tournament in the same order as linked_list_of_games.

        Arguments:
        None

        Returns:
        Returns a tuple with three elements, the names of the two teams that battle, and  a list of strings representing PokeTypes which, for the particular battle listed, are
        not present in either PokeTeam, but were represented by some other PokeTeam, which if they hadn't lost any of their matches, would be playing this match
        
        Complexity: : O(M * P), where M is the total number of matches played and P is the limit on the number of pokemon per team
        """
        custom_set = BSet()
        custom_set2 = BSet()
        lst = []
        l = LinkedList()
        Max_Poke_Capacity = 6
        while True:
            res = self.advance_tournament()
            if res is None:
                break
            x = self.loser_stack.pop()
            x.regenerate_team()
            y = self.lst2.pop()
            y.regenerate_team()
            for _ in range(0,Max_Poke_Capacity):
                if not x.is_empty():
                    poke_x = x.retrieve_pokemon()
                    if poke_x.poke_type == 'Fire':
                        custom_set.add(1)
                        custom_set2.add(1)
                    elif poke_x.poke_type == 'Grass':
                        custom_set.add(2)
                        custom_set2.add(2)
                    elif poke_x.poke_type == 'Water':
                        custom_set.add(3)
                        custom_set2.add(3)
                    elif poke_x.poke_type == 'Ghost':
                        custom_set.add(4)
                        custom_set2.add(4)
                    elif poke_x.poke_type == 'Normal':
                        custom_set.add(5)
                        custom_set2.add(5)
                if not y.is_empty():
                    poke_y = y.retrieve_pokemon()
                    if poke_y.poke_type == 'Fire':
                        custom_set2.add(1)
                    elif poke_y.poke_type == 'Grass':
                        custom_set2.add(2)
                    elif poke_y.poke_type == 'Water':
                        custom_set2.add(3)
                    elif poke_y.poke_type == 'Ghost':
                        custom_set2.add(4)
                    elif poke_y.poke_type == 'Normal':
                        custom_set2.add(5)
        
            if y.matches_played > 1:
                if 1 not in custom_set2:
                    if 1 in custom_set:
                        lst.append('FIRE') # Note: You can use a tuple/list for the output. lst is being used for ouput.
        
                if 2 not in custom_set2:
                    if 2 in custom_set:
                        lst.append('GRASS')
            
                if 3 not in custom_set2:
                    if 3 in custom_set:
                        lst.append('WATER')
        
                if 4 not in custom_set2:
                    if 4 in custom_set:
                        lst.append('GHOST')

                if 5 not in custom_set:
                    if 5 in custom_set:
                        lst.append('NORMAL')
            l.insert(0, (res[0], res[1], list(lst)))
            lst.clear()
            custom_set2.clear()
        return l
            

    
    # def flip_tournament(self, tournament_list: LinkedList[tuple[PokeTeam, PokeTeam]], team1: PokeTeam, team2: PokeTeam) -> None:
    #     # 1054
    #     raise NotImplementedError()