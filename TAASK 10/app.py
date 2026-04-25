from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# Knowledge base for University Admission Chatbot
ADMISSION_DATA = {
    "programs": {
        "computer_science": {
            "name": "Bachelor of Computer Science",
            "duration": "4 years",
            "requirements": [
                "High School Diploma or equivalent",
                "Minimum GPA: 3.0",
                "SAT Score: 1200+ or ACT Score: 26+",
                "English proficiency (TOEFL 80+ for international)",
                "Letters of recommendation (3)"
            ],
            "deadline": "January 15, 2025",
            "tuition": "$25,000 per year",
            "specializations": ["AI/ML", "Cybersecurity", "Software Engineering", "Data Science"]
        },
        "business": {
            "name": "Bachelor of Business Administration",
            "duration": "4 years",
            "requirements": [
                "High School Diploma or equivalent",
                "Minimum GPA: 2.8",
                "SAT Score: 1100+ or ACT Score: 24+",
                "Personal statement",
                "Letters of recommendation (2)"
            ],
            "deadline": "February 1, 2025",
            "tuition": "$22,000 per year",
            "specializations": ["Finance", "Marketing", "Management", "Entrepreneurship"]
        },
        "engineering": {
            "name": "Bachelor of Engineering",
            "duration": "4 years",
            "requirements": [
                "High School Diploma or equivalent",
                "Minimum GPA: 3.2",
                "Advanced Math (Pre-Calculus or higher)",
                "Physics and Chemistry courses",
                "SAT Score: 1250+ or ACT Score: 28+",
                "Letters of recommendation (3)"
            ],
            "deadline": "December 31, 2024",
            "tuition": "$28,000 per year",
            "specializations": ["Civil", "Mechanical", "Electrical", "Software"]
        },
        "nursing": {
            "name": "Bachelor of Science in Nursing",
            "duration": "4 years",
            "requirements": [
                "High School Diploma or equivalent",
                "Minimum GPA: 3.1",
                "Biology and Chemistry courses",
                "SAT Score: 1150+ or ACT Score: 25+",
                "Health screening",
                "Letters of recommendation (2)",
                "Personal essay on healthcare goals"
            ],
            "deadline": "March 1, 2025",
            "tuition": "$26,000 per year",
            "specializations": ["Pediatrics", "Critical Care", "Mental Health", "Community Health"]
        }
    },
    "general_info": {
        "application_fee": "$75",
        "early_admission_deadline": "November 1, 2024",
        "regular_admission_deadline": "January 15, 2025",
        "late_admission_deadline": "March 1, 2025",
        "acceptance_rate": "65%",
        "average_gpa": "3.4",
        "campus_location": "Central City, USA",
        "contact_email": "admissions@university.edu",
        "contact_phone": "(555) 123-4567"
    }
}

# Chatbot responses
def get_chatbot_response(user_message):
    """Generate chatbot response based on user query"""
    message = user_message.lower().strip()
    
    # Greeting responses
    if any(word in message for word in ["hello", "hi", "hey", "greetings"]):
        return "Hello! 👋 Welcome to our University Admissions Chatbot. I can help you with information about our programs, admission requirements, deadlines, and more. What would you like to know?"
    
    # Programs list
    if any(word in message for word in ["programs", "majors", "degrees", "courses"]):
        programs_list = ", ".join([ADMISSION_DATA["programs"][p]["name"] for p in ADMISSION_DATA["programs"]])
        return f"We offer the following programs:\n\n{programs_list}\n\nWould you like more details about any specific program?"
    
    # Requirements
    if "requirement" in message:
        if "computer science" in message or "cs" in message:
            program = ADMISSION_DATA["programs"]["computer_science"]
            return format_program_response(program)
        elif "business" in message or "bba" in message:
            program = ADMISSION_DATA["programs"]["business"]
            return format_program_response(program)
        elif "engineering" in message or "engineer" in message:
            program = ADMISSION_DATA["programs"]["engineering"]
            return format_program_response(program)
        elif "nursing" in message:
            program = ADMISSION_DATA["programs"]["nursing"]
            return format_program_response(program)
        else:
            return "I'd like to know which program you're interested in. We have:\n- Computer Science\n- Business Administration\n- Engineering\n- Nursing\n\nWhich one would you like to learn about?"
    
    # Deadlines
    if "deadline" in message:
        general = ADMISSION_DATA["general_info"]
        return f"📅 Application Deadlines:\n\n- Early Admission: {general['early_admission_deadline']}\n- Regular Admission: {general['regular_admission_deadline']}\n- Late Admission: {general['late_admission_deadline']}\n\nNote: Some programs have earlier deadlines. Would you like details about a specific program?"
    
    # Tuition/Fees
    if any(word in message for word in ["tuition", "fee", "cost", "price", "payment"]):
        response = f"💰 Tuition and Fees:\n\n"
        response += f"Application Fee: ${ADMISSION_DATA['general_info']['application_fee']}\n\n"
        response += "Annual Tuition by Program:\n"
        for prog_key, prog in ADMISSION_DATA["programs"].items():
            response += f"• {prog['name']}: {prog['tuition']}\n"
        return response
    
    # Contact information
    if any(word in message for word in ["contact", "phone", "email", "address"]):
        general = ADMISSION_DATA["general_info"]
        return f"📞 Contact Us:\n\nEmail: {general['contact_email']}\nPhone: {general['contact_phone']}\nCampus Location: {general['campus_location']}\n\nFeel free to reach out if you have any questions!"
    
    # Statistics
    if any(word in message for word in ["statistics", "stats", "acceptance", "average", "gpa"]):
        general = ADMISSION_DATA["general_info"]
        return f"📊 University Statistics:\n\n- Acceptance Rate: {general['acceptance_rate']}\n- Average GPA: {general['average_gpa']}\n\nWould you like more information about any specific program?"
    
    # Default response
    return "I'm here to help with information about our university programs, admission requirements, and deadlines. You can ask me about:\n- Available programs\n- Admission requirements\n- Application deadlines\n- Tuition and fees\n- Contact information\n\nWhat would you like to know?"

def format_program_response(program):
    """Format program information in a readable way"""
    response = f"📚 {program['name']}\n\n"
    response += f"Duration: {program['duration']}\n"
    response += f"Annual Tuition: {program['tuition']}\n"
    response += f"Application Deadline: {program['deadline']}\n\n"
    response += "Requirements:\n"
    for req in program['requirements']:
        response += f"• {req}\n"
    response += f"\nSpecializations: {', '.join(program['specializations'])}\n"
    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Empty message'}), 400
        
        # Get chatbot response
        bot_response = get_chatbot_response(user_message)
        
        return jsonify({'response': bot_response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/programs', methods=['GET'])
def get_programs():
    """Get list of all programs"""
    programs_list = []
    for key, program in ADMISSION_DATA["programs"].items():
        programs_list.append({
            'id': key,
            'name': program['name'],
            'tuition': program['tuition'],
            'deadline': program['deadline']
        })
    return jsonify(programs_list)

@app.route('/program/<program_id>', methods=['GET'])
def get_program(program_id):
    """Get detailed information about a specific program"""
    if program_id in ADMISSION_DATA["programs"]:
        return jsonify(ADMISSION_DATA["programs"][program_id])
    return jsonify({'error': 'Program not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
