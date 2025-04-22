// src/pages/ChatPage.jsx
import { Link } from "react-router-dom";
import Chat from "../components/chatbot";

const ChatPage = () => {
  return (
    <div>
      <h2 style={chatStyle}>
          <Link to="/" className="logo">
            SeekSense
          </Link>
        </h2>
      <Chat />
    </div>
  );
};

export default ChatPage;


const chatStyle = { textAlign: 'center', 
  fontSize: '2rem', marginTop: '20px', color: '#333'
  , fontFamily: 'Arial, sans-serif'
  , fontWeight: 'bold',
  color: '#4CAF50',
  textTransform: 'uppercase'
 }