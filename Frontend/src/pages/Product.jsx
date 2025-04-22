import React, { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { fetchbyID } from "../hooks/Reviewhook";
import "../styles/product.css";

const ProductPage = () => {
    const { id } = useParams(); // Get the ID from the URL
    const [review, setReview] = useState([]); // State to store fetched data
    const [loading, setLoading] = useState(true); // State to handle loading

    useEffect(() => {
        // Fetch data based on the ID
        var i=1;
        const fetchData = async () => {
            if (i<1) {
                console.log("return");
                return;
            }
            i--;
            try {
                const data = await fetchbyID(id);                
                if (data.length === 0) {
                    console.error("No data found for the given ID");
                    return;
                }
                setReview(data);
                console.log("Data fetched successfully:", data);
            } catch (error) {
                console.error("Error fetching review:", error);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [id]);

    if (loading) {
        return <div>Loading...</div>;
    }

    if (!review) {
        return <div>Review not found</div>;
    }

    return (
        <>
        <div className="seeksense">
            <Link to="/" className="logo">

            <h1>SeekSense</h1>
            </Link>
        </div>
        <div className="heading">
            <h1>Product Review</h1>
        </div>

        <div className="product-page-wrapper">
            {review.map((item, index) => (
                <div className="product-card" key={index}>
                    <div className="product-header">
                        <h2>{item.title || "Untitled Review"}</h2>
                        {item.rating && (
                            <div className="product-rating">
                                {"⭐".repeat(item.rating)}{" "}
                                <span className="rating-num">({item.rating})</span>
                            </div>
                        )}
                    </div>

                    {item.reviewtext && (
                        <p className="review-text">"{item.reviewtext}"</p>
                    )}

                    <div className="product-details">
                        <span className="info-chip">Clothing ID: {item.clothingid}</span>
                        {item.age && <span className="info-chip">Age: {item.age}</span>}
                        {item.recommendedind !== null && (
                            <span
                                className={`recommend ${
                                    item.recommendedind ? "yes" : "no"
                                }`}
                            >
                                {item.recommendedind ? "✅ Recommended" : "❌ Not Recommended"}
                            </span>
                        )}
                        {item.PositiveFeedbackCount !== null && (
                            <span className="feedback">
                                👍 {item.PositiveFeedbackCount} helpful
                            </span>
                        )}
                    </div>

                    <div className="category-info">
                        {item.DivisionName && <span>{item.DivisionName}</span>}
                        {item.DepartmentName && <span> › {item.DepartmentName}</span>}
                        {item.ClassName && <span> › {item.ClassName}</span>}
                    </div>
                </div>
            ))}
        </div>
    </>
    );
};

export default ProductPage;
