import React, { useState } from 'react';
import './styles.css';

const Login = () => {
  const [isLogin, setIsLogin] = useState(true); // Toggle between Login and Sign Up

  // Form state
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  // Toggle form
  const toggleForm = () => setIsLogin(!isLogin);

  // Handle submit (placeholder function)
  const handleSubmit = (e) => {
    e.preventDefault();
    if (isLogin) {
      console.log('Logging in with:', { email, password });
      // Implement login logic
    } else {
      if (password !== confirmPassword) {
        alert('Passwords do not match');
      } else {
        console.log('Creating account with:', { email, password });
        // Implement account creation logic
      }
    }
  };

  return (
    <div className="auth-page">
      <h1>{isLogin ? 'Login' : 'Create Account'}</h1>
      <form className="auth-form" onSubmit={handleSubmit}>
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
        <button type="submit" className="auth-btn">
          {isLogin ? 'Login' : 'Sign Up'}
        </button>
      </form>
      <p onClick={toggleForm} className="toggle-link">
        {isLogin ? 'Create an account' : 'Already have an account? Login'}
      </p>
    </div>
  );
};

export default Login;
