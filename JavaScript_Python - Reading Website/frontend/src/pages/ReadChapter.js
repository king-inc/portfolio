import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { Container } from "react-bootstrap";
import parse from "html-react-parser";
import api from "../api";

const ReadChapter = () => {
    const { bookId, chapterId } = useParams();
    const [chapter, setChapter] = useState({});
    const [chapterContent, setChapterContent] = useState('')

    useEffect(() => {
        const fetchChapter = async () => {
          try {
            const response = await api.get(
              `/api/books/${bookId}/chapter/${chapterId}`
            );
            setChapter(response.data);
            setChapterContent(response.data.content)
          } catch (err) {
            console.error("Error fetching chapters:", err);
          }
        };
        fetchChapter();
      }, [bookId, chapterId]);
    return (
        <Container>
            <h1>{chapter.title}</h1>
            {parse(chapterContent)}
        </Container>
    );
}

export default ReadChapter;
