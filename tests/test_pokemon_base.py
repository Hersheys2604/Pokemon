from random_gen import RandomGen
from pokemon_base import PokemonBase, PokeType
from pokemon import *
from tests.base_test import BaseTest

class TestPokemonBase(BaseTest):

    def test_cannot_init(self):
        """Tests that we cannot initialise PokemonBase, and that it raises the correct error."""
        self.assertRaises(TypeError, lambda: PokemonBase(30, PokeType.FIRE))

    def test_level(self):
        e = Eevee()
        self.assertEqual(e.get_level(), 1)
        e.level_up()
        self.assertEqual(e.get_level(), 2)
    
    def test_hp(self):
        e = Eevee()
        self.assertEqual(e.get_hp(), 10)
        e.lose_hp(4)
        self.assertEqual(e.get_hp(), 6)
        e.heal()
        self.assertEqual(e.get_hp(), 10)

    def test_status(self):
        RandomGen.set_seed(0)
        e1 = Eevee()
        e2 = Eevee()
        e1.attack(e2)
        # e2 now is confused.
        e2.attack(e1)
        # e2 takes damage in confusion.
        self.assertEqual(e1.get_hp(), 10)

    def test_evolution(self):
        g = Gastly()
        self.assertEqual(g.can_evolve(), True)
        self.assertEqual(g.should_evolve(), True)
        new_g = g.get_evolved_version()
        self.assertIsInstance(new_g, Haunter)

    def test_evolution_hp(self):
        b = Bulbasaur()
        b.lose_hp(5)
        b.level_up()
        if b.should_evolve() == True:
            x = b.get_evolved_version()
        self.assertEqual(x.get_hp(), 16)
        self.assertEqual(x.get_speed(), 4)

    #//////////////////////////////////////////////////////////////
    #Own test cases below
    #//////////////////////////////////////////////////////////////
    def test_custom_is_fainted(self):
        """
        Tests if is_fainted is able to recognise when a pokemon:
        Test 1: is fainted when its hp = 0
        Test 2: is fainted when its hp < 0 
        Test 3: has not been dealt enough damage to faint.
        """
        p = Eevee()
        p.lose_hp(10)
        self.assertEqual(p.is_fainted(), True)

        p = Charizard()
        p.lose_hp(20)
        self.assertEqual(p.is_fainted(), True)

        p = Bulbasaur()
        p.lose_hp(11)
        self.assertEqual(p.is_fainted(), False)


    def test_get_speed(self):
        """
        Tests if get_speed is able to correctly retreive the speed of a:
        Test 1: base pokemon.
        Test 2: leveled up pokemon 
        Test 3: evolved pokemon.
        """
        p = Charmander()
        self.assertEqual(p.get_speed(), 8)
        
        p = Gastly()
        p.level_up()
        self.assertEqual(p.get_speed(), 2)

        p = Charizard()
        self.assertEqual(p.get_speed(), 12)


    def test_custom_get_attack_damage(self):
        """
        Tests if get_attack_damage is able to retreive the attack damage of a:
        Test 1: evolved pokemon 
        Test 2: leveled up pokemon
        Test 3: multiple leveled up pokemon
        """
        p = Venusaur()
        self.assertEqual(p.get_attack_damage(), 5)

        p = Squirtle()
        p.level_up()
        self.assertEqual(p.get_attack_damage(), 5)

        p = Eevee()
        p.level_up()
        p.level_up()
        p.level_up()
        self.assertEqual(p.get_attack_damage(), 10)


    def test_custom_get_defence(self):
        """
        Tests if get_defence is able to correctly retreieve the defence of a:
        Test 1: base pokemon 
        Test 2:  leveled up pokemon
        Test 3: evolved pokemon
        """ 
        p = Gastly()
        self.assertEqual(p.get_defence(), 8)

        p = Blastoise()
        p.level_up()
        self.assertEqual(p.get_defence(), 12)

        p = Haunter()
        self.assertEqual(p.get_defence(), 6)


    def test_custom_lose_hp(self):
        """
        Tests if lose_hp is able to correctly change the hp of a:
        Test 1: pokemon that is left with positive hp after losing hp.
        Test 2: pokemon that is left with negative hp after losing hp.
        Test 3: pokemon that is left with 0 hp after losing hp.
        """
        p = Haunter()
        p.lose_hp(5)
        self.assertEqual(p.get_hp(), 4)

        p = Gengar()
        p.lose_hp(14)
        self.assertEqual(p.get_hp(), -1)

        p = Eevee()
        p.lose_hp(10)
        self.assertEqual(p.get_hp(), 0)


    def test_custom_get_poke_name(self):
        """
        Test if get_poke_name is able to correctly return the names of the pokemon:
        Test 1: Charizard 
        Test 2: Charmander 
        Test 3: Blastoise
        """
        p = Charizard()
        self.assertEqual(p.get_poke_name(), "Charizard")

        p = Charmander()
        self.assertEqual(p.get_poke_name(), "Charmander")
        
        p = Blastoise()
        self.assertEqual(p.get_poke_name(), "Blastoise")


    def test_custom_get_hp(self):
        """
        Tests if get_hp is able to correctly retreive the hp of a pokemon that has undergone the actions:
        Test 1: nothing (base hp)
        Test 2: lose 2 hp, heal
        Test 3: level up, lose 5 hp
        """
        p = Gastly()
        self.assertEqual(p.get_hp(), 6)

        p = Bulbasaur()
        p.lose_hp(2)
        p.heal()
        self.assertEqual(p.get_hp(), 13)

        p = Charmander()
        p.level_up()
        p.lose_hp(5)
        self.assertEqual(p.get_hp(), 5)


    def test_custom_get_level(self):
        """
        Tests if get_level is able to correctly retreive the level of a pokemon that has:
        Test 1: leveled up once 
        Test 2: at a base level 
        Test 3: levelled up multiple times 
        """
        p = Charmander()
        p.level_up()
        self.assertEqual(p.get_level(), 2)

        p = Squirtle()
        self.assertEqual(p.get_level(), 1)

        p = Eevee()
        p.level_up()
        p.level_up()
        p.level_up()
        p.level_up()
        p.level_up()
        p.level_up()
        self.assertEqual(p.get_level(), 7)


    def test_custom_str(self):
        """
        Tests if __str__ is able to correctly return a string representation of a pokemon that has undergone: 
        Test 1: base hp, base level 
        Test 2: lose 5 hp, base level 
        Test 3: level up, level up, level up, lose hp 3, lose hp 2
        """
        p = Charmander()
        self.assertEqual(p.__str__(), "LV. 1 Charmander: 9 HP")
        
        p = Blastoise()
        p.lose_hp(5)
        self.assertEqual(p.__str__(), "LV. 3 Blastoise: 16 HP")

        p = Eevee()
        p.level_up()
        p.level_up()
        p.level_up()
        p.lose_hp(3)
        p.lose_hp(2)
        self.assertEqual(p.__str__(), "LV. 4 Eevee: 5 HP")


    def test_custom_can_evolve(self):
        """
        Tests if can_evolve is able to correctly determine if a pokemon can evolve or not:
        Test 1: Charmander can further evolve.
        Test 2: Charizard cannot further evolve.
        Test 3: Blastoise cannot further evolve.
        """
        p = Charmander()
        self.assertEqual(p.can_evolve(), True)

        p = Charizard()
        self.assertEqual(p.can_evolve(), False)

        p = Blastoise()
        self.assertEqual(p.can_evolve(), False)


    def test_custom_clear_status_effect(self):
        """
        Tests if clear_status_effect is able to correctly clear the status effects of a pokemon: 
        Test 1: currently inflcited with "Burn"
        Test 2: currently inflicted with "Confusion"
        Test 3: with no status effects.
        """
        p = Charmander()
        p.status_effect = "Burn"
        p.clear_status_effects()
        self.assertEqual(p.status_effect, None)

        p = Eevee()
        p.status_effect = "Confusion"
        p.clear_status_effects()
        self.assertEqual(p.status_effect, None)

        p = Blastoise()
        p.status_effect = None
        p.clear_status_effects()
        self.assertEqual(p.status_effect, None)

    def test_custom_multiplier(self):
        """
        Test if the multiplier is able to correct return the multipler for two pokemon's attacking each other:
        Test 1: Grass attacks Fire 
        Test 2: Normal attacks Ghost
        Test 3: Ghost attacks Ghost 
        """
        p = Venusaur()
        q = Charmander()
        attack_mulitplier = PokeType(p.poke_type, q.poke_type)
        self.assertEqual(attack_mulitplier.multiplier(), 0.5)

        p = Eevee()
        q = Gastly()
        attack_mulitplier = PokeType(p.poke_type, q.poke_type)
        self.assertEqual(attack_mulitplier.multiplier(), 0)

        p = Gastly()
        q = Haunter()
        attack_mulitplier = PokeType(p.poke_type, q.poke_type)
        self.assertEqual(attack_mulitplier.multiplier(), 2)

        
