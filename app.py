from shiny import App, render, ui
import random

# Load entries from a text file
def load_entries():
    with open('randomItems.txt', 'r') as file:
        entries = file.readlines()
    return [entry.strip() for entry in entries if entry.strip()]

entries = load_entries()

app_ui = ui.page_fluid(
    ui.input_action_button("random_button", "Get Random Entry"),
    ui.output_text("random_entry")
)

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

app = App(app_ui, server)

if __name__ == "__main__":
    app.run()