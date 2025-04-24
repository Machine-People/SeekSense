import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import CancelIcon from "@mui/icons-material/Cancel";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import ThumbUpIcon from "@mui/icons-material/ThumbUp";
import {
    AppBar,
    Box,
    Button,
    Chip,
    CircularProgress,
    Container,
    Divider,
    Paper,
    Rating,
    Toolbar,
    Typography,
} from "@mui/material";
import React, { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { fetchbyID } from "../hooks/Reviewhook";

const ProductPage = () => {
    const { id } = useParams();
    const [review, setReview] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Fetch data based on the ID
        var i = 1;
        const fetchData = async () => {
            if (i < 1) {
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
        return (
            <Box
                display="flex"
                justifyContent="center"
                alignItems="center"
                minHeight="100vh"
                bgcolor="#f5f7fa"
            >
                <CircularProgress color="primary" />
            </Box>
        );
    }

    if (!review) {
        return (
            <Box
                display="flex"
                justifyContent="center"
                alignItems="center"
                minHeight="100vh"
                bgcolor="#f5f7fa"
            >
                <Typography variant="h5" color="error">
                    Review not found
                </Typography>
            </Box>
        );
    }

    return (
        <Box sx={{ bgcolor: "#f5f7fa", minHeight: "100vh", pb: 6 }}>
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
                    <Typography variant="h6" component="div" sx={{ flexGrow: 1, color: "#4CAF50", fontWeight: "bold" }}>
                        SeekSense
                    </Typography>
                </Toolbar>
            </AppBar>

            <Container maxWidth="md" sx={{ mt: 4 }}>
                <Typography variant="h4" component="h1" gutterBottom fontWeight="bold" color="#333">
                    Product Review
                </Typography>

                {review.map((item, index) => (
                    <Paper
                        key={index}
                        elevation={3}
                        sx={{
                            p: 4,
                            mb: 3,
                            borderRadius: "16px",
                            transition: "transform 0.2s",
                            "&:hover": {
                                transform: "translateY(-4px)",
                                boxShadow: "0 10px 20px rgba(0,0,0,0.1)",
                            },
                        }}
                    >
                        <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                            <Typography variant="h5" fontWeight="bold">
                                {item.title || "Untitled Review"}
                            </Typography>
                            {item.rating && (
                                <Box display="flex" alignItems="center">
                                    <Rating value={item.rating} readOnly precision={0.5} />
                                    <Typography variant="body2" color="text.secondary" ml={1}>
                                        ({item.rating})
                                    </Typography>
                                </Box>
                            )}
                        </Box>

                        <Divider sx={{ mb: 3 }} />

                        {item.reviewtext && (
                            <Typography
                                variant="body1"
                                sx={{
                                    mb: 3,
                                    p: 2,
                                    borderLeft: "4px solid #4CAF50",
                                    bgcolor: "rgba(76, 175, 80, 0.05)",
                                    borderRadius: "0 8px 8px 0",
                                    fontStyle: "italic",
                                }}
                            >
                                "{item.reviewtext}"
                            </Typography>
                        )}

                        <Box display="flex" flexWrap="wrap" gap={1} mb={3}>
                            <Chip
                                label={`Clothing ID: ${item.clothingid}`}
                                variant="outlined"
                                sx={{ borderRadius: "8px" }}
                            />

                            {item.age && (
                                <Chip
                                    label={`Age: ${item.age}`}
                                    variant="outlined"
                                    sx={{ borderRadius: "8px" }}
                                />
                            )}

                            {item.recommendedind !== null && (
                                <Chip
                                    icon={item.recommendedind ? <CheckCircleIcon /> : <CancelIcon />}
                                    label={item.recommendedind ? "Recommended" : "Not Recommended"}
                                    color={item.recommendedind ? "success" : "error"}
                                    sx={{ borderRadius: "8px" }}
                                />
                            )}

                            {item.PositiveFeedbackCount !== null && (
                                <Chip
                                    icon={<ThumbUpIcon />}
                                    label={`${item.PositiveFeedbackCount} helpful`}
                                    variant="outlined"
                                    sx={{ borderRadius: "8px" }}
                                />
                            )}
                        </Box>

                        <Box sx={{ color: "text.secondary", fontSize: "0.9rem" }}>
                            <Typography variant="body2" color="text.secondary">
                                {item.DivisionName && <span>{item.DivisionName}</span>}
                                {item.DepartmentName && <span> › {item.DepartmentName}</span>}
                                {item.ClassName && <span> › {item.ClassName}</span>}
                            </Typography>
                        </Box>
                    </Paper>
                ))}
            </Container>
        </Box>
    );
};

export default ProductPage;
