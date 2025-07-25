import pytesseract
from PIL import ImageGrab, Image, ImageDraw, ImageFont, ImageTk
import tkinter as tk
from tkinter import Frame, Label
import time
import threading
import textwrap
from pynput import mouse
from win32api import GetSystemMetrics
import pystray
from pathlib import Path
import os
from re import findall, match, sub

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

positive_conditions ={
    "Charming": "Raises Friendship Bond gain.",
    "Fast Learner": "Reduces the cost of skills.",
    "Hot Topic": "Raises Friendship Bond gain for Director Akikawa and Reporter Etsuko Otonashi.",
    "Practice Perfect": "Lowers chance of training failure.",
    "Shining Brightly": "Lowers chance of training failure."
}
negative_conditions ={
    "Migraine": "Mood cannot be increased (except when using Alarm Clocks to retry races)",
    "Night Owl": "Character may lose energy.",
    "Skin Outbreak": "Character's mood may decrease by one stage.",
    "Slacker": "Character may not show up for training.",
    "Slow Metabolism": "Character cannot gain Speed from speed training.",
    "Under the Weather": "Increases chance of training failure.",
    "Practice Poor": "Lowers chance of training failure.",
}
Positive_skills = {
    # Rare Speed Skills
    "Technician": "Moderately increase ability to navigate smoothly. (Pace Chaser)",
    "Lightning Step": "Avoid becoming surrounded when positioned toward the back mid-race. (Medium)",
    "Vanguard Spirit": "Increase ability to maintain the lead when leading by a large margin mid-race. (Long)",
    "Professor of Curvature": "Increase velocity on a corner with skilled turning.",
    "The Coast Is Clear!": "Moderately widen field of view with situational awareness when moving sideways. (End Closer)",
    "Concentration": "Decrease time lost to slow starts.",
    "Unrestrained": "Increase ability to keep the lead on the final corner. (Front Runner)",
    "Killer Tunes": "Increase positioning ability when positioned toward the front mid-race. (Medium)",
    "Furious Feat": "Increase ability when positioned toward the back late-race. (Mile)",
    "In Body and Mind": "Increase velocity in the last spurt.",
    "Changing Gears": "Increase passing ability when positioned toward the front mid-race. (Mile)",
    "Step on the Gas!": "Increase acceleration when passing runner mid-race. (Mile)",
    "Corner Connoisseur": "Increase acceleration on a corner with masterful turning.",
    "Mile Maven": "Widen the margin when in the lead early-race. (Mile)",
    "Speed Star": "Increase the ability to break out of the pack on the final corner. (Pace Chaser)",
    "Determined Descent": "Moderately improve running on a downhill. (Pace Chaser)",
    "Taking the Lead": "Increase ability to go to the front early-race. (Front Runner)",
    "On Your Left!": "Increase acceleration late-race. (Late Surger)",
    "Clairvoyance": "Widen field of view with heightened observation early-race. (Medium)",
    "Lane Legerdemain": "Increase navigation late-race.",
    "No Stopping Me!": "Increase maneuverability when the way ahead is blocked in the last spurt",
    "Rising Dragon": "Increase velocity when passing another runner on the outside on the final corner. (Late Surger)",
    "Hard Worker": "Moderately increase passing ability. (Late Surger)",
    "Fast & Furious": "Increase velocity mid-race. (Late Surger)",
    "Turbo Sprint": "Increase acceleration on a straight. (Sprint)",
    "Staggering Lead": "Increase ability to maintain the lead when leading by a large margin mid-race. (Sprint)",
    "Blinding Flash": "Increase spurting ability when positioned toward the back late-race. (Sprint)",
    "The Bigger Picture": "Widen field of view with heightened observation mid-race. (Late Surger)",
    "Rushing Gale!": "Increase acceleration on a straight.",
    "Escape Artist": "Increase ability to go to the front mid-race. (Front Runner)",
    "Unyielding": "Increase ability to fight back when passed by another runner on the final corner. (Medium)",
    "Center Stage": "Increase navigation early-race.",
    "Plan X": "Increase passing ability when positioned toward the front mid-race. (Sprint)",
    "Beeline Burst": "Increase velocity on a straight",
    
    # Normal Speed Skills
    "Prudent Positioning": "Moderately increase navigation early-race.",
    "Go with the Flow": "Moderately increase navigation late-race.",
    "Thunderbolt Step": "Moderately avoid becoming surrounded when positioned toward the back mid-race. (Medium)",
    "Shrewd Step": "Slightly increase ability to navigate smoothly. (Pace Chaser)",
    "Keeping the Lead": "Slightly increase ability to maintain the lead when leading by a large margin mid-race. (Long)",
    "Long Corners": "Slight increase velocity on a corner. (Long)",
    "Corner Adept": "Slightly increase velocity on a corner with skilled turning.",
    "Pace Chaser Corners": "Slightly increase velocity on a corner. (Pace Chaser)",
    "Pressure": "Slightly increase velocity when passing another runner late-race. (Long)",
    "I Can See Right Through You": "Slightly widen field of view with situational awareness when moving sideways. (End Closer)",
    "Uma Stan": "Slightly increase velocity when close to many runners",
    "Focus": "Slightly decrease time lost to slow starts.",
    "Final Push": "Slightly increase ability to keep the lead on the final corner. (Front Runner)",
    "Fast-Paced": "Slightly increase ability to go to the front mid-race. (Front Runner)",
    "Up-Tempo": "Slightly increase positioning ability when positioned toward the front mid-race. (Medium)",
    "Prepared to Pass": "Slightly increase ability to break out of the pack on the final corner. (Pace Chaser)",
    "Slick Surge": "Slightly increase acceleration late-race. (Late Surger)",
    "Updrafters": "Slightly increase passing ability when positioned toward the back late-race. (Mile)",
    "Straightaway Acceleration": "Slightly increase acceleration on a straight.",
    "Mile Straightaway": "Slightly increase velocity on a straight. (Mile)",
    "Homestretch Haste": "Slightly increase velocity in the last spurt.",
    "Steadfast": "Slightly increase ability to fight back when passed by another runner on the final corner. (Medium)",
    "Outer Swell": "Slightly increase velocity when passing another runner on the outside on the final corner. (Late Surger)",
    "Straightaway Adept": "Slightly increase velocity on a straight.",
    "Early Lead": "Slightly increase ability to go to the front early-race. (Front Runner)",
    "Shifting Gears": "Slightly increase passing ability when positioned toward the front mid-race. (Mile)",
    "Acceleration": "Slightly increase acceleration when passing another runner mid-race. (Mile)",
    "Corner Acceleration": "Slightly increase acceleration on a corner with masterful turning.",
    "Nimble Navigator": "Slightly increase maneuverability when the way ahead is blocked in the last spurt.",
    "Productive Plan": "Slightly widen the margin when in the lead early-race. (Mile)",
    "Straight Descent": "Slightly improve running on a downhill. (Pace Chaser)",
    "Highlander": "Slightly improve running on an uphill.",
    "Front Runner Straightaways": "Slightly increase velocity on a straight. (Front Runner)",
    "Front Runner Corners": "Slightly increase velocity on a corner. (Front Runner)",
    "Position Pilfer": "Slightly increase velocity mid-race. (Late Surger)",
    "Pace Chaser Straightaways": "Slightly increase velocity on a straight. (Pace Chaser)",
    "Hawkeye": "Moderately wider field of view with heightened observation early-race. (Medium)",
    "Leader's Pride": "Slightly avoid being passed early-race. (Front Runner)",
    "Ramp Up": "Slightly increase velocity when passing another runner mid-race.",
    "Medium Straightaways": "Slightly increase velocity on a straight. (Medium)",
    "Medium Corners": "Slightly increase velocity on a corner. (Medium)",
    "Fighter": "Slightly increase passing ability. (Late Surger)",
    "Late Surger Corners": "Slightly increase velocity on a corner. (Late Surger)",
    "Sprinting Gear": "Slightly increase acceleration on a straight. (Sprint)",
    "Huge Lead": "Slightly increase ability to maintain the lead when leading by a large margin mid-race. (Sprint)",
    "Countermeasure": "Slightly increase passing ability when positioned toward the front mid-race. (Sprint)",
    "1,500,000 CC": "Slightly increase velocity on an uphill. (Late Surger)",
    "Studious": "Slightly widen field of view with heightened observation mid-race. (Late Surger)",
    "Gap Closer": "Slightly increase spurting ability when positioned toward the back late-race. (Sprint)",
    "Unyielding Spirit": "Slightly increase passing ability. (Mile)",
    "Straightaway Spurt": "Slightly increase acceleration on a straight in the last spurt. (End Closer)",
    "Inside Scoop": "Slightly increase velocity when near the inner rail on the final corner. (Long)",
    "Strategist": "Slightly widen field of view when positioned toward the back late-race. (End Closer)",
    "Groundwork": "Slightly increase acceleration after activating many skills early-race.",
    "Tail Held High": "Slightly increase velocity after activating many skills mid-race.",
    "Second Wind": "Slightly increase acceleration when positioned toward the back mid-race. (Front Runner)",
    "Slipstream": "Slightly decrease wind resistance when following directly behind another runner.",
    "Playtime's Over!": "Slightly increase velocity when followed by another runner directly behind for a long time.",
    "Sprint Straightaways": "Slightly increase velocity on a straight. (Sprint)",
    "Sprint Corners": "Slightly increase velocity on a corner. (Sprint)",
    "Meticulous Measures": "Moderately prepare to make for the finish line mid-race. (Sprint)",
    "Mile Corners": "Slightly increase velocity on a corner (Mile)",
    "End Closer Straightaways": "Slightly increase velocity on a straight. (End Closer)",
    "Masterful Gambit": "Slightly move up in preparation to close the gap late-race. (End Closer)",
    "Long Straightaways": "Slightly increase velocity on a straight. (Long)",
    "Late Surger Straightaways": "Slightly increase velocity on a straight. (Late Surger)",
    "End Closer Corners": "Slightly increase velocity on a corner. (End Closer)",
    "Tactical Tweak": "Slightly increase acceleration when positioned toward the back mid-race. (Pace Chaser)",
    "Dodging Danger": "Moderately avoid becoming surrounded early-race. (Front Runner)",

    # Rare Passive Skills
    "Super Lucky Seven": "Good things may happen when in bracket 7.",

    # Rare Recovery Skills
    "Calm and Collected": "Decrease fatigue early-race. (Pace Chaser)",
    "Go-Home Specialist": "Reduce fatigue on a downhill. (End Closer)",
    "Race Planner": "Decrease fatigue mid-race. (Pace Chaser)",
    "Breath of Fresh Air": "Recover endurance on a straight",
    "Gourmand": "Recover endurance mid-race. (Pace Chaser)",
    "Cooldown": "Decrease fatigue by taking a breather upon entering a straight. (Long)",
    "Trackblazer": "Decrease fatigue when in the lead mid-race. (Medium)",
    "Swinging Maestro": "Recover endurance on a corner with efficient turning.",
    "Iron Will": "Recover endurance when the way ahead is jammed early-race.",
    "Indomitable": "Recover endurance when passed by another runner mid-race.",
    "Restless": "Reduce fatigue on an uphill. (Front Runner)",
    "Keen Eye": "Decrease fatigue when positioned toward the back early-race. (Mile)",
    "Unruffled": "Recover endurance when surrounded mid-race.",
    "Adrenaline Rush": "Regain the energy to run after exhausting strength. (Long)",
    "Miraculous Step": "Decrease fatigue when moving sideways. (Medium)",

    # Normal Passive Skills
    "Spring Runner": "Moderately increase performance in spring.",
    "Left-Handed": "Moderately increase performance on left-handed tracks.",
    "Competitive Spirit": "Moderately increase performance when at least 5 other runners are using the same strategy.",
    "Wet Conditions": "Moderately increase performance on good, soft, and heavy ground.",
    "Cloudy Days": "Moderately increase performance in cloudy weather.",
    "Pace Chaser Savvy": "Moderately increase ability to get into a good position. (Pace Chaser)",
    "Non-Standard Distance": "Moderately increase performance over non-standard distances (non-multiples of 400m)",
    "Rainy Days": "Moderately increase performance in rainy weather.",
    "Standard Distance": "Moderately increase performance over standard distances (multiples of 400m).",
    "Firm Conditions": "Moderately increase performance on firm ground.",
    "Long Shot": "Moderately increase performance when 4th favorite or below.",
    "Lucky Seven": "Moderately good things may happen when in bracket 7.",
    "Kokura Racecourse": "Moderately increase performance at Kokura Racecourse.",
    "Outer Post Proficiency": "Moderately increase performance in brackets 6-8.",
    "Late Surger Savvy": "Moderately increase ability to get into a good position. (Late Surger)",
    "Front Runner Savvy": "Moderately increase ability to get into a good position. (Front Runner)",
    "End Closer Savvy": "Moderately increase ability to get into a good position. (End Closer)",
    "Sympathy": "Moderately increase performance when many runner share a sympathetic heart.",
    "Hanshin Racecourse": "Moderately increase performance at Hanshin Racecourse.",
    "Tokyo Racecourse": "Moderately increase performance at Tokyo Racecourse.",
    "Nakayama Racecourse": "Moderately increase performance at Nakayama Racecourse.",
    "Target in Sight": "Moderately increase performance when the favorite is using the same strategy.",
    "Sunny Days": "Moderately increase performance in sunny weather.",
    "Inner Post Proficiency": "Moderately increase performance in brackets 1-3.",
    "Right-Handed": "Moderately increase performance on right-handed tracks.",
    "Fall Runner": "Moderately increase performance in fall.",
    "Sapporo Racecourse": "Moderately increase performance at Sapporo Racecourse.",
    "Oi Racecourse": "Moderately increase performance at Oi Racecourse.",
    "Summer Runner": "Moderately increase performance in summer.",
    "Snowy Days": "Moderately increase performance in snowy weather.",
    "Winter Runner": "Moderately increase performance in winter.",
    "Lone Wolf": "Moderately increase performance when no other runners have the heart of a lone wolf.",
    "Maverick": "Moderately increase performance when no other runners are using the same strategy.",
    "Hakodate Racecourse": "Moderately increase performance at Hakodate Racecourse.",
    "Kyoto Racecourse": "Moderately increase performance at Kyoto Racecourse.",

    # Normal Recovery Skills
    "Soft Step": "Slightly decrease fatigue when moving sideways. (Medium)",
    "Stamina to Spare": "Slightly decrease fatigue early-race. (Pace Chaser)",
    "Hydrate": "Slightly recover endurance mid-race. (Pace Chaser)",
    "Preferred Position": "Slightly decrease fatigue mid-race. (Pace Chaser)",
    "After-School Stroll": "Slightly reduce fatigue on a downhill. (End Closer)",
    "Standing By": "Slightly decrease fatigue mid-race. (End Closer)",
    "Rosy Outlook": "Slightly decrease fatigue when in the lead mid-race. (Medium)",
    "Straightaway Recovery": "Slightly recover endurance on a straight",
    "Deep Breaths": "Slightly decrease fatigue by taking a breather upon entering a straight (Long)",
    "Corner Recovery": "Slightly recover endurance on a corner with efficient turning.",
    "Pace Strategy": "Slightly recover endurance when passed by another runner mid-race.",
    "Lay Low": "Slightly recover endurance when the way ahead is jammed early-race.",
    "A Small Breather": "Slightly recover endurance late-race. (Late Surger)",
    "Triple 7s": "Slightly gain energy with 777m remaining.",
    "Extra Tank": "Slightly regain the energy to run after exhausting strength. (Long)",
    "Calm in a Crowd": "Slightly recover endurance when surrounded mid-race.",
    "Moxie": "Slightly reduce fatigue on an uphill. (Front Runner)",
    "Levelheaded": "Slightly regain composure by calming down when the way ahead is jammed. (End Closer)",
    "Watchful Eye": "Slightly decrease fatigue when positioned toward the back early-race. (Mile)",
    "Wait-and-See": "Slightly decrease fatigue when positioned toward the back mid-race. (Sprint)",
    "Passing Pro": "Slightly decrease fatigue when determined to pass another runner. (Long)",
    "Shake It Out": "Slightly recover endurance after activating many skills late-race."
}
Unique_skills = {
    "Introduction to Physiology": "Moderately recover endurance when conserving energy on a corner in the second half of the race.",
    "Empress's Pride": "Moderately increase velocity with the stride of an empress when passing another runner toward the back on the final corner.",
    "∴win Q.E.D.": "Increase velocity by deriving the winning equation when passing another runner toward the front on the final corner.",
    "Red Ace": "Slightly swell with the determination to stay number one in the second half of the race.",
    "Corazón ☆ Ardiente": "Slightly hang on to the advantage when positioned toward the front with energy to spare on the final straight.",
    "Warning Shot!": "Slightly increase velocity with a long spurt starting halfway through the race.",
    "Focused Mind": "Moderately increase velocity with a strong turn of foot when passing another runner toward the back on the final straight.",
    "Super-Duper Stoked": "Moderately recover endurance with a glance at nearby runners when positioned toward the back on the final corner.",
    "Call Me King": "Increase velocity in a true display of skill with 200m remaining after racing calmly.",
    "Red Shift/LP1211-M": "Increase acceleration by shifting gears when positioned toward the front on the final corner or later.",
    "Luck Be with Me!": "Moderately clear a path forward with the power of divination when the way ahead is jammed late-race.",
    "1st Place Kiss☆": "Slightly increase ability to break out of the pack on the straight after engaging in a challenge toward the front on the final corner.",
    "Legacy of the Strong": "Increase velocity when pressured by another runner and running out of energy toward the front on the final corner or later.",
    "The Duty of Dignity Calls": "Increase velocity with the determination to not be overtaken when positioned toward the front on the final corner.",
    "Feel the Burn!": "Moderately increase acceleration in an attempt to move up on a corner late-race.",
    "G00 1st. F∞;": "Increase velocity when positioned toward the front after making it to the final straight without faltering.",
    "I Can Win Sometimes, Right?": "Moderately increase velocity with an arousal of fighting spirit when positioned 3rd and about to lose late-race.",
    "Triumphant Pulse": "Greatly increase ability to break out of the pack by opening up a path when positioned toward the front with 200m remaining.",
    "Blue Rose Closer": "Increase velocity with strong willpower when breaking out of the pack on the final straight.",
    "Class Rep + Speed = Bakushin": "Moderately increase velocity with BAKUSHIN power when engaged in a challenge toward the front in the second half of the race.",
    "The View from the Lead is Mine!": "Increase velocity by drawing on all remaining strength when in the lead by a fair margin on the final straight.",
    "Shooting Star": "Ride the momentum and increase velocity after passing another runner toward the front late-race.",
    "Clear Heart": "Moderately recover endurance when well-positioned mid-race.",
    "Behold Thine Emperor's Divine Might": "Greatly increase velocity on the final straight after passing another runner 3 times late-race.",
    "This Dance Is for Vittoria!": "Increase velocity with royal brilliance when engaged in a challenge toward the front on the final corner.",
    "Shooting for Victory!": "Increase acceleration with a pow, a wow, and a bang when well-positioned on the final corner.",
    "Certain Victory": "Increase velocity with an indomitable fighting spirit when on the heels of another runner toward the front of the final straight.",
    "Sky-High Teio Step": "Greatly increase velocity with flashy footwork when closing gap to runners ahead on the final straight.",
    "Xceleration": "Become stronger at challenging rivals and moderately increase velocity when positioned toward the front with 200m or less remaining.",
    "V Is for Victory!": "Refuse to back down from a challenge, moderately increasing velocity on the final straight."
}
EVENTOS = {
    "New Year's Shrine Visit": [
        "Energy 30",
        "All stats 5",
        "Skill points 35"
    ],
    "Expression of Conviction": [
        "Stamina 20",
        "Speed 20"
    ],
    "Obtain Data!": [
        "Wisdom 20",
        "Power 20"
    ],
    "Tachyon the Spoiled Child": [
        "Stamina 10, Guts 10",
        "Wisdom 20"
    ],
    "At Tachyons Pace": [
        "Guts 10",
        "Speed 5, Power 5"
    ],
    "The Strongest Collaborator?!": [
        "Energy -20, Stamina 15, Guts 10",
        "Energy 5, Wisdom 5"
    ],
    "The Pressure of Justice?": [
        "Wisdom 10, Skill points 15",
        "Corner Adept 1"
    ],
    "Hamburger Helper!": [
        "Energy 10, Skill points 5",
        "Energy 30, Skill points 10"
    ],
    "Medicine That Makes You Faster?": [
        "Power 5, Guts 5",
        "Speed 5, Wisdom 5"
    ],
    "The Significance of Research": [
        "Wisdom 10",
        "Speed 10"
    ],
    "No Shortcuts": [
        "Guts 10",
        "Wisdom 10",
        "Power 10"
    ],
    "A Gift From the Dark Sky": [
        "Speed 5, Power 5",
        "Guts 10"
    ],
    "Body Modification!": [
        "Power 5, Wisdom 5",
        "Stamina 10"
    ],
    "Flowers for You": [
        "Wisdom 20",
        "Speed 20"
    ],
    "A Beautiful Stress Relief Method?": [
        "Stamina 20",
        "Guts 20"
    ],
    "Guidepost": [
        "Speed 20",
        "Power 20"
    ],
    "Empress and Monarch": [
        "Power 10",
        "Wisdom 10"
    ],
    "Operation Flowerbed": [
        "Energy 5, Wisdom 5",
        "Energy -10, Speed 10, Power 10"
    ],
    "Empress and Emperor": [
        "Homestretch Haste 1",
        "Mood 1, Skill points 15"
    ],
    "Seize Her!": [
        "Energy 10",
        "Energy -10, Mood 1, Speed 10"
    ],
    "Take Good Care of Your Tail": [
        "Energy 10",
        "Energy -10, Mood 1, Power 10"
    ],
    "Suggestion Box of Freedom": [
        "Energy 10",
        "Energy -10, Mood 1, Wisdom 10"
    ],
    "A Taste of Effort": [
        "Energy 10, Skill points 5",
        "Energy 30, Skill points 10"
    ],
    "A Little Encounter": [
        "Wisdom 10",
        "Guts 10"
    ],
    "Sweet Potato Cake": [
        "Power 10",
        "Stamina 10"
    ],
    "Imprinted Memories": [
        "Speed 10",
        "Power 10",
        "Stamina 10"
    ],
    "A Blinking Light Means Stop": [
        "Wisdom 10",
        "Power 10"
    ],
    "Smoldering Silently": [
        "Stamina 10",
        "Speed 10"
    ],
    "To Keep or Not to Keep?": [
        "Wisdom 20",
        "Stamina 10, Power 10"
    ],
    "A Realistic Fairytale": [
        "Power 20",
        "Guts 20"
    ],
    "Theory the Greatest Weapon": [
        "Stamina 20",
        "Wisdom 20"
    ],
    "Memories of Cooking and Sisterhood": [
        "Power 10",
        "Stamina 5, Wisdom 5"
    ],
    "A New Side": [
        "Speed 10",
        "Stamina 10"
    ],
    "Battle With a Raging Dragon": [
        "Power 5, Guts 5",
        "Hanshin Racecourse 1"
    ],
    "Banana Fiend": [
        "Energy 10, Skill points 5",
        "Energy 30, Skill points 10"
    ],
    "Reading in a Cafe": [
        "Stamina 10",
        "Speed 10"
    ],
    "Sharp Contrast": [
        "Wisdom 10",
        "Guts 10"
    ],
    "Emergency Presentation": [
        "Wisdom 10",
        "Power 10",
        "Stamina 10"
    ],
    "Hide and Seek Master": [
        "Guts 10",
        "Speed 10"
    ],
    "Game Theory": [
        "Wisdom 10",
        "Power 10"
    ],
    "The Best Pose": [
        "Stamina 10, Power 10",
        "Wisdom 20"
    ],
    "The Weight of Racewear": [
        "Speed 20",
        "Guts 20"
    ],
    "Looking Good": [
        "Stamina 10, Wisdom 10",
        "Speed 10, Guts 10"
    ],
    "Recommended Restaurant": [
        "Speed 5, Power 5",
        "Guts 5, Mood 1"
    ],
    "Advice from an Older Student": [
        "Speed 10",
        "Power 10"
    ],
    "Enjoying Number One": [
        "Stamina 10, Skill points 15",
        "Unyielding Spirit 1"
    ],
    "Can't Lose Sight of Number One!": [
        "Energy 10, Skill points 5",
        "Energy 30, Skill points 10"
    ],
    "As a Model Student": [
        "Wisdom 10",
        "Skill points 30"
    ],
    "Just a Little More": [
        "Skill points 30",
        "Power 10"
    ],
    "Under the Evening Star": [
        "Skill points 30",
        "Speed 5, Stamina 5",
        "Power 10"
    ],
    "Rained On": [
        "Guts 10",
        "Wisdom 10"
    ],
    "How to Spend a Day Off": [
        "Energy 10",
        "Mood 1, Wisdom 5"
    ],
    "Determination of the World's Strongest": [
        "Power 20",
        "Stamina 20"
    ],
    "Cactus Feast": [
        "Speed 10, Stamina 10",
        "Wisdom 20"
    ],
    "Song of Courage": [
        "Power 20",
        "Speed 10, Power 10"
    ],
    "A Personalized Mask": [
        "Speed 10",
        "Power 10"
    ],
    "Salsa Roja": [
        "Stamina 10",
        "Power 10"
    ],
    "Go for the Extra Large Pizza!": [
        "Power 10, Skill points 15",
        "Soft Step 1"
    ],
    "Hot and Spicy!": [
        "Energy 10, Skill points 5",
        "Energy 30, Skill points 10"
    ],
    "The Wrestler I Admire": [
        "Stamina 10",
        "Speed 10"
    ],
    "Shocking Retirement": [
        "Guts 10",
        "Power 10"
    ],
    "Renewed Resolve": [
        "Guts 10",
        "Stamina 10",
        "Speed 5, Stamina 5"
    ],
    "The Academy at Night": [
        "Mood 1, Guts 5",
        "Energy 10"
    ],
    "Flower Language": [
        "Mood 1, Wisdom 5",
        "Energy 10"
    ],
    "The Red of the Protagonist!": [
        "Wisdom 20",
        "Guts 20"
    ],
    "A Date Golshi Style": [
        "Stamina 20",
        "Power 20"
    ],
    "A Sudden Episode from Golshi's Past!": [
        "Stamina 10, Wisdom 10",
        "Speed 20"
    ],
    "Pair Discount Repeat Offender": [
        "Guts 10",
        "Stamina 10"
    ],
    "Which Did You Lose?": [
        "Energy -10, Power 20",
        "Speed 10"
    ],
    "My Part Time Job Is Crazy!": [
        "Stamina 10, Skill points 15",
        "Hanshin Racecourse 1"
    ],
    "The Day After Voices Hoarse": [
        "Stamina 10",
        "Guts 10"
    ],
    "This One's For Keeps!": [
        "Energy 10",
        "Skill points 15, Slacker -1"
    ],
    "Summer Camp Year 3 Ends": [
        "Random stats 15"
    ],
    "Killer Appetite!": [
        "Energy 10, Skill points 5",
        "Energy 30, Skill points 10"
    ],
    "Legend of the Left Pinky": [
        "Stamina 10",
        "Speed 10"
    ],
    "Hello From About 15 Billion Years Ago": [
        "Guts 10",
        "Wisdom 10"
    ],
    "And Then She": [
        "Speed 10",
        "Guts 10",
        "Power 10"
    ],
    "A Lovely Place": [
        "Stamina 10",
        "Wisdom 10"
    ],
    "Nighttime Park Visit": [
        "Guts 10",
        "Speed 10"
    ],
    "After the Takarazuka Kinen Keyword 2": [
        "All stats 5, Mood 1, Skill points 45",
        "All stats 3, Mood 1, Skill points 45, (random) Charming 1, (random) Gatekept OBTAIN"
    ],
    "Hidden Meaning": [
        "Stamina 10, Guts 10",
        "Power 20"
    ],
    "Principles": [
        "Speed 20",
        "Stamina 20"
    ],
    "Hate to Lose": [
        "Wisdom 20",
        "Stamina 10, Guts 10"
    ],
    "Errands Have Perks": [
        "Speed 5, Stamina 5",
        "Energy 5, Wisdom 5"
    ],
    "Beauteaful": [
        "Wisdom 5, Skill points 15",
        "Speed 10"
    ],
    "Tracen Karuta Queen": [
        "Speed 10, Wisdom 5",
        "Competitive Spirit 1"
    ],
    "In Search of Refreshment": [
        "Mood -1, Guts 25",
        "Mood -1, Wisdom 25"
    ],
    "Together for Tea": [
        "Energy 10, Skill points 5",
        "Energy 30, Skill points 10"
    ],
    "Yamato Nadeshiko": [
        "Power 5, Wisdom 5",
        "Speed 10"
    ],
    "Childhood's Apart": [
        "Guts 10",
        "Stamina 10"
    ],
    "Nadeshiko Gal": [
        "Power 10",
        "Wisdom 10",
        "Speed 10"
    ],
    "Childhood Dream": [
        "Speed 5, Guts 5",
        "Stamina 5, Wisdom 5"
    ],
    "Flower Vase": [
        "Guts 5, Wisdom 5",
        "Speed 5, Stamina 5"
    ],
    "The Racewear I Love!": [
        "Speed 20",
        "Power 20"
    ],
    "Pair Interview!": [
        "Power 20",
        "Stamina 20"
    ],
    "Tug of War Tournament!": [
        "Guts 20",
        "Speed 20"
    ],
    "Arm Wrestling Contest": [
        "Wisdom 10",
        "Power 10"
    ],
    "Looking for Something Important": [
        "Energy -10, Guts 20",
        "Stamina 10"
    ],
    "Sand Training!": [
        "Guts 10, Skill points 15",
        "Energy 15"
    ],
    "The Final Boss Spe!": [
        "Energy 10, Skill points 5",
        "Energy 30, Skill points 10"
    ],
    "A Little Detour!": [
        "Skill points 30",
        "Stamina 10"
    ],
    "Parks Are Fun!": [
        "Speed 10",
        "Power 10"
    ],
    "Secret Day Off Plan!": [
        "Speed 10",
        "Power 10",
        "Wisdom 10"
    ],
    "So Cool!": [
        "Skill points 30",
        "Wisdom 10"
    ],
    "Forgot to Eat!": [
        "Guts 10",
        "Stamina 10"
    ],
    "The Outfit That Suits Me Most": [
        "Speed 10, Guts 10",
        "Power 20"
    ],
    "Running Isn't Everything": [
        "Stamina 20",
        "Speed 10, Power 10"
    ],
    "Manners Are Common Sense": [
        "Guts 20",
        "Stamina 10, Wisdom 10"
    ],
    "Movies Are Full of Learning Opportunities": [
        "Speed 5, Guts 5",
        "Stamina 10"
    ],
    "The King Knows No Exhaustion": [
        "Energy 5",
        "Power 10"
    ],
    "First Rate in Studies Too": [
        "Wisdom 10, Skill points 15",
        "Outer Swell 1"
    ],
    "After School Soda": [
        "Guts 10",
        "Speed 10"
    ],
    "Three Heads Are Better than One": [
        "Wisdom 10",
        "Stamina 10"
    ],
    "Sweet Tooth Temptation": [
        "Energy 10, Skill points 5",
        "Energy 30, Skill points 10"
    ],
    "First Rate Spot": [
        "Guts 10",
        "Speed 10"
    ],
    "First Rate Harvest": [
        "Power 5, Guts 5",
        "Speed 5, Stamina 5"
    ],
    "First Rate Terms": [
        "Power 10",
        "Wisdom 10",
        "Guts 10"
    ],
    "Crowds Are No Problem": [
        "Speed 10",
        "Power 10"
    ],
    "Breaking Curfew is Second Rate": [
        "Guts 5, Wisdom 5",
        "Speed 5, Power 5"
    ],
    "Trendsetter": [
        "Speed 10, Wisdom 10",
        "Power 20"
    ],
    "Sewing Star": [
        "Guts 20",
        "Stamina 10, Power 10"
    ],
    "My Favorite Things": [
        "Speed 20",
        "Stamina 10, Guts 10"
    ],
    "Hot Rod": [
        "Speed 10",
        "Wisdom 10"
    ],
    "Let's Play": [
        "Energy 10",
        "Energy -5, Power 10, Guts 5"
    ],
    "A Lady's Style": [
        "Speed 5, Skill points 10, Mood 1",
        "Huge Lead 1"
    ],
    "Let's Cook!": [
        "Speed 10",
        "Guts 10"
    ],
    "The Road to a Rad Victory!": [
        "Stamina 10",
        "Wisdom 10"
    ],
    "Down to Dance!": [
        "Speed 10",
        "Power 10"
    ],
    "Nostalgia Fever": [
        "Energy 10, Skill points 5",
        "Energy 30, Skill points 10"
    ],
    "The Secret to Supporting Each Other": [
        "Speed 10",
        "Power 10"
    ],
    "Even Role Models Get Lonely": [
        "Stamina 5, Guts 5",
        "Speed 5, Power 5"
    ],
    "Take the Wheel": [
        "Wisdom 10",
        "Guts 10",
        "Power 10"
    ],
    "Meeting New People Is Trendy": [
        "Guts 10",
        "Wisdom 10"
    ],
    "The Fun Never Stops": [
        "Speed 5, Wisdom 5",
        "Stamina 5, Power 5"
    ],
    "Room of the Chosen Ones": [
        "Guts 20",
        "Speed 20"
    ],
    "Better Fortune! Lucky Telephone": [
        "Stamina 10, Wisdom 10",
        "Power 20"
    ],
    "Under the Meteor Shower": [
        "Speed 10, Power 10",
        "Stamina 10, Guts 10"
    ],
    "Cursed Camera": [
        "Wisdom 10",
        "Skill points 30"
    ],
    "Manhattan's Dream": [
        "Hesitant Front Runners 1",
        "Stamina 10"
    ],
    "Pretty Gunslingers": [
        "Skill points 15, Mood 1",
        "Power 15"
    ],
    "Which One is the Lucky Card?!": [
        "Random stats 5"
    ],
    "Seven Gods of Fortune Fine Food Tour": [
        "Energy 10, Skill points 5",
        "Energy 30, Skill points 10"
    ],
    "Fukukitaru's Protection against Misfortune": [
        "Guts 10",
        "Power 10"
    ],
    "Punch in a Pinch": [
        "Speed 10",
        "Stamina 5, Wisdom 5"
    ],
    "Fukukitaru's Unique Good Luck Spell": [
        "Speed 5, Guts 5",
        "Stamina 5, Power 5",
        "Wisdom 10"
    ],
    "Taking the Plunge": [
        "Stamina 10",
        "Speed 5, Wisdom 5"
    ],
    "Shrine Visit": [
        "Power 5, Guts 5",
        "Speed 5, Stamina 5"
    ],
    "Maya's Thrilling Test of Courage": [
        "Power 20",
        "Guts 20"
    ],
    "Sweet Feelings for You": [
        "Stamina 20",
        "Wisdom 20"
    ],
    "Mayano Takes Off": [
        "Speed 20",
        "Stamina 20"
    ],
    "Maya Will Teach You": [
        "Power 5, Guts 5",
        "Wisdom 10"
    ],
    "Tips from a Top Model!": [
        "Energy -10, Stamina 20",
        "Speed 10"
    ],
    "Maya's Race Class": [
        "Stamina 10, Skill points 15",
        "Straightaway Adept 1"
    ],
    "Hearty Chanko": [
        "Energy 10, Skill points 5",
        "Energy 30, Skill points 10"
    ],
    "Maya's Exciting Livestream!": [
        "Stamina 5, Power 5",
        "Guts 10"
    ],
    "Maya's Euphoric Livestream!": [
        "Speed 10",
        "Stamina 10"
    ],
    "Maya's Twinkly Determination!": [
        "Speed 5, Stamina 5",
        "Power 10",
        "Wisdom 10"
    ],
    "Maya's Special Someone!": [
        "Speed 10",
        "Guts 10"
    ],
    "Wish on a Star": [
        "Wisdom 10",
        "Speed 10"
    ],
    "Resolve and Duty": [
        "Speed 10, Wisdom 10",
        "Power 20"
    ],
    "Late Night Fanservice Training": [
        "Guts 20",
        "Speed 20"
    ],
    "Elegance": [
        "Stamina 10, Power 10",
        "Wisdom 20"
    ],
    "Queen of the Island": [
        "Speed 10",
        "Stamina 10"
    ],
    "It's Called a Sea Pineapple!": [
        "Skill points 30",
        "Stamina 10"
    ],
    "Cooking Up Memories": [
        "Energy 15",
        "Early Lead 1"
    ],
    "The Allure of Racecourse Food": [
        "Energy 30, Skill points 10",
        "Guts 15, Skill points 5"
    ],
    "Attack of the Chestnut Feast!": [
        "Energy 10, Skill points 5",
        "Energy 30, Skill points 10"
    ],
    "Two Tickets for the Silver Screen": [
        "Stamina 10",
        "Wisdom 5, Skill points 15"
    ],
    "An Excited Young Lady": [
        "Guts 10",
        "Power 10"
    ],
    "Endless Kingdom": [
        "Stamina 10",
        "Wisdom 10",
        "Speed 5, Power 5"
    ],
    "Bargain Find": [
        "Speed 10",
        "Guts 10"
    ],
    "Three Ramen Bowls Worth of Temptation": [
        "Skill points 30",
        "Speed 5, Stamina 5"
    ],
    "My Signature Racewear": [
        "Guts 20",
        "Speed 20"
    ],
    "Heart Pounding Aquarium": [
        "Power 10, Wisdom 10",
        "Stamina 10, Wisdom 10"
    ],
    "Refreshingly Real": [
        "Stamina 20",
        "Power 20"
    ],
    "Muscle Jealousy": [
        "Guts 10",
        "Wisdom 10"
    ],
    "The Pony Girl and the Wolf Prince": [
        "Energy 5, Stamina 5",
        "Energy 5, Speed 5"
    ],
    "Real Gains": [
        "Power 10, Skill points 15",
        "Wet Conditions 1"
    ],
    "Rest Day": [
        "Energy 10, Skill points 5",
        "Energy 30, Skill points 10"
    ],
    "Nerve Racking Rest Time": [
        "Stamina 10",
        "Power 10"
    ],
    "Flush with Feelings": [
        "Wisdom 10",
        "Speed 10"
    ],
    "With Relaxation and Trust Comes": [
        "Speed 10",
        "Stamina 10",
        "Power 10"
    ],
    "Ryan to the Rescue!": [
        "Power 10",
        "Guts 10"
    ],
    "The Little Fans of the Umadol": [
        "Power 10",
        "Wisdom 10"
    ],
    "Trail of Light": [
        "Speed 20",
        "Power 20"
    ],
    "Smiles Are Contagious": [
        "Stamina 20",
        "Guts 20"
    ],
    "Who to Count On": [
        "Wisdom 20",
        "Power 20"
    ],
    "Operation Execute Orders": [
        "Stamina 10",
        "Power 10"
    ],
    "Operation Extra Classes": [
        "Energy 10, Mood 1",
        "Wisdom 10"
    ],
    "Operation Excursion Trouble": [
        "Stamina 10, Skill points 15",
        "Wet Conditions 1"
    ],
    "Brutal Training": [
        "Energy -10, Power 5, Skill points 5",
        "Energy 5"
    ],
    "The Perfect Dessert": [
        "Energy 10, Skill points 5",
        "Energy 30, Skill points 10"
    ],
    "Let's Make Memories": [
        "Speed 10",
        "Guts 10"
    ],
    "Bourbon's Challenge?": [
        "Power 10",
        "Wisdom 10"
    ],
    "You're Irreplaceable to Me": [
        "Stamina 10",
        "Speed 10",
        "Power 10"
    ],
    "Operation Dance Fever": [
        "Stamina 5, Guts 5",
        "Stamina 5, Wisdom 5"
    ],
    "Operation Festival Fun": [
        "Power 10",
        "Stamina 5, Guts 5"
    ],
    "Nature and Her Tired Trainer": [
        "Power 20",
        "Stamina 20"
    ],
    "Bittersweet Sparkle": [
        "Power 20",
        "Speed 20"
    ],
    "Festive Colors": [
        "Guts 20",
        "Stamina 20"
    ],
    "Rainy Day Fun": [
        "Wisdom 10",
        "Energy -10, Stamina 10, Guts 10"
    ],
    "Not My Style": [
        "Energy 5, Mood 1",
        "Speed 5, Power 5"
    ],
    "Whirlwind Advice": [
        "Studious 1",
        "Speed 5, Stamina 5, Power 5"
    ],
    "A Little Can't Hurt": [
        "Energy 10, Skill points 5",
        "Energy 30, Skill points 10"
    ],
    "A Phone Call from Mom": [
        "Stamina 10",
        "Speed 10"
    ],
    "Once in a While": [
        "Stamina 5, Guts 5",
        "Stamina 5, Power 5"
    ],
    "Bittersweet Twilight": [
        "Speed 10",
        "Guts 10",
        "Wisdom 10"
    ],
    "Snapshot of Emotions": [
        "Speed 10",
        "Power 10"
    ],
    "Let's Watch the Fish": [
        "Guts 10",
        "Speed 10"
    ],
    "Pinned Hopes": [
        "Stamina 10, Power 10",
        "Wisdom 20"
    ],
    "Oguri the Forest Guide?": [
        "Speed 20",
        "Power 20"
    ],
    "Better Than a Plushie": [
        "Guts 20",
        "Stamina 20"
    ],
    "Lost Umamusume": [
        "Guts 10",
        "Speed 10"
    ],
    "Field Workout": [
        "Guts 10",
        "Power 10"
    ],
    "Running on Full": [
        "Energy 10, Skill points 15",
        "Nakayama Racecourse 1"
    ],
    "Oguri's Gluttony Championship": [
        "Energy 30, Power 10, Skill points 10",
        "Energy 10, Power 5, Skill points 5"
    ],
    "Bottomless Pit": [
        "Energy 10, Skill points 5",
        "Energy 30, Skill points 10"
    ],
    "Oguri Makes a Resolution": [
        "Speed 5, Wisdom 5",
        "Stamina 5, Guts 5"
    ],
    "Oguri Perseveres": [
        "Guts 10",
        "Power 10"
    ],
    "Oguri Matures": [
        "Wisdom 10",
        "Stamina 10",
        "Power 10"
    ],
    "Something Smells Good": [
        "Speed 10",
        "Guts 10"
    ],
    "High Level Rival": [
        "Speed 5, Stamina 5",
        "Power 5, Wisdom 5"
    ],
    "Am I Enough?": [
        "Guts 20",
        "Power 20"
    ],
    "Sweet Lively Joy": [
        "Speed 10, Stamina 10",
        "Wisdom 20"
    ],
    "I Am Enough": [
        "Guts 10, Wisdom 10",
        "Stamina 10, Power 10"
    ],
"Training Inspiration": [
        "Energy -10, Guts 20",
        "Energy 5, Skill points 15"
    ],
    "Wonderful New Worlds": [
        "Stamina 10",
        "Speed 5, Wisdom 5"
    ],
    "Looking on the Bright Side": [
        "Stamina 5, Guts 10",
        "Firm Conditions 1"
    ],
    "A Page about Apples": [
        "Energy 10, Skill points 5",
        "Energy 30, Skill points 10"
    ],
    "Even When the Ladybugs Are Gone": [
        "Stamina 10",
        "Wisdom 10"
    ],
    "Even When Clouds Cover the Sky": [
        "Speed 5, Power 5",
        "Guts 10"
    ],
    "My Sun": [
        "Guts 5, Wisdom 5",
        "Speed 5, Power 5",
        "Stamina 10"
    ],
    "I've Got This": [
        "Guts 10",
        "Speed 10"
    ],
    "A Page about Sunsets": [
        "Power 5, Guts 5",
        "Stamina 5, Wisdom 5"
    ],
    "Bakushin for Love!": [
        "Stamina 10, Wisdom 10",
        "Guts 20"
    ],
    "A Day Without a Class Rep": [
        "Speed 20",
        "Power 20"
    ],
    "Bakushin in Signature Racewear!": [
        "Power 10, Guts 10",
        "Wisdom 20"
    ],
    "The Bakushin Book!": [
        "Wisdom 10",
        "Stamina 10"
    ],
    "The Voices of the Students": [
        "Energy -10, Stamina 10, Power 10",
        "Speed 10"
    ],
    "Solving Riddles Bakushin Style!": [
        "Guts 10, Skill points 15",
        "Nakayama Racecourse 1"
    ],
    "Bakushin?! Class?!": [
        "Energy 10, Skill points 5",
        "Energy 30, Skill points 10"
    ],
    "Bakushining with a Classmate!": [
        "Power 5, Guts 5",
        "Speed 5, Wisdom 5"
    ],
    "The Best Bakushin!": [
        "Wisdom 10",
        "Stamina 5, Guts 5"
    ],
    "Bakushin Now and Forever!": [
        "Speed 10",
        "Guts 5, Wisdom 5",
        "Power 5"
    ],
    "Together with Someone Important!": [
        "Guts 10",
        "Speed 5, Stamina 5"
    ],
    "The Speed King": [
        "Power 5, Wisdom 5",
        "Stamina 10"
    ],
    "The Color of the Landscape": [
        "Guts 20",
        "Power 20"
    ],
    "Hobbies and Talents": [
        "Stamina 20",
        "Speed 10, Wisdom 10"
    ],
    "Umadol Special Class!": [
        "Speed 10, Power 10",
        "Guts 10, Wisdom 10"
    ],
    "Teaching Suzuka's Style": [
        "Speed 10",
        "Wisdom 10"
    ],
    "Party Time": [
        "Energy 10",
        "Stamina 5, Power 5"
    ],
    "On My Heels": [
        "Speed 5, Skill points 15",
        "Left-Handed 1"
    ],
    "White Temptation": [
        "Energy 10, Skill points 5",
        "Energy 30, Skill points 10"
    ],
    "My Little Snowscape": [
        "Stamina 10",
        "Wisdom 10"
    ],
    "To Make You Happy": [
        "Power 10",
        "Speed 5, Guts 5"
    ],
    "Our Little Snowscape": [
        "Stamina 10",
        "Speed 10",
        "Power 10"
    ],
    "How to Spend a Rainy Day": [
        "Guts 10",
        "Speed 5, Wisdom 5"
    ],
    "Are They Compatible?": [
        "Power 5, Guts 5",
        "Stamina 10"
    ],
    "How Should I Pose?": [
        "Power 20",
        "Skill points 40"
    ],
    "Wear Your Heart on Your Sleeve": [
        "Stamina 20",
        "Guts 20"
    ],
    "Today and Tomorrow Too": [
        "Speed 20",
        "Wisdom 20"
    ],
    "A Beautiful Day for Tennis": [
        "Speed 10",
        "Stamina 10"
    ],
    "Karaoke Connoisseur": [
        "Energy 10",
        "Power 10"
    ],
    "Early Afternoon Payback": [
        "Energy 5, Wisdom 5",
        "Pace Strategy 1"
    ],
    "Putting It Away at the Cafeteria": [
        "Energy 10, Skill points 5",
        "Energy 30, Skill points 10"
    ],
    "Because It's Special": [
        "Stamina 10",
        "Speed 10"
    ],
    "A Place I Want to Take You": [
        "Wisdom 10",
        "Stamina 10"
    ],
    "Someone I Respect": [
        "Skill points 30",
        "Stamina 5, Guts 5",
        "Speed 5, Power 5"
    ],
    "Research Fanatic": [
        "Tokyo Racecourse 1",
        "Nakayama Racecourse 1"
    ],
    "A Self-Satisfying Wish": [
        "Power 20",
        "Stamina 20"
    ],
    "Fill Life with Love": [
        "Speed 10, Stamina 10",
        "Wisdom 10"
    ],
    "Patience Is Key": [
        "Guts 20",
        "Stamina 10, Power 10"
    ],
    "One Day Experience Ceramics Class": [
        "Speed 5, Wisdom 5",
        "Stamina 10"
    ],
    "Find the Lost Child!": [
        "Energy -10, Stamina 10, Power 10",
        "Wisdom 10"
    ],
    "A Dangerous Treat": [
        "Guts 10, Skill points 15",
        "Corner Recovery 1"
    ],
    "Sweet Nighttime Temptation": [
        "Energy 30, Speed 10, Skill points 10",
        "Energy 10, Speed 5, Skill points 5"
    ],
    "For My Friends": [
        "Energy 10, Skill points 5",
        "Energy 30, Skill points 10"
    ],
    "Is Relaxing Being Spoiled?": [
        "Stamina 10",
        "Wisdom 10"
    ],
    "Dispel Your Anxieties": [
        "Power 10",
        "Speed 5, Guts 5"
    ],
    "Let's Share": [
        "Stamina 10",
        "Speed 10",
        "Power 10"
    ],
    "Rough Massage!": [
        "Guts 10",
        "Speed 5, Wisdom 5"
    ],
    "Stargazing is Better Together": [
        "Power 5, Guts 5",
        "Stamina 10"
    ],
    "Midway Reflection": [
        "Speed 20",
        "Power 20"
    ],
    "The Smiling Emperor's New Clothes": [
        "Wisdom 20",
        "Guts 20"
    ],
    "The Distant View from the End of the Road": [
        "Stamina 20",
        "Guts 20"
    ],
    "Those Who March Forth": [
        "Speed 5, Power 5",
        "Stamina 5, Guts 5"
    ],
    "The Emperor's Social Studies": [
        "Energy -10, Stamina 10, Power 10",
        "Wisdom 5, Skill points 15"
    ],
    "The Emperor's Spare Time": [
        "Wisdom 10, Skill points 15",
        "Rainy Days 1"
    ],
    "At Any Time": [
        "Energy -10, Guts 20",
        "Energy 10"
    ],
    "Sudden Kindness": [
        "Energy -10, Stamina 20",
        "Energy 10"
    ],
    "As Good As My Word": [
        "Energy -10, Power 20",
        "Energy 10"
    ],
    "The Emperor's Satiation": [
        "Energy 10, Skill points 5",
        "Energy 30, Skill points 10"
    ],
    "Birds of a Feather": [
        "Speed 10",
        "Stamina 10"
    ],
    "Well-Earned Respect": [
        "Wisdom 10",
        "Power 10"
    ],
    "A Clear and Beautiful Night": [
        "Speed 10",
        "Wisdom 10",
        "Stamina 10"
    ],
    "The Emperor's Daily Routine": [
        "Power 10",
        "Guts 10"
    ],
    "The Emperor's Path": [
        "Wisdom 10",
        "Power 10"
    ],
    "Quick Draw Showdown": [
        "Energy 10, Speed 10",
        "Energy 10, Wisdom 10"
    ],
    "Must Win Match": [
        "Wisdom 20",
        "Stamina 20"
    ],
    "To the Top!": [
        "Power 10, Guts 10",
        "Speed 10, Wisdom 10"
    ],
    "Hide and Seek": [
        "Speed 10",
        "Stamina 10"
    ],
    "Embracing Guidance": [
        "Power 10",
        "Energy 10"
    ],
    "Harvest Festival": [
        "Power 10, Skill points 15",
        "Prepared to Pass 1"
    ],
    "Serial Riddler": [
        "Mood -1",
        "Wisdom 10"
    ],
    "Taste of Home": [
        "Mood -1",
        "Wisdom 10"
    ],
    "Meaty Heaven": [
        "Energy 10, Skill points 5",
        "Energy 30, Skill points 10"
    ],
    "Rainy Power": [
        "Power 10",
        "Skill points 30"
    ],
    "Rainy Choice": [
        "Speed 5, Guts 5",
        "Stamina 5, Wisdom 5"
    ],
    "Rainy Rescue": [
        "Skill points 30",
        "Power 5, Wisdom 5",
        "Speed 5, Guts 5"
    ],
    "Let's Patrol!": [
        "Power 10",
        "Energy 10"
    ],
    "Going Home Together": [
        "Mood 1, Speed 5",
        "Mood 1, Stamina 5"
    ],
    "Fit for a King": [
        "Wisdom 20",
        "Power 20"
    ],
    "For My Admirer": [
        "Stamina 10, Guts 10",
        "Speed 20"
    ],
    "Strength of Will": [
        "Wisdom 20",
        "Speed 10, Power 10"
    ],
    "Fantastic Voyeur": [
        "Power 10",
        "Wisdom 10"
    ],
    "Blinding Beauty": [
        "Energy -10, Power 20",
        "Speed 10"
    ],
    "Bring Me Your Finest": [
        "Speed 10, Skill points 15",
        "Non-Standard Distance 1"
    ],
    "Battle of Kings - The Great Ramen War": [
        "Energy 10, Skill points 5",
        "Energy 30, Skill points 10"
    ],
    "The Princess in Pajamas": [
        "Speed 10",
        "Stamina 10"
    ],
    "What the Mirror Reflects": [
        "Wisdom 10",
        "Guts 10"
    ],
    "My Radiance is Yours": [
        "Power 10",
        "Guts 10",
        "Wisdom 10"
    ],
    "Maintaining Magnificence": [
        "Speed 10",
        "Wisdom 10"
    ],
    "Evening Opera Theater": [
        "Power 10",
        "Energy 10"
    ],
    "Good Luck Charm": [
        "Stamina 20",
        "Wisdom 20"
    ],
    "Selfish Teio and a Nostalgic View": [
        "Guts 20",
        "Speed 10, Power 10"
    ],
    "Racewear Like Prez": [
        "Speed 10, Wisdom 10",
        "Stamina 10, Guts 10"
    ],
    "Empress vs Monarch": [
        "Guts 10",
        "Skill points 30"
    ],
    "Cupcakes for All": [
        "Energy 5, Mood 1",
        "Speed 5, Power 5"
    ],
    "Teio's Warrior Training": [
        "Guts 10, Skill points 15",
        "Prepared to Pass 1"
    ],
    "Karaoke Power?": [
        "Guts 10",
        "Speed 10"
    ],
    "Teio an Umadol?!": [
        "Power 10",
        "Speed 10"
    ],
    "Secret to Strength": [
        "Energy 10, Skill points 5",
        "Energy 30, Skill points 10"
    ],
    "I Got Praised!": [
        "Stamina 10",
        "Speed 10"
    ],
    "I Got Scolded!": [
        "Wisdom 10",
        "Power 5, Guts 5"
    ],
    "I Figured It Out!": [
        "Speed 5, Stamina 5",
        "Guts 5, Wisdom 5",
        "Power 10"
    ],
    "Grown Up Time": [
        "Guts 10",
        "Wisdom 10"
    ],
    "Punny Prez": [
        "Stamina 5, Power 5",
        "Speed 10"
    ],
    "Vintage Style": [
        "Power 20",
        "Stamina 20"
    ],
    "Making so of a Friend": [
        "Speed 20",
        "Guts 20"
    ],
    "Hot and Cool": [
        "Speed 20",
        "Speed 10, Power 10"
    ],
    "Like a Kid": [
        "Speed 10",
        "Power 10"
    ],
    "Challenging Fate": [
        "Stamina 10",
        "Speed 10"
    ],
    "Showdown by the River!": [
        "Wisdom 10, Skill points 15",
        "Shifting Gears 1"
    ],
    "Awkward Honesty": [
        "Energy 10, Skill points 5",
        "Energy 30, Skill points 10"
    ],
    "The Standards of Coolness": [
        "Wisdom 10",
        "Guts 10"
    ],
    "Ring Out Passionate Sound!": [
        "Speed 10",
        "Stamina 10"
    ],
    "The Way of Cool": [
        "Power 10",
        "Speed 10",
        "Stamina 5, Guts 5"
    ],
    "Let's Take a Little Detour": [
        "Speed 10",
        "Energy 5, Mood 1"
    ],
    "Sugar and Spice": [
        "Energy 5",
        "Power 10"
    ],
    "Full Power Testing!": [
        "Guts 20",
        "Speed 20"
    ],
    "Full Power Fashion!": [
        "Stamina 20",
        "Power 10, Guts 10"
    ],
    "Full Power Effort!": [
        "Speed 10, Wisdom 10",
        "Power 20"
    ],
    "Rain or Shine": [
        "Energy -10, Stamina 10, Skill points 15",
        "Power 10"
    ],
    "Overcome the Towering Obstacle!": [
        "Mood 1, Guts 5",
        "Mood 1, Power 5"
    ],
    "A Fresh Perspective": [
        "Speed 10, Skill points 15",
        "Nimble Navigator 1"
    ],
    "Full Power Eating!": [
        "Energy 10, Skill points 5",
        "Energy 30, Skill points 10"
    ],
    "Play of the Three Kingdoms": [
        "Stamina 5, Skill points 15",
        "Power 5, Skill points 15"
    ],
    "Futsal Now?!": [
        "Guts 10",
        "Speed 10"
    ],
    "The Last Ticket": [
        "Guts 10",
        "Speed 10",
        "Power 10"
    ],
    "Shake Off Your Blues!": [
        "Mood 1, Power 5",
        "Speed 5, Skill points 15"
    ],
    "Big Girls Cry Too": [
        "Guts 5, Skill points 15",
        "Mood 1, Power 5"
    ],
    "Exhilarating! What a Scoop!": [
        "Stamina 10",
        "Guts 10"
    ],
    "A Trainer's Knowledge": [
        "Power 10",
        "Speed 10"
    ],
    "Best Foot Forward!": [
        "Energy -10, Power 20, Guts 20, Beeline Burst 1",
        "Energy 30, Stamina 20, Breath of Fresh Air 1"
    ],
    "Get Well Soon!": [
        "Mood -1, Last trained stat -5, Chance to get Practice Poor -1",
        "(85/15) |Mood -1, Last trained stat -10, Chance to get Practice Poor -1| OR |Practice Perfect 1|"
    ],
    "Don't Overdo It!": [
        "Energy 10, Mood -2, Last trained stat -10, 2 Random stats -10, Chance to get Practice Poor -1",
        "(95/5) |Mood -3, Last trained stat -10, 2 Random stats -10, Practice Poor -1| OR |Energy 10, Practice Perfect 1|"
    ],
    "Extra Training": [
        "Energy -5, Last trained stat 5,  |(random) Heal a negative status effect|",
        "Energy 5"
    ],
    "At Summer Camp Year 2": [
        "Power 10",
        "Guts 10"
    ],
    "Dance Lesson": [
        "Power 10",
        "Speed 10"
    ],
    "New Year's Resolutions": [
        "(Depends on the horse)",
        "Energy 20",
        "Skill points 20"
    ],
    "Acupuncture - Just an Acupuncturist No Worries!": [
        "(50/50) |All stats 20| OR |Mood -2, All stats -15, Night Owl -1|",
        "(60/40) |Corner Recovery OBTAIN, Straightaway Recovery OBTAIN| OR |Energy -20, Mood -2|",
        "(80/20) |Maximum Energy 12, Energy 40, Heal all negative status effects| OR |Energy -20, Mood -2, (random) Practice Poor -1|",
        "(90/10) |Energy 20, Mood 1, Charming 1| OR |Energy -10/-20, Mood -1, (random) Practice Poor -1|",
        "Energy 10"
    ],
    "Victory!": [
        "Energy -15/-25 (The higher the placement, the lower the chance of losing more energy)",
        "Energy -5/-35 (The higher the placement, the lower the chance of losing more energy)"
    ],
    "Solid Showing": [
        "Energy -20",
        "Energy -30"
    ],
    "Defeat": [
        "Energy -25",
        "Energy -35"
    ],
    "Etsuko's Exhaustive Coverage": [
        "Energy -25",
        "Energy -35"
    ],
    "Run Away to First Base": [
        "Energy -15, Stamina 10, Guts 10",
        "Energy -15, Guts 10, Wisdom 10"
    ],
    "Runaway Romance": [
        "Energy 10, Guts 5, Wisdom 5",
        "Energy 10, Front Runner Savvy 1"
    ],
    "Optimistic Escapism: Never Give Up!": [
        "Energy -20, Stamina 5, Guts 5, |Vanguard Spirit 3| or |Keeping the Lead 1/3|",
        "Energy 10, Lone Wolf 1"
    ],
    "An Inescapable Choice?": [
        "Energy -15, Guts 20",
        "Power 5, Skill points 15"
    ],
    "Optimistic Escapism": [
        "Guts 15",
        "Wet Conditions 1"
    ],
    "Ikuno-Style Support": [
        "Wisdom 15, Frenzied Front Runners 3",
        "Wisdom 15, Frenzied Front Runners 3"
    ],
    "Ikuno-Style Flawless Method": [
        "Wisdom 10",
        "Skill points 30"
    ],
    "Ikuno-Style Management": [
        "Stamina 20",
        "Trick (Rear) 1"
    ],
    "I'm Not Afraid!": [
        "(0/0) |Speed 10| OR |Energy -10, Speed 10|",
        "Energy 20"
    ],
    "Can't Catch Me!": [
        "(0/0) |Speed 15, Leader's Pride 3| OR |Energy -10, Speed 10|",
        "Energy 25"
    ],
    "Turbo Is Strong!": [
        "(0/0) |Energy -10, Speed 25, Taking the Lead 3| OR |Energy -10, Speed 5, Early Lead 1|",
        "Energy 15, Watchful Eye 1"
    ],
    "Just Start Running!": [
        "Mood -1, Speed 20",
        "Energy -10, Power 20"
    ],
    "I'm All Fired Up!": [
        "Energy 15",
        "Early Lead 1"
    ],
    "BFF Party!": [
        "Power 10",
        "Speed 10"
    ],
    "LOL Party! Round2": [
        "Power 10, Straight Descent 1/3",
        "Energy 20, Watchful Eye 1"
    ],
    "Encounter With the Sun": [
        "Power 10",
        "Hot Topic 1"
    ],
    "Smiles Forever": [
        "Speed 5, Power 10",
        "Long Shot 1"
    ],
    "Some Very Green Friends": [
        "Speed 5, Skill points 10, Lucky Seven 1",
        "Mood -1, Maverick 1"
    ],
    "Premeditated Mischief": [
        "Speed 10, Skill points 20, Levelheaded 1",
        "Mood -1, Lone Wolf 1"
    ],
    "Miracle Escape!": [
        "Energy 10, Speed 5",
        "Energy -10, Speed 20"
    ],
    "Wonderful Mistake!": [
        "(0/0) |Energy -15, Skill points 40| OR |Energy -20, Skill points 40|",
        "Charming 1"
    ],
    "Just a Little Closer": [
        "Energy -10, Speed 15",
        "Energy -10, Skill points 20",
        "Energy -10, Shake It Out 1"
    ],
    "A Roller Coaster of Feelings!": [
        "Energy -10, Speed 5, Stamina 5, Guts 10",
        "Energy 20, Wisdom 10"
    ],
    "Watch Where You're Going!": [
        "Extra Tank 1",
        "Guts 15"
    ],
    "So Many Options!": [
        "Energy 10, Mood 1",
        "Energy -10, Stamina 15, Skill points 15"
    ],
    "On and On": [
        "Speed 10, Stamina 5",
        "Speed 15"
    ],
    "What Should I Do?": [
        "Speed 5, Stamina 5, Wisdom 5",
        "Left-Handed 1"
    ],
    "My Way Or": [
        "Mood 1, Skill points 15",
        "Guts 15"
    ],
    "My Weapon": [
        "Mood 1, Guts 10",
        "Pace Chaser Straightaways 1"
    ],
    "For an Adorable Younger Student": [
        "Early Lead 1",
        "Energy 5, Speed 10"
    ],
    "Drive Destination": [
        "Mood 1, Speed 5",
        "Mood 1, Wisdom 5"
    ],
    "What I Want to Say": [
        "(0/0) |Power 10, Guts 5, Skill points 10, Furious Feat 1| OR |Power 15, Guts 10, Skill points 15, Furious Feat 3|",
        "Energy 30"
    ],
    "How Should I Respond?": [
        "if the event is a chain event (>>) use the top options as reference",
        ">> Power 5, Skill points 10, Stamina to Spare 1",
        ">> Stamina 5, Skill points 10, Outer Swell 1",
        "Energy 5, Power 5",
        "Energy -10, Guts 15"
    ],
    "Conquering the Crowds": [
        "Power 5, Skill points 15",
        "Nakayama Racecourse 1"
    ],
    "Adventurer Gold Ship": [
        "Stamina 15",
        "Guts 10, Skill points 15"
    ],
    "Revive the Brand! Golshi's Yakisoba": [
        "Mood 1, Stamina 5",
        "Hanshin Racecourse 1"
    ],
    "The Coolest Line": [
        "Power 10",
        "Power 5, Skill points 15"
    ],
    "Enemies on Main Street": [
        "Nimble Navigator 1",
        "Power 5, Skill points 15"
    ],
    "Yes! Let's Hug": [
        "Speed 10",
        "Speed 5, Power 5"
    ],
    "Yeehaw! Party Tonight": [
        "Energy -10, Speed 5, Power 10",
        "Prepared to Pass 1"
    ],
    "A Moment's Respite": [
        "Energy 15",
        "(0/0) |Energy -10, Power 5, Guts 5, Wisdom 5| OR |Power 5, Guts 5, Wisdom 10|"
    ],
    "Library Vexation": [
        "Wisdom 10",
        "Guts 5, Wisdom 5"
    ],
    "A Friendly Daytime Discussion": [
        "Frenzied Pace Chasers 1",
        "Target in Sight 1"
    ],
    "To Maintain My Weight": [
        "Energy -10, Stamina 15",
        "Maximum Energy 4, Stamina 5"
    ],
    "To Reach the Greatest Heights": [
        "Stamina 5, Guts 5",
        "Early Lead 1"
    ],
    "Umame": [
        "Energy 30",
        "Stamina to Spare 1"
    ],
    "Blazing Fire!": [
        "Stamina 10",
        "Energy -10, Power 20"
    ],
    "Secret Notebook!": [
        "Power 10",
        "Sunny Days 1"
    ],
    "Uma-me": [
        "Energy 30",
        "Stamina to Spare 1"
    ],
    "Etude to Victory": [
        "Mood -1, Speed 5, Skill points 30",
        "Power 5, Skill points 15"
    ],
    "Beyond Our Limited Time": [
        "Energy 10, Skill points 15",
        "Non-Standard Distance 1"
    ],
    "The Emperor's Encouragement": [
        "Speed 10",
        "Energy -10, Skill points 30"
    ],
    "The Student Council President's Thoughtfulness": [
        "Rainy Days 1",
        "Stamina 15"
    ],
    "Be Strategic": [
        "Energy 10, Wisdom 5",
        "Skill points 30, Second Wind 1, bond -5"
    ],
    "Recruiting Cat Catchers": [
        "Energy 10, Wisdom 5",
        "Energy -10, Speed 15, Stamina 5"
    ],
    "Recruiting Advisors": [
        "Wisdom 15",
        "Keeping the Lead 1"
    ],
    "A Page of Flower Shop Assistance": [
        "Mood 2",
        "Stamina 10"
    ],
    "A Page About Cloudy Weather": [
        "Speed 5, Guts 5",
        "Firm Conditions 1"
    ],
    "Full Power Muscles!": [
        "Stamina 5, Skill points 15",
        "Mood 1, Skill points 15"
    ],
    "Full Power Racing!": [
        "Late Surger Corners 1",
        "Skill points 30"
    ],
    "Crap I Overslept": [
        "Mood -1, Skill points 45",
        "Energy 10, Wisdom 5"
    ],
    "Lunch Break Gotta Get My Together": [
        "Skill points 30",
        "A Small Breather 1"
    ],
    "Genius Efficiency!": [
        "Speed 15",
        "Speed 5, Power 10"
    ],
    "Enough to Break into a Dash!": [
        "Gap Closer 1",
        "Energy -10, Speed 10, Power 5"
    ],
    "Leave it to Me to Help Out!": [
        "Energy 15",
        "Stamina 10"
    ],
    "Leave it to Me to Be Considerate!": [
        "Deep Breaths 1",
        "Energy 10, Stamina 5"
    ],
    "Urara's Study Review": [
        "Energy 10, Wisdom 5",
        "Mood 1, Wisdom 5"
    ],
    "Uraras Long Shot Dash!": [
        "Long Shot 1",
        "Mood 1, Energy 10"
    ],
    "Memories of Cinema": [
        "Energy 25, Stamina 5, Mood 1",
        "Stamina 10, Guts 10, Mood 1"
    ],
    "My Chosen Way of Life": [
        "Energy 14, Mood 1",
        "Mood 1, Wisdom 6"
    ],
    "Enthusiastic Pair": [
        "Energy 14, Wisdom 6, Mood 1, Can start dating",
        "Mood -1, bond -5, Watchful Eye 1, Chain ended"
    ],
    "How I Play at the Park": [
        "Energy 35, Wisdom 6",
        "(0/0) |Skill Points 18| OR |Speed 6, Skill points 56, Mood 1|"
    ],
    "Trainer Tip Always Improve Your Coaching": [
        "Energy 10, Skill Points 15",
        "Speed 5, Wisdom 5"
    ],
    "The Search for a Hobby": [
        "Energy 20, Skill Points 15, Mood 1, Can start dating",
        "Mood -1, Maverick 1, bond -5, Chain ended"
    ],
    "I'm Going to Win Tomorrow!": [
        "Wisdom 10",
        "Mood 1, Skill Points 15"
    ],
    "This Is Nothing!": [
        "Stamina to Spare 1",
        "Energy 20, Mood 1"
    ],
    "Hishiama's Struggles Problem Children": [
        "Energy 10, Wisdom 5",
        "Energy -10, Speed 10, Guts 5"
    ],
    "Hishiama's Struggles: Final Stretch": [
        "Hesitant End Closers 1",
        "Power 5, Skill Points 15"
    ],
    "Strict but Gracious": [
        "Go with the Flow 1",
        "Energy 10, Wisdom 10"
    ],
    "Agile but Strong": [
        "Power 15",
        "Speed 10, Stamina 5"
    ],
    "Umamusume Deficiency!": [
        "Energy 5, Speed 5",
        "Speed 5, Power 5"
    ],
    "Heavy Romance": [
        "Rainy Days 1",
        "Wet Conditions 1"
    ],
    "Tamamo's School Tour": [
        "Wisdom 10",
        "Stamina 5, Guts 5"
    ],
    "A Battle I Can't Lose!": [
        "Calm in a Crowd 1",
        "Stamina 5, Wisdom 5"
    ],
    "Lovely Training Weather": [
        "Wisdom 5, Skill Points 20",
        "Speed 10, Stamina 5",
        "Practice Perfect 1"
    ],
    "Wonderful New Shoes": [
        "Speed 5, Skill Points 10",
        "Energy -10, Stamina 5, Skill Points 20"
    ],
    "Reminiscent Clover": [
        "Corner Adept 1",
        "Guts 15"
    ],
    "Last-Minute Modal Theory": [
        "Power 15",
        "Speed 10, Skill Points 15"
    ],
    "Step-Out-of-Your-Comfort-Zone Theory": [
        "Energy -10, Inside Scoop 1",
        "Energy 10, Stamina 10"
    ],
    "Snack Advice for Mayano!": [
        "Stamina 5, Guts 5",
        "Stamina 10"
    ],
    "Fashion Advice for Mayano!": [
        "Straightaway Adept 1",
        "Stamina 10"
    ],
    "Solo Nighttime Run": [
        "Stamina 10",
        "Energy 10, Stamina 5"
    ],
    "A Taste of Silence": [
        "Stamina 5, Skill Points 15",
        "Non-Standard Distance 1"
    ],
    "I'm Not a Cyborg": [
        "Guts 10, Skill Points 15",
        "Energy -10, Corner Recovery 1, bond -5, Chain ended"
    ],
    "Do No Harm": [
        "Energy -10, Stamina 5, Power 15",
        "Energy 10, Wisdom 5"
    ],
    "Orders Must Be Followed": [
        "Focus 1",
        "Speed 10, Skill Points 15"
    ],
    "My Muscles and Me Onward to Tomorrow!": [
        "Energy -10, Power 15",
        "Energy 4, Power 5"
    ],
    "It's Not Like I Like Romance!": [
        "Pace Strategy 1",
        "Energy 30"
    ],
    "For a Spiffy Concert": [
        "Guts 10",
        "Energy -10, Guts 15"
    ],
    "Aiming for the City Spots": [
        "Energy -10, Mood 1, Guts 10",
        "Corner Acceleration 1"
    ],
    "It's a Game of Tag!": [
        "Energy 10, Speed 5",
        "Fast-Paced 1"
    ],
    "Full-Power Muscles!": [
        "Late Surger Corners 1",
        "Skill points 30"
    ],
    "Full-Power Muscles!": [
        "Stamina 5, Skill points 15",
        "Mood 1, Skill points 15"
    ],
    "Ten Minutes Left!": [
        "Guts 15",
        "Wisdom 10"
    ],
    "The Correlation between Sleep and Efficiency": [
        "Power 5, Wisdom 5",
        "Wisdom 10"
    ],
    "Happenstance Introduced Through Intervention": [
        "Late Surger Savvy 1",
        "Wisdom 10"
    ],
    "Verification Required": [
        "Energy 10, Guts 5",
        "Energy -10, Stamina 5, Guts 10"
    ],
    "Absolute Desire": [
        "Pace Strategy 1",
        "Maximum Energy 4, Guts 5"
    ],
    "Unforeseen Lunch": [
        "Energy 15",
        "Speed 5, Guts 5"
    ],
    "Responding to the Unforeseen": [
        "Guts 10",
        "Target in Sight 1"
    ],
    "Always on Stage": [
        "Wisdom 10",
        "Energy 25, Focus 1, Chain ended"
    ],
    "Chants Are the Life of a Concert": [
        "Stamina 5, Guts 10",
        "Wisdom 15"
    ],
    "If I'm Cute Come to My Show!": [
        "Energy -10, Power 10, Final Push 1",
        "Energy 10, Wisdom 5"
    ],
    "Just Leave Me Alone": [
        "Stamina 5, Skill Points 15",
        "Power 5, Skill Points 15"
    ],
    "Just Don't Bother Me": [
        "Pressure 1",
        "Skill Points 30"
    ],
    "Aspiring to Adulthood": [
        "Energy -10, Wisdom 20",
        "Wisdom 5, Skill Points 15"
    ],
    "Warmth Love and Lunch": [
        "Charming 1",
        "Energy 20"
    ],
    "Let's Bloom Beautifully": [
        "Wisdom 15",
        "Speed 10, Power 5"
    ],
    "A Hero's Woes": [
        "Energy 15",
        "Energy 5, Power 5"
    ],
    "Preparing My Special Move!": [
        "Sprint Straightaways 1",
        "Energy 30"
    ],
    "Marvelous No Question": [
        "Energy 10, Speed 5",
        "Mood 1, Speed 5"
    ],
    "How To Be More Marvelous": [
        "Energy 10, Mood 1",
        "Hanshin Racecourse 1"
    ],
    "Guidance and Friends": [
        "Skill Points 45",
        "(0/0) |Energy 10, Mood 1, Right-Handed 3| OR |Energy -20, Right-Handed 1|"
    ],
    "Maximum Spirituality": [
        "Wisdom 5, Skill Points 15",
        "Energy -10, Speed 5, Stamina 5, Power 5"
    ],
    "When Piety and Kindness Intersect": [
        "Skill Points 30",
        "Energy 20"
    ],
    "What I'm Destined For": [
        "Energy 10, Guts 5",
        "(0/0) |Energy -10, Wisdom 5| OR |Maximum Energy 4, Mood 1, Guts 5, Wisdom 5|"
    ],
    "I Will Change": [
        "Energy 10, Mood 1",
        "Guts 15"
    ],
    "Please Buy Some Carrots": [
        "Energy 10, Wisdom 5",
        "Pace Chaser Corners 1"
    ],
    "Give It a Try": [
        "Energy 15",
        "Mood 1, Skill Points 15"
    ],
    "Hope She'll Like It": [
        "Skill Points 45",
        "Unyielding Spirit 1"
    ],
    "Not like Meow": [
        "Energy 20",
        "Energy 10, Wisdom 5"
    ],
    "Chasing Their Backs": [
        "Energy 5, Wisdom 3",
        "bond 20"
    ],
    "Delicious Burden": [
        "Ramp Up 1",
        "Mood 1, Energy 4"
    ],
    "You May Socialize With Me!": [
        "Energy -20, Speed 10, Power 10, Wisdom 5",
        "Mood -1, Guts 25"
    ],
    "You May Advise Me!": [
        "Guts 10, Wisdom 5",
        "Homestretch Haste 1"
    ],
    "Sleight of Hand": [
        "Wisdom 5, Skill Points 15",
        "Power 5, Skill Points 15"
    ],
    "Seeking Uniqueness!": [
        "Mood 1",
        "Energy 10/30"
    ],
    "Just A Typical Accident?!": [
        "Stamina 5, Guts 10",
        "Subdued Front Runners 1"
    ],
    "Just Your Typical Hard Work!": [
        "Speed 10",
        "Power 10"
    ],
    "Misdirection": [
        "Prepared to Pass 1",
        "Skill Points 30"
    ],
    "Diamond Fixation": [
        "Wisdom 5",
        "(0/0) |Energy 15 Stamina 10| OR |Mood -1, Guts 20|"
    ],
    "Only for You": [
        "Energy -20, Stamina 30, Iron Will 1",
        "Energy 5, Guts 5, Iron Will 1"
    ],
    "I Love New Things!": [
        "Guts 10",
        "Energy -10, Stamina 20"
    ],
    "I Love Complicated Things!": [
        "Stamina 5, Guts 10",
        "Hesitant Front Runners 1"
    ],
    "Paying It Forward": [
        "Energy 10, Mood 1",
        "Speed 5/10, Straightaway Adept 1"
    ],
    "Ah Home Sweet Home": [
        "Speed 5, Power 10",
        "Practice Perfect 1"
    ],
    "Ah Friendship": [
        "Mood 1, Power 5",
        "Energy 10"
    ],
    "Copythisformore": [
        "",
        ""
    ],
}
colored_terms = {
    # ===== CONDITIONS =====
    # Negative Conditions (Blue)
    "Migraine": "#0066CC",
    "Night Owl": "#0066CC",
    "Skin Outbreak": "#0066CC",
    "Slacker": "#0066CC",
    "Slow Metabolism": "#0066CC",
    "Under the Weather": "#0066CC",
    "Practice Poor": "#0066CC",
    
    # Positive Conditions (Orange)
    "Practice Perfect": "#FF8C00",
    "Charming": "#FF8C00",
    "Fast Learner": "#FF8C00",
    "Hot Topic": "#FF8C00",
    "Shining Brightly": "#FF8C00",
    
    # ===== OTHER TERMS =====
    "Mood": "#63019B",
    "OR": "#22009E",
    "Skill": "#0066CC",
    "Skill points": "#0066CC",
    
    # ===== POSITIVE SKILLS (Orange) =====
    # Rare Speed Skills
    "Technician": "#FF8C00",
    "Lightning Step": "#FF8C00",
    "Vanguard Spirit": "#FF8C00",
    "Professor of Curvature": "#FF8C00",
    "The Coast Is Clear!": "#FF8C00",
    "Concentration": "#FF8C00",
    "Unrestrained": "#FF8C00",
    "Killer Tunes": "#FF8C00",
    "Furious Feat": "#FF8C00",
    "In Body and Mind": "#FF8C00",
    "Changing Gears": "#FF8C00",
    "Step on the Gas!": "#FF8C00",
    "Corner Connoisseur": "#FF8C00",
    "Mile Maven": "#FF8C00",
    "Speed Star": "#FF8C00",
    "Determined Descent": "#FF8C00",
    "Taking the Lead": "#FF8C00",
    "On Your Left!": "#FF8C00",
    "Clairvoyance": "#FF8C00",
    "Lane Legerdemain": "#FF8C00",
    "No Stopping Me!": "#FF8C00",
    "Rising Dragon": "#FF8C00",
    "Hard Worker": "#FF8C00",
    "Fast & Furious": "#FF8C00",
    "Turbo Sprint": "#FF8C00",
    "Staggering Lead": "#FF8C00",
    "Blinding Flash": "#FF8C00",
    "The Bigger Picture": "#FF8C00",
    "Rushing Gale!": "#FF8C00",
    "Escape Artist": "#FF8C00",
    "Unyielding": "#FF8C00",
    "Center Stage": "#FF8C00",
    "Plan X": "#FF8C00",
    "Beeline Burst": "#FF8C00",
    
    # Normal Speed Skills
    "Prudent Positioning": "#FF8C00",
    "Go with the Flow": "#FF8C00",
    "Thunderbolt Step": "#FF8C00",
    "Shrewd Step": "#FF8C00",
    "Keeping the Lead": "#FF8C00",
    "Long Corners": "#FF8C00",
    "Corner Adept": "#FF8C00",
    "Pace Chaser Corners": "#FF8C00",
    "Pressure": "#FF8C00",
    "I Can See Right Through You": "#FF8C00",
    "Uma Stan": "#FF8C00",
    "Focus": "#FF8C00",
    "Final Push": "#FF8C00",
    "Fast-Paced": "#FF8C00",
    "Up-Tempo": "#FF8C00",
    "Prepared to Pass": "#FF8C00",
    "Slick Surge": "#FF8C00",
    "Updrafters": "#FF8C00",
    "Straightaway Acceleration": "#FF8C00",
    "Mile Straightaway": "#FF8C00",
    "Homestretch Haste": "#FF8C00",
    "Steadfast": "#FF8C00",
    "Outer Swell": "#FF8C00",
    "Straightaway Adept": "#FF8C00",
    "Early Lead": "#FF8C00",
    "Shifting Gears": "#FF8C00",
    "Acceleration": "#FF8C00",
    "Corner Acceleration": "#FF8C00",
    "Nimble Navigator": "#FF8C00",
    "Productive Plan": "#FF8C00",
    "Straight Descent": "#FF8C00",
    "Highlander": "#FF8C00",
    "Front Runner Straightaways": "#FF8C00",
    "Front Runner Corners": "#FF8C00",
    "Position Pilfer": "#FF8C00",
    "Pace Chaser Straightaways": "#FF8C00",
    "Hawkeye": "#FF8C00",
    "Leader's Pride": "#FF8C00",
    "Ramp Up": "#FF8C00",
    "Medium Straightaways": "#FF8C00",
    "Medium Corners": "#FF8C00",
    "Fighter": "#FF8C00",
    "Late Surger Corners": "#FF8C00",
    "Sprinting Gear": "#FF8C00",
    "Huge Lead": "#FF8C00",
    "Countermeasure": "#FF8C00",
    "1,500,000 CC": "#FF8C00",
    "Studious": "#FF8C00",
    "Gap Closer": "#FF8C00",
    "Unyielding Spirit": "#FF8C00",
    "Straightaway Spurt": "#FF8C00",
    "Inside Scoop": "#FF8C00",
    "Strategist": "#FF8C00",
    "Groundwork": "#FF8C00",
    "Tail Held High": "#FF8C00",
    "Second Wind": "#FF8C00",
    "Slipstream": "#FF8C00",
    "Playtime's Over!": "#FF8C00",
    "Sprint Straightaways": "#FF8C00",
    "Sprint Corners": "#FF8C00",
    "Meticulous Measures": "#FF8C00",
    "Mile Corners": "#FF8C00",
    "End Closer Straightaways": "#FF8C00",
    "Masterful Gambit": "#FF8C00",
    "Long Straightaways": "#FF8C00",
    "Late Surger Straightaways": "#FF8C00",
    "End Closer Corners": "#FF8C00",
    "Tactical Tweak": "#FF8C00",
    "Dodging Danger": "#FF8C00",
    
    # Rare Passive Skills
    "Super Lucky Seven": "#008A29",
    
    # Rare Recovery Skills
    "Calm and Collected": "#008CA5",
    "Go-Home Specialist": "#008CA5",
    "Race Planner": "#008CA5",
    "Breath of Fresh Air": "#008CA5",
    "Gourmand": "#008CA5",
    "Cooldown": "#008CA5",
    "Trackblazer": "#008CA5",
    "Swinging Maestro": "#008CA5",
    "Iron Will": "#008CA5",
    "Indomitable": "#008CA5",
    "Restless": "#008CA5",
    "Keen Eye": "#008CA5",
    "Unruffled": "#008CA5",
    "Adrenaline Rush": "#008CA5",
    "Miraculous Step": "#008CA5",
    
    # Normal Passive Skills
    "Spring Runner": "#008A29",
    "Left-Handed": "#008A29",
    "Competitive Spirit": "#008A29",
    "Wet Conditions": "#008A29",
    "Cloudy Days": "#008A29",
    "Pace Chaser Savvy": "#008A29",
    "Non-Standard Distance": "#008A29",
    "Rainy Days": "#008A29",
    "Standard Distance": "#008A29",
    "Firm Conditions": "#008A29",
    "Long Shot": "#008A29",
    "Lucky Seven": "#008A29",
    "Kokura Racecourse": "#008A29",
    "Outer Post Proficiency": "#008A29",
    "Late Surger Savvy": "#008A29",
    "Front Runner Savvy": "#008A29",
    "End Closer Savvy": "#008A29",
    "Sympathy": "#008A29",
    "Hanshin Racecourse": "#008A29",
    "Tokyo Racecourse": "#008A29",
    "Nakayama Racecourse": "#008A29",
    "Target in Sight": "#008A29",
    "Sunny Days": "#008A29",
    "Inner Post Proficiency": "#008A29",
    "Right-Handed": "#008A29",
    "Fall Runner": "#008A29",
    "Sapporo Racecourse": "#008A29",
    "Oi Racecourse": "#008A29",
    "Summer Runner": "#008A29",
    "Snowy Days": "#008A29",
    "Winter Runner": "#008A29",
    "Lone Wolf": "#008A29",
    "Maverick": "#008A29",
    "Hakodate Racecourse": "#008A29",
    "Kyoto Racecourse": "#008A29",
    
    # Normal Recovery Skills
    "Soft Step": "#008CA5",
    "Stamina to Spare": "#008CA5",
    "Hydrate": "#008CA5",
    "Preferred Position": "#008CA5",
    "After-School Stroll": "#008CA5",
    "Standing By": "#008CA5",
    "Rosy Outlook": "#008CA5",
    "Straightaway Recovery": "#008CA5",
    "Deep Breaths": "#008CA5",
    "Corner Recovery": "#008CA5",
    "Pace Strategy": "#008CA5",
    "Lay Low": "#008CA5",
    "A Small Breather": "#008CA5",
    "Triple 7s": "#008CA5",
    "Extra Tank": "#008CA5",
    "Calm in a Crowd": "#008CA5",
    "Moxie": "#008CA5",
    "Levelheaded": "#008CA5",
    "Watchful Eye": "#008CA5",
    "Wait-and-See": "#008CA5",
    "Passing Pro": "#008CA5",
    "Shake It Out": "#008CA5",
    
    # ===== UNIQUE SKILLS (Orange) =====
    "Introduction to Physiology": "#CC00FF",
    "Empress's Pride": "#CC00FF",
    "∴win Q.E.D.": "#CC00FF",
    "Red Ace": "#CC00FF",
    "Corazón ☆ Ardiente": "#CC00FF",
    "Warning Shot!": "#CC00FF",
    "Focused Mind": "#CC00FF",
    "Super-Duper Stoked": "#CC00FF",
    "Call Me King": "#CC00FF",
    "Red Shift/LP1211-M": "#CC00FF",
    "Luck Be with Me!": "#CC00FF",
    "1st Place Kiss☆": "#CC00FF",
    "Legacy of the Strong": "#CC00FF",
    "The Duty of Dignity Calls": "#CC00FF",
    "Feel the Burn!": "#CC00FF",
    "G00 1st. F∞;": "#CC00FF",
    "I Can Win Sometimes, Right?": "#CC00FF",
    "Triumphant Pulse": "#CC00FF",
    "Blue Rose Closer": "#CC00FF",
    "Class Rep + Speed = Bakushin": "#CC00FF",
    "The View from the Lead is Mine!": "#CC00FF",
    "Shooting Star": "#CC00FF",
    "Clear Heart": "#CC00FF",
    "Behold Thine Emperor's Divine Might": "#CC00FF",
    "This Dance Is for Vittoria!": "#CC00FF",
    "Shooting for Victory!": "#CC00FF",
    "Certain Victory": "#CC00FF",
    "Sky-High Teio Step": "#CC00FF",
    "Xceleration": "#CC00FF",
    "V Is for Victory!": "#CC00FF"
}
positive_color = "#009900"
negative_color = "#FF0000"

all_skills = {**positive_conditions, **negative_conditions, **Positive_skills, **Unique_skills}

Width = GetSystemMetrics(0)
Height = GetSystemMetrics(1)

REGION = (0, 0, Width/3, Height/3)

class SupportOptionsApp:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.overrideredirect(True)
        self.ventana.attributes("-topmost", True)
        self.ventana.attributes("-transparentcolor", "white")
        self.ventana.config(bg='white')
        self.ventana.withdraw()
        self.evento_terminar = threading.Event()

        self.frame = Frame(self.ventana, bg='white')
        self.frame.pack(padx=10, pady=10)

        self.mostrando = False
        self.opciones_actuales = []
        self.listener = None

        self.create_system_tray_icon()

        self.hilo_deteccion = threading.Thread(target=self.revisar_texto)
        self.hilo_deteccion.daemon = True
        self.hilo_deteccion.start()

        self.ventana.mainloop()

    def create_system_tray_icon(self):
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "icon.ico")
        try:
            image = Image.open(icon_path).resize((16, 16))
        except Exception as e:
            print(f"No se pudo cargar el icono: {e}. Usando icono por defecto")
            image = Image.new('RGB', (16, 16), color='black')
            draw = ImageDraw.Draw(image)
            draw.text((4, 2), "O", fill="orange")

        menu = pystray.Menu(
            pystray.MenuItem("Cerrar", self.cerrar_aplicacion)
        )

        self.icon = pystray.Icon(
            "umamusume_support",
            image,
            "Uma Event Helper",
            menu
        )
        threading.Thread(target=self.icon.run, daemon=True).start()

    def cerrar_aplicacion(self):
        self.icon.stop()
        self.ventana.quit()
        self.evento_terminar.set()
        if hasattr(self, 'icon'):
            self.icon.stop()
        self.ventana.destroy()
        os._exit(0)

    def crear_rectangulo_redondeado(self, text, option_index, width=300, height=60):
        # Colores de outline según el orden de las opciones
        outline_colors = [
            "#8FC74A",  # Primera opción
            "#E7C03F",  # Segunda opción
            "#E28EAF",  # Tercera opción
            "#80C0E4",  # Cuarta opción
            "#9898E0",  # Quinta opción
            "#404040"   # Sexta y siguientes
        ]
        
        # Seleccionar el color basado en el índice
        outline_color = outline_colors[option_index] if option_index < len(outline_colors) else outline_colors[-1]
        
        # Detectar si es una opción con probabilidades
        probability_match = match(r'\((\d+)/(\d+)\)', text)
        
        if probability_match:
            # Para opciones con probabilidad
            return self.crear_rectangulo_probabilidades(text, 380, 100, outline_color)
        else:
            # Para opciones normales
            return self.crear_rectangulo_simple(text.replace('|', '').strip(), width, height, outline_color)

    def crear_rectangulo_probabilidades(self, text, width, height, outline_color):
        probability_match = match(r'\((\d+)/(\d+)\)', text)
        prob1, prob2 = probability_match.groups()
        
        clean_text = sub(r'\((\d+)/(\d+)\)\s*', '', text).replace('|', '').strip()
        parts = [p.strip() for p in clean_text.split("OR") if p.strip()]
        
        if len(parts) != 2:
            return self.crear_rectangulo_simple(clean_text, width, height, outline_color)
        
        # Configuración con fondo completamente transparente
        image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        padding = 8
        
        # 1. Solo el borde exterior (transparente interior)
        draw.rounded_rectangle(
            [(0, 0), (width-1, height-1)],
            radius=15,
            outline=outline_color,  # Usar el color proporcionado
            width=4,
            fill="#F0F0F0"
        )
        try:
            font = ImageFont.truetype("arial.ttf", 11)
            bold_font = ImageFont.truetype("arialbd.ttf", 12)
        except:
            font = ImageFont.load_default()
            bold_font = font
        
        # Áreas de texto
        left_width = (width - padding*3 - 2) // 2
        right_width = left_width
        left_x = padding
        right_x = left_x + left_width + padding + 2
        
        # Divisor central
        divider_top = 25
        draw.line(
            [(left_x + left_width + padding//2, divider_top),
            (left_x + left_width + padding//2, height - padding)],
            fill=outline_color,
            width=2
        )
        
        # Porcentajes (con fondo negro)
        prob_y = 5
        prob_left = left_x + left_width//2 - bold_font.getlength(f"{prob1}%")//2
        prob_right = right_x + right_width//2 - bold_font.getlength(f"{prob2}%")//2
        
        prob_bg_height = 20
        for prob_x, prob in [(prob_left, prob1), (prob_right, prob2)]:
            draw.rounded_rectangle(
                [(prob_x-5, prob_y), (prob_x + bold_font.getlength(f"{prob}%") + 10, prob_y + prob_bg_height)],
                radius=6,
                fill="#333333"
            )
            draw.text((prob_x, prob_y + 3), f"{prob}%", fill="#F0F0F0", font=bold_font)
        
        # Fondos blancos SOLO para áreas de texto
        option_height = height - divider_top - padding
        option_y = divider_top + 5
        
        for x, w in [(left_x, left_width), (right_x, right_width)]:
            draw.rounded_rectangle(
                [(x, option_y), (x + w, option_y + option_height)],
                radius=6,
                fill="#F0F0F0"  # Usamos un blanco ligeramente grisáceo para evitar conflicto con la transparencia
            )
        
        # Dibujar texto
        text_padding = 5
        for i, part in enumerate(parts):
            x = left_x + text_padding if i == 0 else right_x + text_padding
            self.dibujar_texto_opcion(draw, part, x, option_y + text_padding, 
                                    left_width - text_padding*2, font)
        
        return image

    def crear_rectangulo_simple(self, text, width, height, outline_color):
        border_width = 1
        image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        # Fondo principal
        draw.rounded_rectangle(
            [(border_width, border_width), (width-border_width-1, height-border_width-1)],
            radius=12,
            fill="#F0F0F0"
        )
        
        # Borde exterior
        draw.rounded_rectangle(
            [(0, 0), (width-1, height-1)],
            radius=15,
            outline=outline_color,  # Usar el color proporcionado
            width=3,
            fill=None
        )

        try:
            font = ImageFont.truetype("arial.ttf", 12)
        except:
            font = ImageFont.load_default()

        self.dibujar_texto_opcion(draw, text, 15, 15, width - 30, font)
        
        return image

    def dibujar_texto_opcion(self, draw, text, x, y, max_width, font):
        def process_segment(segment, x_pos, y_pos, color="#000000"):
            tokens = findall(r'(\s+|\S+)', segment)
            for token in tokens:
                token_width = font.getlength(token)
                
                if x_pos + token_width > x + max_width:
                    x_pos = x
                    y_pos += font.size + 1
                
                final_color = color
                if color == "#000000":
                    if match(r'^-\d+[\W_]?$', token.strip()):
                        final_color = negative_color
                    elif match(r'^\+\d+[\W_]?$', token.strip()) or match(r'(?<!\S)\d+[\W_]?(?!\S)', token.strip()):
                        final_color = positive_color
                
                draw.text((x_pos, y_pos), token, fill=final_color, font=font)
                x_pos += token_width
            return x_pos, y_pos
        
        clean_text = text.replace('|', '').strip()
        remaining_text = clean_text
        x_pos, y_pos = x, y
        
        while remaining_text:
            found_term = None
            lowest_idx = len(remaining_text)
            
            for term in colored_terms:
                idx = remaining_text.lower().find(term.lower())
                if 0 <= idx < lowest_idx:
                    lowest_idx = idx
                    found_term = term
            
            if found_term:
                before_text = remaining_text[:lowest_idx]
                if before_text:
                    x_pos, y_pos = process_segment(before_text, x_pos, y_pos)
                
                term_text = remaining_text[lowest_idx:lowest_idx+len(found_term)]
                x_pos, y_pos = process_segment(term_text, x_pos, y_pos, colored_terms[found_term])
                
                remaining_text = remaining_text[lowest_idx+len(found_term):]
            else:
                x_pos, y_pos = process_segment(remaining_text, x_pos, y_pos)
                remaining_text = ""

    def crear_rectangulo_redondeado_simple(self, text, width, height):
        border_width = 1
        image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        draw.rounded_rectangle(
            [(border_width, border_width), (width-border_width-1, height-border_width-1)],
            radius=15,
            fill="#F0F0F0",
            outline="#00B4D8",
            width=3
        )

        try:
            font = ImageFont.truetype("arial.ttf", 12)
        except:
            font = ImageFont.load_default()

        self.dibujar_texto_opcion(draw, text, 15, 15, width - 30, font)
        
        return image

    def crear_info_habilidad(self, nombre, descripcion, color_fondo):
        width = 250
        font_title = 10   # Tamaño mínimo legible
        font_desc = 9     # Tamaño mínimo legible
        padding = 10
        margin = 5
        
        try:
            font_title = ImageFont.truetype("arialbd.ttf", 12)
            font_desc = ImageFont.truetype("arial.ttf", 11)
        except:
            font_title = ImageFont.load_default()
            font_desc = font_title
        
        # Calcular altura necesaria
        title_height = font_title.size + 5
        desc_lines = self.wrap_text(descripcion, font_desc, width - 2*padding)
        desc_height = len(desc_lines) * (font_desc.size + 2)
        
        total_height = title_height + desc_height + 2*padding + margin
        
        image = Image.new('RGBA', (width, total_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # Fondo del rectángulo
        draw.rounded_rectangle(
            [(0, 0), (width-1, total_height-1)],
            radius=12,
            fill=color_fondo
        )
        
        # Nombre de la habilidad
        draw.text(
            (padding, padding),
            nombre,
            fill="#F0F0F0",
            font=font_title
        )
        
        # Descripción
        y_pos = padding + title_height
        for line in desc_lines:
            draw.text(
                (padding, y_pos),
                line,
                fill="#F0F0F0",
                font=font_desc
            )
            y_pos += font_desc.size + 2
        
        return image

    def wrap_text(self, text, font, max_width):
        lines = []
        words = text.split()
        
        current_line = []
        current_width = 0
        
        for word in words:
            word_width = font.getlength(word + ' ')
            if current_width + word_width <= max_width:
                current_line.append(word)
                current_width += word_width
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
                current_width = word_width
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    def mostrar_opciones(self, opciones):
        if self.mostrando:
            return

        for widget in self.frame.winfo_children():
            widget.destroy()

        # Mostrar opciones normales
        for index, opcion in enumerate(opciones):
            img = self.crear_rectangulo_redondeado(opcion, index)
            tk_img = ImageTk.PhotoImage(img)

            label = Label(self.frame, image=tk_img, bg='white', bd=0)
            label.image = tk_img
            label.pack(pady=5)

        # Buscar habilidades únicas
        habilidades_encontradas = set()
        opciones_lower = [opcion.lower() for opcion in opciones]
        
        def buscar_habilidades(diccionario, color_default):
            for habilidad in diccionario:
                habilidad_lower = habilidad.lower()
                if any(habilidad_lower in opcion for opcion in opciones_lower):
                    descripcion = diccionario[habilidad]
                    if isinstance(descripcion, list):
                        descripcion = "\n".join(descripcion)  # Unir con saltos de línea
                    elif not isinstance(descripcion, str):
                        descripcion = str(descripcion)
                    
                    habilidad_info = (
                        str(habilidad),
                        descripcion.strip(),
                        colored_terms.get(habilidad, color_default)
                    )
                    habilidades_encontradas.add(habilidad_info)
        
        # Buscar en todos los diccionarios de habilidades
        buscar_habilidades(positive_conditions, "#D48A00")
        buscar_habilidades(negative_conditions, "#0066CC")
        buscar_habilidades(Positive_skills, "#009900")
        buscar_habilidades(Unique_skills, "#800080")  # Color púrpura para habilidades únicas

        # Mostrar habilidades encontradas
        for nombre, descripcion, color in habilidades_encontradas:
            img_habilidad = self.crear_info_habilidad(nombre, descripcion, color)
            tk_img_habilidad = ImageTk.PhotoImage(img_habilidad)
            
            label_habilidad = Label(self.frame, image=tk_img_habilidad, bg='white', bd=0)
            label_habilidad.image = tk_img_habilidad
            label_habilidad.pack(pady=5)

        # Posicionar ventana
        x_pos = 0
        y_pos = 0
        self.ventana.geometry(f"+{x_pos}+{y_pos}")

        self.ventana.deiconify()
        self.mostrando = True
        self.opciones_actuales = opciones
        self.iniciar_listener()

    def cerrar_opciones(self):
        if self.mostrando:
            self.ventana.withdraw()
            self.mostrando = False
            self.detener_listener()

    def revisar_texto(self):
        while not self.evento_terminar.is_set():
            captura = ImageGrab.grab(bbox=REGION)
            texto = pytesseract.image_to_string(captura)

            caracteres_a_ignorar = [".", ",", "(", ")", "#"]
            for char in caracteres_a_ignorar:
                texto = texto.replace(char, "")

            for frase, opciones in EVENTOS.items():
                frase_limpia = frase
                for char in caracteres_a_ignorar:
                    frase_limpia = frase_limpia.replace(char, "")
                if frase.lower() in texto.lower():
                    self.mostrar_opciones(opciones)
                    break

            time.sleep(1)

    def on_click(self, x, y, button, pressed):
        if pressed and self.mostrando:
            self.cerrar_opciones()

    def iniciar_listener(self):
        if self.listener is None or not self.listener.is_alive():
            self.listener = mouse.Listener(on_click=self.on_click)
            self.listener.daemon = True
            self.listener.start()

    def detener_listener(self):
        if self.listener is not None:
            self.listener.stop()
            self.listener = None

if __name__ == "__main__":
    app = SupportOptionsApp()