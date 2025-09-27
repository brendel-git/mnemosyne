from notion_client import Client

class NotionClientWrapper:
    def __init__(self, api_key: str, db_id: str):
        self.client = Client(auth=api_key)
        self.db_id = db_id

    def add_entry(self, title: str, summary: str):
        # Your DB must have properties "Title" (title) and "Summary" (rich_text)
        self.client.pages.create(
            parent={"database_id": self.db_id},
            properties={
                "Title":   {"title": [{"text": {"content": title or "Mnemosyne Entry"}}]},
                "Summary": {"rich_text": [{"text": {"content": summary[:1900]}}]},
            },
        )
