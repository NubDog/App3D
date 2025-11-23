import { BrowserRouter, Routes, Route} from "react-router-dom";
import HomePage from "./pages/HomePage,jsx/HomePage";
import NotFoundPage from "./pages/NotFoundPage/NotFoundPage"
function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App;