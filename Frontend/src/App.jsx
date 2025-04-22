import React from "react";
import Home from "./pages/Home";
import { Route, Routes } from "react-router-dom";
import ChatPage from "./pages/Chat";
import ProductPage from "./pages/Product";



function App () {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/chat" element={<ChatPage />} />
      <Route path="/product/:id" element={<ProductPage />} />

    </Routes>
  );
};

export default App;
