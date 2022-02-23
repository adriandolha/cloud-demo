import React, { useEffect, useState } from 'react'
import { withFormik, Form, Field } from 'formik'
import Spinner from 'react-bootstrap/Spinner';
import { useNavigate } from 'react-router';
import { useSearchParams } from 'react-router-dom';
import * as Yup from 'yup';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'

const LoginPage = (props) => {
    const API_URL = "https://localhost";
    const GOOGLE_LOGIN_URL = "https://localhost/api/auth/google/login"
    const navigate = useNavigate()

    const {
        values,
        touched,
        errors,
        setFieldValue,
        handleSubmit,
        isSubmitting,
        setStatus,
        status
    } = props;

    const [data, setData] = useState()
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(false)
    const [searchParams] = useSearchParams();
    console.log(searchParams.get('state'));
    const state = searchParams && searchParams.get('state');

    useEffect(() => {
        let queryString = searchParams.toString();
        if (state) {
            console.log(queryString);
            fetch(`${API_URL}/api/auth/google/token?${queryString}`, {
                method: 'get',
                headers: new Headers({
                    'Content-Type': 'application/json'
                })
            })
                .then(data => data.json())
                .then(setData)
                .then(() => setLoading(false))
                .catch((error) => {
                    console.log(error);
                    setError(error);
                });
        }
    }, [state]);


    if (isSubmitting) {
        console.log('Fetch login...')
        let loginType = values.login_type
        console.log(loginType)
        if (loginType === 'google') {
            window.location.href = GOOGLE_LOGIN_URL
        } else {
            login();

        }

    }

    if (data) {
        console.log(data)
        if (data.access_token) {
            localStorage.setItem("user", JSON.stringify(data));
            navigate('/profile')
            window.location.reload();
        }
    }
    if (loading && isSubmitting) {
        return <Spinner animation="border" />
    }

    return (
        <React.Fragment>
            <div className="col-md-12">

                <div className="card card-container bg-light">
                    <h2>Login Page</h2>
                    <Form >
                        <div className="form-group">
                            <label htmlFor="username">Username</label>
                            <Field type="text" name="username" className={"form-control"} placeholder="username" />
                            {touched.username && errors.username && <span className="help-block text-danger">{errors.username}</span>}
                        </div>
                        <div className="form-group">
                            <label htmlFor="password">Password</label>
                            <Field type="password" name="password" className={"form-control"} placeholder="Password" />
                            {touched.password && errors.password && <span className="help-block text-danger">{errors.password}</span>}
                        </div>
                        <button type="submit" className="btn btn-primary me-2">Login</button>

                        <button type="submit" className="btn btn-success" onClick={() => {
                            setFieldValue('login_type', 'google')
                            handleSubmit(values, props)
                        }}>
                            <FontAwesomeIcon icon={['fab', 'google']} />
                            <span className="ms-1">
                                Login
                            </span>
                        </button>

                    </Form>
                    {error && <div className="alert alert-danger mt-2" role="alert"> {error.message} </div>}
                </div>
            </div>

        </React.Fragment>
    )

    function login() {
        fetch(`${API_URL}/api/auth/signin`, {
            method: 'post',
            headers: new Headers({
                'Content-Type': 'application/json'
            }),
            body: JSON.stringify(values)
        })
            .then(data => data.json())
            .then(setData)
            .then(() => setLoading(false))
            .catch((error) => {
                console.log(error);
                setError(error);
            });
    }
    function googleLogin() {
        fetch(`${API_URL}/api/auth/signin`, {
            method: 'post',
            headers: new Headers({
                'Content-Type': 'application/json'
            }),
            body: JSON.stringify(values)
        })
            .then(data => data.json())
            .then(setData)
            .then(() => setLoading(false))
            .catch((error) => {
                console.log(error);
                setError(error);
            });
    }
}

const LoginFormik = withFormik({

    mapPropsToValues: (props) => {
        return {
            username: props.username || '',
            password: props.password || ''
        }
    },
    validationSchema: Yup.object().shape({
        username: Yup.string().required('Username is required'),
        password: Yup.string().required('Password is required')
    }),
    handleSubmit: (values, props) => {
        console.log(values);
        props.setSubmitting(false);
    }
})(LoginPage)



export default function Login() {
    return (
        <LoginFormik />
    )
}