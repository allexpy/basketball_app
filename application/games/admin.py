# Third-party
from django.contrib import admin

# Local
from games.models import Game, League, Season, Team

admin.site.register(Season)
admin.site.register(League)
admin.site.register(Team)
admin.site.register(Game)
