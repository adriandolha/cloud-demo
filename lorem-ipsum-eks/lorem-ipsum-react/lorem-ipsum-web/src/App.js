import React, { Component } from "react";
import { Routes, Route } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import "@fortawesome/fontawesome-free/css/all.css";
import "@fortawesome/fontawesome-free/js/all.js";
import "./App.css";
import NotFoundPage from "./pages/not-found.page";

import Login from "./components/login.component";
import Register from "./components/register.component";
import Home from "./components/home.component";
import Profile from "./components/profile.component";
import UsersView from "./pages/users-view.component";
import BooksView from "./components/books-view.component";
import Dashboard from './components/dashboard.component';

import Sidebar from './components/sidebar.component';
import NavBar from './components/navbar.component';
import PermissionsView from "./pages/permissions-view.component";
import RolesView from "./pages/roles-view.component";

class App extends Component {
  constructor(props) {
    super(props);
  }



  render() {
    return (
      <div className="d-flex">
        <Sidebar />
        <div className="flex-column ms-0 flex-fill">
          <NavBar></NavBar>
          <div className="container-fluid" style={{ "font-size": '0.83rem' }}>
            <Routes>
              <Route path="/home" element={<Home />} />
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route path="/profile" element={<Profile />} />
              <Route path="/books" element={<BooksView />} />
              <Route path="/users" element={<UsersView />} />
              <Route path="/roles" element={<RolesView />} />
              <Route path="/permissions" element={<PermissionsView />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="*" element={<NotFoundPage />} />

            </Routes>
          </div>
        </div>
      </div>
    );
  }
}

export default App;