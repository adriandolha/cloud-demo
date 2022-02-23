import { Modal, Button, Row, Col, Container, Carousel } from "react-bootstrap"
import { useState } from 'react'
import BookService from '../services/books.service';


function BookView({ book_data, show, handleClose, handleSave }) {
    const book_json = JSON.parse(book_data.book);
    const book_text = Object.values(book_json).map(page => page.reduce((prev, crt) => prev + "\n" + crt));
    const book = {
        title: book_data.title,
        author: book_data.author,
        pages: book_text
    };
    const [error, setError] = useState();
    const [data, setData] = useState();
    const [loading, setLoading] = useState();
    const pageCount = book.pages.length
    const _handleSave = () => {
        setLoading(true)
        BookService.add(book_data)
            .then(res => {
                if (!res.ok) {
                    return res.json().then(message => { setLoading(false); throw new Error(message); })
                }
                return res.json();
            })
            .then(handleSave)
            .then(() => setLoading(false))
            .catch((error) => {
                console.log(`Error: ${error}`);
                setError(error);
            });
    }

    return (
        <>
            <Modal show={show} onHide={handleClose} animation={false} size="xl" aria-labelledby="contained-modal-title-vcenter" centered>
                <Modal.Header className="flex-column text-left text-dark bg-light">
                    <Modal.Title className="col-md-11 ms-5">{book.title}</Modal.Title>
                    {/* <h1 className="bg-light text-dark col-md-11 ms-5 ">{book.title}</h1> */}
                    <h6 className=" font-italic col-md-11 ms-5 ">{book.author}</h6>
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
                    {error && <div className="alert alert-danger" role="alert"> {error.message} </div>}
                    <span className={loading ? "visible" : "invisible"}>
                        <i className="fas fa-spinner action fa-spin"></i>
                    </span>
                    <div className="btn-group" role="group" aria-label="Basic example">
                        {handleSave &&
                            <Button variant="primary" onClick={_handleSave}>
                                Save
                            </Button>
                        }
                        <Button variant="secondary" onClick={handleClose}>
                            Close
                        </Button>
                    </div>
                </Modal.Footer>
            </Modal>
        </>
    );
}

export default BookView;