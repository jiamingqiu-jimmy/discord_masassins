rule_tag = "TAG"
rule_cheating = "CHEATING"
rule_safe_zones = "SAFE ZONES"


rule_tag_desc = """
Name tags must contain your name and your team name. Name tags that lack either or both will not register as a hit.
You can only write your name and your team name ONCE per tag.
When you run out, contact the Team Rocket for more (STEALING NAME TAGS IS FORBIDDEN!)
A player may restock name tags only when they run out. 
Each player is only allowed to have a maximum of three name tags as weapons on their person.
A name tag ripped in action may count as a valid kill IF AND ONLY IF all information (name and team name) is on the name tag portion affixed to your target.​ Do not cheat and rip up your name tags. We will find you.
"""
rule_cheating_desc = """
FALSIFY YOUR DEATH (i.e. put a tag on yourself and claim you are dead when you are not), you will be penalized with 75 HP damage
Enlist the help of others who are NOT playing the game to help kill your target, your kill will be invalidated and your team will lose EXP and gold and you will lose HP.
Steal name tags from other teams, your team will lose EXP
Do not report a schedule change to Team Rocket (i.e. you add or drop a class, change your work schedule, etc.), your team will lose gold.
Physically involved with the MASAssins game despite your status as “fainting” or “flinching”, your team will lose EXP and gold. If you are fainted or flinched, you are not allowed to physically engage in the MASAssins game. This includes (but is not limited to) physically blocking kill attempts, restraining other players’ movements, and any other form of physical action.
"""

rule_safe_zones_desc = """
You may not Masassinate while you or your target are safe.
Safe zones are explained more in !safezones
"""

rule_list = [
    rule_tag,
    rule_cheating,
    rule_safe_zones
]

rule_dict = {
    rule_tag : rule_tag_desc,
    rule_cheating : rule_cheating_desc,
    rule_safe_zones : rule_safe_zones_desc
}