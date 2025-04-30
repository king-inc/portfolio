import React, { useEffect, useState } from "react";
import api from "../api";
import Container from "react-bootstrap/esm/Container";
import Card from "react-bootstrap/Card";
import { Nav } from "react-bootstrap";

const Home = () => {
  const [books, setBooks] = useState([]);

  useEffect(() => {
    // Fetch books from the backend
    const fetchBooks = async () => {
      try {
        const response = await api.get("/api/books");
        setBooks(response.data);
      } catch (err) {
        console.error("Error fetching books:", err);
      }
    };
    fetchBooks();
  }, []);

  const renderBook = (book, index) => {
    return (
      <Nav.Link key={index} href={`/books/${book.id}`}>
        <Card style={{ width: "18rem" }} className="box">
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
      <h2>All Books</h2>
      <div className="grid">{books.map(renderBook)}</div>
    </Container>
  );
};

export default Home;
