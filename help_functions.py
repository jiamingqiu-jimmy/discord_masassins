import help_emojis as e_help

#Help Emojis
e_h3lp = e_help.get_emoji(emoji_help)
e_desc = e_help.emoji_desc
e_rule = e_help.emoji_rule
e_safezone = e_help.emoji_safezone
e_use = e_help.emoji_use
e_buy = e_help.emoji_buy
e_shop = e_help.emoji_shop
e_viewall = e_help.emoji_view_all
e_viewteam = e_help.emoji_view_team
e_attack = e_help.emoji_attack
e_trade = e_help.emoji_trade
e_join = e_help.emoji_join

#Help Name and descriptions


help_help = f"{e_h3lp} Help : !help"
help_desc = f"{e_desc} Description : !desc"
help_rule = f"{e_rule} Rules : !rule"
help_safezone = f"{e_safezone} Safe zones : !safezones"
help_use = f"{e_use} Use : !use <item_name> <player_name>"
help_buy = f"{e_buy} Buy : !buy <item_name>"
help_shop = f"{e_shop} Shop : !shop"
help_view_all = f"{e_viewall} View All : !view_all"
help_view_team = f"{e_viewteam} v : !v <team_name>"
help_attack = f"{e_attack} Attack : !attack <player_name>"
help_trade = f"{e_trade} Trade : !trade <team_name> <gold_amount>"
help_join = f"{e_join} Join the game! : !join"

help_help_description = "Gives a list of useful commands and how to use them"
help_use_description = "Use an item on the player or give it to them to hold"
help_desc_description = "Gives details on important aspects of the game"
help_rule_description = "Listing of the rules to make the game fun and fair for everyone"
help_safezone_description = "Rules regarding safe zones"
help_buy_description = "Buy an item for your team, make sure you have enough gold for it"
help_shop_description = "Shows you the shop and the items for sale"
help_view_all_description = "Shows you a list of all the teams"
help_view_team_description = "Shows you a specific team"
help_attack_description = "Attacks a player, they must confirm for you to receive rewards"
help_trade_description = "Trades with a team, basically you just give them gold, so be sure to make a trade agreement first"
help_join_description = "Allows you to join the game if you signed up! Make sure to join before anything!"

list_of_help = [
    help_help, help_desc, help_rule, help_safezone, help_join, help_attack, help_view_team, help_view_all,
    help_shop, help_buy, help_use, help_trade
]

help_dict = {
    help_help : help_help_description,
    help_desc : help_desc_description,
    help_rule : help_rule_description,
    help_safezone : help_safezone_description,
    help_attack : help_attack_description,
    help_view_team : help_view_team_description,
    help_view_all : help_view_all_description,
    help_shop : help_shop_description,
    help_buy : help_buy_description,
    help_use : help_use_description,
    help_trade : help_trade_description,
    help_join : help_join_description
}
