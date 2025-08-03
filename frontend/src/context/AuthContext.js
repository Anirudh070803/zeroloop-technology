import React, { createContext, useState, useContext } from 'react';
import axios from 'axios';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [token, setToken] = useState(localStorage.getItem('token'));

    // Set the default auth token for all axios requests when the app loads
    if (token) {
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    }

    const login = (newToken) => {
        localStorage.setItem('token', newToken);
        setToken(newToken);
        axios.defaults.headers.common['Authorization'] = `Bearer ${newToken}`;
    };

    const logout = () => {
        localStorage.removeItem('token');
        setToken(null);
        delete axios.defaults.headers.common['Authorization'];
    };

    return (
        <AuthContext.Provider value={{ token, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    return useContext(AuthContext);
};