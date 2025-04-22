import React, { useEffect, useState } from "react";
import axios from "axios";
import SearchBar from "../components/SearchBar";
import ReviewTable from "../components/ReviewTable";
import { fetchReviews } from "../hooks/Reviewhook";
import "../styles/app.css";
import "../styles/loader.css";

const Home = () => {
    const [loading, setLoading] = useState(false); 
    const [search, setSearch] = useState("");
    const [reviews, setReviews] = useState([]);

  const fetchReview = async () => {
      try {
        setLoading(true);
        const data = await fetchReviews(search);
        setLoading(false);
        setReviews(data);
    } catch (err) {
      console.error("Failed to fetch reviews:", err);
    }
  };


  return (
    <div className="container">
        
        {!loading && reviews.length > 0 && (
            <div className="results-count">
            Found {reviews.length} review(s).
            </div>
        )}
      <h1 className="title">Welcome to the SeekSense search !  
        <span role="img" aria-label="wave">👋</span>
      </h1>
      <h3 className="description" style={{ textAlign: 'center', fontSize: '1.5rem', marginTop: '20px', color: '#333', fontFamily: 'Arial, sans-serif', fontWeight: 'bold', color: '#4CAF50', textTransform: 'uppercase' }}>
        Where intent meets insight, intellect meets innovation, and 
        information meets inspiration.
      </h3>
      <h4 className="chatbot" style={{ textAlign: 'center', fontSize: '1.5rem', marginTop: '20px', color: '#333', fontFamily: 'Arial, sans-serif', fontWeight: 'bold', color: '#4CAF50', textTransform: 'uppercase' }}>
        <a href="/chat" style={{ textDecoration: 'none', color: '#4CAF50' }}>
          Chat with our AI  
          <span role="img" aria-label="wave">🤖</span>
          </a>
      </h4>

      { loading &&
          <div className="loader-container">
            { (
                <div className="loader">
                </div>
            )}
        </div>
      }

      { !loading && (
        <>
          <SearchBar search={search} setSearch={setSearch} onSearch={fetchReview} />
          <ReviewTable reviews={reviews} />
        </>
      )}
    </div>
  );
};

export default Home;
