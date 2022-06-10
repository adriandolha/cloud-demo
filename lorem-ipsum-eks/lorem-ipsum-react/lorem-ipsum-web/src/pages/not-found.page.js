import React from 'react';
import { Row, Col } from 'react-bootstrap';

const NotFoundPage = () => {
    return (
        <Row>
            <Col>
                <div className="text-center m-5 align-items-center justify-content-center">
                    <h1>
                        Oops!</h1>
                    <h2>
                        404 Not Found</h2>
                    <div className="m-1">
                        Sorry, an error has occured, Requested page not found!
                    </div>
                    <div className="mt-2">
                        <a href="/home" className="btn btn-primary btn-lg"><span><i className="fas fa-solid fa-home pe-1"></i></span>
                            Take Me Home </a>
                    </div>
                </div>
            </Col>
        </Row>
    )
}
export default NotFoundPage;