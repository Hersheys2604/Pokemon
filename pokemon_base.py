from __future__ import annotations
from abc import ABC, abstractmethod
from random_gen import RandomGen
from math import floor, ceil

"""
The file contains classes: PokemonBase, PokeType
Each Pokemon should contain the PokemonBase class as all pokemons should have the functionalities created in PokemonBase
Poketype uses the type of the Pokemon attacking and the Pokemon being attacked to determine the multiplier used for attack
"""
__author__ = "Scaffold by Jackson Goerner, Code by ______________"



class PokemonBase(ABC):
    """
    This class creates characteristics/attributes that every pokemon should have
    """

    def __init__(self, hp: int, poke_type: str) -> None:
        """ 
        Initialises multiple functionalities that each pokemon has. 
        All methods unless stated otherwise have a best case and worst case complexity of O(1) 
        
        The init function has a best case and worst case complexity of O(k) where k is the cost of comparison for strings
        """
        try:
            int(hp)
            type(poke_type) == str
            poke_type == "Fire" or poke_type == "Water" or poke_type == "Grass" or poke_type == "Ghost" or poke_type == "Normal"
        except:
            raise ValueError
        else:
            self.hp = hp
            self.poke_type = poke_type
            self.evolve_to = None
            self.status_effect = None

    def is_fainted(self) -> bool:
        """
        Description:
        "is_fainted" is a method of the class PokemonBase that returns a boolean value TRUE or FALSE depending 
        on if the pokemon's hp is less than or equal to 0. When a pokemon's hp is equal to or less than 0, the 
        pokemon is considered to be "fainted".

        Complexity: O(1)

        Arguments: 
        Takes no arguement.

        Returns:
        Returns a boolean TRUE if a pokemon has fainted (their hp is equal to or less than 0) or boolean FALSE if a pokemon's has 
        not fainted (their hp is greater than 0)
        """
        return self.hp <= 0


    @abstractmethod
    def level_up(self) -> None:
        pass

    def get_speed(self) -> int:
        """
        Description: 
        "get_speed" is a method of the class PokemonBase that returns the speed of the pokemon.

        Complexity: O(1)

        Arguments: 
        Takes no arguement.

        Returns: 
        Returns the speed of the pokemon as a integer value.
        """
        return self.speed

    def get_attack_damage(self) -> int:
        """
        Description: 
        "get_attack_damage" is a method of the class PokemonBase that returns the attack damage of the pokemon. 

        Complexity: O(1)
        
        Arguments:
        Takes no arguement.

        Returns:
        Returns the attack damage of the pokemon as a integer value.
        """
        return self.attack_power

    def get_defence(self) -> int:
        """
        Description:
        "get_defence" is a method of the class PokemonBase that returns the defence value of the pokemon.

        Complexity: O(1)
        
        Arguments:
        Takes no arguement.

        Returns:
        Returns the defence value of the pokemon as an integer value.
        """
        return self.defence

    def lose_hp(self, lost_hp: int) -> None:
        """
        Description: 
        "lose_hp" is a method of the class PokemonBase that decrements the hp of a pokemon by the value of its argument.

        Complexity: O(1)

        Arguments:
        Takes one argument, lost_hp that the amount of health the pokemon loses.

        Returns:
        No return values.
        """
        self.hp = self.hp - lost_hp
        if self.hp - floor(self.hp) < 0.5:
            return floor(self.hp)
        return ceil(self.hp)
        
    @abstractmethod
    def defend(self, damage: int) -> None:
        pass
    
    @abstractmethod
    def attack(self, other: PokemonBase):
        pass

    def get_poke_name(self) -> str:
        """
        Description:
        "get_poke_name" is a method of the class PokemonBase that returns the name of the pokemon.

        Complexity: O(1)

        Arguments: 
        Takes no arguments. 

        Returns:
        Returns the name of the pokemon as a string.
        """
        return self.name
    
    def get_hp(self) -> int:
        """
        Description: 
        "get_hp" is a method of the class PokemonBase that returns the current hp of the pokemon. 

        Complexity: O(1)

        Arguments: 
        Takes no arguments. 

        Returns:
        Returns the current hp of the pokemon as an integer.
        """
        return self.hp
    
    def get_level(self) -> int:
        """
        Description:
        "get_level" is a method of the class PokemonBase that returns the current level of the pokemon.

        Complexity: O(1)

        Arguments:
        Takes no arguments. 

        Returns:
        Returns the current level of the pokemon as an integer.
        
        """
        return self.level

    @abstractmethod
    def heal(self):
        pass
        
    def __str__(self) -> str:
        """
        Description: 
        "__str__" is a magic method of the class PokemonBase that returns a string with information of the current pokemon.

        Complexity: O(1)

        Arguments:
        Takes no arguments. 

        Returns:
        Returns the level, name and hp of the pokemon as a string.
        
        """
        return f"LV. {self.level} {self.name}: {self.hp} HP"
        
    @abstractmethod
    def should_evolve(self) -> bool:
        pass

    def can_evolve(self) -> bool:
        """
        Description: 
        "can_evolve" is a method of the class PokemonBase that returns a boolean value depending on whether or not the current pokemon can further evovlve.
        Note that this method tells us if it is POSSIBLE for the pokemon to return or not, not whether or not it is of level to evolve.

        Complexity: O(1)

        Arguments:
        Takes no argument.

        Returns:
        Returns a boolean TRUE if the pokemon is able to further evolve, returns a boolean FALSE if the pokemon is unable to further evolve (final form).
        
        """
        if self.evolve_to == None:
            return False
        else:
            return True

    @abstractmethod
    def get_evolved_version(self) -> PokemonBase:
        pass #Done

    def clear_status_effects(self):
        """
        Description: 
        "clear_status_effects" is a method of the class PokemonBase, it clears the status effects of the pokemon.

        Complexity: O(1)

        Arguments: 
        None 

        Returns: 
        None        
        """
        self.status_effect = None

class PokeType:
    """
    This class uses the Pokemon's type to determine the attack multiplier (whether it is super effective or not)
    """

    FIRE = "Fire"
    GRASS = "Grass"
    WATER = "Water"
    GHOST = "Ghost"
    NORMAL = "Normal"         

    def __init__(self, type, other_type) -> None:
        """ 
        initialises the poketype of itself and the poketpye of the pokemon it's attacking
        :complexity: O(1) 
        """
        self.type = type
        self.other_type = other_type

    def multiplier(self):
        """
        Description:
        "mulitplier" is a method of the class PokeType which returns a numerical multipler value that is multiplied with 
        the attack_damage of an attacking pokemon to get the attacking pokemon's effective attack.

        Complexity: O(k), where k is the cost of comparison for strings

        Arguments:
        Takes no arguments

        Returns:
        Returns the attack multiplier (due to attack v. defending pokemon types) for the attacking pokemon as a numerical value.
        """
        if self.type == 'Fire':
            if self.other_type == "Fire" or self.other_type == "Ghost" or self.other_type == "Normal":
                multiplier = 1
                return multiplier 
            if self.other_type == "Grass":
                multiplier = 2
                return multiplier 
            if self.other_type == "Water":
                multiplier = 0.5
                return multiplier 

        
        if self.type == 'Grass':
            if self.other_type == "Grass" or self.other_type == "Ghost" or self.other_type == "Normal":
                multiplier = 1
                return multiplier 
            if self.other_type == "Water":
                multiplier = 2
                return multiplier 
            if self.other_type == "Fire":
                multiplier = 0.5
                return multiplier 

        
        if self.type == 'Water':
            if self.other_type == "Water" or self.other_type == "Ghost" or self.other_type == "Normal":
                multiplier = 1
                return multiplier 
            if self.other_type == "Fire":
                multiplier = 2
                return multiplier 
            if self.other_type == "Grass":
                multiplier = 0.5
                return multiplier 


        if self.type == 'Ghost':
            if self.other_type == "Water" or self.other_type == "Fire" or self.other_type == "Grass":
                multiplier = 1.25
                return multiplier 
            if self.other_type == "Ghost":
                multiplier = 2
                return multiplier 
            if self.other_type == "Normal":
                multiplier = 0
                return multiplier 


        if self.type == 'Normal':
            if self.other_type == "Water" or self.other_type == "Grass" or self.other_type == "Fire":
                multiplier = 1.25
                return multiplier 
            if self.other_type == "Normal":
                multiplier = 1
                return multiplier 
            if self.other_type == "Ghost":
                multiplier = 0
                return multiplier 


