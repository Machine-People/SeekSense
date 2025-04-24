import React from "react";
import { Link } from "react-router-dom";
import Chat from "../components/chatbot";
import { Box, Typography, AppBar, Toolbar, Button } from "@mui/material";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";

const ChatPage = () => {
  return (
    <Box sx={{ height: "100vh", display: "flex", flexDirection: "column" }}>
      <AppBar position="static" color="transparent" elevation={0} sx={{ bgcolor: "white" }}>
        <Toolbar>
          <Button
            component={Link}
            to="/"
            startIcon={<ArrowBackIcon />}
            color="primary"
            sx={{ mr: 2 }}
          >
            Back
          </Button>
          <Typography 
            variant="h6" 
            component="div" 
            sx={{ 
              flexGrow: 1, 
              color: "#4CAF50", 
              fontWeight: "bold",
              textTransform: "uppercase"
            }}
          >
            SeekSense AI Chat
          </Typography>
        </Toolbar>
      </AppBar>
      
      <Box sx={{ flexGrow: 1, overflow: "hidden" }}>
        <Chat />
      </Box>
    </Box>
  );
};

export default ChatPage;