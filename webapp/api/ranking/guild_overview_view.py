import typing

from flask_restx import Resource, abort, fields
from sqlalchemy import func, text

from webapp.api.common_api_models import paginationData, guildData
from webapp.api.utils import get_url_parameter
from webapp.models import RankingPlayer
from webapp.models.enums import Server
from webapp.extensions import cache, api_


guildOverviewRequestParser = api_.parser()
guildOverviewRequestParser.add_argument('server', type=str, help='Unique string to identify a table.',
                                        choices=["both"]+[s.name for s in Server], default="both")
guildOverviewRequestParser.add_argument('page', type=int, help='Which data-block to select.', default=1)
guildOverviewRequestParser.add_argument('limit', type=int, help='Max number of items in a data-block.', default=60)


guildOverviewData = api_.model('guildOverviewData', {
    "items": fields.List(fields.Nested(guildData)),
    "pagination": fields.Nested(paginationData)
})


@api_.expect(guildOverviewRequestParser)
class GuildOverviewView(Resource):
    @api_.marshal_with(guildOverviewData, code=200, description="Get guild ranking data")
    @api_.response(400, 'Unknown server')
    def get(self):
        req_args = guildOverviewRequestParser.parse_args()

        resp = self._get_response(
            server=req_args.server,
            page=req_args.page,
            per_page=req_args.limit,
        )

        return resp, 200

    @cache.memoize(timeout=0)
    def _get_response(
        self,
        page: int,
        per_page: int,
        server: typing.Optional[str] = None,
    ) -> typing.List[dict]:
        query = (
            RankingPlayer.query
            .with_entities(
                RankingPlayer.guild,
                RankingPlayer.server,
                func.count(RankingPlayer.guild).label("member_count"),
                func.avg(RankingPlayer.level_land).label("avg_level_land"),
                func.avg(RankingPlayer.level_sea).label("avg_level_sea"),
                func.avg(RankingPlayer.rank).label("avg_rank"),
            ).filter(
                RankingPlayer.guild.isnot(None),
            ).group_by(
                RankingPlayer.guild,
            ).order_by(
                text("-member_count"),
            )
        )

        # Apply server filter, if server is given
        if server != "both":
            try:
                server_value = Server[server]
            except ValueError:
                abort(400, "Unknown server")
            query = query.filter(RankingPlayer.server == server_value)

        # Create pagination based on query and return in
        pagination_obj = query.paginate(page=page, per_page=per_page)

        return {
            "items": [
                {
                    "name": item.guild,
                    "server": item.server.to_dict(),
                    "member_count": int(item.member_count),
                    "avg_level_land": float(item.avg_level_land),
                    "avg_level_sea": float(item.avg_level_sea),
                    "avg_rank": float(item.avg_rank),
                } for item in pagination_obj.items
            ],
            "pagination": {
                "has_next": pagination_obj.has_next,
                "has_previous": pagination_obj.has_prev,
                "labels": list(pagination_obj.iter_pages()),
            }
        }
