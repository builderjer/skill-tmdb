# Copyright 2016 Mycroft AI, Inc.
#
# This file is part of Mycroft Core.
#
# Mycroft Core is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mycroft Core is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mycroft Core.  If not, see <http://www.gnu.org/licenses/>.


#from tmdbv3api import TMDb
import tmdbv3api as TM

from adapt.intent import IntentBuilder

from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger
import requests

__author__ = 'eClarity'

LOGGER = getLogger(__name__)

tmdb = TM.TMDb()
collection = TM.Collection()
company = TM.Company()
configuration = TM.Configuration()
discover = TM.Discover()
genre = TM.Genre()
movie = TM.Movie()
person = TM.Person()
season = TM.Season()
tv = TM.TV()

##This will eventually move to the mycroft configuration


class TmdbSkill(MycroftSkill):
    def __init__(self):
        super(TmdbSkill, self).__init__(name="TmdbSkill")
        tmdb.api_key = self.settings.get("v3api")
        tmdb.language = "en_US"

    def initialize(self):
        search_actor_intent = IntentBuilder("SearchActorIntent").require("SearchActorKeyword").require("Actor").build()
        self.register_intent(search_actor_intent, self.handle_search_actor_intent)

        upcoming_intent = IntentBuilder("UpcomingIntent").require("UpcomingKeyword").build()
        self.register_intent(upcoming_intent, self.handle_upcoming_intent)

        now_playing_intent = IntentBuilder("NowPlayingIntent").require("NowPlayingKeyword").build()
        self.register_intent(now_playing_intent, self.handle_now_playing_intent)

        movie_intent = IntentBuilder("MovieIntent").require("MovieKeyword").require("Movie").build()
        self.register_intent(movie_intent, self.handle_movie_intent)

        popular_tv_intent = IntentBuilder("PopularTvIntent").require("PopularTvKeyword").build()
        self.register_intent(popular_tv_intent, self.handle_popular_tv_intent)


    def handle_upcoming_intent(self, message):
        upcoming = movie.upcoming()
        for m in upcoming:
            self.speak(m.title)

    def handle_now_playing_intent(self, message):
        now_playing = movie.now_playing()
        for m in now_playing:
            self.speak(m.title)

    def handle_search_actor_intent(self, message):
        actor = message.data.get("Actor")
        search = person.search(actor)
        for result in search [:1]:
            actor = result.id
            p = person.details(actor)
            self.speak(p.biography)

    def handle_movie_intent(self, message):
        mov = message.data.get("Movie")
        search = movie.search(mov)
        for result in search [:1]:
            id = str(result.id)
            m = movie.details(id)
            for k, v in m.__dict__.items():
                s = str(k) + ': ' + str(v)
                LOGGER.info(s)
            #response = m.overview
            if m.overview:
                self.speak(m.overview)
            else:
                self.speak("no info")

    def handle_popular_tv_intent(self, message):
        popular = tmdb.popular_shows()
        self.speak("Sure, here are the most popular shows" )
        for show in popular:
            self.speak(show.name)
        

    def stop(self):
        pass


def create_skill():
    return TmdbSkill()
