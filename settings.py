# settings.py

#Channels
#Channels MUST NOT have spaces and spaces must have -
masassins_category_channel_name = "Masassins-Team-Channels"
masassins_announcements_channel_name = "masamon-announcements"
masassins_all_team_channel_name = "All-Team-Discussion"

#NEW AUTO CHANNELS MUST BE ADDED TO THIS LIST
base_channels_namelist = [
    masassins_all_team_channel_name,
    masassins_announcements_channel_name,
    masassins_category_channel_name
]

#Roles
masassins_alive_role = "masassins2020-ALIVE"
masassins_dead_role = "masassins2020-FAINTED"
admin_role = "masassins-planner"
MASA_staff_role = "MASA Staff"
base_masassins_roles = [
    masassins_alive_role,
    masassins_dead_role,
    admin_role
]
admins_list = ["Jimmy"]


#Team Initialization
team_name_fire = "Fire"
team_name_bug = "Bug"
team_name_dark = "Dark"
team_name_ghost = "Ghost"
team_name_psychic = "Psychic"
team_name_fighting = "Fighting"
team_name_rock = "Rock"
team_name_alumni = "Alumni"
team_name_team_rocket = "Team Rocket"

team_list = [
    team_name_fire, team_name_bug,
    team_name_dark, team_name_ghost,
    team_name_psychic, team_name_fighting,
    team_name_rock, team_name_alumni,
    team_name_team_rocket
]
team_starting_experience = 0
team_starting_gold = 0

team_effectiveness = {
    team_name_fire : team_name_bug,
    team_name_bug : team_name_dark,
    team_name_dark : team_name_ghost,
    team_name_ghost : team_name_psychic,
    team_name_psychic : team_name_fighting,
    team_name_fighting : team_name_rock,
    team_name_alumni : "Normal",
    team_name_team_rocket : "Normal"
}

#Battle Calculations
super_effective_damage = 75
normal_damage = 50
not_very_effective_damage = 25

base_experience_reward = 10
base_gold_reward = 10
bonus_experience_reward = 20
bonus_gold_reward = 20

team_kill_bonus_gold = 50
team_kill_bonus_experience = 50

#Items Initialization
item_name_x_attack = "X Attack"
item_name_x_defense = "X Defense"
item_name_amulet_coin = "Amulet Coin"
item_name_shell_bell = "Shell Bell"
item_name_potion = "Potion"
item_name_revive = "Revive"
item_name_expshare = "EXP Share"

item_cost_x_attack = 150
item_cost_x_defense = 150
item_cost_amulet_coin = 50
item_cost_shell_bell = 100
item_cost_potion = 50
item_cost_revive = 70

item_list = [
    item_name_potion,
    item_name_revive,
    item_name_shell_bell,
    item_name_amulet_coin,
    item_name_x_attack,
    item_name_x_defense,
    item_name_expshare
]

item_cost_dict = {
    item_name_potion : item_cost_potion,
    item_name_revive : item_cost_revive,
    item_name_shell_bell : item_cost_shell_bell,
    item_name_amulet_coin : item_cost_amulet_coin,
    item_name_x_attack : item_cost_x_attack,
    item_name_x_defense : item_cost_x_defense
}

item_dict = {
    item_name_potion : "Heals 50 HP. Note: you cannot heal a player past their maximum HP",
    item_name_revive : "Revives a player from fainting to 75 HP",
    item_name_shell_bell : "Heals 15 HP even time you tag someone. Each shell bell can only be held by one player. A player can either have a shell bell OR amulet coin.",
    item_name_amulet_coin : "Gain an additional 5 gold each time you tag someone. Each amulet coin can only be held by one player. A player can either have a shell bell OR amulet coin.",
    item_name_x_attack : "Entire team deals an extra 25 HP damage each time they tag someone. Only lasts until midnight of the following day.",
    item_name_x_defense : "Entire team negates 25 damage when tagged. Only lasts until midnight of the following day.",
    item_name_expshare : "Grants an additional 10 EXP per hit. Can only be held by one player and only affects that one player’s actions. If that player faints, then the EXP share is lost."
}

x_attack_damage_bonus = 25
x_defense_damage_negation = 25
shell_bell_hit_healing = 15
amulet_coin_gold_bonus = 5
exp_share_exp_bonus = 10
potion_healing = 50
revive_healing = 75

#New Player Initialization
new_player_starting_health = 200
new_player_starting_experience = 0

#Alumni Player Initialization
alumni_player_starting_health = 200
alumni_player_starting_experience = 0

player_team_dict = {
    "Aizzer":team_name_bug,
    "Jimmy":team_name_fighting,
    "Annie":team_name_dark,
    "Selina":team_name_ghost
}

#String Creation Initialization
spacing = 1
length_of_team = 10
length_of_name = 15
length_of_health = 3
length_of_experience = 4
length_of_items = 10