import React, { useState, useEffect } from "react";
import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import Navb from "react-bootstrap/Navbar";
//import { useNavigate } from "react-router-dom";
import api from "../api";

const Navbar = ({
  setShowLogin,
  setShowRegister,
  setShowBecomeAuthor,
  loggedIn,
}) => {
  //const navigate = useNavigate();
  const [isAuthor, setIsAuthor] = useState(false);

  useEffect(() => {
    const checkAuthorStatus = async () => {
      if (loggedIn) {
        try {
          const response = await api.get("/auth/is-author", {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("token")}`,
            },
          });
          setIsAuthor(response.data);
        } catch (err) {
          console.error("Error fetching user profile:", err);
        }
      }
    };
    checkAuthorStatus();
  }, [loggedIn]);

  const handleLogout = () => {
    localStorage.removeItem("token");
    //navigate("/login");
  };

  return (
    <Navb
      expand="lg"
      className="bg-dark border-bottom border-body"
      data-bs-theme="dark"
    >
      <Container>
        <Navb.Brand href="/">My Reading Site</Navb.Brand>
        <Navb.Toggle aria-controls="basic-navbar-nav" />
        <Navb.Collapse id="basic-navbar-nav" className="justify-content-end">
          <Nav>
            {loggedIn ? (
              <>
                <Nav.Link href="/profile">User Profile</Nav.Link>
                {isAuthor ? (
                  <Nav.Link href="/my-books">My Books</Nav.Link>
                ) : (
                  <Nav.Link onClick={() => setShowBecomeAuthor(true)}>
                    Become an Author
                  </Nav.Link>
                )}
                <Nav.Link href="/" onClick={handleLogout}>
                  Logout
                </Nav.Link>
              </>
            ) : (
              <>
                <Nav.Link onClick={() => setShowLogin(true)}>Login</Nav.Link>
                <Nav.Link onClick={() => setShowRegister(true)}>
                  Register
                </Nav.Link>
              </>
            )}
          </Nav>
        </Navb.Collapse>
      </Container>
    </Navb>
  );
};

export default Navbar;
