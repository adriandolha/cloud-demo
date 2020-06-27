import covid19_symptoms
from covid19_symptoms.repo import transaction


class SymptomService:
    def __init__(self, app_context: covid19_symptoms.AppContext):
        self._app_context = app_context

    @transaction
    def get(self, id=None):
        return self._app_context.symptom_repo.get(id)

    @transaction
    def save(self, data_records):
        saved_records = []
        for record in data_records:
            saved_records.append(self._app_context.symptom_repo.save(record))
        return {'items': saved_records, 'total': len(saved_records)}
