from random_gen import RandomGen
from battle import Battle
from poke_team import Criterion, PokeTeam
from pokemon import Bulbasaur, Charizard, Charmander, Eevee, Gastly, Squirtle, Venusaur, Gengar
from tests.base_test import BaseTest

class TestBattle(BaseTest):

    def test_basic_battle(self):
        RandomGen.set_seed(1337)
        team1 = PokeTeam("Ash", [1, 1, 1, 0, 0], 0, PokeTeam.AI.ALWAYS_ATTACK)
        team2 = PokeTeam("Gary", [0, 0, 0, 0, 3], 0, PokeTeam.AI.ALWAYS_ATTACK)
        b = Battle(verbosity=0)
        res = b.battle(team1, team2)
        self.assertEqual(res, 1)
        self.assertTrue(team2.is_empty())
        remaining = []
        while not team1.is_empty():
            remaining.append(team1.retrieve_pokemon())
        self.assertEqual(len(remaining), 2)
        self.assertEqual(remaining[0].get_hp(), 1)
        self.assertIsInstance(remaining[0], Venusaur)
        self.assertEqual(remaining[1].get_hp(), 11)
        self.assertIsInstance(remaining[1], Squirtle)

    def test_complicated_battle(self):
        RandomGen.set_seed(192837465)
        team1 = PokeTeam("Brock", [1, 1, 1, 1, 1], 2, PokeTeam.AI.SWAP_ON_SUPER_EFFECTIVE, criterion=Criterion.HP)
        team2 = PokeTeam("Misty", [0, 0, 0, 3, 3], 2, PokeTeam.AI.SWAP_ON_SUPER_EFFECTIVE, criterion=Criterion.SPD)
        b = Battle(verbosity=0)
        res = b.battle(team1, team2)
        self.assertEqual(res, 1)
        remaining = []
        while not team1.is_empty():
            remaining.append(team1.retrieve_pokemon())
        self.assertEqual(len(remaining), 2)
        self.assertEqual(remaining[0].get_hp(), 11)
        self.assertIsInstance(remaining[0], Charizard)
        self.assertEqual(remaining[1].get_hp(), 6)
        self.assertIsInstance(remaining[1], Gastly)

    #//////////////////////////////////////////////////////////////
    #Own test cases below
    #//////////////////////////////////////////////////////////////

    def test_custom_test_1(self):
        """
        test_custom_test_1 tests the battle() function using: 
        - Battle mode 1 
        - Team 1 ai = ALWAYS_ATTACK 
        - Team 2 ai = ALWAYS_ATTACK
        """
        team1 = PokeTeam("Tony Stark", [1, 1, 1, 1, 1], 1, PokeTeam.AI.ALWAYS_ATTACK)
        team2 = PokeTeam("Thanos", [0, 0, 0, 3, 3], 1, PokeTeam.AI.ALWAYS_ATTACK)
        b = Battle(verbosity=0)
        res = b.battle(team1, team2)
        self.assertEqual(res, 1)
        remaining = []
        while not team1.is_empty():
            remaining.append(team1.retrieve_pokemon())
        self.assertEqual(len(remaining), 5)
        self.assertEqual(remaining[0].get_hp(), 13)
        self.assertIsInstance(remaining[0], Bulbasaur)
        self.assertEqual(remaining[1].get_hp(), 11)
        self.assertIsInstance(remaining[1], Squirtle)
    
    def test_custom_test_2(self):
        """
        test_custom_test_2 tests the battle() function using: 
        - Battle mode 12
        - Team 1 ai = Criterion.DEF
        - Team 2 ai = Criterion.SPD
        """
        RandomGen.set_seed(20000)
        team1 = PokeTeam("Cap", [1, 1, 1, 1, 1], 2, PokeTeam.AI.RANDOM, criterion=Criterion.DEF)
        team2 = PokeTeam("Bucky", [0, 0, 0, 3, 3], 2, PokeTeam.AI.RANDOM, criterion=Criterion.SPD)
        b = Battle(verbosity=0)
        res = b.battle(team1, team2)
        self.assertEqual(res, 2)
        remaining = []
        while not team2.is_empty():
            remaining.append(team2.retrieve_pokemon())
        self.assertEqual(len(remaining), 2)
        self.assertEqual(remaining[0].get_hp(), 7)
        self.assertIsInstance(remaining[0], Eevee)
        self.assertEqual(remaining[1].get_hp(), 11)
        self.assertIsInstance(remaining[1], Gengar)
