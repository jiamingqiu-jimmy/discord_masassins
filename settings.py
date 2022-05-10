import shop_emojis as e_shop

#Item Emojis
e_potion = e_shop.emoji_potion
e_revive = e_shop.emoji_revive
e_master = e_shop.emoji_master_ball
e_gacha = e_shop.emoji_gacha_ball
e_poke = e_shop.emoji_poke_ball

# settings.py

#MASASSINS Database Name
MASASSINS_DB_NAME = "masassins.db"

#Channels
#Channels MUST NOT have spaces and spaces must have -
masassins_category_channel_name = "Masassins-Channels"
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
admins_list = ["Jimmy", "Selina", "Ruby", "Sophia"]
admin_player_bonus_faint_gold = 20
admin_player_bonus_faint_exp = 20
admin_player_bonus_base_gold = 20
admin_player_bonus_base_exp = 20

#Team Initialization
team_name_fire = "Fire"
team_name_ice = "Ice"
team_name_dragon = "Dragon"
team_name_alumni = "Legendaries"
team_name_gym_leaders = "Gym-Leaders"
team_name_elite_four = "Elite-Four"

team_list = [
    team_name_fire, team_name_ice,
    team_name_dragon, team_name_alumni,
    team_name_gym_leaders, team_name_elite_four
]

team_starting_gold = 0

# team_effectiveness = {
#     team_name_fire : team_name_ice,
#     team_name_ice : team_name_dragon,
#     team_name_dragon : team_name_fire,
#     team_name_alumni : "Normal",
#     team_name_gym_leaders : "Normal"
# }

#Reverse
# team_effectiveness = {
#     team_name_fire : team_name_dragon,
#     team_name_ice : team_name_fire,
#     team_name_dragon : team_name_ice,
#     team_name_alumni : "Normal",
#     team_name_gym_leaders : "Normal"
# }

#ALl_SUPER
team_effectiveness = {
    team_name_fire : "SUPER",
    team_name_ice : "SUPER",
    team_name_dragon : "SUPER",
    team_name_alumni : "SUPER",
    team_name_gym_leaders : "SUPER",
    team_name_elite_four : "SUPER"
}

#Battle Calculations
effective_string = "Effectiveness"
total_damage_string = "Total Damage"
super_effective_damage = 60
normal_damage = 40
not_very_effective_damage = 25

base_experience_reward = 10
base_gold_reward = 10
bonus_experience_reward = 20
bonus_gold_reward = 20

team_kill_bonus_gold = 50
team_kill_bonus_experience = 50

master_ball_catch_chance = 1
gacha_ball_catch_chance = 0.005

#Items Initialization
item_name_potion = f"Potion"
item_name_revive = f"Revive"
item_name_master_ball = f"Master-Ball"
item_name_gacha_ball = f"Gacha-Ball"
item_name_poke_ball = f"Poke-Ball"
item_name_exp_share = f"Exp-Share"
item_name_pineapple = f"Pineapple"
item_name_keyboard = f"Keyboard"
item_name_boba = f"Boba"
item_name_gummy_bear = f"Gummy-Bear"

item_emoji_dict = {
    item_name_potion:e_potion,
    item_name_revive:e_revive,
    item_name_master_ball:e_master,
    item_name_gacha_ball:e_gacha,
    item_name_poke_ball:e_poke
}

item_cost_potion = 30
item_cost_revive = 60
item_cost_master_ball = 300
item_cost_gacha_ball = 5
item_cost_poke_ball = 100

exp_reward_exp_share = 5
gold_reward_exp_share = 5

item_list = [
    item_name_potion,
    item_name_revive,
    item_name_master_ball,
    item_name_gacha_ball,
    item_name_poke_ball,
    item_name_exp_share,
    item_name_keyboard,
    item_name_boba,
    item_name_pineapple,
    item_name_gummy_bear
]

DMG_BOOST_ITEMS = [
    item_name_pineapple,
    item_name_keyboard,
    item_name_boba,
    item_name_gummy_bear
]
DMG_BOOST = 40

item_cost_dict = {
    item_name_potion : item_cost_potion,
    item_name_revive : item_cost_revive,
    item_name_master_ball : item_cost_master_ball,
    item_name_gacha_ball : item_cost_gacha_ball,
    item_name_poke_ball : item_cost_poke_ball,
    item_name_exp_share : "Obtainable through Scavenger Hunt",
    item_name_pineapple : "Elite-Four Unique",
    item_name_keyboard : "Elite-Four Unique",
    item_name_boba : "Elite-Four Unique",
    item_name_gummy_bear : "Elite-Four Unique"
}

item_dict = {
    item_name_potion : "Heals 40 HP. Note: you cannot heal a player past their maximum HP",
    item_name_revive : "Revives a player from fainting to 75 HP",
    item_name_master_ball : "Add one person of your choice from another team to your team",
    item_name_gacha_ball : "Add a player of choice to your team 0.5% of the time",
    item_name_poke_ball : "Add one person (not currently signed up for the game) to your team",
    item_name_exp_share : "Event-only item. Every time Player tags someone, Player will gain an additional 5 EXP and 5 gold.",
    item_name_keyboard : "RGB Back-Lit Keyboard +40 DMG",
    item_name_boba : "Camellia Honey Boba +40 DMG",
    item_name_pineapple : "Pineapple Squishmallow +40 DMG",
    item_name_gummy_bear : "Pouch of Gummy Bears +40 DMG"
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
    "Tommy":team_name_fire,
    "Nicole":team_name_fire,
    "Rachana":team_name_fire,
    "Jasen":team_name_fire,
    "Naasik":team_name_fire,
    "Sherry":team_name_fire,
    "Jasmeet":team_name_fire,
    "Alexander":team_name_fire,
    "Brian":team_name_ice,
    "Brianna":team_name_ice,
    "Johnny":team_name_ice,
    "Kelly":team_name_ice,
    "Derek":team_name_ice,
    "Alvin":team_name_ice,
    "Eunice":team_name_ice,
    "Luis":team_name_ice,
    "Andrew":team_name_dragon,
    "Yi":team_name_dragon,
    "Justin":team_name_dragon,
    "Lucy":team_name_dragon,
    "William":team_name_dragon,
    "Anurag":team_name_dragon,
    "Angela":team_name_dragon,
    "Ryan":team_name_dragon,
    "Shelby":team_name_alumni,
    "Sarena":team_name_alumni,
    "Aizzer":team_name_alumni,
    "Matt":team_name_alumni,
    "Jimmy":team_name_gym_leaders,
    "Selina":team_name_gym_leaders,
    "Sophia":team_name_gym_leaders,
    "Ruby":team_name_gym_leaders
}

bounty_list = []
bounty_reward_gold = 10
bounty_reward_exp = 10