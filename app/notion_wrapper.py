from notion_client import Client

class NotionClientWrapper:
    """
    Wrapper around Notion API for inserting summaries into a database.
    """

    def __init__(self, api_key: str, db_id: str):
        self.client = Client(auth=api_key)
        self.db_id = db_id

    def add_entry(self, title: str, summary: str):
        """
        Add an entry to the Notion database.
        Args:
            title (str): entry title
            summary (str): summary text
        """
        self.client.pages.create(
            parent={"database_id": self.db_id},
            properties={
                "Title": {
                    "title": [{"text": {"content": title or "Mnemosyne Entry"}}]
                },
                "Summary": {
                    "rich_text": [{"text": {"content": summary[:1900]}}]
                }
            }
        )
