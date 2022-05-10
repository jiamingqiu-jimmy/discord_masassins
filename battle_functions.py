import settings
import sql_functions as sql
import sqlite3
import discord


def damage_check_team(cur, attacking_player_name, attacking_player_team, defending_player_name, defending_player_team):
    total_damage_dealt = 0
    damage_output_list = []

    #Check for effectiveness
    super_effective_team_attack = settings.team_effectiveness[attacking_player_team]
    super_effective_team_defend = settings.team_effectiveness[defending_player_team]
    if super_effective_team_attack == defending_player_team or super_effective_team_attack == "SUPER":
        total_damage_dealt += settings.super_effective_damage
        damage_output_list.append("Super effective attack : {} DMG".format(settings.super_effective_damage))
    elif super_effective_team_defend == attacking_player_team:
        total_damage_dealt += settings.not_very_effective_damage
        damage_output_list.append("Not very effective attack : {} DMG".format(settings.not_very_effective_damage))
    else:
        total_damage_dealt += settings.normal_damage
        damage_output_list.append("Normal attack : {} DMG".format(settings.normal_damage))

    player_items = [item[0] for item in sql.get_player_items(cur, attacking_player_name)]
    if any(x in player_items for x in settings.DMG_BOOST_ITEMS):
        total_damage_dealt += settings.DMG_BOOST
        one_item = list(set(player_items).intersection(settings.DMG_BOOST_ITEMS))[0]
        damage_output_list.append(f"{one_item} : {settings.DMG_BOOST} DMG")

    damage_output_list.append(f'Total Damage Dealt : {total_damage_dealt} HP')
    
    return total_damage_dealt, damage_output_list

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
    if defending_player_team == settings.team_name_elite_four:
        total_gold_amount += settings.alumni_player_bonus_base_gold
        total_experience_amount += settings.alumni_player_bonus_base_exp
        total_reward_list.append("Bonus Elite-Four gold reward: {} gold".format(settings.admin_player_bonus_base_gold))
        total_reward_list.append("Bonus Elite-Four EXP reward: {} EXP".format(settings.admin_player_bonus_base_exp))
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
        if defending_player_team == settings.team_name_elite_four:
            total_gold_amount += settings.admin_player_bonus_faint_gold
            total_experience_amount += settings.admin_player_bonus_faint_exp
            total_reward_list.append("Fainting Elite-Four bonus: {} gold".format(settings.admin_player_bonus_faint_gold))
            total_reward_list.append("Fainting Elite-Four bonus: {} EXP".format(settings.admin_player_bonus_faint_exp))
    # if defending_player_team == settings.team_name_fire:
    #     total_gold_amount += 20
    #     total_experience_amount += 20
    #     total_reward_list.append("Tagging Fire gold reward: 20 gold")
    #     total_reward_list.append("Tagging Fire EXP reward: 20 EXP")
    
    # if defending_player_team == settings.team_name_dragon:
    #     total_gold_amount += 10
    #     total_experience_amount += 10
    #     total_reward_list.append("Tagging Dragon gold reward: 10 gold")
    #     total_reward_list.append("Tagging Dragon EXP reward: 10 EXP")

    if settings.item_name_exp_share in [item [0] for item in sql.get_player_items(cur, attacking_player_name)]:
        total_gold_amount += settings.gold_reward_exp_share
        total_experience_amount += settings.exp_reward_exp_share
        total_reward_list.append("EXP Share gold reward: {} gold".format(settings.gold_reward_exp_share))
        total_reward_list.append("EXP Share EXP reward: {} EXP".format(settings.exp_reward_exp_share))

    if defending_player_name in settings.bounty_list:
        total_gold_amount += settings.bounty_reward_gold
        total_experience_amount += settings.bounty_reward_exp
        total_reward_list.append(f'Bounty Gold Reward: {settings.bounty_reward_gold} gold')
        total_reward_list.append(f'Bounty EXP Reward: {settings.bounty_reward_exp} EXP')

    total_reward_list.append("--------- Total Rewards ---------")
    total_reward_list.append("Total gold: " + str(total_gold_amount))
    total_reward_list.append("Total EXP: " + str(total_experience_amount))

    return total_gold_amount, total_experience_amount, total_reward_list
    
