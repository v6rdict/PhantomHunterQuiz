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
            "You wake up bright and early to the sunlight shining through your window.\n "
            "As you blinked away the sleep from your eyes, you: "
        ),
        "image": "images/start.jpg",
        "choices": [
            ("Check your phone first. ", "path_d", "diffident"),
            ("Get up and immediately start your day. ", "path_s", "strategic"),
            ("Sit up in bed and enjoy the warm sunshine. ", "path_a", "affable"),
            ("Go back to sleep. ", "path_c", "capricious"),
        ],
    },

    "path_d": {
        "text": (
            "You check your phone. There are no new notifications related to work/school, so you decide: "
        ),
        "image": "images/checkphone.jpg",
        "choices": [
            ("To start your day. ", "path_s", "strategic"),
            ("To sit up in bed and enjoy the warm sunshine. ", "path_a", "affable"),
            ("To go back to sleep. ", "path_c", "diffident"),
        ],
    },

    "path_s": {
        "text": (
            "As you make your way through your morning tasks, you think about what to do today. \n "
            "It's the weekend, so you: "
        ),
        "image": "images/startday.jpg",
        "choices": [
            ("Stay at home and work on your hobbies. ", "path_hobby", "diffident"),
            ("Get some work done first before you enjoy the weekend. ", "path_sure", "strategic"),
            ("Call up some friends for a get together. ", "path_friends", "affable"),
            ("Get out of the house to do something. ", "path_go", "capricious"),
        ],
    },

    "path_a": {
        "text": (
            "After a short while of enjoying the sunshine, you think: "
        ),
        "image": "images/start.jpg",
        "choices": [
            ("You want to stay home to work on your hobbies.", "path_hobby", "diffident"),
            ("You should probably just get up and start your day.", "path_s", "strategic"),
            ("You feel like reaching out to some friends for a get together.", "path_friends", "affable"),
            ("You need to get out of the house and do something.", "path_go", "capricious"),
        ],
    },

    "path_c": {
        "text": (
            "You go back to sleep but eventually wake up in the afternoon. "
            "It's the weekend, so you: "
        ),
        "image": "images/afterwake.jpg",
        "choices": [
            ("Stay at home and work on your hobbies. ", "path_hobby", "diffident"),
            ("Get some work done. ", "path_sure", "strategic"),
            ("Call up some friends for a get together. ", "path_friends", "affable"),
            ("Get out of the house to do something. ", "path_go", "capricious"),
        ],
    },

    "path_hobby": {
        "text": (
            "What would you like to do? "
        ),
        "choices": [
            ("Reading ", "cnext", "neutral"),
            ("Crafting ", "cnext", "diffident"),
            ("Programming ", "cnext", "strategic"),
            ("Puzzles ", "cnext", "strategic"),
            ("Music", "cnext", "capricious"),
            ("Others", "cnext", "neutral"),

        ],
    },

    "cnext": {
        "text": (
            "While you carry out your activities, the end of the day approaches. "
        ),
        "choices": [
            ("Start cleaning up your home before preparing for bed and ending your day. ", "end", "strategic"),
            ("You think that you rather enjoyed your day, and start preparing for bed. ", "end", "affable"),
            ("You clean your house thoroughly before carefully carrying out your bedtime routine. ", "end", "diffident"),
            ("Stay up and continue before giving in to exhaustion and going to bed. ", "end", "capricious"),
        ],
    },

    "path_friends": {
        "text": (
            "You reach out to some friends and organised a spontaneous get together at your home. "
            "How will you be hosting?: "
        ),
        "choices": [
            ("Clean up your home while thinking of some activities for later. ", "pres_end", "strategic"),
            ("Simply take care of some messes in your home and focus on planning out the activities for later. ", "prea_end", "affable"),
        ],
    },

    "path_sure": {
        "text": (
            "You get started on your work after lunch, and day dissolves into night. \n"
            "When you realised it was almost dark out, you: "
        ),
        "choices": [
            ("Have dinner and start winding down for the end of your day. ", "end", "strategic"),
            ("Decide to stay up and continue before giving in to exhaustion and going to bed. ", "end", "capricious"),
        ],
    },

    "path_go": {
        "text": (
            "You head out without a plan. "
            "What will you do? "
        ),
        "choices": [
            ("Get on the next bus and see where it takes you. ", "prec_end", "capricious"),
            ("Take a short walk before heading back. ", "preago_end", "affable"),
        ],
    },

    "preago_end": {
        "text": (
            "You walk around your neighbourhood at a leisurely pace, taking in the fresh air. \n "
            "After a short while, you start heading home. "
        ),
        "choices": [
            ("You think that you rather enjoyed your day, and start preparing for bed. ", "end", "affable"),
            ("You clean your house thoroughly before carefully carrying out your bedtime routine. ", "end", "diffident"),
            ("You stay up to look at social media before giving in to exhaustion and going to bed. ", "end", "capricious"),
        ],
    },

    "prec_end": {
        "text": (
            "You get on the next bus and manage to get a seat. \n "
            "Eventually, you get off somewhere unfamiliar to you, and start exploring until "
            "it was starting to get dark, at which you decided to head back home. Once home:"
        ),
        "choices": [
            ("You think that you rather enjoyed your day, and start preparing for bed. ", "end", "affable"),
            ("You clean your house thoroughly before carefully carrying out your bedtime routine. ", "end", "diffident"),
            ("You stay up to look at social media before giving in to exhaustion and going to bed. ", "end", "capricious"),
        ],
    },

    "pres_end": {
        "text": (
            "You have fun hanging out with your friends, and it is soon time for them to head home. \n "
            "You say your goodbyes, then:"
        ),
        "choices": [
            ("Start cleaning up your home before preparing for bed and ending your day. ", "end", "strategic"),
            ("Think that you rather enjoyed your day, and start preparing for bed. ", "end", "affable"),
            ("Clean your house thoroughly before carefully carrying out your bedtime routine. ", "end", "diffident"),
            ("Stay up to look at social media before giving in to exhaustion and going to bed. ", "end", "capricious"),
        ],
    },

    "prea_end": {
        "text": (
            "You have fun hanging out with your friends, and it is soon time for them to head home. \n "
            "You say your goodbyes, then:"
        ),
        "choices": [
            ("Start cleaning up your home before preparing for bed and ending your day. ", "end", "strategic"),
            ("Think that you rather enjoyed your day, and start preparing for bed. ", "end", "affable"),
            ("Clean your house thoroughly before carefully carrying out your bedtime routine. ", "end", "diffident"),
            ("Stay up to look at social media before giving in to exhaustion and going to bed. ", "end", "capricious"),
        ],
    },



    "end": {},
}

RESULTS = {
    "diffident": {
        "name": "Completer",
        "title": "The Detail-Oriented",
        "blurb": (
            "You lack the self confidence to face up to uncertainty,  "
            "so you feel the need to have to check through things thoroughly when faced with any task at hand. \n"
            "You work best with a coordinator, who can help guide you through your reservations. "
        ),
    },
    "strategic": {
        "name": "Streamliner",
        "title": "The Pragmatic",
        "blurb": (
            "You like to think things through and make sure that you're making the most efficient choices you can to reach your goals. \n "
            "You work best with a implementer, who can follow your strategic mind. "
        ),
    },
    "capricious": {
        "name": "Implementer",
        "title": "The Action-Oriented",
        "blurb": (
            "You like to keep things simple and do whatever you feel like doing to keep busy. \n "
            "You work best with someone pragmatic, whose strategic mind can help guide you. "
        ),
    },
    "affable": {
        "name": "Coordinator",
        "title": "The People-Oriented",
        "blurb": (
            "You like to go through life with a postive mindset and take things in stride, making you ideal for social settings. \n "
            "You work best with someone detail oriented, who responds well to your positive outlook. "
        ),
    },
}

BASE_CSS = """
:root {
    --bg: #0b1224;
    --bg-soft: #121a33;
    --line: #253158;
    --gold: #FFE169;
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
<title>What Role Do You Play In A Team?</title><style>{{ css }}</style></head>
<body><div class="card">
  <p class="eyebrow">A choose-your-own-adventure quiz.</p>
  <h1>What Kind Of Team Player Are You?</h1>
  <p class="sub">There's no wrong answer, just be honest. </p>
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
  <p class="eyebrow">Your story ends here. You are the: </p>
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