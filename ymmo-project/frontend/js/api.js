const API_URL = 'http://127.0.0.1:5000/api';

class ApiClient {
    async get(endpoint) {
        const response = await fetch(`${API_URL}${endpoint}`);
        if (!response.ok) throw new Error(`API error: ${response.status}`);
        return await response.json();
    }

    async post(endpoint, data) {
        const response = await fetch(`${API_URL}${endpoint}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        if (!response.ok) throw new Error(`API error: ${response.status}`);
        return await response.json();
    }

    async getProperties(filters = {}) {
        const query = new URLSearchParams(filters);
        return this.get(`/properties?${query}`);
    }

    async getProperty(id) {
        return this.get(`/properties/${id}`);
    }

    async createProperty(data) {
        return this.post('/properties', data);
    }
}

const api = new ApiClient();
