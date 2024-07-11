/*import axios from 'axios';

axios.defaults.xsrfCookieName = 'HTTP_X_CSRFTOKEN';
axios.defaults.xsrfHeaderName = 'x-csrftoken';
axios.defaults.withCredentials = true;

const client = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

const getCSRFToken = async () => {
  try {
    const response = await client.get('/api/csrf');
    console.log(response)
    return response.data.csrfToken;  // Assuming your server returns the token
  } catch (error) {
    console.error('Error fetching CSRF token:', error);
    return null;
  }
};*/

import axios from 'axios';

const client = axios.create({
  baseURL: "http://localhost:8000",
  withCredentials: true,
});

// Function to get CSRF token
const getCSRFToken = async () => {
  const response = await client.get('/api/csrf');
  return response.data.csrfToken;
};

// Axios interceptor to add CSRF token to every request
client.interceptors.request.use(async (config) => {
  if (config.method === 'post' || config.method === 'put' || config.method === 'delete') {
    const csrfToken = await getCSRFToken();
    config.headers['X-CSRFToken'] = csrfToken;
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

export { client };