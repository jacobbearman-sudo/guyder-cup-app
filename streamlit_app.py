import streamlit as st
import pandas as pd
import snowflake.connector
import os
import json

st.set_page_config(page_title="Guyder Cup IX - Captain's War Room", layout="wide")

SCOUTING_FILE = os.path.join(os.path.dirname(__file__), "scouting_data.json")
LINEUPS_FILE = os.path.join(os.path.dirname(__file__), "lineups_data.json")

def load_scouting_data():
    if os.path.exists(SCOUTING_FILE):
        with open(SCOUTING_FILE, "r") as f:
            return json.load(f)
    return {}

def save_scouting_data(data):
    with open(SCOUTING_FILE, "w") as f:
        json.dump(data, f, indent=2)

def load_lineups():
    if os.path.exists(LINEUPS_FILE):
        with open(LINEUPS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_lineups(data):
    with open(LINEUPS_FILE, "w") as f:
        json.dump(data, f, indent=2)

@st.cache_resource
def get_snowflake_conn():
    return snowflake.connector.connect(
        connection_name=os.getenv("SNOWFLAKE_CONNECTION_NAME") or "snowhouse"
    )

# ── DATA ──────────────────────────────────────────────────────────────────────

COURSES = {
    "Highlands": {
        "slope": 138, "rating": 71.3, "par": 71, "yardage": 6618, "tee": "II",
        "designer": "Bill Bergin & Rees Jones",
        "notes": (
            "Mountain course atop Lookout Mountain at McLemore Resort in Rising Fawn, GA. "
            "Huge greens, big elevation changes, wide fairways but steep hillsides punish misses. "
            "Starts Par 5-3-5-3-4-5. Bentgrass tee-to-green. Heroic par-3 tee shots over gullies. "
            "Favors: accurate iron players & good putters on huge undulating greens."
        ),
    },
    "The Keep": {
        "slope": 140, "rating": 73.7, "par": 72, "yardage": 7067, "tee": "Blue",
        "designer": "Bill Bergin & Rees Jones",
        "notes": (
            "Championship course at McLemore Resort on Lookout Mountain, Rising Fawn, GA. "
            "1.5 miles of cliff edge with dramatic views. Slope 140, rating 73.7. "
            "Blue tees at 7,067 yards. Over 70 acres of fairway. "
            "Demanding shot shaping off the tee with tight corridors. "
            "Favors: longer hitters who can work the ball both ways."
        ),
    },
}

SCHEDULE = [
    ("THURS PM", "Highlands", "1:00 - 1:30"),
    ("FRI AM", "The Keep", "8:30 - 8:50"),
    ("FRI PM", "The Keep", "2:00 - 2:50"),
    ("SAT AM", "The Keep", "10:40 - 11:10"),
]

TEAM_FISH = {
    "Fish": 1.6, "Larson": 8.0, "Bearman": 8.4, "Danny": 8.5,
    "Rames": 9.2, "Littel": 15.6, "Meyer": 20.9, "Doug": 23.7,
}

TEAM_BOOTH = {
    "Clinton": 3.6, "Niemeyer": 7.8, "J4": 9.6, "Rams": 10.7,
    "Rio": 11.9, "Booth": 15.6, "AB": 18.0, "Bobby": 20.5,
}

CAREER = {
    "Doug": {"overall": "4-2-0", "match": "9-3-1", "pts": 9.5, "pct": .667},
    "Rams": {"overall": "5-3-0", "match": "9-4-0", "pts": 9.0, "pct": .625},
    "Danny": {"overall": "4-4-0", "match": "8-3-2", "pts": 9.0, "pct": .500},
    "Clinton": {"overall": "4-4-0", "match": "9-4-0", "pts": 9.0, "pct": .500},
    "Bobby": {"overall": "3-4-0", "match": "7-4-2", "pts": 8.0, "pct": .429},
    "Niemeyer": {"overall": "2-2-0", "match": "7-5-1", "pts": 7.5, "pct": .500},
    "Rio": {"overall": "2-5-0", "match": "7-5-1", "pts": 7.5, "pct": .286},
    "Rames": {"overall": "4-2-0", "match": "7-3-0", "pts": 7.0, "pct": .667},
    "Bearman": {"overall": "4-4-0", "match": "6-6-1", "pts": 6.5, "pct": .500},
    "Fish": {"overall": "2-2-0", "match": "6-7-0", "pts": 6.0, "pct": .500},
    "AB": {"overall": "3-5-0", "match": "5-8-0", "pts": 5.0, "pct": .375},
    "AJ": {"overall": "4-3-0", "match": "4-8-1", "pts": 4.5, "pct": .571},
    "Meyer": {"overall": "1-7-0", "match": "2-7-4", "pts": 4.0, "pct": .125},
    "J4": {"overall": "5-3-0", "match": "4-9-0", "pts": 4.0, "pct": .625},
    "Larson": {"overall": "4-4-0", "match": "2-10-1", "pts": 2.5, "pct": .500},
    "Booth": {"overall": "1-3-0", "match": "2-10-1", "pts": 2.5, "pct": .250},
    "Littel": {"overall": "0-1-0", "match": "1-2-0", "pts": 1.0, "pct": .000},
}

MATCH_HISTORY = [
    {"year": 2025, "event": "Battle for Sarah", "type": "BB", "course": "Sand",
     "team_a": "Littel/Larson", "team_b": "Bobby/Danny", "result": "5&4", "winner": "a"},
    {"year": 2025, "event": "Battle for Sarah", "type": "BB", "course": "Sand",
     "team_a": "J4/AJ", "team_b": "Rio/Niemeyer", "result": "1up", "winner": "b"},
    {"year": 2025, "event": "Battle for Sarah", "type": "BB", "course": "Sand",
     "team_a": "Bearman/Booth", "team_b": "Doug/Clinton", "result": "1up", "winner": "b"},
    {"year": 2025, "event": "Battle for Sarah", "type": "BB", "course": "Sand",
     "team_a": "Meyer/Rams", "team_b": "Fish/AB", "result": "3&2", "winner": "a"},
    {"year": 2025, "event": "Battle for Sarah", "type": "BB", "course": "Mammoth",
     "team_a": "Bearman/J4", "team_b": "Rio/Niemeyer", "result": "1up", "winner": "b"},
    {"year": 2025, "event": "Battle for Sarah", "type": "BB", "course": "Mammoth",
     "team_a": "Larson/Littel", "team_b": "Doug/Clinton", "result": "4&2", "winner": "b"},
    {"year": 2025, "event": "Battle for Sarah", "type": "BB", "course": "Mammoth",
     "team_a": "Rams/Booth", "team_b": "Danny/Fish", "result": "2&1", "winner": "b"},
    {"year": 2025, "event": "Battle for Sarah", "type": "BB", "course": "Mammoth",
     "team_a": "Meyer/AJ", "team_b": "AB/Bobby", "result": "3&2", "winner": "b"},
    {"year": 2025, "event": "Battle for Sarah", "type": "Singles", "course": "Sedge",
     "team_a": "J4", "team_b": "Fish", "result": "2&1", "winner": "a"},
    {"year": 2025, "event": "Battle for Sarah", "type": "Singles", "course": "Sedge",
     "team_a": "Larson", "team_b": "Danny", "result": "6&4", "winner": "b"},
    {"year": 2025, "event": "Battle for Sarah", "type": "Singles", "course": "Sedge",
     "team_a": "Booth", "team_b": "Doug", "result": "2&1", "winner": "b"},
    {"year": 2025, "event": "Battle for Sarah", "type": "Singles", "course": "Sedge",
     "team_a": "Littel", "team_b": "Bobby", "result": "1up", "winner": "b"},
    {"year": 2025, "event": "Battle for Sarah", "type": "Singles", "course": "Sedge",
     "team_a": "Meyer", "team_b": "AB", "result": "5&4", "winner": "b"},
    {"year": 2025, "event": "Battle for Sarah", "type": "Singles", "course": "Sedge",
     "team_a": "Bearman", "team_b": "Niemeyer", "result": "3&2", "winner": "a"},
    {"year": 2025, "event": "Battle for Sarah", "type": "Singles", "course": "Sedge",
     "team_a": "Littel", "team_b": "Clinton", "result": "2&1", "winner": "b"},
    {"year": 2025, "event": "Battle for Sarah", "type": "Singles", "course": "Sedge",
     "team_a": "Rams", "team_b": "Rio", "result": "2&1", "winner": "a"},
    {"year": 2024, "event": "Wet", "type": "BB", "course": "Loop Red",
     "team_a": "Bearman/Rams", "team_b": "Bobby/AJ", "result": "4&2", "winner": "b"},
    {"year": 2024, "event": "Wet", "type": "BB", "course": "Loop Red",
     "team_a": "Danny/AB", "team_b": "Larson/Doug", "result": "1up", "winner": "a"},
    {"year": 2024, "event": "Wet", "type": "BB", "course": "Loop Red",
     "team_a": "Clinton/Rames", "team_b": "J4/Meyer", "result": "1up", "winner": "a"},
    {"year": 2024, "event": "Wet", "type": "BB", "course": "Loop Red",
     "team_a": "Rio/Niemeyer", "team_b": "Fish/Booth", "result": "1up", "winner": "b"},
    {"year": 2024, "event": "Wet", "type": "BB", "course": "FD",
     "team_a": "Rames/Clinton", "team_b": "J4/Larson", "result": "2&1", "winner": "a"},
    {"year": 2024, "event": "Wet", "type": "BB", "course": "FD",
     "team_a": "Rio/Niemeyer", "team_b": "AJ/Bobby", "result": "2&1", "winner": "a"},
    {"year": 2024, "event": "Wet", "type": "BB", "course": "FD",
     "team_a": "AB/Rams", "team_b": "Meyer/Doug", "result": "2&1", "winner": "b"},
    {"year": 2024, "event": "Wet", "type": "BB", "course": "FD",
     "team_a": "Danny/Bearman", "team_b": "Fish/Booth", "result": "1up", "winner": "a"},
    {"year": 2024, "event": "Wet", "type": "Singles", "course": "FD",
     "team_a": "AB", "team_b": "Doug", "result": "4&3", "winner": "b"},
    {"year": 2024, "event": "Wet", "type": "Singles", "course": "FD",
     "team_a": "Rio", "team_b": "J4", "result": "3&2", "winner": "a"},
    {"year": 2024, "event": "Wet", "type": "Singles", "course": "FD",
     "team_a": "Bearman", "team_b": "Booth", "result": "3&2", "winner": "a"},
    {"year": 2024, "event": "Wet", "type": "Singles", "course": "FD",
     "team_a": "Clinton", "team_b": "Fish", "result": "1up", "winner": "b"},
    {"year": 2024, "event": "Wet", "type": "Singles", "course": "FD",
     "team_a": "Rams", "team_b": "Bobby", "result": "4&2", "winner": "a"},
    {"year": 2024, "event": "Wet", "type": "Singles", "course": "FD",
     "team_a": "Niemeyer", "team_b": "Larson", "result": "4&2", "winner": "a"},
    {"year": 2024, "event": "Wet", "type": "Singles", "course": "FD",
     "team_a": "Rames", "team_b": "AJ", "result": "3&1", "winner": "a"},
    {"year": 2024, "event": "Wet", "type": "Singles", "course": "FD",
     "team_a": "Danny", "team_b": "Meyer", "result": "AS", "winner": "as"},
    {"year": 2023, "event": "Black Magic", "type": "BB", "course": "Player",
     "team_a": "Doug/Clinton", "team_b": "Larson/AB", "result": "5&4", "winner": "a"},
    {"year": 2023, "event": "Black Magic", "type": "BB", "course": "Player",
     "team_a": "Rames/J4", "team_b": "Niemeyer/Rio", "result": "3&1", "winner": "b"},
    {"year": 2023, "event": "Black Magic", "type": "BB", "course": "Player",
     "team_a": "Bobby/AJ", "team_b": "Danny/Meyer", "result": "AS", "winner": "as"},
    {"year": 2023, "event": "Black Magic", "type": "BB", "course": "Player",
     "team_a": "Bearman/Rams", "team_b": "Booth/Fish", "result": "3&2", "winner": "a"},
    {"year": 2023, "event": "Black Magic", "type": "BB", "course": "Trevino",
     "team_a": "J4/Rames", "team_b": "Danny/Booth", "result": "3&2", "winner": "a"},
    {"year": 2023, "event": "Black Magic", "type": "BB", "course": "Trevino",
     "team_a": "Bearman/Rams", "team_b": "AB/Niemeyer", "result": "3&1", "winner": "a"},
    {"year": 2023, "event": "Black Magic", "type": "BB", "course": "Trevino",
     "team_a": "Clinton/Doug", "team_b": "Fish/Meyer", "result": "5&4", "winner": "a"},
    {"year": 2023, "event": "Black Magic", "type": "BB", "course": "Trevino",
     "team_a": "Bobby/AJ", "team_b": "Larson/Rio", "result": "1up", "winner": "a"},
    {"year": 2023, "event": "Black Magic", "type": "Singles", "course": "Erin Hills",
     "team_a": "Rames", "team_b": "Rio", "result": "3&2", "winner": "b"},
    {"year": 2023, "event": "Black Magic", "type": "Singles", "course": "Erin Hills",
     "team_a": "Doug", "team_b": "Meyer", "result": "AS", "winner": "as"},
    {"year": 2023, "event": "Black Magic", "type": "Singles", "course": "Erin Hills",
     "team_a": "Clinton", "team_b": "Larson", "result": "4&3", "winner": "a"},
    {"year": 2023, "event": "Black Magic", "type": "Singles", "course": "Erin Hills",
     "team_a": "AJ", "team_b": "AB", "result": "2&1", "winner": "b"},
    {"year": 2023, "event": "Black Magic", "type": "Singles", "course": "Erin Hills",
     "team_a": "Bearman", "team_b": "Niemeyer", "result": "3&2", "winner": "b"},
    {"year": 2023, "event": "Black Magic", "type": "Singles", "course": "Erin Hills",
     "team_a": "Bobby", "team_b": "Danny", "result": "1up", "winner": "a"},
    {"year": 2023, "event": "Black Magic", "type": "Singles", "course": "Erin Hills",
     "team_a": "J4", "team_b": "Booth", "result": "5&4", "winner": "a"},
    {"year": 2023, "event": "Black Magic", "type": "Singles", "course": "Erin Hills",
     "team_a": "Rams", "team_b": "Fish", "result": "1up", "winner": "a"},
    {"year": 2022, "event": "Wheels Up", "type": "BB", "course": "#7",
     "team_a": "Bearman/Rio", "team_b": "Larson/J4", "result": "3&2", "winner": "b"},
    {"year": 2022, "event": "Wheels Up", "type": "BB", "course": "#7",
     "team_a": "Rames/Clinton", "team_b": "Fish/Booth", "result": "5&3", "winner": "b"},
    {"year": 2022, "event": "Wheels Up", "type": "BB", "course": "#7",
     "team_a": "Niemeyer/Meyer", "team_b": "Bobby/Danny", "result": "2up", "winner": "b"},
    {"year": 2022, "event": "Wheels Up", "type": "BB", "course": "#7",
     "team_a": "Rams/Doug", "team_b": "AJ/AB", "result": "3&2", "winner": "a"},
    {"year": 2022, "event": "Wheels Up", "type": "BB", "course": "#4",
     "team_a": "Bearman/Rams", "team_b": "Fish/Bobby", "result": "2&1", "winner": "a"},
    {"year": 2022, "event": "Wheels Up", "type": "BB", "course": "#4",
     "team_a": "Clinton/Doug", "team_b": "Larson/J4", "result": "4&3", "winner": "a"},
    {"year": 2022, "event": "Wheels Up", "type": "BB", "course": "#4",
     "team_a": "Rames/Niemeyer", "team_b": "Booth/AB", "result": "1up", "winner": "a"},
    {"year": 2022, "event": "Wheels Up", "type": "BB", "course": "#4",
     "team_a": "Rio/Meyer", "team_b": "AJ/AJ", "result": "5&4", "winner": "b"},
    {"year": 2022, "event": "Wheels Up", "type": "Singles", "course": "#2",
     "team_a": "Meyer", "team_b": "Bobby", "result": "AS", "winner": "as"},
    {"year": 2022, "event": "Wheels Up", "type": "Singles", "course": "#2",
     "team_a": "Clinton", "team_b": "Fish", "result": "4&3", "winner": "b"},
    {"year": 2022, "event": "Wheels Up", "type": "Singles", "course": "#2",
     "team_a": "Bearman", "team_b": "Larson", "result": "AS", "winner": "as"},
    {"year": 2022, "event": "Wheels Up", "type": "Singles", "course": "#2",
     "team_a": "Niemeyer", "team_b": "J4", "result": "6&5", "winner": "a"},
    {"year": 2022, "event": "Wheels Up", "type": "Singles", "course": "#2",
     "team_a": "Doug", "team_b": "AJ", "result": "2up", "winner": "b"},
    {"year": 2022, "event": "Wheels Up", "type": "Singles", "course": "#2",
     "team_a": "Rams", "team_b": "Danny", "result": "2&1", "winner": "b"},
    {"year": 2022, "event": "Wheels Up", "type": "Singles", "course": "#2",
     "team_a": "Rio", "team_b": "AB", "result": "2&1", "winner": "a"},
    {"year": 2022, "event": "Wheels Up", "type": "Singles", "course": "#2",
     "team_a": "Rames", "team_b": "Booth", "result": "4&2", "winner": "a"},
]

CRADLE_TIEBREAKER = {
    "year": 2022, "event": "Wheels Up", "course": "The Cradle",
    "overall_winner": "Team Larson", "overall_result": "5-3",
    "matches": [
        {"team_a": "Clinton", "team_b": "Fish", "winner": "b"},
        {"team_a": "Niemeyer", "team_b": "Larson", "winner": "a"},
        {"team_a": "Bearman", "team_b": "Danny", "winner": "b"},
        {"team_a": "Rames", "team_b": "J4", "winner": "a"},
        {"team_a": "Rams", "team_b": "AJ", "winner": "a"},
        {"team_a": "Rio", "team_b": "Booth", "winner": "as"},
        {"team_a": "Meyer", "team_b": "AB", "winner": "b"},
        {"team_a": "Doug", "team_b": "Bobby", "winner": "b"},
    ],
}

def course_hcap(index, course_name):
    c = COURSES[course_name]
    return round(index * (c["slope"] / 113) + (c["rating"] - c["par"]), 1)

def stroke_diff(fish_idx, opp_idx, course_name):
    return round(course_hcap(fish_idx, course_name) - course_hcap(opp_idx, course_name), 1)

def get_h2h(player_a, player_b):
    wins, losses, halves = 0, 0, 0
    details = []
    for m in MATCH_HISTORY:
        a_in, b_in = False, False
        a_players = [p.strip() for p in m["team_a"].split("/")]
        b_players = [p.strip() for p in m["team_b"].split("/")]
        if player_a in a_players:
            a_in = True
        if player_a in b_players:
            b_in = True
        if player_b in a_players and a_in:
            continue
        if player_b in b_players and b_in:
            continue
        opp_side = None
        if a_in and player_b in b_players:
            opp_side = "b"
        elif b_in and player_b in a_players:
            opp_side = "a"
        if opp_side is None:
            continue
        if m["winner"] == "as":
            halves += 1
            details.append(f"{m['year']} {m['type']}: AS")
        elif (a_in and m["winner"] == "a") or (b_in and m["winner"] == "b"):
            wins += 1
            details.append(f"{m['year']} {m['type']}: W {m['result']}")
        else:
            losses += 1
            details.append(f"{m['year']} {m['type']}: L {m['result']}")
    for m in CRADLE_TIEBREAKER["matches"]:
        a_in = player_a == m["team_a"]
        b_in = player_a == m["team_b"]
        if not a_in and not b_in:
            continue
        if (a_in and player_b != m["team_b"]) or (b_in and player_b != m["team_a"]):
            continue
        yr = CRADLE_TIEBREAKER["year"]
        if m["winner"] == "as":
            halves += 1
            details.append(f"{yr} Cradle: AS")
        elif (a_in and m["winner"] == "a") or (b_in and m["winner"] == "b"):
            wins += 1
            details.append(f"{yr} Cradle: W")
        else:
            losses += 1
            details.append(f"{yr} Cradle: L")
    return wins, losses, halves, details

SCOUTING_CATEGORIES = ["Driving Dist", "Driving Acc", "Iron Dist", "Iron Acc", "Short Game", "Putting", "Shot Shape", "X-Factor"]
SCOUTING_WEIGHTS = {"Driving Dist": 1, "Driving Acc": 1, "Iron Dist": 1, "Iron Acc": 1, "Short Game": 1, "Putting": 1, "Shot Shape": 1, "X-Factor": 2}

COURSE_SKILL_WEIGHTS = {
    "The Keep": {"Driving Dist": 3, "Driving Acc": 2, "Iron Dist": 2, "Iron Acc": 2, "Short Game": 1, "Putting": 1, "Shot Shape": 3, "X-Factor": 3},
}

def scouting_score(player):
    if "scouting" not in st.session_state:
        return 0
    ratings = st.session_state.scouting.get(player, {})
    total_w = sum(SCOUTING_WEIGHTS[c] * (ratings.get(c, {}).get("rating", 3)) for c in SCOUTING_CATEGORIES)
    total_weight = sum(SCOUTING_WEIGHTS[c] for c in SCOUTING_CATEGORIES)
    return (total_w / total_weight) - 3

def course_fit_score(player, course_name):
    if "scouting" not in st.session_state:
        return 3.0
    ratings = st.session_state.scouting.get(player, {})
    weights = COURSE_SKILL_WEIGHTS[course_name]
    total_w = sum(weights[c] * ratings.get(c, {}).get("rating", 3) for c in SCOUTING_CATEGORIES)
    total_weight = sum(weights[c] for c in SCOUTING_CATEGORIES)
    return total_w / total_weight

def course_fit_grade(score):
    if score >= 4.5:
        return "A"
    elif score >= 3.5:
        return "B"
    elif score >= 2.5:
        return "C"
    elif score >= 1.5:
        return "D"
    return "F"

def singles_record(player):
    w, l, h = 0, 0, 0
    for m in MATCH_HISTORY:
        if m["type"] != "Singles":
            continue
        if m["team_a"] == player:
            if m["winner"] == "a":
                w += 1
            elif m["winner"] == "b":
                l += 1
            else:
                h += 1
        elif m["team_b"] == player:
            if m["winner"] == "b":
                w += 1
            elif m["winner"] == "a":
                l += 1
            else:
                h += 1
    return f"{w}-{l}-{h}"

def match_win_pct(player):
    rec = CAREER.get(player, {}).get("match", "0-0-0")
    parts = rec.split("-")
    mw, ml = int(parts[0]), int(parts[1])
    return mw / (mw + ml) if (mw + ml) > 0 else 0.5

def singles_match_win_pct(player):
    w, l, h = 0, 0, 0
    for m in MATCH_HISTORY:
        if m["type"] != "Singles":
            continue
        if m["team_a"] == player:
            if m["winner"] == "a":
                w += 1
            elif m["winner"] == "b":
                l += 1
            else:
                h += 1
        elif m["team_b"] == player:
            if m["winner"] == "b":
                w += 1
            elif m["winner"] == "a":
                l += 1
            else:
                h += 1
    return w / (w + l) if (w + l) > 0 else 0.5

def get_singles_h2h(player_a, player_b):
    wins, losses, halves = 0, 0, 0
    for m in MATCH_HISTORY:
        if m["type"] != "Singles":
            continue
        if m["team_a"] == player_a and m["team_b"] == player_b:
            if m["winner"] == "a":
                wins += 1
            elif m["winner"] == "b":
                losses += 1
            else:
                halves += 1
        elif m["team_b"] == player_a and m["team_a"] == player_b:
            if m["winner"] == "b":
                wins += 1
            elif m["winner"] == "a":
                losses += 1
            else:
                halves += 1
    return wins, losses, halves

def matchup_grade(stroke_adv, h2h_w, h2h_l, opp_career_pct, fish_player=None, opp_player=None):
    sw, sl, sh = get_singles_h2h(fish_player, opp_player) if fish_player and opp_player else (h2h_w, h2h_l, 0)

    if sw + sl > 0:
        h2h_score = 5 + ((sw - sl) / (sw + sl)) * 5
    else:
        h2h_score = 5
    fish_match_pct = singles_match_win_pct(fish_player) if fish_player else 0.5
    opp_match_pct = singles_match_win_pct(opp_player) if opp_player else 0.5
    match_score = min(max(5 + (fish_match_pct - opp_match_pct) * 5, 0), 10)
    h2h_total = sw + sl + sh
    if h2h_total == 0:
        h2h_w_pct, match_w_pct = 0.60, 0.40
    elif h2h_total == 1:
        h2h_w_pct, match_w_pct = 0.50, 0.50
    else:
        h2h_w_pct, match_w_pct = 0.70, 0.30
    historical = min(max(h2h_score * h2h_w_pct + match_score * match_w_pct, 0), 10)

    handicap = min(max(5 - stroke_adv * 1.5, 0), 10)

    scout_diff = 0
    if fish_player and opp_player:
        scout_diff = scouting_score(fish_player) - scouting_score(opp_player)
    scouting = min(max(5 + scout_diff * 2.5, 0), 10)

    fish_fit = course_fit_score(fish_player, "The Keep") if fish_player else 3.0
    opp_fit = course_fit_score(opp_player, "The Keep") if opp_player else 3.0
    fit_diff = fish_fit - opp_fit
    course_fit = min(max(5 + fit_diff * 2.5, 0), 10)

    total = historical * 0.35 + scouting * 0.25 + course_fit * 0.25 + handicap * 0.15

    if total >= 7.5:
        grade = "A"
    elif total >= 6:
        grade = "B"
    elif total >= 4.5:
        grade = "C"
    elif total >= 3:
        grade = "D"
    else:
        grade = "F"

    return grade, {"historical": round(historical, 1), "handicap": round(handicap, 1), "scouting": round(scouting, 1), "course_fit": round(course_fit, 1), "total": round(total, 1)}

def bb_matchup_grade(f1, f2, b1, b2):
    fish_low_k = min(course_hcap(TEAM_FISH[f1], "The Keep"), course_hcap(TEAM_FISH[f2], "The Keep"))
    opp_low_k = min(course_hcap(TEAM_BOOTH[b1], "The Keep"), course_hcap(TEAM_BOOTH[b2], "The Keep"))
    avg_edge = opp_low_k - fish_low_k
    handicap = min(max(5 - avg_edge * 1.5, 0), 10)

    total_w, total_l = 0, 0
    for fp in (f1, f2):
        for bp in (b1, b2):
            w, l, _, _ = get_h2h(fp, bp)
            total_w += w
            total_l += l
    if total_w + total_l > 0:
        h2h_score = 5 + ((total_w - total_l) / (total_w + total_l)) * 5
    else:
        h2h_score = 5
    avg_fish_pct = (CAREER.get(f1, {}).get("pct", 0) + CAREER.get(f2, {}).get("pct", 0)) / 2
    avg_opp_pct = (CAREER.get(b1, {}).get("pct", 0) + CAREER.get(b2, {}).get("pct", 0)) / 2
    career_score = 5 + (avg_fish_pct - avg_opp_pct) * 5
    avg_fish_match = (match_win_pct(f1) + match_win_pct(f2)) / 2
    avg_opp_match = (match_win_pct(b1) + match_win_pct(b2)) / 2
    match_score = min(max(5 + (avg_fish_match - avg_opp_match) * 5, 0), 10)
    historical = min(max(h2h_score * 0.50 + match_score * 0.35 + career_score * 0.15, 0), 10)

    fish_scout = (scouting_score(f1) + scouting_score(f2)) / 2
    opp_scout = (scouting_score(b1) + scouting_score(b2)) / 2
    scout_diff = fish_scout - opp_scout
    scouting = min(max(5 + scout_diff * 2.5, 0), 10)

    fish_fit = (course_fit_score(f1, "The Keep") + course_fit_score(f2, "The Keep")) / 2
    opp_fit = (course_fit_score(b1, "The Keep") + course_fit_score(b2, "The Keep")) / 2
    fit_diff = fish_fit - opp_fit
    course_fit = min(max(5 + fit_diff * 2.5, 0), 10)

    total = historical * 0.35 + scouting * 0.25 + course_fit * 0.25 + handicap * 0.15

    if total >= 7.5:
        grade = "A"
    elif total >= 6:
        grade = "B"
    elif total >= 4.5:
        grade = "C"
    elif total >= 3:
        grade = "D"
    else:
        grade = "F"

    return grade, {"historical": round(historical, 1), "handicap": round(handicap, 1), "scouting": round(scouting, 1), "course_fit": round(course_fit, 1), "total": round(total, 1)}


def bb_pair_history(p1, p2):
    w, l = 0, 0
    for m in MATCH_HISTORY:
        if m["type"] != "BB":
            continue
        pair_a = set(m["team_a"].split("/"))
        pair_b = set(m["team_b"].split("/"))
        pair = {p1, p2}
        if pair == pair_a:
            if m["winner"] == "a":
                w += 1
            elif m["winner"] == "b":
                l += 1
        elif pair == pair_b:
            if m["winner"] == "b":
                w += 1
            elif m["winner"] == "a":
                l += 1
    return w, l


def bb_individual_record(player):
    w, l = 0, 0
    for m in MATCH_HISTORY:
        if m["type"] != "BB":
            continue
        in_a = player in m["team_a"].split("/")
        in_b = player in m["team_b"].split("/")
        if in_a:
            if m["winner"] == "a":
                w += 1
            elif m["winner"] == "b":
                l += 1
        elif in_b:
            if m["winner"] == "b":
                w += 1
            elif m["winner"] == "a":
                l += 1
    return w, l


def scouting_complement_score(p1, p2):
    if "scouting" not in st.session_state:
        return 5.0
    r1 = st.session_state.scouting.get(p1, {})
    r2 = st.session_state.scouting.get(p2, {})
    if not r1 and not r2:
        return 5.0
    covered = 0
    for cat in SCOUTING_CATEGORIES:
        v1 = r1.get(cat, {}).get("rating", 3)
        v2 = r2.get(cat, {}).get("rating", 3)
        best = max(v1, v2)
        covered += best
    return min(max((covered / len(SCOUTING_CATEGORIES) - 3) * 5, 0), 10)


def bb_partner_grade(p1, p2):
    idx1, idx2 = TEAM_FISH[p1], TEAM_FISH[p2]
    spread = abs(idx1 - idx2)
    if spread >= 12:
        hcap_score = 9.0
    elif spread >= 8:
        hcap_score = 7.5
    elif spread >= 4:
        hcap_score = 5.5
    else:
        hcap_score = 3.5

    complement = scouting_complement_score(p1, p2)

    fit1 = course_fit_score(p1, "The Keep")
    fit2 = course_fit_score(p2, "The Keep")
    avg_fit = (fit1 + fit2) / 2
    best_fit = max(fit1, fit2)
    combined_fit = min(max((avg_fit + best_fit) / 2 - 2, 0) * 3.33, 10)

    pair_w, pair_l = bb_pair_history(p1, p2)
    ind_w1, ind_l1 = bb_individual_record(p1)
    ind_w2, ind_l2 = bb_individual_record(p2)
    if pair_w + pair_l > 0:
        pair_pct = pair_w / (pair_w + pair_l)
        history = min(max(pair_pct * 10, 0), 10)
    else:
        total_ind_w = ind_w1 + ind_w2
        total_ind_l = ind_l1 + ind_l2
        if total_ind_w + total_ind_l > 0:
            ind_pct = total_ind_w / (total_ind_w + total_ind_l)
            history = min(max(ind_pct * 10, 0), 10)
        else:
            history = 5.0

    total = hcap_score * 0.30 + complement * 0.25 + combined_fit * 0.25 + history * 0.20

    if total >= 7.5:
        grade = "A"
    elif total >= 6:
        grade = "B"
    elif total >= 4.5:
        grade = "C"
    elif total >= 3:
        grade = "D"
    else:
        grade = "F"

    return grade, {
        "handicap_spread": round(hcap_score, 1),
        "scouting_comp": round(complement, 1),
        "course_fit": round(combined_fit, 1),
        "bb_history": round(history, 1),
        "total": round(total, 1),
    }


# ── SIDEBAR ───────────────────────────────────────────────────────────────────

st.sidebar.title(":golf: Guyder Cup IX")
st.sidebar.caption("2026 Civil War - Captain's War Room")
st.sidebar.divider()

if "fish_indexes" not in st.session_state:
    st.session_state.fish_indexes = dict(TEAM_FISH)
if "booth_indexes" not in st.session_state:
    st.session_state.booth_indexes = dict(TEAM_BOOTH)

with st.sidebar.expander("Edit handicap indexes", expanded=False):
    st.caption("Team Fish")
    for name in sorted(TEAM_FISH.keys(), key=lambda n: TEAM_FISH[n]):
        st.session_state.fish_indexes[name] = st.number_input(
            name, value=st.session_state.fish_indexes[name],
            min_value=-5.0, max_value=54.0, step=0.1, format="%.1f",
            key=f"idx_fish_{name}",
        )
    st.caption("Team Booth")
    for name in sorted(TEAM_BOOTH.keys(), key=lambda n: TEAM_BOOTH[n]):
        st.session_state.booth_indexes[name] = st.number_input(
            name, value=st.session_state.booth_indexes[name],
            min_value=-5.0, max_value=54.0, step=0.1, format="%.1f",
            key=f"idx_booth_{name}",
        )

TEAM_FISH = st.session_state.fish_indexes
TEAM_BOOTH = st.session_state.booth_indexes

st.sidebar.subheader("Team Fish")
fish_avg = sum(TEAM_FISH.values()) / len(TEAM_FISH)
booth_avg = sum(TEAM_BOOTH.values()) / len(TEAM_BOOTH)
st.sidebar.metric("Avg Handicap Index", f"{fish_avg:.1f}", f"{fish_avg - booth_avg:+.1f} vs Booth")
for name, idx in sorted(TEAM_FISH.items(), key=lambda x: x[1]):
    st.sidebar.text(f"  {name}: {idx}")
st.sidebar.divider()
st.sidebar.subheader("Team Booth")
st.sidebar.metric("Avg Handicap Index", f"{booth_avg:.1f}")
for name, idx in sorted(TEAM_BOOTH.items(), key=lambda x: x[1]):
    st.sidebar.text(f"  {name}: {idx}")
st.sidebar.divider()
st.sidebar.subheader("Schedule")
for day, course, times in SCHEDULE:
    st.sidebar.text(f"{day}: {course} ({times})")

st.sidebar.divider()
st.sidebar.subheader(":robot_face: War Room AI")

def build_war_room_context():
    lines = ["You are the Guyder Cup IX strategy assistant. Answer questions about matchup data, grades, and strategy."]
    lines.append("\n## Teams & Handicap Indices")
    lines.append("Team Fish: " + ", ".join(f"{n} ({v})" for n, v in sorted(TEAM_FISH.items(), key=lambda x: x[1])))
    lines.append("Team Booth: " + ", ".join(f"{n} ({v})" for n, v in sorted(TEAM_BOOTH.items(), key=lambda x: x[1])))
    lines.append("\n## Courses")
    for cname, cd in COURSES.items():
        lines.append(f"{cname}: slope={cd['slope']}, rating={cd['rating']}, par={cd['par']}")
    lines.append("\n## Course Handicap Formula")
    lines.append("Course Handicap = Index * (Slope / 113) + (Rating - Par)")
    lines.append("\n## Matchup Grading System (Category Blend 50/25/25)")
    lines.append("Three sub-scores 0-10: Historical Performance (H2H win rate 50% + match W% differential 35% + career W% differential 15%), Handicap Edge (stroke advantage), Scouting (rating differential).")
    lines.append("Total = Intangibles*0.50 + Handicap*0.25 + Scouting*0.25. A>=6.5, B>=4, C<4. All sub-scores centered at 5 (neutral/even).")
    lines.append("\n## Career Stats")
    for name in sorted(CAREER.keys()):
        c = CAREER[name]
        team = "Fish" if name in TEAM_FISH else "Booth"
        lines.append(f"{name} ({team}): overall={c.get('overall','N/A')}, match={c.get('match','N/A')}, pts={c.get('pts',0)}, win%={c.get('pct',0):.0%}")
    lines.append("\n## Head-to-Head Records (Fish players vs Booth players)")
    for fp in sorted(TEAM_FISH.keys()):
        for bp in sorted(TEAM_BOOTH.keys()):
            w, l, h, details = get_h2h(fp, bp)
            if w + l + h > 0:
                lines.append(f"{fp} vs {bp}: {w}-{l}-{h} — {'; '.join(details)}")
    if "singles_assignments" in st.session_state:
        lines.append("\n## Current Singles Assignments")
        for fp, opp in st.session_state.singles_assignments.items():
            fi = TEAM_FISH[fp]
            oi = TEAM_BOOTH[opp]
            h_diff = round(course_hcap(oi, "Highlands") - course_hcap(fi, "Highlands"), 1)
            k_diff = round(course_hcap(oi, "The Keep") - course_hcap(fi, "The Keep"), 1)
            w, l, h, _ = get_h2h(fp, opp)
            opp_pct = CAREER.get(opp, {}).get("pct", 0)
            grade, breakdown = matchup_grade(h_diff, w, l, opp_pct, fp, opp)
            lines.append(f"{fp} vs {opp}: strokes H={h_diff:+.0f} K={k_diff:+.0f}, H2H={w}-{l}-{h}, opp_pct={opp_pct:.0%}, grade={grade} (historical={breakdown['historical']}, handicap={breakdown['handicap']}, scouting={breakdown['scouting']}, course_fit={breakdown['course_fit']})")
    if "scouting" in st.session_state:
        scouted = {p: s for p, s in st.session_state.scouting.items() if any(s.get(c, {}).get("rating", 3) != 3 for c in SCOUTING_CATEGORIES) or s.get("notes", "")}
        if scouted:
            lines.append("\n## Scouting Reports")
            for p, s in sorted(scouted.items()):
                ratings = ", ".join(f"{c}={s.get(c,{}).get('rating',3)}" for c in SCOUTING_CATEGORIES)
                notes = s.get("notes", "")
                lines.append(f"{p}: {ratings}" + (f" — {notes}" if notes else ""))
    return "\n".join(lines)

def ask_war_room(question):
    ctx = build_war_room_context()
    prompt = f"{ctx}\n\n## User Question\n{question}\n\nAnswer concisely and specifically, referencing the data above. If discussing grades, explain the score calculation."
    try:
        conn = get_snowflake_conn()
        cur = conn.cursor()
        cur.execute(
            "SELECT SNOWFLAKE.CORTEX.COMPLETE(%s, %s)",
            ("claude-3-5-sonnet", prompt)
        )
        result = cur.fetchone()[0]
        cur.close()
        return result
    except Exception as e:
        return f"Error: {e}"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for msg in st.session_state.chat_history:
    with st.sidebar.chat_message(msg["role"]):
        st.sidebar.markdown(msg["content"])

if prompt := st.sidebar.chat_input("Ask about matchups..."):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.sidebar.chat_message("user"):
        st.sidebar.markdown(prompt)
    with st.sidebar.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = ask_war_room(prompt)
        st.sidebar.markdown(response)
    st.session_state.chat_history.append({"role": "assistant", "content": response})

if "scouting" not in st.session_state:
    st.session_state.scouting = load_scouting_data()
    for p in st.session_state.scouting:
        if "Mental" in st.session_state.scouting[p] and "X-Factor" not in st.session_state.scouting[p]:
            st.session_state.scouting[p]["X-Factor"] = st.session_state.scouting[p].pop("Mental")

# ── TABS ──────────────────────────────────────────────────────────────────────

tab1, tab2, tab5, tab4, tab3, tab6, tab7 = st.tabs([
    ":crossed_swords: Singles Matchups",
    ":handshake: Best Ball Pairings",
    ":mag: Scouting Report",
    ":scroll: History",
    ":mountain: Course Fit",
    ":bar_chart: Matchup Matrix",
    ":trophy: H2H Singles",
])


# ── TAB 1: SINGLES ────────────────────────────────────────────────────────────

with tab1:
    st.header("Singles matchup builder")
    st.caption("Assign each Team Fish player an opponent.")

    default_order = ["Bobby", "J4", "Rio", "Niemeyer", "Booth", "Clinton", "AB", "Rams"]
    fish_order = ["Fish", "Rames", "Bearman", "Danny", "Larson", "Doug", "Meyer", "Littel"]

    saved_lineups = load_lineups()
    if "singles_assignments" not in st.session_state:
        saved_singles = saved_lineups.get("singles", {})
        if saved_singles:
            st.session_state.singles_assignments = saved_singles
        else:
            st.session_state.singles_assignments = {f: default_order[i] for i, f in enumerate(fish_order)}

    save_s_col, status_s_col = st.columns([1, 4])
    with save_s_col:
        if st.button("💾 Save singles lineup", type="primary", use_container_width=True):
            lineups = load_lineups()
            lineups["singles"] = st.session_state.singles_assignments
            save_lineups(lineups)
            st.session_state._singles_saved = True
    with status_s_col:
        if st.session_state.get("_singles_saved"):
            st.success("Singles lineup saved!", icon="✅")
            st.session_state._singles_saved = False

    new_assignments = {}
    opponents_list = list(TEAM_BOOTH.keys())

    booth_sorted = sorted(TEAM_BOOTH.keys(), key=lambda n: TEAM_BOOTH[n])

    for fish_player in fish_order:
        current = st.session_state.singles_assignments.get(fish_player, opponents_list[0])
        if current not in opponents_list:
            current = opponents_list[0]

        with st.expander(f"**{fish_player}** ({TEAM_FISH[fish_player]})", expanded=False):
            choice = st.selectbox(
                "Assigned opponent", opponents_list,
                index=opponents_list.index(current),
                key=f"singles_{fish_player}",
            )
            new_assignments[fish_player] = choice

            rows = []
            for bp in booth_sorted:
                opp_idx = TEAM_BOOTH[bp]
                strokes_k = round(course_hcap(opp_idx, "The Keep") - course_hcap(TEAM_FISH[fish_player], "The Keep"))
                k_diff = stroke_diff(TEAM_FISH[fish_player], opp_idx, "The Keep")
                w, l, h = get_singles_h2h(fish_player, bp)
                opp_pct = CAREER.get(bp, {}).get("pct", 0)
                grade, breakdown = matchup_grade(k_diff, w, l, opp_pct, fish_player, bp)
                win_pct = breakdown["total"] * 10

                fish_sc = scouting_score(fish_player)
                opp_sc = scouting_score(bp)
                has_scout = "scouting" in st.session_state and (fish_player in st.session_state.scouting or bp in st.session_state.scouting)
                scout_str = f"{fish_sc - opp_sc:+.1f}" if has_scout else "—"

                fish_fit = course_fit_score(fish_player, "The Keep")
                opp_fit = course_fit_score(bp, "The Keep")
                fit_diff = fish_fit - opp_fit

                rows.append({
                    "Opponent": f"{bp} ({opp_idx})",
                    "Strokes": f"+{strokes_k}" if strokes_k > 0 else str(strokes_k),
                    "Scout": scout_str,
                    "H2H": f"{w}-{l}-{h}" if w + l + h > 0 else "—",
                    "Fit": f"{fit_diff:+.1f}",
                    "Opp Singles": singles_record(bp),
                    "Win%": f"{win_pct:.0f}%",
                    "Grade": grade,
                })

            df_matchups = pd.DataFrame(rows)

            def _highlight_assigned(row):
                is_assigned = row["Opponent"].startswith(choice)
                if is_assigned:
                    return ["background-color: #1a3a2a"] * len(row)
                return [""] * len(row)

            def _color_grade(val):
                if val == "A":
                    return "background-color: #d4edda; color: #155724"
                elif val == "B":
                    return "background-color: #cce5ff; color: #004085"
                elif val == "C":
                    return "background-color: #fff3cd; color: #856404"
                elif val == "D":
                    return "background-color: #f8d7da; color: #721c24"
                elif val == "F":
                    return "background-color: #dc3545; color: #ffffff"
                return ""

            styled = df_matchups.style.apply(_highlight_assigned, axis=1).map(_color_grade, subset=["Grade"])
            st.dataframe(styled, hide_index=True, use_container_width=True)

    st.session_state.singles_assignments = new_assignments

    st.divider()
    st.subheader("Matchup summary")

    summary_data = []
    for fp in fish_order:
        opp = new_assignments[fp]
        opp_idx = TEAM_BOOTH[opp]
        k_strokes = round(course_hcap(opp_idx, "The Keep") - course_hcap(TEAM_FISH[fp], "The Keep"))
        summary_data.append({"Match": f"{fp} vs {opp}", "Strokes": k_strokes})

    df_summary = pd.DataFrame(summary_data)
    st.bar_chart(df_summary.set_index("Match"))

    total_k = sum(d["Strokes"] for d in summary_data)
    c1, c2 = st.columns(2)
    c1.metric("Total stroke edge (The Keep)", f"+{total_k}" if total_k > 0 else str(total_k))
    favorable = sum(1 for d in summary_data if d["Strokes"] > 0)
    c2.metric("Favorable matchups", f"{favorable}/8")


# ── TAB 2: BEST BALL ──────────────────────────────────────────────────────────

with tab2:
    st.header("Best ball partner finder")
    st.caption("Find the best Team Fish pairings. Each player's potential partners are graded on handicap spread, scouting complement, course fit, and BB history.")

    fish_sorted = sorted(TEAM_FISH.keys(), key=lambda n: TEAM_FISH[n])

    for fish_player in fish_sorted:
        fi = TEAM_FISH[fish_player]
        with st.expander(f"**{fish_player}** ({fi})"):
            partners = [p for p in fish_sorted if p != fish_player]

            rows = []
            for partner in partners:
                pi = TEAM_FISH[partner]
                grade, bd = bb_partner_grade(fish_player, partner)

                low_hcap = min(course_hcap(fi, "The Keep"), course_hcap(pi, "The Keep"))
                spread = abs(fi - pi)
                style = "Anchor+Floater" if spread > 8 else "Balanced"

                pair_w, pair_l = bb_pair_history(fish_player, partner)
                bb_rec = f"{pair_w}-{pair_l}" if pair_w + pair_l > 0 else "—"

                rows.append({
                    "Partner": f"{partner} ({pi})",
                    "Grade": grade,
                    "Total": bd["total"],
                    "Spread (30%)": bd["handicap_spread"],
                    "Scout (25%)": bd["scouting_comp"],
                    "Fit (25%)": bd["course_fit"],
                    "History (20%)": bd["bb_history"],
                    "BB Rec": bb_rec,
                    "Low Hcap": f"{low_hcap:.0f}",
                    "Style": style,
                })

            df_partners = pd.DataFrame(rows).sort_values("Total", ascending=False)

            def _color_bb_grade(val):
                if val == "A":
                    return "background-color: #d4edda; color: #155724"
                elif val == "B":
                    return "background-color: #cce5ff; color: #004085"
                elif val == "C":
                    return "background-color: #fff3cd; color: #856404"
                elif val == "D":
                    return "background-color: #f8d7da; color: #721c24"
                elif val == "F":
                    return "background-color: #dc3545; color: #ffffff"
                return ""

            styled = df_partners.style.map(_color_bb_grade, subset=["Grade"])
            st.dataframe(styled, hide_index=True, use_container_width=True)


# ── TAB 3: COURSE FIT ─────────────────────────────────────────────────────────

with tab3:
    st.header("Course fit — The Keep")

    cdata = COURSES["The Keep"]
    with st.container(border=True):
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Tees", cdata["tee"])
        c2.metric("Slope", cdata["slope"])
        c3.metric("Rating", cdata["rating"])
        c4.metric("Par", cdata["par"])
        c5.metric("Yardage", f"{cdata['yardage']:,}")
        st.caption(cdata["notes"])

    st.divider()
    st.subheader("Course fit grades")
    st.caption("Based on scouting ratings weighted by skills The Keep demands. Fill in the Scouting Report tab to see personalized grades.")

    for cname in COURSE_SKILL_WEIGHTS:
        weights = COURSE_SKILL_WEIGHTS[cname]
        top_skills = sorted(SCOUTING_CATEGORIES, key=lambda c: weights[c], reverse=True)
        key_skills = [s for s in top_skills if weights[s] >= 2]

        with st.container(border=True):
            st.markdown(f"**{cname}** — Key skills: {', '.join(f'{s} (x{weights[s]})' for s in key_skills)}")

            fit_rows = []
            all_players = {**TEAM_FISH, **TEAM_BOOTH}
            for name in sorted(all_players.keys()):
                team = "Fish" if name in TEAM_FISH else "Booth"
                score = course_fit_score(name, cname)
                grade = course_fit_grade(score)
                row = {"Player": name, "Team": team, "Fit Score": round(score, 1), "Grade": grade}
                ratings = st.session_state.get("scouting", {}).get(name, {})
                for s in SCOUTING_CATEGORIES:
                    row[s] = ratings.get(s, {}).get("rating", 3)
                fit_rows.append(row)

            df_fit = pd.DataFrame(fit_rows).sort_values("Fit Score", ascending=False)

            def _color_fit_grade(val):
                if val == "A":
                    return "background-color: #d4edda; color: #155724"
                elif val == "B":
                    return "background-color: #cce5ff; color: #004085"
                elif val == "C":
                    return "background-color: #fff3cd; color: #856404"
                elif val == "D":
                    return "background-color: #f8d7da; color: #721c24"
                elif val == "F":
                    return "background-color: #dc3545; color: #ffffff"
                return ""

            st.dataframe(
                df_fit.style.map(_color_fit_grade, subset=["Grade"]),
                hide_index=True,
                use_container_width=True,
                column_config={
                    "Fit Score": st.column_config.NumberColumn(format="%.1f"),
                },
            )

    st.divider()
    st.subheader("Course handicaps")

    rows = []
    all_players = {**TEAM_FISH, **TEAM_BOOTH}
    for name, idx in sorted(all_players.items(), key=lambda x: x[1]):
        k_hcap = course_hcap(idx, "The Keep")
        team = "Fish" if name in TEAM_FISH else "Booth"
        rows.append({
            "Player": name, "Team": team, "Index": idx,
            "The Keep": k_hcap,
        })

    df_course = pd.DataFrame(rows)
    st.dataframe(
        df_course,
        hide_index=True,
        column_config={
            "The Keep": st.column_config.NumberColumn(format="%.1f"),
        },
        use_container_width=True,
    )

    st.divider()
    st.subheader("Stroke matchup grid")
    st.caption("Strokes Team Fish player RECEIVES from each opponent (positive = advantage)")

    grid_rows = []
    for fp, fi in sorted(TEAM_FISH.items(), key=lambda x: x[1]):
        row = {"Fish Player": fp}
        for op, oi in sorted(TEAM_BOOTH.items(), key=lambda x: x[1]):
            diff = round(course_hcap(oi, "The Keep") - course_hcap(fi, "The Keep"))
            row[op] = diff
        grid_rows.append(row)

    df_grid = pd.DataFrame(grid_rows)
    st.dataframe(df_grid, hide_index=True, use_container_width=True)



# ── TAB 4: HISTORY ─────────────────────────────────────────────────────────────

with tab4:
    st.header("Historical records")

    st.subheader("Career stats (2026 field only)")
    career_rows = []
    for name in sorted({**TEAM_FISH, **TEAM_BOOTH}.keys()):
        c = CAREER.get(name, {})
        team = "Fish" if name in TEAM_FISH else "Booth"
        match_rec = c.get("match", "0-0-0")
        parts = match_rec.split("-")
        mw, ml = int(parts[0]), int(parts[1])
        match_pct = round(100 * mw / (mw + ml)) if (mw + ml) > 0 else 0
        career_rows.append({
            "Player": name, "Team": team,
            "Guyder Record": c.get("overall", "N/A"),
            "Match record": c.get("match", "N/A"),
            "Total pts": c.get("pts", 0),
            "Match W%": match_pct,
        })

    df_career = pd.DataFrame(career_rows).sort_values("Total pts", ascending=False)
    st.dataframe(
        df_career, hide_index=True, use_container_width=True,
        column_config={
            "Match W%": st.column_config.NumberColumn(format="%d%%"),
        },
    )

    st.divider()
    st.subheader("Head-to-head lookup")
    h2h_cols = st.columns(2)
    all_names = sorted({**TEAM_FISH, **TEAM_BOOTH}.keys())
    with h2h_cols[0]:
        p1 = st.selectbox("Player 1", all_names, index=all_names.index("Fish"))
    with h2h_cols[1]:
        p2 = st.selectbox("Player 2", [n for n in all_names if n != p1])

    w, l, h, details = get_h2h(p1, p2)
    if details:
        st.metric(f"{p1} vs {p2}", f"{w}-{l}-{h}")
        for d in details:
            st.text(f"  {d}")
    else:
        st.info(f"No recorded matches between {p1} and {p2}")

    st.divider()
    st.subheader("Full match log")
    year_filter = st.multiselect("Filter by year", sorted(set(m["year"] for m in MATCH_HISTORY), reverse=True))
    type_filter = st.segmented_control("Type", ["All", "BB", "Singles"], default="All", key="type_filter")
    player_filter = st.selectbox("Filter by player", ["All"] + sorted(all_names), key="player_hist")

    filtered = MATCH_HISTORY
    if year_filter:
        filtered = [m for m in filtered if m["year"] in year_filter]
    if type_filter != "All":
        filtered = [m for m in filtered if m["type"] == type_filter]
    if player_filter != "All":
        filtered = [m for m in filtered if player_filter in m["team_a"] or player_filter in m["team_b"]]

    log_rows = []
    for m in filtered:
        winner_team = m["team_a"] if m["winner"] == "a" else (m["team_b"] if m["winner"] == "b" else "Halved")
        log_rows.append({
            "Year": m["year"], "Event": m["event"], "Type": m["type"],
            "Course": m["course"],
            "Team A": m["team_a"], "Team B": m["team_b"],
            "Result": m["result"], "Winner": winner_team,
        })

    if log_rows:
        st.dataframe(pd.DataFrame(log_rows), hide_index=True, use_container_width=True)
    else:
        st.info("No matches found with current filters")


# ── TAB 5: SCOUTING REPORT ───────────────────────────────────────────────────

with tab5:
    st.header("Scouting report")
    st.caption(
        "Rate each player's game on a 1-5 scale and add free-form notes. "
        "Ratings feed into the matchup grade: higher-rated Fish players "
        "and lower-rated opponents shift the grade favorably."
    )

    save_col, status_col = st.columns([1, 4])
    with save_col:
        if st.button("💾 Save scouting data", type="primary", use_container_width=True):
            save_scouting_data(st.session_state.scouting)
            st.session_state._scout_saved = True
    with status_col:
        if st.session_state.get("_scout_saved"):
            st.success("Scouting data saved!", icon="✅")
            st.session_state._scout_saved = False

    team_sel = st.segmented_control("Team", ["Team Fish", "Team Booth"], default="Team Fish", key="scout_team")
    roster = TEAM_FISH if team_sel == "Team Fish" else TEAM_BOOTH

    for player in sorted(roster.keys()):
        if player not in st.session_state.scouting:
            st.session_state.scouting[player] = {c: {"rating": 3} for c in SCOUTING_CATEGORIES}
        else:
            for c in SCOUTING_CATEGORIES:
                if c not in st.session_state.scouting[player]:
                    st.session_state.scouting[player][c] = {"rating": 3}
        if "notes" not in st.session_state.scouting[player]:
            st.session_state.scouting[player]["notes"] = ""

        overall = CAREER.get(player, {}).get("match", "N/A")
        with st.expander(f"**{player}** ({roster[player]} index · {overall})", expanded=False):
            row1_cats = SCOUTING_CATEGORIES[:4]
            row2_cats = SCOUTING_CATEGORIES[4:]
            for row_cats in [row1_cats, row2_cats]:
                cols = st.columns(len(row_cats))
                for j, cat in enumerate(row_cats):
                    with cols[j]:
                        val = st.slider(
                            cat, 1, 5,
                            value=st.session_state.scouting[player][cat]["rating"],
                            key=f"scout_{player}_{cat}",
                        )
                        st.session_state.scouting[player][cat]["rating"] = val

            avg = sum(SCOUTING_WEIGHTS[c] * st.session_state.scouting[player][c]["rating"] for c in SCOUTING_CATEGORIES) / sum(SCOUTING_WEIGHTS[c] for c in SCOUTING_CATEGORIES)
            labels = {1: "Well Below Avg", 2: "Below Avg", 3: "Average", 4: "Above Avg", 5: "Elite"}
            bar_cols = st.columns([3, 1])
            with bar_cols[0]:
                st.progress(avg / 5, text=f"Composite: {avg:.1f} / 5")
            with bar_cols[1]:
                nearest = min(labels.keys(), key=lambda k: abs(k - avg))
                st.markdown(f"**{labels[nearest]}**")

            notes = st.text_area(
                "Scouting notes",
                value=st.session_state.scouting[player]["notes"],
                key=f"scout_notes_{player}",
                placeholder="e.g., Long off the tee but struggles with short game...",
                height=80,
            )
            st.session_state.scouting[player]["notes"] = notes

    st.divider()
    st.subheader("Scouting overview")

    overview_rows = []
    all_scouted = {**TEAM_FISH, **TEAM_BOOTH}
    for name in sorted(all_scouted.keys()):
        if name in st.session_state.scouting:
            s = st.session_state.scouting[name]
            row = {"Player": name, "Team": "Fish" if name in TEAM_FISH else "Booth"}
            for cat in SCOUTING_CATEGORIES:
                row[cat] = s.get(cat, {}).get("rating", 3)
            row["Composite"] = round(sum(SCOUTING_WEIGHTS[c] * row[c] for c in SCOUTING_CATEGORIES) / sum(SCOUTING_WEIGHTS[c] for c in SCOUTING_CATEGORIES), 1)
            row["Notes"] = s.get("notes", "")
            overview_rows.append(row)
        else:
            row = {"Player": name, "Team": "Fish" if name in TEAM_FISH else "Booth"}
            for cat in SCOUTING_CATEGORIES:
                row[cat] = 3
            row["Composite"] = 3.0
            row["Notes"] = ""
            overview_rows.append(row)

    df_scout = pd.DataFrame(overview_rows).sort_values("Composite", ascending=False)
    st.dataframe(df_scout, hide_index=True, use_container_width=True)


# ── TAB 6: MATCHUP MATRIX ────────────────────────────────────────────────────

with tab6:
    st.header("Matchup matrix")
    st.caption("Grade for each Team Fish player against every Team Booth opponent. Hover cells for score breakdown.")

    course_mm = st.segmented_control("Course", ["Highlands", "The Keep"], default="Highlands", key="matrix_course")

    fish_sorted = sorted(TEAM_FISH.keys(), key=lambda n: TEAM_FISH[n])
    booth_sorted = sorted(TEAM_BOOTH.keys(), key=lambda n: TEAM_BOOTH[n])

    matrix_rows = []
    for fp in fish_sorted:
        row = {"Fish Player": f"{fp} ({TEAM_FISH[fp]})"}
        for bp in booth_sorted:
            sa = course_hcap(TEAM_BOOTH[bp], course_mm) - course_hcap(TEAM_FISH[fp], course_mm)
            w, l, h, _ = get_h2h(fp, bp)
            opp_pct = CAREER.get(bp, {}).get("pct", 0)
            grade, bd = matchup_grade(sa, w, l, opp_pct, fp, bp)
            h2h = f"{w}-{l}-{h}" if w + l + h > 0 else "-"
            row[bp] = f"{grade} ({bd['total']})"
        matrix_rows.append(row)

    df_matrix = pd.DataFrame(matrix_rows)

    def color_grade(val):
        if isinstance(val, str):
            if val.startswith("A"):
                return "background-color: #d4edda; color: #155724"
            elif val.startswith("B"):
                return "background-color: #cce5ff; color: #004085"
            elif val.startswith("C"):
                return "background-color: #fff3cd; color: #856404"
            elif val.startswith("D"):
                return "background-color: #f8d7da; color: #721c24"
            elif val.startswith("F"):
                return "background-color: #dc3545; color: #ffffff"
        return ""

    st.dataframe(
        df_matrix.style.map(color_grade, subset=booth_sorted),
        hide_index=True,
        use_container_width=True,
        height=350,
    )

    st.divider()
    st.subheader("Detail view")
    st.caption("Select a Fish player to see full breakdown against all opponents.")

    detail_player = st.selectbox("Fish player", fish_sorted, key="matrix_detail")
    detail_rows = []
    for bp in booth_sorted:
        sa = course_hcap(TEAM_BOOTH[bp], course_mm) - course_hcap(TEAM_FISH[detail_player], course_mm)
        w, l, h, _ = get_h2h(detail_player, bp)
        opp_pct = CAREER.get(bp, {}).get("pct", 0)
        grade, bd = matchup_grade(sa, w, l, opp_pct, detail_player, bp)
        detail_rows.append({
            "Opponent": bp,
            "Grade": grade,
            "Total": bd["total"],
            "Historical (35%)": bd["historical"],
            "Scouting (25%)": bd["scouting"],
            "Course Fit (25%)": bd["course_fit"],
            "Handicap (15%)": bd["handicap"],
            "Strokes": f"{sa:+.1f}",
            "H2H": f"{w}-{l}-{h}" if w + l + h > 0 else "-",
            "Opp W%": f"{opp_pct:.0%}",
        })

    df_detail = pd.DataFrame(detail_rows)
    st.dataframe(
        df_detail.style.map(color_grade, subset=["Grade"]),
        hide_index=True,
        use_container_width=True,
    )

# ── TAB 7: H2H SINGLES ──────────────────────────────────────────────────────

with tab7:
    st.header("H2H Singles History")
    st.caption("All head-to-head singles match results for each player.")

    team_booth_col, team_fish_col = st.columns(2)

    with team_booth_col:
        st.subheader("Team Booth")
    with team_fish_col:
        st.subheader("Team Fish")

    def _singles_history(player):
        singles_matches = []
        for m in MATCH_HISTORY:
            if m["type"] != "Singles":
                continue
            if m["team_a"] == player:
                opponent = m["team_b"]
                if m["winner"] == "a":
                    result_str = f"W {m['result']}"
                elif m["winner"] == "b":
                    result_str = f"L {m['result']}"
                else:
                    result_str = "Halved"
                singles_matches.append({
                    "Opponent": opponent, "Result": result_str,
                    "Year": m["year"], "Event": m["event"], "Course": m["course"],
                })
            elif m["team_b"] == player:
                opponent = m["team_a"]
                if m["winner"] == "b":
                    result_str = f"W {m['result']}"
                elif m["winner"] == "a":
                    result_str = f"L {m['result']}"
                else:
                    result_str = "Halved"
                singles_matches.append({
                    "Opponent": opponent, "Result": result_str,
                    "Year": m["year"], "Event": m["event"], "Course": m["course"],
                })
        w = sum(1 for s in singles_matches if s["Result"].startswith("W"))
        l = sum(1 for s in singles_matches if s["Result"].startswith("L"))
        h = sum(1 for s in singles_matches if s["Result"].startswith("H"))
        return singles_matches, f"{w}-{l}-{h}"

    for booth_player in sorted(TEAM_BOOTH.keys(), key=lambda n: TEAM_BOOTH[n]):
        singles_matches, record = _singles_history(booth_player)
        with team_booth_col:
            with st.expander(f"**{booth_player}** ({TEAM_BOOTH[booth_player]}) — {record}", expanded=False):
                if singles_matches:
                    st.dataframe(pd.DataFrame(singles_matches), hide_index=True, use_container_width=True)
                else:
                    st.info("No singles match history.")

    for fish_player in sorted(TEAM_FISH.keys(), key=lambda n: TEAM_FISH[n]):
        singles_matches, record = _singles_history(fish_player)
        with team_fish_col:
            with st.expander(f"**{fish_player}** ({TEAM_FISH[fish_player]}) — {record}", expanded=False):
                if singles_matches:
                    st.dataframe(pd.DataFrame(singles_matches), hide_index=True, use_container_width=True)
                else:
                    st.info("No singles match history.")
