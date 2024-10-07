from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from shiny import App, render, ui, Inputs, Outputs, Session
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
    with open('randomItems.txt', 'r') as file:
        file_entries = file.readlines()
    return [entry.strip() for entry in file_entries if entry.strip()]

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
    ui.input_action_button("random_button", "Get Random Entry")
)

# Define the server logic for Shiny app
def server(user_input: Inputs, output: Outputs, session: Session):
    @output()
    @render.text()
    def random_entry():
        if user_input.random_button():
            selected_entry = random.choice(entries)
            return selected_entry
        return "Press the button to get a random entry!"

# Create the Shiny app
shiny_app = App(app_ui, server)

# Route to serve only the Shiny app directly, no wrapper HTML
@app.get("/")
async def serve_shiny_app():
    logger.info("Shiny app endpoint accessed")
    return shiny_app  # Serving Shiny app directly without iframe

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
