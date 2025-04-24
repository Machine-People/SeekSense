import {
  Chip,
  Paper,
  Rating,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography
} from "@mui/material";
import React from "react";
import { Link } from "react-router-dom";

function ReviewTable({ reviews }) {
  return (
    <TableContainer component={Paper} elevation={3} sx={{ borderRadius: "12px", overflow: "hidden" }}>
      <Table sx={{ minWidth: 650 }}>
        <TableHead>
          <TableRow sx={{ backgroundColor: "#f5f5f5" }}>
            <TableCell sx={{ fontWeight: "bold" }}>ClothingID</TableCell>
            <TableCell sx={{ fontWeight: "bold" }}>Title</TableCell>
            <TableCell sx={{ fontWeight: "bold" }}>ReviewText</TableCell>
            <TableCell sx={{ fontWeight: "bold" }}>Rating</TableCell>
            <TableCell sx={{ fontWeight: "bold" }}>Division</TableCell>
            <TableCell sx={{ fontWeight: "bold" }}>Department</TableCell>
            <TableCell sx={{ fontWeight: "bold" }}>Class</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {reviews.length === 0 ? (
            <TableRow>
              <TableCell colSpan={7} align="center" sx={{ py: 4 }}>
                <Typography variant="body1" color="text.secondary">
                  No results found.
                </Typography>
              </TableCell>
            </TableRow>
          ) : (
            reviews.map((r, i) => (
              <TableRow
                key={i}
                sx={{
                  "&:hover": {
                    backgroundColor: "rgba(76, 175, 80, 0.08)"
                  }
                }}
              >
                <TableCell>
                  <Link
                    to={`/product/${r.clothingid}`}
                    style={{ textDecoration: "none", color: "#4CAF50", fontWeight: "medium" }}
                  >
                    {r.clothingid}
                  </Link>
                </TableCell>
                <TableCell>
                  <Link
                    to={`/product/${r.clothingid}`}
                    style={{ textDecoration: "none", color: "#333" }}
                  >
                    <Typography variant="body1" fontWeight="medium">
                      {r.title}
                    </Typography>
                  </Link>
                </TableCell>
                <TableCell>
                  <Typography variant="body2" color="text.secondary">
                    {r.reviewtext?.slice(0, 50)}...
                  </Typography>
                </TableCell>
                <TableCell>
                  <Rating value={r.rating} readOnly precision={0.5} size="small" />
                </TableCell>
                <TableCell>
                  <Chip
                    label={r.divisionname}
                    size="small"
                    sx={{ backgroundColor: "rgba(76, 175, 80, 0.1)" }}
                  />
                </TableCell>
                <TableCell>{r.departmentname}</TableCell>
                <TableCell>{r.classname}</TableCell>
              </TableRow>
            ))
          )}
        </TableBody>
      </Table>
    </TableContainer>
  );
}

export default ReviewTable;
