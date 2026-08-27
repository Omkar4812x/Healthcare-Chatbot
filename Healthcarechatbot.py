import os
import sys
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table
from rich.prompt import Prompt

# Load environment variables from .env file
load_dotenv()

console = Console()

SYSTEM_INSTRUCTION = """
You are HealthcareAI, a helpful, empathetic, and knowledgeable healthcare information assistant.

Guidelines:
1. Provide accurate, clear, and easy-to-understand health & wellness information.
2. ALWAYS include a brief safety disclaimer when offering advice: emphasize that you are an AI assistant and not a medical doctor, and your advice is for educational/informational purposes only.
3. If the user presents severe symptoms (e.g., severe chest pain, extreme shortness of breath, sudden numbness, severe bleeding), strongly advise them to seek IMMEDIATE emergency medical assistance (call local emergency services like 911/112/108 or visit an ER).
4. Structure your answers logically using markdown headings, bullet points, and actionable tips when appropriate.
5. Maintain a compassionate, supportive, and professional tone.
"""

generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
}

def setup_gemini_api():
    """Initializes and returns configured Gemini API client."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "YOUR_GEMINI_API_KEY":
        console.print("\n[bold yellow]⚠️ WARNING: GEMINI_API_KEY environment variable not set or contains default placeholder.[/bold yellow]")
        api_key = Prompt.ask("[cyan]Please enter your Gemini API Key (or press Enter to exit)[/cyan]", password=True).strip()
        if not api_key:
            console.print("[bold red]❌ Cannot proceed without a valid API key. Exiting.[/bold red]")
            sys.exit(1)

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        generation_config=generation_config,
        system_instruction=SYSTEM_INSTRUCTION
    )
    return model

def create_chat_session(model):
    """Starts a new chat session with history enabled."""
    return model.start_chat(history=[])

def generate_response(prompt: str, chat_session=None, model=None) -> str:
    """Generates a response using the model or active chat session."""
    try:
        if chat_session:
            response = chat_session.send_message(prompt)
        elif model:
            response = model.generate_content(prompt)
        else:
            return "Error: Neither active chat session nor model was provided."
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"

# Legacy compatibility alias
GenerateResponce = generate_response

def display_banner():
    """Prints a styled ASCII banner and disclaimer."""
    banner = """
  🩺  HEALTHCARE AI CHATBOT  🩺
  =========================================
  Your 24/7 AI guide for wellness, medical info & symptom advice.
    """
    console.print(Panel(banner, style="bold cyan", border_style="bright_blue"))
    console.print(Panel(
        "⚠️ [bold yellow]Medical Disclaimer:[/bold yellow] General educational guidance only. "
        "NOT a substitute for professional diagnosis or emergency care.",
        border_style="yellow"
    ))

def print_help_menu():
    """Displays command list table."""
    table = Table(title="Available CLI Commands", border_style="cyan")
    table.add_column("Command", style="bold green")
    table.add_column("Description", style="white")

    table.add_row("/help", "Show this command reference table")
    table.add_row("/sos", "Display international emergency numbers & hotlines")
    table.add_row("/clear", "Reset active chat conversation history")
    table.add_row("/export", "Export current chat history to a Markdown file")
    table.add_row("exit / quit / q", "Terminate the chatbot session")
    console.print(table)

def print_sos_directory():
    """Displays emergency hotlines panel."""
    sos_text = """
🚨 [bold red]EMERGENCY NUMBERS DIRECTORY[/bold red]
• 🇺🇸/🇨🇦 **US & Canada**: 911
• 🇪🇺/🇬🇧 **EU & UK**: 112 / 999
• 🇮🇳 **India**: 108 / 102
• 🇦🇺 **Australia**: 000
• 🧪 **Poison Control**: 1-800-222-1222
• 🧠 **Mental Health Crisis**: 988
    """
    console.print(Panel(sos_text, title="Emergency Hotline", border_style="red"))

def export_chat_history(messages):
    """Exports conversation to a markdown file."""
    if not messages:
        console.print("[yellow]No chat history to export yet![/yellow]")
        return

    filename = f"chat_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    content = f"# Healthcare AI Chat Export\nDate: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    for msg in messages:
        content += f"### {msg['role'].capitalize()}\n{msg['text']}\n\n"

    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        console.print(f"[bold green]✅ Conversation exported successfully to '{filename}'![/bold green]")
    except Exception as e:
        console.print(f"[bold red]Failed to export chat: {e}[/bold red]")

def main():
    display_banner()
    model = setup_gemini_api()
    chat = create_chat_session(model)
    message_log = []

    console.print("[bold green]Chat initialized! Type '/help' for options or start typing your question below.[/bold green]\n")

    while True:
        try:
            user_input = Prompt.ask("\n[bold cyan]You[/bold cyan]").strip()
            if not user_input:
                continue

            cmd = user_input.lower()
            if cmd in ["exit", "quit", "q"]:
                console.print("\n[bold cyan]Thank you for using Healthcare Chatbot. Stay healthy! 👋[/bold cyan]\n")
                break
            elif cmd == "/help":
                print_help_menu()
                continue
            elif cmd == "/sos":
                print_sos_directory()
                continue
            elif cmd == "/clear":
                chat = create_chat_session(model)
                message_log.clear()
                console.print("\n[bold yellow]🔄 Chat history successfully reset![/bold yellow]\n")
                continue
            elif cmd == "/export":
                export_chat_history(message_log)
                continue

            message_log.append({"role": "User", "text": user_input})

            with console.status("[bold green]HealthcareAI is thinking...", spinner="dots"):
                response_text = generate_response(user_input, chat_session=chat, model=model)

            message_log.append({"role": "HealthcareAI", "text": response_text})

            console.print("\n[bold green]HealthcareAI:[/bold green]")
            console.print(Markdown(response_text))
            console.print("-" * 60)

        except KeyboardInterrupt:
            console.print("\n\n[bold yellow]Session terminated. Stay healthy! 👋[/bold yellow]\n")
            break
        except Exception as e:
            console.print(f"\n[bold red]❌ An error occurred: {e}[/bold red]\n")

if __name__ == "__main__":
    main()