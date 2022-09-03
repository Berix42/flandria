from flask_restx import Resource, abort
from webapp.api.database.constants import ALLOWED_DATABASE_TABLES
from webapp.api.database.utils import get_model_from_tablename
from webapp.extensions import cache, api_

detailTableRequestParser = api_.parser()
detailTableRequestParser.add_argument('table', type=str, help='Unique string to identify a table.',
                                      choices=ALLOWED_DATABASE_TABLES)
detailTableRequestParser.add_argument('code', type=str, help='Unique code to identify a specific item / monster, '
                                                             'depends on selected table.')


@api_.expect(detailTableRequestParser)
@api_.response(200, '')
@api_.response(404, '&lt;Error description&gt;')
class DetailedTableView(Resource):
    def get(self, table: str, code: str):
        if table not in ALLOWED_DATABASE_TABLES:
            abort(404, "Table does not exist.")

        resp = self._get_response(table, code)

        return resp, 200

    @cache.memoize(timeout=0)
    def _get_response(self, table: str, code: str) -> dict:
        model = get_model_from_tablename(table)
        item = model.query.get_or_404(code, 'Code not found')

        return item.to_dict()
