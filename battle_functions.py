import settings
import sql_functions as sql
import sqlite3
import discord


def damage_check_team(cur, attacking_player_name, attacking_player_team, defending_player_name, defending_player_team):
    total_damage_dealt = 0
    total_life_steal = 0
    damage_output_list = []

    #Check for effectiveness
    super_effective_team_attack = settings.team_effectiveness[attacking_player_team]
    super_effective_team_defend = settings.team_effectiveness[defending_player_team]
    if super_effective_team_attack == defending_player_team:
        total_damage_dealt += settings.super_effective_damage
        damage_output_list.append("Super effective attack : {} DMG".format(settings.super_effective_damage))
    elif super_effective_team_defend == attacking_player_team:
        total_damage_dealt += settings.not_very_effective_damage
        damage_output_list.append("Not very effective attack : {} DMG".format(settings.not_very_effective_damage))
    else:
        total_damage_dealt += settings.normal_damage
        damage_output_list.append("Normal attack : {} DMG".format(settings.normal_damage))
    #Check for X-attack on attacking team
    if sql.get_team_item(cur, attacking_player_team, settings.item_name_x_attack) is not None:
        total_damage_dealt += settings.x_attack_damage_bonus
        damage_output_list.append("X attack : +{} DMG".format(settings.x_attack_damage_bonus))

    #Check for X-Defense on defending team
    if sql.get_team_item(cur, defending_player_team, settings.item_name_x_defense) is not None:
        total_damage_dealt -= settings.x_defense_damage_negation
        damage_output_list.append("Defending Team X-Defense: -{} DMG".format(settings.x_defense_damage_negation))

    damage_output_list.append("Total Damage Dealt : " + str(total_damage_dealt))
        
    #Check for attacking player shell bell
    if sql.get_player_item(cur, attacking_player_name, settings.item_name_shell_bell) is not None:
        total_life_steal += settings.shell_bell_hit_healing
        damage_output_list.append("=====\nAttacking Player Shell Bell: +{} HP to {}".format(settings.shell_bell_hit_healing, attacking_player_name))
    
    return total_life_steal, total_damage_dealt, damage_output_list

def reward_check_player(cur, defending_player_death, attacking_player_name, attacking_player_team, defending_player_name, defending_player_team):
    total_gold_amount = 0
    total_experience_amount = 0
    total_reward_list = []

    #Give base experience and gold amounts
    total_gold_amount += settings.base_gold_reward
    total_experience_amount += settings.base_experience_reward

    total_reward_list.append("Base gold reward: {} gold".format(settings.base_gold_reward))
    total_reward_list.append("Base EXP reward: {} EXP".format(settings.base_experience_reward))
    if defending_player_team == settings.team_name_alumni:
        total_gold_amount += settings.alumni_player_bonus_base_gold
        total_experience_amount += settings.alumni_player_bonus_base_exp
        total_reward_list.append("Bonus Alumni gold reward: {} gold".format(settings.alumni_player_bonus_base_gold))
        total_reward_list.append("Bonus Alumni EXP reward: {} EXP".format(settings.alumni_player_bonus_base_exp))
    if defending_player_team == settings.team_name_fire:
        total_gold_amount += 20
        total_experience_amount += 20
        total_reward_list.append("Bonus gold/exp for hitting fire : 20")
    elif defending_player_team == settings.team_name_psychic:
        total_gold_amount += 10
        total_experience_amount += 10
        total_reward_list.append("Bonus gold/exp for hitting psychic : 10")
    #If death is true add extra experience and gold amounts
    if defending_player_death:
        total_gold_amount += settings.bonus_gold_reward
        total_experience_amount += settings.bonus_experience_reward
        total_reward_list.append("Fainting gold reward: {} gold".format(settings.bonus_gold_reward))
        total_reward_list.append("Fainting EXP reward: {} EXP".format(settings.bonus_experience_reward))
        if defending_player_team == settings.team_name_alumni:
            total_gold_amount += settings.alumni_player_bonus_faint_gold
            total_experience_amount += settings.alumni_player_bonus_faint_exp
            total_reward_list.append("Fainting Alumni bonus: {} gold".format(settings.alumni_player_bonus_faint_gold))
            total_reward_list.append("Fainting Alumni bonus: {} EXP".format(settings.alumni_player_bonus_faint_exp))

    #Check attacking player for Amulet Coin gold bonus
    if sql.get_player_item(cur, attacking_player_name, settings.item_name_amulet_coin) is not None:
        total_gold_amount += settings.amulet_coin_gold_bonus
        total_reward_list.append("=====\nBonus Amulet Coin reward: +{} gold".format(settings.amulet_coin_gold_bonus))

    #Check attacking palyer for Share Exp experience bonus
    if sql.get_player_item(cur, attacking_player_name, settings.item_name_expshare) is not None:
        total_experience_amount += settings.exp_share_exp_bonus
        total_reward_list.append("=====\nBonus exp share reward : +{} EXP".format(settings.item_name_expshare))

    total_reward_list.append("--------- Total Rewards ---------")
    total_reward_list.append("Total gold: " + str(total_gold_amount))
    total_reward_list.append("Total EXP: " + str(total_experience_amount))

    return total_gold_amount, total_experience_amount, total_reward_list
    
