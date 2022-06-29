import { withFormik, Form, Field } from 'formik';
import * as Yup from 'yup';
import { useState } from 'react';
import UserService from '../services/user.service';


function AddPermissionPage(props) {
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
    return (
        <>
            <div className="mb-2 me-1 d-inline-flex" >
                <Form>
                    <label htmlFor="name" className="me-2 flex-column">Permission name: 
                        <Field type="text" name="name" className="ml-1" />
                    </label>

                    <button type="submit" className="btn btn-primary btn-sm ms-0 mb-3 mt-3"> Add </button>
                    {touched.name && errors.name && <span className="ms-1 help-block text-danger">{errors.name}</span>}
                </Form>
                {errors && errors.submit && <span className="d-block alert alert-danger mt-3 mb-3 ml-2 pb-1 pt-1" role="alert"> {errors.submit.message} </span>}
            </div>
        </>
    )
}

const AddPermissionFormik = withFormik({

    mapPropsToValues: (props) => {
        return {
            name: props.name || ''
        }
    },
    validationSchema: Yup.object().shape({
        name: Yup.string().required('Permission name is required').min(5).max(100),
    }),
    handleSubmit: (values, { setSubmitting, setErrors, setStatus, props }) => {
        console.log('Add permission...')
        UserService.add_permission(values.name)
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
})(AddPermissionPage)



export default function AddPermission({ onSave }) {
    return (
        <AddPermissionFormik onSave={onSave} />
    )
}