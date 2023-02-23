from pokemon import *
from tests.base_test import BaseTest

class TestPokemon(BaseTest):

    def test_venusaur_stats(self):
        v = Venusaur()
        self.assertEqual(v.get_hp(), 21)
        self.assertEqual(v.get_level(), 2)
        self.assertEqual(v.get_attack_damage(), 5)
        self.assertEqual(v.get_speed(), 4)
        self.assertEqual(v.get_defence(), 10)
        v.level_up()
        v.level_up()
        v.level_up()
        self.assertEqual(v.get_hp(), 22)
        self.assertEqual(v.get_level(), 5)
        self.assertEqual(v.get_attack_damage(), 5)
        self.assertEqual(v.get_speed(), 5)
        self.assertEqual(v.get_defence(), 10)
        v.lose_hp(5)

        self.assertEqual(str(v), "LV. 5 Venusaur: 17 HP")




    #//////////////////////////////////////////////////////////////
    #Own test cases below
    #//////////////////////////////////////////////////////////////

    def test_custom_level_up(self):
        """
        Tests if level_up is able to correctly level up:
        Test 1: Charizard 
        Test 2: Bulbasaur 
        Test 3: Squirtle 
        """
        c = Charizard()
        c.level_up()
        self.assertEqual(c.get_level(), 4)

        b = Bulbasaur()
        b.level_up()
        self.assertEqual(b.get_level(), 2)

        s = Squirtle()
        s.level_up()
        s.level_up()
        self.assertEqual(s.get_level(), 3)

    def test_custom_heal(self):
        """
        Test if heal is able to correctly heal (heal hp and clear status effects) a pokemon that has: 
        Test 1: lost 4 hp
        Test 2: has a status effect 
        Test 3: has a status effect and lost hp 
        """
        v = Venusaur()
        v.lose_hp(4)
        v.heal()
        self.assertEqual(v.hp, 21)
        self.assertEqual(v.status_effect, None)    

        h = Haunter()
        h.status_effect = "Burn"
        h.heal()
        self.assertEqual(h.status_effect, None)

        c = Charmander()
        c.status_effect = "Paralysis"
        c.lose_hp(2)
        c.heal()
        self.assertEqual(c.get_speed(), 8) 
    

    def test_custom_defend(self):
        """"
        Test if defend is able to correctly modify the hp of the pokemon involve in the defence:
        Test 1: hp equal to positive value after defending 
        Test 2: hp equal to 0 after defending 
        Test 3: hp equal to negative value after defending 
        """
        c = Charmander()
        c.defend(5)
        self.assertEqual(c.get_hp(), 4)

        c = Charmander()
        c.defend(9)
        self.assertEqual(c.get_hp(), 0)

        b = Blastoise()
        b.defend(40)
        self.assertEqual(b.get_hp(), -19)


    def test_custom_should_evolve(self):
        """
        Test if should_evolve is able to correctly determine if a pokemon should evolve or not: 
        Test 1: Charizard should not further evolve, no matter the level.
        Test 2: Gengar should not further evolve, no matter the level.
        Test 3: Bulbsaur at level 1 should not evolve, after leveling up, it should now evolve.
        """
        c = Charizard()
        self.assertEqual(c.should_evolve(), False)

        g = Gengar()
        self.assertEqual(g.should_evolve(), False)

        b = Bulbasaur()
        self.assertEqual(b.should_evolve(), False)
        b.level_up()
        self.assertEqual(b.should_evolve(), True)


    def test_custom_get_evolved_version(self):
        """
        Tests if get_evolved_version is able to correctly retrieve the evolved version of a pokemon: 
        Test 1: Eevee cannot evolve.
        Test 2: Haunter evolves into Gengar
        Test 3: Charmander evolves into Charizard.
        """
        e = Eevee()
        self.assertEqual(e.get_evolved_version(), None)

        s = Haunter()
        self.assertIsInstance(s.get_evolved_version(), Gengar)

        c = Charmander()
        self.assertIsInstance(c.get_evolved_version(), Charizard)


    def test_custom_attack(self):
        """
        Test if the attack function is able to correctly simulate an attack between two pokemons:
        Test 1: Eevee attacks Bublasaur (inc "Posion" status effect)
        Test 2: Bulbasaur attacks Eevee (inc "Burn" status effect)
        Test 3: Bulbasaur attacks Eevee (inc "Sleep" status effect)
        """
        e = Eevee()
        b = Bulbasaur()
        e.status_effect = "Poison"
        e.attack(b)
        self.assertEqual(b.get_hp(), 9)
        self.assertEqual(e.get_hp(), 7)

        e = Eevee()
        b = Bulbasaur()
        b.status_effect = "Burn"
        b.attack(e)
        self.assertEqual(e.get_hp(), 10)
        self.assertEqual(b.get_hp(), 12)

        e = Eevee()
        b = Bulbasaur()
        b.status_effect = "Sleep"
        b.attack(e)
        self.assertEqual(e.get_hp(), 10)