import React from 'react';
import { withFormik, Form, Field, withRouter, setNestedObjectValues } from 'formik'
import { useNavigate } from 'react-router';
import * as Yup from 'yup';
const API_URL = "https://localhost";

const RegisterPage = (props) => {

    const {
        values,
        touched,
        errors,
        status,
        handleChange,
        handleBlur,
        handleSubmit,
        setErrors,
        isSubmitting,
    } = props;
    const navigate = useNavigate()
    console.log(status)
    if (status && status.data && status.data.access_token) {
        localStorage.setItem("user", JSON.stringify(status.data));
        navigate('/profile')
        window.location.reload();
    }
    return (
        <React.Fragment>

            <div className="col-md-12">
                <div className="card card-container">
                    <h2>Register Page</h2>
                    <Form className="form-container">
                        <div className="form-group">
                            <label htmlFor="username">Username</label>
                            <Field type="text" name="username" className={"form-control"} placeholder="username" />
                            {touched.username && errors.username && <span className="help-block text-danger">{errors.username}</span>}
                        </div>
                        <div className="form-group">
                            <label htmlFor="email">Email</label>
                            <Field type="text" name="email" className={"form-control"} placeholder="email" />
                            {touched.email && errors.email && <span className="help-block text-danger">{errors.email}</span>}
                        </div>
                        <div className="form-group">
                            <label htmlFor="password">Password</label>
                            <Field type="password" name="password" className={"form-control"} placeholder="Password" />
                            {touched.password && errors.password && <span className="help-block text-danger">{errors.password}</span>}
                        </div><br></br>
                        <button type="submit" className="btn btn-primary" formAction='user'>Register</button>
                        {errors.submit && <div className="alert alert-danger" role="alert"> {errors.submit} </div>}
                    </Form><br></br>
                </div>
            </div>

        </React.Fragment>
    )
}

const RegisterFormik = withFormik({

    mapPropsToValues: (props) => {
        return {
            username: props.username || '',
            email: props.email || '',
            password: props.password || ''
        }
    },
    validationSchema: Yup.object().shape({
        username: Yup.string().required('Username is required'),
        email: Yup.string().email('Email is not valid').required('Email is required'),
        password: Yup.string().required('Password is required')
    }),
    handleSubmit: (values, { setSubmitting, setErrors, setStatus }) => {
        console.log(values);
        console.log(window.location.pathname);

        const request = async () => {
            console.log('Fetch register...')
            try {
                let res = await fetch(`${API_URL}/api/auth/signup`, {
                    method: 'post',
                    headers: new Headers({
                        'Content-Type': 'application/json'
                    }),
                    body: JSON.stringify(values)
                })
                let data = await res.json()
                console.log(data);

                if (res.status != 200) {
                    setErrors({ submit: data })
                    setSubmitting(false);
                    return null;
                };
                setSubmitting(false);
                setStatus({data: data});
            } catch (error) {
                console.log('Eror')
                console.log(error);
                setSubmitting(false);
                setErrors({ submit: error.message });
            }
        }
        request()
    }
})(RegisterPage)

export default function Register() {
    return (
        <RegisterFormik />
    )
}