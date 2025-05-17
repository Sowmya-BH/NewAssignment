Here's a comprehensive README.md file for your project:

```markdown
# Nexus.AI Chatbot with Authentication

![Nexus.AI Logo](https://via.placeholder.com/150x50?text=Nexus.AI) *(Replace with actual logo)*

A secure, multi-LLM chatbot application with email-based authentication and conversation history.

## Features

- 🔒 **Simple Email Authentication** (No password required)
- 💬 **Multi-LLM Chat Interface** (Gemini, Groq)
- 🧠 **Conversation Memory** (Save/Load chat sessions)
- ⚡ **Streaming Responses** (Real-time AI responses)
- 📚 **Session History** (Track past conversations)
- 🛢️ **Text-to-SQL Conversion** (Natural language to SQL queries)

## Project Structure

```
nexus-ai/
├── README.md
├── app.py               # Main authentication application
├── pages/
│   └── myapp.py         # Chatbot application
└── users.db             # SQLite database (auto-created)
```

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/nexus-ai.git
   cd nexus-ai
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.streamlit/secrets.toml` file with your API keys:
   ```toml
   GOOGLE_API_KEY = "your_google_api_key"
   GROQ_API_KEY = "your_groq_api_key"
   ```

## Usage

### Authentication System

1. **Run the application**
   ```bash
   streamlit run app.py
   ```

2. **Authentication Flow**
   - Register with just your email (username optional)
   - Login with your registered email
   - No password required

### Chatbot Features

- **Switch between LLM providers** (Gemini/Groq)
- **Save conversation history**
- **Load previous sessions**
- **Adjust memory length**

## API Requirements

| Provider | API Key Required |
|----------|------------------|
| Gemini   | ✅ Yes           |
| Groq     | ✅ Yes           |

## Configuration

Edit `app.py` to modify:
- Database name/location
- Email validation rules
- Session timeout settings

Edit `pages/myapp.py` to modify:
- Available LLM providers
- System prompt
- Memory settings
- UI elements

## Screenshots

*(Add actual screenshots here)*

1. **Login Screen**
   ![Login Screen](screenshots/login.png)

2. **Chat Interface**
   ![Chat Interface](screenshots/chat.png)

3. **Session History**
   ![History](screenshots/history.png)

## Troubleshooting

**Common Issues:**

1. **"Email not found" error**
   - Ensure you've registered first
   - Check database connection in `users.db`

2. **API errors in chat**
   - Verify API keys in `secrets.toml`
   - Check provider status pages

3. **Session not saving**
   - Ensure you click "Save Current Chat"
   - Check browser cookie settings

## License

MIT License - See [LICENSE](LICENSE) for details.

---

**Note:** This application stores user emails in a local SQLite database. For production use, features to be added:
- Password authentication
- Email verification
- Proper user role management
```



