import React, { useState, useEffect, useRef } from "react";
import { useParams } from "react-router-dom";
import { Editor } from "@tinymce/tinymce-react";
import { plugins } from "../constants/plugins";
import { toolbars } from "../constants/toolbars";
import { Container } from "react-bootstrap";
import Button from "react-bootstrap/Button";
import Col from "react-bootstrap/Col";
import Form from "react-bootstrap/Form";
import Row from "react-bootstrap/Row";
import api from "../api";

const EditChapter = () => {
  const { bookId, chapterId } = useParams();
  const [chapter, setChapter] = useState({});
  const [chapterTitle, setChapterTitle] = useState("");
  const editorRef = useRef(null);
  const [chapterContent, setChapterContent] = useState("");
  const [newChapterContent, setNewChapterContent] = useState("");

  useEffect(() => {
    const fetchChapter = async () => {
      try {
        const response = await api.get(
          `/api/books/${bookId}/chapter/${chapterId}`
        );
        setChapter(response.data);
        setChapterTitle(response.data.title);
        setChapterContent(response.data.content);
      } catch (err) {
        console.error("Error fetching chapters:", err);
      }
    };
    fetchChapter();
  }, [bookId, chapterId]);

  const submitChapter = async () => {
    try {
      const response = await api.post(
        `/api/books/${bookId}/chapter/${chapterId}`,
        {
          title: chapterTitle,
          content: newChapterContent,
        },
        {
          headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
        }
      );
    } catch (err) {
      console.error("Error adding chapter:", err);
    }
  };

  function updateChapterContent() {
    let content = editorRef.current.getContent();
    setNewChapterContent(content)
  }

  return (
    <Container centered="true">
      <span>
        <br />
        <Form>
          <Row>
            <Col xs={7}>
              <Form.Control
                size="lg"
                type="text"
                onChange={(e) => {
                  setChapterTitle(e.target.value);
                }}
                placeholder={
                  chapterTitle === "" ? "Set Chapter Title" : chapterTitle
                }
              />
            </Col>
          </Row>
        </Form>
        <br />
      </span>
      <Editor
        apiKey="88pb83a1e7lg1vuj66gj6osihy71r5ebdtldqvohimk45a8s"
        onInit={(evt, editor) => editorRef.current = editor}
        initialValue={chapterContent}
        onEditorChange={updateChapterContent}
        init={{ plugins: plugins, toolbar: toolbars }}
      />
      <Button onClick={() => submitChapter()}> Add Chapter</Button>
    </Container>
  );
};

export default EditChapter;
