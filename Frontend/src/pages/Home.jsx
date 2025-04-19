import React, { useEffect, useState } from "react";
import axios from "axios";
import SearchBar from "../components/SearchBar";
import ReviewTable from "../components/ReviewTable";
import "../styles/app.css";
import "../styles/loader.css";

const Home = () => {
    const [loading, setLoading] = useState(false); 
    const [search, setSearch] = useState("");
    const [reviews, setReviews] = useState([]);

  const fetchReviews = async () => {
      try {
        setLoading(true);
      const res = await axios.post(`http://localhost:8000/api/reviews/search`, {
        query: search,
      });
      console.log(res.data);
        setLoading(false);
      setReviews(res.data);
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
      <h1 className="title">Welcome to the Review Dashboard</h1>
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
          <SearchBar search={search} setSearch={setSearch} onSearch={fetchReviews} />
          <ReviewTable reviews={reviews} />
        </>
      )}
    </div>
  );
};

export default Home;
