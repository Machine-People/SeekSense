import React, { useState } from "react";
import {
  Container,
  Typography,
  Box,
  Paper,
  CircularProgress,
  Button,
  Link as MuiLink
} from "@mui/material";
import SearchBar from "../components/SearchBar";
import ReviewTable from "../components/ReviewTable";
import { fetchReviews } from "../hooks/Reviewhook";
import { Link } from "react-router-dom";
import ChatIcon from "@mui/icons-material/Chat";

const Home = () => {
  const [loading, setLoading] = useState(false);
  const [search, setSearch] = useState("");
  const [reviews, setReviews] = useState([]);
  // const theme = useTheme();

  const fetchReview = async () => {
    try {
      setLoading(true);
      const data = await fetchReviews(search);
      setLoading(false);
      setReviews(data);
    } catch (err) {
      console.error("Failed to fetch reviews:", err);
      setLoading(false);
    }
  };

  return (
    <Box
      sx={{
        minHeight: "100vh",
        background: "linear-gradient(135deg, #f5f7fa 0%, #e4e8eb 100%)",
        py: 4,
      }}
    >
      <Container maxWidth="lg">
        <Paper
          elevation={3}
          sx={{
            borderRadius: "16px",
            overflow: "hidden",
            p: 4,
            mb: 4,
            background: "rgba(255, 255, 255, 0.9)",
            backdropFilter: "blur(10px)",
          }}
        >
          <Box textAlign="center" mb={4}>
            <Typography
              variant="h3"
              component="h1"
              fontWeight="bold"
              color="primary"
              gutterBottom
            >
              Welcome to SeekSense
              <span role="img" aria-label="wave" style={{ marginLeft: "10px" }}>
                👋
              </span>
            </Typography>

            <Typography
              variant="h6"
              color="text.secondary"
              sx={{ maxWidth: "700px", mx: "auto", mb: 3 }}
            >
              Where intent meets insight, intellect meets innovation, and
              information meets inspiration.
            </Typography>

            <Button
              component={Link}
              to="/chat"
              variant="contained"
              color="primary"
              startIcon={<ChatIcon />}
              size="large"
              sx={{
                borderRadius: "30px",
                px: 3,
                py: 1,
                mb: 4,
                backgroundColor: "#4CAF50",
                "&:hover": {
                  backgroundColor: "#388E3C",
                },
              }}
            >
              Chat with our AI
            </Button>
          </Box>

          <SearchBar search={search} setSearch={setSearch} onSearch={fetchReview} />

          {loading ? (
            <Box
              display="flex"
              justifyContent="center"
              alignItems="center"
              minHeight="200px"
            >
              <CircularProgress color="primary" />
            </Box>
          ) : (
            <>
              {reviews.length > 0 && (
                <Box mb={2}>
                  <Typography variant="body1" color="text.secondary">
                    Found <strong>{reviews.length}</strong> review(s).
                  </Typography>
                </Box>
              )}
              <ReviewTable reviews={reviews} />
            </>
          )}
        </Paper>
      </Container>
    </Box>
  );
};

export default Home;
