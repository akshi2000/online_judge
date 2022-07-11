import axios from "axios";

const baseURL = process.env.REACT_APP_SERVER_URL;
let headers = {};

const axiosInstance = axios.create({
  baseURL: baseURL,
  headers,
});

export default axiosInstance;
