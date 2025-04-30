import React from "react";
import api from "../api";
import { useNavigate } from "react-router-dom";
import Modal from "react-bootstrap/Modal";
import Button from "react-bootstrap/Button";

const BecomeAuthor = ({ showBecomeAuthor, handleBecomeAuthorClose }) => {
  const navigate = useNavigate();

  const handleBecomeAuthor = async () => {
    try {
      await api.post(
        "/auth/become-author",
        {},
        {
          headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
        }
      );
      handleBecomeAuthorClose();
      navigate("/my-books"); // Redirect to My Books after becoming an author
    } catch (err) {
      console.error("Error becoming an author:", err);
    }
  };

  return (
    <Modal
      show={showBecomeAuthor}
      onHide={handleBecomeAuthorClose}
      size="lg"
      aria-labelledby="contained-modal-title-vcenter"
      centered
    >
      <Modal.Header closeButton>
        <Modal.Title id="contained-modal-title-vcenter">
          Become an Author
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Button variant="primary" onClick={handleBecomeAuthor}>
          Confirm
        </Button>
      </Modal.Body>
    </Modal>
  );
};

export default BecomeAuthor;
