"""
Open http://127.0.0.1:5000 in a browser
"""
import random
from flask import Flask, render_template_string, url_for, abort, session, request, redirect
 
app = Flask(__name__)
app.secret_key = "123"

# ---------------------------------------------------------------------------
STORY = {
    "start": {
        "text": (
            "You wake up to a bright light shining through the window.\n "
            "As you blinked away the sleep from your eyes, you realise you've been shipwrecked on an island. "
        ),
        "image": "images/start.jpg",
        "choices": [
            ("Get up", "pg2", "neutral"),
        ],
    },
    "pg2": {
        "text": (
            "You get up, and slowly make your way out of your cabin and off the ship.\n "
            "There's a path up towards a huge mansion, and you decide, apprehensively, to walk towards it. "
        ),
        "image": "images/pg2.jpg",
        "choices": [
            ("Walk up", "pg3", "neutral"),
        ],
    },
    "pg3": {
        "text": (
            "On the way, you see a doll on the ground. "
        ),
        "image": "images/pg3.jpg",
        "choices": [
            ("Ignore it and continue on", "pg4", "neutral"),
        ],
    },
    "pg4": {
        "text": (
            "The doll suddenly gets up and screams at you, causing you to: "
        ),
        "image": "images/pg4.jpg",
        "choices": [
            ("Scream and run away", "path_t", "diffident"),
            ("Stare blankly at it", "path_s", "strategic"),
            ("Kick it away", "path_i", "capricious"),
            ("'Hey... Since when could dolls talk??'", "path_a", "affable"),
        ],
    },
    "path_t": {
        "text": (
            "As you make a mad dash away from the doll, you see it slowly floating away into the mansion.\n "
            "You keep running but eventually stop when you've exhausted all your energy.\n "
            "It's only when you stopped you realised that you haven't moved from your original spot at all. "
        ),
        "image": "images/run.jpg",
        "choices": [
            ("Keep trying to make your way back to the cabin", "path_loop", "diffident"),
            ("Continue up the path", "path_mansion", "capricious"),
        ],
    },
    "path_loop": {
        "text": (
            "You try to head back, but it feels like an endless loop- "
            "the path back never shortens. "
        ),
        "image": "images/path_loop.jpg",
        "choices": [
            ("Keep trying to make your way back to the cabin", "path_loop", "diffident"),
            ("Continue up the path", "path_mansion", "diffident"),
        ],
    },
    "path_mansion": {
        "text": (
            "It dawned on you that you had no other choice but to walk towards the mansion to seek answers "
            "from that doll, so you sighed and resigned yourself to whatever fate had in store... "
        ),
        "image": "images/path_mansion.jpg",
        "choices": [
            ("Chase after the doll and enter the mansion", "path_inMansion", "neutral"),
        ],
    },
    "path_s": {
        "text": (
            "As you stared blankly at the doll, weighing your options, it stared back- but only for a split second, "
            "before it floated away towards the mansion at an unfathomable speed, leaving you pondering. "
        ),
        "image": "images/dollaway.jpg",
        "choices": [
            ("Chase after the doll and enter the mansion", "path_inMansion", "strategic"),
            ("Go back", "path_loop", "strategic")
        ],
    },
    
    "path_i": {
        "text": (
            "THWAK! You kicked the doll with full force instinctively.\n"
            " 'WHY WOULD YOU DO THAT??!' "
            "You looked around in search of the voice, but all you saw was the doll floating away hastily. "
        ),
        "image": "images/dollaway.jpg",
        "choices": [
            ("Chase after the doll and enter the mansion", "path_inMansion", "capricious"),
            ("Go back", "path_loop", "strategic")
        ],
    },

    "path_a": {
        "text": (
            "'Ugh, people are so unimaginative.. I can fly too, you know!' and before you knew it, she had "
            "flown away into the mansion. "
        ),
        "image": "images/dollFly.jpg",
        "choices": [
            ("Chase after the doll and enter the mansion", "path_inMansion", "affable"),
            ("Go back", "path_loop", "diffident")
        ],
    },

    "path_inMansion": {
        "text": (
            "The moment you entered the mansion, a cold gust of wind blew by, sending chills down your spine.\n "
            "You look around and spot some newspapers left on a table."
        ),
        "image": "images/papers.jpg",
        "choices": [
            ("Read the papers", "path_papers", "neutral"),
        ],
    },
    
    "path_papers": {
        "text": (
            "You pick up the papers and read the headlines of the first one.\n "
            "'I haven't seen those in a while.' You turn around and saw the doll again.\n\n 'You should leave. "
            "My father doesn't take kindly to strangers.' \n At that, you start to question her but she "
            "once again leaves before you could say anything. "
        ),
        "image": "images/papers.jpg",
        "choices": [
            ("Follow her", "path_follow", "neutral"),
        ],
    },

    "path_follow": {
        "text": (
            "The doll went down the stairs into a nearby room, with you tailing behind. \n "
            "You look around the room, but there was no sign of the doll anymore. "
        ),
        "image": "images/room.jpg",
        "choices": [
            ("Keep going", "cont", "neutral"),
        ],
    },

    "cont": {
        "text": (
            "Eventually, you spot her near the end next to a chest that had been sealed away. \n "
            "There appeared to have been attempts at opening it, but clearly to no avail. \n"
            "Strange strangled sounds started coming from the doll, almost like crying, and you:"
        ),
        "image": "images/dollChestroom.jpg",
        "choices": [
            ("Carefully approach her with the aim of finding out more.", "path_approach", "strategic"),
            ("Sit by her to offer her some comfort.", "path_comfort", "affable"),
            ("Slowly walk away.", "path_walkAway", "diffident"),
            ("Ask her what she's up to.", "path_ask", "capricious"),
        ],
    },
    
    
    "path_walkAway": {
        "text": (
            "You try to walk away, but you somehow trip and fall flat on your face. \n"
            "The doll realises your presence, and the strangled sounds ceased. \n "
            "'You can leave now, you know. I told them to stop their silly tricks.' "
        ),
        "image": "images/dollDialogue.jpg",
        "choices": [
            ("Them?", "path_who", "capricious"),
            ("'I see.. are you.. okay though?'", "path_comfort", "affable"),
            ("Run away and leave.", "path_leave", "diffident"),
        ],
    },

    "path_approach": {
        "text": (
            "The doll realises your presence, and the strangled sounds ceased. \n "
            "'You can leave now, you know. I told them to stop their silly tricks.' "
        ),
        "image": "images/dollDialogue.jpg",
        "choices": [
            ("Them?", "path_who", "strategic"),
            ("'What're you doing down here?'", "path_ask", "capricious"),
            ("'I see... are you okay though?'", "path_comfort", "affable"),
            ("Run away and leave.","path_leave", "diffident"),
        ],
    },

    "path_ask": {
        "text": (
            "'What?' she says, startled. \n"
            "'I'm... nothing. You should leave. I was being serious about my father.' she continues, her mind seemingly somewhere else. \n"
        ),
        "image": "images/dollDialogue.jpg",
        "choices": [
            ("Leave", "path_leave", "strategic"),
            ("Stay", "path_stay", "capricious"),
        ],
    },
    
    "path_comfort": {
        "text": (
            "'What?' she says, confused. \n"
            "'Are you okay? You seem rather upset...' you said slowly. \n"
            "She falls silent for a while, and you started to wonder if she had gone back to being inanimate,"
            "when she finally spoke again. 'I'm fine, but you won't be if my father catches you. Please, "
            "just leave, as fast as you can.'"
        ),
        "image": "images/dollDialogue.jpg",
        "choices": [
            ("Leave", "path_leave", "strategic"),
            ("Stay", "path_stay", "capricious"),
        ],
    },

    "path_who": {
        "text": (
            "'The... phantoms were keeping you in a loop on that path.\n"
            "I've told them to stop, so you can leave now. They just like"
            "to have a bit of fun with newcomers on the island.' "
        ),
        "image": "images/dollDialogue.jpg",
        "choices": [
            ("'I see,' you say, unsure of what to do next", "path_stay", "neutral"),
            ("'I see,' you say, then turn to leave. You felt it unwise to stay any longer.", "path_leave", "strategic"),
            ("'I see... are you okay though?'", "path_comfort", "affable"),
        ],
    },

    "path_leave": {
        "text": (
            "You take your leave, and start making your way back to the ship.\n"
            "As you walked, you thought about the doll and the possible secrets hidden in the mansion, "
            " but still believed leaving was the right thing to do."
        ),
        "image": "images/leaving.jpg",
        "choices": [
            ("Continue", "leave_2", "neutral"),
        ],
    },

    "leave_2": {
        "text": (
            "Once you were back to the ship, you called for help and was soon rescued from the island.\n"
        ),
        "image": "images/help.jpg",
        "choices": [
            ("Go home", "leave_3", "neutral"),
        ],
    },
    
    "leave_3": {
        "text": (
            "Back home, life started going back to normal.\n "
            "Bzzt...\n Your phone buzzes in your pocket."
        ),
        "image": "images/normallife.jpg",
        "choices": [
            ("Check your phone", "phone", "neutral"),
        ],
    },

    "phone": {
        "text": (
            " "
        ),
        "image": "images/wewantyouPhone.jpg",
        "choices": [
            ("...", "end", "neutral"),
        ],
    },

    "path_stay": {
        "text": (
            "The doll waits for you to leave. \n"
            "When you don't, she scoffs and says 'Suit yourself.' and leaves."
            "You then take a closer look at the chest. It seems like it's already been unlocked- perhaps "
            "she was simply too small to open it."
        ),
        "image": "images/dollDialogue.jpg",
        "choices": [
            ("Open the chest.", "path_chest", "neutral"),
            ("Forget about it and leave", "path_leave", "strategist"),
        ],
    },

    "path_chest": {
        "text": (
            "You open the chest and peer inside. \n"
        ),
        "image": "images/chestOpen.jpg",
        "choices": [
            ("Pick up and inspect it", "path_inspect", "neutral"),
            ("Forget about it and leave", "path_leave", "strategist"),
        ],
    },

    "path_inspect": {
        "text": (
            "You inspect the item, and realise there were some papers and blueprints underneath it. \n"
            "You read the papers and find out that it was a healing tool... but why was it hidden away here? \n"
            "Just then, you hear a muffled voice behind you: \n "
            "'I see you've found my H.A.T.'"
        ),
        "image": "images/HAT.jpg",
        "choices": [
            ("'Your hat??'", "path_hat", "capricious"),
        ],
    },

    "path_hat": {
        "text": (
            "'Not hat, H.A.T.!' \n"
            "You stood there, confused by the octogenarian's strange presence. There was something off "
            "about him. \n "
            "'Whatever. It doesn't matter. You're coming with me.' He reaches out to grab you, but:"
        ),
        "image": "images/weirdguy.jpg",
        "choices": [
            ("You punch him square in the face and run off.", "path_preLeave", "capricious"),
            ("You aim the H.A.T. at him", "path_aim", "strategist"),
            ("Try to talk to him", "path_talk", "affable"),
        ],
    },

    "path_aim": {
        "text": (
            "You aim the H.A.T at the man, and he freezes and raises his arms above his head- \n"
            "'Be careful with that!' He shouts, and you: "
        ),
        "image": "images/weirdguy.jpg",
        "choices": [
            ("Pull the trigger", "path_preLeave", "capricious"),
            ("'Why?'", "path_talk", "affable"),
        ],
    },

    "path_talk": {
        "text": (
            "You start to talk, but before you could finish, he disarms you. \n"
            "'This is very important to me,' he explains, but you found yourself starting to feel lightheaded. \n "
            "The man continued speaking, but you could no longer focus on his words... \n"
            "Eventually, you found yourself on the ground, spots swimming before your eyes."
        ),
        "image": "images/blackout.jpg",
        "choices": [
            ("...", "path_black", "neutral"),
        ],
    },

    "path_black": {
        "text": (
            "'I did tell you to leave.' A familiar voice could be heard, but you still didn't have the strength to move. \n"
            "'That was my father. The one in the papers you read about.' It was the doll from before. \n "
            "'He had been depressed after my mother passed before we could use the H.A.T. on her, but I think my death was "
            "what pushed him over the edge.. to think that he would turn to necromancy.."
        ),
        "image": "images/dollLore.jpg",
        "choices": [
            ("...", "path_black2", "neutral"),
        ],
    },

    "path_black2": {
        "text": (
            "'I did tell you to leave.' A familiar voice could be heard, but you still didn't have the strength to move. \n"
            "'That was my father. The one in the papers you read about.' It was the doll from before. \n "
            "'He had been depressed after my mother passed before we could use the H.A.T. on her, but I think my death was "
            "what pushed him over the edge.. to think that he would turn to necromancy.."
        ),
        "image": "images/dollLore.jpg",
        "choices": [
            ("...", "path_black2", "neutral"),
        ],
    },

    "path_preLeave": {
        "text": (
            "You speed away up the stairs and out of the mansion, your breath catching \n"
            "but you not caring, continuing to run all the way down the path back to the ship. \n"
        ),
        "image": "images/dollDialogue.jpg",
        "choices": [
            ("Call for help", "leave_2", "strategist"),
        ],
    },


    "end": {},
}

RESULTS = {
    "diffident": {
        "name": "Diffident",
        "title": "The Timid",
        "blurb": (
            "You lack the self confidence to face up to uncertainty,  "
            "so you run from any situation without a guaranteed outcome. "
            "Some call it strategic, others, cowardice. \n"
            "You work best with someone affable. "
        ),
    },
    "strategic": {
        "name": "Strategist",
        "title": "The Calculated",
        "blurb": (
            "You pause to map the safest route, not out of fear, "
            "but to make sure you're making the best choices you can. \n "
            "You work best with someone capricous. "
        ),
    },
    "capricious": {
        "name": "Capricious",
        "title": "The Instinctive",
        "blurb": (
            "Your trust in your instincts are steadfast, so "
            "you like to dive in headfirst no matter the situation. \n "
            "You work best with someone strategic. "
        ),
    },
    "affable": {
        "name": "Affable",
        "title": "The Amiable",
        "blurb": (
            "You may not always know what is the right thing to do, "
            "but you always try your best not to assume the worst and "
            "be a source of kindness. \n "
            "You work best with someone diffident. "
        ),
    },
}

BASE_CSS = """
:root {
    --bg: #0b1224;
    --bg-soft: #121a33;
    --line: #253158;
    --gold: #23E628;
    --text: #eef1fb;
    --text-dim: #9aa3c7;
}
* { box-sizing: border-box; }
body {
    margin: 0;
    min-height: 100vh;
    background: radial-gradient(ellipse at top, #16204a 0%, var(--bg) 60%);
    color: var(--text);
    font-family: 'Georgia', 'Iowan Old Style', serif;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 24px;
}
.card {
    width: 100%;
    max-width: 560px;
    background: var(--bg-soft);
    border: 1px solid var(--line);
    border-radius: 18px;
    padding: 40px 36px;
    position: relative;
    overflow: hidden;
}
.card::before {
    content: "";
    position: absolute;
    inset: 0;
    background-image:
        radial-gradient(1px 1px at 20px 30px, #ffffff55 0%, transparent 60%),
        radial-gradient(1px 1px at 120px 80px, #ffffff33 0%, transparent 60%),
        radial-gradient(1.5px 1.5px at 200px 20px, #ffffff44 0%, transparent 60%),
        radial-gradient(1px 1px at 300px 120px, #ffffff33 0%, transparent 60%),
        radial-gradient(1px 1px at 40px 160px, #ffffff44 0%, transparent 60%),
        radial-gradient(1.5px 1.5px at 420px 60px, #ffffff33 0%, transparent 60%);
    pointer-events: none;
}
.eyebrow {
    font-family: 'Helvetica Neue', Arial, sans-serif;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    font-size: 12px;
    color: var(--gold);
    margin: 0 0 10px 0;
}
h1 {
    font-size: 21px;
    line-height: 1.4;
    margin: 0 0 6px 0;
    white-space: pre-line;
}
p.sub {
    color: var(--text-dim);
    font-family: 'Helvetica Neue', Arial, sans-serif;
    font-size: 14px;
    margin: 0 0 28px 0;
}
.question-image {
    width: 100%;
    height: 220px;
    object-fit: cover;
    border-radius: 12px;
    border: 1px solid var(--line);
    margin-bottom: 22px;
    display: block;
}
.choices { display: flex; flex-direction: column; gap: 12px; margin-top: 24px; }
a.option, button.option {
    text-align: left;
    background: #0e1630;
    border: 1px solid var(--line);
    color: var(--text);
    padding: 16px 18px;
    border-radius: 12px;
    font-family: 'Helvetica Neue', Arial, sans-serif;
    font-size: 15px;
    cursor: pointer;
    text-decoration: none;
    display: block;
    transition: border-color 0.15s ease, background 0.15s ease;
}
a.option:hover, button.option:hover { border-color: var(--gold); background: #131c3c; }
a.start-btn {
    display: inline-block;
    margin-top: 8px;
    background: var(--gold);
    color: #1a1204;
    font-family: 'Helvetica Neue', Arial, sans-serif;
    font-weight: 700;
    text-decoration: none;
    padding: 14px 22px;
    border-radius: 10px;
    text-align: center;
    font-size: 15px;
}
.result-name {
    font-size: 34px;
    color: var(--gold);
    margin: 4px 0 2px 0;
}
.result-title {
    font-family: 'Helvetica Neue', Arial, sans-serif;
    color: var(--text-dim);
    letter-spacing: 0.08em;
    text-transform: uppercase;
    font-size: 13px;
    margin-bottom: 20px;
}
.blurb { line-height: 1.6; font-size: 16px; }
"""

INTRO_HTML = """
<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>What kind of Phantom Hunter are you?</title><style>{{ css }}</style></head>
<body><div class="card">
  <p class="eyebrow">A choose-your-own-adventure story.</p>
  <h1>What kind of Phantom Hunter are you?</h1>
  <p class="sub">Every choice leads somewhere different. There's no wrong answer, just be honest.</p>
  <a class="start-btn" href="{{ url_for('story', node_id='start') }}">Begin</a>
</div></body></html>
"""

PASSAGE_HTML = """
<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Your story</title><style>{{ css }}</style></head>
<body><div class="card">
  <p class="eyebrow"></p>
  {% if node.image %}
    <img class="question-image" src="{{ url_for('static', filename=node.image) }}" alt="">
  {% endif %}
  <h1>{{ node.text }}</h1>
  <div class="choices">
    {% for label, next_node, tag in node.choices %}
      <a class="option" href="{{ url_for('story', node_id=next_node, tag=tag) }}">{{ label }}</a>
    {% endfor %}
  </div>
</div></body></html>
"""

ENDING_HTML = """
<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Your result: {{ result.name }}</title><style>{{ css }}</style></head>
<body><div class="card">
  <p class="eyebrow">Your story ends here. You are: </p>
  <div class="result-name">{{ result.name }}</div>
  <div class="result-title">{{ result.title }}</div>
  <p class="blurb">{{ result.blurb }}</p>
  <a class="start-btn" href="{{ url_for('intro') }}">Start over</a>
</div></body></html>
"""

 
@app.route("/")
def intro():
    session.clear()  
    return render_template_string(INTRO_HTML, css=BASE_CSS)
 
 
@app.route("/story/<node_id>")
def story(node_id):
    node = STORY.get(node_id)
    if node is None:
        abort(404)
 
    tag = request.args.get("tag")
    if tag:
        tags = session.get("tags", [])
        tags.append(tag)
        session["tags"] = tags
 
    if not node.get("choices"):
        tags = session.get("tags", [])
        if not tags:
            return redirect(url_for("intro"))
        
        counts = {}
        for t in tags:
            if t == "neutral":
                continue
            counts[t] = counts.get(t, 0) + 1
        top_score = max(counts.values())
        winners = [t for t, n in counts.items() if n == top_score]
        winner = random.choice(winners)  
        return render_template_string(
            ENDING_HTML, css=BASE_CSS, result=RESULTS[winner]
        )
 
    return render_template_string(PASSAGE_HTML, css=BASE_CSS, node=node)
 
 
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)