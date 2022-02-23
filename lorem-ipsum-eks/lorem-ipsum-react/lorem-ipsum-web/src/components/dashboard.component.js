import { Row, Col } from 'react-bootstrap';

import React, { useState } from "react";
import { Pie } from "react-chartjs-2";
import { CDBContainer } from "cdbreact";

const Dashboard = () => {

  const [data] = useState({
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
        label: "My First dataset",
        backgroundColor: "rgba(194, 116, 161, 0.5)",
        borderColor: "rgb(194, 116, 161)",
        data: [65, 59, 90, 81, 56, 55, 40],
      },
      {
        label: "My Second dataset",
        backgroundColor: "rgba(71, 225, 167, 0.5)",
        borderColor: "rgb(71, 225, 167)",
        data: [28, 48, 40, 19, 96, 27, 100],
      },
    ],
  })

  return (
    <>
      <Row className="text-info text-center">
        <Col>
          <h1>Total Books</h1>
        </Col>
        <Col>
          <h1>Total Pages</h1>
        </Col>
        <Col>
          <h1>Total Words</h1>
        </Col>
      </Row>
      <CDBContainer>
        <h3 className="mt-5">Word stats</h3>
        <Pie data={data} options={{ responsive: true }} />
      </CDBContainer>
    </>
  );
}

export default Dashboard;

