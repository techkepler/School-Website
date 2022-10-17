import axios from "axios";
// const baseURL = "https://techkepler.com/api/";
const baseURL = "http://127.0.0.1:8000/api/";

const axiosPublic = axios.create({
  baseURL: baseURL,
  headers: {
    "Content-Type": "application/json",
    accept: "application/json",
  },
});

export default axiosPublic;
