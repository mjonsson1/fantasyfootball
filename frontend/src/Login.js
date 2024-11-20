import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './styles.css';

const Login = ({ onLogin }) => {
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
// Check if there's a token on component mount
useEffect(() => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    setIsLoggedIn(true); // User is already logged in
  }

  const handleUnload = () => {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('userID');
    console.log('User logged out due to app closure');
  };

  window.addEventListener('beforeunload', handleUnload);

  return () => {
    window.removeEventListener('beforeunload', handleUnload);
  };
}, []);


  // Toggle form between Login and Sign Up
  const toggleForm = () => setIsLogin(!isLogin);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');
  
    const requestData = { email, password };
  
    try {
      const response = await axios.post(
        'http://localhost:5000/api/login', 
        requestData
      );
  
      console.log('Login successful:', response.data);
  
      // Store token and userID in localStorage
      localStorage.setItem('auth_token', response.data.token);
      localStorage.setItem('userID', response.data.userID);
  
      // Call onLogin and pass userID to parent
      onLogin(response.data.userID); // Pass userID to parent
      navigate('/');
    } catch (err) {
      setError(err.response?.data?.error || 'An error occurred');
      console.error('Error:', err);
    } finally {
      setIsLoading(false);
    }
  };
  

// Handle logout
const handleLogout = () => {
  localStorage.removeItem('auth_token');
  setIsLoggedIn(false);
  console.log('User logged out');
  window.location.reload(); // Refresh the page
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
          <button onClick={toggleForm} className="auth-btn">
            {isLogin ? 'Create Account' : 'Already have an account? Login'}
          </button>
        </div>
      )}
    </div>
  );
};

export default Login;
