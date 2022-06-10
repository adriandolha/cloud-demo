import { withFormik, Form, Field, FieldArray } from 'formik';
import * as Yup from 'yup';
import { useState, useEffect } from 'react';
import UserService from '../services/user.service';


function AddRolePage(props) {
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
    const [perms, setPerms] = useState()
    const [selectedPermission, setSelectedPermission] = useState()
    const fetch_permissions = () => {
        UserService.get_permissions()
            .then(res => {
                if (!res.ok) {
                    return res.json().then(message => { throw new Error(message); });
                }
                return res.json();
            })
            .then((res) => {
                setPerms(res)
                setSelectedPermission(res.items[0].name)
            })
            .catch((error) => {
                console.log(`Error: ${error}`);
                setError(error);
            });
    }

    useEffect(() => {
        fetch_permissions();
    }, []);

    const handlePermissionSelect = (e) => {
        console.log(e.target.value)
    }
    return (
        <>
            <div className="mb-2 me-1 d-block col-6" >
                <Form>
                    <div>
                        <label htmlFor="name" className="me-2">Name:</label>
                        <Field type="text" name="name" className="ml-1" />
                        {touched.name && errors.name && <span className="ms-1 help-block text-danger">{errors.name}</span>}

                    </div>
                    <div>
                        <label htmlFor="default" className="me-2">Default:</label>
                        <Field type="checkbox" name="default" />
                    </div>
                    <div>
                        <label htmlFor="permissions" className="me-2">Permissions:</label>
                        <FieldArray name="permissions"
                            render={({ insert, remove, push }) => (
                                <div>
                                    <div className='d-inline-flex'>
                                        <select onChange={(e) => {
                                            setSelectedPermission(e.target.value)
                                        }} onKeyPress={(e) => {
                                            if (e.key === 'Enter') {
                                                const _permission = e.target.value
                                                console.log(`Enter triggered  ${_permission}`)
                                                console.log(values.permissions)
                                                // push({'id':_permission, 'name':_permission})
                                                // insert(values.permissions.length, { 'id': _permission, 'name': _permission })
                                                console.log(values.permissions)
                                            }
                                        }} className="custom-select mr-sm-2" id="inlineFormCustomSelect">
                                            {perms && perms.items.map(perm => (
                                                <option value={perm.name} key={perm.name}>{perm.name}</option>
                                            ))}
                                        </select>
                                        <span className="btn btn-sm btn-rpimary-outline" onClick={() => {
                                            console.log(`Add new role permission ${selectedPermission}`)
                                            const existing_permissions = values.permissions.filter(val => val.name == selectedPermission)
                                            if (existing_permissions.length > 0) {
                                                console.log(`Found ${existing_permissions}`)
                                            } else {
                                                push({ 'id': selectedPermission, 'name': selectedPermission })

                                            }
                                        }}><i className="fas fa-plus action"></i></span>
                                    </div>
                                    <div className="d-flex-inline mt-2">
                                        {values.permissions.length > 0 &&
                                            values.permissions.map((permission, index) => (
                                                <span key={index} className="btn btn-sm btn-primary text-light ms-1 mt-1 pl-1 pt-1 pb-1">
                                                    <i className="fas fa-key action pe-1"></i> {permission.name}
                                                    <button className="btn btn-sm btn-rpimary-outline" onClick={() => {
                                                        remove(index)
                                                    }}><i className="fas fa-trash action"></i></button>
                                                </span>
                                            ))}
                                    </div>
                                </div>
                            )} />
                        {touched.permissions && errors.permissions && <span className="ms-1 help-block text-danger">{errors.permissions}</span>}

                    </div>

                    <button type="submit" className="btn btn-primary btn-sm ms-0 mb-3 mt-3"> Add </button>
                </Form>
                {errors && errors.submit && <span className="d-block alert alert-danger mt-3 mb-3 ml-2 pb-1 pt-1" role="alert"> {errors.submit.message} </span>}
            </div>
        </>
    )
}

const AddRoleFormik = withFormik({

    mapPropsToValues: (props) => {
        return {
            name: props.name || '',
            default: props.default || false,
            permissions: props.permissions || [],
        }
    },
    validationSchema: Yup.object().shape({
        name: Yup.string().required('Role name is required').min(5).max(100),
        default: Yup.bool().required(),
        permissions: Yup.array().min(1).required(),

    }),
    handleSubmit: (values, { setSubmitting, setErrors, setStatus, props }) => {
        console.log('Add role...')
        console.log(values)
        const role = {
            name: values.name,
            default: values.default,
            permissions: values.permissions
        }
        const add_role = () => {
            UserService.add_role(role)
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
        add_role()
    }
})(AddRolePage)



export default function AddRole({ onSave }) {
    return (
        <AddRoleFormik onSave={onSave} />
    )
}