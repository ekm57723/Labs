#Parent class Item
class Item:
    def __init__(self, name, description="", rarity="common"):
        self.name = name
        self.description = description
        self.rarity = rarity
        self._ownership = ""
    
    def pick_up(self, character: str):
        self._ownership = character
        return f"{self.name} is now owned by {character}"
    
    def throw_away(self):
        self._ownership = ""
        return f"{self.name} is thrown away"
    
    def use(self):
        if not self._ownership:
            return ""
        return f"{self.name} is used"
    
    def __str__(self):
        return f"{self.name} ({self.rarity}): {self.description}"

#Child class Weapon, inherits characteristics from parent class Item
class Weapon(Item):
    def __init__(self, name, damage, weapon_type, rarity="common"):
        description = self.get_weapon_description(weapon_type, damage)
        super().__init__(name, description, rarity)
        self.damage = damage
        self.weapon_type = weapon_type
        self.active = False
        self.attack_modifier = 1.15 if rarity == "legendary" else 1.0
    
    def equip(self):
        self.active = True
        return f"{self.name} is equipped by {self._ownership}"
    
    def use(self):
        if not self._ownership or not self.active:
            return ""
        attack_power = self.damage * self.attack_modifier
        return f"{self._ownership} used {self.name} ({self.rarity}): {self.description} Deals {attack_power} damage."
    
    #Weapon descriptions
    @staticmethod
    def get_weapon_description(weapon_type, damage):
        """Generate appropriate description based on weapon type."""
        descriptions = {
            "bow": f"A ranged weapon that allows for precise long-distance attacks. Deals {damage} base damage.",
            "sword": f"A balanced melee weapon favored by warriors. Slashes enemies with {damage} base damage.",
            "axe": f"A heavy-hitting weapon capable of cleaving through armor. Delivers {damage} base damage.",
            "hammer": f"A devastating blunt weapon that crushes foes with {damage} base damage."
        }
        return descriptions.get(weapon_type, "A mysterious weapon of unknown origin.")
    
#Child class Shield, inherits characteristics from parent class Item
class Shield(Item):
    def __init__(self, name, defense, broken=False, shield_type="", rarity="common"):
        description = self.get_shield_description(shield_type)
        super().__init__(name, description, rarity)  
        self.defense = defense
        self.broken = broken
        self.active = False
        self.shield_type = shield_type
        self.defense_modifier = 1.10 if rarity == "legendary" else 1.0

    def equip(self):
        if not self._ownership:  #need owner to equip
            return ""
        self.active = True
        return f"{self.name} is equipped by {self._ownership}"

    def use(self):
        if not self._ownership or not self.active:
            return ""  
        block_power = self.defense * self.defense_modifier * (0.5 if self.broken else 1)
        return f"{self._ownership} used {self.name} ({self.rarity}): {self.description} Blocks {block_power} damage."

    def throw_away(self):
        self._ownership = ""  
        self.active = False 
        return f"{self.name} is thrown away"

    def __str__(self):
        return f"{self.name} ({self.rarity})"

    #Shield descriptions
    @staticmethod
    def get_shield_description(shield_type):
        """Generate appropriate description based on shield type."""
        descriptions = {
            "Cast Iron": "A sturdy iron shield, reliable in battle. Though simple, it provides solid protection against incoming attacks.",
            "Trash Can Lid": "A makeshift shield, surprisingly effective in a pinch. Offers decent defense but is not designed for prolonged battles.",
            "Wooden Lid": "A lightweight shield that offers basic protection. Best suited for quick movements and agility-based defense.",
            "Steel Shield": "A strong and well-crafted shield, offering excellent protection against powerful attacks."
        }
        return descriptions.get(shield_type, "A mysterious shield of unknown origin.")

#Child class Potion, inherits characteristics from parent class Item
class Potion(Item):
    def __init__(self, name, potion_type, value, effective_time=0, rarity='common'):
        super().__init__(name, self.get_potion_description(potion_type, value), rarity)
        self.potion_type = potion_type
        self.value = value
        self.effective_time = effective_time
        self.used = False

    def use(self):
        if not self._ownership or self.used:
            return ""
        self.used = True

        if self.potion_type == "HP":
            return f"{self._ownership} used {self.name}."
        
        return f"{self._ownership} used {self.name} for {self.effective_time}s."

    @classmethod
    def from_ability(cls, name, owner, potion_type):
        potion = cls(name, potion_type, 50, 30, 'common')
        potion._ownership = owner
        return potion
    
    #Potion descriptions
    @staticmethod
    def get_potion_description(potion_type, value):
        """Generate appropriate description based on potion type."""
        descriptions = {
            "attack": f"Increases attack power by {value}",
            "defense": f"Boosts defense by {value}",
            "HP": f"Restores {value} health instantly"
        }
        return descriptions.get(potion_type)

#Potions
attack_potion = Potion(name='Mighty Strike Elixir', potion_type='attack', value=50, effective_time=30, rarity='epic')
defense_potion = Potion(name='Shielding Brew', potion_type='defense', value=25, effective_time=25, rarity='rare')
hp_potion = Potion(name='Healing Tonic', potion_type='HP', value=50, effective_time=0, rarity='common')


#Examples of everything
axe = Weapon(name = 'axe', damage = 3000, weapon_type = 'axe', rarity = 'uncommon')
print(axe.pick_up('Emily'))
print(axe.equip())
print(axe.use())
print(axe.throw_away())
print(axe.use())  

sword = Weapon(name = 'sword', damage = 5000, weapon_type = 'sword', rarity = 'epic')
print(sword.pick_up('AJ'))
print(sword.equip())
print(sword.use())
print(sword.throw_away())
print(sword.use())  

hammer = Weapon(name = 'hammer', damage = 1000, weapon_type = 'hammer', rarity = 'common')
print(hammer.pick_up('Matthew'))
print(hammer.equip())
print(hammer.use())
print(hammer.throw_away())
print(hammer.use())  

bow = Weapon(name = 'bow', damage = 5000, weapon_type = 'bow', rarity = 'legendary')
print(bow.pick_up('Emily'))
print(bow.equip())
print(bow.use())
print(bow.throw_away())
print(bow.use())  

cast_iron = Shield(name = 'Cast Iron', defense = 100, broken = False, shield_type = 'Cast Iron', rarity = 'epic')
print(cast_iron.pick_up('AJ'))
print(cast_iron.equip())
print(cast_iron.use())
print(cast_iron.throw_away())
print(cast_iron.use())

trash_can_lid = Shield(name = 'Trash Can Lid', defense = 75, broken = False, shield_type = 'Trash Can Lid', rarity = 'uncommon')
print(trash_can_lid.pick_up('Matthew'))
print(trash_can_lid.equip())
print(trash_can_lid.use())
print(trash_can_lid.throw_away())
print(trash_can_lid.use())  

wooden_lid = Shield(name = 'Wooden Lid', defense = 25, broken = False, shield_type = 'Wooden Lid', rarity = 'common')
print(wooden_lid.pick_up('Matthew'))
print(wooden_lid.equip())
print(wooden_lid.use())
print(wooden_lid.throw_away())
print(wooden_lid.use())  

steel_shield = Shield(name = 'Steel Shield', defense = 125, broken = False, shield_type = 'Steel Shield', rarity = 'legendary')
print(steel_shield.pick_up('AJ'))
print(steel_shield.equip())
print(steel_shield.use())
print(steel_shield.throw_away())
print(steel_shield.use())  

hp_potion = Potion.from_ability(hp_potion, owner = 'Emily', potion_type = 'HP')
print(hp_potion.use())
print(hp_potion.use())

attack_potion = Potion.from_ability(attack_potion, owner = 'AJ', potion_type = 'attack')
print(attack_potion.use())
print(attack_potion.use())

defense_potion = Potion.from_ability(defense_potion, owner = 'Matthew', potion_type = 'defense')
print(defense_potion.use())
print(defense_potion.use())

print(isinstance(attack_potion, Weapon)) #False
print(isinstance(axe, Potion)) #False
print(isinstance(steel_shield, Shield)) #True
print(isinstance(hp_potion, Potion)) #True
print(isinstance(wooden_lid, Item)) #True