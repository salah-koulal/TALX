import { useState, useEffect } from 'react';
import axios from 'axios';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;

const client = axios.create({
  baseURL: "http://127.0.0.1:8000"
});

export default function Auth() {
    const [currentUser, setCurrentUser] = useState();
    const [registrationToggle, setRegistrationToggle] = useState(false);
    const [email, setEmail] = useState('');
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
  
    useEffect(() => {
    client.get("/api/user")
    .then(function(res) {
      setCurrentUser(true);
    })
    .catch(function(error) {
      setCurrentUser(false);
    });
  }, [currentUser]);
  
    function update_form_btn() {
      if (registrationToggle) {
        document.getElementById("form_btn").innerHTML = "Register";
        setRegistrationToggle(false);
      } else {
        document.getElementById("form_btn").innerHTML = "Log in";
        setRegistrationToggle(true);
      }
    }
  
    function submitRegistration(e) {
      e.preventDefault();
      client.post(
        "/api/register",
        {
          email: email,
          username: username,
          password: password
        }
      ).then(function(res) {
        client.post(
          "/api/login",
          {
            username: username,
            password: password
          }
        ).then(function(res) {
          
          setCurrentUser(true);
        });
      });
    }
  
    function submitLogin(e) {
      e.preventDefault();
      client.post(
        "/api/login",
        {
          username: username,
          password: password
        }
      ).then(function(res) {
        setCurrentUser(true);
      });
    }
  
    function submitLogout(e) {
      e.preventDefault();
      client.post(
        "/api/logout",
        {withCredentials: true}
      ).then(function(res) {
        setCurrentUser(false);
      });
    }
  
    if (currentUser) {
      return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
          <div className="w-full max-w-md bg-white rounded-lg shadow-md p-8">
            <form onSubmit={e => submitLogout(e)} className="mb-4">
              <button type="submit" className="w-full bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
                Log out
              </button>
            </form>
            <div className="text-center">
              <h2 className="text-2xl font-bold text-gray-800">You're logged in!</h2>
            </div>
          </div>
        </div>
      );
    }
  
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
        <div className="w-full max-w-md bg-white rounded-lg shadow-md p-8">
          <form onSubmit={registrationToggle ? submitRegistration : submitLogin} className="mb-4">
            
            <div className="mb-4">
                <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="username">
                  Username
                </label>
                <input 
                  className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                  id="username"
                  type="text"
                  placeholder="Username"
                  value={username}
                  onChange={e => setUsername(e.target.value)}
                  required
                />
              </div>
            {registrationToggle && (
              <>
              
              <div className="mb-4">
                <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="username">
                  Username
                </label>
                <input 
                  className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                  id="username"
                  type="text"
                  placeholder="Username"
                  value={username}
                  onChange={e => setUsername(e.target.value)}
                  required
                />
              </div>
              <div className="mb-4">
              <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="email">
                Email
              </label>
              <input 
                className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                id="email"
                type="email"
                placeholder="Email"
                value={email}
                onChange={e => setEmail(e.target.value)}
                required
              />
              
            </div>
              </>
            )}
            <div className="mb-6">
              <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="password">
                Password
              </label>
              <input 
                className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline"
                id="password"
                type="password"
                placeholder="******************"
                value={password}
                onChange={e => setPassword(e.target.value)}
                required
              />
            </div>
            <div className="flex items-center justify-between">
              <button 
                className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline" 
                type="submit"
                id="form_btn"
              >
                {registrationToggle ? 'Register' : 'Log In'}
              </button>
              <button 
                className="inline-block align-baseline font-bold text-sm text-blue-500 hover:text-blue-800"
                type="button"
                onClick={update_form_btn}
              >
                {registrationToggle ? 'Already have an account? Log in' : 'Need an account? Register'}
              </button>
            </div>
          </form>
        </div>
      </div>
    );
}