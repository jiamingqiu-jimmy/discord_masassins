#Help Name and descriptions


help_help = "Help : !help"
help_use = "Use : !use <item_name> <player_name>"
help_buy = "Buy : !buy <item_name>"
help_shop = "Shop : !shop"
help_view_all = "View All : !view_all"
help_view_team = "v : !v <team_name>"
help_attack = "Attack : !attack <player_name>"
help_trade = "Trade : !trade <team_name> <gold_amount>"
help_join = "Join the game! : !join"

help_help_description = "Gives a list of useful commands and how to use them"
help_use_description = "Use an item on the player or give it to them to hold (for shell-bell/amulet coin)"
help_buy_description = "Buy an item for your team, make sure you have enough gold for it"
help_shop_description = "Shows you the shop and the items for sale"
help_view_all_description = "Shows you a list of all the teams"
help_view_team_description = "Shows you a specific team"
help_attack_description = "Attacks a player, they must confirm for you to receive rewards"
help_trade_description = "Trades with a team, basically you just give them gold, so be sure to make a trade agreement first"
help_join_description = "Allows you to join the game if you signed up! Make sure to join before anything!"

list_of_help = [
    help_help, help_join, help_attack, help_view_team, help_view_all,
    help_shop, help_buy, help_use, help_trade
]

help_dict = {
    help_help : help_help_description,
    help_attack : help_attack_description,
    help_view_team : help_view_team_description,
    help_view_all : help_view_all_description,
    help_shop : help_shop_description,
    help_buy : help_buy_description,
    help_use : help_use_description,
    help_trade : help_trade_description,
    help_join : help_join_description
}