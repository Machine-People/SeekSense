import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000', // Change this to your FastAPI server
});

export const fetchReviews = async (searchParams = '') => {
  const response = await api.post(`api/reviews/search`, {
    "query": searchParams,
  });
  console.log(response.data);
  
    return response.data;
}
