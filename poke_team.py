from __future__ import annotations

"""
This file contains the class: Action, Criterion, PokeTeam
The goal of this file is to set up a team with functionalities to reorganise the order of the team
as well as to set up automated functions for it to either attack, swap, heal or special
"""
__author__ = "Scaffold by Jackson Goerner, Code by ______________"

from enum import Enum, auto
from pokemon_base import PokemonBase, PokeType
from stack_adt import ArrayStack
from queue_adt import CircularQueue
from random_gen import RandomGen
from array_sorted_list import *
from pokemon import *
from linked_list import *

class Action(Enum):
    """
    Decides on an action for a Pokemon
    """
    ATTACK = auto()
    SWAP = auto()
    HEAL = auto()
    SPECIAL = auto()
    
class Criterion(Enum):
    """
    The criterion it will base the order of the pokemon on
    """
    SPD = auto()
    HP = auto()
    LV = auto()
    DEF = auto()

class PokeTeam(ArrayStack, CircularQueue, ArraySortedListBattle2):
    """
    PokeTeam is a class that creates a team of Pokemon by placing it either in an ArrayStack, Circular Queue, or a sorted list
    """
    class AI(Enum):
        ALWAYS_ATTACK = auto()
        SWAP_ON_SUPER_EFFECTIVE = auto()
        RANDOM = auto()
        USER_INPUT = auto()

    def __init__(self, team_name: str, team_numbers: list[int], battle_mode: int, ai_type: PokeTeam.AI, criterion=None, criterion_value=None) -> None:
        """
        Initialises PokeTeam and creates a team of Pokemons using the team_numbers provided
        Depending on the battle_mode, the Poketeam will either be stored in an Arraystack, CircularQueue or a SortedList

        Best case complexity: O(n), where n is the integer inside the list of "team_numbers"
        Worse case complexity: O(n * log2(m)), where n is the integer inside the list of "team_numbers" and m is the length of SortedList
        """
        if type(team_name) != str:
            raise ValueError ("team_name is not equal to a string")
        if type(battle_mode) != int:
            raise ValueError ("battle_mode is not equal to an int")
        if type(ai_type) != PokeTeam.AI:
            raise ValueError ("ai_type is not valid")
        
        self.team_name = team_name
        self.team_numbers = team_numbers
        self.length = 0
        self.battle_mode = battle_mode
        self.criterion = criterion
        self.heal_counter = 0
        if not self.criterion == None:
            self.criterion_value = self.criterion.value
        self.ai_type = ai_type
        # c, b, s, g, e = Charmander(), Bulbasaur(), Squirtle(), Gastly(), Eevee()
        try:
            if self.battle_mode == 0:
                ArrayStack.__init__(self,6)
                for _ in range(team_numbers[4]):
                    self.push(Eevee())
                for _ in range(team_numbers[3]):
                    self.push(Gastly())
                for _ in range(team_numbers[2]):
                    self.push(Squirtle())
                for _ in range(team_numbers[1]):
                    self.push(Bulbasaur())
                for _ in range(team_numbers[0]):
                    self.push(Charmander())
            elif self.battle_mode == 1:
                CircularQueue.__init__(self,6)
                for _ in range(team_numbers[0]):
                    self.append(Charmander())
                for _ in range(team_numbers[1]):
                    self.append(Bulbasaur())
                for _ in range(team_numbers[2]):
                    self.append(Squirtle())
                for _ in range(team_numbers[3]):
                    self.append(Gastly())
                for _ in range(team_numbers[4]):
                    self.append(Eevee())
            elif self.battle_mode == 2:
                self.battle2special = 2 #For battle mode 2 special
                ArraySortedListBattle2.__init__(self,6,self.criterion_value,self.battle2special)
                for _ in range(team_numbers[4]):
                    self.add(Eevee())
                for _ in range(team_numbers[3]):
                    self.add(Gastly())
                for _ in range(team_numbers[2]):
                    self.add(Squirtle())
                for _ in range(team_numbers[1]):
                    self.add(Bulbasaur())
                for _ in range(team_numbers[0]):
                    self.add(Charmander())

            self.matches_played = 0
        except:
            raise ValueError ("team_numbers is not a list or the element inside the list is not an int")

    @classmethod
    def random_team(cls, team_name: str, battle_mode: int, team_size=None, ai_mode=None, **kwargs):
        """
        Description:

        Arguments:
        team_name: The name of the team.
        battle_mode: The selected battle mode 
        team_size: The amount of pokemon in the team, if not team size is given generate random team size.
        ai_mode: The desired choice of action 
        kwargs: Criterion, which is the order of the Pokemon in the Poketeam

        Worst case complexity O(log2(m) + k), where m is length of the ArraySortedList and k is kwargs
        Best case scenario O(1), if the SortedList adds it to the middle every single time

        Returns:
        Returns PokeTeam class      
        """
        # step 1
        # if no team_size is given, team size = randint(half of pokemon limit, pokemon limit)
        if team_size == None:
            team_size = RandomGen.randint(3, 6)     # the 3 is half the team size, the 6 is the full team size
        
        # step 2
        # Create a sorted list, add the values 0 and team size, and generate 4 random
        # numbers from 0 to team size and insert them into the sorted list
        # im gonna use array_sorted_list as its already given to us. i THINK we can use it
        sorted_list = ArraySortedList(6)
        sorted_list.add(0)
        sorted_list.add(team_size)

        for i in range(4):      # this is correct
            random_num = RandomGen.randint(0, team_size)
            sorted_list.add(random_num)     # it will never access the resize method or the entire team is wrong
        
        # differences = how many of each pokemon will be on the team
        charmander_amount = sorted_list[1] - sorted_list[0]
        bulbasur_amount = sorted_list[2] - sorted_list[1]
        squirtle_amount = sorted_list[3] - sorted_list[2]
        gastly_amount = sorted_list[4] - sorted_list[3] 
        eevee_amount = sorted_list[5] - sorted_list[4]
        team_numbers = [charmander_amount, bulbasur_amount, squirtle_amount, gastly_amount, eevee_amount]   # end of page 16, says this is allowed
        if ai_mode == None:     # doesnt this have to be self.ai_mode
            ai_mode = PokeTeam.AI.RANDOM
        
        criterion = None
        criterion_value = None
        for key, value in kwargs.items():
            criterion = value
            criterion_value = criterion.value

        return PokeTeam(team_name, team_numbers, battle_mode, ai_mode, criterion, criterion_value)

        # If no AI mode is specified, the PokeTeam should pick options at random (for all
        # options available, so heal should be removed from the options after 3 heals)
        # ^ idk what this means, will worry about it later

    def __len__(self) -> int:
        """
        Description:
        "__len__" is a magic method of the class PokeTeam. It returns the length of a pokemon team.

        Complexity: best and worst case complexity is O(1)
        
        Arguments: 
        "__len__" takes no arguments.

        Returns:
        Returns the length of the poekmon team as an integer.
        """
        return self.length
        
    def return_pokemon(self, poke: PokemonBase) -> None:
        """
        Description:
        "return_pokemon" is a method of the class PokeTeam, it returns a pokemon from the field, depending on the battle mode selected, it will then return the pokemon to a specific place in the pokemon team:
        battle_mode == 0 --> returns the pokemon to the front of the team, having everything shuffle down.
        battle_mode == 1 --> returns the pokemon to the end of the team, having stay where they are.
        battle_mode == 2 --> returns the pokemon to their correcct position within the ordering of the team.

        Best case compplexity is O(1)
        Worst case complexity is O(log2(n)), where n is the length of the list

        Arguments:
        poke: the pokemon to be returned

        Returns:
        None

        Complexity : Best Case : O(1) -> if ballte mode is 0 or 1
                     Worst Case: O(n) where n is the maxiumum number of pokemons in a team. This is for battle mode 2.
        """
        if not poke.is_fainted():
            if self.battle_mode == 0:
                
                self.push(poke)
            elif self.battle_mode == 1:
                
                self.append(poke)
            elif self.battle_mode == 2:
                
                self.add(poke)

    def retrieve_pokemon(self) -> PokemonBase | None:
        """
        Description:
        "retrieve_pokemon" is a method of the class PokeTeam, it retreives a pokemon into the field from the pokemon team list depending on the battle mode selected:
        battle_mode == 0 --> retrieves the first pokemon in the team, having everyone shuffle up
        battle_mode == 1 --> retreives the first pokemon in the team, having everyone shuffle up
        battle_mode == 2 --> retreives the pokemon from the front of the team, having every shuffle up.

        Complexity: Best Case : O(1) -> if ballte mode is 0 or 1
                    Worst Case: O(n) where n is the maxiumum number of pokemons in a team. This is for battle mode 2 (shuffle left)

        Arguments: 
        None

        Returns:
        Returns the pokemon retrieved at that location.        
        """
        if self.battle_mode == 0:
            return self.pop()
     
        elif self.battle_mode == 1:
            return self.serve()

        elif self.battle_mode == 2:
            return self.delete_at_index(0)

    def special(self):
        """
        Description: 
        "special" is a method of the class PokeTeam, it manipulates the order of a pokemon team depending on the battle mode selected:
        battle_mode == 0 --> swaps the first and last pokemon on the team
        battle_mode == 1 --> swaps the first and second halves of the team and reverse the order of the previously front half of the team
        battle_mode == 2 --> reverses the sorting order of the team

        Best case is O(n), where n is the length of the list // 2
        Worst case is O(n^2), where n is the length of the list
        Arguments:
        None

        Returns:
        None    

        Complexity : Best Case    
        """
        if self.battle_mode == 0:
            if self.length >= 2:
                pokemon = LinkedList(self.length)
                while not ArrayStack.is_empty(self): 
                    pokemon.append(self.pop())

                self.push(pokemon[0])
                for index in range(len(pokemon)-2,0,-1):
                    self.push(pokemon[index])
                self.push(pokemon[len(pokemon)-1])
            else:
                return

        elif self.battle_mode == 1:
            if self.length >= 2:
                temp_queue = CircularQueue(self.length) #for first half
                temp_stack = ArrayStack(self.length) #for second half

                for _ in range(0,self.length//2): #first half (reverse)
                    poke = self.queue_peek()
                    temp_stack.push(poke)
                for _ in range(self.length//2,self.length): #second half
                    poke = self.queue_peek()
                    temp_queue.append(poke)

                CircularQueue.clear(self) 
                while not CircularQueue.is_empty(temp_queue):
                    poke = temp_queue.serve()
                    self.append(poke)
                while not ArrayStack.is_empty(temp_stack):
                    poke = temp_stack.pop()
                    self.append(poke)
            else:
                return

        elif self.battle_mode == 2:
            #Use odd/even numbers to differentiate between the two
            #Reverses the order of the list
            if self.length >= 2:
                self.special_mode_increment()
                temp_stack = ArrayStack(self.length)
                for _ in range(0,self.length):
                    temp_stack.push(self.retrieve_pokemon())
                
                while not ArrayStack.is_empty(temp_stack):
                    poke = temp_stack.pop()
                    self.add(poke)
            else:
                return

            

    def regenerate_team(self):
        """
        Description:
        "regenerate_team" is a method of the class PokeTeam, it makes the existing team ready for another battle.

        Complexity:
        Best case complexity: O(n), where n is the integer inside the list of "team_numbers"
        Worse case complexity: O(n * log2(m)), where n is the integer inside the list of "team_numbers" and m is the length of SortedList

        Arguments:
        None

        Returns:
        None
        """
        if self.criterion != None and self.criterion_value != None:
            if self.matches_played == 0:
                self.__init__(self.team_name,self.team_numbers,self.battle_mode,self.ai_type,self.criterion,self.criterion_value)
            else:
                matches_played = self.matches_played
                self.__init__(self.team_name,self.team_numbers,self.battle_mode,self.ai_type,self.criterion,self.criterion_value)
                self.matches_played = matches_played
        else:
            if self.matches_played == 0:
                self.__init__(self.team_name,self.team_numbers,self.battle_mode,self.ai_type)
            else:
                matches_played = self.matches_played
                self.__init__(self.team_name,self.team_numbers,self.battle_mode,self.ai_type)
                self.matches_played = matches_played

    
    def __str__(self):
        """
        Description:
        "__str__" is a magic method of the class PokeTeam, it returns a valid string representation of the pokemon team.

        Worst case complexity is O(n^2)
        Best case complexity is O(n)

        Arguments:
        None

        Returns:
        Returns a valid string representation of a pokemon team. An example is shown below:
        "Dawn (2): [LV. 1 Gastly: 6 HP, LV. 1 Squirtle: 11 HP, LV. 1 Bulbasaur: 13 HP, LV. 1 Eevee: 10 HP, LV. 1 Charmander: 9 HP]"
        """
        team_name = self.team_name
        battle_mode = self.battle_mode
        poketeam_string = f"{team_name} ({battle_mode}): ["

        if self.battle_mode == 0:
            temp_stack = ArrayStack(6)
            actual_length = len(self)
            for i in range(len(self)):
                poke = self.retrieve_pokemon()
                temp_stack.push(poke)
                if i != actual_length - 1:
                    poketeam_string = poketeam_string + f"{poke}, "
                else:
                    poketeam_string = poketeam_string + f"{poke}]"
            while not ArrayStack.is_empty(temp_stack):
                self.push(temp_stack.pop())

        elif self.battle_mode == 1:
            temp_queue= CircularQueue(6)
            actual_length = len(self)
            for i in range(len(self)):
                poke = self.retrieve_pokemon()
                temp_queue.append(poke)
                if i != actual_length-1:
                    poketeam_string = poketeam_string + f"{poke}, "
                else:
                    poketeam_string = poketeam_string + f"{poke}]"
            while not CircularQueue.is_empty(temp_queue):
                self.append(temp_queue.serve())
                
        elif self.battle_mode == 2:
            for i in range(len(self)):
                if i != len(self)-1:
                    poketeam_string = poketeam_string + f"{self[i]}, "
                else:
                    poketeam_string = poketeam_string + f"{self[i]}]"

        return poketeam_string


    def is_empty(self):
        """
        Description:
        "is_empty" is a method of the class PokeTeam. It returns a boolean value of whether or not the pokemon team is empty or not. 

        Complexity: O(1)

        Arguments:
        None

        Returns:
        Returns a boolean TRUE if the legnth of the pokemon team is 0 (empty). Otherwise, return a boolean FALSE. 
        """
        return len(self) == 0

    def choose_battle_option(self, my_pokemon: PokemonBase, their_pokemon: PokemonBase) -> Action:
        """
        Description:
        "choose_battle_option" is a method of the class PokeTeam. This method decides the AI of the pokemon, it dictates the action depending on the 
        pokemon currently on the field.

        Complexity: O(1)

        Arguments:
        my_pokemon --> pokemon on team choosing battle option
        their_pokemon --> pokemon on the opposing team

        Returns:
        Returns either Action.ATTACK, Action.SWAP, Action.HEAL or Action.SWAP depending on the inputs.
        """
        if self.ai_type.value == 1:   # always_attack
            return Action.ATTACK
            
        if self.ai_type.value == 2:   # swap_on_super_effective
            burn_effective_attack_multiplier = 1 
            if my_pokemon.status_effect == "Burn":
                burn_effective_attack_multiplier = 0.5 
                
            attack_multiplier = PokeType(my_pokemon.poke_type, their_pokemon.poke_type)
            type_multiplier = attack_multiplier.multiplier()
            effective_attack = (burn_effective_attack_multiplier)*(type_multiplier) #Multiplier depending on attacking and defending pokemon
            
            if effective_attack >= 1.5:   
                return Action.SWAP
            else:
                return Action.ATTACK

        if self.ai_type.value == 3:   # random
            actions = list(Action)
            if self.heal_counter >= 3:
                actions.remove(Action.HEAL)
            action = actions[RandomGen.randint(0, len(actions)-1)]
            if action == Action.HEAL:
                self.heal_counter += 1
            return action


        if self.ai_type.value == 4:   # user_input
            print('1. Attack\n2. Swap\n3. Heal\n4. Special')
            choice = input("Input an integer to choose an action: ")
            if choice == 1:
                return Action.ATTACK
            if choice == 2:
                return Action.SWAP
            if choice == 3:
                return Action.HEAL
            if choice == 4:
                return Action.SPECIAL


    @classmethod
    def leaderboard_team(cls):
        raise NotImplementedError()