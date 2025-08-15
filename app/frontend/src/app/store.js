// src/app/store.js
import { configureStore } from '@reduxjs/toolkit';
import counterReducer from '../features/counter/counterSlice'; // Example slice

export const store = configureStore({
  reducer: {
    counter: counterReducer, // Add your reducers here
  },
});