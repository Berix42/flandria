from flask_restx import fields

from webapp.extensions import api_
from webapp.models.enums import CharacterClass, Server

characterClassData = api_.model("characterClassData", {
    "value": fields.String(description="Short technical value to identify class",
                           enum=[cc.value for cc in CharacterClass]),
    "name": fields.String(description="Human readable name of class", enum=list(CharacterClass.names().values()))
})

serverData = api_.model("serverData", {
    "value": fields.Integer(description="Short technical value to identify server",
                            min=min([s.value for s in Server]), max=max([s.value for s in Server])),
    "name": fields.String(description="Human readable name of server", enum=list(Server.luxplena.names.values()))
})

paginationData = api_.model("paginationData", {
    "has_next": fields.Boolean,
    "has_previous": fields.Boolean,
    "labels": fields.List(fields.Integer, example=[1, 2, 3, 4, 5, None, 15, 16]),
})

guildData = api_.model('guildData', {
    "name": fields.String(example="~WorldsEnd~"),
    "server": fields.Nested(serverData),
    "member_count": fields.Integer(example=42),
    "avg_level_land": fields.Float(example=42.42),
    "avg_level_sea": fields.Float(example=13.37),
    "avg_rank": fields.Float(example=42013.37),
})

playerData = api_.model('playerData', {
    "name": fields.String(example="Celty"),
    "rank": fields.Integer(example=1),
    "server": fields.Nested(serverData),
    "guild": fields.String(example="~WorldsEnd~"),
    "character_class": fields.Nested(characterClassData),
    "level_land": fields.Integer(example=105),
    "level_sea": fields.Integer(example=69)
})
