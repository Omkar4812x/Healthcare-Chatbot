import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file if available
load_dotenv()

# Retrieve API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key or api_key == "YOUR_GEMINI_API_KEY":
    print("\n⚠️ WARNING: GEMINI_API_KEY environment variable not set or contains default placeholder.")
    print("Please set your GEMINI_API_KEY in a .env file or environment variable.\n")
    api_key = input("Enter your Gemini API Key (or press Enter to skip if configured in system): ").strip()
    if not api_key:
        print("❌ Cannot proceed without a valid API key. Exiting.")
        sys.exit(1)

genai.configure(api_key=api_key)

# System prompt guidelines for Healthcare Chatbot
SYSTEM_INSTRUCTION = """
You are HealthcareAI, a helpful, empathetic, and knowledgeable healthcare information assistant.

Guidelines:
1. Provide accurate, clear, and easy-to-understand health & wellness information.
2. ALWAYS include a brief safety disclaimer when offering advice: emphasize that you are an AI assistant and not a medical doctor, and your advice is for educational/informational purposes only.
3. If the user presents severe symptoms (e.g., severe chest pain, extreme shortness of breath, sudden numbness, severe bleeding), strongly advise them to seek IMMEDIATE emergency medical assistance (call local emergency services like 911 or visit an ER).
4. Structure your answers logically using markdown headings, bullet points, and actionable tips when appropriate.
5. Maintain a compassionate, supportive, and professional tone.
"""

generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config,
    system_instruction=SYSTEM_INSTRUCTION
)

def create_chat_session():
    """Starts a new chat session with history enabled."""
    return model.start_chat(history=[])

# Main chat generation helper (maintaining backward-compatible function name)
def generate_response(prompt: str, chat_session=None) -> str:
    """Generates a response using the model or active chat session."""
    try:
        if chat_session:
            response = chat_session.send_message(prompt)
        else:
            response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"

# Alias for legacy compatibility
GenerateResponce = generate_response

def main():
    print("=" * 60)
    print("🩺 WELCOME TO HEALTHCARE CHATBOT")
    print("=" * 60)
    print("⚠️ Disclaimer: This bot provides general health information only.")
    print("   For emergencies or medical diagnosis, consult a healthcare professional.")
    print("-" * 60)
    print("Commands: Type 'exit', 'quit', or 'q' to end. Type '/clear' to reset chat.")
    print("=" * 60 + "\n")

    chat = create_chat_session()

    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue

            if user_input.lower() in ["exit", "quit", "q"]:
                print("\nThank you for using Healthcare Chatbot. Stay healthy! 👋\n")
                break

            if user_input.lower() == "/clear":
                chat = create_chat_session()
                print("\n🔄 Chat session history cleared!\n")
                continue

            print("\nBot: ", end="", flush=True)
            response_text = generate_response(user_input, chat_session=chat)
            print(response_text)
            print("-" * 60 + "\n")

        except KeyboardInterrupt:
            print("\n\nGoodbye! Stay healthy! 👋\n")
            break
        except Exception as e:
            print(f"\n❌ An error occurred: {e}\n")

if __name__ == "__main__":
    main()