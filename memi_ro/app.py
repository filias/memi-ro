"""Memi Romania - practise your memory of Romania."""

from memi_engine import MemiConfig, create_app

# Import providers to register them
import memi_ro.providers  # noqa: F401

# The home page's empty card shows Romania's outline in its flag above
# "pick a category". The engine has no setting for that, so this borrows
# analytics_html (raw HTML at the bottom of every page, after app.js): while
# the card still says "pick a category", put the flag map above the text.
# Loading a category replaces the card's text, so the map goes with it.
# Flag map: Wikimedia Commons, "Flag map of Romania.svg", public domain.
HOME_CARD_HTML = """
<style>
    #status.home { width: 100%; text-align: center; }
    #status .home-map, #done-art .home-map { display: block; width: 80%; margin: 0 auto 1.5rem; }
</style>
<script>
(function () {
    var status = document.getElementById('status');
    if (status && status.textContent.trim() === 'pick a category') {
        status.classList.add('home');
        status.insertAdjacentHTML('afterbegin', '<img class="home-map" src="/static/flag-map-romania.svg" alt="Romania">');
    }
})();
</script>
"""

config = MemiConfig(
    # Details panel beside the card on reveal: the Wikipedia intro and, for
    # places, a map.
    layout="enriched",
    wikipedia_lang="en",
    title="memi romania",
    subtitle="practise your memory of Romania",
    favicon_color="#002B7F",
    analytics_html=HOME_CARD_HTML,
    sponsor_url="https://github.com/sponsors/filias",
    sponsor_text="sponsor",
    related_sites=[
        {"name": "memi", "url": "https://world.memi.games"},
        {"name": "memi portugal", "url": "https://pt.memi.games"},
        {"name": "memi lisboa", "url": "https://lx.memi.games"},
        {"name": "memi slovensko", "url": "https://sk.memi.games"},
        {"name": "memi kraków", "url": "https://kr.memi.games"},
        {"name": "memi united states", "url": "https://us.memi.games"},
    ],
    about_html="""
        <p>Memi Romania is a memory game about Romania. Counties, sights,
        food, famous people &mdash; there's always something new to
        learn.</p>

        <h2>How to play</h2>
        <p>Pick a category, look at the picture and try to name it before
        revealing the answer. No accounts, no scores, no time limits.</p>
        <p>The bottom bar has a few helpers:</p>
        <ul>
            <li><strong>clues:</strong> turns on progressive letter clues
            &mdash; show the first letter, then the next, and so on. Handy
            when the name is on the tip of your tongue.</li>
            <li><strong>know more:</strong> appears on reveal and opens the
            item's Wikipedia article (or its source page), so you can read
            more.</li>
            <li><strong>report:</strong> flags a card whose picture doesn't
            match the answer (wrong image, broken thumbnail, etc.).</li>
        </ul>
        <p>You can play in two ways:</p>
        <ul>
            <li><strong>To learn:</strong> when you don't recognise
            something, reveal the answer and follow <em>know more</em>.
            Each exposure strengthens the link between the picture and the
            name.</li>
            <li><strong>To test yourself:</strong> once a category feels
            familiar, go through it and see how many you can name without
            revealing.</li>
        </ul>

        <h2>Why it works</h2>
        <p>It's a simple form of <em>active recall</em> &mdash; pulling a
        name out of memory instead of re-reading it. The <em>testing
        effect</em>, well documented in cognitive psychology, shows that
        retrieval practice builds more durable memory than re-exposure
        alone.</p>
        <p>Because each prompt is a picture, the game also leans on the
        <em>picture superiority effect</em>: pictures are encoded more
        richly than words and are easier to recall later.</p>
        <p>Short, frequent sessions work better than long ones &mdash; the
        <em>spacing effect</em>. A few minutes a day is enough.</p>

        <h2>Credits</h2>
        <p>Images and descriptions from Wikipedia and Wikimedia Commons, under
        their Creative Commons licences. Romanian recordings by native
        speakers for <a href="https://lingualibre.org">Lingua Libre</a>
        (CC BY-SA 4.0 / CC0; speakers listed in
        <a href="https://github.com/filias/memi-ro/blob/main/static/audio/CREDITS.md">CREDITS.md</a>).
        Maps &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>
        contributors.</p>
    """,
    # The "all done" card shows the same flag map as the home card.
    done_html='<img class="home-map" src="/static/flag-map-romania.svg" alt="Romania">',
)

import os
from flask import redirect

instance_static = os.path.join(os.path.dirname(__file__), "..", "static")
app = create_app(config, instance_static=instance_static)


# "monarchy 1859–1947" had an en dash, which the address dropped
# (/monarchy-18591947); the hyphen gives /monarchy-1859-1947.
@app.route("/monarchy-18591947")
def old_monarchy_link():
    return redirect("/monarchy-1859-1947", code=301)

if __name__ == "__main__":
    app.run(debug=True, port=8110)
