import SearchIcon from "@mui/icons-material/Search";
import { Box, Button, InputAdornment, TextField } from "@mui/material";
import React from "react";

function SearchBar({ search, setSearch, onSearch }) {
  return (
    <Box sx={{ display: "flex", gap: 2, width: "100%", mb: 3 }}>
      <TextField
        fullWidth
        variant="outlined"
        placeholder="Search by title, department, etc."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            onSearch();
          }
        }}
        InputProps={{
          startAdornment: (
            <InputAdornment position="start">
              <SearchIcon />
            </InputAdornment>
          ),
        }}
        sx={{
          "& .MuiOutlinedInput-root": {
            borderRadius: "8px",
            backgroundColor: "rgba(255, 255, 255, 0.9)",
          },
        }}
      />
      <Button
        variant="contained"
        onClick={onSearch}
        sx={{
          borderRadius: "8px",
          backgroundColor: "#4CAF50",
          "&:hover": {
            backgroundColor: "#388E3C",
          },
          px: 3,
        }}
      >
        Search
      </Button>
    </Box>
  );
}

export default SearchBar;
