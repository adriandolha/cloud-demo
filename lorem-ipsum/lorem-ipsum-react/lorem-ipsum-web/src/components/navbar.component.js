import { Link } from "react-router-dom";
import AuthService from "../services/auth.service";
import { useEffect, useState } from 'react';

const NavBar = () => {
    const [currentUser, setCurrentUser] = useState();
    useEffect(() => {
        const user = AuthService.getCurrentUser();
        user && setCurrentUser(user);
    }, []);
    return (
        <nav className="navbar navbar-expand navbar-dark bg-primary ms-0 justify-content-md-end" style={{"background-color": "#e3f2fd"}}>
            <div className="navbar-nav">
                <li className="nav-item">
                    <Link to={"/home"} className="nav-link">
                        Home
                    </Link>
                </li>

            </div>

            {currentUser ? (
                <div className="navbar-nav">
                    <li className="nav-item">
                        <Link to={"/books"} className="nav-link">
                            Books
                        </Link>
                    </li>

                    <li className="nav-item">
                        <Link to={"/users"} className="nav-link">
                            Users
                        </Link>
                    </li>

                    <li className="nav-item ">
                        <Link to={"/roles"} className="nav-link">
                            Roles
                        </Link>
                    </li>
                    <li className="nav-item d-none d-sm-block">
                        <Link to={"/permissions"} className="nav-link">
                            Permissions
                        </Link>
                    </li>
                    <li className="nav-item">
                        <Link to={"/profile"} className="nav-link">
                            Profile
                        </Link>
                    </li>
                    <li className="nav-item">
                        <a href="/login" className="nav-link" onClick={() => { AuthService.logout() }}>
                            LogOut
                        </a>
                    </li>
                </div>
            ) : (
                <div className="navbar-nav">
                    <li className="nav-item">
                        <Link to={"/login"} className="nav-link">
                            Login
                        </Link>
                    </li>

                    <li className="nav-item">
                        <Link to={"/register"} className="nav-link">
                            Sign Up
                        </Link>
                    </li>
                </div>
            )}
        </nav>
    )
}

export default NavBar;