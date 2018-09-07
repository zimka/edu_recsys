from collections import namedtuple
Rule = namedtuple("Rule", ['title', 'check'])
QUESTIONS_GUID_RULE_SETS = {

}


class Check:
    def __init__(self, uuid, answers, guid):
        self.uuid = uuid
        self.answers = answers
        self.guid_rule_set = QUESTIONS_GUID_RULE_SETS.get(guid, {})


    @classmethod
    def from_results(cls, result, guid):
        try:
            return cls(result['question']['uuid'], result['answers'])
        except:
            return Check(None, [], None)

    def _is_valid(self):

        known_uuid = self.uuid in self.guid_rule_set
        has_answers = len(self.answers)
        return known_uuid and has_answers

    def is_correct(self):
        return self.guid_rule_set[self.uuid](self.answers)

