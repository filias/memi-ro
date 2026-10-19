"""Memi Romania - practise your memory of Romania."""

from memi_engine import MemiConfig, create_app

# Import providers to register them
import memi_ro.providers  # noqa: F401

config = MemiConfig(
    default_category="geography:counties",
    # Details panel beside the card on reveal: the Wikipedia intro and, for
    # places, a map.
    layout="enriched",
    wikipedia_lang="en",
    title="memi romania",
    subtitle="practise your memory of Romania",
    favicon_color="#002B7F",
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
    """,
    done_html="""
        <svg width="200" height="180" viewBox="0 0 80 72" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <clipPath id="heart-clip">
                    <path d="M40 68 C40 68 4 44 4 22 C4 10 14 2 24 2 C30 2 36 6 40 12 C44 6 50 2 56 2 C66 2 76 10 76 22 C76 44 40 68 40 68Z"/>
                </clipPath>
            </defs>
            <g clip-path="url(#heart-clip)">
                <rect x="0" y="0" width="27" height="72" fill="#002B7F"/>
                <rect x="27" y="0" width="26" height="72" fill="#FCD116"/>
                <rect x="53" y="0" width="27" height="72" fill="#CE1126"/>
            </g>
            <path d="M40 68 C40 68 4 44 4 22 C4 10 14 2 24 2 C30 2 36 6 40 12 C44 6 50 2 56 2 C66 2 76 10 76 22 C76 44 40 68 40 68Z"
                  fill="none" stroke="var(--subtle, #888)" stroke-width="1.5"/>
        </svg>
    """,
)

import os
instance_static = os.path.join(os.path.dirname(__file__), "..", "static")
app = create_app(config, instance_static=instance_static)

if __name__ == "__main__":
    app.run(debug=True, port=8093)
