# settings.py

#MASASSINS Database Name
MASASSINS_DB_NAME = "masassins.db"

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
MASA_staff_role = "Puffles"
base_masassins_roles = [
    masassins_alive_role,
    masassins_dead_role,
    admin_role
]
admins_list = ["Jimmy", "Selina", "Annie", "Aizzer"]


#Team Initialization
team_name_fire = "Fire"
team_name_bug = "Bug"
team_name_dark = "Dark"
team_name_ghost = "Ghost"
team_name_psychic = "Psychic"
team_name_fighting = "Fighting"
team_name_rock = "Rock"
team_name_alumni = "Alumni"
team_name_gym_leaders = "Gym-Leaders"

team_list = [
    team_name_fire, team_name_bug,
    team_name_dark, team_name_ghost,
    team_name_psychic, team_name_fighting,
    team_name_rock, team_name_alumni,
    team_name_gym_leaders
]

team_starting_gold = 0

team_effectiveness = {
    team_name_fire : team_name_bug,
    team_name_bug : team_name_dark,
    team_name_dark : team_name_ghost,
    team_name_ghost : team_name_psychic,
    team_name_psychic : team_name_fighting,
    team_name_fighting : team_name_rock,
    team_name_rock : team_name_fire,
    team_name_alumni : "Normal",
    team_name_gym_leaders : "Normal"
}

#Battle Calculations
effective_string = "Effectiveness"
total_damage_string = "Total Damage"
super_effective_damage = 60
normal_damage = 40
not_very_effective_damage = 25

base_experience_reward = 10
base_gold_reward = 10
bonus_experience_reward = 30
bonus_gold_reward = 30

team_kill_bonus_gold = 50
team_kill_bonus_experience = 50

master_ball_catch_chance = 1
gacha_ball_catch_chance = 0.003

#Items Initialization
item_name_potion = "Potion"
item_name_revive = "Revive"
item_name_master_ball = "Master-Ball"
item_name_gacha_ball = "Gacha-Ball"
item_name_poke_ball = "Poke-Ball"

item_cost_potion = 30
item_cost_revive = 60
item_cost_master_ball = 300
item_cost_gacha_ball = 3
item_cost_poke_ball = 100

item_list = [
    item_name_potion,
    item_name_revive,
    item_name_master_ball,
    item_name_gacha_ball,
    item_name_poke_ball,
]

item_cost_dict = {
    item_name_potion : item_cost_potion,
    item_name_revive : item_cost_revive,
    item_name_master_ball : item_cost_master_ball,
    item_name_gacha_ball : item_cost_gacha_ball,
    item_name_poke_ball : item_cost_poke_ball
}

item_dict = {
    item_name_potion : "Heals 40 HP. Note: you cannot heal a player past their maximum HP",
    item_name_revive : "Revives a player from fainting to 75 HP",
    item_name_master_ball : "Add one person of your choice from another team to your team",
    item_name_gacha_ball : "Add a player of choice to your team 0.3% of the time",
    item_name_poke_ball : "Add one person (not currently signed up for the game) to your team"
}

potion_healing = 40
revive_healing = 75

#New Player Initialization
new_player_starting_health = 200
new_player_starting_experience = 0
max_player_hp = 200

#Alumni Player Initialization
alumni_player_starting_health = 300
alumni_player_starting_experience = 0
alumni_player_bonus_faint_gold = 10
alumni_player_bonus_faint_exp = 10
alumni_player_bonus_base_gold = 10
alumni_player_bonus_base_exp = 10

player_team_dict = {
    "Andrew":team_name_bug,
    "Brian":team_name_psychic,
    "Brianna":team_name_psychic,
    "Johnny":team_name_bug,
    "jsutin":team_name_fighting,
    "Nathan":team_name_fire,
    "Nicole":team_name_fighting,
    "Selina":team_name_fire,
    "soph920":team_name_ghost,
    "Tommy":team_name_rock,
    "Yi":team_name_dark,
    "Jimmy":team_name_gym_leaders,
    "Ruby":team_name_gym_leaders,
    "Cindy":team_name_ghost,
    "Nick":team_name_fire
}