import React, { useState, useEffect } from "react";
import {
  Button,
  ButtonGroup,
  Col,
  Row,
  Nav,
  Container,
  ListGroup,
} from "react-bootstrap";
import api from "../api";

const ViewBranches = () => {
  const [ownRequests, setOwnRquests] = useState([]);
  const [authorRequests, setAuthorRquests] = useState([]);

  useEffect(() => {
    const fetchRequests = async () => {
      try {
        const response = await api.get("/api/my-books/branch-requests", {
          headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
        });
        setOwnRquests(response.data.own);
        setAuthorRquests(response.data.author);
      } catch (err) {
        console.error("Error fetching branches:", err);
      }
    };
    fetchRequests();
  }, []);

  const handleAuthorRequest = async (id, status) => {
    try {
      const response = await api.patch(
        `/api/branch-requests/${id}`,
        { status },
        {
          headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
        }
      );
      setAuthorRquests(authorRequests.filter((req) => req.id !== id));
    } catch (error) {
      console.error("Error updating branch request", error);
    }
  };

  return (
    <div>
      <Container>
        <h3>Your Branch Requests</h3>
        <ListGroup>
          <ListGroup.Item>
            <Row>
              <Col>Book Title</Col>
              <Col>Request Info</Col>
              <Col>Status</Col>
            </Row>
          </ListGroup.Item>
          {ownRequests.map((req) => (
            <>
              {req.status === "pending" ? (
                <ListGroup.Item>
                  <Row>
                    <Col>{req.book_title}</Col>
                    <Col>{req.request_info}</Col>
                    <Col>{req.status}</Col>
                  </Row>
                </ListGroup.Item>
              ) : (
                <Nav.Link href={`/create-new-book/${req.id}`}>
                  <ListGroup.Item>
                    <Row>
                      <Col>{req.book_title}</Col>
                      <Col>{req.request_info}</Col>
                      <Col>{req.status}</Col>
                    </Row>
                  </ListGroup.Item>
                </Nav.Link>
              )}
            </>
          ))}
        </ListGroup>
      </Container>
      {authorRequests.length > 0 ? (
        <Container>
          <h3>Your Books Branch Requests</h3>
          <ListGroup>
            <ListGroup.Item>
              <Row>
                <Col>Book Title</Col>
                <Col>Requester</Col>
                <Col>Request Info</Col>
                <Col>Request Summary</Col>
                <Col>Decision</Col>
              </Row>
              {authorRequests.map((req) => (
                <Row>
                  <Col>{req.book_title}</Col>
                  <Col>{req.requester}</Col>
                  <Col>{req.request_info}</Col>
                  <Col>{req.request_summary}</Col>
                  <Col>
                    <ButtonGroup>
                      <Button
                        onClick={() => handleAuthorRequest(req.id, "accepted")}
                      >
                        Accept
                      </Button>
                      <Button
                        onClick={() => handleAuthorRequest(req.id, "rejected")}
                      >
                        Deny
                      </Button>
                    </ButtonGroup>
                  </Col>
                </Row>
              ))}
            </ListGroup.Item>
          </ListGroup>
        </Container>
      ) : (
        ""
      )}
    </div>
  );
};

export default ViewBranches;
