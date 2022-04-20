safezone_class = "During class"
safezone_work = "During work"
safezone_vehicle = "In/On Vehicles"
safezone_residence = "At Target's Residence"
safezone_stairs = "Stairs or Other Dangerous Places"
safezone_gym = "Gym"
safezone_bathroom = "Public Bathroom"
safezone_nametags = "Obtaining Nametags"
safezone_masa_event = "15 minutes before and after ANY MASA-related event*** including:"

safezone_class_desc = """
Target is safe 5 minutes before class. You may be killed if you are sitting in class 6 minutes before your class. You are NOT safe after class. If you have back to back classes, you are not safe until 5 minutes before your next class. As soon as class is over (the professor ends the class), you are no longer safe, even if you are still in the classroom. **If you are NOT IN A CLASS that is on your schedule (i.e. you have decided to skip lecture), YOU ARE NOT SAFE.
YOU CANNOT SIT IN ANOTHER PERSON'S CLASS AND DISRUPT THEIR LEARNING. KILLS ACHIEVED THIS WAY WILL BE INVALIDATED. (For example: if you walk into your target’s lecture and sit down next to them to intimidate, your kill will not be counted and your team will face punishment.)
"""
safezone_work_desc = """
Target is safe 5 minutes before work, and for the duration of your shift. You are not safe travelling to or from work other than the 5 minutes before.
"""
safezone_vehicle_desc = """
Motor Vehicles:
You are safe in vehicles such as buses and cars. As soon as you step off the vehicle, you are no longer safe (unless it is 5 minutes before class OR 15 minutes before/after MASA events).
Bikes, skateboards, and scooters:
Don’t be an ASSHOLE and get on your skateboard/scooter if you are gonna get fucked
Heelys are not counted as a vehicle.
*PLEASE maintain SAFE behavior while attempting to tag others while they are in motion. NO INJURIES PLEASE!!! If your target is injured in the course of tagging, your tag will be INVALIDATED!
An injury is defined by profuse bleeding requiring multiple bandages, grievous non-bleeding injuries such as sprains, etc. If your target requires medical attention (ex: someone else helping your target walk, your target requiring a visit to Student Health, or anything more extreme), an injury has occurred.
"""
safezone_residence_desc = """
You cannot tag a target if they are standing in their own room. However, your target is fair game in the bathroom, common room, kitchen, etc. You must get permission from at least one resident to enter a residence that is not your own.
You are NOT safe in anyone's home under any circumstances besides the ones described above, even if you have made a truce with someone else. Don’t trust anyone!
"""
safezone_stairs_desc = """
Players cannot be tagged on staircases
If a Player has been on a staircase for more than 2 mins, the Player will lose 20 EXP.
A Player cannot safely go to the same/another flight of stairs within a 2 minute window. 
"""
safezone_gym_desc = """
Players cannot be tagged if they're in the weight room or on a treadmill.
"""
safezone_bathroom_desc = """
You are only safe within the stall/urinal. Once you leave the stall/urinal, you may be tagged.
"""
safezone_nametags_desc = """
You are only safe while receiving name tags from Gym Leaders. You are not safe on route to obtain tags. After the tags have changed hands, you are no longer safe.
"""
safezone_masa_event_desc = """
MASA Staff/Fusion Meetings
Deco/Fusion-related work parties
Fusion-related Sponsorship/Marketing outreach
kF practice
**Staff-approved MoMASA events. Such events must: 1) have agreement from staff, and 2) be planned and executed like any other MoMASA. The Gym Leaders have the right to remove this safety opportunity if it is abused.
"""

safezone_list = [
    safezone_class,
    safezone_work,
    safezone_vehicle,
    safezone_residence,
    safezone_stairs,
    safezone_gym,
    safezone_bathroom,
    safezone_nametags,
    safezone_masa_event
]

safezone_dict = {
    safezone_class : safezone_class_desc,
    safezone_work : safezone_work_desc,
    safezone_vehicle : safezone_vehicle_desc,
    safezone_residence : safezone_residence_desc,
    safezone_stairs : safezone_stairs_desc,
    safezone_gym : safezone_gym_desc,
    safezone_bathroom : safezone_bathroom_desc,
    safezone_nametags : safezone_nametags_desc,
    safezone_masa_event : safezone_masa_event_desc
}