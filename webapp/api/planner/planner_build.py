from flask import request
from flask_jwt_extended import (current_user,
                                verify_jwt_in_request)
from flask_restx import Resource, abort, fields

from webapp.api.common_api_models import characterClassData
from webapp.extensions import db, api_, AUTH_KEY
from webapp.models.enums import CharacterClass
from webapp.models.tables.planner_build import PlannerBuild, PlannerStar

plannerBuildData = api_.model('plannerBuildData', {
    "id": fields.Integer(description="Unique identifier"),
    "user": fields.Nested(api_.model("userData", {
        "id": fields.Integer,
        "username": fields.String(example="Celty")
    })),
    "created_at": fields.String(example="2022-01-01 11:46:04.204582"),
    "character_class": fields.Nested(characterClassData),
    "build_hash": fields.String(description='Represents which skills / stats are picked for this build.',
                                example="1:0.0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0:0.1:1:0.0:0:0"
                                        ":0:0:0"),
    "build_title": fields.String(example="Initial noble build"),
    "build_description": fields.String(example="Very gud build"),
    "stars": fields.List(fields.Nested(api_.model("starData", {
        "id": fields.Integer,
        "user_id": fields.Integer,
        "created_at": fields.String(example="2022-01-01 11:46:04.204582"),
    })))
})


class PlannerBuildView(Resource):
    @api_.marshal_with(plannerBuildData, code=200, description="Get builds data")
    @api_.response(404, 'Class not found')
    def get(self, classname: str):
        try:
            base_class = getattr(CharacterClass, classname)
        except AttributeError:
            abort(404, 'Class not found')

        query = db.session.query(
            PlannerBuild,
        )

        if base_class == CharacterClass.noble:
            classes = [CharacterClass.noble,
                       CharacterClass.court_magician,
                       CharacterClass.magic_knight]
        elif base_class == CharacterClass.explorer:
            classes = [CharacterClass.explorer,
                       CharacterClass.sniper,
                       CharacterClass.excavator]
        elif base_class == CharacterClass.saint:
            classes = [CharacterClass.saint,
                       CharacterClass.shaman,
                       CharacterClass.priest]
        elif base_class == CharacterClass.mercenary:
            classes = [CharacterClass.mercenary,
                       CharacterClass.gladiator,
                       CharacterClass.guardian_swordsman]
        else:
            classes = [base_class]

        query = query.filter(PlannerBuild.character_class.in_(classes))
        return [build.to_dict() for build in query.all()], 200

    @api_.doc(security=[AUTH_KEY])
    @api_.response(201, '')
    @api_.response(400, '&lt;Error description&gt;')
    @api_.response(401, 'Too many builds')
    def post(self):
        verify_jwt_in_request()

        # Check if user already has more than 20 builds
        user_builds_count = PlannerBuild.query.filter(
            PlannerBuild.user_id == current_user.id).count()

        if user_builds_count > 15:
            abort(401, 'Too many builds.')

        json = request.json

        needed_keys = ["title", "description", "hash", "character_class"]

        if not all(key in json for key in needed_keys):
            abort(400)

        # Check title length > 2, < 100
        if not (2 < len(json["title"].strip()) < 100):
            abort(400, "Title too short")

        if not len(json["description"]) <= 1000:
            abort(400, "Description too long")

        try:
            char_class = CharacterClass(json["character_class"])
        except ValueError:
            abort(400, "Unknown class")

        build = PlannerBuild(
            user_id=current_user.id,
            build_hash=json["hash"],
            build_title=json["title"],
            build_description=json["description"],
            character_class=char_class,
        )
        db.session.add(build)
        db.session.commit()

        return {}, 201

    @api_.doc(security=[AUTH_KEY])
    def delete(self, id: int):
        verify_jwt_in_request()

        build = PlannerBuild.query.get_or_404(id)

        if build.user_id != current_user.id:
            if not current_user.admin:  # allow admins to delete all builds
                abort(401)

        db.session.delete(build)
        db.session.commit()

        return {}, 204


@api_.param('build_id', 'Technical identifier to select a specific build')
class PlannerStarView(Resource):
    @api_.doc(security=[AUTH_KEY])
    @api_.response(201, '')
    @api_.response(409, 'Star already exists')
    def post(self, build_id: int):
        verify_jwt_in_request()

        # Check if already voted on that build
        star = PlannerStar.query.filter(
            PlannerStar.user_id == current_user.id,
            PlannerStar.build_id == build_id,
        ).first()

        if star:
            abort(409, "Star already exists")

        db.session.add(PlannerStar(
            build_id=build_id,
            user_id=current_user.id,
        ))
        db.session.commit()

        return {}, 201

    @api_.doc(security=[AUTH_KEY])
    @api_.response(204, '')
    def delete(self, build_id: int):
        verify_jwt_in_request()

        PlannerStar.query.filter(
            PlannerStar.user_id == current_user.id,
            PlannerStar.build_id == build_id,
        ).delete()

        db.session.commit()

        return {}, 204
