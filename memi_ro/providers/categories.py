"""Romanian category providers."""

import base64
from pathlib import Path
from urllib.parse import quote

from memi_engine import CategoryProvider, ScientificNameProvider, images, register

from memi_ro.categories.cities import (
    CITIES,
    REGIONS as CITY_REGIONS,
    WIKIPEDIA as CITY_WIKI,
)
from memi_ro.categories.counties import (
    COUNTIES,
    MAP_FILES as COUNTY_MAPS,
    WIKIPEDIA as COUNTY_WIKI,
)
from memi_ro.categories.food import (
    COMMONS_FILES as FOOD_FILES,
    FOOD,
    WIKIPEDIA as FOOD_WIKI,
)
from memi_ro.categories.language import ENGLISH, PHRASE_NOTES, PHRASES, phrase_slug
from memi_ro.categories.nature import (
    ANIMAL_WIKIPEDIA,
    ANIMALS,
    PLANTS,
    SCIENTIFIC_NAMES,
)
from memi_ro.categories.people import (
    BEFORE_1859,
    COMMONS_FILES as PEOPLE_FILES,
    KINGDOM,
    SINCE_1947,
    TAGS as PEOPLE_TAGS,
    WIKIPEDIA as PEOPLE_WIKI,
)
from memi_ro.categories.sights import (
    COMMONS_FILES as SIGHT_FILES,
    LOCATIONS as SIGHT_LOCATIONS,
    SIGHTS,
    WIKIPEDIA as SIGHT_WIKI,
)

AUDIO_DIR = Path(__file__).resolve().parent.parent.parent / "static" / "audio"

# Romania. Wikidata coordinates outside it belong to something other than the
# place on the card, so they get no map.
ROMANIA_BOUNDS = ((43.6, 48.3), (20.2, 29.8))


class CountiesProvider(CategoryProvider):
    key = "geography:counties"
    items = COUNTIES
    override_name = True
    map_zoom = 8
    map_bounds = ROMANIA_BOUNDS

    def get_image(self, item):
        map_file = COUNTY_MAPS.get(item)
        if map_file:
            result = images.get_wikipedia_file_image(map_file)
            if result:
                return result
        return images.get_wikipedia_image(COUNTY_WIKI.get(item, item))

    def get_wikipedia_title(self, item):
        # The card is a map file with no article link of its own.
        return ("en", COUNTY_WIKI.get(item, item))


class CitiesProvider(CategoryProvider):
    key = "geography:cities"
    items = CITIES
    override_name = True
    map_zoom = 12
    map_bounds = ROMANIA_BOUNDS

    def get_image(self, item):
        return images.get_wikipedia_image(CITY_WIKI.get(item, item))

    def get_tag(self, item):
        return CITY_REGIONS.get(item)


class SightsProvider(CategoryProvider):
    key = "culture:sights"
    items = SIGHTS
    override_name = True
    map_zoom = 16
    map_bounds = ROMANIA_BOUNDS

    def get_image(self, item):
        filename = SIGHT_FILES.get(item)
        if filename:
            return images.get_commons_file_image(filename)
        return images.get_wikipedia_image(SIGHT_WIKI.get(item, item))

    def get_tag(self, item):
        return SIGHT_LOCATIONS.get(item)

    def get_wikipedia_title(self, item):
        # Commons photos have no article link of their own.
        return ("en", SIGHT_WIKI.get(item, item))


class FoodProvider(CategoryProvider):
    key = "culture:food"
    items = FOOD
    override_name = True

    def get_image(self, item):
        filename = FOOD_FILES.get(item)
        if filename:
            return images.get_commons_file_image(filename)
        return images.get_wikipedia_image(FOOD_WIKI.get(item, item))

    def get_wikipedia_title(self, item):
        # Commons photos have no article link of their own.
        return ("en", FOOD_WIKI.get(item, item))


class PeopleProvider(CategoryProvider):
    override_name = True

    def get_image(self, item):
        filename = PEOPLE_FILES.get(item)
        if filename:
            return images.get_commons_file_image(filename)
        return images.get_wikipedia_image(PEOPLE_WIKI.get(item, item))

    def get_tag(self, item):
        return PEOPLE_TAGS.get(item)

    def get_wikipedia_title(self, item):
        # Commons portraits have no article link of their own.
        return ("en", PEOPLE_WIKI.get(item, item))


class PeopleBefore1859(PeopleProvider):
    key = "people:before 1859"
    items = BEFORE_1859


class PeopleKingdom(PeopleProvider):
    key = "people:monarchy 1859-1947"
    items = KINGDOM


class PeopleSince1947(PeopleProvider):
    key = "people:since 1947"
    items = SINCE_1947


class AnimalsProvider(ScientificNameProvider):
    key = "nature:animals"
    items = ANIMALS
    override_name = True
    scientific_names = SCIENTIFIC_NAMES

    def get_image(self, item):
        return images.get_wikipedia_image(ANIMAL_WIKIPEDIA.get(item, item))


class PlantsProvider(ScientificNameProvider):
    key = "nature:plants"
    items = PLANTS
    override_name = True
    scientific_names = SCIENTIFIC_NAMES

    def get_image(self, item):
        # Plant articles mostly live under the scientific name (the common
        # one is often a genus or a disambiguation page), but a few are the
        # other way round, with the Latin name only a redirect.
        result = images.get_wikipedia_image(SCIENTIFIC_NAMES[item])
        if not result or not result.get("image"):
            result = images.get_wikipedia_image(item)
        return result


def _text_card(text):
    """Render a short phrase as an SVG data-URI to use as the card image."""
    size = min(60, max(28, 780 // max(len(text), 1)))
    safe = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="640" height="420" '
        'viewBox="0 0 640 420">'
        '<rect width="640" height="420" fill="#f7f5f0"/>'
        f'<text x="320" y="140" text-anchor="middle" dominant-baseline="middle" '
        f"font-family=\"Georgia, 'Times New Roman', serif\" font-size=\"{size}\" "
        f'fill="#223344">{safe}</text>'
        "</svg>"
    )
    b64 = base64.b64encode(svg.encode("utf-8")).decode("ascii")
    return "data:image/svg+xml;base64," + b64


class EnglishToRomanian(CategoryProvider):
    """Read the English, say the Romanian."""

    key = "language:english → romanian"
    light_bg = True
    items = list(PHRASES)

    def romanian(self, item):
        return PHRASES[item]

    def get_image(self, item):
        romanian = self.romanian(item)
        return {
            "name": romanian,
            "image": _text_card(item),
            "url": f"https://en.wiktionary.org/wiki/{quote(romanian)}",
        }

    def get_details(self, item):
        say, note = PHRASE_NOTES[self.romanian(item)]
        return {"text": f"Say: {say}\n\n{note}"}

    def get_audio(self, item):
        """The Romanian, spoken: a native speaker's recording from
        static/audio/<slug>.mp3 when there is one, else the browser's voice."""
        romanian = self.romanian(item)
        audio = {"text": romanian, "lang": "ro-RO"}
        recording = AUDIO_DIR / f"{phrase_slug(romanian)}.mp3"
        if recording.exists():
            audio["src"] = f"/static/audio/{recording.name}"
        return audio


class RomanianToEnglish(EnglishToRomanian):
    """The other way round: read the Romanian, name the English."""

    key = "language:romanian → english"
    items = list(ENGLISH)
    submenu_default = True

    def romanian(self, item):
        return item

    def get_image(self, item):
        return {**super().get_image(item), "name": ENGLISH[item]}

    def get_audio(self, item):
        # Hearing the Romanian is part of the question here: listen, then answer.
        return {**super().get_audio(item), "before_reveal": True}


register(CountiesProvider())
register(CitiesProvider())
register(SightsProvider())
register(FoodProvider())
register(PeopleBefore1859())
register(PeopleKingdom())
register(PeopleSince1947())
register(AnimalsProvider())
register(PlantsProvider())
register(RomanianToEnglish())
register(EnglishToRomanian())
