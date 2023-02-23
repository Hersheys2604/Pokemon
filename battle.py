"""
This file contains the class: Battle
Battle uses 2 teams and has them battle each other with their team of Pokemon
"""
__author__ = "Scaffold by Jackson Goerner, Code by ______________"

from random_gen import RandomGen
from poke_team import Action, PokeTeam, Criterion
from print_screen import print_game_screen

class Battle:
    
    def __init__(self, verbosity=0) -> None:
        """
        This initialises the heal counter for each team. Each counter starts as 0 as no team has used heal yet.
        Complexity = O(1)
        """
        self.heal_counter_team1 = 0
        self.heal_counter_team2 = 0

    def battle(self, team1: PokeTeam, team2: PokeTeam) -> int:
        """
        Description:
        "battle" is a method of the class Battle that simulates a battle between two pokemon teams returning 0 (draw), 1 (team1 wins) or 2 (team2 wins) depending 
        on the result of the battle.

        Arguments:
        "battle" takes two arguments to perform the battle on, team 1 and team 2. 

        Returns:
        Return the value 0 when the battle is a draw, 1 when team 1 wins the battle and 2 when team 2 wins the battle.

        Complexity:
        Best Case: O(n), where n is the maxiumum capacity of pokemons in a team. This only occurs when battle mode is 0 or 1.
        """
        
        #Battle starts by retrieving pokemon to send to battle.
        self.heal_counter_team1 = 0
        self.heal_counter_team2 = 0
        poke1 = team1.retrieve_pokemon()
        poke2 = team2.retrieve_pokemon()
        
        while True: #THEN, they have 4 choices: Attack, Swap, Heal, Special
            action1 = team1.choose_battle_option(poke1,poke2)
            action2 = team2.choose_battle_option(poke2,poke1)

            if action1 == Action.SWAP: #Handle any swap conditions
                poke1.clear_status_effects()
                team1.return_pokemon(poke1)
                poke1 = team1.retrieve_pokemon()
            if action2 == Action.SWAP:
                poke2.clear_status_effects()
                team2.return_pokemon(poke2)
                poke2 = team2.retrieve_pokemon()
            
            if action1 == Action.SPECIAL: #Handle any special conditions 
                poke1.clear_status_effects()
                team1.return_pokemon(poke1)
                team1.special()
                poke1 = team1.retrieve_pokemon()
            if action2 == Action.SPECIAL:
                poke2.clear_status_effects()
                team2.return_pokemon(poke2)
                team2.special()
                poke2 = team2.retrieve_pokemon()

            if action1 == Action.HEAL: #Handle any heal actions (if they have healed 3 times, lose if they pick heal)
                if self.heal_counter_team1 < 3:
                    poke1.heal()
                    self.heal_counter_team1 +=1
                else:
                    return 2
            if action2 == Action.HEAL:
                if self.heal_counter_team2 < 3:
                    poke2.heal()
                    self.heal_counter_team2 +=1
                else:
                    return 1

            #Handle attacks (if both pokemon are attacking, look at indented below)
            if action1 == Action.ATTACK and action2 != Action.ATTACK:
                poke1.attack(poke2)

            if action1 != Action.ATTACK and action2 == Action.ATTACK:
                poke2.attack(poke1)
        
            
            #Faster pokemon attacks first, if the slower pokemon has not fainted. It then attacks. (same speed --> team 1 attack)
            if action1 == Action.ATTACK and action2 == Action.ATTACK:
                if poke1.get_speed() > poke2.get_speed():
                    poke1.attack(poke2)
                    if not poke2.is_fainted():
                        poke2.attack(poke1)

                elif poke1.get_speed() < poke2.get_speed():
                    poke2.attack(poke1)
                    if not poke1.is_fainted():
                        poke1.attack(poke2)

                elif poke1.get_speed() == poke2.get_speed():
                    poke1.attack(poke2)

                    poke2.attack(poke1)

            #If both pokemon are fainted then both lose 1 hp.
            if poke1.is_fainted() == False and poke2.is_fainted() == False:
                poke1.lose_hp(1)
                poke2.lose_hp(1)

            #If both pokemon have fainted and both teams are empty then 0 is returned
            if poke1.is_fainted() and poke2.is_fainted():
                if team1.is_empty() and team2.is_empty():
                    return 0
            #If one pokemon has fainted and the other has not, other pokemon levels up.
            if poke1.is_fainted() and poke2.is_fainted() == False:
                poke2.level_up()
            if poke2.is_fainted() and poke1.is_fainted() == False:
                poke1.level_up()
            
            #If a pokemon has not fainted and can evolve, they evolve
            if not poke1.is_fainted():
                if poke1.should_evolve():
                    poke1 = poke1.get_evolved_version()
            if not poke2.is_fainted():
                if poke2.should_evolve():
                    poke2 = poke2.get_evolved_version()

            #If a pokemon has fainted, a new pokemon is retrieved from that team. If team is empty then the other team wins 
            if poke1.is_fainted():
                if not team1.is_empty():
                    poke1 = team1.retrieve_pokemon()
                else:
                    poke2.clear_status_effects()
                    team2.return_pokemon(poke2)
                    return 2
            if poke2.is_fainted():
                if not team2.is_empty():
                    poke2  = team2.retrieve_pokemon()
                else:
                    poke1.clear_status_effects()
                    team1.return_pokemon(poke1)
                    return 1
    


if __name__ == "__main__":
    b = Battle(verbosity=3)
    RandomGen.set_seed(16)
    t1 = PokeTeam.random_team("Cynthia", 0, criterion=Criterion.SPD)
    t1.ai_type = PokeTeam.AI.USER_INPUT
    t2 = PokeTeam.random_team("Barry", 1)
    print(b.battle(t1, t2))
