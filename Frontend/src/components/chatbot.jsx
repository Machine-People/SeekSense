import { useState, useEffect, useRef, } from "react";
import { useNavigate } from "react-router-dom";
import { fetchReviews } from "../hooks/Reviewhook";

import "../styles/chatStyle.css";


export default function Chat() {
  const navigate = useNavigate();
  const MAXIMUM_DATA_SHOWN = 5;
  const handleSeeMore = (productId) => {
    console.log("Product ID:", productId);
    
    navigate(`/product/${productId}`);
  }
const [messages, setMessages] = useState([
    { text: "Welcome to ShopEase! How can I assist you today?", self: false }
]);


const [input, setInput] = useState("");
const messagesRef = useRef(null);
const [overflown, setOverflown] = useState(false);

// Scroll to the bottom of the chat when new messages are added
  useEffect(() => {
    if (messagesRef.current) {
      messagesRef.current.scrollTop = messagesRef.current.scrollHeight;
      if (messagesRef.current.scrollHeight > messagesRef.current.clientHeight) {
        messagesRef.current.style["overflow-y"] = "auto";
        setOverflown(true);
      }
    }
  }, [messages]);

  // Handle window resize to adjust overflow
  useEffect(() => {
    const handleResize = () => {
      if (messagesRef.current.scrollHeight > messagesRef.current.clientHeight) {
        messagesRef.current.style["overflow-y"] = "auto";
        setOverflown(true);
      } else {
        setOverflown(false);
      }
    };

    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  // Handle input change and send message on Enter key press
  const sendMessage = async () => {
    if (!input.trim()) return;
    fetchReviews(input);
    setMessages((prev) => [...prev, { text: input, self: true }]);
    setInput("");
    try {
      const data = await fetchReviews(input);
      var length = data.length;
      //  Limit the number of reviews shown
      if (length > MAXIMUM_DATA_SHOWN) {
        length = MAXIMUM_DATA_SHOWN;
      }
      // Check if the data is empty
      if (length === 0) {
        setMessages((prev) => [
          ...prev,
          { text: "No results found. Please try again.", self: false }
        ]);
        return;
      }
      setMessages((prev) => [
        ...prev,
        { text: "Here are some of the product reviews I compiled for you 🔍",
           self: false }
      ]);
      // Add the product reviews to the chat
      for (let i = 0; i < length; i++) {
        setMessages((prev) => [
          ...prev,
          {
            text: data[i].reviewtext,
            self: false,
            loading: false,
            type: "product",
            title: data[i].title,
            rating: data[i].rating,
            clothingid: data[i].clothingid
          }
        ]);
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div className="wrapper">
      <div className="chat">
        <div className="messages" ref={messagesRef}>
        {messages.map((msg, index) => (
  <div
    key={index}
    className={`message ${msg.self ? "self" : ""} ${msg.loading ? "loading" : ""} ${msg.type === "product" ? "product" : ""}`}
  >
    {
      // Check if the message is a product type or text
      msg.type === "product" ? (
        // Display the product card if it's a product type
        <div className="product-card">
          <div className="product-info">
            <div className="product-title">{msg.title}</div>
          <button className="see-more-btn" onClick={() => handleSeeMore(msg.clothingid)}>
            See More
          </button>
            <div className="product-rating">⭐ {msg.rating}</div>
          </div>
        </div>
      ) : (
        // Display the text message if it's not a product type
        msg.text
    )}
  </div>
  ))}
        </div>
        <div className="write">
          <input
            className="input"
            placeholder="Your message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === "Enter" && sendMessage()}
          />
        </div>
      </div>
    </div>
  );
}
