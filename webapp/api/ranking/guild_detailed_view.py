from flask_restx import Resource, abort, fields
from sqlalchemy import func

from webapp.api.common_api_models import guildData, playerData
from webapp.extensions import cache, api_
from webapp.models import RankingPlayer


guildDetailRequestParser = api_.parser()
guildDetailRequestParser.add_argument('name', type=str, help='Name of the guild the details are requested for.')

guildDetailData = api_.model('guildDetailData', {
    "guild": fields.Nested(guildData),
    "members": fields.List(fields.Nested(playerData))
})


@api_.expect(guildDetailRequestParser)
class GuildDetailedView(Resource):
    @api_.marshal_with(guildDetailData, code=200, description="Get guild detail data")
    @api_.response(404, 'Guild was not found.')
    def get(self, name: str):

        resp = self._get_response(name=name)

        return resp, 200

    @cache.memoize(timeout=0)
    def _get_response(
        self,
        name: str
    ) -> dict:
        guild = (
            RankingPlayer.query
            .with_entities(
                RankingPlayer.guild,
                RankingPlayer.server,
                func.count(RankingPlayer.guild).label("member_count"),
                func.avg(RankingPlayer.level_land).label("avg_level_land"),
                func.avg(RankingPlayer.level_sea).label("avg_level_sea"),
                func.avg(RankingPlayer.rank).label("avg_rank"),
            ).filter(
                RankingPlayer.guild == name
            ).first()
        )

        if not guild.guild:
            abort(404, "Guild was not found.")

        members = (
            RankingPlayer.query
            .filter(RankingPlayer.guild == name)
            .all()
        )

        return {
            "guild": {
                "name": guild.guild,
                "server": guild.server.to_dict(),
                "member_count": int(guild.member_count),
                "avg_level_land": float(guild.avg_level_land),
                "avg_level_sea": float(guild.avg_level_sea),
                "avg_rank": float(guild.avg_rank),
            },
            "members": [player.to_dict(minimal=True)
                        for player in members],
        }
