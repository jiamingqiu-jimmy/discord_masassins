import settings
import sql_functions as sql
import sqlite3


def damage_check_team(cur, attacking_player_name, attacking_player_team, defending_player_name, defending_player_team):
    total_damage_dealt = 0
    total_life_steal = 0

    effectiveness_string = ""
    x_attack_string = ""
    x_defense_string = ""
    shell_bell_string = ""
    spacing = " - "

    #Check for effectiveness
    super_effective_team_attack = settings.team_effectiveness[attacking_player_team]
    super_effective_team_defend = settings.team_effectiveness[defending_player_team]
    if super_effective_team_attack == defending_player_team:
        total_damage_dealt += settings.super_effective_damage
        effectiveness_string = "Super effective attack : {} damage".format(settings.super_effective_damage)
    else if super_effective_team_defend == attacking_player_team:
        total_damage_dealt += settings.not_very_effective_damage
        effectiveness_string = "Not very effective attack : {} damage".format(settings.not_very_effective_damage)
    else:
        total_damage_dealt += settings.normal_damage
        effectiveness_string = "Normal attack : {} damage".,format(settings.normal_damage)

    #Check for X-attack on attacking team
    if sql.find_team_item(attacking_player_team, settings.item_name_x_attack) != 0:
        total_damage_dealt += settings.x_attack_damage_bonus
        x_attack_string = spacing + "Attacking Team X-Attack: {} bonus damage".format(settings.x_attack_damage_bonus)

    #Check for X-Defense on defending team
    if sql.find_team_item(defending_player_team, settings.item_name_x_defense) != 0:
        total_damage_dealt += settings.x_defense_damage_negation
        x_defense_string = spacing + "Defending Team X-Defense: {} damage negation".format(settings.x_defense_damage_negation)

    #Check for attacking player shell bell
    if sql.find_player_item(attacking_player_name, settings.item_name_shell_bell) != 0:
        total_life_steal += settings.shell_bell_hit_healing
        shell_bell_string = spacing + "Attacking Player Shell Bell: {} has been healed to {}".format(settings.shell_bell_hit_healing, attacking_player_name)
    
    total_damage_string = "Total Damage:" + str(total_damage_dealt)
    final_output_string = "Damage Calculations: " + 
        total_damage_string + 
        " Breakdown: " + 
        effectiveness_string + spacing +
        x_attack_string + spacing + 
        x_defense_string + spacing +
        shell_bell_string
        
    return total_life_steal, total_damage_dealt, total_damage_string

def reward_check_player(cur, defending_player_death, attacking_player_name, attacking_player_team, defending_player_name, defending_player_team):
    total_gold_amount = 0
    total_experience_amount = 0
    total_reward_calculations_string = ""

    base_gold_string = ""
    base_experience_string = ""
    bonus_gold_string = ""
    bonus_experience_string = ""
    amulet_coin_gold_bonus_string = ""
    exp_share_bonus_string = ""
    spacing = " - "

    #Give base experience and gold amounts
    total_gold_amount += settings.base_gold_reward
    total_experience_amount += settings.base_experience_reward

    base_gold_string = "Base gold reward: {} gold".format(settings.base_gold_reward)
    base_experience_string= "Base experience reward: {} EXP".format(settings.base_experience_reward)

    #If death is true add extra experience and gold amounts
    if defending_player_death:
        total_gold_amount += settings.bonus_gold_reward
        total_experience_amount += settings.bonus_experience_reward
        bonus_gold_string = spacing + "Bonus gold reward: {} gold".format(settings.bonus_gold_reward)
        bonus_experience_string = spacing + "Bonus experience reward: {} experience".format(settings.bonus_experience_reward)

    #Check attacking player for Amulet Coin gold bonus
    if sql.find_player_item(cur, attacking_player_name, settings.item_name_amulet_coin) != 0:
        total_gold_amount += settings.amulet_coin_gold_bonus
        amulet_coin_gold_bonus_string = spacing + "Bonus amulet coin reward: {} gold".format(settings.amulet_coin_gold_bonus)

    #Check attacking palyer for Share Exp experience bonus
    if sql.find_player_item(cur, attacking_player_name, settings.item_name_expshare) != 0:
        total_experience_amount += settings.exp_share_exp_bonus
        exp_share_bonus_string = spacing + "Bonus exp share reward : {} experience".format(settings.item_name_expshare)

    total_gold_string = "Total gold: " + str(total_gold_amount)
    total_experience_string = "Total experience: " + str(total_experience_amount)

    final_string = total_gold_string +
        "Breakdown: " +
        base_gold_string + bonus_gold_string + amulet_coin_gold_bonus_string + "\n"
        total_experience_string + 
        "Breakdown: " +
        base_experience_string + bonus_experience_string + exp_share_bonus_string

    return total_gold_amount, total_experience_amount, final_string
    
