"""Memi România - practise your memory of Romania."""

from memi_engine import MemiConfig, create_app

# Import providers to register them
import memi_ro.providers  # noqa: F401

config = MemiConfig(
    default_category="geografie:județe",
    # What the page tells Google and screen readers it is: this game
    # is Romanian, not the engine's default English.
    html_lang="ro",
    # Details panel beside the card on reveal: the Wikipedia intro (in
    # Romanian where it exists) and, for places, a map.
    layout="enriched",
    title="memi românia",
    subtitle="exersează-ți memoria",
    favicon_color="#002B7F",
    sponsor_url="https://github.com/sponsors/filias",
    sponsor_text="susține",
    related_sites=[
        {"name": "memi", "url": "https://world.memi.games"},
        {"name": "memi portugal", "url": "https://pt.memi.games"},
        {"name": "memi lisboa", "url": "https://lx.memi.games"},
        {"name": "memi slovensko", "url": "https://sk.memi.games"},
        {"name": "memi kraków", "url": "https://kr.memi.games"},
        {"name": "memi united states", "url": "https://us.memi.games"},
    ],
    label_related_sites="alte jocuri memi",
    about_html="""
        <p>Memi România este un joc de memorie despre România. Județe,
        monumente, mâncare, oameni celebri &mdash; e mereu ceva nou de
        învățat.</p>

        <h2>Cum se joacă</h2>
        <p>Alege o categorie, uită-te la imagine și încearcă să ghicești
        ce este înainte de a dezvălui răspunsul. Fără conturi, fără
        punctaj, fără limită de timp.</p>
        <p>În bara de jos ai câteva ajutoare:</p>
        <ul>
            <li><strong>indicii:</strong> activează indicii progresive
            &mdash; dezvăluie prima literă, apoi următoarea și așa mai
            departe. Util când numele îți stă pe limbă.</li>
            <li><strong>află mai mult:</strong> apare la dezvăluire și
            deschide articolul de pe Wikipedia (sau pagina sursei), ca să
            poți citi mai mult.</li>
            <li><strong>raportează:</strong> marchează o carte dacă imaginea
            nu se potrivește cu răspunsul (imagine greșită, miniatură
            stricată etc.).</li>
        </ul>
        <p>Poți juca în două feluri:</p>
        <ul>
            <li><strong>Ca să înveți:</strong> când nu recunoști ceva,
            dezvăluie răspunsul și urmează linkul <em>află mai mult</em>.
            Fiecare expunere întărește legătura dintre imagine și
            nume.</li>
            <li><strong>Ca să te testezi:</strong> când o categorie îți e
            deja familiară, parcurge-o și vezi câte poți numi fără să
            dezvălui.</li>
        </ul>

        <h2>De ce funcționează</h2>
        <p>Este o formă simplă de <em>reamintire activă</em> &mdash;
        recuperarea informației din memorie în loc de recitire.
        <em>Efectul de testare</em>, bine documentat în psihologia
        cognitivă, arată că exersarea reamintirii creează amintiri mai
        durabile decât simpla re-expunere.</p>
        <p>Pentru că fiecare stimul este o imagine, jocul folosește și
        <em>efectul de superioritate a imaginii</em>: imaginile sunt
        codificate mai bogat decât cuvintele și mai ușor de reamintit
        apoi.</p>
        <p>Sesiunile scurte și dese funcționează mai bine decât cele
        lungi &mdash; <em>efectul de spațiere</em>. Câteva minute pe zi
        sunt de ajuns.</p>
    """,
    # Romanian labels
    label_theme="temă",
    label_about="despre",
    label_report="raportează",
    label_reported="raportat",
    label_clues_on="indicii: da",
    label_clues_off="indicii: nu",
    label_show_letter="arată o literă",
    label_pick_category="alege o categorie",
    label_loading="se încarcă...",
    label_all_done="gata! apasă ca să reîncepi",
    label_click_to_reveal="apasă pe imagine ca să vezi răspunsul",
    label_click_for_new="apasă din nou pentru alta",
    label_back="înapoi la joc",
    label_more="află mai mult",
    label_open_map="deschide harta",
    label_listen="ascultă",
    label_all="toate",
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
