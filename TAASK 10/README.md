# University Admission Chatbot

A web-based chatbot application that provides information about university admissions, programs, requirements, and deadlines.

## Features

✨ **Intelligent Chatbot**
- Natural language processing for admission-related queries
- Provides information about multiple university programs
- Answers questions about admission requirements
- Displays application deadlines
- Shares tuition and fee information
- Offers contact details

🎓 **Programs Supported**
- Bachelor of Computer Science
- Bachelor of Business Administration
- Bachelor of Engineering
- Bachelor of Science in Nursing

📚 **Information Provided**
- Program details and specializations
- Admission requirements for each program
- Application deadlines and fees
- Tuition costs
- University statistics
- Contact information

## Project Structure

```
├── app.py                 # Flask backend application
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Main chatbot interface
└── static/
    ├── style.css         # CSS styling
    └── script.js         # Frontend JavaScript
```

## Installation

1. **Clone or download the project**
   ```bash
   cd "TAASK 10"
   ```

2. **Create a virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # source venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. **Start the Flask server**
   ```bash
   python app.py
   ```

2. **Open in browser**
   - Navigate to `http://localhost:5000` in your web browser

3. **Start chatting!**
   - Ask the chatbot about programs, requirements, deadlines, or any admission-related questions

## Usage Examples

Try asking the chatbot:
- "Tell me about your programs"
- "What are the admission requirements for Computer Science?"
- "When is the application deadline?"
- "How much is the tuition?"
- "What is your contact information?"
- "What are your specializations in Engineering?"

## API Endpoints

- **GET `/`** - Main chatbot interface
- **POST `/chat`** - Send a message and get a response
  - Request: `{"message": "user message"}`
  - Response: `{"response": "bot response"}`
- **GET `/programs`** - Get list of all programs
- **GET `/program/<program_id>`** - Get details about a specific program

## Features

### Frontend
- Clean, modern chat interface
- Real-time message sending
- Loading indicators
- Quick action buttons for common queries
- Responsive design (works on mobile and desktop)
- Smooth animations and transitions

### Backend
- Natural language understanding for admission queries
- Comprehensive knowledge base with program information
- RESTful API endpoints
- Error handling

## Customization

### Adding New Programs
Edit `app.py` and add new entries to the `ADMISSION_DATA["programs"]` dictionary.

### Modifying Chat Responses
Edit the `get_chatbot_response()` function in `app.py` to customize responses.

### Styling
Edit `static/style.css` to customize the appearance.

## Technologies Used

- **Backend**: Python, Flask
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Communication**: RESTful API with JSON

## Browser Compatibility

- Chrome/Edge (Latest)
- Firefox (Latest)
- Safari (Latest)
- Mobile browsers

## License

This project is created for educational purposes.

## Support

For questions or issues, contact: admissions@university.edu
