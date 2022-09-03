from flask_restx import Resource, abort, fields

from webapp.api.common_api_models import playerData
from webapp.models import RankingPlayer
from webapp.models.enums import Server
from webapp.extensions import cache, api_


playerDetailRequestParser = api_.parser()
playerDetailRequestParser.add_argument('server', type=str, choices=[s.name for s in Server],
                                       help='Server of the ranking.')
playerDetailRequestParser.add_argument('name', type=str,
                                       help='Name of the player the details are requested for.')

playerDetailData = api_.inherit('playerDetailData', playerData, {
    "history": fields.List(fields.Raw),
    "updated_at": fields.String(example="2022-01-01 11:46:04.204582"),
    "indexed_at": fields.String(example="2022-01-01 11:46:04.204582"),
})


@api_.expect(playerDetailRequestParser)
class PlayerDetailedView(Resource):
    @api_.marshal_with(playerDetailData, code=200, description="Get player ranking data")
    @api_.response(400, 'Unknown server')
    @api_.response(404, 'Player not found')
    def get(self, server: str, name: str):
        resp = self._get_response(
            server=server,
            name=name,
        )

        return resp, 200

    @cache.memoize(timeout=0)
    def _get_response(
        self,
        server: str,
        name: str,
    ) -> dict:
        try:
            server_value = Server[server]
        except ValueError:
            abort(400, "Unknown server")
        player = RankingPlayer.query.get_or_404((server_value, name), "Player not found")

        return player.to_dict()
