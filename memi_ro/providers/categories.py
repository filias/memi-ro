"""Romanian category providers."""

from memi_engine import CategoryProvider, images, register

from memi_ro.categories.counties import (
    COUNTIES,
    MAP_FILES as COUNTY_MAPS,
    WIKIPEDIA as COUNTY_WIKI,
)

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


register(CountiesProvider())
