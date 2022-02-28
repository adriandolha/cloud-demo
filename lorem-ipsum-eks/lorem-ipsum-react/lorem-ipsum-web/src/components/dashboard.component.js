import { Row, Col, Spinner } from 'react-bootstrap';

import React, { useEffect, useState } from "react";
import { HorizontalBar } from "react-chartjs-2";
import { CDBContainer } from "cdbreact";
import BookService from '../services/books.service';
import WordService from '../services/words.service';
const Dashboard = () => {
  const get_data = (words) => {
    return {
      labels: words.map(word => word.id),
      datasets: [
        {
          label: "Words Frequency",
          backgroundColor: "rgba(71, 225, 167, 0.5)",
          borderColor: "rgb(71, 225, 167)",
          data: words.map(word => word.count),
        }
      ],
    }
  }

  const [{ data, no_of_books, no_of_pages, no_of_words, loading }, setState] = useState({
    data: {
      labels: [
        "Eating",
        "Drinking",
        "Sleeping",
        "Designing",
        "Coding",
        "Cycling",
        "Running",
      ],
      datasets: [
        {
          label: "Words Frequency",
          backgroundColor: "rgba(71, 225, 167, 0.5)",
          borderColor: "rgb(71, 225, 167)",
          data: [65, 59, 90, 81, 56, 55, 40],
        }
      ],
    }, no_of_books: 0, no_of_pages: 0, no_of_words: 0, loading: true
  })
  const state = { data: data, no_of_books: no_of_books, no_of_pages: no_of_pages, no_of_words: no_of_words, loading: loading }
  const fetchData = (setData) => {
    BookService.get_all(1, 0, 'page_count')
      .then(res => res.json())
      .then(new_data => {
        console.log('new data', new_data);
        const book_data = new_data;
        WordService.get_all(20, 0)
          .then(res => res.json())
          .then(words => setData(book_data, words))
          .catch((error) => {
            console.log(`Error: ${error}`);
            // setError(error);
          });
      })
      .catch((error) => {
        console.log(`Error: ${error}`);
      });
  }

  useEffect(() => {
    fetchData((book_data, words) => {
      setState({
        ...state,
        data: get_data(words.items),
        no_of_books: book_data.total,
        no_of_pages: book_data.page_count,
        no_of_words: words.total,
        loading: false,
      });
    });
  }, []);
  if (loading) {
    return <Spinner animation="border" />
  }
  return (
    <>
      <Row className="text-dark text-center bg-light justify-content-around ">
        <Col md={3} className="bg-light m-3">
          <h3 className='text-primary'>Books Count</h3>
          <h5><i className="fas fa-book pe-1"></i>{no_of_books}</h5>
        </Col>
        <Col md={3} className="bg-light m-3">
          <h3 className='text-info'>Pages Count</h3>
          <h5><i className="fas fa-book pe-1"></i>{no_of_pages}</h5>
        </Col>
        <Col md={4} className="bg-light m-3">
          <h3 className='text-danger'>Unique Words Count</h3>
          <h5><i className="fas fa-file-word pe-1"></i>{no_of_words}</h5>
        </Col>
      </Row>
      <CDBContainer>
        <h3 className="mt-5">Top Words<button className='btn btn-lg' onClick={() => {
          console.log('clicked')
          setState({
            ...state,
            loading: true
          });
          fetchData((book_data, words) => {
            setState({
              ...state,
              data: get_data(words.items),
              no_of_books: book_data.total,
              no_of_pages: book_data.page_count,
              no_of_words: words.total,
              loading: false,
            });
          })
        }}><i className="fas fa-sync ps-1"></i></button><i className="fa-solid fa-rotate"></i></h3>
        <HorizontalBar data={data} options={{ responsive: true }} />
      </CDBContainer>
    </>
  );
}

export default Dashboard;


