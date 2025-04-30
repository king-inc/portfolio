import React, { useState } from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Home from "./pages/Home";
import Register from "./components/Register";
import Login from "./components/Login";
import Navbar from "./components/Navbar";
import BecomeAuthor from "./pages/BecomeAuthor";
import MyBooks from "./pages/MyBooks";
import ViewBranches from "./pages/ViewBranches";
import NewBook from "./pages/NewBook";
import BookPage from "./pages/BookPage";
import ManageBook from "./pages/ManageBook";
import EditChapter from "./pages/EditChapter";
import ReadChapter from "./pages/ReadChapter";

const App = () => {
  const [showLogin, setShowLogin] = useState(false);
  const [showRegister, setShowRegister] = useState(false);
  const [showBecomeAuthor, setShowBecomeAuthor] = useState(false);
  const [loggedIn, setLoggedIn] = useState(!!localStorage.getItem("token"));
  const handleLoginClose = () => setShowLogin(false);
  const handleRegisterClose = () => setShowRegister(false);
  const handleBecomeAuthorClose = () => setShowBecomeAuthor(false);
  return (
    <Router>
      <Navbar
        setShowLogin={setShowLogin}
        setShowRegister={setShowRegister}
        setShowBecomeAuthor={setShowBecomeAuthor}
        loggedIn={loggedIn}
      />
      <Login
        showLogin={showLogin}
        handleLoginClose={handleLoginClose}
        setLoggedIn={setLoggedIn}
      />
      <Register
        showRegister={showRegister}
        handleRegisterClose={handleRegisterClose}
      />
      <BecomeAuthor
        showBecomeAuthor={showBecomeAuthor}
        handleBecomeAuthorClose={handleBecomeAuthorClose}
      />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route exact path="/my-books" element={<MyBooks />} />
        <Route exact path="/my-books/view-branches" element={<ViewBranches />} />
        <Route exact path="/create-new-book/:reqId" element={<NewBook />} />
        <Route exact path="/books/:id" element={<BookPage />} />
        <Route exact path="/my-books/:bookId/manage" element={<ManageBook />} />
        <Route
          exact
          path="/my-books/:bookId/manage/:chapterId"
          element={<EditChapter />}
        />
        <Route
          exact
          path="/books/:bookId/read/:chapterId"
          element={<ReadChapter />}
        />
      </Routes>
    </Router>
  );
};

export default App;
