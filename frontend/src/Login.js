import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom'; // Import useNavigate
import './styles.css';

const Login = () => {
  const [isLogin, setIsLogin] = useState(true); // Toggle between Login and Sign Up
  const [isLoggedIn, setIsLoggedIn] = useState(false); // Track if user is logged in

  // Form state
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [username, setUsername] = useState('');
  const [birthdate, setBirthdate] = useState('');
  const [age, setAge] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const navigate = useNavigate(); // Hook to navigate programmatically

  // Check if there's a token on component mount
  useEffect(() => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      setIsLoggedIn(true); // User is already logged in
    }
  }, []);

  // Toggle form
  const toggleForm = () => setIsLogin(!isLogin);

  // Handle submit (make API requests to backend using axios)
  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');  // Reset error before trying

    const requestData = { email, password };

    // Handle validation for sign-up
    if (!isLogin) {
      if (password !== confirmPassword) {
        setError('Passwords do not match');
        setIsLoading(false);
        return;
      }

      // Additional validation for form fields
      if (password.length < 8 || !/[A-Z]/.test(password) || !/[0-9]/.test(password)) {
        setError('Password must be at least 8 characters long and include a number and a capital letter.');
        setIsLoading(false);
        return;
      }

      // Include additional registration fields
      Object.assign(requestData, { 
        FirstName: firstName, 
        LastName: lastName, 
        Username: username, 
        Birthdate: birthdate, 
        Age: age 
      });
    }

    try {
      const url = isLogin
        ? 'http://localhost:5000/api/login' // Login route
        : 'http://localhost:5000/api/register'; // Registration route

      // Make the API request using Axios
      const response = await axios.post(url, requestData);

      if (!isLogin) {
        console.log('Account created successfully:', response.data);
      } else {
        console.log('Login successful:', response.data);
        
        // Store token in localStorage
        localStorage.setItem('auth_token', response.data.token);
        localStorage.setItem('userID', response.data.userID);
        console.log(response.data.userID)

        // Update login state
        setIsLoggedIn(true);

        // Redirect to the home page
        navigate('/');  // You can change '/home' to whatever your home route is
      }
    } catch (err) {
      setError(err.response?.data?.error || 'An error occurred');
      console.error('Error:', err);
    }

    setIsLoading(false);
  };

  // Handle logout
  const handleLogout = () => {
    // Clear token from localStorage
    localStorage.removeItem('auth_token');
    setIsLoggedIn(false);
    console.log('User logged out');
  };

  return (
    <div className="auth-page">
      {isLoggedIn ? (
        <div>
          <h1>Welcome, you are logged in!</h1>
          <button onClick={handleLogout} className="auth-btn">
            Log Out
          </button>
        </div>
      ) : (
        <div>
          <h1>{isLogin ? 'Login' : 'Create Account'}</h1>
          <form className="auth-form" onSubmit={handleSubmit}>
            {!isLogin && (
              <>
                <label>
                  First Name:
                  <input
                    type="text"
                    value={firstName}
                    onChange={(e) => setFirstName(e.target.value)}
                    required
                  />
                </label>
                <label>
                  Last Name:
                  <input
                    type="text"
                    value={lastName}
                    onChange={(e) => setLastName(e.target.value)}
                    required
                  />
                </label>
                <label>
                  Username:
                  <input
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                  />
                </label>
                <label>
                  Birthdate:
                  <input
                    type="date"
                    value={birthdate}
                    onChange={(e) => setBirthdate(e.target.value)}
                    required
                  />
                </label>
                <label>
                  Age:
                  <input
                    type="number"
                    value={age}
                    onChange={(e) => setAge(e.target.value)}
                    required
                  />
                </label>
              </>
            )}
            <label>
              Email:
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </label>
            <label>
              Password:
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </label>
            {!isLogin && (
              <label>
                Confirm Password:
                <input
                  type="password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  required
                />
              </label>
            )}
            {error && <p className="error-message">{error}</p>}
            <button type="submit" className="auth-btn" disabled={isLoading}>
              {isLoading ? 'Loading...' : isLogin ? 'Login' : 'Sign Up'}
            </button>
          </form>
          <p onClick={toggleForm} className="toggle-link">
            {isLogin ? 'Create an account' : 'Already have an account? Login'}
          </p>
        </div>
      )}
    </div>
  );
};

export default Login;
