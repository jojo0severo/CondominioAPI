from model.rule import Rule
from setup import db
from sqlalchemy import exc


class RuleController:
    def get_rule_by_id(self, rule_id):
        rule = Rule.query.get(rule_id)
        if not rule:
            raise ReferenceError

        return rule

    def register_rule(self, text, condominium_id):
        try:
            rule = Rule(text=text, condominium_id=condominium_id)
            db.session.add(rule)
            db.session.commit()

            return rule.id

        except exc.IntegrityError:
            db.session.rollback()
            return None

    def remove_rule(self, rule_id):
        rule = Rule.query.get(rule_id)
        if not rule:
            raise ReferenceError

        db.session.delete(rule)
        db.session.commit()
