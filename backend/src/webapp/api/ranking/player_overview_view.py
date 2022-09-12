from flask_restx import Resource, abort

from webapp.api.common_api_models import playerData
from webapp.extensions import cache, api_
from webapp.models import RankingPlayer
from webapp.models.enums import Server


playerRankingRequestParser = api_.parser()
playerRankingRequestParser.add_argument('server', type=str, choices=[s.name for s in Server],
                                        help='Server of the ranking.')
playerRankingRequestParser.add_argument('min_lv_land', type=int, default=1,
                                        help='Minimum level of players to be included in the ranking.')


@api_.expect(playerRankingRequestParser)
class PlayerOverviewView(Resource):
    @api_.marshal_with(playerData, code=200, description="Get player ranking data")
    @api_.response(400, 'Unknown server')
    def get(self):
        req_args = playerRankingRequestParser.parse_args()

        resp = self._get_response(
            server=req_args.server,
            min_level_land=req_args.min_lv_land
        )

        return resp, 200

    @cache.memoize(timeout=0)
    def _get_response(
        self,
        server: str,
        min_level_land: int,
    ) -> dict:
        query = (
            RankingPlayer.query
            .filter(
                RankingPlayer.level_land >= min_level_land,
            )
        )

        if server:
            try:
                server_value = Server[server]
            except ValueError:
                abort(400, "Unknown server")
            query = query.filter(RankingPlayer.server == server_value)

        return [player.to_dict(minimal=True) for player in query.all()]
