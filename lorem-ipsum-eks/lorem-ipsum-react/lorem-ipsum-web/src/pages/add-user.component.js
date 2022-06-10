import { withFormik, Form, Field } from 'formik';
import * as Yup from 'yup';
import { useState, useEffect } from 'react';
import UserService from '../services/user.service';


function AddUserPage(props) {
    const {
        values,
        touched,
        errors,
        setFieldValue,
        handleSubmit,
        handleReset,
        isSubmitting,
        setSubmitting,
        setStatus,
        status,
        onSave
    } = props;
    const [error, setError] = useState(false)
    const [roles, setRoles] = useState()
    const fetch_roles = () => {
        UserService.get_roles()
            .then(res => {
                if (!res.ok) {
                    return res.json().then(message => { throw new Error(message); });
                }
                return res.json();
            })
            .then((res) => {
                setRoles(res)
            })
            .catch((error) => {
                console.log(`Error: ${error}`);
                setError(error);
            });
    }

    useEffect(() => {
        fetch_roles();
    }, []);

    return (
        <>
            <div className="mb-2 me-1 col-4 flex-column" >
                <Form>
                    <label htmlFor="username" className="me-2 d-block">Username:
                        <Field type="text" name="username" className="ml-1 float-right" />
                    </label>
                    {touched.username && errors.username && <span className="ms-1 help-block text-danger">{errors.username}</span>}

                    <label htmlFor="email" className="me-2 d-block">Email:
                        <Field type="text" name="email" className="ml-1 float-right" />
                    </label>
                    <label htmlFor="password" className="me-2 d-block">Password:
                        <Field type="password" name="password" className="ml-1 float-right" />
                    </label>
                    {touched.password && errors.password && <span className="ms-1 help-block text-danger">{errors.password}</span>}

                    <label htmlFor="role" className="me-2 d-block">Role:
                        <Field as="select" name="role" className="float-right form-select-sm d-inline" >
                            {roles && roles.items.map(role => (
                                <option value={role} key={role.name}>{role.name}</option>
                            ))}
                        </Field>
                    </label>
                    {touched.role && errors.role && <span className="ms-1 help-block text-danger">{errors.role}</span>}

                    <button type="submit" className="btn btn-primary btn-sm ms-0 mb-3 mt-3">Add</button>
                </Form>
                {errors && errors.submit && <span className="d-block alert alert-danger mt-3 mb-3 ml-2 pb-1 pt-1" role="alert"> {errors.submit.message} </span>}
            </div>
        </>
    )
}

const AddUserFormik = withFormik({

    mapPropsToValues: (props) => {
        return {
            username: props.username || '',
            email: props.email || '',
            password: props.password || '',
            role: props.role || 'ROLE_USER'
        }
    },
    validationSchema: Yup.object().shape({
        username: Yup.string().required('Username is required').min(5).max(100),
        password: Yup.string().required('Password is required').min(10).max(100),
        email: Yup.string().email('Invalid email format').required('Email is required'),
        role: Yup.string().required('Role is required'),
    }),
    handleSubmit: (values, { setSubmitting, setErrors, setStatus, props }) => {
        console.log('Add user...')
        const [existing_role] = props.roles.items.filter(role => role.name == values.role)
        const user = {
            username: values.username,
            email: values.email,
            password: values.password,
            role: existing_role
        }
        console.log(user)

        UserService.add_user(user)
            .then(res => {
                if (!res.ok) {
                    return res.json().then(message => { throw new Error(message); })
                }
                return res.json();
            })
            .then(data => {
                props.onSave()
            })
            .catch((error) => {
                console.log(`Error: ${error}`);
                setSubmitting(false);
                setErrors({ submit: error });
            });
    }
})(AddUserPage)



export default function AddUser({ onSave }) {
    const [roles, setRoles] = useState()
    const [error, setError] = useState()
    const fetch_roles = () => {
        UserService.get_roles()
            .then(res => {
                if (!res.ok) {
                    return res.json().then(message => { throw new Error(message); });
                }
                return res.json();
            })
            .then((res) => {
                setRoles(res)
            })
            .catch((error) => {
                console.log(`Error: ${error}`);
                setError(error);
            });
    }

    useEffect(() => {
        fetch_roles();
    }, []);
    return (
        <AddUserFormik onSave={onSave} roles={roles} />
    )
}