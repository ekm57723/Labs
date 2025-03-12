from abc import ABC, abstractmethod
from fileinput import filename
import json

#Parent class Item
class Item:
    def __init__(self, name, description="", rarity="common"):
        self.name = name
        self.description = description
        self.rarity = rarity
        self._ownership = None
    
    def pick_up(self, character: str):
        self._ownership = character
        return f"{self.name} is now owned by {character}"
    
    def throw_away(self):
        self._ownership = None
        return f"{self.name} is thrown away"
    
    def use(self):
        if not self._ownership:
            return ""
        return f"{self.name} is used"
    
    def __str__(self):
        return f"{self.name} ({self.rarity}): {self.description}"
    
    def to_json(self):
        """Returns a JSON-encodable dictionary representation of the item."""
        return {
            "type": self.__class__.__name__,
            "name": self.name,
            "description": self.description,
            "rarity": self.rarity,
            "ownership": self._ownership
        }

    @classmethod
    def from_json(cls, data):
        """Creates an instance from a JSON dictionary."""
        obj = cls(data["name"], data["description"], data["rarity"])
        obj._ownership = data["ownership"]
        return obj

#Weapon class
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
    
    def __str__(self):
        base_string = f"{self.name} ({self.rarity}): {self.description}"
        return base_string
    
    @staticmethod
    def get_weapon_description(weapon_type, damage):
        descriptions = {
            "bow": f"A ranged weapon that allows for precise long-distance attacks. Deals {damage} base damage.",
            "sword": f"A balanced melee weapon favored by warriors. Slashes enemies with {damage} base damage.",
            "axe": f"A heavy-hitting weapon capable of cleaving through armor. Delivers {damage} base damage.",
            "hammer": f"A devastating blunt weapon that crushes foes with {damage} base damage."
        }
        return descriptions.get(weapon_type, "A mysterious weapon of unknown origin.")
    
    def to_json(self):
        data = super().to_json()
        data.update({
            "damage": self.damage,
            "weapon_type": self.weapon_type,
            "active": self.active,
            "attack_modifier": self.attack_modifier
        })
        return data

    @classmethod
    def from_json(cls, data):
        weapon = super().from_json(data)
        weapon.damage = data["damage"]
        weapon.weapon_type = data["weapon_type"]
        weapon.active = data["active"]
        weapon.attack_modifier = data["attack_modifier"]
        return weapon

#Shield class
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
        if not self._ownership:
            return ""
        self.active = True
        return f"{self.name} is equipped by {self._ownership}"

    def use(self):
        if not self._ownership or not self.active:
            return ""
        block_power = self.defense * self.defense_modifier * (0.5 if self.broken else 1)
        return f"{self._ownership} used {self.name} ({self.rarity}): {self.description} Blocks {block_power} damage."

    def __str__(self):
        return f"{self.name} ({self.rarity})"
    
    @staticmethod
    def get_shield_description(shield_type):
        descriptions = {
            "Cast Iron": "A sturdy iron shield, reliable in battle.",
            "Trash Can Lid": "A makeshift shield, surprisingly effective.",
            "Wooden Lid": "A lightweight shield for quick defense.",
            "Steel Shield": "A well-crafted shield offering excellent protection."
        }
        return descriptions.get(shield_type, "A mysterious shield of unknown origin.")
    
    def to_json(self):
        data = super().to_json()
        data.update({
            "defense": self.defense,
            "broken": self.broken,
            "shield_type": self.shield_type,
            "defense_modifier": self.defense_modifier
        })
        return data

    @classmethod
    def from_json(cls, data):
        shield = super().from_json(data)
        shield.defense = data["defense"]
        shield.broken = data["broken"]
        shield.shield_type = data["shield_type"]
        shield.defense_modifier = data["defense_modifier"]
        return shield

#Potion class
class Potion(Item):
    def __init__(self, name, potion_type, value, effective_time=0, rarity='common'):
        description = Potion.get_potion_description(potion_type, value)
        super().__init__(name, description, rarity)
        self.potion_type = potion_type
        self.value = value
        self.effective_time = effective_time
        self.used = False

    def use(self):
        if not self._ownership or self.used:
            return ""
        self.used = True
        return f"{self._ownership} used {self.name} ({self.rarity})."

    def __str__(self):
        base_string = f"{self.name} ({self.rarity}): {self.description}"
        return base_string
    
    @staticmethod
    def get_potion_description(potion_type, value):
        descriptions = {
            "attack": f"Increases attack power by {value}",
            "defense": f"Boosts defense by {value}",
            "HP": f"Restores {value} health instantly"
        }
        return descriptions.get(potion_type, "A mysterious potion of unknown effect.")

    def to_json(self):
        data = super().to_json()
        data.update({
            "potion_type": self.potion_type,
            "value": self.value,
            "effective_time": self.effective_time,
            "used": self.used
        })
        return data

    @classmethod
    def from_json(cls, data):
        potion = super().from_json(data)
        potion.potion_type = data["potion_type"]
        potion.value = data["value"]
        potion.effective_time = data["effective_time"]
        potion.used = data["used"]
        return potion

#Inventory class
class Inventory:

    """
    Represents the player's inventory containing a collection of items.

    The serialized JSON structure for the Inventory object is as follows:

    {
        "owner": "Player Name",
        "items": [
            {
                "type": "ItemType",  # The class name of the item (e.g., "Weapon", "Potion")
                "name": "Item Name",
                "description": "Item Description",
                "rarity": "Item Rarity",
                "ownership": "Player Name or None",  # Ownership is either the player's name or None if not owned
                # Item-specific attributes (e.g., damage, value, etc.) would follow based on the item type
            },
            # Additional items here
        ]
    }

    Each item is represented as a dictionary containing the type (class name), basic attributes (name, description, rarity), 
    and additional class-specific attributes.
    """
    
    def __init__(self, owner=None):
        self.owner = owner
        self.items = []
    
    def add_item(self, item):
        item.pick_up(self.owner)
        self.items.append(item)
    
    def drop_item(self, item):
        if item in self.items:
            item.throw_away()
            self.items.remove(item)
    
    def view(self, item_type=None):
        if item_type:
            return [str(item) for item in self.items if isinstance(item, item_type)]
        return [str(item) for item in self.items]
    
    def __iter__(self):
        return iter(self.items)
    
    def __contains__(self, item):
        return item in self.items

    def to_json(self):
        return {
            "owner": self.owner,
            "items": [item.to_json() for item in self.items]
        }
    
    @classmethod
    def from_json(cls, data):
        inventory = cls(data["owner"])
        inventory.items = [globals()[item_data["type"]].from_json(item_data) for item_data in data["items"]]
        return inventory

    def save_inventory(self, filename="inventory.json"):
        """
        Saves the inventory to a JSON file.
    
        Parameters:
            filename: Name of the file to save to.
        """
        with open(filename, "w") as f:
            json.dump(self.to_json(), f, indent=4)
    
#ABC for weapons
class Weapon(Item, ABC):
    def __init__(self, name, damage, rarity="common"):
        super().__init__(name, rarity=rarity)
        self.damage = damage
        self.active = False
        self.attack_modifier = 1.15 if rarity == "legendary" else 1.0
    
    @abstractmethod
    def attack_move(self):
        pass
    
    def equip(self):
        self.active = True
        return f"{self.name} is equipped by {self._ownership}"
    
    def use(self):
        if not self._ownership or not self.active:
            return ""
        attack_power = self.damage * self.attack_modifier
        return f"{self._ownership} {self.attack_move()} using {self.name}. Deals {attack_power} damage."

#Subclasses for different weapon types
class SingleHandedWeapon(Weapon):
    def attack_move(self):
        return "slashes"

class DoubleHandedWeapon(Weapon):
    def attack_move(self):
        return "spins"

class Pike(Weapon):
    def attack_move(self):
        return "thrusts"

class RangedWeapon(Weapon):
    def attack_move(self):
        return "shoots"

#Shield class
class Shield(Item):
    def __init__(self, name, defense, broken=False, shield_type="", rarity="common"):
        super().__init__(name, rarity=rarity)
        self.defense = defense
        self.broken = broken
        self.active = False
        self.shield_type = shield_type
        self.defense_modifier = 1.10 if rarity == "legendary" else 1.0

    def equip(self):
        if not self._ownership:
            return ""
        self.active = True
        return f"{self.name} is equipped by {self._ownership}"

    def use(self):
        if not self._ownership or not self.active:
            return ""  
        block_power = self.defense * self.defense_modifier * (0.5 if self.broken else 1)
        return f"{self._ownership} used {self.name} ({self.rarity}). Blocks {block_power} damage."

#Potion class
class Potion(Item):
    def __init__(self, name, potion_type, value, effective_time=0, rarity='common'):
        description = Potion.get_potion_description(potion_type, value)  # Call the static method via the class
        super().__init__(name, description, rarity)
        self.potion_type = potion_type
        self.value = value
        self.effective_time = effective_time
        self.used = False

    def use(self):
        if not self._ownership or self.used:
            return ""
        self.used = True

        if self.potion_type == "HP":
            return f"{self._ownership} used {self.name}. Restores {self.value} health instantly."
        
        return f"{self._ownership} used {self.name} ({self.rarity}). {self.description} Lasts for {self.effective_time} seconds."

    @classmethod
    def from_ability(cls, name, owner, potion_type, value=50, effective_time=30, rarity='common'):
        potion = cls(name, potion_type, value, effective_time, rarity)
        potion._ownership = owner
        return potion

    @staticmethod
    def get_potion_description(potion_type, value):
        """Generate appropriate description based on potion type."""
        descriptions = {
            "attack": f"Increases attack power by {value}",
            "defense": f"Boosts defense by {value}",
            "HP": f"Restores {value} health instantly"
        }
        return descriptions.get(potion_type, "A mysterious potion of unknown effect.")

#Inventory system
class Inventory:
    def __init__(self, owner=None):
        self.owner = owner
        self.items = []
    
    def add_item(self, item: Item):
        item.pick_up(self.owner)
        self.items.append(item)
    
    def drop_item(self, item: Item):
        if item in self.items:
            item.throw_away()
            self.items.remove(item)
    
    def view(self, item_type=None):
        if item_type:
            return [str(item) for item in self.items if isinstance(item, item_type)]
        return [str(item) for item in self.items]
    
    def __iter__(self):
        return iter(self.items)
    
    def __contains__(self, item):
        return item in self.items

#Example usage for Mr. Beleg as per lab 05 instructions
beleg_backpack = Inventory(owner="Beleg")

beleg_backpack.save_inventory("beleg_inventory.json")

#To load inventory from the file
with open("beleg_inventory.json", "r") as f:
    data = json.load(f)
    loaded_inventory = Inventory.from_json(data)

#Adding weapons
master_sword = SingleHandedWeapon("Master Sword", 300, "legendary")
muramasa = DoubleHandedWeapon("Muramasa", 580, "legendary")
beleg_backpack.add_item(master_sword)
beleg_backpack.add_item(muramasa)

#Adding shields
steel_shield = Shield(name="Steel Shield", defense=125, rarity="legendary")
cast_iron_shield = Shield(name="Cast Iron Shield", defense=100, rarity="epic")
beleg_backpack.add_item(steel_shield)
beleg_backpack.add_item(cast_iron_shield)

#Adding potions
healing_potion = Potion(name="Healing Potion", potion_type="HP", value=50, rarity="common")
attack_potion = Potion(name="Attack Boost Potion", potion_type="attack", value=30, rarity="rare")
beleg_backpack.add_item(healing_potion)
beleg_backpack.add_item(attack_potion)

if master_sword in beleg_backpack:
    master_sword.equip()
    print(master_sword)
    master_sword.use()

#Creating an inventory
beleg_backpack = Inventory(owner="Beleg")

#Adding and using weapons
master_sword = SingleHandedWeapon("Master Sword", 300, "legendary")
beleg_backpack.add_item(master_sword)
print(master_sword.equip()) 
print(master_sword.use())

#Adding and using shields
steel_shield = Shield(name="Steel Shield", defense=125, rarity="legendary")
beleg_backpack.add_item(steel_shield)
print(steel_shield.equip())  
print(steel_shield.use())   

#Adding and using potions
healing_potion = Potion(name="Healing Potion", potion_type="HP", value=50, rarity="common")
beleg_backpack.add_item(healing_potion)
print(healing_potion.use())  # Use potion

#Viewing inventory by type
print("All shields in Beleg's inventory:")
for item in beleg_backpack.view(Shield):
    print(item)

print("\nAll weapons in Beleg's inventory:")
for item in beleg_backpack.view(Weapon):
    print(item)

print("\nAll potions in Beleg's inventory:")
for item in beleg_backpack.view(Potion):
    print(item)

#Dropping an item
beleg_backpack.drop_item(steel_shield)
print("\nAfter dropping Steel Shield:")
for item in beleg_backpack.view(Shield):
    print(item)

#Examples of everything else
axe = SingleHandedWeapon(name='Axe', damage=3000, rarity='uncommon')
print(axe.pick_up('Emily'))
print(axe.equip())
print(axe.use())
print(axe.throw_away())
print(axe.use())

sword = SingleHandedWeapon(name='Sword', damage=5000, rarity='epic')
print(sword.pick_up('AJ'))
print(sword.equip())
print(sword.use())
print(sword.throw_away())
print(sword.use())

hammer = DoubleHandedWeapon(name='Hammer', damage=1000, rarity='common')
print(hammer.pick_up('Matthew'))
print(hammer.equip())
print(hammer.use())
print(hammer.throw_away())
print(hammer.use())

bow = RangedWeapon(name='Bow', damage=5000, rarity='legendary')
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

hp_potion = Potion(name="Healing Potion", potion_type="HP", value=50, rarity="common")
hp_potion = Potion.from_ability(hp_potion, owner='Emily', potion_type='HP')
print(hp_potion.use())
print(hp_potion.use())

attack_potion = Potion.from_ability(attack_potion, owner = 'AJ', potion_type = 'attack')
print(attack_potion.use())
print(attack_potion.use())

defense_potion = Potion(name="Defense Potion", potion_type="defense", value=30, rarity="common")
defense_potion = Potion.from_ability(defense_potion, owner = 'Matthew', potion_type = 'defense')
print(defense_potion.use())
print(defense_potion.use())

print(isinstance(attack_potion, Weapon)) #False
print(isinstance(axe, Potion)) #False
print(isinstance(steel_shield, Shield)) #True
print(isinstance(hp_potion, Potion)) #True
print(isinstance(wooden_lid, Item)) #True