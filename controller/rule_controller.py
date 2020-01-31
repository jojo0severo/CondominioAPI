from model.rule import Rule
from setup import db
from sqlalchemy import exc


class RuleController:
    def __init__(self, system_session):
        self.sessions = {system_session}

    def get_rule_by_id(self, rule_id):
        return Rule.query.filter_by(id=rule_id).first()

    def register_rule(self, session, text, condominium_id):
        if session not in self.sessions:
            raise PermissionError

        try:
            rule = Rule(text=text, condominium_id=condominium_id)
            db.session.add(rule)
            db.session.commit()

            return rule

        except exc.IntegrityError:
            db.session.rollback()
            return None

    def remove_rule(self, session, rule_id):
        if session not in self.sessions:
            raise PermissionError

        deleted = Rule.query.filter_by(id=rule_id).delete()
        if deleted:
            db.session.commit()
            return True
        return False
