"""
Creates 10 Pokemon classes where each individual Pokemon has its own unique stats
"""
__author__ = "Scaffold by Jackson Goerner, Code by ______________"

from random_gen import RandomGen
from abc import ABC
from pokemon_base import PokemonBase, PokeType
from math import floor, ceil

class Charizard(PokemonBase):
    def __init__(self):
        """ 
        Initialises a Charizard object where it has its own individual attributes. Inherits from PokemonBase as it is a Pokemon
        and therefore has attributes that are common across all Pokemon
        :complexity: best case and worst case of O(1) 
        """
        self.name = "Charizard"
        self.poke_type = "Fire"
        self.level = 3   
        self.hp = 12 + 1 * self.level #max evolved hp - (max prev hp - current prev hp)
        PokemonBase.__init__(self, self.hp, self.poke_type)
        self.attack_power = 10 + 2 * self.level #NOTe: I need to access charmanders current hp stat while in the Charizard class 
        self.speed = 9 + 1 * self.level
        self.defence = 4
        self.status_effect = None
    
    def level_up(self) -> None:
        """
        Description:
        "level_up" is a method of the class Charizard. It increases the level of the pokemon. Upon levelling, it takes into 
        consideration the amount of HP lost previously before levelling and subracts it from the max hp of the new pokemon.

        Complexity: best case and worst case of O(1+k) = O(k), where k is the cost of comparison 

        Arguments: 
        Takes no argument.

        Returns:
        Does not return anything.
        """
        lost_hp = (12 + 1 * self.level) - self.hp
        self.level += 1
        self.hp = (12 + 1 * self.level) - lost_hp
        self.attack_power = 10 + 2 * self.level
        if self.status_effect == "Paralysis":
            self.speed = (9 + 1 * self.level)//2
        else:
            self.speed = (9 + 1 * self.level)



    def heal(self) -> None:
        """
        Description:
        "heal" is a method of the class Charizard. It restores the max HP of the pokemon and removes any status effects that it may have. 

        Complexity: best case and worst case of O(1)

        Arguments: 
        Takes no argument.

        Returns:
        Does not return anything.
        """
        self.hp = 12 + 1 * self.level
        self.status_effect = None
        self.speed = (9 + 1 * self.level)

    def defend(self, damage: int) -> None:
        """
        Description:
        "defend" is a method of the class Charizard. It determines how much damage the pokemon should take. If the damage is greater than 
        defence, it will take twice the damage else it will lose the same amount of HP as the damage dealt. 

        Complexity: O(1)

        Arguments: 
        damage: the amount of damage the enemy pokemon is inflicting 

        Returns:
        Does not return anything.
        """
        if damage > self.defence:
            self.lose_hp(2*damage)
        else:
            self.lose_hp(damage)

    def should_evolve(self) -> bool:
        """
        Description:
        "should_evolve" is a method of the class Charizard. It determines if the pokemon should evolve. In the case of Charizard, it has
        already evolved previously and therefore can no longer evolve.

        Complexity: best case and worst case of O(1)

        Arguments: 
        None

        Returns:
        False: Charizard can no longer evolve
        """
        return False

    def get_evolved_version(self) -> PokemonBase:
        """
        Description:
        "get_evolved_version" is a method of the class Charizard. It gets the evolved version of the pokemon. But Charizard can no longer evolve.

        Complexity: best case and worst case of O(1)

        Arguments: 
        None

        Returns:
        None: Returns none as there is no polemon Charizard can evolve into
        """
        return None

    def attack(self, other: PokemonBase) -> None:
        """
        Description:
        "attack" is a method of the class Charizard. It simulates Charizard attacking another enemy pokemon, taking into consideration: status effects, 
        effective attack multiplers, lost hp.

        Complexity: best case and worst case of O(k), where k is the cost of comparison

        Arguments:
        other: the defending pokemon
        
        Returns:
        No return value.
        """
        # Step 1: Status effects on attack damage / redirecting attacks
            #Check three conditions:
            # - Sleep: FAILS - stop attack 
            # - Confusion: Chance to attack yourself 50% 
            # - Burn: Halves effective attack (To be calculated AFTER effective attack is calculated, have a multiplier for now)
        if self.status_effect == "Sleep":
            return #If its alseep, it will not attack (dont need step 2 - 3), it will not lose hp to status effects (step 4) and it will not attack, therefore cannot apply status effects (step 5)

        if self.status_effect == "Confusion":
            if RandomGen.random_chance(0.5) == True: 
                other = self #Set other (defending pokemon) equal to self (attacking pokemon). This simulates the pokemon attacking itself.
            

        burn_effective_attack_multiplier = 1 #If the pokemon isn't "Burn", multiplying by 1 will not change the "effective attack" value
        if self.status_effect == "Burn":
            burn_effective_attack_multiplier = 0.5 
            

        # Step 2: Do the attack calculation taking into "attack v defender type" multipliers (effective attack)
            #NOTe: Need to calculate the effective attack depending on the defences of the "other" pokemon
            #NOTe: Account for the burn 50% less effective attack 
            #NOTe: Account for the 50% chance to attack yourself from confusion (already accounted for)
        attack_multiplier = PokeType(self.poke_type, other.poke_type)
        type_multiplier = attack_multiplier.multiplier()
        attack_damage = self.get_attack_damage()
        effective_attack = (burn_effective_attack_multiplier)*(attack_damage)*(type_multiplier) #Multiplier depending on attacking and defending pokemon



        # Step 3: Losing hp to 'effective attack - any defence multiplers/constants"
        other.defend(effective_attack) #"other.defend" calculates how much hp is loss and changes the values of "other.hp"


        # Step 4: Losing hp to status effects
        #Check 2 conditions (only two status effects make you lose hp):      
        if self.status_effect == "Burn": # - Burn: Lose 1 hp
            self.lose_hp(1)

        if self.status_effect == "Poison": # - Poison: After SUCCCESSFUL attack, lose 3 hp
            self.lose_hp(3) 


        # Step 5: Possibly applying status effects
        if RandomGen.random_chance(0.2): # 20% chance to see if the pokemon gets hit with a status effect
            if self.poke_type == "Fire": 
                other.status_effect = "Burn"
            if self.poke_type == "Grass":
                other.status_effect = "Poison"
            if self.poke_type == "Water":
                other.status_effect = "Paralysis"
                other.speed = other.speed//2
            if self.poke_type == "Ghost":
                other.status_effect = "Sleep"
            if self.poke_type == "Normal":
                other.status_effect = "Confusion"

        return #No return value as other.defend already changes the hp


class Charmander(PokemonBase):
    """ 
    Initialises a Charmander object where it has its own individual attributes. Inherits from PokemonBase as it is a Pokemon
    and therefore has attributes that are common across all Pokemon
    :complexity: best case and worst case of O(1) 
    """
    def __init__(self):
        self.name = 'Charmander'
        self.level = 1
        self.hp = 8 + 1 * self.level
        self.poke_type = 'Fire'
        PokemonBase.__init__(self, self.hp, self.poke_type)
        self.attack_power = 6 + 1 * self.level
        self.speed = 7 + 1 * self.level
        self.defence = 4
        self.status_effect = None
        self.evolve_to = 'Charizard'
    
    def level_up(self) -> None:
        """
        Description:
        "level_up" is a method of the class Charmander. It increases the level of the pokemon. Upon levelling, it takes into 
        consideration the amount of HP lost previously before levelling and subracts it from the max hp of the new pokemon.

        Complexity: best case and worst case of O(k), where k is the cost of comparison 

        Arguments: 
        Takes no arguement.

        Returns:
        Does not return anything.
        """
        lost_hp = (8 + 1 * self.level) - self.hp
        self.level += 1
        self.hp = (8 + 1 * self.level) - lost_hp
        self.attack_power = 6 + 1 * self.level
        if self.status_effect == "Paralysis":
            self.speed = (7 + 1 * self.level)//2
        else:
            self.speed = 7 + 1 * self.level

    def heal(self) -> None:
        """
        Description:
        "heal" is a metod of the class Charmander. It restores the max HP of the pokemon and removes any status effects that it may have. 

        Complexity: best case and worst case of O(1)

        Arguments: 
        Takes no arguement.

        Returns:
        Does not return anything.
        """
        self.hp = 8 + 1 * self.level
        self.status_effect = None
        self.speed = 7 + 1 * self.level

    def defend(self, damage: int) -> None:
        """
        Description:
        "defend" is a method of the class Charmander. It determines how much damage the pokemon should take from an attack. If the effective attack damage is greater than 
        defence, Charmander takes damage equal to the attacks damage. Otherwise, Charmander loses hp equal to half of the attack (//2). 

        Complexity: best case and worst case of O(1)

        Arguments: 
        damage: the amount of damage the enemy pokemon is inflicting 

        Returns:
        Does not return anything.
        """
        if damage > self.defence:
            self.lose_hp(damage)
        else:
            self.lose_hp(damage//2)

    def should_evolve(self) -> bool:
        """
        Description:
        "should_evolve" is a method of the class Charmander. It determines if the pokemon should evolve. In the case of Charmander, it will evolve into Charizard.

        Complexity: best case and worst case of O(1)

        Arguments: 
        None

        Returns:
        Returns a boolean TRUE if Charmander is of level to evolve (lv 3) and a boolean FALSE if Charmander is not ready to evolve (not lv 3).
        """
        return self.level >= 3#: #Evolve at lv 3 (Charizard - not handled here)

    
    def get_evolved_version(self) -> PokemonBase:
        """
        Description:
        "get_evolved_version" is a method of the class Charmander. It retrieves the Pokemoon that Charmander is about to evolve into and returns it

        Complexity: best case and worst case of O(1)

        Arguments: 
        None

        Returns:
        Returns Charizard
        """

        lost_hp = (8 + 1 * self.level) - self.hp
        evolved_poke = Charizard()
        evolved_poke.lose_hp(lost_hp)
        return evolved_poke

    def attack(self, other: PokemonBase) -> None:
        """
        Description:
        "attack" is a method of the class Charmander. It simulates Charmander attacking another enemy pokemon, taking into consideration: status effects, 
        effective attack multiplers, lost hp.

        Complexity: best case and worst case of O(k), where k is the cost of comparison 

        Arguments:
        other: the defending pokemon
        
        Returns:
        No return value.
        """
        # Step 1: Status effects on attack damage / redirecting attacks
            #Check three conditions:
            # - Sleep: FAILS - stop attack 
            # - Confusion: Chance to attack yourself 50% 
            # - Burn: Halves effective attack (To be calculated AFTER effective attack is calculated, have a multiplier for now)
        if self.status_effect == "Sleep":
            return #If its alseep, it will not attack (dont need step 2 - 3), it will not lose hp to status effects (step 4) and it will not attack, therefore cannot apply status effects (step 5)

        if self.status_effect == "Confusion":
            if RandomGen.random_chance(0.5) == True: 
                other = self #Set other (defending pokemon) equal to self (attacking pokemon). This simulates the pokemon attacking itself.
            

        burn_effective_attack_multiplier = 1 #If the pokemon isn't "Burn", multiplying by 1 will not change the "effective attack" value
        if self.status_effect == "Burn":
            burn_effective_attack_multiplier = 0.5 
            

        # Step 2: Do the attack calculation taking into "attack v defender type" multipliers (effective attack)
            #NOTe: Need to calculate the effective attack depending on the defences of the "other" pokemon
            #NOTe: Account for the burn 50% less effective attack 
            #NOTe: Account for the 50% chance to attack yourself from confusion (already accounted for)
        attack_multiplier = PokeType(self.poke_type, other.poke_type) 
        type_multiplier = attack_multiplier.multiplier()
        attack_damage = self.get_attack_damage()
        effective_attack = (burn_effective_attack_multiplier)*(attack_damage)*(type_multiplier) #Multiplier depending on attacking and defending pokemon



        # Step 3: Losing hp to 'effective attack - any defence multiplers/constants"
        other.defend(effective_attack) #"other.defend" calculates how much hp is loss and changes the values of "other.hp"


        # Step 4: Losing hp to status effects
        #Check 2 conditions (only two status effects make you lose hp):      
        if self.status_effect == "Burn": # - Burn: Lose 1 hp
            self.lose_hp(1)

        if self.status_effect == "Poison": # - Poison: After SUCCCESSFUL attack, lose 3 hp
            self.lose_hp(3) 


        # Step 5: Possibly applying status effects
        if RandomGen.random_chance(0.2): # 20% chance to see if the pokemon gets hit with a status effect
            if self.poke_type == "Fire": 
                other.status_effect = "Burn"
            if self.poke_type == "Grass":
                other.status_effect = "Poison"
            if self.poke_type == "Water":
                other.status_effect = "Paralysis"
                other.speed = other.speed//2
            if self.poke_type == "Ghost":
                other.status_effect = "Sleep"
            if self.poke_type == "Normal":
                other.status_effect = "Confusion"

        return #No return value as other.defend already changes the hp


class Venusaur(PokemonBase):
    def __init__(self):
        """ 
        Initialises a Venusaur object where it has its own individual attributes. Inherits from PokemonBase as it is a Pokemon
        and therefore has attributes that are common across all Pokemon
        :complexity: best case and worst case of O(1) 
        """
        self.name = "Venusaur"
        self.poke_type = "Grass"
        self.level = 2
        self.hp = 20 + (self.level//2)
        PokemonBase.__init__(self, self.hp, self.poke_type)
        self.attack_power = 5
        self.speed = 3 + (self.level//2)
        self.defence = 10
        self.status_effect = None
        
    def level_up(self) -> None:
        """
        Description:
        "level_up" is a method of the class Venusaur. It increases the level of the pokemon. Upon levelling, it takes into 
        consideration the amount of HP lost previously before levelling and subracts it from the max hp of the new pokemon.

        Complexity: best case and worst case of O(k), where k is the cost of comparison

        Arguments: 
        Takes no argument.

        Returns:
        Does not return anything.
        """
        lost_hp = (20 + (self.level//2)) - self.hp
        self.level += 1
        self.hp = (20 + (self.level//2)) - lost_hp
        if self.status_effect == "Paralysis":
            self.speed = (3 + (self.level//2))//2
        else:
            self.speed = 3 + (self.level//2)

    def heal(self) -> None:
        """
        Description:
        "heal" is a method of the class Venusaur. It restores the max HP of the pokemon and removes any status effects that it may have. 

        Complexity: best case and worst case of O(1)

        Arguments: 
        Takes no argument.

        Returns:
        Does not return anything.
        """
        self.hp = 20 + (self.level//2)
        self.status_effect = None
        self.speed = 3 + (self.level//2)

    def defend(self, damage: int) -> None:
        """
        Description:
        "defend" is a method of the class Venusaur. It determines how much damage the pokemon should take. If the effective attack damage is greater than the
        defence, Venusaur takes damage equal to the attack. Otherwise, Venusaur loses hp equal to half the attack (//2).

        Complexitity: best case and worst case of O(1)

        Arguments: 
        damage: the amount of damage the enemy pokemon is inflicting 

        Returns:
        Does not return anything.
        """
        if damage > (self.defence + 5):
            self.lose_hp(damage)
        else:
            self.lose_hp(damage//2)

    def should_evolve(self) -> bool:
        """
        Description:
        "should_evolve" is a method of the class Venusaur. It determines if the pokemon should evolve. In the case of Venusaur, it has
        already evolved previously and therefore can no longer evolve.

        Complexitity: best case and worst case of O(1)

        Arguments: 
        None

        Returns:
        False: Venusaur can no longer evolve
        """
        return False

    def get_evolved_version(self) -> PokemonBase:
        """
        Description:
        "get_evolved_version" is a method of the class Venusaur. It gets the evolved version of the pokemon. But Venusaur can no longer evolve.

        Complexitity: best case and worst case of O(1)

        Arguments: 
        None

        Returns:
        None: Returns none as there is no pokemon Venusaur can evolve into.
        """
        return None
    
    def attack(self, other: PokemonBase) -> None:
        """
        Description:
        "attack" is a method of the class Venusaur. It simulates Venusaur attacking another enemy pokemon, taking into consideration: status effects, 
        effective attack multiplers, lost hp.

        Complexitity: best case and worst case of O(k), where k is the cost of comparison 

        Arguments:
        other: the defending pokemon
        
        Returns:
        No return value.
        """
        # Step 1: Status effects on attack damage / redirecting attacks
            #Check three conditions:
            # - Sleep: FAILS - stop attack 
            # - Confusion: Chance to attack yourself 50% 
            # - Burn: Halves effective attack (To be calculated AFTER effective attack is calculated, have a multiplier for now)
        if self.status_effect == "Sleep":
            return #If its alseep, it will not attack (dont need step 2 - 3), it will not lose hp to status effects (step 4) and it will not attack, therefore cannot apply status effects (step 5)

        if self.status_effect == "Confusion":
            if RandomGen.random_chance(0.5) == True: 
                other = self #Set other (defending pokemon) equal to self (attacking pokemon). This simulates the pokemon attacking itself.
            

        burn_effective_attack_multiplier = 1 #If the pokemon isn't "Burn", multiplying by 1 will not change the "effective attack" value
        if self.status_effect == "Burn":
            burn_effective_attack_multiplier = 0.5 
            

        # Step 2: Do the attack calculation taking into "attack v defender type" multipliers (effective attack)
            #NOTe: Need to calculate the effective attack depending on the defences of the "other" pokemon
            #NOTe: Account for the burn 50% less effective attack 
            #NOTe: Account for the 50% chance to attack yourself from confusion (already accounted for)
        attack_multiplier = PokeType(self.poke_type, other.poke_type)
        type_multiplier = attack_multiplier.multiplier()
        attack_damage = self.get_attack_damage()
        effective_attack = (burn_effective_attack_multiplier)*(attack_damage)*(type_multiplier) #Trying to get: Multiplier depending on attacking and defending pokemon
        


        # Step 3: Losing hp to 'effective attack - any defence multiplers/constants"
        other.defend(effective_attack) #"other.defend" calculates how much hp is loss and changes the values of "other.hp"


        # Step 4: Losing hp to status effects
        #Check 2 conditions (only two status effects make you lose hp):      
        if self.status_effect == "Burn": # - Burn: Lose 1 hp
            self.lose_hp(1)

        if self.status_effect == "Poison": # - Poison: After SUCCCESSFUL attack, lose 3 hp
            self.lose_hp(3) 


        # Step 5: Possibly applying status effects
        if RandomGen.random_chance(0.2): # 20% chance to see if the pokemon gets hit with a status effect
            if self.poke_type == "Fire": 
                other.status_effect = "Burn"
            if self.poke_type == "Grass":
                other.status_effect = "Poison"
            if self.poke_type == "Water":
                other.status_effect = "Paralysis"
                other.speed = other.speed//2
            if self.poke_type == "Ghost":
                other.status_effect = "Sleep"
            if self.poke_type == "Normal":
                other.status_effect = "Confusion"

        return #No return value as other.defend already changes the hp

class Bulbasaur(PokemonBase):
    def __init__(self):
        """ 
        Initialises a Bulbasaur object where it has its own individual attributes. Inherits from PokemonBase as it is a Pokemon
        and therefore has attributes that are common across all Pokemon
        :complexity: best case and worst case of O(1) 
        """
        self.name = "Bulbasaur"
        self.poke_type = "Grass"
        self.level = 1
        self.hp = 12 + 1 * self.level
        PokemonBase.__init__(self, self.hp, self.poke_type)
        self.attack_power = 5
        self.speed = 7 + (self.level//2)
        self.defence = 5
        self.status_effect = None
        self.evolve_to = 'Venusaur' 
    
    def level_up(self) -> None:
        """
        Description:
        "level_up" is a method of the class Bulbasaur. It increases the level of the pokemon. Upon levelling, it takes into 
        consideration the amount of HP lost previously before levelling and subracts it from the max hp of the new pokemon.

        Complexity: best case and worst case of O(k), where k is the cost of comparison 

        Arguments: 
        Takes no arguement.

        Returns:
        Does not return anything.
        """
        lost_hp = (12 + 1 * self.level) - self.hp
        self.level += 1
        self.hp = (12 + 1 * self.level) - lost_hp
        if self.status_effect == "Paralysis":
            self.speed = (7 + (self.level//2))//2
        else:
            self.speed = 7 + (self.level//2)

    def heal(self) -> None:
        """
        Description:
        "heal" is a method of the class Bulbasaur. It restores the max HP of the pokemon and removes any status effects that it may have. 

        Complexity: best case and worst case of O(1)

        Arguments: 
        Takes no arguement.

        Returns:
        Does not return anything.
        """
        self.hp = 12 + 1 * self.level
        self.status_effect = None
        self.speed = 7 + (self.level//2)

    def defend(self, damage: int) -> None:
        """
        Description:
        "defend" is a method of the class Bulbasaur. It determines how much damage the pokemon should take. If the damage is greater than 
        defence, it will lose hp equal to the damage. Otherwise, Bulbasaur only loses hp equal to half of the damage (//2).

        Complexity: best case and worst case of O(1)

        Arguments: 
        damage: the amount of damage the enemy pokemon is inflicting 

        Returns:
        Does not return anything.
        """
        if damage > (self.defence + 5):
            self.lose_hp(damage)
        else:
            self.lose_hp(damage//2)

    def should_evolve(self) -> bool:
        """
        Description:
        "should_evolve" is a method of the class Bulbasaur. It determines if the pokemon should evolve. In the case of Bulbsaur, it can evolve at lv 2.

        Complexity: best case and worst case of O(1)

        Arguments: 
        None

        Returns:
        Returns a boolean FALSE if Bulbasaur's level isn't 2, which means it is not ready to evolve. Otherwise, if it is lv 2, it will return a boolean TRUE.
        """
        return self.level >= 2


    def get_evolved_version(self) -> PokemonBase:
        """
        Description:
        "get_evolved_version" is a method of the class Bulbasaur. It gets the evolved version of the pokemon. Bulbasaur evolves into Venusaur.

        Complexity: best case and worst case of O(1)

        Arguments: 
        None

        Returns:
        Returns Venusaur and intialises Venusaur's hp, taking into account the amount of damage Bulbasaur has already taken.
        """
        lost_hp = (12 + 1 * self.level) - self.hp
        evolved_poke = Venusaur()
        evolved_poke.lose_hp(lost_hp)
        return evolved_poke

    def attack(self, other: PokemonBase) -> None:
        """
        Description:
        "attack" is a method of the class Bulbasaur. It simulates Bulbasaur attacking another enemy pokemon, taking into consideration: status effects, 
        effective attack multiplers, lost hp.

        Complexity: best case and worst case of O(k), where k is the cost of comparison 

        Arguments:
        other: the defending pokemon
        
        Returns:
        No return value.
        """
        # Step 1: Status effects on attack damage / redirecting attacks
            #Check three conditions:
            # - Sleep: FAILS - stop attack 
            # - Confusion: Chance to attack yourself 50% 
            # - Burn: Halves effective attack (To be calculated AFTER effective attack is calculated, have a multiplier for now)
        if self.status_effect == "Sleep":
            return #If its alseep, it will not attack (dont need step 2 - 3), it will not lose hp to status effects (step 4) and it will not attack, therefore cannot apply status effects (step 5)

        if self.status_effect == "Confusion":
            if RandomGen.random_chance(0.5) == True: 
                other = self #Set other (defending pokemon) equal to self (attacking pokemon). This simulates the pokemon attacking itself.
            

        burn_effective_attack_multiplier = 1 #If the pokemon isn't "Burn", multiplying by 1 will not change the "effective attack" value
        if self.status_effect == "Burn":
            burn_effective_attack_multiplier = 0.5 
            

        # Step 2: Do the attack calculation taking into "attack v defender type" multipliers (effective attack)
            #NOTe: Need to calculate the effective attack depending on the defences of the "other" pokemon
            #NOTe: Account for the burn 50% less effective attack 
            #NOTe: Account for the 50% chance to attack yourself from confusion (already accounted for)
        attack_multiplier = PokeType(self.poke_type, other.poke_type) 
        type_multiplier = attack_multiplier.multiplier()
        attack_damage = self.get_attack_damage()
        effective_attack = (burn_effective_attack_multiplier)*(attack_damage)*(type_multiplier) #Trying to get: Multiplier depending on attacking and defending pokemon



        # Step 3: Losing hp to 'effective attack - any defence multiplers/constants"
        other.defend(effective_attack) #"other.defend" calculates how much hp is loss and changes the values of "other.hp"


        # Step 4: Losing hp to status effects
        #Check 2 conditions (only two status effects make you lose hp):      
        if self.status_effect == "Burn": # - Burn: Lose 1 hp
            self.lose_hp(1)

        if self.status_effect == "Poison": # - Poison: After SUCCCESSFUL attack, lose 3 hp
            self.lose_hp(3) 


        # Step 5: Possibly applying status effects
        if RandomGen.random_chance(0.2): # 20% chance to see if the pokemon gets hit with a status effect
            if self.poke_type == "Fire": 
                other.status_effect = "Burn"
            if self.poke_type == "Grass":
                other.status_effect = "Poison"
            if self.poke_type == "Water":
                other.status_effect = "Paralysis"
                other.speed = other.speed//2
            if self.poke_type == "Ghost":
                other.status_effect = "Sleep"
            if self.poke_type == "Normal":
                other.status_effect = "Confusion"

        return #No return value as other.defend already changes the hp


class Blastoise(PokemonBase):
    def __init__(self):
        """ 
        Initialises a Blastoise object where it has its own individual attributes. Inherits from PokemonBase as it is a Pokemon
        and therefore has attributes that are common across all Pokemon
        :complexity: best case and worst case of O(1) 
        """
        self.name = "Blastoise"
        self.level = 3
        self.hp = 15 + 2*self.level 
        self.poke_type = "Water"
        PokemonBase.__init__(self, self.hp, self.poke_type)
        self.attack_power = 8 + (self.level//2)
        self.speed = 10 
        self.defence = 8 + 1*self.level 
        self.status_effect = None
        
    def level_up(self) -> None:
        """
        Description:
        "level_up" is a method of the class Blastoise. It increases the level of the pokemon. Upon levelling, it takes into 
        consideration the amount of HP lost previously before levelling and subracts it from the max hp of the new pokemon.

        Complexity: best case and worst case of O(1)

        Arguments: 
        Takes no arguement.

        Returns:
        Does not return anything.
        """
        lost_hp = (15 + 2*self.level ) - self.hp
        self.level += 1
        self.hp = (15 + 2*self.level) - lost_hp
        self.attack_power = 8 + (self.level//2)
        self.defence = 8 + 1*self.level
        

    def heal(self) -> None:
        """
        Description:
        "heal" is a method of the class Blastoise. It restores the max HP of the pokemon and removes any status effects that it may have. 

        Complexity: best case and worst case of O(1)

        Arguments: 
        Takes no argument.

        Returns:
        Does not return anything.
        """
        self.hp = 15 + 2*self.level 
        self.status_effect = None

    def defend(self, damage: int) -> None:
        """
        Description:
        "defend" is a method of the class Blastoise. It determines how much damage the pokemon should take. If the effective attack damage is greater than 
        double Blastoise's defence, Blastoise loses HP equal to the effective attack. Otherwise, it loses HP equal to half of the effective attack (//2).

        Complexity: best case and worst case of O(1)

        Arguments: 
        damage: the amount of damage the enemy pokemon is inflicting 

        Returns:
        Does not return anything.
        """
        if damage > (self.defence * 2):
            self.lose_hp(damage)
        else:
            self.lose_hp(damage//2)

    def should_evolve(self) -> bool:
        """
        Description:
        "should_evolve" is a method of the class Blastoise. It determines if the pokemon should evolve. Blastoise is the final evolved pokemon and will not evolve.

        Complexity: best case and worst case of O(1)

        Arguments: 
        None

        Returns:
        False: Blastoise can no longer evolve.
        """
        return False

    def get_evolved_version(self) -> PokemonBase:
        """
        Description:
        "get_evolved_version" is a method of the class Blatoise. It gets the evolved version of the pokemon. But Blastoise can no longer evolve.

        Complexity: best case and worst case of O(1)

        Arguments: 
        None

        Returns:
        None: Returns none as there is no pokemon Blastoise can evolve into
        """
        return None

    def attack(self, other: PokemonBase) -> None:
        """
        Description:
        "attack" is a method of the class Blastoise. It simulates Blastoise attacking another enemy pokemon, taking into consideration: status effects, 
        effective attack multiplers, lost hp.

        Complexity: best case and worst case of O(k)

        Arguments:
        other: the defending pokemon
        
        Returns:
        No return value.
        """
        # Step 1: Status effects on attack damage / redirecting attacks
            #Check three conditions:
            # - Sleep: FAILS - stop attack 
            # - Confusion: Chance to attack yourself 50% 
            # - Burn: Halves effective attack (To be calculated AFTER effective attack is calculated, have a multiplier for now)
        if self.status_effect == "Sleep":
            return #If its alseep, it will not attack (dont need step 2 - 3), it will not lose hp to status effects (step 4) and it will not attack, therefore cannot apply status effects (step 5)

        if self.status_effect == "Confusion":
            if RandomGen.random_chance(0.5) == True: 
                other = self #Set other (defending pokemon) equal to self (attacking pokemon). This simulates the pokemon attacking itself.
            

        burn_effective_attack_multiplier = 1 #If the pokemon isn't "Burn", multiplying by 1 will not change the "effective attack" value
        if self.status_effect == "Burn":
            burn_effective_attack_multiplier = 0.5 
            

        # Step 2: Do the attack calculation taking into "attack v defender type" multipliers (effective attack)
            #NOTe: Need to calculate the effective attack depending on the defences of the "other" pokemon
            #NOTe: Account for the burn 50% less effective attack 
            #NOTe: Account for the 50% chance to attack yourself from confusion (already accounted for)
        attack_multiplier = PokeType(self.poke_type, other.poke_type) 
        type_multiplier = attack_multiplier.multiplier()
        attack_damage = self.get_attack_damage()
        effective_attack = (burn_effective_attack_multiplier)*(attack_damage)*(type_multiplier) #Multiplier depending on attacking and defending pokemon



        # Step 3: Losing hp to 'effective attack - any defence multiplers/constants"
        other.defend(effective_attack) #"other.defend" calculates how much hp is loss and changes the values of "other.hp"


        # Step 4: Losing hp to status effects
        #Check 2 conditions (only two status effects make you lose hp):      
        if self.status_effect == "Burn": # - Burn: Lose 1 hp
            self.lose_hp(1)

        if self.status_effect == "Poison": # - Poison: After SUCCCESSFUL attack, lose 3 hp
            self.lose_hp(3) 


        # Step 5: Possibly applying status effects
        if RandomGen.random_chance(0.2): # 20% chance to see if the pokemon gets hit with a status effect
            if self.poke_type == "Fire": 
                other.status_effect = "Burn"
            if self.poke_type == "Grass":
                other.status_effect = "Poison"
            if self.poke_type == "Water":
                other.status_effect = "Paralysis"
                other.speed = other.speed//2
            if self.poke_type == "Ghost":
                other.status_effect = "Sleep"
            if self.poke_type == "Normal":
                other.status_effect = "Confusion"

        return #No return value as other.defend already changes the hp
  

class Squirtle(PokemonBase):
    def __init__(self):
        """ 
        Initialises a Squirtle object where it has its own individual attributes. Inherits from PokemonBase as it is a Pokemon
        and therefore has attributes that are common across all Pokemon
        :complexity: best case and worst case of O(1) 
        """
        self.name = "Squirtle"
        self.level = 1 
        self.hp = 9 + 2*self.level
        self.poke_type = "Water"
        PokemonBase.__init__(self, self.hp, self.poke_type)
        self.attack_power = 4 + (self.level//2)
        self.speed = 7 
        self.defence = 6 + self.level
        self.status_effect = None
        self.evolve_to = 'Blastoise' 

    def level_up(self) -> None:
        """
        Description:
        "level_up" is a method of the class Squirtle. It increases the level of the pokemon. Upon levelling, it takes into 
        consideration the amount of HP lost previously before levelling and subracts it from the max hp of the new pokemon.

        Complexity: best case and worst case of O(1)

        Arguments: 
        Takes no arguement.

        Returns:
        Does not return anything.
        """
        lost_hp = (9 + 2*self.level ) - self.hp
        self.level += 1
        self.hp = (9 + 2*self.level) - lost_hp
        self.attack_power = 4 + (self.level//2)
        self.defence = 6 + self.level

    def heal(self) -> None:
        """
        Description:
        "heal" is a method of the class Squirtle. It restores the max HP of the pokemon and removes any status effects that it may have. 

        Complexity: best case and worst case of O(1)

        Arguments: 
        Takes no argument.

        Returns:
        Does not return anything.
        """
        self.hp = 9 + 2*self.level
        self.status_effect = None

    def defend(self, damage: int) -> None:
        """
        Description:
        "defend" is a method of the class Squirtle. It determines how much damage the pokemon should take. If the effective attack damage is greater than double
        of Squirtle's defence, Squirtle loses HP equal to the effective attack. Otherwise, Squirtle only loses half as much Hp as the attack (//2).

        Complexity: best case and worst case of O(1)

        Arguments: 
        damage: the amount of damage the enemy pokemon is inflicting 

        Returns:
        Does not return anything.
        """
        if damage > (self.defence * 2):
            self.lose_hp(damage)
        else:
            self.lose_hp(damage//2)

    def should_evolve(self) -> bool:
        """
        Description:
        "should_evolve" is a method of the class Squirtle. It determines if the pokemon should evolve. In the case of Squirtle, it will evolve into Blastiose.

        Complexity: best case and worst case of O(1)

        Arguments: 
        None

        Returns:
        Returns a boolean TRUE when Squirtle is at the reuqired lv 3 to evolve. Otherwise return a boolean FALSE.
        """
        return self.level >= 3#: #Evolve at lv 3 (Blastoise - not handled here)


    def get_evolved_version(self) -> PokemonBase:
        """
        Description:
        "get_evolved_version" is a method of the class Squirtle. It gets the evolved version of the pokemon. Squirtle will evolve Blastiose.

        Complexity: best case and worst case of O(1)

        Arguments: 
        None

        Returns:
        Returns the pokemon Blastoise and intialises the HP of Blastoise, taking into account the damage that Squirtle has already sustained.
        """
        lost_hp = (20 + (self.level//2)) - self.hp
        evolved_poke = Blastoise()
        evolved_poke.lose_hp(lost_hp)
        return evolved_poke

    def attack(self, other: PokemonBase) -> None:
        """
        Description:
        "attack" is a method of the class Squirtle. It simulates Squirtle attacking another enemy pokemon, taking into consideration: status effects, 
        effective attack multiplers, lost hp.

        Complexity: best case and worst case of O(k), where k is the cost of comparison

        Arguments:
        other: the defending pokemon
        
        Returns:
        No return value.
        """
        # Step 1: Status effects on attack damage / redirecting attacks
            #Check three conditions:
            # - Sleep: FAILS - stop attack 
            # - Confusion: Chance to attack yourself 50% 
            # - Burn: Halves effective attack (To be calculated AFTER effective attack is calculated, have a multiplier for now)
        if self.status_effect == "Sleep":
            return #If its alseep, it will not attack (dont need step 2 - 3), it will not lose hp to status effects (step 4) and it will not attack, therefore cannot apply status effects (step 5)

        if self.status_effect == "Confusion":
            if RandomGen.random_chance(0.5) == True: 
                other = self #Set other (defending pokemon) equal to self (attacking pokemon). This simulates the pokemon attacking itself.
            

        burn_effective_attack_multiplier = 1 #If the pokemon isn't "Burn", multiplying by 1 will not change the "effective attack" value
        if self.status_effect == "Burn":
            burn_effective_attack_multiplier = 0.5 
            

        # Step 2: Do the attack calculation taking into "attack v defender type" multipliers (effective attack)
            #NOTe: Need to calculate the effective attack depending on the defences of the "other" pokemon
            #NOTe: Account for the burn 50% less effective attack 
            #NOTe: Account for the 50% chance to attack yourself from confusion (already accounted for)
        attack_multiplier = PokeType(self.poke_type, other.poke_type) 
        type_multiplier = attack_multiplier.multiplier()
        attack_damage = self.get_attack_damage()
        effective_attack = (burn_effective_attack_multiplier)*(attack_damage)*(type_multiplier) #Trying to get: Multiplier depending on attacking and defending pokemon



        # Step 3: Losing hp to 'effective attack - any defence multiplers/constants"
        other.defend(effective_attack) #"other.defend" calculates how much hp is loss and changes the values of "other.hp"


        # Step 4: Losing hp to status effects
        #Check 2 conditions (only two status effects make you lose hp):      
        if self.status_effect == "Burn": # - Burn: Lose 1 hp
            self.lose_hp(1)

        if self.status_effect == "Poison": # - Poison: After SUCCCESSFUL attack, lose 3 hp
            self.lose_hp(3) 


        # Step 5: Possibly applying status effects
        if RandomGen.random_chance(0.2): # 20% chance to see if the pokemon gets hit with a status effect
            if self.poke_type == "Fire": 
                other.status_effect = "Burn"
            if self.poke_type == "Grass":
                other.status_effect = "Poison"
            if self.poke_type == "Water":
                other.status_effect = "Paralysis"
                other.speed = other.speed//2
            if self.poke_type == "Ghost":
                other.status_effect = "Sleep"
            if self.poke_type == "Normal":
                other.status_effect = "Confusion"

        return #No return value as other.defend already changes the hp

class Gengar(PokemonBase):
    def __init__(self):
        """ 
        Initialises a Gengar object where it has its own individual attributes. Inherits from PokemonBase as it is a Pokemon
        and therefore has attributes that are common across all Pokemon
        :complexity: best case and worst case of O(1) 
        """
        self.name = 'Gengar'
        self.level = 3
        self.hp = 12 + (self.level//2)
        self.poke_type = 'Ghost'
        PokemonBase.__init__(self, self.hp, self.poke_type)
        self.attack_power = 18
        self.speed = 12
        self.defence = 3
        self.status_effect = None
        
    def level_up(self) -> None:
        """
        Description:
        "level_up" is a method of the class Gengar. It increases the level of the pokemon. Upon levelling, it takes into 
        consideration the amount of HP lost previously before levelling and subracts it from the max hp of the new pokemon.

        Complexity: best case and worst case of O(1)

        Arguments: 
        Takes no arguement.

        Returns:
        Does not return anything.
        """
        lost_hp = (12 + (self.level//2)) - self.hp
        self.level += 1
        self.hp = 12 + (self.level//2) - lost_hp

    def heal(self) -> None:
        """
        Description:
        "heal" is a method of the class Gengar. It restores the max HP of the pokemon and removes any status effects that it may have. 

        Complexity: best case and worst case of O(1)

        Arguments: 
        Takes no argument.

        Returns:
        Does not return anything.
        """
        self.hp = 12 + (self.level//2)
        self.status_effect = None
    
    def defend(self, damage: int) -> None:
        """
        Description:
        "defend" is a method of the class Gengar. It determines how much damage the pokemon should take. Gengar loses hp equal to the effective attack.

        Complexity: best case and worst case of O(1)

        Arguments: 
        damage: the amount of damage the enemy pokemon is inflicting 

        Returns:
        Does not return anything.
        """
        self.lose_hp(damage)

    def should_evolve(self) -> bool:
        """
        Description:
        "should_evolve" is a method of the class Gengar. It determines if the pokemon should evolve. In the case of Gengar, it has
        already evolved previously and therefore can no longer evolve.

        Complexity: best case and worst case of O(1)

        Arguments: 
        None

        Returns:
        False: Gengar can no longer evolve
        """
        return False

    def get_evolved_version(self) -> PokemonBase:
        """
        Description:
        "get_evolved_version" is a method of the class Gengar. It gets the evolved version of the pokemon. But Gengar can no longer evolve.

        Complexity: best case and worst case of O(1)

        Arguments: 
        None

        Returns:
        None: Returns none as there is no pokemon Gengar can evolve into
        """
        return None

    def attack(self, other: PokemonBase) -> None:
        """
        Description:
        "attack" is a method of the class Gengar. It simulates Gengar attacking another enemy pokemon, taking into consideration: status effects, 
        effective attack multiplers, lost hp.

        Complexity: best case and worst case of O(k), where k is the cost of comparison

        Arguments:
        other: the defending pokemon
        
        Returns:
        No return value.
        """
        # Step 1: Status effects on attack damage / redirecting attacks
            #Check three conditions:
            # - Sleep: FAILS - stop attack 
            # - Confusion: Chance to attack yourself 50% 
            # - Burn: Halves effective attack (To be calculated AFTER effective attack is calculated, have a multiplier for now)
        if self.status_effect == "Sleep":
            return #If its alseep, it will not attack (dont need step 2 - 3), it will not lose hp to status effects (step 4) and it will not attack, therefore cannot apply status effects (step 5)

        if self.status_effect == "Confusion":
            if RandomGen.random_chance(0.5) == True: 
                other = self #Set other (defending pokemon) equal to self (attacking pokemon). This simulates the pokemon attacking itself.
            

        burn_effective_attack_multiplier = 1 #If the pokemon isn't "Burn", multiplying by 1 will not change the "effective attack" value
        if self.status_effect == "Burn":
            burn_effective_attack_multiplier = 0.5 
            

        # Step 2: Do the attack calculation taking into "attack v defender type" multipliers (effective attack)
            #NOTe: Need to calculate the effective attack depending on the defences of the "other" pokemon
            #NOTe: Account for the burn 50% less effective attack 
            #NOTe: Account for the 50% chance to attack yourself from confusion (already accounted for)
        attack_multiplier = PokeType(self.poke_type, other.poke_type)
        type_multiplier = attack_multiplier.multiplier()
        attack_damage = self.get_attack_damage()
        effective_attack = (burn_effective_attack_multiplier)*(attack_damage)*(type_multiplier) #Trying to get: Multiplier depending on attacking and defending pokemon



        # Step 3: Losing hp to 'effective attack - any defence multiplers/constants"
        other.defend(effective_attack) #"other.defend" calculates how much hp is loss and changes the values of "other.hp"


        # Step 4: Losing hp to status effects
        #Check 2 conditions (only two status effects make you lose hp):      
        if self.status_effect == "Burn": # - Burn: Lose 1 hp
            self.lose_hp(1)

        if self.status_effect == "Poison": # - Poison: After SUCCCESSFUL attack, lose 3 hp
            self.lose_hp(3)     


        # Step 5: Possibly applying status effects
        if RandomGen.random_chance(0.2): # 20% chance to see if the pokemon gets hit with a status effect
            if self.poke_type == "Fire": 
                other.status_effect = "Burn"
            if self.poke_type == "Grass":
                other.status_effect = "Poison"
            if self.poke_type == "Water":
                other.status_effect = "Paralysis"
                other.speed = other.speed//2
            if self.poke_type == "Ghost":
                other.status_effect = "Sleep"
            if self.poke_type == "Normal":
                other.status_effect = "Confusion"

        return #No return value as other.defend already changes the hp
    

class Haunter(PokemonBase):
    def __init__(self):
        """ 
        Initialises a Haunter object where it has its own individual attributes. Inherits from PokemonBase as it is a Pokemon
        and therefore has attributes that are common across all Pokemon
        :complexity: best case and worst case of O(1) 
        """
        self.name = 'Haunter'
        self.level = 1
        self.hp = 9 + (self.level//2)
        self.poke_type = 'Ghost'
        PokemonBase.__init__(self, self.hp, self.poke_type)
        self.attack_power = 8
        self.speed = 6
        self.defence = 6
        self.status_effect = None
        self.evolve_to = 'Gengar' 

    def level_up(self) -> None:
        """
        Description:
        "level_up" is a method of the class Haunter. It increases the level of the pokemon. Upon levelling, it takes into 
        consideration the amount of HP lost previously before levelling and subracts it from the max hp of the new pokemon.

        Complexity: best case and worst case of O(1)

        Arguments: 
        Takes no arguement.

        Returns:
        Does not return anything.
        """
        lost_hp = (9 + (self.level//2)) - self.hp
        self.level += 1
        self.hp = (9 + (self.level//2)) - lost_hp

    def heal(self) -> None:
        """
        Description:
        "heal" is a method of the class Haunter. It restores the max HP of the pokemon and removes any status effects that it may have. 

        Complexity: best case and worst case of O(1)

        Arguments: 
        Takes no argument.

        Returns:
        Does not return anything.
        """
        self.hp = 9 + (self.level//2)
        self.status_effect = None

    def defend(self, damage: int) -> None:
        """
        Description:
        "defend" is a method of the class Haunter. It determines how much damage the pokemon should take. Loses hp equal to the effective attack.

        Complexity: best case and worst case of O(1)
        
        Arguments: 
        damage: the amount of damage the enemy pokemon is inflicting 

        Returns:
        Does not return anything.
        """
        self.lose_hp(damage)

    def should_evolve(self) -> bool:
        """
        Description:
        "should_evolve" is a method of the class Haunter. It determines if the pokemon should evolve. In the case of Haunter, it has
        already evolved previously and therefore can no longer evolve.

        Complexity: best case and worst case of O(1)

        Arguments: 
        None

        Returns:
        False: Haunter can no longer evolve
        """
        return self.level == 3

    
    def get_evolved_version(self) -> PokemonBase:
        """
        Description:
        "get_evolved_version" is a method of the class Haunter. It gets the evolved version of the pokemon. Haunter evolves into Gengar.

        Complexity: best case and worst case of O(1)

        Arguments: 
        None

        Returns:
        Always returns Gengar as Haunter evolves at the base lv 1. Also intilsiaes Gengar's hp by taking into account how much damage Haunter has previously taken.
        """
        lost_hp = (9 + (self.level//2)) - self.hp
        evolved_poke = Gengar()
        evolved_poke.lose_hp(lost_hp)
        return evolved_poke

    def attack(self, other: PokemonBase) -> None:
        """
        Description:
        "attack" is a method of the class Haunter. It simulates Haunter attacking another enemy pokemon, taking into consideration: status effects, 
        effective attack multiplers, lost hp.

        Complexity: best case and worst case of O(k), where k is the cost of comparison

        Arguments:
        other: the defending pokemon
        
        Returns:
        No return value.
        """
        # Step 1: Status effects on attack damage / redirecting attacks
            #Check three conditions:
            # - Sleep: FAILS - stop attack 
            # - Confusion: Chance to attack yourself 50% 
            # - Burn: Halves effective attack (To be calculated AFTER effective attack is calculated, have a multiplier for now)
        if self.status_effect == "Sleep":
            return #If its alseep, it will not attack (dont need step 2 - 3), it will not lose hp to status effects (step 4) and it will not attack, therefore cannot apply status effects (step 5)

        if self.status_effect == "Confusion":
            if RandomGen.random_chance(0.5) == True: 
                other = self #Set other (defending pokemon) equal to self (attacking pokemon). This simulates the pokemon attacking itself.
            

        burn_effective_attack_multiplier = 1 #If the pokemon isn't "Burn", multiplying by 1 will not change the "effective attack" value
        if self.status_effect == "Burn":
            burn_effective_attack_multiplier = 0.5 
            

        # Step 2: Do the attack calculation taking into "attack v defender type" multipliers (effective attack)
            #NOTe: Need to calculate the effective attack depending on the defences of the "other" pokemon
            #NOTe: Account for the burn 50% less effective attack 
            #NOTe: Account for the 50% chance to attack yourself from confusion (already accounted for)
        attack_multiplier = PokeType(self.poke_type, other.poke_type) 
        type_multiplier = attack_multiplier.multiplier()
        attack_damage = self.get_attack_damage()
        effective_attack = (burn_effective_attack_multiplier)*(attack_damage)*(type_multiplier) #Trying to get: Multiplier depending on attacking and defending pokemon



        # Step 3: Losing hp to 'effective attack - any defence multiplers/constants"
        other.defend(effective_attack) #"other.defend" calculates how much hp is loss and changes the values of "other.hp"


        # Step 4: Losing hp to status effects
        #Check 2 conditions (only two status effects make you lose hp):      
        if self.status_effect == "Burn": # - Burn: Lose 1 hp
            self.lose_hp(1)

        if self.status_effect == "Poison": # - Poison: After SUCCCESSFUL attack, lose 3 hp
            self.lose_hp(3)


        # Step 5: Possibly applying status effects
        if RandomGen.random_chance(0.2): # 20% chance to see if the pokemon gets hit with a status effect
            if self.poke_type == "Fire": 
                other.status_effect = "Burn"
            if self.poke_type == "Grass":
                other.status_effect = "Poison"
            if self.poke_type == "Water":
                other.status_effect = "Paralysis"
                other.speed = other.speed//2
            if self.poke_type == "Ghost":
                other.status_effect = "Sleep"
            if self.poke_type == "Normal":
                other.status_effect = "Confusion"

        return #No return value as other.defend already changes the hp
    

class Gastly(PokemonBase):
    def __init__(self):
        """ 
        Initialises a Gastly object where it has its own individual attributes. Inherits from PokemonBase as it is a Pokemon
        and therefore has attributes that are common across all Pokemon
        :complexity: best case and worst case of O(1) 
        """
        self.name = "Gastly"
        self.level = 1
        self.hp = 6+(self.level//2)
        self.poke_type = "Ghost"
        PokemonBase.__init__(self, self.hp, self.poke_type)
        self.attack_power = 4
        self.speed = 2 
        self.defence = 8 
        self.status_effect = None
        self.evolve_to = 'Haunter' 

    def level_up(self) -> None:
        """
        Description:
        "level_up" is a method of the class Gastly. It increases the level of the pokemon. Upon levelling, it takes into 
        consideration the amount of HP lost previously before levelling and subracts it from the max hp of the new pokemon.

        Complexity: best case and worst case of O(1)

        Arguments: 
        Takes no arguement.

        Returns:
        Does not return anything.
        """
        lost_hp = (6 + (self.level//2)) - self.hp
        self.level += 1
        self.hp = (6+(self.level//2)) - lost_hp

    def heal(self):
        """
        Description:
        "heal" is a method of the class Gastly. It restores the max HP of the pokemon and removes any status effects that it may have. 

        Complexity: best case and worst case of O(1)

        Arguments: 
        Takes no argument.

        Returns:
        Does not return anything.
        """
        self.hp = 6+(self.level//2)
        self.status_effect = None

    def defend(self, damage: int) -> None:
        """
        Description:
        "defend" is a method of the class Gastly. It determines how much damage the pokemon should take. Loses hp equal to the effective attack.

        Complexity: best case and worst case of O(1)

        Arguments: 
        damage: the amount of damage the enemy pokemon is inflicting 

        Returns:
        Does not return anything.
        """
        self.lose_hp(damage)

    def should_evolve(self) -> bool:
        """
        Description:
        "should_evolve" is a method of the class Gastly. It determines if the pokemon should evolve. In the case of Gastly, it has
        already evolved previously and therefore can no longer evolve.

        Complexity: best case and worst case of O(1)

        Arguments: 
        None

        Returns:
        False: Gastly can no longer evolve
        """
        return self.level >= 1 #: #Evolve at lv 1 (Haunter - not handled here)
        #     return True 
        # return False
    
    def get_evolved_version(self) -> PokemonBase:
        
        """
        Description:
        "get_evolved_version" is a method of the class Gastly. It gets the evolved version of the pokemon. Gastly evolves into Haunter.

        Complexity: best case and worst case of O(self.level), where self.level is the level of Gastly.

        Arguments: 
        None

        Returns:
        Always returns Gastly as Haunter evolves at the base lv 1. Also intilsiaes Haunter's hp by taking into account how much damage Haunter has previously taken.
        """
        lost_hp = 6+(self.level//2) - self.hp
        evolved_poke = Haunter()
        evolved_poke.lose_hp(lost_hp)
        if self.level > 1:
            for _ in range(0, self.level):
                evolved_poke.level_up()
        return evolved_poke

    def attack(self, other: PokemonBase) -> None:
        """
        Description:
        "attack" is a method of the class Gastly. It simulates Gastly attacking another enemy pokemon, taking into consideration: status effects, 
        effective attack multiplers, lost hp.

        Complexity: best case and worst case of O(k), where k is the cost of comparison

        Arguments:
        other: the defending pokemon
        
        Returns:
        No return value.
        """
        # Step 1: Status effects on attack damage / redirecting attacks
            #Check three conditions:
            # - Sleep: FAILS - stop attack 
            # - Confusion: Chance to attack yourself 50% 
            # - Burn: Halves effective attack (To be calculated AFTER effective attack is calculated, have a multiplier for now)
        if self.status_effect == "Sleep":
            return #If its alseep, it will not attack (dont need step 2 - 3), it will not lose hp to status effects (step 4) and it will not attack, therefore cannot apply status effects (step 5)

        if self.status_effect == "Confusion":
            if RandomGen.random_chance(0.5) == True: 
                other = self #Set other (defending pokemon) equal to self (attacking pokemon). This simulates the pokemon attacking itself.
            

        burn_effective_attack_multiplier = 1 #If the pokemon isn't "Burn", multiplying by 1 will not change the "effective attack" value
        if self.status_effect == "Burn":
            burn_effective_attack_multiplier = 0.5 
            

        # Step 2: Do the attack calculation taking into "attack v defender type" multipliers (effective attack)
            #NOTe: Need to calculate the effective attack depending on the defences of the "other" pokemon
            #NOTe: Account for the burn 50% less effective attack 
            #NOTe: Account for the 50% chance to attack yourself from confusion (already accounted for)
        attack_multiplier = PokeType(self.poke_type, other.poke_type) 
        type_multiplier = attack_multiplier.multiplier()
        attack_damage = self.get_attack_damage()
        effective_attack = (burn_effective_attack_multiplier)*(attack_damage)*(type_multiplier) #Trying to get: Multiplier depending on attacking and defending pokemon
        


        # Step 3: Losing hp to 'effective attack - any defence multiplers/constants"
        other.defend(effective_attack) #"other.defend" calculates how much hp is loss and changes the values of "other.hp"


        # Step 4: Losing hp to status effects
        #Check 2 conditions (only two status effects make you lose hp):      
        if self.status_effect == "Burn": # - Burn: Lose 1 hp
            self.lose_hp(1)

        if self.status_effect == "Poison": # - Poison: After SUCCCESSFUL attack, lose 3 hp
            self.lose_hp(3) 


        # Step 5: Possibly applying status effects
        if RandomGen.random_chance(0.2): # 20% chance to see if the pokemon gets hit with a status effect
            if self.poke_type == "Fire": 
                other.status_effect = "Burn"
            if self.poke_type == "Grass":
                other.status_effect = "Poison"
            if self.poke_type == "Water":
                other.status_effect = "Paralysis"
                other.speed = other.speed // 2
            if self.poke_type == "Ghost":
                other.status_effect = "Sleep"
            if self.poke_type == "Normal":
                other.status_effect = "Confusion"

        return #No return value as other.defend already changes the hp


class Eevee(PokemonBase):
    def __init__(self):
        """ 
        Initialises a Eevee object where it has its own individual attributes. Inherits from PokemonBase as it is a Pokemon
        and therefore has attributes that are common across all Pokemon
        :complexity: best case and worst case of O(1) 
        """
        self.name = 'Eevee'
        self.level = 1
        self.hp = 10
        self.poke_type = 'Normal'
        PokemonBase.__init__(self, self.hp, self.poke_type)
        self.attack_power = 6 + self.level
        self.speed = 7 + self.level
        self.defence = 4 + self.level
        self.status_effect = None

    def level_up(self) -> None:
        """
        Description:
        "level_up" is a method of the class Eevee. It increases the level of the pokemon. Upon levelling, it takes into 
        consideration the amount of HP lost previously before levelling and subracts it from the max hp of the new pokemon.

        Complexity: best case and worst case of O(k), where k is the cost of comparison

        Arguments: 
        Takes no arguement.

        Returns:
        Does not return anything.
        """
        self.level += 1
        self.attack_power = 6 + self.level
        if self.status_effect == "Paralysis":
            self.speed = (7 + self.level)//2
        else:
            self.speed = (7 + self.level)
        self.defence = 4 + self.level

    def heal(self) -> None:
        """
        Description:
        "heal" is a method of the class Eevee. It restores the max HP of the pokemon and removes any status effects that it may have. 

        Complexity: best case and worst case of O(1)

        Arguments: 
        Takes no argument.

        Returns:
        Does not return anything.
        """
        self.hp = 10
        self.status_effect = None
        self.speed = (7 + self.level)
    def defend(self, damage: int) -> None:
        """
        Description:
        "defend" is a method of the class Eevee. It determines how much damage the pokemon should take. If the effective attack is equal to or greater than defence,
        lose hp equal to the effective attack. Otherwise, take no damage.

        Complexity: best case and worst case of O(1)

        Arguments: 
        damage: the amount of damage the enemy pokemon is inflicting 

        Returns:
        Does not return anything.
        """
        if damage >= self.defence:
            self.lose_hp(damage)
    
    def should_evolve(self) -> bool:
        """
        Description:
        "should_evolve" is a method of the class Eevee. It determines if the pokemon should evolve. In the case of Eevee, it doesn't evolve into anything.

        Complexity: best case and worst case of O(1)

        Arguments: 
        None

        Returns:
        False: Eevee can not evolve.
        """
        return False

    def get_evolved_version(self) -> None:
        """
        Description:
        "get_evolved_version" is a method of the class Eevee. It gets the evolved version of the pokemon. But Eevee can no longer evolve.

        Complexity: best case and worst case of O(1)

        Arguments: 
        None

        Returns:
        None: Returns none as there is no pokemon Eevee can evolve into
        """
        return None
    
    def attack(self, other: PokemonBase) -> None:
        """
        Description:
        "attack" is a method of the class Eevee. It simulates Eevee attacking another enemy pokemon, taking into consideration: status effects, 
        effective attack multiplers, lost hp.

        Complexity: best case and worst case of O(k)

        Arguments:
        other: the defending pokemon
        
        Returns:
        No return value.
        """
        # Step 1: Status effects on attack damage / redirecting attacks
            #Check three conditions:
            # - Sleep: FAILS - stop attack 
            # - Confusion: Chance to attack yourself 50% 
            # - Burn: Halves effective attack (To be calculated AFTER effective attack is calculated, have a multiplier for now)
        if self.status_effect == "Sleep":
            return #If its alseep, it will not attack (dont need step 2 - 3), it will not lose hp to status effects (step 4) and it will not attack, therefore cannot apply status effects (step 5)

        if self.status_effect == "Confusion":
            if RandomGen.random_chance(0.5) == True: 
                other = self #Set other (defending pokemon) equal to self (attacking pokemon). This simulates the pokemon attacking itself.
            

        burn_effective_attack_multiplier = 1 #If the pokemon isn't "Burn", multiplying by 1 will not change the "effective attack" value
        if self.status_effect == "Burn":
            burn_effective_attack_multiplier = 0.5 
            

        # Step 2: Do the attack calculation taking into "attack v defender type" multipliers (effective attack)
            #NOTe: Need to calculate the effective attack depending on the defences of the "other" pokemon
            #NOTe: Account for the burn 50% less effective attack 
            #NOTe: Account for the 50% chance to attack yourself from confusion (already accounted for)
        attack_multiplier = PokeType(self.poke_type, other.poke_type) 
        type_multiplier = attack_multiplier.multiplier()
        attack_damage = self.get_attack_damage()
        effective_attack = round((burn_effective_attack_multiplier)*(attack_damage)*(type_multiplier)) #Trying to get: Multiplier depending on attacking and defending pokemon


        # Step 3: Losing hp to 'effective attack - any defence multiplers/constants"
        other.defend(effective_attack) #"other.defend" calculates how much hp is loss and changes the values of "other.hp"


        # Step 4: Losing hp to status effects
        #Check 2 conditions (only two status effects make you lose hp):      
        if self.status_effect == "Burn": # - Burn: Lose 1 hp
            self.lose_hp(1)

        if self.status_effect == "Poison": # - Poison: After SUCCCESSFUL attack, lose 3 hp
            self.lose_hp(3) 


        # Step 5: Possibly applying status effects
        if RandomGen.random_chance(0.2): # 20% chance to see if the pokemon gets hit with a status effect
            if self.poke_type == "Fire": 
                other.status_effect = "Burn"
            if self.poke_type == "Grass":
                other.status_effect = "Poison"
            if self.poke_type == "Water":
                other.status_effect = "Paralysis"
                other.speed = other.speed//2
            if self.poke_type == "Ghost":
                other.status_effect = "Sleep"
            if self.poke_type == "Normal":
                other.status_effect = "Confusion"

        return #No return value as other.defend already changes the hp
