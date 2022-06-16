import { withFormik, Form, Field } from 'formik';
import * as Yup from 'yup';
import { useState, useEffect } from 'react';
import UserService from '../services/user.service';
import { Modal, Button } from "react-bootstrap"


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

        <div className="row" >
            <div className='col-2'></div>
            <div className='col-8'>
                <Form>
                    <div className="form-group row">
                        <label htmlFor="username" className="col-4 col-form-label">Username
                        </label>
                        <div className="col-4">
                            <Field type="text" name="username" className="form-control-sm" />
                        </div>
                        {touched.username && errors.username && <span className="ms-1 help-block text-danger">{errors.username}</span>}
                    </div>
                    <div className="form-group row">
                        <label htmlFor="email" className="col-4 col-form-label">Email
                        </label>
                        <div className="col-4">
                            <Field type="text" name="email" className="form-control-sm" />
                        </div>
                        {touched.email && errors.email && <span className="ms-1 help-block text-danger">{errors.email}</span>}

                    </div>
                    <div className="form-group row">
                        <label htmlFor="password" className="col-4 col-form-label">Password</label>
                        <div className="col-4">
                            <Field type="password" name="password" className="form-control-sm" />
                        </div>
                        {touched.password && errors.password && <span className="ms-1 help-block text-danger">{errors.password}</span>}
                    </div>

                    <div className="form-group row">
                        <label htmlFor="role" className="col-4 col-form-label">Role</label>
                        <div className="col-4">
                            <Field as="select" name="role" className="form-control-sm " >
                                {roles && roles.items.map(role => (
                                    <option value={role.name} key={role.name}>{role.name}</option>
                                ))}
                            </Field>
                        </div>
                        {touched.role && errors.role && <span className="ms-1 help-block text-danger">{errors.role}</span>}
                    </div>
                    <div className="form-group row">
                        <div className="">
                            <button type="submit" className="btn btn-primary">Add</button>
                            <button type="secondary" onClick={props.onClose} className="ms-2 btn btn-secondary">Close</button>


                        </div>
                    </div>
                </Form>

                {errors && errors.submit && <span className="d-block alert alert-danger mt-3 mb-3 ml-2 pb-1 pt-1" role="alert"> {errors.submit.message} </span>}
            </div>
        </div>
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
        console.log(values.role)
        console.log(props.roles)

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



export default function AddUser({ onSave, roles, handleClose, show }) {
    const [error, setError] = useState()

    return (
        <Modal show={show} onHide={handleClose} animation={false} size="md" aria-labelledby="contained-modal-title-vcenter" centered>
            <Modal.Header className="flex-column text-left text-dark bg-light">
                <Modal.Title className="col-md-11 ms-5">Add new user</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <AddUserFormik onSave={onSave} roles={roles} onClose={handleClose} />
            </Modal.Body>
        </Modal>
    )
}