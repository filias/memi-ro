"""Romanian category providers."""

from memi_engine import CategoryProvider, images, register

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
from memi_ro.categories.sights import (
    COMMONS_FILES as SIGHT_FILES,
    LOCATIONS as SIGHT_LOCATIONS,
    SIGHTS,
    WIKIPEDIA as SIGHT_WIKI,
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


register(CountiesProvider())
register(CitiesProvider())
register(SightsProvider())
register(FoodProvider())
