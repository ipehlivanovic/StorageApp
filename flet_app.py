import flet as ft
import requests

# API base URL (your FastAPI server)
API_BASE_URL = "http://localhost:8000"
TITLE = "Storage Tracker"


def main(page: ft.Page):
    # Definition of basic page settings
    page.title = TITLE
    page.padding = 20
    page.appbar = ft.AppBar(
        title=ft.Text(TITLE),
        center_title=True
    )

    load_items(page)

    page.update()


def load_items(page):
    """Fetch all items from the API and display them."""
    # Clear the page before loading items
    page.controls.clear()
    status_text = ft.Text("Loading...", size=16)
    page.add(status_text)

    try:
        # Fetch items from database
        response = requests.get(f"{API_BASE_URL}/items/")
        items = response.json()

        # Clear the "Loading..." message
        page.controls.clear()

        # Create a container for items
        items_column = ft.Column([])  # Empty column
        page.add(
            ft.Text("Your Pantry", size=18, weight=ft.FontWeight.BOLD),
            items_column,
        )

        # Build a list of Text controls containing items
        items_column.controls = []  # Clear
        for item in items:
            text = f"{item['name']} - {item['quantity']} {item['unit']}"
            card = ft.Container(
                content=ft.Text(text),
                padding=10,
                bgcolor=ft.Colors.DEEP_PURPLE_500,
                border_radius=10
            )
            items_column.controls.append(card)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    print("🚀 Starting Flet Desktop app...")
    ft.app(target=main, view=ft.AppView.FLET_APP)
