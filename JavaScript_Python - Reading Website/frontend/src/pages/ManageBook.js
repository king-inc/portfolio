import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { Container, Nav, ListGroup, Button } from "react-bootstrap";
import Card from "react-bootstrap/Card";
import api from "../api";

const ManageBook = () => {
  const { bookId } = useParams();
  const [chapters, setChapters] = useState([]);

  useEffect(() => {
    const fetchChapters = async () => {
      try {
        const response = await api.get(`/api/books/${bookId}/chapters`);
        setChapters(response.data.chapters);
      } catch (err) {
        console.error("Error fetching chapters:", err);
      }
    };
    fetchChapters();
  }, [bookId]);

  return (
    <Container className="manage-book">
      <h2>Manage Book</h2>
      <Container>
        <h3>Book Details</h3>
        <p>Book Title: {}</p>
        <p>Branches: {}</p>
        <Button>View Branches</Button>
        <p />
      </Container>
      <Container>
        <h3>Chapters</h3>
        <ListGroup className="list-group-flush">
          <Nav.Link href={`/my-books/${bookId}/manage/${chapters.length + 1}`}>
            <Card body>Add New Chapter, Chapter {chapters.length + 1}</Card>
          </Nav.Link>
          {chapters.map((chapter) => (
            <Nav.Link href={`/my-books/${bookId}/manage/${chapter.id}`}>
              <Card body>
                Chapter {chapter.id}, {chapter.title}
              </Card>
            </Nav.Link>
          ))}
        </ListGroup>
      </Container>
    </Container>
  );
};

export default ManageBook;
