'use client';

import { useEffect, useState, useRef } from 'react';
import { useRouter } from 'next/navigation';

export default function dashboard() {
  const router = useRouter();
  const [url, setUrl] = useState('');
  const [response, setReponse] = useState('');
  const token = useRef<string | null>(null);
  const [prompt, setPrompt] = useState('');
  const [promptResponse, setPromptResponse] = useState('');

  async function createRepository() {
    const response = await fetch('http://localhost:8000/repositories', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token.current}`,
      },
      body: JSON.stringify({
        url,
      }),
    });

    const data = await response.json();
    setReponse(JSON.stringify(data));
  }

  async function sendPrompt() {
    const response = await fetch('http://localhost:8000/prompt', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token.current}`,
      },
      body: JSON.stringify({
        prompt,
      }),
    });

    const data = await response.json();
    setPromptResponse(JSON.stringify(data));
  }

  useEffect(() => {
    token.current = localStorage.getItem('access_token');
    if (!token.current) {
      router.push('/login');
    }
  }, [router]);

  return (
    <div>
      this is the dashboard
      <input onChange={(e) => setUrl(e.target.value)} placeholder='send url' />
      <button onClick={createRepository}> Create Repository</button>
      <div>
        <h1>Send your prompt</h1>
        <input onChange={(e) => setPrompt(e.target.value)} placeholder='send prompt' />
        <div>{promptResponse}</div>
        <button onClick={sendPrompt}>send</button>
      </div>
    </div>
  );
}
