import re
import typing

from flask_restx import Resource, abort, fields
from sqlalchemy import or_

from webapp.api.common_api_models import paginationData
from webapp.api.database.constants import ALLOWED_DATABASE_TABLES
from webapp.api.database.utils import get_model_from_tablename
from webapp.api.utils import get_url_parameter
from webapp.extensions import cache, api_
from webapp.models.enums import (AccessoryType, Area, EffectCode, EssenceEquipType,
                                 ProductionType, RatingType)

tableRequestParser = api_.parser()
tableRequestParser.add_argument('table', type=str, help='Unique string to identify a table.',
                                choices=ALLOWED_DATABASE_TABLES)
tableRequestParser.add_argument('page', type=int, help='Which data-block to select.', default=1)
tableRequestParser.add_argument('order', type=str, help='Sorting order.', default="asc", choices=("asc", "desc"))
tableRequestParser.add_argument('limit', type=int, help='Max number of items in a data-block.', default=60)
tableRequestParser.add_argument('sort', type=str, help='Column to sort by, depends on selected table.', default="index")
tableRequestParser.add_argument('area', type=int, help='Filter for Land(0) or Sea(1) area.', default=-1,
                                choices=(-1, 0, 1))
tableRequestParser.add_argument('filter', type=str, help='Filter fields, depend on selected table.', default="all")
tableRequestParser.add_argument('minimal', type=int, help='Get minimal data output.', default=1, choices=(0, 1))
# TODO: Find a way to document the effects-array in swagger
# tableRequestParser.add_argument('effects', type=int, help='Effects for filtering.', action="split")


tableData = api_.model('tableData', {
    "items": fields.List(fields.Raw),
    "pagination": fields.Nested(paginationData)
})


@api_.expect(tableRequestParser)
class TableView(Resource):
    @api_.marshal_with(tableData, code=200, description="Get table data")
    @api_.response(404, 'Table does not exist.')
    def get(self, table: str):
        if table not in ALLOWED_DATABASE_TABLES:
            abort(404, "Table does not exist.")

        # Get filter from url parameters
        req_args = tableRequestParser.parse_args()
        effects = get_url_parameter("effects", list, [])

        resp = self._get_response(
            table=table,
            current_page=req_args.page,
            order=req_args.order,
            per_page=req_args.limit,
            sort_by=req_args.sort,
            area=req_args.area,
            filter_=req_args.filter,
            minimal=bool(req_args.minimal),
            effects=effects
        )

        return resp, 200

    @cache.memoize(timeout=0)
    def _get_response(
        self,
        table: str,
        current_page: int,
        order: str,
        per_page: int,
        sort_by: str,
        area: int,
        filter_: str,
        minimal: bool,
        effects: typing.List[int],
    ) -> dict:
        # Create query for model
        model = get_model_from_tablename(table)
        query = model.query

        # Apply all sorts of filters, ordering etc.
        query = self._apply_order(query, model, order, sort_by)
        if area != -1:
            query = self._apply_area(query, model, area)
        if filter_ != "all":
            query = self._apply_filter(query, model, filter_)
        if effects:
            query = self._apply_effects(query, model, effects)

        # Create pagination based on query and return in
        pagination_obj = query.paginate(page=current_page,
                                        per_page=per_page)

        return {
            "items": [item.to_dict(minimal=minimal)
                      for item in pagination_obj.items],
            "pagination": {
                "has_next": pagination_obj.has_next,
                "has_previous": pagination_obj.has_prev,
                "labels": list(pagination_obj.iter_pages()),
            }
        }

    def _apply_filter(self, query, model, filter_: str):
        # Filter rating type for monsters
        if match := re.match(r"rating:(\d)$", filter_):
            rating = int(match.group(1))
            return query.filter(model.rating_type == RatingType(rating))

        # Filter class land
        elif match := re.match(r"class_land:(\w)$", filter_):
            class_land = match.group(1)
            return query.filter(model.class_land.contains(class_land))

        # Filter class sea
        elif match := re.match(r"class_sea:(\w)$", filter_):
            class_sea = match.group(1)
            return query.filter(model.class_sea.contains(class_sea))

        # Filter core essences
        elif match := re.match(r"core_essence:(\d)$", filter_):
            core_essence = bool(int(match.group(1)))
            return query.filter(model.is_core_essence == core_essence)

        # Filter essence equip type essences
        elif match := re.match(r"essence_equip:(\d)$", filter_):
            equip_type = EssenceEquipType(int(match.group(1)))
            return query.filter(model.equip_type == equip_type)

        # Filter production type
        elif match := re.match(r"production:(\d)$", filter_):
            production = int(match.group(1))
            return query.filter(
                model.production_type == ProductionType(production))

        # Accessory type
        elif match := re.match(r"accessory:(\d)$", filter_):
            accessory_type = int(match.group(1))
            return query.filter(
                model.accessory_type == AccessoryType(accessory_type))

        # If no filter was matched, but it was not all, just return the query
        # again :shrug:
        return query

    def _apply_effects(self, query, model, effects):
        # Applies a or filter for each bonus code
        for effect_code in effects:
            effect = EffectCode(effect_code)

            query = query.filter(
                or_(
                    model.bonus_1_code == effect,
                    model.bonus_2_code == effect,
                    model.bonus_3_code == effect,
                    model.bonus_4_code == effect,
                    model.bonus_5_code == effect,
                )
            )

        return query

    def _apply_area(self, query, model, area: int):
        try:
            return query.filter(model.area == Area(area))
        except AttributeError:
            return query

    def _apply_order(self, query, model, order: str, sort_by: str):
        try:
            column = getattr(model, sort_by)
        except AttributeError:
            column = getattr(model, "index")

        if order == "asc":
            return query.order_by(column.asc())
        elif order == "desc":
            return query.order_by(column.desc())
