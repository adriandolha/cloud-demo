// import { Jumbotron, Button } from 'react-bootstrap'
import AuthService from '../services/auth.service'
import { useNavigate } from 'react-router';
import {Row, Col} from 'react-bootstrap';
function Home(props) {
  const currentUser = AuthService.getCurrentUser();
  const navigate = useNavigate();

  return (
    <div className="jumbotron">
      <h1 className="display-4">Hello, {currentUser.username}!</h1>
      <p className="lead">This is a simple text generator, useful to generate books and get some random content to be used elsewhere.</p>
      <hr className="my-4"/>
        <p>It uses faker library in the backend to generate books with a given number of pages, a random title and random author.</p>
        <p className="lead">
          <a className="btn btn-primary btn-lg" href="#" role="button" onClick={()=>{
            navigate('/books');
            // window.location.reload();
          }}>Let's start!</a>
        </p>
    </div>
  )
}

export default Home;