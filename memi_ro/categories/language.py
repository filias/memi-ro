"""Everyday Romanian: about 20 useful words and phrases."""

import re
import unicodedata

PHRASES = {
    "hello": "bună ziua",
    "hi": "salut",
    "good morning": "bună dimineața",
    "good evening": "bună seara",
    "good night": "noapte bună",
    "goodbye": "la revedere",
    "thank you": "mulțumesc",
    "please": "vă rog",
    "you're welcome": "cu plăcere",
    "yes": "da",
    "no": "nu",
    "sorry": "îmi pare rău",
    "excuse me": "scuzați-mă",
    "how are you?": "ce mai faci?",
    "cheers!": "noroc!",
    "enjoy your meal!": "poftă bună!",
    "I don't understand": "nu înțeleg",
    "how much is it?": "cât costă?",
    "the bill, please": "nota, vă rog",
    "help!": "ajutor!",
    "water": "apă",
    "beer": "bere",
    "wine": "vin",
    "friend": "prieten",
    "love": "dragoste",
}

# For the details panel: how to say it (stress in capitals) and when to use it.
PHRASE_NOTES = {
    "bună ziua": ("BOO-nuh ZEE-wa", "The polite hello, used through the day; literally \"good day\"."),
    "salut": ("sa-LOOT", "Hi — and bye — among friends."),
    "bună dimineața": ("BOO-nuh dee-mee-NYA-tsa", "Good morning, until about ten or eleven."),
    "bună seara": ("BOO-nuh SYA-ra", "Good evening, the hello once it gets dark."),
    "noapte bună": ("NWAP-teh BOO-nuh", "Good night, when going to bed or leaving late — not a greeting."),
    "la revedere": ("la reh-veh-DEH-reh", "The polite goodbye; literally \"until seeing again\"."),
    "mulțumesc": ("mool-tsoo-MESK", "Thank you. Mersi, from French, is just as common."),
    "vă rog": ("vuh ROG", "Please, to a stranger or more than one person. To a friend: te rog."),
    "cu plăcere": ("koo pluh-CHEH-reh", "You're welcome; literally \"with pleasure\"."),
    "da": ("da", "Yes."),
    "nu": ("noo", "No — and \"not\": nu știu, \"I don't know\"."),
    "îmi pare rău": ("uhm PA-reh ruh-oo", "I'm sorry; literally \"it seems bad to me\"."),
    "scuzați-mă": ("skoo-ZATS-muh", "Excuse me — to get past or get someone's attention."),
    "ce mai faci?": ("cheh my FAHCH", "How are you? — to a friend. Politely: ce mai faceți?"),
    "noroc!": ("no-ROK", "Cheers! It also means \"luck\"."),
    "poftă bună!": ("POF-tuh BOO-nuh", "Enjoy your meal — said as the food arrives."),
    "nu înțeleg": ("noo uhn-tseh-LEG", "I don't understand. Add mai încet, vă rog — \"slower, please\"."),
    "cât costă?": ("kuht KOS-tuh", "How much is it?"),
    "nota, vă rog": ("NO-ta vuh ROG", "The bill, please."),
    "ajutor!": ("a-zhoo-TOR", "Help! Emergency number in Romania: 112."),
    "apă": ("A-puh", "Water. Plată is still, minerală is sparkling."),
    "bere": ("BEH-reh", "Beer. O bere, vă rog — \"a beer, please\"."),
    "vin": ("veen", "Wine: roșu (red), alb (white)."),
    "prieten": ("pree-EH-ten", "Friend; a woman friend is prietenă."),
    "dragoste": ("DRA-gos-teh", "Love. \"I love you\" is te iubesc (teh yoo-BESK)."),
}

# The same phrases keyed by their Romanian, for the Romanian → English direction.
ENGLISH = {romanian: english for english, romanian in PHRASES.items()}

# Native recordings on Wikimedia Commons, from Lingua Libre. Speakers and
# licences are in static/audio/CREDITS.md; phrases missing here use the
# browser's voice.
RECORDINGS = {
    "bună ziua": "LL-Q7913 (ron)-Andreea Teodoraa-bună ziua.wav",
    "salut": "LL-Q7913 (ron)-Andreea Teodoraa-salut.wav",
    "bună dimineața": "LL-Q7913 (ron)-Andreea Teodoraa-bună dimineața.wav",
    "bună seara": "LL-Q7913 (ron)-Andreea Teodoraa-bună seara.wav",
    "noapte bună": "LL-Q7913 (ron)-Andreea Teodoraa-noapte bună.wav",
    "la revedere": "LL-Q7913 (ron)-Andreea Teodoraa-la revedere.wav",
    "mulțumesc": "LL-Q7913 (ron)-Papaeta-mulțumesc.wav",
    "cu plăcere": "LL-Q7913 (ron)-Andreea Teodoraa-cu plăcere.wav",
    "da": "LL-Q7913 (ron)-Andreea Teodoraa-da.wav",
    "nu": "LL-Q7913 (ron)-Andreea Teodoraa-nu.wav",
    "scuzați-mă": "LL-Q7913 (ron)-Andreea Teodoraa-scuzați-mă.wav",
    "noroc!": "LL-Q7913 (ron)-Andreea Teodoraa-noroc.wav",
    "ajutor!": "LL-Q7913 (ron)-Andreea Teodoraa-ajutor.wav",
    "apă": "LL-Q7913 (ron)-Andreea Teodoraa-apă.wav",
    "bere": "LL-Q7913 (ron)-Andreea Teodoraa-bere.wav",
    "vin": "LL-Q7913 (ron)-Andreea Teodoraa-vin.wav",
    "prieten": "LL-Q7913 (ron)-Andreea Teodoraa-prieten.wav",
    "dragoste": "LL-Q7913 (ron)-Andreea Teodoraa-dragoste.wav",
}


def phrase_slug(romanian):
    """``"ce mai faci?"`` -> ``"ce-mai-faci"`` (recording filename)."""
    folded = unicodedata.normalize("NFKD", romanian)
    ascii_text = folded.encode("ascii", "ignore").decode().lower()
    return "-".join(re.findall(r"[a-z0-9]+", ascii_text))
