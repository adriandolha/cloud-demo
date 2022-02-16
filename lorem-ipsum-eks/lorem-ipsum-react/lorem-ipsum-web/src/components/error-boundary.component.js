import React, { Component } from "react";
import Alert from 'react-bootstrap/Alert';
function ErrorScreen({ error }) {
  //
  // Here you can handle or track the error before rendering the message
  //

  return (
    <div className="error">
      <Alert variant="danger">
        <Alert.Heading>We are sorry... something went wrong</Alert.Heading>
        <p>
          We cannot process your request at this moment.
        </p>
        <hr />
        <p className="mb-0">
          {error.message}
        </p>

      </Alert>
    </div>
  );
}

export default class ErrorBoundary extends Component {
  state = { error: null };

  static getDerivedStateFromError(error) {
    return { error };
  }

  render() {
    const { error } = this.state;
    const { children, fallback } = this.props;

    if (error && !fallback) return <ErrorScreen error={error} />;
    if (error) return <fallback error={error} />;

    return children;
  }
}