// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyDloYR_MJkCeDo_G9NQ41WRw3TAjhjw9sI",
  authDomain: "my-shop-ca0c9.firebaseapp.com",
  projectId: "my-shop-ca0c9",
  storageBucket: "my-shop-ca0c9.firebasestorage.app",
  messagingSenderId: "394422129187",
  appId: "1:394422129187:web:be2837cae6e8e3949a1796",
  measurementId: "G-G0PKSY7BJ9"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);