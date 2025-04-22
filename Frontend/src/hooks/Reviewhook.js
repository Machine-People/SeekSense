import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000', // Change this to your FastAPI server
});

const fetchReviews = async (searchParams = '') => {
  const response = await api.post(`api/reviews/search`, {
    "query": searchParams,
  });  
  // console.log(await response.data);
  
    return response.data;
}

const fetchbyID = async (id) => {
  const response = await api.get(`api/product/${id}`);
  console.log(response.data);
  return response.data;
}

export { fetchReviews, fetchbyID };