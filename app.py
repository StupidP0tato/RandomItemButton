from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from shiny import App, render, ui
import random
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Print current directory and static files
logger.info("Current directory: %s", os.getcwd())
logger.info("Static files: %s", os.listdir('static'))
logger.info("ChestSymbol.png exists: %s", os.path.isfile("static/ChestSymbol.png"))
logger.info("styles.css exists: %s", os.path.isfile("static/styles.css"))

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
    ui.output_text("random_entry"),
    ui.button_input("random_button", "Get Random Entry")  # Adding a button for interaction
)

# Define the server logic
def server(input, output, session):
    @output()
    @render.text()
    def random_entry():
        logger.info("Button pressed")
        if input.random_button():
            selected_entry = random.choice(entries)
            logger.info("Selected entry: %s", selected_entry)
            return selected_entry
        return "Press the button to get a random entry!"

# Create the Shiny app
shiny_app = App(app_ui, server)

# Route for the Shiny app
@app.get("/")
async def read_root():
    logger.info("Root endpoint accessed")
    return shiny_app  # Return the shiny app instance itself, FastAPI will handle it correctly

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
