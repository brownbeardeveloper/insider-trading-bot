import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin.exceptions import FirebaseError
import logging


class Firebase:
    def __init__(self) -> None:
        """
        Initializes the instance and sets up the connection to Firestore.

        Raises:
            FirebaseError: If an error occurs while connecting to the Firestore database.
        """
        try:
            if not firebase_admin._apps:
                cred = credentials.Certificate("database-key.json")
                firebase_admin.initialize_app(cred)

            db = firestore.client()  # Initialize Firestore DB
            self.transactions_ref = db.collection("insider-trading").document(
                "transactions"
            )

        except FirebaseError as e:
            logging.error(
                "An error occurred while connecting to the database.\n"
                f"Firebase Error:\n{e}"
            )
            raise FirebaseError(
                "An error occurred while connecting to Database."
                "Please try again later."
            )

    def _read_data(self, company: str) -> list[dict]:
        # Get a specific document from the collection
        collection_ref = self.transactions_ref.collection(company)
        collection = collection_ref.stream()
        collection_list = []

        for data in collection:
            collection_list.append(data)

        return collection_list

    def add_insider_trading_to_db(self, company: str, data_list: list[dict]) -> bool:
        try:
            doc_ref = self.transactions_ref.document(company)
            doc_ref.add(data_list)

        except FirebaseError as e:
            logging.error(
                "An error occurred while connecting to the database.\n"
                f"Firebase Error:\n{e}"
            )
            raise FirebaseError(
                "An error occurred while connecting to Database."
                "Please try again later."
            )


if __name__ == "__main__":
    db = Firebase()
    data = db._read_data(company="nibe")
    print(data)
