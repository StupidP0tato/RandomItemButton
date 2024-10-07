from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from shiny import App, render, ui
import random
import os

# Print current directory and static files
print("Current directory:", os.getcwd())
print("Static files:", os.listdir('static'))
print(os.path.isfile("static/ChestSymbol.png"))

# Create FastAPI app
app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load entries from a text file
def load_entries():
    with open('randomItems.txt', 'r') as file:
        entries = file.readlines()
    return [entry.strip() for entry in entries if entry.strip()]

entries = load_entries()

# Define the Shiny UI
app_ui = ui.page_fluid(
    ui.HTML("""
    <link rel="stylesheet" href="/static/styles.css">
    """),
    # Only keep the image that acts as a button
    ui.HTML(
        '<img src="/static/ChestSymbol.png" style="width: 200px; height: auto; cursor: pointer;" onclick="document.getElementById(\'random_button\').click();">'
    ),
    ui.output_text("random_entry")
)

# Define the server logic
def server(input, output, session):
    @output()
    @render.text()  # Updated to use render.text()
    def random_entry():
        print("Button pressed")  # Debug statement
        if input.random_button():  # Call the function to check if button was pressed
            selected_entry = random.choice(entries)
            print(f"Selected entry: {selected_entry}")  # Debug statement
            return selected_entry
        return "Press the button to get a random entry!"

# Create and run the Shiny app
shiny_app = App(app_ui, server)

# Route for the Shiny app
@app.get("/", response_class=shiny_app)
async def read_root():
    return shiny_app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
