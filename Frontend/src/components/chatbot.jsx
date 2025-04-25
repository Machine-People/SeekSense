import PersonIcon from "@mui/icons-material/Person";
import SendIcon from "@mui/icons-material/Send";
import SmartToyIcon from "@mui/icons-material/SmartToy";
import VisibilityIcon from "@mui/icons-material/Visibility";
import {
  Box,
  Button,
  Card,
  CardContent,
  CircularProgress,
  IconButton,
  Paper,
  Rating,
  TextField,
  Typography,
} from "@mui/material";
import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { fetchReviews } from "../hooks/Reviewhook";

export default function Chat() {
  const navigate = useNavigate();
  const MAXIMUM_DATA_SHOWN = 5;

  const handleSeeMore = (productId) => {
    console.log("Product ID:", productId);
    navigate(`/product/${productId}`);
  };

  // Initialize messages from localStorage or use default welcome message
  const [messages, setMessages] = useState(() => {
    const savedMessages = localStorage.getItem('chatMessages');
    return savedMessages ? JSON.parse(savedMessages) : [
      {
        text: "Welcome to SeekSense! How can I assist you today?",
        self: false,
      },
    ];
  });

  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const messagesRef = useRef(null);
  const inputRef = useRef(null);

  // Save messages to localStorage whenever they change
  useEffect(() => {
    localStorage.setItem('chatMessages', JSON.stringify(messages));
  }, [messages]);

  // Scroll to the bottom of the chat when new messages are added
  useEffect(() => {
    if (messagesRef.current) {
      messagesRef.current.scrollTop = messagesRef.current.scrollHeight;
    }
  }, [messages]);

  // Focus input field on load
  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.focus();
    }
  }, []);

  // Function to clear chat history
  const clearChat = () => {
    setMessages([
      {
        text: "Welcome to SeekSense! How can I assist you today?",
        self: false,
      },
    ]);
    // This will trigger the useEffect to update localStorage
  };

  const sendMessage = async () => {
    if (!input.trim()) return;

    // Add user message
    setMessages((prev) => [...prev, { text: input, self: true }]);
    const userQuery = input;
    setInput("");
    setIsTyping(true);

    try {
      // Simulate typing indicator
      setMessages((prev) => [
        ...prev,
        { text: "", self: false, loading: true },
      ]);

      // Fetch data
      const data = await fetchReviews(userQuery);

      // Remove typing indicator
      setMessages((prev) => prev.filter((msg) => !msg.loading));

      var length = data.length;
      // Limit the number of reviews shown
      if (length > MAXIMUM_DATA_SHOWN) {
        length = MAXIMUM_DATA_SHOWN;
      }

      // Check if the data is empty
      if (length === 0) {
        setMessages((prev) => [
          ...prev,
          {
            text: "No results found. Please try again with different keywords.",
            self: false,
          },
        ]);
        return;
      }

      // Add response message
      setMessages((prev) => [
        ...prev,
        {
          text: "Here are some of the product reviews I compiled for you 🔍",
          self: false,
        },
      ]);

      // Add the product reviews to the chat
      for (let i = 0; i < length; i++) {
        setMessages((prev) => [
          ...prev,
          {
            text: data[i].reviewtext,
            self: false,
            type: "product",
            title: data[i].title,
            rating: data[i].rating,
            clothingid: data[i].clothingid,
          },
        ]);
      }
    } catch (error) {
      console.error("Error:", error);
      setMessages((prev) => [
        ...prev.filter((msg) => !msg.loading),
        {
          text: "Sorry, I encountered an error while searching. Please try again.",
          self: false,
        },
      ]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <Box
      sx={{
        height: "100%",
        display: "flex",
        flexDirection: "column",
        bgcolor: "#f5f7fa",
        p: 2,
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <Box
        sx={{
          width: "100%",
          maxWidth: "800px",
          display: "flex",
          justifyContent: "flex-end",
          mb: 1,
        }}
      >
        <Button 
          variant="outlined" 
          size="small" 
          onClick={clearChat}
          sx={{ 
            borderRadius: "20px",
            textTransform: "none",
          }}
        >
          Clear Chat
        </Button>
      </Box>
      
      <Box
        ref={messagesRef}
        sx={{
          width: "100%",
          maxWidth: "800px",
          flexGrow: 1,
          overflowY: "auto",
          display: "flex",
          flexDirection: "column",
          gap: 2,
          p: 2,
          mb: 3,
        }}
      >
        {messages.map((msg, index) => (
          <Box
            key={index}
            sx={{
              alignSelf: msg.self ? "flex-end" : "flex-start",
              maxWidth: "70%",
              animation: "fadeIn 0.3s",
              "@keyframes fadeIn": {
                from: {
                  opacity: 0,
                  transform: msg.self
                    ? "translateX(20px)"
                    : "translateX(-20px)",
                },
                to: {
                  opacity: 1,
                  transform: "translateX(0)",
                },
              },
            }}
          >
            {msg.loading ? (
              <Box sx={{ display: "flex", alignItems: "center", gap: 1, p: 1 }}>
                <CircularProgress size={20} />
                <Typography variant="body2" color="text.secondary">
                  Searching...
                </Typography>
              </Box>
            ) : msg.type === "product" ? (
              <Card
                elevation={2}
                sx={{
                  borderRadius: "12px",
                  overflow: "hidden",
                  transition: "transform 0.2s, box-shadow 0.2s",
                  "&:hover": {
                    transform: "translateY(-2px)",
                    boxShadow: "0 8px 16px rgba(0,0,0,0.1)",
                  },
                }}
              >
                <CardContent>
                  <Box
                    sx={{
                      display: "flex",
                      justifyContent: "space-between",
                      alignItems: "flex-start",
                      mb: 1,
                    }}
                  >
                    <Typography variant="h6" component="div" fontWeight="medium">
                      {msg.title}
                    </Typography>
                    <Rating value={msg.rating} readOnly size="small" />
                  </Box>

                  <Typography
                    variant="body2"
                    color="text.secondary"
                    sx={{ mb: 2 }}
                  >
                    {msg.text.length > 150
                      ? `${msg.text.substring(0, 150)}...`
                      : msg.text}
                  </Typography>

                  <Button
                    variant="outlined"
                    size="small"
                    startIcon={<VisibilityIcon />}
                    onClick={() => handleSeeMore(msg.clothingid)}
                    sx={{
                      borderRadius: "20px",
                      textTransform: "none",
                    }}
                  >
                    View Details
                  </Button>
                </CardContent>
              </Card>
            ) : (
              <Paper
                elevation={1}
                sx={{
                  p: 2,
                  borderRadius: msg.self ? "12px 12px 0 12px" : "12px 12px 12px 0",
                  bgcolor: msg.self ? "#4CAF50" : "white",
                  color: msg.self ? "white" : "inherit",
                  display: "flex",
                  alignItems: "flex-start",
                  gap: 1,
                }}
              >
                {!msg.self && (
                  <SmartToyIcon
                    fontSize="small"
                    sx={{ mt: 0.5, color: "#4CAF50" }}
                  />
                )}
                <Typography variant="body1">{msg.text}</Typography>
                {msg.self && (
                  <PersonIcon
                    fontSize="small"
                    sx={{ mt: 0.5, color: "white" }}
                  />
                )}
              </Paper>
            )}
          </Box>
        ))}
      </Box>

      <Box
        component="form"
        onSubmit={(e) => {
          e.preventDefault();
          sendMessage();
        }}
        sx={{
          width: "100%",
          maxWidth: "600px",
          display: "flex",
          gap: 1,
        }}
      >
        <TextField
          fullWidth
          variant="outlined"
          placeholder="Type your message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          inputRef={inputRef}
          disabled={isTyping}
          sx={{
            "& .MuiOutlinedInput-root": {
              borderRadius: "30px",
              bgcolor: "white",
            },
          }}
        />
        <IconButton
          color="primary"
          onClick={sendMessage}
          disabled={!input.trim() || isTyping}
          sx={{
            bgcolor: "#4CAF50",
            color: "white",
            "&:hover": {
              bgcolor: "#388E3C",
            },
            "&.Mui-disabled": {
              bgcolor: "#e0e0e0",
              color: "#9e9e9e",
            },
          }}
        >
          <SendIcon />
        </IconButton>
      </Box>
    </Box>
  );
}
