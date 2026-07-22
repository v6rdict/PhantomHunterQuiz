"""
Open http://127.0.0.1:5000 in a browser
"""
from flask import Flask, render_template_string, url_for, abort

app = Flask(__name__)

# ---------------------------------------------------------------------------
STORY = {
    "start": {
        "text": (
            "You wake in a clearing under a sky you don't recognize. "
            "Something is moving in the treeline, and it's getting closer."
        ),
        "image": "images/start.jpg",
        "choices": [
            ("Stand your ground and face it", "path_fight"),
            ("Slip away before it gets any closer", "path_flee"),
        ],
    },
    "path_fight": {
        "text": (
            "It isn't one shape — it's several, closing in from different "
            "angles. You have seconds to decide how you meet them."
        ),
        "image": "images/path_fight.jpg",
        "choices": [
            ("Charge in alone", "end_orion"),
            ("Call out for the others camped nearby", "end_ursa"),
        ],
    },
    "path_flee": {
        "text": (
            "You slip into the dark. The path splits ahead — one way "
            "vanishes into shadow, the other opens toward distant firelight."
        ),
        "image": "images/path_flee.jpg",
        "choices": [
            ("Map the safest route before moving", "end_draco"),
            ("Head straight for the fire and the people around it", "end_cass"),
        ],
    },
    # Endings have no "choices" key — instead they point at a RESULTS entry.
    "end_diffident": {"result": "diffident"},
    "end_strategic": {"result": "strategic"},
    "end_capricious": {"result": "capricious"},
    "end_affable": {"result": "affable"},
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
            "You paused to map the safest route, not out of fear, "
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
    font-size: 26px;
    line-height: 1.4;
    margin: 0 0 6px 0;
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
  <p class="eyebrow">What do you do?</p>
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
    return render_template_string(INTRO_HTML, css=BASE_CSS)


@app.route("/story/<node_id>")
def story(node_id):
    node = STORY.get(node_id)
    if node is None:
        abort(404)

    if "result" in node:
        return render_template_string(
            ENDING_HTML, css=BASE_CSS, result=RESULTS[node["result"]]
        )

    return render_template_string(PASSAGE_HTML, css=BASE_CSS, node=node)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
