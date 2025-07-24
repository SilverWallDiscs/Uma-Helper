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



pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

EVENTOS = {
    "New Year's Shrine Visit": [
        "Energy +30",
        "All stats +5",
        "Skill points +35"
    ],
    "Expression of Conviction": [
        "Stamina +20",
        "Speed +20"
    ],
    "Obtain Data!": [
        "Wisdom +20",
        "Power +20"
    ],
    "Tachyon the Spoiled Child": [
        "Stamina +10, Guts +10",
        "Wisdom +20"
    ],
    "At Tachyons Pace": [
        "Guts +10",
        "Speed +5, Power +5"
    ],
    "The Strongest Collaborator?!": [
        "Energy -20, Stamina +15, Guts +10",
        "Energy +5, Wisdom +5"
    ],
    "The Pressure of Justice?": [
        "Wisdom +10, Skill points +15",
        "Skill +1"
    ],
    "Hamburger Helper!": [
        "Energy +10, Skill points +5",
        "Energy +30, Skill points +10"
    ],
    "Medicine That Makes You Faster?": [
        "Power +5, Guts +5",
        "Speed +5, Wisdom +5"
    ],
    "The Significance of Research": [
        "Wisdom +10",
        "Speed +10"
    ],
    "No Shortcuts": [
        "Guts +10",
        "Wisdom +10",
        "Power +10"
    ],
    "A Gift From the Dark Sky": [
        "Speed +5, Power +5",
        "Guts +10"
    ],
    "Body Modification!": [
        "Power +5, Wisdom +5",
        "Stamina +10"
    ],
    "Flowers for You": [
        "Wisdom +20",
        "Speed +20"
    ],
    "A Beautiful Stress Relief Method?": [
        "Stamina +20",
        "Guts +20"
    ],
    "Guidepost": [
        "Speed +20",
        "Power +20"
    ],
    "Empress and Monarch": [
        "Power +10",
        "Wisdom +10"
    ],
    "Operation Flowerbed": [
        "Energy +5, Wisdom +5",
        "Energy -10, Speed +10, Power +10"
    ],
    "Empress and Emperor": [
        "Skill +1",
        "Mood +1, Skill points +15"
    ],
    "Seize Her!": [
        "Energy +10",
        "Energy -10, Mood +1, Speed +10"
    ],
    "Take Good Care of Your Tail": [
        "Energy +10",
        "Energy -10, Mood +1, Power +10"
    ],
    "Suggestion Box of Freedom": [
        "Energy +10",
        "Energy -10, Mood +1, Wisdom +10"
    ],
    "A Taste of Effort": [
        "Energy +10, Skill points +5",
        "Energy +30, Skill points +10"
    ],
    "A Little Encounter": [
        "Wisdom +10",
        "Guts +10"
    ],
    "Sweet Potato Cake": [
        "Power +10",
        "Stamina +10"
    ],
    "Imprinted Memories": [
        "Speed +10",
        "Power +10",
        "Stamina +10"
    ],
    "A Blinking Light Means Stop": [
        "Wisdom +10",
        "Power +10"
    ],
    "Smoldering Silently": [
        "Stamina +10",
        "Speed +10"
    ],
    "To Keep or Not to Keep?": [
        "Wisdom +20",
        "Stamina +10, Power +10"
    ],
    "A Realistic Fairytale": [
        "Power +20",
        "Guts +20"
    ],
    "Theory the Greatest Weapon": [
        "Stamina +20",
        "Wisdom +20"
    ],
    "Memories of Cooking and Sisterhood": [
        "Power +10",
        "Stamina +5, Wisdom +5"
    ],
    "A New Side": [
        "Speed +10",
        "Stamina +10"
    ],
    "Battle With a Raging Dragon": [
        "Power +5, Guts +5",
        "Skill +1"
    ],
    "Banana Fiend": [
        "Energy +10, Skill points +5",
        "Energy +30, Skill points +10"
    ],
    "Reading in a Cafe": [
        "Stamina +10",
        "Speed +10"
    ],
    "Sharp Contrast": [
        "Wisdom +10",
        "Guts +10"
    ],
    "Emergency Presentation": [
        "Wisdom +10",
        "Power +10",
        "Stamina +10"
    ],
    "Hide and Seek Master": [
        "Guts +10",
        "Speed +10"
    ],
    "Game Theory": [
        "Wisdom +10",
        "Power +10"
    ],
    "The Best Pose": [
        "Stamina +10, Power +10",
        "Wisdom +20"
    ],
    "The Weight of Racewear": [
        "Speed +20",
        "Guts +20"
    ],
    "Looking Good": [
        "Stamina +10, Wisdom +10",
        "Speed +10, Guts +10"
    ],
    "Recommended Restaurant": [
        "Speed +5, Power +5",
        "Guts +5, Mood +1"
    ],
    "Advice from an Older Student": [
        "Speed +10",
        "Power +10"
    ],
    "Enjoying Number One": [
        "Stamina +10, Skill points +15",
        "Skill +1"
    ],
    "Can't Lose Sight of Number One!": [
        "Energy +10, Skill points +5",
        "Energy +30, Skill points +10"
    ],
    "As a Model Student": [
        "Wisdom +10",
        "Skill points +30"
    ],
    "Just a Little More": [
        "Skill points +30",
        "Power +10"
    ],
    "Under the Evening Star": [
        "Skill points +30",
        "Speed +5, Stamina +5",
        "Power +10"
    ],
    "Rained On": [
        "Guts +10",
        "Wisdom +10"
    ],
    "How to Spend a Day Off": [
        "Energy +10",
        "Mood +1, Wisdom +5"
    ],
    "Determination of the World's Strongest": [
        "Power +20",
        "Stamina +20"
    ],
    "Cactus Feast": [
        "Speed +10, Stamina +10",
        "Wisdom +20"
    ],
    "Song of Courage": [
        "Power +20",
        "Speed +10, Power +10"
    ],
    "A Personalized Mask": [
        "Speed +10",
        "Power +10"
    ],
    "Salsa Roja": [
        "Stamina +10",
        "Power +10"
    ],
    "Go for the Extra Large Pizza!": [
        "Power +10, Skill points +15",
        "Skill +1"
    ],
    "Hot and Spicy!": [
        "Energy +10, Skill points +5",
        "Energy +30, Skill points +10"
    ],
    "The Wrestler I Admire": [
        "Stamina +10",
        "Speed +10"
    ],
    "Shocking Retirement": [
        "Guts +10",
        "Power +10"
    ],
    "Renewed Resolve": [
        "Guts +10",
        "Stamina +10",
        "Speed +5, Stamina +5"
    ],
    "The Academy at Night": [
        "Mood +1, Guts +5",
        "Energy +10"
    ],
    "Flower Language": [
        "Mood +1, Wisdom +5",
        "Energy +10"
    ],
    "The Red of the Protagonist!": [
        "Wisdom +20",
        "Guts +20"
    ],
    "A Date Golshi Style": [
        "Stamina +20",
        "Power +20"
    ],
    "A Sudden Episode from Golshi's Past!": [
        "Stamina +10, Wisdom +10",
        "Speed +20"
    ],
    "Pair Discount Repeat Offender": [
        "Guts +10",
        "Stamina +10"
    ],
    "Which Did You Lose?": [
        "Energy -10, Power +20",
        "Speed +10"
    ],
    "My Part Time Job Is Crazy!": [
        "Stamina +10, Skill points +15",
        "Skill +1"
    ],
    "The Day After Voices Hoarse": [
        "Stamina +10",
        "Guts +10"
    ],
    "This One's For Keeps!": [
        "Energy +10",
        "Skill points +15, Skill -1"
    ],
    "Summer Camp Year 3 Ends": [
        "Random stats +15"
    ],
    "Killer Appetite!": [
        "Energy +10, Skill points +5",
        "Energy +30, Skill points +10"
    ],
    "Legend of the Left Pinky": [
        "Stamina +10",
        "Speed +10"
    ],
    "Hello From About 15 Billion Years Ago": [
        "Guts +10",
        "Wisdom +10"
    ],
    "And Then She": [
        "Speed +10",
        "Guts +10",
        "Power +10"
    ],
    "A Lovely Place": [
        "Stamina +10",
        "Wisdom +10"
    ],
    "Nighttime Park Visit": [
        "Guts +10",
        "Speed +10"
    ],
    "After the Takarazuka Kinen Keyword 2": [
        "All stats +5, Mood +1, Skill points +45",
        "All stats +3, Mood +1, Skill points +45, Skill +2"
    ],
    "Hidden Meaning": [
        "Stamina +10, Guts +10",
        "Power +20"
    ],
    "Principles": [
        "Speed +20",
        "Stamina +20"
    ],
    "Hate to Lose": [
        "Wisdom +20",
        "Stamina +10, Guts +10"
    ],
    "Errands Have Perks": [
        "Speed +5, Stamina +5",
        "Energy +5, Wisdom +5"
    ],
    "Beauteaful": [
        "Wisdom +5, Skill points +15",
        "Speed +10"
    ],
    "Tracen Karuta Queen": [
        "Speed +10, Wisdom +5",
        "Skill +1"
    ],
    "In Search of Refreshment": [
        "Mood -1, Guts +25",
        "Mood -1, Wisdom +25"
    ],
    "Together for Tea": [
        "Energy +10, Skill points +5",
        "Energy +30, Skill points +10"
    ],
    "Yamato Nadeshiko": [
        "Power +5, Wisdom +5",
        "Speed +10"
    ],
    "Childhood's Apart": [
        "Guts +10",
        "Stamina +10"
    ],
    "Nadeshiko Gal": [
        "Power +10",
        "Wisdom +10",
        "Speed +10"
    ],
    "Childhood Dream": [
        "Speed +5, Guts +5",
        "Stamina +5, Wisdom +5"
    ],
    "Flower Vase": [
        "Guts +5, Wisdom +5",
        "Speed +5, Stamina +5"
    ],
    "The Racewear I Love!": [
        "Speed +20",
        "Power +20"
    ],
    "Pair Interview!": [
        "Power +20",
        "Stamina +20"
    ],
    "Tug of War Tournament!": [
        "Guts +20",
        "Speed +20"
    ],
    "Arm Wrestling Contest": [
        "Wisdom +10",
        "Power +10"
    ],
    "Looking for Something Important": [
        "Energy -10, Guts +20",
        "Stamina +10"
    ],
    "Sand Training!": [
        "Guts +10, Skill points +15",
        "Energy +15"
    ],
    "The Final Boss Spe!": [
        "Energy +10, Skill points +5",
        "Energy +30, Skill points +10"
    ],
    "A Little Detour!": [
        "Skill points +30",
        "Stamina +10"
    ],
    "Parks Are Fun!": [
        "Speed +10",
        "Power +10"
    ],
    "Secret Day Off Plan!": [
        "Speed +10",
        "Power +10",
        "Wisdom +10"
    ],
    "So Cool!": [
        "Skill points +30",
        "Wisdom +10"
    ],
    "Forgot to Eat!": [
        "Guts +10",
        "Stamina +10"
    ],
    "The Outfit That Suits Me Most": [
        "Speed +10, Guts +10",
        "Power +20"
    ],
    "Running Isn't Everything": [
        "Stamina +20",
        "Speed +10, Power +10"
    ],
    "Manners Are Common Sense": [
        "Guts +20",
        "Stamina +10, Wisdom +10"
    ],
    "Movies Are Full of Learning Opportunities": [
        "Speed +5, Guts +5",
        "Stamina +10"
    ],
    "The King Knows No Exhaustion": [
        "Energy +5",
        "Power +10"
    ],
    "First Rate in Studies Too": [
        "Wisdom +10, Skill points +15",
        "Skill +1"
    ],
    "After School Soda": [
        "Guts +10",
        "Speed +10"
    ],
    "Three Heads Are Better than One": [
        "Wisdom +10",
        "Stamina +10"
    ],
    "Sweet Tooth Temptation": [
        "Energy +10, Skill points +5",
        "Energy +30, Skill points +10"
    ],
    "First Rate Spot": [
        "Guts +10",
        "Speed +10"
    ],
    "First Rate Harvest": [
        "Power +5, Guts +5",
        "Speed +5, Stamina +5"
    ],
    "First Rate Terms": [
        "Power +10",
        "Wisdom +10",
        "Guts +10"
    ],
    "Crowds Are No Problem": [
        "Speed +10",
        "Power +10"
    ],
    "Breaking Curfew is Second Rate": [
        "Guts +5, Wisdom +5",
        "Speed +5, Power +5"
    ],
    "Trendsetter": [
        "Speed +10, Wisdom +10",
        "Power +20"
    ],
    "Sewing Star": [
        "Guts +20",
        "Stamina +10, Power +10"
    ],
    "My Favorite Things": [
        "Speed +20",
        "Stamina +10, Guts +10"
    ],
    "Hot Rod": [
        "Speed +10",
        "Wisdom +10"
    ],
    "Let's Play": [
        "Energy +10",
        "Energy -5, Power +10, Guts +5"
    ],
    "A Lady's Style": [
        "Speed +5, Skill points +10, Mood +1",
        "Skill +1"
    ],
    "Let's Cook!": [
        "Speed +10",
        "Guts +10"
    ],
    "The Road to a Rad Victory!": [
        "Stamina +10",
        "Wisdom +10"
    ],
    "Down to Dance!": [
        "Speed +10",
        "Power +10"
    ],
    "Nostalgia Fever": [
        "Energy +10, Skill points +5",
        "Energy +30, Skill points +10"
    ],
    "The Secret to Supporting Each Other": [
        "Speed +10",
        "Power +10"
    ],
    "Even Role Models Get Lonely": [
        "Stamina +5, Guts +5",
        "Speed +5, Power +5"
    ],
    "Take the Wheel": [
        "Wisdom +10",
        "Guts +10",
        "Power +10"
    ],
    "Meeting New People Is Trendy": [
        "Guts +10",
        "Wisdom +10"
    ],
    "The Fun Never Stops": [
        "Speed +5, Wisdom +5",
        "Stamina +5, Power +5"
    ],
    "Room of the Chosen Ones": [
        "Guts +20",
        "Speed +20"
    ],
    "Better Fortune! Lucky Telephone": [
        "Stamina +10, Wisdom +10",
        "Power +20"
    ],
    "Under the Meteor Shower": [
        "Speed +10, Power +10",
        "Stamina +10, Guts +10"
    ],
    "Cursed Camera": [
        "Wisdom +10",
        "Skill points +30"
    ],
    "Manhattan's Dream": [
        "Skill +1",
        "Stamina +10"
    ],
    "Pretty Gunslingers": [
        "Skill points +15, Mood +1",
        "Power +15"
    ],
    "Which One is the Lucky Card?!": [
        "Random stats +5"
    ],
    "Seven Gods of Fortune Fine Food Tour": [
        "Energy +10, Skill points +5",
        "Energy +30, Skill points +10"
    ],
    "Fukukitaru's Protection against Misfortune": [
        "Guts +10",
        "Power +10"
    ],
    "Punch in a Pinch": [
        "Speed +10",
        "Stamina +5, Wisdom +5"
    ],
    "Fukukitaru's Unique Good Luck Spell": [
        "Speed +5, Guts +5",
        "Stamina +5, Power +5",
        "Wisdom +10"
    ],
    "Taking the Plunge": [
        "Stamina +10",
        "Speed +5, Wisdom +5"
    ],
    "Shrine Visit": [
        "Power +5, Guts +5",
        "Speed +5, Stamina +5"
    ],
    "Maya's Thrilling Test of Courage": [
        "Power +20",
        "Guts +20"
    ],
    "Sweet Feelings for You": [
        "Stamina +20",
        "Wisdom +20"
    ],
    "Mayano Takes Off": [
        "Speed +20",
        "Stamina +20"
    ],
    "Maya Will Teach You": [
        "Power +5, Guts +5",
        "Wisdom +10"
    ],
    "Tips from a Top Model!": [
        "Energy -10, Stamina +20",
        "Speed +10"
    ],
    "Maya's Race Class": [
        "Stamina +10, Skill points +15",
        "Skill +1"
    ],
    "Hearty Chanko": [
        "Energy +10, Skill points +5",
        "Energy +30, Skill points +10"
    ],
    "Maya's Exciting Livestream!": [
        "Stamina +5, Power +5",
        "Guts +10"
    ],
    "Maya's Euphoric Livestream!": [
        "Speed +10",
        "Stamina +10"
    ],
    "Maya's Twinkly Determination!": [
        "Speed +5, Stamina +5",
        "Power +10",
        "Wisdom +10"
    ],
    "Maya's Special Someone!": [
        "Speed +10",
        "Guts +10"
    ],
    "Wish on a Star": [
        "Wisdom +10",
        "Speed +10"
    ],
    "Resolve and Duty": [
        "Speed +10, Wisdom +10",
        "Power +20"
    ],
    "Late Night Fanservice Training": [
        "Guts +20",
        "Speed +20"
    ],
    "Elegance": [
        "Stamina +10, Power +10",
        "Wisdom +20"
    ],
    "Queen of the Island": [
        "Speed +10",
        "Stamina +10"
    ],
    "It's Called a Sea Pineapple!": [
        "Skill points +30",
        "Stamina +10"
    ],
    "Cooking Up Memories": [
        "Energy +15",
        "Skill +1"
    ],
    "The Allure of Racecourse Food": [
        "Energy +30, Skill points +10",
        "Guts +15, Skill points +5"
    ],
    "Attack of the Chestnut Feast!": [
        "Energy +10, Skill points +5",
        "Energy +30, Skill points +10"
    ],
    "Two Tickets for the Silver Screen": [
        "Stamina +10",
        "Wisdom +5, Skill points +15"
    ],
    "An Excited Young Lady": [
        "Guts +10",
        "Power +10"
    ],
    "Endless Kingdom": [
        "Stamina +10",
        "Wisdom +10",
        "Speed +5, Power +5"
    ],
    "Bargain Find": [
        "Speed +10",
        "Guts +10"
    ],
    "Three Ramen Bowls Worth of Temptation": [
        "Skill points +30",
        "Speed +5, Stamina +5"
    ],
    "My Signature Racewear": [
        "Guts +20",
        "Speed +20"
    ],
    "Heart Pounding Aquarium": [
        "Power +10, Wisdom +10",
        "Stamina +10, Wisdom +10"
    ],
    "Refreshingly Real": [
        "Stamina +20",
        "Power +20"
    ],
    "Muscle Jealousy": [
        "Guts +10",
        "Wisdom +10"
    ],
    "The Pony Girl and the Wolf Prince": [
        "Energy +5, Stamina +5",
        "Energy +5, Speed +5"
    ],
    "Real Gains": [
        "Power +10, Skill points +15",
        "Skill +1"
    ],
    "Rest Day": [
        "Energy +10, Skill points +5",
        "Energy +30, Skill points +10"
    ],
    "Nerve Racking Rest Time": [
        "Stamina +10",
        "Power +10"
    ],
    "Flush with Feelings": [
        "Wisdom +10",
        "Speed +10"
    ],
    "With Relaxation and Trust Comes": [
        "Speed +10",
        "Stamina +10",
        "Power +10"
    ],
    "Ryan to the Rescue!": [
        "Power +10",
        "Guts +10"
    ],
    "The Little Fans of the Umadol": [
        "Power +10",
        "Wisdom +10"
    ],
    "Trail of Light": [
        "Speed +20",
        "Power +20"
    ],
    "Smiles Are Contagious": [
        "Stamina +20",
        "Guts +20"
    ],
    "Who to Count On": [
        "Wisdom +20",
        "Power +20"
    ],
    "Operation Execute Orders": [
        "Stamina +10",
        "Power +10"
    ],
    "Operation Extra Classes": [
        "Energy +10, Mood +1",
        "Wisdom +10"
    ],
    "Operation Excursion Trouble": [
        "Stamina +10, Skill points +15",
        "Skill +1"
    ],
    "Brutal Training": [
        "Energy -10, Power +5, Skill points +5",
        "Energy +5"
    ],
    "The Perfect Dessert": [
        "Energy +10, Skill points +5",
        "Energy +30, Skill points +10"
    ],
    "Let's Make Memories": [
        "Speed +10",
        "Guts +10"
    ],
    "Bourbon's Challenge?": [
        "Power +10",
        "Wisdom +10"
    ],
    "You're Irreplaceable to Me": [
        "Stamina +10",
        "Speed +10",
        "Power +10"
    ],
    "Operation Dance Fever": [
        "Stamina +5, Guts +5",
        "Stamina +5, Wisdom +5"
    ],
    "Operation Festival Fun": [
        "Power +10",
        "Stamina +5, Guts +5"
    ],
    "Nature and Her Tired Trainer": [
        "Power +20",
        "Stamina +20"
    ],
    "Bittersweet Sparkle": [
        "Power +20",
        "Speed +20"
    ],
    "Festive Colors": [
        "Guts +20",
        "Stamina +20"
    ],
    "Rainy Day Fun": [
        "Wisdom +10",
        "Energy -10, Stamina +10, Guts +10"
    ],
    "Not My Style": [
        "Energy +5, Mood +1",
        "Speed +5, Power +5"
    ],
    "Whirlwind Advice": [
        "Skill +1",
        "Speed +5, Stamina +5, Power +5"
    ],
    "A Little Can't Hurt": [
        "Energy +10, Skill points +5",
        "Energy +30, Skill points +10"
    ],
    "A Phone Call from Mom": [
        "Stamina +10",
        "Speed +10"
    ],
    "Once in a While": [
        "Stamina +5, Guts +5",
        "Stamina +5, Power +5"
    ],
    "Bittersweet Twilight": [
        "Speed +10",
        "Guts +10",
        "Wisdom +10"
    ],
    "Snapshot of Emotions": [
        "Speed +10",
        "Power +10"
    ],
    "Let's Watch the Fish": [
        "Guts +10",
        "Speed +10"
    ],
    "Pinned Hopes": [
        "Stamina +10, Power +10",
        "Wisdom +20"
    ],
    "Oguri the Forest Guide?": [
        "Speed +20",
        "Power +20"
    ],
    "Better Than a Plushie": [
        "Guts +20",
        "Stamina +20"
    ],
    "Lost Umamusume": [
        "Guts +10",
        "Speed +10"
    ],
    "Field Workout": [
        "Guts +10",
        "Power +10"
    ],
    "Running on Full": [
        "Energy +10, Skill points +15",
        "Skill +1"
    ],
    "Oguri's Gluttony Championship": [
        "Energy +30, Power +10, Skill points +10",
        "Energy +10, Power +5, Skill points +5"
    ],
    "Bottomless Pit": [
        "Energy +10, Skill points +5",
        "Energy +30, Skill points +10"
    ],
    "Oguri Makes a Resolution": [
        "Speed +5, Wisdom +5",
        "Stamina +5, Guts +5"
    ],
    "Oguri Perseveres": [
        "Guts +10",
        "Power +10"
    ],
    "Oguri Matures": [
        "Wisdom +10",
        "Stamina +10",
        "Power +10"
    ],
    "Something Smells Good": [
        "Speed +10",
        "Guts +10"
    ],
    "High Level Rival": [
        "Speed +5, Stamina +5",
        "Power +5, Wisdom +5"
    ],
    "Am I Enough?": [
        "Guts +20",
        "Power +20"
    ],
    "Sweet Lively Joy": [
        "Speed +10, Stamina +10",
        "Wisdom +20"
    ],
    "I Am Enough": [
        "Guts +10, Wisdom +10",
        "Stamina +10, Power +10"
    ],
"Training Inspiration": [
        "Energy -10, Guts +20",
        "Energy +5, Skill points +15"
    ],
    "Wonderful New Worlds": [
        "Stamina +10",
        "Speed +5, Wisdom +5"
    ],
    "Looking on the Bright Side": [
        "Stamina +5, Guts +10",
        "Skill +1"
    ],
    "A Page about Apples": [
        "Energy +10, Skill points +5",
        "Energy +30, Skill points +10"
    ],
    "Even When the Ladybugs Are Gone": [
        "Stamina +10",
        "Wisdom +10"
    ],
    "Even When Clouds Cover the Sky": [
        "Speed +5, Power +5",
        "Guts +10"
    ],
    "My Sun": [
        "Guts +5, Wisdom +5",
        "Speed +5, Power +5",
        "Stamina +10"
    ],
    "I've Got This": [
        "Guts +10",
        "Speed +10"
    ],
    "A Page about Sunsets": [
        "Power +5, Guts +5",
        "Stamina +5, Wisdom +5"
    ],
    "Bakushin for Love!": [
        "Stamina +10, Wisdom +10",
        "Guts +20"
    ],
    "A Day Without a Class Rep": [
        "Speed +20",
        "Power +20"
    ],
    "Bakushin in Signature Racewear!": [
        "Power +10, Guts +10",
        "Wisdom +20"
    ],
    "The Bakushin Book!": [
        "Wisdom +10",
        "Stamina +10"
    ],
    "The Voices of the Students": [
        "Energy -10, Stamina +10, Power +10",
        "Speed +10"
    ],
    "Solving Riddles Bakushin Style!": [
        "Guts +10, Skill points +15",
        "Skill +1"
    ],
    "Bakushin?! Class?!": [
        "Energy +10, Skill points +5",
        "Energy +30, Skill points +10"
    ],
    "Bakushining with a Classmate!": [
        "Power +5, Guts +5",
        "Speed +5, Wisdom +5"
    ],
    "The Best Bakushin!": [
        "Wisdom +10",
        "Stamina +5, Guts +5"
    ],
    "Bakushin Now and Forever!": [
        "Speed +10",
        "Guts +5, Wisdom +5",
        "Power +5"
    ],
    "Together with Someone Important!": [
        "Guts +10",
        "Speed +5, Stamina +5"
    ],
    "The Speed King": [
        "Power +5, Wisdom +5",
        "Stamina +10"
    ],
    "The Color of the Landscape": [
        "Guts +20",
        "Power +20"
    ],
    "Hobbies and Talents": [
        "Stamina +20",
        "Speed +10, Wisdom +10"
    ],
    "Umadol Special Class!": [
        "Speed +10, Power +10",
        "Guts +10, Wisdom +10"
    ],
    "Teaching Suzuka's Style": [
        "Speed +10",
        "Wisdom +10"
    ],
    "Party Time": [
        "Energy +10",
        "Stamina +5, Power +5"
    ],
    "On My Heels": [
        "Speed +5, Skill points +15",
        "Skill +1"
    ],
    "White Temptation": [
        "Energy +10, Skill points +5",
        "Energy +30, Skill points +10"
    ],
    "My Little Snowscape": [
        "Stamina +10",
        "Wisdom +10"
    ],
    "To Make You Happy": [
        "Power +10",
        "Speed +5, Guts +5"
    ],
    "Our Little Snowscape": [
        "Stamina +10",
        "Speed +10",
        "Power +10"
    ],
    "How to Spend a Rainy Day": [
        "Guts +10",
        "Speed +5, Wisdom +5"
    ],
    "Are They Compatible?": [
        "Power +5, Guts +5",
        "Stamina +10"
    ],
    "How Should I Pose?": [
        "Power +20",
        "Skill points +40"
    ],
    "Wear Your Heart on Your Sleeve": [
        "Stamina +20",
        "Guts +20"
    ],
    "Today and Tomorrow Too": [
        "Speed +20",
        "Wisdom +20"
    ],
    "A Beautiful Day for Tennis": [
        "Speed +10",
        "Stamina +10"
    ],
    "Karaoke Connoisseur": [
        "Energy +10",
        "Power +10"
    ],
    "Early Afternoon Payback": [
        "Energy +5, Wisdom +5",
        "Skill +1"
    ],
    "Putting It Away at the Cafeteria": [
        "Energy +10, Skill points +5",
        "Energy +30, Skill points +10"
    ],
    "Because It's Special": [
        "Stamina +10",
        "Speed +10"
    ],
    "A Place I Want to Take You": [
        "Wisdom +10",
        "Stamina +10"
    ],
    "Someone I Respect": [
        "Skill points +30",
        "Stamina +5, Guts +5",
        "Speed +5, Power +5"
    ],
    "Research Fanatic": [
        "Skill +1",
        "Skill +1"
    ],
    "A Self-Satisfying Wish": [
        "Power +20",
        "Stamina +20"
    ],
    "Fill Life with Love": [
        "Speed +10, Stamina +10",
        "Wisdom +10"
    ],
    "Patience Is Key": [
        "Guts +20",
        "Stamina +10, Power +10"
    ],
    "One Day Experience Ceramics Class": [
        "Speed +5, Wisdom +5",
        "Stamina +10"
    ],
    "Find the Lost Child!": [
        "Energy -10, Stamina +10, Power +10",
        "Wisdom +10"
    ],
    "A Dangerous Treat": [
        "Guts +10, Skill points +15",
        "Skill +1"
    ],
    "Sweet Nighttime Temptation": [
        "Energy +30, Speed +10, Skill points +10",
        "Energy +10, Speed +5, Skill points +5"
    ],
    "For My Friends": [
        "Energy +10, Skill points +5",
        "Energy +30, Skill points +10"
    ],
    "Is Relaxing Being Spoiled?": [
        "Stamina +10",
        "Wisdom +10"
    ],
    "Dispel Your Anxieties": [
        "Power +10",
        "Speed +5, Guts +5"
    ],
    "Let's Share": [
        "Stamina +10",
        "Speed +10",
        "Power +10"
    ],
    "Rough Massage!": [
        "Guts +10",
        "Speed +5, Wisdom +5"
    ],
    "Stargazing is Better Together": [
        "Power +5, Guts +5",
        "Stamina +10"
    ],
    "Midway Reflection": [
        "Speed +20",
        "Power +20"
    ],
    "The Smiling Emperor's New Clothes": [
        "Wisdom +20",
        "Guts +20"
    ],
    "The Distant View from the End of the Road": [
        "Stamina +20",
        "Guts +20"
    ],
    "Those Who March Forth": [
        "Speed +5, Power +5",
        "Stamina +5, Guts +5"
    ],
    "The Emperor's Social Studies": [
        "Energy -10, Stamina +10, Power +10",
        "Wisdom +5, Skill points +15"
    ],
    "The Emperor's Spare Time": [
        "Wisdom +10, Skill points +15",
        "Skill +1"
    ],
    "At Any Time": [
        "Energy -10, Guts +20",
        "Energy +10"
    ],
    "Sudden Kindness": [
        "Energy -10, Stamina +20",
        "Energy +10"
    ],
    "As Good As My Word": [
        "Energy -10, Power +20",
        "Energy +10"
    ],
    "The Emperor's Satiation": [
        "Energy +10, Skill points +5",
        "Energy +30, Skill points +10"
    ],
    "Birds of a Feather": [
        "Speed +10",
        "Stamina +10"
    ],
    "Well-Earned Respect": [
        "Wisdom +10",
        "Power +10"
    ],
    "A Clear and Beautiful Night": [
        "Speed +10",
        "Wisdom +10",
        "Stamina +10"
    ],
    "The Emperor's Daily Routine": [
        "Power +10",
        "Guts +10"
    ],
    "The Emperor's Path": [
        "Wisdom +10",
        "Power +10"
    ],
    "Quick Draw Showdown": [
        "Energy +10, Speed +10",
        "Energy +10, Wisdom +10"
    ],
    "Must Win Match": [
        "Wisdom +20",
        "Stamina +20"
    ],
    "To the Top!": [
        "Power +10, Guts +10",
        "Speed +10, Wisdom +10"
    ],
    "Hide and Seek": [
        "Speed +10",
        "Stamina +10"
    ],
    "Embracing Guidance": [
        "Power +10",
        "Energy +10"
    ],
    "Harvest Festival": [
        "Power +10, Skill points +15",
        "Skill +1"
    ],
    "Serial Riddler": [
        "Mood -1",
        "Wisdom +10"
    ],
    "Taste of Home": [
        "Mood -1",
        "Wisdom +10"
    ],
    "Meaty Heaven": [
        "Energy +10, Skill points +5",
        "Energy +30, Skill points +10"
    ],
    "Rainy Power": [
        "Power +10",
        "Skill points +30"
    ],
    "Rainy Choice": [
        "Speed +5, Guts +5",
        "Stamina +5, Wisdom +5"
    ],
    "Rainy Rescue": [
        "Skill points +30",
        "Power +5, Wisdom +5",
        "Speed +5, Guts +5"
    ],
    "Let's Patrol!": [
        "Power +10",
        "Energy +10"
    ],
    "Going Home Together": [
        "Mood +1, Speed +5",
        "Mood +1, Stamina +5"
    ],
    "Fit for a King": [
        "Wisdom +20",
        "Power +20"
    ],
    "For My Admirer": [
        "Stamina +10, Guts +10",
        "Speed +20"
    ],
    "Strength of Will": [
        "Wisdom +20",
        "Speed +10, Power +10"
    ],
    "Fantastic Voyeur": [
        "Power +10",
        "Wisdom +10"
    ],
    "Blinding Beauty": [
        "Energy -10, Power +20",
        "Speed +10"
    ],
    "Bring Me Your Finest": [
        "Speed +10, Skill points +15",
        "Skill +1"
    ],
    "Battle of Kings - The Great Ramen War": [
        "Energy +10, Skill points +5",
        "Energy +30, Skill points +10"
    ],
    "The Princess in Pajamas": [
        "Speed +10",
        "Stamina +10"
    ],
    "What the Mirror Reflects": [
        "Wisdom +10",
        "Guts +10"
    ],
    "My Radiance is Yours": [
        "Power +10",
        "Guts +10",
        "Wisdom +10"
    ],
    "Maintaining Magnificence": [
        "Speed +10",
        "Wisdom +10"
    ],
    "Evening Opera Theater": [
        "Power +10",
        "Energy +10"
    ],
    "Good Luck Charm": [
        "Stamina +20",
        "Wisdom +20"
    ],
    "Selfish Teio and a Nostalgic View": [
        "Guts +20",
        "Speed +10, Power +10"
    ],
    "Racewear Like Prez": [
        "Speed +10, Wisdom +10",
        "Stamina +10, Guts +10"
    ],
    "Empress vs Monarch": [
        "Guts +10",
        "Skill points +30"
    ],
    "Cupcakes for All": [
        "Energy +5, Mood +1",
        "Speed +5, Power +5"
    ],
    "Teio's Warrior Training": [
        "Guts +10, Skill points +15",
        "Skill +1"
    ],
    "Karaoke Power?": [
        "Guts +10",
        "Speed +10"
    ],
    "Teio an Umadol?!": [
        "Power +10",
        "Speed +10"
    ],
    "Secret to Strength": [
        "Energy +10, Skill points +5",
        "Energy +30, Skill points +10"
    ],
    "I Got Praised!": [
        "Stamina +10",
        "Speed +10"
    ],
    "I Got Scolded!": [
        "Wisdom +10",
        "Power +5, Guts +5"
    ],
    "I Figured It Out!": [
        "Speed +5, Stamina +5",
        "Guts +5, Wisdom +5",
        "Power +10"
    ],
    "Grown Up Time": [
        "Guts +10",
        "Wisdom +10"
    ],
    "Punny Prez": [
        "Stamina +5, Power +5",
        "Speed +10"
    ],
    "Vintage Style": [
        "Power +20",
        "Stamina +20"
    ],
    "Making so of a Friend": [
        "Speed +20",
        "Guts +20"
    ],
    "Hot and Cool": [
        "Speed +20",
        "Speed +10, Power +10"
    ],
    "Like a Kid": [
        "Speed +10",
        "Power +10"
    ],
    "Challenging Fate": [
        "Stamina +10",
        "Speed +10"
    ],
    "Showdown by the River!": [
        "Wisdom +10, Skill points +15",
        "Skill +1"
    ],
    "Awkward Honesty": [
        "Energy +10, Skill points +5",
        "Energy +30, Skill points +10"
    ],
    "The Standards of Coolness": [
        "Wisdom +10",
        "Guts +10"
    ],
    "Ring Out Passionate Sound!": [
        "Speed +10",
        "Stamina +10"
    ],
    "The Way of Cool": [
        "Power +10",
        "Speed +10",
        "Stamina +5, Guts +5"
    ],
    "Let's Take a Little Detour": [
        "Speed +10",
        "Energy +5, Mood +1"
    ],
    "Sugar and Spice": [
        "Energy +5",
        "Power +10"
    ],
    "Full Power Testing!": [
        "Guts +20",
        "Speed +20"
    ],
    "Full Power Fashion!": [
        "Stamina +20",
        "Power +10, Guts +10"
    ],
    "Full Power Effort!": [
        "Speed +10, Wisdom +10",
        "Power +20"
    ],
    "Rain or Shine": [
        "Energy -10, Stamina +10, Skill points +15",
        "Power +10"
    ],
    "Overcome the Towering Obstacle!": [
        "Mood +1, Guts +5",
        "Mood +1, Power +5"
    ],
    "A Fresh Perspective": [
        "Speed +10, Skill points +15",
        "Skill +1"
    ],
    "Full Power Eating!": [
        "Energy +10, Skill points +5",
        "Energy +30, Skill points +10"
    ],
    "Play of the Three Kingdoms": [
        "Stamina +5, Skill points +15",
        "Power +5, Skill points +15"
    ],
    "Futsal Now?!": [
        "Guts +10",
        "Speed +10"
    ],
    "The Last Ticket": [
        "Guts +10",
        "Speed +10",
        "Power +10"
    ],
    "Shake Off Your Blues!": [
        "Mood +1, Power +5",
        "Speed +5, Skill points +15"
    ],
    "Big Girls Cry Too": [
        "Guts +5, Skill points +15",
        "Mood +1, Power +5"
    ],
    "Exhilarating! What a Scoop!": [
        "Stamina +10",
        "Guts +10"
    ],
    "A Trainer's Knowledge": [
        "Power +10",
        "Speed +10"
    ],
    "Best Foot Forward!": [
        "Energy -10, Power +20, Guts +20, Skill +1",
        "Energy +30, Stamina +20, Skill +1"
    ],
    "Get Well Soon!": [
        "Mood -1, Last trained stat -5, Chance to get Practice Poor -1",
        "|Mood -1, Last trained stat -10, Chance to get Practice Poor -1| OR |Practice Perfect +1|"
    ],
    "Don't Overdo It!": [
        "Energy +10, Mood -2, Last trained stat -10, 2 random stats -10, Chance to get Practice Poor -1",
        "|Mood -3, Last trained stat -10, 2 random stats -10, Practice Poor| OR |Energy +10, Practice Perfect +1|"
    ],
    "Extra Training": [
        "Energy -5, Last trained stat +5,  |(random) Heal a negative status effect|",
        "Energy +5"
    ],
    "At Summer Camp Year 2": [
        "Power +10",
        "Guts +10"
    ],
    "Dance Lesson": [
        "Power +10",
        "Speed +10"
    ],
    "New Year's Resolutions": [
        "(Depends on the horse)",
        "Energy +20",
        "Skill points +20"
    ],
    "Acupuncture - Just an Acupuncturist No Worries!": [
        "(50/50) |All stats +20| OR |Mood -2, All stats -15, Night Owl|",
        "(60/40) |Corner Recovery OBTAIN, Straightaway Recovery OBTAIN| OR |Energy -20, Mood -2|",
        "(80/20) |Maximum Energy +12, Energy +40, Heal all negative status effects| OR |Energy -20, Mood -2, Skill -1|",
        "(90/10) |Energy +20, Mood +1, Charming +1| OR |Energy -10/-20, Mood -1, (random) Practice Poor -1|",
        "Energy +10"
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
        "Energy -15, Stamina +10, Guts +10",
        "Energy -15, Guts +10, Wisdom +10"
    ],
    "Runaway Romance": [
        "Energy +10, Guts +5, Wisdom +5",
        "Energy +10, Front Runner Savvy +1"
    ],
    "Optimistic Escapism: Never Give Up!": [
        "Energy -20, Stamina +5, Guts +5, |Vanguard Spirit +3| or |Keeping the Lead +1/+3|",
        "Energy +10, Lone Wolf +1"
    ],
    "An Inescapable Choice?": [
        "Energy -15, Guts +20",
        "Power +5, Skill points +15"
    ],
    "Optimistic Escapism": [
        "Guts +15",
        "Wet Conditions +1"
    ],
    "Ikuno-Style Support": [
        "Wisdom +15, Frenzied Front Runners +3",
        "Wisdom +15, Frenzied Front Runners +3"
    ],
    "Ikuno-Style Flawless Method": [
        "Wisdom +10",
        "Skill points +30"
    ],
    "Ikuno-Style Management": [
        "Stamina +20",
        "Trick (Rear) +1"
    ],
    "I'm Not Afraid!": [
        "|Speed +10| OR |Energy -10, Speed +10|",
        "Energy +20"
    ],
    "Can't Catch Me!": [
        "|Speed +15, Leader's Pride +3| OR |Energy -10, Speed +10|",
        "Energy +25"
    ],
    "Turbo Is Strong!": [
        "|Energy -10, Speed +25, Taking the Lead +3| OR |Energy -10, Speed +5, Early Lead +1|",
        "Energy +15, Skill +1"
    ],
    "Just Start Running!": [
        "Mood -1, Speed +20",
        "Energy -10, Power +20"
    ],
    "I'm All Fired Up!": [
        "Energy +15",
        "Skill +1"
    ],
    "BFF Party!": [
        "Power +10",
        "Speed +10"
    ],
    "LOL Party! Round2": [
        "Power +10, Straight Descent +1/+3",
        "Energy +20, Watchful Eye +1"
    ],
    "Encounter With the Sun": [
        "Power +10",
        "Hot Topic +1"
    ],
    "Smiles Forever": [
        "Speed +5, Power +10",
        "Long Shot +1"
    ],
    "Some Very Green Friends": [
        "Speed +5, Skill points +10, Lucky Seven +1",
        "Mood -1, Maverick +1"
    ],
    "Premeditated Mischief": [
        "Speed +10, Skill points +20, Levelheaded +1",
        "Mood -1, Lone Wolf +1"
    ],
    "Miracle Escape!": [
        "Energy +10, Speed +5",
        "Energy -10, Speed +20"
    ],
    "Wonderful Mistake!": [
        "|Energy -15, Skill points +40| OR |Energy -20, Skill points +40|",
        "Charming +1"
    ],
    "Just a Little Closer": [
        "Energy -10, Speed +15",
        "Energy -10, Skill points +20",
        "Energy -10, Shake It Out +1"
    ],
    "A Roller Coaster of Feelings!": [
        "Energy -10, Speed +5, Stamina +5, Guts +10",
        "Energy +20, Wisdom +10"
    ],
    "Watch Where You're Going!": [
        "Extra Tank +1",
        "Guts +15"
    ],
    "So Many Options!": [
        "Energy +10, Mood +1",
        "Energy -10, Stamina +15, Skill points +15"
    ],
    "On and On": [
        "Speed +10, Stamina +5",
        "Speed +15"
    ],
    "What Should I Do?": [
        "Speed +5, Stamina +5, Wisdom +5",
        "Left-Handed +1"
    ],
    "My Way Or": [
        "Mood +1, Skill points +15",
        "Guts +15"
    ],
    "My Weapon": [
        "Mood +1, Guts +10",
        "Pace Chaser Straightaways +1"
    ],
    "For an Adorable Younger Student": [
        "Early Lead +1",
        "Energy +5, Speed +10"
    ],
    "Drive Destination": [
        "Mood +1, Speed +5",
        "Mood +1, Wisdom +5"
    ],
    "What I Want to Say": [
        "|Power +10, Guts +5, Skill points +10, Furious Feat +1| OR |Power +15, Guts +10, Skill points +15, Furious Feat +3|",
        "Energy +30"
    ],
    "How Should I Respond?": [
        "if the event is a chain event (>>) use the top options as reference",
        ">> Power +5, Skill points +10, Stamina to Spare +1",
        ">> Stamina +5, Skill points +10, Outer Swell +1",
        "Energy +5, Power +5",
        "Energy -10, Guts +15"
    ],
    "Conquering the Crowds": [
        "Power +5, Skill points +15",
        "Nakayama Racecourse +1"
    ],
    "Adventurer Gold Ship": [
        "Stamina +15",
        "Guts +10, Skill points +15"
    ],
    "Revive the Brand! Golshi's Yakisoba": [
        "Mood +1, Stamina +5",
        "Hanshin Racecourse +1"
    ],
    "The Coolest Line": [
        "Power +10",
        "Power +5, Skill points +15"
    ],
    "Enemies on Main Street": [
        "Nimble Navigator +1",
        "Power +5, Skill points +15"
    ],
    "Yes! Let's Hug": [
        "Speed +10",
        "Speed +5, Power +5"
    ],
    "Yeehaw! Party Tonight": [
        "Energy -10, Speed +5, Power +10",
        "Prepared to Pass +1"
    ],
    "A Moment's Respite": [
        "Energy +15",
        "|Energy -10, Power +5, Guts +5, Wisdom +5| OR |Power +5, Guts +5, Wisdom +10|"
    ],
    "Library Vexation": [
        "Wisdom +10",
        "Guts +5, Wisdom +5"
    ],
    "A Friendly Daytime Discussion": [
        "Frenzied Pace Chasers +1",
        "Target in Sight +1"
    ],
    "To Maintain My Weight": [
        "Energy -10, Stamina +15",
        "Maximum Energy +4, Stamina +5"
    ],
    "To Reach the Greatest Heights": [
        "Stamina +5, Guts +5",
        "Early Lead +1"
    ],
    "Umame": [
        "Energy +30",
        "Stamina to Spare +1"
    ],
    "Blazing Fire!": [
        "Stamina +10",
        "Energy -10, Power +20"
    ],
    "Secret Notebook!": [
        "Power +10",
        "Sunny Days +1"
    ],
    "Uma-me": [
        "Energy +30",
        "Stamina to Spare +1"
    ],
    "Etude to Victory": [
        "Mood -1, Speed +5, Skill points +30",
        "Power +5, Skill points +15"
    ],
    "Beyond Our Limited Time": [
        "Energy +10, Skill points +15",
        "Non-Standard Distance +1"
    ],
    "The Emperor's Encouragement": [
        "Speed +10",
        "Energy -10, Skill points +30"
    ],
    "The Student Council President's Thoughtfulness": [
        "Rainy Days +1",
        "Stamina +15"
    ],
    "Be Strategic": [
        "Energy +10, Wisdom +5",
        "Skill points +30, Second Wind +1, bond -5"
    ],
    "Recruiting Cat Catchers": [
        "Energy +10, Wisdom +5",
        "Energy -10, Speed +15, Stamina +5"
    ],
    "Recruiting Advisors": [
        "Wisdom +15",
        "Keeping the Lead +1"
    ],
    "A Page of Flower Shop Assistance": [
        "Mood +2",
        "Stamina +10"
    ],
    "A Page About Cloudy Weather": [
        "Speed +5, Guts +5",
        "Firm Conditions +1"
    ],
    "Full Power Muscles!": [
        "Stamina +5, Skill points +15",
        "Mood +1, Skill points +15"
    ],
    "Full Power Racing!": [
        "Skill +1",
        "Skill points +30"
    ],
    "Crap I Overslept": [
        "Mood -1, Skill points +45",
        "Energy +10, Wisdom +5"
    ],
    "Lunch Break Gotta Get My Together": [
        "Skill points +30",
        "A Small Breather +1"
    ],
    "Genius Efficiency!": [
        "Speed +15",
        "Speed +5, Power +10"
    ],
    "Enough to Break into a Dash!": [
        "Gap Closer +1",
        "Energy -10, Speed +10, Power +5"
    ],
    "Leave it to Me to Help Out!": [
        "Energy +15",
        "Stamina +10"
    ],
    "Leave it to Me to Be Considerate!": [
        "Deep Breaths +1",
        "Energy +10, Stamina +5"
    ],
    "Urara's Study Review": [
        "Energy +10, Wisdom +5",
        "Mood +1, Wisdom +5"
    ],
    "Uraras Long Shot Dash!": [
        "Long Shot +1",
        "Mood +1, Energy +10"
    ],
    "Memories of Cinema": [
        "Energy +25, Stamina +5, Mood +1",
        "Stamina +10, Guts +10, Mood +1"
    ],
    "My Chosen Way of Life": [
        "Energy +14, Mood +1",
        "Mood +1, Wisdom +6"
    ],
    "Enthusiastic Pair": [
        "Energy +14, Wisdom +6, Mood +1, Can start dating",
        "Mood -1, bond -5, Watchful Eye +1, Chain ended"
    ],
    "How I Play at the Park": [
        "Energy +35, Wisdom +6",
        "|Skill Points +18| OR |Speed +6, Skill points +56, Mood +1|"
    ],
    "Trainer Tip Always Improve Your Coaching": [
        "Energy +10, Skill Points +15",
        "Speed +5, Wisdom +5"
    ],
    "The Search for a Hobby": [
        "Energy +20, Skill Points +15, Mood +1, Can start dating",
        "Mood -1, Maverick +1, bond -5, Chain ended"
    ],
    "I'm Going to Win Tomorrow!": [
        "Wisdom +10",
        "Mood +1, Skill Points +15"
    ],
    "This Is Nothing!": [
        "Stamina to Spare +1",
        "Energy +20, Mood +1"
    ],
    "Hishiama's Struggles Problem Children": [
        "Energy +10, Wisdom +5",
        "Energy -10, Speed +10, Guts +5"
    ],
    "Hishiama's Struggles: Final Stretch": [
        "Hesitant End Closers +1",
        "Power +5, Skill Points +15"
    ],
    "Strict but Gracious": [
        "Go with the Flow +1",
        "Energy +10, Wisdom +10"
    ],
    "Agile but Strong": [
        "Power +15",
        "Speed +10, Stamina +5"
    ],
    "Umamusume Deficiency!": [
        "Energy +5, Speed +5",
        "Speed +5, Power +5"
    ],
    "Heavy Romance": [
        "Rainy Days +1",
        "Wet Conditions +1"
    ],
    "Tamamo's School Tour": [
        "Wisdom +10",
        "Stamina +5, Guts +5"
    ],
    "A Battle I Can't Lose!": [
        "Calm in a Crowd +1",
        "Stamina +5, Wisdom +5"
    ],
    "Lovely Training Weather": [
        "Wisdom +5, Skill Points +20",
        "Speed +10, Stamina +5",
        "Practice Perfect +1"
    ],
    "Wonderful New Shoes": [
        "Speed +5, Skill Points +10",
        "Energy -10, Stamina +5, Skill Points +20"
    ],
    "Reminiscent Clover": [
        "Corner Adept +1",
        "Guts +15"
    ],
    "Last-Minute Modal Theory": [
        "Power +15",
        "Speed +10, Skill Points +15"
    ],
    "Step-Out-of-Your-Comfort-Zone Theory": [
        "Energy -10, Inside Scoop +1",
        "Energy +10, Stamina +10"
    ],
    "Snack Advice for Mayano!": [
        "Stamina +5, Guts +5",
        "Stamina +10"
    ],
    "Fashion Advice for Mayano!": [
        "Straightaway Adept +1",
        "Stamina +10"
    ],
    "Solo Nighttime Run": [
        "Stamina +10",
        "Energy +10, Stamina +5"
    ],
    "A Taste of Silence": [
        "Stamina +5, Skill Points +15",
        "Non-Standard Distance +1"
    ],
    "I'm Not a Cyborg": [
        "Guts +10, Skill Points +15",
        "Energy -10, Corner Recovery +1, bond -5, Chain ended"
    ],
    "Do No Harm": [
        "Energy -10, Stamina +5, Power +15",
        "Energy +10, Wisdom +5"
    ],
    "Orders Must Be Followed": [
        "Focus +1",
        "Speed +10, Skill Points +15"
    ],
    "My Muscles and Me Onward to Tomorrow!": [
        "Energy -10, Power +15",
        "Energy +4, Power +5"
    ],
    "It's Not Like I Like Romance!": [
        "Pace Strategy +1",
        "Energy +30"
    ],
    "For a Spiffy Concert": [
        "Guts +10",
        "Energy -10, Guts +15"
    ],
    "Aiming for the City Spots": [
        "Energy -10, Mood +1, Guts +10",
        "Corner Acceleration +1"
    ],
    "It's a Game of Tag!": [
        "Energy +10, Speed +5",
        "Fast-Paced +1"
    ],
    "Full-Power Muscles!": [
        "Late Surger Corners +1",
        "Skill points +30"
    ],
    "Full-Power Muscles!": [
        "Stamina +5, Skill points +15",
        "Mood +1, Skill points +15"
    ],
    "Ten Minutes Left!": [
        "Guts +15",
        "Wisdom +10"
    ],
    "The Correlation between Sleep and Efficiency": [
        "Power +5, Wisdom +5",
        "Wisdom +10"
    ],
    "Happenstance Introduced Through Intervention": [
        "Late Surger Savvy +1",
        "Wisdom +10"
    ],
    "Verification Required": [
        "Energy +10, Guts +5",
        "Energy -10, Stamina +5, Guts +10"
    ],
    "Absolute Desire": [
        "Pace Strategy +1",
        "Maximum Energy +4, Guts +5"
    ],
    "Unforeseen Lunch": [
        "Energy +15",
        "Speed +5, Guts +5"
    ],
    "Responding to the Unforeseen": [
        "Guts +10",
        "Target in Sight +1"
    ],
    "Always on Stage": [
        "Wisdom +10",
        "Energy +25, Focus +1, Chain ended"
    ],
    "Chants Are the Life of a Concert": [
        "Stamina +5, Guts +10",
        "Wisdom +15"
    ],
    "If I'm Cute Come to My Show!": [
        "Energy -10, Power +10, Final Push +1",
        "Energy +10, Wisdom +5"
    ],
    "Just Leave Me Alone": [
        "Stamina +5, Skill Points +15",
        "Power +5, Skill Points +15"
    ],
    "Just Don't Bother Me": [
        "Pressure +1",
        "Skill Points +30"
    ],
    "Aspiring to Adulthood": [
        "Energy -10, Wisdom +20",
        "Wisdom +5, Skill Points +15"
    ],
    "Warmth Love and Lunch": [
        "Charming +1",
        "Energy +20"
    ],
    "Let's Bloom Beautifully": [
        "Wisdom +15",
        "Speed +10, Power +5"
    ],
    "A Hero's Woes": [
        "Energy +15",
        "Energy +5, Power +5"
    ],
    "Preparing My Special Move!": [
        "Sprint Straightaways +1",
        "Energy +30"
    ],
    "Marvelous No Question": [
        "Energy +10, Speed +5",
        "Mood +1, Speed +5"
    ],
    "How To Be More Marvelous": [
        "Energy +10, Mood +1",
        "Hanshin Racecourse +1"
    ],
    "Guidance and Friends": [
        "Skill Points +45",
        "|Energy +10, Mood +1, Right-Handed +3| OR |Energy -20, Right-Handed +1|"
    ],
    "Maximum Spirituality": [
        "Wisdom +5, Skill Points +15",
        "Energy -10, Speed +5, Stamina +5, Power +5"
    ],
    "When Piety and Kindness Intersect": [
        "Skill Points +30",
        "Energy +20"
    ],
    "What I'm Destined For": [
        "Energy +10, Guts +5",
        "|Energy -10, Wisdom +5| OR |Maximum Energy +4, Mood +1, Guts +5, Wisdom +5|"
    ],
    "I Will Change": [
        "Energy +10, Mood +1",
        "Guts +15"
    ],
    "Please Buy Some Carrots": [
        "Energy +10, Wisdom +5",
        "Pace Chaser Corners +1"
    ],
    "Give It a Try": [
        "Energy +15",
        "Mood +1, Skill Points +15"
    ],
    "Hope She'll Like It": [
        "Skill Points +45",
        "Unyielding Spirit +1"
    ],
    "Not like Meow": [
        "Energy +20",
        "Energy +10, Wisdom +5"
    ],
    "Chasing Their Backs": [
        "Energy +5, Wisdom +3",
        "bond +20"
    ],
    "Delicious Burden": [
        "Ramp Up +1",
        "Mood +1, Energy +4"
    ],
    "You May Socialize With Me!": [
        "Energy -20, Speed +10, Power +10, Wisdom +5",
        "Mood -1, Guts +25"
    ],
    "You May Advise Me!": [
        "Guts +10, Wisdom +5",
        "Homestretch Haste +1"
    ],
    "Sleight of Hand": [
        "Wisdom +5, Skill Points +15",
        "Power +5, Skill Points +15"
    ],
    "Seeking Uniqueness!": [
        "Mood +1",
        "Energy +10/+30"
    ],
    "Just A Typical Accident?!": [
        "Stamina +5, Guts +10",
        "Subdued Front Runners +1"
    ],
    "Just Your Typical Hard Work!": [
        "Speed +10",
        "Power +10"
    ],
    "Misdirection": [
        "Prepared to Pass +1",
        "Skill Points +30"
    ],
    "Diamond Fixation": [
        "Wisdom +5",
        "|Energy +15 Stamina +10| OR |Mood -1, Guts +20|"
    ],
    "Only for You": [
        "Energy -20, Stamina +30, Iron Will +1",
        "Energy +5, Guts +5, Iron Will +1"
    ],
    "I Love New Things!": [
        "Guts +10",
        "Energy -10, Stamina +20"
    ],
    "I Love Complicated Things!": [
        "Stamina +5, Guts +10",
        "Hesitant Front Runners +1"
    ],
    "Paying It Forward": [
        "Energy +10, Mood +1",
        "Speed +5/+10, Straightaway Adept +1"
    ],
    "Ah Home Sweet Home": [
        "Speed +5, Power +10",
        "Practice Perfect +1"
    ],
    "Ah Friendship": [
        "Mood +1, Power +5",
        "Energy +10"
    ],
    "CopyThisTextForMore": [
        "",
        ""
    ],
}

Width = GetSystemMetrics(0)
Height = GetSystemMetrics(1)

REGION = (0, 0, Width/3, Height/3)

class SupportOptionsApp:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.overrideredirect(True)
        self.ventana.attributes("-topmost", True)
        self.ventana.withdraw()
        self.ventana.config(bg='white')
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

        icon_path = Path(__file__).parent / "icon.ico"
        image = Image.open(icon_path)

        menu = pystray.Menu(
            pystray.MenuItem("Close", self.cerrar_aplicacion)
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

    def crear_rectangulo_redondeado(self, text, width=300, height=60):
        border_width = 1
        image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        draw.rounded_rectangle(
            [(border_width, border_width), (width-border_width-1, height-border_width-1)],
            radius=12,
            fill="#FFFFFF"
        )

        draw.rounded_rectangle(
            [(0, 0), (width-1, height-1)],
            radius=15,
            outline="#00B4D8",
            width=border_width,
            fill=None
        )

        try:
            font = ImageFont.truetype("arial.ttf", 12)
        except:
            font = ImageFont.load_default()

        lines = textwrap.wrap(text, width=48)
        y_text = 10
        for line in lines:
            draw.text((10, y_text), line, fill="#000000", font=font)
            y_text += 15

        return image

    def mostrar_opciones(self, opciones):
        if self.mostrando:
            return

        for widget in self.frame.winfo_children():
            widget.destroy()

        for opcion in opciones:
            img = self.crear_rectangulo_redondeado(opcion)
            tk_img = ImageTk.PhotoImage(img)

            label = Label(self.frame, image=tk_img, bg='white', bd=0)
            label.image = tk_img
            label.pack(pady=5)

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