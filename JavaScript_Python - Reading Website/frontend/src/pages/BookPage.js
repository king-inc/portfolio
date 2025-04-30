import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { Nav, Button, Modal, Form } from "react-bootstrap";
import api from "../api";
import Card from "react-bootstrap/Card";
import ListGroup from "react-bootstrap/ListGroup";

const BookPage = () => {
  const { id } = useParams();
  const [book, setBook] = useState(null);
  const [chapters, setChapters] = useState([]);
  const [error, setError] = useState(null);
  const [showRequest, setShowRequest] = useState(false);
  const [requestSummary, setRequestSummary] = useState("");
  const [requestInfo, setRequestInfo] = useState("");

  const handleClose = () => setShowRequest(false);
  const handleShow = () => setShowRequest(true);

  useEffect(() => {
    const fetchBookDetails = async () => {
      try {
        const b_response = await api.get(`/api/books/${id}`);
        const c_response = await api.get(`/api/books/${id}/chapters`);
        setBook(b_response.data);
        setChapters(c_response.data.chapters);
      } catch (err) {
        console.error("Error fetching book details:", err);
        setError("Could not fetch book details.");
      }
    };
    fetchBookDetails();
  }, [id]);

  const submitRequest = async () => {
    try {
      const response = await api.post(
        `/api/books/${id}/branch-request`,
        {
          request_summary: requestSummary,
          request_info: requestInfo,
        },
        {
          headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
        }
      );
      handleClose();
      setRequestInfo('');
      setRequestSummary('');
    } catch (err) {
      console.error("Error submitting request", err);
    }
  }

  if (error) return <div>{error}</div>;
  if (!book) return <div>Loading...</div>;
  return (
    <>
      <Card style={{ width: "500px", height: "600px", justifySelf: "center" }}>
        <Card.Img
          variant="top"
          src={`http://127.0.0.1:5000/uploads/${book.image_filename}`}
        />
        <Card.Body>
          <Card.Title>{book.title}</Card.Title>
          <Card.Text>
            <p>Author: {book.author.username}</p>
            <p>Summary: {book.content}</p>
          </Card.Text>
        </Card.Body>
        <ListGroup className="list-group-flush">
          {chapters.map((chapter) => (
            <Nav.Link href={`/books/${id}/read/${chapter.id}`}>
              <ListGroup.Item>
                Chapter {chapter.id}, {chapter.title}
              </ListGroup.Item>
            </Nav.Link>
          ))}
        </ListGroup>
        <Card.Body>
          <Nav.Link onClick={handleShow}>
            Feeling Inspired? Click here to create a spin off{" "}
          </Nav.Link>
        </Card.Body>
      </Card>
      <Modal show={showRequest} onHide={handleClose} size="lg" centered>
        <Modal.Header closeButton>
          <Modal.Title>{book.title}'s Branch Request</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <Form.Group>
              <Form.Label>Spinoff Idea</Form.Label>
              <Form.Control
                as="textarea"
                rows={3}
                placeholder="Epic idea"
                value={requestSummary}
                onChange={(e) => setRequestSummary(e.target.value)}
              />
            </Form.Group>
            <Form.Group>
              <Form.Label>
                What part of this book do you need for this spinoff?
              </Form.Label>
              <Form.Control
                placeholder="e.g.World setting or spinoff of  certain characters"
                value={requestInfo}
                onChange={(e) => setRequestInfo(e.target.value)}
              />
            </Form.Group>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button onClick={submitRequest}>
            Submit
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
};

export default BookPage;
