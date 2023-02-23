from poke_team import Action, Criterion, PokeTeam
from random_gen import RandomGen
from pokemon import Bulbasaur, Charizard, Charmander, Gastly, Squirtle, Eevee
from tests.base_test import BaseTest

class TestPokeTeam(BaseTest):

    def test_random(self):
        RandomGen.set_seed(123456789)
        t = PokeTeam.random_team("Cynthia", 0)
        pokemon = []
        while not t.is_empty():
            pokemon.append(t.retrieve_pokemon())
        expected_classes = [Squirtle, Gastly, Eevee, Eevee, Eevee, Eevee]
        self.assertEqual(len(pokemon), len(expected_classes))
        for p, e in zip(pokemon, expected_classes):
            self.assertIsInstance(p, e)

    #ADD test_regen_team 0 and 1
    def test_regen_team(self):
        RandomGen.set_seed(123456789)
        t = PokeTeam.random_team("Cynthia", 2, team_size=4, criterion=Criterion.HP)
        # This should end, since all pokemon are fainted, slowly.
        while not t.is_empty():
            p = t.retrieve_pokemon()
            p.lose_hp(1)
            t.return_pokemon(p)
        t.regenerate_team()
        pokemon = []
        while not t.is_empty():
            pokemon.append(t.retrieve_pokemon())
        expected_classes = [Bulbasaur, Eevee, Charmander, Gastly]
        self.assertEqual(len(pokemon), len(expected_classes))
        for p, e in zip(pokemon, expected_classes):
            self.assertIsInstance(p, e)

    def test_battle_option_attack(self):
        t = PokeTeam("Wallace", [1, 0, 0, 0, 0], 1, PokeTeam.AI.ALWAYS_ATTACK)
        p = t.retrieve_pokemon()
        e = Eevee()
        self.assertEqual(t.choose_battle_option(p, e), Action.ATTACK)
    
    #ADD TEST_SPECIAL_MODE_0 and ADD TEST_SPECIAL_MODE_2
    def test_special_mode_1(self):
        t = PokeTeam("Lance", [1, 1, 1, 1, 1], 1, PokeTeam.AI.SWAP_ON_SUPER_EFFECTIVE)
        # C B S G E
        t.special()
        # S G E B C
        pokemon = []
        while not t.is_empty():
            pokemon.append(t.retrieve_pokemon())
        expected_classes = [Squirtle, Gastly, Eevee, Bulbasaur, Charmander]
        self.assertEqual(len(pokemon), len(expected_classes))
        for p, e in zip(pokemon, expected_classes):
            self.assertIsInstance(p, e)

    def test_string(self):
        t = PokeTeam("Dawn", [1, 1, 1, 1, 1], 2, PokeTeam.AI.RANDOM, Criterion.DEF)
        self.assertEqual(str(t), "Dawn (2): [LV. 1 Gastly: 6 HP, LV. 1 Squirtle: 11 HP, LV. 1 Bulbasaur: 13 HP, LV. 1 Eevee: 10 HP, LV. 1 Charmander: 9 HP]")
    
    #//////////////////////////////////////////////////////////////
    #Own test cases below
    #//////////////////////////////////////////////////////////////

    def test_special_0(self):
        """
        test_special_0 tests the special() function for battle_mode = 0. special() should swap the first and last pokemon on the team.
        """
        RandomGen.set_seed(123456789)
        t = PokeTeam.random_team("Cynthia", 0)
        t.special()
        pokemon = []
        self.assertEqual(str(t), 'Cynthia (0): [LV. 1 Eevee: 10 HP, LV. 1 Gastly: 6 HP, LV. 1 Eevee: 10 HP, LV. 1 Eevee: 10 HP, LV. 1 Eevee: 10 HP, LV. 1 Squirtle: 11 HP]')
        while not t.is_empty():
            pokemon.append(t.retrieve_pokemon())
        expected_classes = [Eevee, Gastly, Eevee, Eevee, Eevee, Squirtle]
        self.assertEqual(len(pokemon), len(expected_classes))
        for p, e in zip(pokemon, expected_classes):
            self.assertIsInstance(p, e)
    
    def test_special_2(self):
        """
        test_special_2 tests the special() function for battle mode 2. special() should reverse the sorting 
        order of the team (so HP increasing becomes decreasing, and if special is used again it reverts back to increasing)
        """
        RandomGen.set_seed(123456789)
        t = PokeTeam.random_team("Cynthia", 2, team_size=4, criterion=Criterion.HP)
        t.special()
        self.assertEqual(str(t), 'Cynthia (2): [LV. 1 Gastly: 6 HP, LV. 1 Charmander: 9 HP, LV. 1 Eevee: 10 HP, LV. 1 Bulbasaur: 13 HP]')
        pokemon = []
        while not t.is_empty():
            pokemon.append(t.retrieve_pokemon())
        expected_classes = [Gastly, Charmander, Eevee, Bulbasaur]
        self.assertEqual(len(pokemon), len(expected_classes))
        for p, e in zip(pokemon, expected_classes):
            self.assertIsInstance(p, e)

    #ADD test_regen_team 0 and 1
    def test_regen_team_0(self):
        """
        test_regen_team_0 tests the regenerate_team method for battle mode 2, ensuring correct pokemon arrangement.
        """
        RandomGen.set_seed(123456789)
        t = PokeTeam.random_team("Cynthia", 0)
        
        while not t.is_empty():
            p = t.retrieve_pokemon()
            p.lose_hp(1)
            t.return_pokemon(p)
        t.regenerate_team()
        pokemon = []
        while not t.is_empty():
            pokemon.append(t.retrieve_pokemon())
        expected_classes = [Squirtle, Gastly, Eevee, Eevee, Eevee, Eevee]
        self.assertEqual(len(pokemon), len(expected_classes))
        for p, e in zip(pokemon, expected_classes):
            self.assertIsInstance(p, e)

    def test_regen_team_1(self):
        """
        test_regen_team_1 tests the regenerate_team method for battle mode 1, ensuring correct pokemon arrangement.
        """
        t = PokeTeam("Lance", [1, 1, 1, 1, 1], 1, PokeTeam.AI.SWAP_ON_SUPER_EFFECTIVE)
        
        while not t.is_empty():
            p = t.retrieve_pokemon()
            p.lose_hp(1)
            t.return_pokemon(p)
        t.regenerate_team()
        pokemon = []
        while not t.is_empty():
            pokemon.append(t.retrieve_pokemon())
        expected_classes = [Charmander, Bulbasaur, Squirtle, Gastly, Eevee]
        self.assertEqual(len(pokemon), len(expected_classes))
        for p, e in zip(pokemon, expected_classes):
            self.assertIsInstance(p, e)

    def test_custom_str(self):
        """
        test_custom_str tests if __str___() can correctly represent a pokemon team as a string with: 
        Test 1: Battle mode 0, Squirtle - Gastly - Eeevee
        Test 2: Battle mode 2, Gastly - Squirtle - Charmander (ordered by criterion)
        Test 3: Battle mode 1, Squirtle
        """
        t = PokeTeam("Christian", [0, 0, 1, 1, 1], 0, PokeTeam.AI.ALWAYS_ATTACK)
        self.assertEqual(str(t), "Christian (0): [LV. 1 Squirtle: 11 HP, LV. 1 Gastly: 6 HP, LV. 1 Eevee: 10 HP]")

        t = PokeTeam("Jesus", [1, 0, 1, 1, 0], 2, PokeTeam.AI.RANDOM, Criterion.DEF)
        self.assertEqual(str(t), "Jesus (2): [LV. 1 Gastly: 6 HP, LV. 1 Squirtle: 11 HP, LV. 1 Charmander: 9 HP]")

        t = PokeTeam("Ziggy", [0, 0, 1, 0, 0], 1, PokeTeam.AI.SWAP_ON_SUPER_EFFECTIVE)
        self.assertEqual(str(t), "Ziggy (1): [LV. 1 Squirtle: 11 HP]")


    def test_custom_is_empty(self):
        """
        test_custom_is_empty tests if is_empty() is able to correctly recognise when a poke team is empty/
        """
        t = PokeTeam("Christian", [0, 0, 1, 1, 1], 0, PokeTeam.AI.ALWAYS_ATTACK)
        self.assertEqual(t.is_empty(), False)
        
        t = PokeTeam("Jordan", [0, 0, 0, 0, 0], 1, PokeTeam.AI.RANDOM)
        self.assertEqual(t.is_empty(), True)

        t = PokeTeam("Hulk", [0, 0, 0, 0, 1], 2, PokeTeam.AI.SWAP_ON_SUPER_EFFECTIVE, Criterion.SPD)
        self.assertEqual(t.is_empty(), False)


    def test_custom_retrieve_pokemon(self):
        """
        test_custom_retrieve_pokemon tests if retrieve_pokemon is able to correctly retrieve the desired pokemon from a team.
        Test 1: battle mode = 0  
        Test 2: battle_mode = 1 
        Test 3: battle_mode = 2 
        """
        t = PokeTeam("Christian", [0, 0, 1, 1, 1], 0, PokeTeam.AI.ALWAYS_ATTACK)
        self.assertIsInstance(t.retrieve_pokemon(), Squirtle)
        
        t = PokeTeam("Jordan", [1, 0, 0, 0, 0], 1, PokeTeam.AI.RANDOM)
        self.assertIsInstance(t.retrieve_pokemon(), Charmander)

        t = PokeTeam("Hulk", [0, 0, 0, 0, 1], 2, PokeTeam.AI.SWAP_ON_SUPER_EFFECTIVE, Criterion.SPD)
        self.assertIsInstance(t.retrieve_pokemon(), Eevee)


    def test_custom_choose_battle_mode_option(self):
        """
        test_custom_choose_battle_mode_option chooses the pokemon ai depending on:
        Test 1: Battle mode = 1, always attack (True)
        Test 2: Battle mode = 1, swap on super effective (True)
        Test 3: Battle mode = 0, swap on super effective (False)
        """
        t = PokeTeam("Jordan", [1, 1, 1, 0, 1], 1, PokeTeam.AI.ALWAYS_ATTACK)
        p = t.retrieve_pokemon() #Charmander, first pokemon
        c = Charmander()
        self.assertEqual(t.choose_battle_option(p, c), Action.ATTACK)

        t = PokeTeam("James", [0, 0, 1, 1, 1], 1, PokeTeam.AI.SWAP_ON_SUPER_EFFECTIVE)
        p = t.retrieve_pokemon() #Charmander
        e = Charmander() 
        self.assertEqual(t.choose_battle_option(p, e), Action.SWAP) #Squirtle has super effective attack VS Charmander

        t = PokeTeam("Jesus", [1, 0, 0, 0, 0], 0, PokeTeam.AI.SWAP_ON_SUPER_EFFECTIVE)
        p = t.retrieve_pokemon()
        e = Eevee()
        self.assertEqual(t.choose_battle_option(p, e), Action.ATTACK) #Eevee does NOT have super effective VS Charmander