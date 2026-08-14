'use client';

import { useEffect, useState, useRef } from 'react';
import { useRouter } from 'next/navigation';

export default function dashboard() {
  const router = useRouter();
  const [url, setUrl] = useState('');
  const [response, setReponse] = useState('');
  const token = useRef<string | null>(null);

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
    </div>
  );
}
