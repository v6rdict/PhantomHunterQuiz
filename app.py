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
            ("Get up", "pg2"),
        ],
    },
    "pg2": {
        "text": (
            "You get up, and slowly make your way out of your cabin and off the ship.\n "
            "There's a path up towards a huge mansion, and you decide, apprehensively, to walk towards it. "
        ),
        "image": "images/pg2.jpg",
        "choices": [
            ("Walk up", "pg3"),
        ],
    },
    "pg3": {
        "text": (
            "On the way, you see a doll on the ground. "
        ),
        "image": "images/pg3.jpg",
        "choices": [
            ("Ignore it and continue on", "pg4"),
        ],
    },
    "pg4": {
        "text": (
            "The doll suddenly gets up and screams at you, causing you to: "
        ),
        "image": "images/pg4.jpg",
        "choices": [
            ("Scream and run away", "path_t", "timid"),
            ("Stare blankly at it", "path_s", "strategic"),
            ("Kick it away", "path_i", "instinct"),
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
            ("Keep trying to make your way back to the cabin", "path_loop", "timid"),
            ("Continue up the path", "path_mansion", "instinct"),
        ],
    },
    "path_loop": {
        "text": (
            "You try to head back, but it feels like an endless loop- "
            "the path back never shortens. "
        ),
        "image": "images/path_loop.jpg",
        "choices": [
            ("Keep trying to make your way back to the cabin", "path_loop", "timid"),
            ("Continue up the path", "path_mansion"),
        ],
    },
    "path_mansion": {
        "text": (
            "It dawned on you that you had no other choice but to walk towards the mansion to seek answers "
            "from that doll, so you sighed and resigned yourself to whatever fate had in store... "
        ),
        "image": "images/path_mansion.jpg",
        "choices": [
            ("Chase after the doll and enter the mansion", "path_inMansion"),
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
            ("Chase after the doll and enter the mansion", "path_inMansion", "instinct"),
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
            ("Go back", "path_loop", "timid")
        ],
    },

    "path_inMansion": {
        "text": (
            "The moment you entered the mansion, a cold gust of wind blew by, sending chills down your spine.\n "
            "You look around and spot some newspapers left on a table."
        ),
        "image": "images/papers.jpg",
        "choices": [
            ("Read the papers", "path_papers",),
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
            ("Follow her", "path_follow"),
        ],
    },

    "path_follow": {
        "text": (
            "The doll went down the stairs into a nearby room, with you tailing behind. \n "
            "You look around the room, but there was no sign of the doll anymore. "
        ),
        "image": "images/room.jpg",
        "choices": [
            ("Keep going", "cont"),
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
            ("Slowly walk away.", "path_walkAway", "timid"),
            ("Ask her what she's up to.", "path_ask", "instinct"),
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
            ("'What're you doing down here?", "path_ask", "instinct"),
            ("'I see... are you okay though?'","path_comfort", "affable")
            ("Run away.","path_run", "timid")
        ],
    },

    "path_comfort": {
        "text": (
            "'What?' she says, confused. \n"
            "'Are you okay? You seem rather upset...' you said slowly. \n"
            "She falls silent for a while, and you started to wonder if she had gone back to being inanimate,"
            "when she finally spoke again. 'I'm fine, but you won't be if my father catches you. Please"
            "just leave, as fast as you can.'"
        ),
        "image": "images/dollDialogue.jpg",
        "choices": [
            ("Leave", "path_leave", "strategic"),
            ("Stay", "path_leave", "affable"),
        ],
    },

    "path_comfort": {
        "text": (
            "'What?' she says, confused. \n"
            "'Are you okay? You seem rather upset...' you said slowly. \n"
            "She falls silent for a while, and you start to wonder if "
        ),
        "image": "images/dollDialogue.jpg",
        "choices": [
            ("Them?", "cont"),
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
            "Some call it strategic, others, cowardice."
            "You work best with someone affable. "
        ),
    },
    "strategic": {
        "name": "Strategist",
        "title": "The Calculated",
        "blurb": (
            "You pause to map the safest route, not out of fear, "
            "but to make sure you're making the best choices you can. "
            "You work best with someone capricous. "
        ),
    },
    "capricious": {
        "name": "Capricious",
        "title": "The Instinctive",
        "blurb": (
            "Your trust in your instincts are steadfast, so "
            "you like to dive in headfirst no matter the situation. "
            "You work best with someone strategic. "
        ),
    },
    "affable": {
        "name": "Affable",
        "title": "The Amiable",
        "blurb": (
            "You may not always know what is the right thing to do, "
            "but you always try your best not to assume the worst and "
            "be a source of kindness. "
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
    {% for label, next_node in node.choices %}
      <a class="option" href="{{ url_for('story', node_id=next_node) }}">{{ label }}</a>
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