from model.rule import Rule
from setup import db
from sqlalchemy import exc


class RuleController:
    def get_rule_by_id(self, rule_id):
        return Rule.query.get(rule_id)

    def register_rule(self, text, condominium_id):
        try:
            rule = Rule(text=text, condominium_id=condominium_id)
            db.session.add(rule)
            db.session.commit()

            return rule.id

        except exc.IntegrityError:
            db.session.rollback()
            return None

    def remove_rule(self, rule):
        try:
            db.session.delete(rule)
            db.session.commit()

            return True

        except exc.IntegrityError:
            db.session.rollback()
            return False
