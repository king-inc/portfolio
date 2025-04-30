import React, { useState, useEffect } from "react";
import api from "../api";
import Container from "react-bootstrap/esm/Container";
import Card from "react-bootstrap/Card";
import { Button, Nav } from "react-bootstrap";
import { useNavigate } from "react-router-dom";

const MyBooks = () => {
  const [books, setBooks] = useState([]);
  const original = 0;
  const navigate = useNavigate();

  useEffect(() => {
    const fetchBooks = async () => {
      try {
        const response = await api.get("/api/my-books", {
          headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
        });
        setBooks(response.data);
      } catch (err) {
        console.error("Error fetching books:", err);
      }
    };
    fetchBooks();
  }, []);

  const renderBook = (book, index) => {
    return (
      <Nav.Link key={index} href={`/my-books/${book.id}/manage`}>
        <Card style={{ width: "18rem" }} key={index} className="box">
          <Card.Img
            variant="top"
            src={`http://127.0.0.1:5000/uploads/${book.image}`}
            alt={book.title}
          />
          <Card.Body>
            <Card.Title>{book.title}</Card.Title>
            <Card.Text>{book.content.substring(0, 100)}</Card.Text>
          </Card.Body>
        </Card>
      </Nav.Link>
    );
  };
  return (
    <Container>
      <Button onClick={()=> navigate('/my-books/view-branches')}>View Branches</Button>
      <h2>My Books</h2>
      <div className="grid">
        <Nav.Link href={`/create-new-book/${original}`}>
          <Card
            style={{ width: "18rem", height: "20rem" }}
            key={-1}
            className="box"
          >
            <Card.Body>
              <Card.Title>Create a New Book</Card.Title>
              <Card.Text>Want to start something new? Click here!</Card.Text>
            </Card.Body>
          </Card>
        </Nav.Link>
        {books.map(renderBook)}
      </div>
    </Container>
  );
};

export default MyBooks;
