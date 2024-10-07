from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from shiny import App, render, ui
import random
import os

# Print current directory and static files
print("Current directory:", os.getcwd())
print("Static files:", os.listdir('static'))
print(os.path.isfile("static/ChestSymbol.png"))
print(os.path.isfile("static/styles.css"))  # Check for the styles.css file

# Create FastAPI app
app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load entries from a text file
def load_entries():
    if os.path.isfile('randomItems.txt'):
        with open('randomItems.txt', 'r') as file:
            entries = file.readlines()
        return [entry.strip() for entry in entries if entry.strip()]
    return []  # Return an empty list if the file does not exist

entries = load_entries()

# Define the Shiny UI
app_ui = ui.page_fluid(
    ui.HTML("""
    <link rel="stylesheet" href="/static/styles.css">
    """),
    ui.HTML(
        '<img src="/static/ChestSymbol.png" style="width: 200px; height: auto; cursor: pointer;" onclick="document.getElementById(\'random_button\').click();">'
    ),
    ui.output_text("random_entry")
)

# Define the server logic
def server(input, output, session):
    @output()
    @render.text()
    def random_entry():
        print("Button pressed")
        if input.random_button():
            selected_entry = random.choice(entries)
            print(f"Selected entry: {selected_entry}")
            return selected_entry
        return "Press the button to get a random entry!"

# Create and run the Shiny app
shiny_app = App(app_ui, server)

# Route for the Shiny app
@app.get("/", response_class=ui.HTML)
async def read_root():
    return shiny_app

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
