#!/usr/bin/python
# -*- coding: utf-8 -*-

# (C) 2008 by Tomasz bla Fortuna
# License: GNU GPLv2


from PyQt4 import QtCore, QtGui
import GUI

import Vorago
import random
import pickle

ch = Vorago.Character()
world = Vorago.World()

class SkillManager:
    def __init__(self, ui, sk_update = False):
        self.ui = ui
        self.sk_update = sk_update # function to be called when new skills arrive
        self.update_lock = False

    def new_skill_add(self):
        name = ui.NewSkillName.text()
        ability = ui.NewSkillAbility.currentText()
        is_weap = ui.NewSkillCond.isChecked()
        skill = Vorago.Skill(name, ability, is_weap)
        
        # Check if exists
        if world.is_skill(name):
            ui.Status.setText("Blad: Umiejetnosc o tej nazwie juz istnieje.")
        else:
            # It doesn't; add it.
            world.add_skill(skill)
            self.skill_update()

    def new_skill_select(self, name):
        if name == "":
            return
        skill = world.get_skill(name)
        if skill.weap:
            ui.NewSkillCond.setChecked(True)
        else:
            ui.NewSkillCond.setChecked(False)

        idx = ui.NewSkillAbility.findText(skill.ability)
        ui.NewSkillAbility.setCurrentIndex(idx)
        ui.NewSkillName.setText(skill.name)

    def new_skill_del(self):
        skill = ui.NewSkillList.currentItem()
        if not skill:
            self.ui.Status.setText("Blad: Umiejetnosc do usuniecia nie zaznaczona")
            return
        name = skill.text()
        # if the player has it added -- error
        if ch.skills.has_key(name):
            # he has
            ui.Status.setText("Blad: W pierwszej kolejnosci usun ta umiejetnosc postaci.")
        else:
            # He hasn't; Remove the skill
            world.del_skill(name)
            self.skill_update()

    def skill_update(self):
        "Update NewSkill menu from the world object"
        ui.NewSkillList.clear()
        ui.SkillList.clear()
        ui.SkillAdded.clear()

        for item in world.skills:
            name = world.skills[item].name
            ui.NewSkillList.addItem(name)
            # Check if character has this skill
            if not ch.skills.has_key(name):
                # and if not add to second list.
                ui.SkillList.addItem(name)
            else:
                # if is, add to player skill list.
                ui.SkillAdded.addItem(name)

        if self.sk_update:
            self.sk_update()


    # Character skill functions
    def skill_add(self):
        item = ui.SkillList.currentItem()
        if not item:
            self.ui.Status.setText("Blad: Umiejetnosc do dodania nie zaznaczona")
            return
        name = item.text()

        # Exists for sure and for sure is not on character list.
        skill = world.get_skill(name)
        ch.skills[name] = skill
        ch.skills[name].mod = self.ui.SkillMod.value()
        self.skill_update()
        self.ui.Status.setText("OK")


    def skill_del(self):
        item = ui.SkillAdded.currentItem()
        if not item:
            self.ui.Status.setText("Blad: Umiejetnosc do usuniecia nie zaznaczona")
            return
            
        name = item.text()
        ch.skills.pop(name)
        self.skill_update()
        self.ui.Status.setText("OK")

    
    def skill_select(self, name):
        "Updates modifier info"
        if name == "":
            return
        skill = ch.skills[name]
        self.ui.SkillMod.setValue(int(skill.mod))

        
class ItemManager:
    def __init__(self, ui):
        self.ui = ui
        self.weapon_selected_skills = {}

    ##
    # Weapon functions
    ##
    def new_weapon_add(self):
        # Collect data; add to world, call update.
        name = self.ui.NewWeaponName.text()
        attack = self.ui.NewWeaponHit.value()
        damage = self.ui.NewWeaponDamage.value()
        is_range = self.ui.NewWeaponRange.isEnabled()
        if is_range:
            weapon_range = self.ui.NewWeaponRange.value()
        else:
            weapon_range = 0

        if world.is_weapon(name):
            ui.Status.setText("Blad: Taka bron juz istnieje")
        else:
            weapon = Vorago.Weapon(name, attack, damage, is_range, weapon_range,
                                   self.weapon_selected_skills.copy())
            world.add_weapon(weapon)
            self.weapon_update()
            ui.Status.setText("OK")

    
    def new_weapon_del(self):
        weaponit = self.ui.NewWeaponList.currentItem()
        if not weaponit:
            self.ui.Status.setText("Blad: Bron do usuniecia nie zaznaczona")
            return
        name = weaponit.text()

        if ch.weapons.has_key(name):
            self.ui.Status.setText("Blad: Bron wymagana przez postac")
            return

        world.del_weapon(name)
        self.weapon_update()
        ui.Status.setText("OK")


    def new_weapon_select(self, name):
        if name == "":
            return
        
        weapon = world.weapons[name]
        self.ui.NewWeaponName.setText(weapon.name)
        self.ui.NewWeaponHit.setValue(int(weapon.attack))
        self.ui.NewWeaponDamage.setValue(int(weapon.damage))
        if weapon.is_range:
            self.ui.NewWeaponIsRange.setChecked(True)
            self.ui.NewWeaponRange.setValue(int(weapon.weapon_range))
        else:
            self.ui.NewWeaponIsRange.setChecked(False)
            self.ui.NewWeaponRange.setValue(0)

        # Skills
        self.weapon_selected_skills = weapon.skills.copy()
        self.weapon_update(skills_only = True)

    def new_weapon_skill_add(self):
        skill = self.ui.NewWeaponSkills.currentText()
        if skill == "":
            ui.Status.setText("Blad: Brak bieglosci")
            return
        
        self.weapon_selected_skills[skill] = world.skills[skill]
        self.weapon_update()
        ui.Status.setText("OK")
    
    def new_weapon_skill_del(self):
        skill = self.ui.NewWeaponSkillsAdded.currentItem()
        
        if not skill:
            ui.Status.setText("Blad: Umiejetnosc nie zaznaczona")
            return
        
        skill = skill.text()
        self.weapon_selected_skills.pop(skill)
        self.weapon_update()
        ui.Status.setText("OK")

    
    def weapon_update(self, skills_only = False):
        "Update UI menus with world data"
        self.ui.NewWeaponSkillsAdded.clear()
        self.ui.NewWeaponSkills.clear()

        if not skills_only:
            self.ui.NewWeaponList.clear()
            self.ui.WeaponAdded.clear()
            self.ui.WeaponList.clear()

            for item in world.weapons:
                name = world.weapons[item].name
                self.ui.NewWeaponList.addItem(name)
                # Check if character has this weapon
                if not ch.weapons.has_key(name):
                    # and if not add to second list.
                    self.ui.WeaponList.addItem(name)
                else:
                    # if is, add to player skill list.
                    self.ui.WeaponAdded.addItem(name)

        # Add skills to combobox, which are not in
        # weapon_selected_kills
        for skill in world.skills.values():
            if not skill.weap:
                continue
            if skill.name in self.weapon_selected_skills:
                self.ui.NewWeaponSkillsAdded.addItem(skill.name)
            else:
                self.ui.NewWeaponSkills.addItem(skill.name)

    ##
    # Armor functions
    ##
    def new_armor_add(self):
        # Collect data; add to world, call update.
        name = self.ui.NewArmorName.text()
        defense = self.ui.NewArmorDefense.value()
        damage = self.ui.NewArmorDamage.value()
        initiative = self.ui.NewArmorInitiative.value()

        if world.is_armor(name):
            ui.Status.setText("Blad: Taka zbroja juz istnieje")
        else:
            armor = Vorago.Armor(name, defense, damage, initiative)
            world.add_armor(armor)
            self.armor_update()
            ui.Status.setText("OK")

    
    def new_armor_del(self):
        armorit = self.ui.NewArmorList.currentItem()
        if not armorit:
            self.ui.Status.setText("Blad: Zbroja do usuniecia nie zaznaczona")
            return
        name = armorit.text()

        if ch.armors.has_key(name):
            self.ui.Status.setText("Blad: Zbroja wymagana przez postac")
            return

        world.del_armor(name)
        self.armor_update()
        ui.Status.setText("OK")

    def new_armor_select(self, name):
        if name == "":
            return
        
        armor = world.armors[name]
        self.ui.NewArmorName.setText(armor.name)
        self.ui.NewArmorDefense.setValue(int(armor.defense))
        self.ui.NewArmorDamage.setValue(int(armor.damage))
        self.ui.NewArmorInitiative.setValue(int(armor.initiative))

    def armor_update(self):
        "Update UI menus with world data"
        self.ui.NewArmorList.clear()
        self.ui.ArmorAdded.clear()
        self.ui.ArmorList.clear()

        for item in world.armors:
            name = world.armors[item].name
            self.ui.NewArmorList.addItem(name)
            # Check if character has this armor
            if not ch.armors.has_key(name):
                # and if not add to second list.
                self.ui.ArmorList.addItem(name)
            else:
                self.ui.ArmorAdded.addItem(name)

    ##
    # Player armor/weapon
    ##
    def weapon_add(self):
        item = ui.WeaponList.currentItem()
        if not item:
            self.ui.Status.setText("Blad: Bron nie zaznaczona")
            return
        name = item.text()

        ch.weapons[name] = world.weapons[name]
        self.weapon_update()
        ui.Status.setText("OK")
    
    def weapon_del(self):
        item = ui.WeaponAdded.currentItem()
        if not item:
            self.ui.Status.setText("Blad: Bron do usuniecia nie zaznaczona")
            return
        name = item.text()
        ch.weapons.pop(name)
        self.weapon_update()
        ui.Status.setText("OK")
                
    def armor_add(self):
        item = ui.ArmorList.currentItem()
        if not item:
            self.ui.Status.setText("Blad: Zbroja nie zaznaczona")
            return
        name = item.text()

        ch.armors[name] = world.armors[name]
        self.armor_update()
        ui.Status.setText("OK")
    
    def armor_del(self):
        item = ui.ArmorAdded.currentItem()
        if not item:
            self.ui.Status.setText("Blad: Zbroja do usuniecia nie zaznaczona")
            return
        name = item.text()
        ch.armors.pop(name)
        self.armor_update()
        ui.Status.setText("OK")

        

class Manager:
    def __init__(self, ui):

        self.ui = ui
        self.signal_enabled = True

        self.item_manager = ItemManager(self.ui)
        self.skill_manager = SkillManager(self.ui, self.item_manager.weapon_update)

        try:
            self.load_state_from("default.vorago")
        except IOError:
            pass

        # Main page support.
        QtCore.QObject.connect(ui.Str, QtCore.SIGNAL("valueChanged(int)"), self.update_character)
        QtCore.QObject.connect(ui.Dex, QtCore.SIGNAL("valueChanged(int)"), self.update_character)
        QtCore.QObject.connect(ui.Con, QtCore.SIGNAL("valueChanged(int)"), self.update_character)
        QtCore.QObject.connect(ui.Int, QtCore.SIGNAL("valueChanged(int)"), self.update_character)
        QtCore.QObject.connect(ui.Wil, QtCore.SIGNAL("valueChanged(int)"), self.update_character)
        QtCore.QObject.connect(ui.Cha, QtCore.SIGNAL("valueChanged(int)"), self.update_character)

        QtCore.QObject.connect(ui.rand_KV, QtCore.SIGNAL("clicked()"), self.Rand_KV)
        QtCore.QObject.connect(ui.rand_2K6_4, QtCore.SIGNAL("clicked()"), self.Rand_2K6_4)
        QtCore.QObject.connect(ui.rand_2K6_6, QtCore.SIGNAL("clicked()"), self.Rand_2K6_6)

        # Buttons
        QtCore.QObject.connect(ui.ExportCharacter, QtCore.SIGNAL("clicked()"), self.export_character)
        QtCore.QObject.connect(ui.LoadCharacter, QtCore.SIGNAL("clicked()"), self.load_character)
        QtCore.QObject.connect(ui.SaveCharacter, QtCore.SIGNAL("clicked()"), self.save_character)

        QtCore.QObject.connect(ui.ExportState, QtCore.SIGNAL("clicked()"), self.export_state)
        QtCore.QObject.connect(ui.LoadState, QtCore.SIGNAL("clicked()"), self.load_state)
        QtCore.QObject.connect(ui.SaveState, QtCore.SIGNAL("clicked()"), self.save_state)

        # New skill support
        QtCore.QObject.connect(ui.NewSkillAdd, QtCore.SIGNAL("clicked()"),
                               self.skill_manager.new_skill_add)
        QtCore.QObject.connect(ui.NewSkillDel, QtCore.SIGNAL("clicked()"),
                               self.skill_manager.new_skill_del)
        QtCore.QObject.connect(ui.NewSkillList, QtCore.SIGNAL("currentTextChanged(QString)"),
                               self.skill_manager.new_skill_select)
        # Character skill support
        QtCore.QObject.connect(ui.SkillAdd, QtCore.SIGNAL("clicked()"),
                               self.skill_manager.skill_add)
        QtCore.QObject.connect(ui.SkillDel, QtCore.SIGNAL("clicked()"),
                               self.skill_manager.skill_del)
        QtCore.QObject.connect(ui.SkillAdded, QtCore.SIGNAL("currentTextChanged(QString)"),
                               self.skill_manager.skill_select)
        
        # Weapon support
        QtCore.QObject.connect(ui.NewWeaponAdd, QtCore.SIGNAL("clicked()"),
                               self.item_manager.new_weapon_add)
        QtCore.QObject.connect(ui.NewWeaponDel, QtCore.SIGNAL("clicked()"),
                               self.item_manager.new_weapon_del)
        QtCore.QObject.connect(ui.NewWeaponList, QtCore.SIGNAL("currentTextChanged(QString)"),
                               self.item_manager.new_weapon_select)
        
        QtCore.QObject.connect(ui.NewWeaponSkillAdd, QtCore.SIGNAL("clicked()"),
                               self.item_manager.new_weapon_skill_add)
        QtCore.QObject.connect(ui.NewWeaponSkillDel, QtCore.SIGNAL("clicked()"),
                               self.item_manager.new_weapon_skill_del)

        # Armor support
        QtCore.QObject.connect(ui.NewArmorAdd, QtCore.SIGNAL("clicked()"),
                               self.item_manager.new_armor_add)
        QtCore.QObject.connect(ui.NewArmorDel, QtCore.SIGNAL("clicked()"),
                               self.item_manager.new_armor_del)
        QtCore.QObject.connect(ui.NewArmorList, QtCore.SIGNAL("currentTextChanged(QString)"),
                               self.item_manager.new_armor_select)

        # Weapon/Armor/Character functions
        QtCore.QObject.connect(ui.WeaponAdd, QtCore.SIGNAL("clicked()"),
                               self.item_manager.weapon_add)
        QtCore.QObject.connect(ui.WeaponDel, QtCore.SIGNAL("clicked()"),
                               self.item_manager.weapon_del)

        
        QtCore.QObject.connect(ui.ArmorAdd, QtCore.SIGNAL("clicked()"),
                               self.item_manager.armor_add)
        QtCore.QObject.connect(ui.ArmorDel, QtCore.SIGNAL("clicked()"),
                               self.item_manager.armor_del)

        
    def update_character(self):
        if not self.signal_enabled:
            return
        # Set basic coefficients
        ch.Str = ui.Str.value()
        ch.Dex = ui.Dex.value()
        ch.Con = ui.Con.value()
        ch.Int = ui.Int.value()
        ch.Wil = ui.Wil.value()
        ch.Cha = ui.Cha.value()
        # Calculate the rest
        ch.calc()

        # Set names
        ch.Name = ui.Name.text()
        ch.Race = ui.Race.text()
        ch.Comment = ui.Comment.text()

        # Update the rest!
        self.update_ui()

    def update_ui(self):
        self.signal_enabled = False
        ui.Str.setValue(ch.Str)
        ui.Dex.setValue(ch.Dex)
        ui.Con.setValue(ch.Con)
        ui.Int.setValue(ch.Int)
        ui.Wil.setValue(ch.Wil)
        ui.Cha.setValue(ch.Cha)
        vsum = ch.Str + ch.Dex + ch.Con + \
               ch.Int + ch.Wil + ch.Cha

        ui.A.setText("%d" % ch.A)
        ui.M.setText("%d" % ch.M)
        ui.D.setText("%d" % ch.D)
        ui.P.setText("%d" % ch.P)
        ui.R.setText("%d" % ch.R)

        ui.HP.setText("%d" % ch.HP)
        ui.MP.setText("%d" % ch.MP)
        ui.I.setText("%d" % ch.I)
        ui.HC.setText("%d" % ch.HC)
        ui.Status.setText("Info: Suma cech postaci = %d" % vsum)

        self.signal_enabled = True

    def K6(self):
        return random.randint(1,6)

    def _2K6(self):
        return self.K6() + self.K6()

    def _KV(self):
        return random.randint(-8, 8)

    def Rand_KV(self):
        ch.Str = self._KV()
        ch.Dex = self._KV()
        ch.Con = self._KV()
        ch.Int = self._KV()
        ch.Wil = self._KV()
        ch.Cha = self._KV()
        ch.calc()
        self.update_ui()


    def Rand_2K6_4(self):
        ch.Str = self._2K6() - 4
        ch.Dex = self._2K6() - 4
        ch.Con = self._2K6() - 4
        ch.Int = self._2K6() - 4
        ch.Wil = self._2K6() - 4
        ch.Cha = self._2K6() - 4
        ch.calc()
        self.update_ui()

    def Rand_2K6_6(self):
        ch.Str = self._2K6() - 6
        ch.Dex = self._2K6() - 6
        ch.Con = self._2K6() - 6
        ch.Int = self._2K6() - 6
        ch.Wil = self._2K6() - 6
        ch.Cha = self._2K6() - 6
        ch.calc()
        self.update_ui()

    def export_character(self):
        self.update_character()
        self.ui.ExportText.setText(ch.export())

    def export_state(self):
        self.ui.ExportStateText.setText(world.export())

    def load_character(self):
        global ch
        widget = QtGui.QFileDialog()
        filename = widget.getOpenFileName(None, "Wczytaj postac Vorago", "", "Vorago Character (*.vch)")
        if filename == "":
            ui.Status.setText("Blad: Postac nie wczytana.")
            return
        f = open(filename, "r")
        ch = pickle.load(f)
        f.close()
        # Make sure everything needed exists in world and
        # is compatible with this data.
        for skill in ch.skills.values():
            world.skills[skill.name] = skill

        for weapon in ch.weapons.values():
            world.weapons[weapon.name] = weapon

        for armor in ch.armors.values():
            world.armors[armor.name] = armor

        ui.Name.setText(ch.Name)
        ui.Race.setText(ch.Race)
        ui.Comment.setText(ch.Comment)

        self.update_ui()
        self.skill_manager.skill_update()
        self.item_manager.weapon_update()
        self.item_manager.armor_update()
            
        ui.Status.setText("OK: Postac wczytana.")
    
    def save_character(self):
        widget = QtGui.QFileDialog()
        filename = widget.getSaveFileName(None, "Zapisz postac Vorago", "", "Vorago Character (*.vch)")
        if filename == "":
            ui.Status.setText("Blad: Postac nie zapisana.")
            return

        self.update_character() # Set race, name etc.
        
        f = open(filename, "w")
        pickle.dump(ch, f)
        f.close()
        ui.Status.setText("OK: Postac zapisana.")
    
    def load_state(self):
        global ch
        global world
        widget = QtGui.QFileDialog()
        filename = widget.getOpenFileName(None, "Wczytaj stan Vorago", "", "Vorago State (*.vorago)")
        if filename == "":
            ui.Status.setText("Blad: Stan nie wczytany.")
            return
        self.load_state_from(filename)

    def save_state(self):
        widget = QtGui.QFileDialog()
        filename = widget.getSaveFileName(None, "Zapisz stan Vorago", "", "Vorago State (*.vorago)")
        if filename == "":
            ui.Status.setText("Blad: Stan nie zapisany.")
            return

        f = open(filename, "w")
        pickle.dump(world, f)
        f.close()
        ui.Status.setText("OK: Stan zapisany.")

    def load_state_from(self, filename):
        global ch
        global world
        
        f = open(filename, "r")
        try:
            world = pickle.load(f)
        except EOFError:
            world = Vorago.World()
        f.close()
        del ch
        ch = Vorago.Character()
                
        
        self.update_ui()
        self.skill_manager.skill_update()
        self.item_manager.weapon_update()
        self.item_manager.armor_update()
        ui.Status.setText("OK: Stan wczytany.")


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = GUI.Ui_MainWindow()
    ui.setupUi(MainWindow)

    # Setup my signals
    manager = Manager(ui)

    MainWindow.show()
    sys.exit(app.exec_())
