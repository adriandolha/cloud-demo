import { Modal, Button, Row, Col, Container, Carousel } from "react-bootstrap"
import { useState } from 'react'

function BookView({ book_data, show, handleClose }) {
    const book_json = JSON.parse(book_data.book);
    const book_text = Object.values(book_json).map(page => page.reduce((prev, crt) => prev + "\n" + crt));
    const book = {
        title: book_data.title,
        pages: book_text
    };
    const pageCount = book.pages.length

    return (
        <>
            <Modal show={show} onHide={handleClose} size="xl" aria-labelledby="contained-modal-title-vcenter" centered>
                <Modal.Header>
                    <Modal.Title className="bg-dark text-light text-center col-md-11 ms-5">{book.title}</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Carousel>
                        {book.pages.map((page, index) =>
                            <Carousel.Item className="p-5">
                                <Row className="bg-dark text-light p-5">
                                    <p>{page}</p>
                                </Row>
                                <Carousel.Caption className="mb-4">
                                    <h3>Page {index + 1} of {pageCount} </h3>
                                </Carousel.Caption>
                            </Carousel.Item>
                        )}
                    </Carousel>

                </Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={handleClose}>
                        Close
                    </Button>
                </Modal.Footer>
            </Modal>
        </>
    );
}

export default BookView;