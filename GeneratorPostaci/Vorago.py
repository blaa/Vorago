# (C) 2008 by Tomasz bla Fortuna
# License: GNU GPLv2

import math

class Skill:
    def __init__(self, name, ability, weap = False, mod = False):
        self.name = name
        self.ability = ability
        self.mod = mod
        self.weap = weap

    def get_desc(self):
        if self.mod == False:
            mod = ""
        else:
            if self.mod > 0:
                mod = "+%d" % self.mod
            else:
                mod = "%d" % self.mod
        return "%s %s (%s)" % (self.name, mod, self.ability)


class Item:
    def __init__(self, name):
        self.name = name


class Weapon(Item):
    def __init__(self, name, attack, damage, is_range = False,
                 weapon_range = 0, skills = {}):
        self.name = name
        self.range = False		# False or range in meters
        self.skills = skills		# Skills modifying it's attack
        self.attack = attack
        self.damage = damage
        self.is_range = is_range
        self.weapon_range = weapon_range

    def get_desc(self):
        if self.attack > 0:
            attack = "+%d" % self.attack
        else:
            attack = self.attack

        if self.damage > 0:
            damage = "+%d" % self.damage
        else:
            damage = self.damage

        if self.is_range:
            weapon_range = " (%dm)" % self.weapon_range
        else:
            weapon_range = ""
        return "%s (%s/%s%s)" % (self.name, attack, damage, weapon_range)


class Armor(Item):
    def __init__(self, name, defense, damage, initiative):
        self.name = name
        self.defense = defense
        self.damage = damage
        self.initiative = initiative

    def get_desc(self):
        if self.defense > 0:
            defense = "+%d" % self.defense
        else:
            defense = self.defense

        if self.damage > 0:
            damage = "+%d" % self.damage
        else:
            damage = self.damage

        if self.initiative > 0:
            initiative = "+%d" % self.initiative
        else:
            initiative = self.initiative

        return "%s (%s/%s, %s)" % (self.name, defense, damage, initiative)


class World:
    def __init__(self):
        self.skills = {}
        self.weapons = {}
        self.armors = {}


    def add_skill(self, skill):
        name = skill.name
        if self.skills.has_key(name):
            raise KeyError, "Skill by that name already exists!"

        self.skills[name] = skill

    def add_weapon(self, weapon):
        name = weapon.name
        if self.is_weapon(name):
            raise KeyError, "Weapon by that name already exists!"
        self.weapons[name] = weapon

    def add_armor(self, armor):
        name = armor.name
        if self.is_armor(name):
            raise KeyError, "Armor by that name already exists!"
        self.armors[name] = armor

    def get_skill(self, name):
        try:
            return self.skills[name]
        except KeyError:
            raise KeyError, "No skill by that name in the database."

    def is_skill(self, name):
        return self.skills.has_key(name)

    def is_weapon(self, name):
        return self.weapons.has_key(name)

    def is_armor(self, name):
        return self.armors.has_key(name)

    def del_skill(self, name):
        try:
            self.skills.pop(name)
        except KeyError:
            raise KeyError, "No skill by that name in the database"

    def del_weapon(self, name):
        try:
            self.weapons.pop(name)
        except KeyError:
            raise KeyError, "No weapon by that name in the database"

    def del_armor(self, name):
        try:
            self.armors.pop(name)
        except KeyError:
            raise KeyError, "No armor by that name in the database"

    def export(self):
        all = "*** Vorago RPG *** \n"

        skills_txt = ""
        weapon_skills_txt = ""
        for skill in self.skills.values():
            if skill.weap:
                weapon_skills_txt += skill.get_desc() + "\n"
            else:
                skills_txt += skill.get_desc() + "\n"

        
        all += "Umiejetnosci:\n" + skills_txt
        all += "\nBieglosci:\n" + weapon_skills_txt

        # Weapons / Armors
        weapons_txt = ""
        range_weapons_txt = ""
        armors_txt = ""
        for weapon in self.weapons.values():
            tmp = weapon.get_desc()
            if weapon.is_range:
                range_weapons_txt += tmp + "\n"
            else:
                weapons_txt += tmp + "\n"

        for armor in self.armors.values():
            armors_txt += armor.get_desc() + "\n"

        all += "\nBronie:\n" + weapons_txt
        all += "\nZbroje:\n" + armors_txt
        return all

class Character:
    def __init__(self):
        self.Str = 0
        self.Dex = 0
        self.Con = 0
        self.Int = 0
        self.Wil = 0
        self.Cha = 0
        self.calc()

        self.Name = "Noname"
        self.Race = "Norace"
        self.Comment = "Nocomment"
        self.skills = {}
        self.weapons = {}
        self.armors = {}

    def avg(self, fst, snd):
        avg = (fst + snd) / 2.0
        if fst > snd:
            return math.ceil(avg)
        else:
            return math.floor(avg)
    
        
        return (fst + snd) / 2
    
    def calc(self):
        self.A = self.avg(self.Str, self.Dex)
        self.M = self.avg(self.Dex, self.Int)
        self.D = self.avg(self.Dex, self.Con)
        self.P = self.avg(self.Wil, self.Int)
        self.R = self.avg(self.Wil, self.Con)

        self.HP = 2 * self.Con + 20
        self.MP = 2 * self.P + 20
        self.I = self.Dex
        self.HC = self.Con

    def attr_by_name(self, name):
        if name == "Sf" or name == "Str":
            return self.Str
        elif name == "Zr" or name == "Dex":
            return self.Dex
        elif name == "Zw" or name == "Con":
            return self.Con
        elif name == "Pr" or name == "Int":
            return self.Int
        elif name == "Sw" or name == "Wil":
            return self.Wil
        elif name == "Ch" or name == "Cha":
            return self.Cha
        elif name == "A":
            return self.A
        elif name == "M":
            return self.M
        elif name == "D":
            return self.D
        elif name == "P":
            return self.P
        elif name == "R":
            return self.R
        elif name == "HP":
            return self.HP
        elif name == "MP":
            return self.MP
        elif name == "I":
            return self.I
        elif name == "HC":
            return self.HC


    def export(self):
        intro = "*** Karta postaci, Vorago RPG *** \n"
        intro += "Imie: %s Rasa: %s\nKomentarz: %s\n" % (self.Name, self.Race, self.Comment)
        coeffs  = "Sf: %d\tA: %d\tPZ: %d\n" % (self.Str, self.A, self.HP)
        coeffs += "Zr: %d\tM: %d\tPM: %d\n" % (self.Dex, self.M, self.MP)
        coeffs += "Zw: %d\tD: %d\tI: %d\n" % (self.Con, self.D, self.I)
        coeffs += "Pr: %d\tP: %d\tWsp. Zdr.: %d\n" % (self.Int, self.P, self.HC)
        coeffs += "Sw: %d\tR: %d\n" % (self.Wil, self.R)
        coeffs += "Ch: %d\n" % (self.Cha)
        coeffs += "\n\n"

        skills_txt = ""
        weapskills = ""
        for skill in self.skills.values():
            if skill.weap:
                weapskills += skill.get_desc() + "\n"
            else:
                ability = self.attr_by_name(skill.ability) + skill.mod
                skills_txt += skill.get_desc() + " (%c = %d)\n" % \
                              (skill.ability, ability)
            
        all = intro + coeffs
        all += "Umiejetnosci postaci:\n" + skills_txt
        all += "\nBieglosci postaci:\n" + weapskills

        # Weapons / Armors
        weapons_txt = ""
        armors_txt = ""
        for weapon in self.weapons.values():
            tmp = weapon.get_desc()
            attack = weapon.attack
            for skill in weapon.skills.values():
                if skill in self.skills.values():
                    attack += skill.mod
            if weapon.is_range:
                attack_final = attack + self.M
                coeff = "M"
            else:
                attack_final = attack + self.A
                coeff = "A"
                
            if attack > 0:
                attack = "+%d" % attack
            else:
                attack = "%d" % attack
                
            weapons_txt += tmp + " (mod. %c=%s; %c=%d) \n" % \
                           (coeff, attack, coeff, attack_final)

        final_D = self.D
        final_I = self.I
        for armor in self.armors.values():
            tmp = armor.get_desc()
            tmp += ", (D=%d, I=%d)" % (self.D + armor.defense, self.I + armor.initiative)
            final_D += armor.defense
            final_I += armor.initiative
            armors_txt += tmp + "\n"

        all += "\nBron postaci:\n" + weapons_txt
        all += "\nZbroja postaci:\n" + armors_txt
        return all
