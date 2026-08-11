'use client';

import { useState } from 'react';

export default function SignUp() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const [id, setId] = useState(0);

  async function registerUser() {
    const response = await fetch('http://localhost:8000/auth/signup', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username,
        email,
        password,
      }),
    });

    const data = await response.json();

    setId(data.id);
  }

  return (
    <div>
      <div>Please enter your credentials</div>
      <input value={username} onChange={(e) => setUsername(e.target.value)} placeholder='Username' />
      <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder='Email' />
      <input type='password' value={password} onChange={(e) => setPassword(e.target.value)} placeholder='Password' />
      <button onClick={registerUser}>Register</button>

      <div>{id && <div> use id is {id}</div>}</div>
    </div>
  );
}
