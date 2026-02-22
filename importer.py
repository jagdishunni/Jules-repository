import pandas as pd
from google.cloud import firestore

def import_influencers(csv_file='AI influencers for jules - Sheet1.csv', project_id='ai-newsletter-bot-487018'):
    # Initialize Firestore
    try:
        db = firestore.Client(project=project_id)
    except Exception as e:
        print(f"Warning: Could not initialize Firestore client: {e}")
        return

    try:
        # Read CSV
        df = pd.read_csv(csv_file)

        influencers_ref = db.collection('influencers')

        for index, row in df.iterrows():
            name = row['Name']
            handle = row['Twitter/X Handle']

            # Strip '@' from handle
            if handle.startswith('@'):
                handle = handle[1:]

            # Create document
            doc_ref = influencers_ref.document(name)
            doc_ref.set({
                'handle': handle
            })
            print(f"Imported {name} with handle {handle}")

        print("Import complete.")

    except FileNotFoundError:
        print(f"Error: CSV file '{csv_file}' not found.")
    except Exception as e:
        print(f"Error importing influencers: {e}")

if __name__ == "__main__":
    import_influencers()
