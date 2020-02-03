from model.rule import Rule
from setup import db
from sqlalchemy import exc


class RuleController:
    def __init__(self, system_session):
        self.system_session_key = system_session
        self.session_keys = {system_session}

    def get_rule_by_id(self, rule_id):
        return Rule.query.get(rule_id)

    def register_rule(self, session_key, text, condominium_id):
        if session_key not in self.session_keys:
            raise PermissionError

        try:
            rule = Rule(text=text, condominium_id=condominium_id)
            db.session.add(rule)
            db.session.commit()

            return rule

        except exc.IntegrityError:
            db.session.rollback()
            return None

    def remove_rule(self, session_key, rule_id):
        if session_key not in self.session_keys:
            raise PermissionError

        rule = Rule.query.get(rule_id)
        if rule is not None:
            db.session.delete(rule)
            db.session.commit()
            return True
        return False

    def drop_session(self, session_key):
        if session_key not in self.session_keys or session_key == self.system_session_key:
            raise ValueError

        self.session_keys.remove(session_key)
        return True
