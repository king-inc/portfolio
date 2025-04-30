import React, { useState, useEffect } from "react";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import api from "../api";
import { useNavigate, useParams } from "react-router-dom";
import Container from "react-bootstrap/esm/Container";

const NewBook = () => {
  const { reqId } = useParams();
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [image, setImage] = useState(null);
  const [branchInfo, setBranchInfo] = useState("");
  const [originId, setOriginId] = useState(0);
  const navigate = useNavigate();

  useEffect(() => {
    const getRequest = async () => {
      if (reqId > 0) {
        try {
          const response = await api.get(
            `/api/my-books/branch-requests/${reqId}`
          );
          setTitle(response.data.title);
          setContent(response.data.request_summary);
          setBranchInfo(response.data.request_info);
          setOriginId(response.data.origin_id);
        } catch (err) {
          console.error("Error fetching request:", err);
        }
      }
    };
    getRequest();
  }, [reqId]);

  const handleCreateBook = async () => {
    const formData = new FormData();
    formData.append("title", title);
    formData.append("content", content);
    formData.append("req_id", reqId);
    formData.append("origin_book_id", originId);
    formData.append("branch_info", branchInfo);
    if (image) {
      formData.append("image", image); // Attach the image file if selected
    }

    try {
      await api.post("/api/create-book", formData, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
          "Content-Type": "multipart/form-data",
        },
      });
      navigate("/my-books");
      //setTitle("");
      //setContent("");
      //setImage(null);
      //alert("Book created succesfully");
    } catch (err) {
      console.error("Error creating book:", err);
    }
  };

  return (
    <Container className="justify-content-center box">
      <span className="justify-content-center">
        <h3>Create New Book</h3>
      </span>
      <Form onSubmit={handleCreateBook}>
        <Form.Group className="mb-3">
          <Form.Label>Book Title</Form.Label>
          <Form.Control
            type="text"
            placeholder="Epic title"
            value={title}
            onChange={(e) => {
              setTitle(e.target.value);
            }}
          />
        </Form.Group>

        <Form.Group className="mb-3">
          <Form.Label>Book Description</Form.Label>
          <Form.Control
            as="textarea"
            rows={3}
            id="desc"
            placeholder="Epic description"
            value={content}
            onChange={(e) => setContent(e.target.value)}
          />
        </Form.Group>
        <Form.Group controlId="formFile" className="mb-3">
          <Form.Label>Upload Cover Photo</Form.Label>
          <Form.Control
            type="file"
            onChange={(e) => setImage(e.target.files[0])}
            accept="image/*"
          />
        </Form.Group>
        <Button variant="primary" type="submit">
          Submit
        </Button>
      </Form>
    </Container>
  );
};

export default NewBook;
