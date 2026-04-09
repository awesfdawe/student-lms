import { API_BASE_URL } from '@/api/index';

export const API_BASE = `${API_BASE_URL}/auth`;

export const getHeaders = () => {
  const headers: Record<string, string> = {
    'Accept': 'application/json',
  };
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('access_token');
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
  }
  return headers;
};

export const sanitizeEmail = (email: string) => {
  return email.replace(/['"<>\\]/g, "").trim();
};

export const sanitizePassword = (password: string) => {
  return password.replace(/[<>\\]/g, "");
};

export const authApi = {
  async register(data: any) {
    const response = await fetch(`${API_BASE}/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!response.ok) throw await response.json();
    return response.json();
  },

  async login(data: any) {
    const formData = new URLSearchParams();
    formData.append('username', data.email);
    formData.append('password', data.password);
    
    const response = await fetch(`${API_BASE}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: formData.toString(),
    });
    if (!response.ok) throw await response.json();
    return response.json();
  },

  async verify2fa(data: any) {
    const response = await fetch(`${API_BASE}/login/verify-2fa`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!response.ok) throw await response.json();
    return response.json();
  },

  async enable2fa() {
    const response = await fetch(`${API_BASE}/2fa/enable`, {
      method: 'POST',
      headers: getHeaders(),
    });
    if (!response.ok) throw await response.json();
    return response.json();
  },

  async confirm2fa(code: string) {
    const response = await fetch(`${API_BASE}/2fa/confirm`, {
      method: 'POST',
      headers: { ...getHeaders(), 'Content-Type': 'application/json' },
      body: JSON.stringify({ code }),
    });
    if (!response.ok) throw await response.json();
    return response.json();
  },

  async disable2fa(data: any) {
    const response = await fetch(`${API_BASE}/2fa/disable`, {
      method: 'POST',
      headers: { ...getHeaders(), 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!response.ok) throw await response.json();
    return response.json();
  }
};
