# 🚀 AI Calendar Assistant

A stunning, modern calendar management application with an AI-powered assistant that helps you schedule, manage, and organize your appointments with Google Calendar integration.

## ✨ Features

- **🎨 Ultra-Modern UI**: Flashy colors, glassmorphism effects, and smooth animations
- **🤖 AI-Powered**: Intelligent calendar management using OpenAI GPT-4
- **📅 Google Calendar Integration**: Seamless booking and scheduling
- **💫 Real-time Chat Interface**: Interactive conversation with the AI assistant
- **🎭 Responsive Design**: Works perfectly on desktop and mobile devices
- **⚡ Fast Performance**: Built with FastAPI and Streamlit

## 🎨 Design Highlights

### Visual Features
- **Animated Gradient Background**: Dynamic color shifts with smooth transitions
- **Neon Glow Effects**: Eye-catching text and button animations
- **Glassmorphism**: Modern translucent containers with blur effects
- **Floating Elements**: Animated background orbs for visual appeal
- **Custom Typography**: Google Fonts (Poppins & Orbitron) for modern look
- **Interactive Elements**: Hover effects, scale animations, and smooth transitions

### Color Palette
- **Primary**: Electric Blue (#00ffff) and Hot Pink (#ff00ff)
- **Secondary**: Purple (#764ba2), Orange (#f5576c), Teal (#4ecdc4)
- **Background**: Multi-color gradient with animated shifts
- **Text**: Pure white with neon glow effects

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- Google Calendar API credentials
- OpenAI API key

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Assignment
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_APPLICATION_CREDENTIALS=path_to_your_credentials.json
```

### 5. Google Calendar Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google Calendar API
4. Create service account credentials
5. Download the JSON credentials file
6. Place it in your project directory
7. Run the authentication script:
```bash
python src/google_calendar_utils.py
```

## 🚀 Running the Application

### 1. Start the Backend (FastAPI)
```bash
python main.py
```
The backend will be available at `http://localhost:8000`

### 2. Start the Frontend (Streamlit)
```bash
streamlit run app.py
```
The frontend will be available at `http://localhost:8501`

## 🎯 Usage

1. **Open the Application**: Navigate to `http://localhost:8501`
2. **Start Chatting**: Type your calendar requests in natural language
3. **Examples**:
   - "Schedule a meeting tomorrow at 2 PM"
   - "What's my schedule for this week?"
   - "Book a 30-minute call with John on Friday"
   - "Show me my free time next week"

## 🏗️ System Architecture

The application is built with a decoupled frontend and backend architecture, ensuring scalability and maintainability.

-   **Frontend**: A modern and interactive user interface built with **Streamlit**. It's responsible for capturing user input and displaying the conversation in a real-time chat interface.

-   **Backend**: A high-performance backend server powered by **FastAPI**. It exposes API endpoints that the frontend consumes. It handles the core logic of the application.

-   **AI Agent**: At the heart of the backend is an intelligent AI agent built with **LangGraph**. This agent manages the conversational flow, understands user intent, and orchestrates the necessary tools to fulfill user requests.

-   **Tools**: The agent uses a set of tools for specific tasks, primarily for interacting with Google Calendar. These tools are responsible for checking availability, booking appointments, and retrieving schedule information.

-   **Google Calendar Integration**: A utility module handles the communication with the Google Calendar API, including authentication (OAuth 2.0) and data exchange.




## 🎨 UI Components

### Frontend (Streamlit)
- **Glassmorphism Container**: Translucent main content area
- **Animated Title**: Neon glow effect with Orbitron font
- **Modern Input Field**: Rounded with focus animations
- **Gradient Button**: Multi-color animated send button
- **Chat Bubbles**: Different styles for user and AI messages
- **Floating Orbs**: Background animation elements

### Backend (FastAPI)
- **Modern Landing Page**: Matching design with status indicators
- **API Documentation**: Built-in endpoint information
- **Real-time Processing**: Fast response times

## 🔧 Customization

### Colors
You can customize the color scheme by modifying the CSS variables in `app.py`:
```css
/* Primary colors */
--primary-cyan: #00ffff;
--primary-pink: #ff00ff;
--primary-purple: #764ba2;
```

### Animations
Adjust animation speeds and effects in the CSS:
```css
/* Animation duration */
animation: gradientShift 15s ease infinite;
animation: neonPulse 2s ease-in-out infinite alternate;
```

### Typography
Change fonts by updating the Google Fonts import:
```css
@import url('https://fonts.googleapis.com/css2?family=YourFont:wght@400;700&display=swap');
```

## 🐛 Troubleshooting

### Common Issues
1. **Google Calendar Authentication**: Ensure credentials are properly set up
2. **API Rate Limits**: Check OpenAI API usage limits
3. **Port Conflicts**: Change ports if 8000 or 8501 are in use

### Error Messages
- **429 Error**: Rate limit exceeded, wait before retrying
- **Authentication Error**: Check Google Calendar credentials
- **Connection Error**: Ensure both frontend and backend are running

## 📱 Mobile Responsiveness

The application is fully responsive and optimized for:
- Desktop (1200px+)
- Tablet (768px - 1199px)
- Mobile (320px - 767px)

## 🎉 Features in Action

### Visual Effects
- **Gradient Animations**: Continuous background color shifts
- **Neon Glows**: Pulsing text and button effects
- **Glassmorphism**: Translucent containers with blur
- **Hover Animations**: Interactive element responses
- **Loading States**: Custom spinner with neon effects

### User Experience
- **Smooth Transitions**: All interactions are animated
- **Intuitive Interface**: Clear visual hierarchy
- **Real-time Feedback**: Immediate response to user actions
- **Accessibility**: High contrast and readable fonts

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Streamlit**: For the amazing web app framework
- **FastAPI**: For the high-performance backend
- **OpenAI**: For the AI capabilities
- **Google Calendar API**: For calendar integration
- **Google Fonts**: For beautiful typography

---

