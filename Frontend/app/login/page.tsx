'use client';

import { stringify } from 'querystring';
import { useState, useEffect } from 'react';

export default function Login() {
  const [token, setToken] = useState(null);

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  async function loginUser() {
    const response = await fetch('http://localhost:8000/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username,
        password,
      }),
    });

    const data = await response.json();

    setToken(data);
    console.log(data.access_token);
  }

  return (
    <div>
      This is the login page
      <input value={username} onChange={(e) => setUsername(e.target.value)} />
      <input value={password} onChange={(e) => setPassword(e.target.value)} />
      <button onClick={loginUser}>Register</button>
    </div>
  );
}
