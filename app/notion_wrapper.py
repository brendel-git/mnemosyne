from notion_client import Client

class NotionClientWrapper:
    """
    Wrapper around Notion API for inserting summaries into a database.
    """

    def __init__(self, api_key: str, db_id: str):
        self.client = Client(auth=api_key)
        self.db_id = db_id
        self.data_source_id = self._get_data_source_id()

    def _get_data_source_id(self) -> str:
        """Fetch the first data_source_id for this database."""
        db = self.client.databases.retrieve(database_id=self.db_id)
        return db["data_sources"][0]["id"]
    
    def add_entry(self, title: str, summary: str):
        """
        Add an entry to the Notion database.
        Args:
            title (str): entry title
            summary (str): summary text
        """
        self.client.pages.create(
            parent={"type": "data_source_id", "data_source_id": self.data_source_id},
            properties={
                "Title": {
                    "title": [{"text": {"content": title or "Mnemosyne Entry"}}]
                },
                "Summary": {
                    "rich_text": [{"text": {"content": summary[:1900]}}]
                }
            }
        )
