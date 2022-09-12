from flask_restx import Resource, fields
from webapp.extensions import cache, api_
from webapp.models import Map


mapMetaData = api_.model('mapMetaData', {
  "code": fields.String(example="AF2_000"),
  "name": fields.String(example="Weedridge"),
  "left": fields.Float(example=-63875.937),
  "top": fields.Float(example=62559.402),
  "width": fields.Float(example=110000),
  "height": fields.Float(example=110000),
  "points": fields.List(fields.Raw),
})


@api_.param('code', 'Unique string for map selection')
class MapView(Resource):
    @api_.marshal_with(mapMetaData, code=200, description="Get map meta data")
    @api_.response(404, 'Not found')
    def get(self, code: str):
        resp = self._get_response(code)

        return resp, 200

    @cache.memoize(timeout=0)
    def _get_response(self, code: str) -> dict:
        map_ = Map.query.get_or_404(code.strip())

        return map_.to_dict()
