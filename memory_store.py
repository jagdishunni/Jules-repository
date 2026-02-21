import os
import json
from google.cloud import firestore

class MemoryManager:
    def __init__(self, project_id=None):
        try:
            # Check if we are in a testing environment without credentials
            if not os.environ.get('GOOGLE_APPLICATION_CREDENTIALS') and not project_id:
                print("Warning: No Firestore credentials found. Using in-memory mock.")
                self.db = None
                self.mock_store = {
                    'concepts': [],
                    'claims': [],
                    'narrative_shifts': []
                }
            else:
                self.db = firestore.Client(project=project_id)
                self.mock_store = None
        except Exception as e:
            print(f"Warning: Could not initialize Firestore client: {e}. Using in-memory mock.")
            self.db = None
            self.mock_store = {
                'concepts': [],
                'claims': [],
                'narrative_shifts': []
            }

    def get_active_concepts(self):
        """Retrieve concepts with an 'Accelerating' status."""
        if self.db:
            try:
                concepts_ref = self.db.collection('concepts')
                # Correctly query where status == 'Accelerating'
                query = concepts_ref.where(field_path='status', op_string='==', value='Accelerating')
                results = query.stream()
                return [doc.to_dict() for doc in results]
            except Exception as e:
                print(f"Error retrieving active concepts: {e}")
                return []
        else:
            # Mock behavior
            return [c for c in self.mock_store['concepts'] if c.get('status') == 'Accelerating']

    def update_memory(self, new_insights):
        """Write back new concept entities, claims, and narrative shifts."""
        if self.db:
            try:
                batch = self.db.batch()

                if 'concepts' in new_insights:
                    concepts_ref = self.db.collection('concepts')
                    for concept in new_insights['concepts']:
                        doc_ref = concepts_ref.document(concept.get('id', concept.get('name')))
                        batch.set(doc_ref, concept, merge=True)

                if 'claims' in new_insights:
                    claims_ref = self.db.collection('claims')
                    for claim in new_insights['claims']:
                        new_claim_ref = claims_ref.document()
                        # Ensure claim is a dict
                        claim_data = claim if isinstance(claim, dict) else {'text': claim}
                        batch.set(new_claim_ref, claim_data)

                if 'shifts' in new_insights:
                    shifts_ref = self.db.collection('narrative_shifts')
                    for shift in new_insights['shifts']:
                        new_shift_ref = shifts_ref.document()
                        # Ensure shift is a dict
                        shift_data = shift if isinstance(shift, dict) else {'text': shift}
                        batch.set(new_shift_ref, shift_data)

                batch.commit()
                print("Memory updated successfully (Firestore).")

            except Exception as e:
                print(f"Error updating memory: {e}")
        else:
            # Mock behavior
            if 'concepts' in new_insights:
                for concept in new_insights['concepts']:
                    # Simple update or append for mock
                    existing = next((c for c in self.mock_store['concepts'] if c.get('name') == concept.get('name')), None)
                    if existing:
                        existing.update(concept)
                    else:
                        self.mock_store['concepts'].append(concept)

            if 'claims' in new_insights:
                self.mock_store['claims'].extend(new_insights['claims'])

            if 'shifts' in new_insights:
                self.mock_store['narrative_shifts'].extend(new_insights['shifts'])

            print("Memory updated successfully (Mock).")
