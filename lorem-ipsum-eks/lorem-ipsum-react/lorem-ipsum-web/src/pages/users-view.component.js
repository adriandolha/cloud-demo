import React, { useState, useEffect, useMemo } from "react";
import UserService from '../services/user.service';
import Spinner from 'react-bootstrap/Spinner';
import UsersTable from "../components/simple-table.component";
import AddUser from "./add-user.component";
import * as Yup from 'yup';

function UsersView() {
    const [loading, setLoading] = useState(true);
    const [data, setData] = useState();
    const [edit, setEdit] = useState({});
    const [roles, setRoles] = useState();
    const [error, setError] = useState();
    const handleAdd = () => {
        console.log(`Adding new user...`);

    }
    console.log('rendering')
    const handleSave = (row) => {
        console.log(`Saving user...`);
        const _user = row.original
        console.log(_user);
        UserService.update_user(_user)
            .then(res => {
                if (!res.ok) {
                    return res.json().then(message => { throw new Error(message); })
                }
                return res.json();
            })
            .then(res => fetch_users())
            // .then(() => setLoading(false))
            .catch((error) => {
                console.log(`Error: ${error}`);
                setError(error);
            });
    }
    const handleDelete = (row) => {
        console.log(`Adding new user...`);
        const _user = row.original
        console.log(_user);
        UserService.delete_user(_user.username)
            .then(res => {
                if (!res.ok) {
                    return res.json().then(message => { throw new Error(message); })
                }
                return res;
            })
            .then(res => fetch_users())
            // .then(() => setLoading(false))
            .catch((error) => {
                console.log(`Error: ${error}`);
                setError(error);
            });

    }
    const fetch_users = () => {
        UserService.get_all()
            .then(res => {
                if (!res.ok) {
                    return res.json().then(message => { setLoading(false); throw new Error(message); })
                }
                return res.json();
            })
            .then(setData)
            .then(() => setLoading(false))
            .catch((error) => {
                console.log(`Error: ${error}`);
                setError(error);
            });
    }
    const fetch_roles = () => {
        UserService.get_roles()
            .then(res => {
                if (!res.ok) {
                    return res.json().then(message => { setLoading(false); throw new Error(message); })
                }
                return res.json();
            })
            .then(setRoles)
            .then(() => setLoading(false))
            .catch((error) => {
                console.log(`Error: ${error}`);
                setError(error);
            });
    }
    useEffect(() => {
        fetch_users()
        fetch_roles()
    }, []);
    const columns = useMemo(
        () => {
            return [
                {
                    Header: () => (
                        <h3 className="mt-1">Users
                            <span onClick={handleAdd}>
                                <span className="badge-secondary badge ml-2" >{data.items.length}</span>
                            </span>
                            {error && <span className="ms-1 help-block fs-5 text-danger">{error.message}</span>}
                        </h3>
                    ),
                    id: 'Users',
                    columns: [
                        {
                            Header: "username",
                            accessor: "username"
                        },
                        {
                            Header: "email",
                            accessor: "email",
                            Cell: (props) => {
                                const row = props.row;
                                const row_id = row.id
                                const handleEmailChanged = (e) => {

                                    if (e.key === 'Enter') {
                                        const _email = e.target.value
                                        console.log('entered');
                                        console.log(_email)
                                        const is_valid = Yup.string().email('Invalid email format').required('Email is required').isValidSync(_email)
                                        if (!is_valid){
                                            setError(Error('Invalid email'))    
                                        } else{
                                            row.original.email = _email
                                            setEdit({})
                                            setError(null)
                                        }
                                    }
                                }

                                if (edit && edit[row_id]) {
                                    console.log('Editable email')
                                    console.log(row_id)
                                    console.log(edit[row_id])
                                    console.log(edit)
                                    return (
                                        <input type="text" id={`${row_id}-email`} placeholder={row.original.email} onKeyDown={handleEmailChanged}></input>
                                    )
                                }
                                return (
                                    <span onClick={(e) => {
                                        console.log(`Editing email ${row.original.email}`)
                                        console.log(e.target.value)
                                        const newEdit = {
                                            ...edit,
                                            [row_id]: { email: row.original.email }
                                        };
                                        setEdit(newEdit)
                                        console.log(newEdit)

                                    }
                                    } className="text-primary" >
                                        {props.row.values.email}
                                    </span >
                                );
                            },
                        },
                        {
                            Header: 'role',
                            id: 'role',
                            accessor: "role",
                            Cell: (props) => {
                                const row = props.row;
                                const _original_role = row.original.role
                                return (
                                    <span className="text-success">
                                        <select onChange={(e) => {
                                            const _role = e.target.value
                                            const [existing_role] = roles.items.filter(role => role.name == _role)
                                            if (existing_role) {
                                                row.original.role = existing_role
                                            }
                                        }} className="custom-select-sm text-success mr-sm-2" id="inlineFormCustomSelect">
                                            {roles && roles.items.map(role => {
                                                const is_selected = role.name == _original_role.name
                                                if (is_selected) {
                                                    return (
                                                        <option selected value={role.name} key={role.name}>{role.name}</option>
                                                    )
                                                } else {
                                                    return (
                                                        <option value={role.name} key={role.name}>{role.name}</option>
                                                    )
                                                }
                                            })
                                            }
                                        </select>
                                    </span>
                                );
                            },
                        },
                        {
                            Header: "Actions",
                            accessor: "actions",
                            Cell: (props) => {
                                const row = props.row;
                                return (
                                    <>
                                        <span className="me-2" onClick={() => { handleSave(row) }}>
                                            <i className="fas fa-save action"></i>
                                        </span>
                                        <span onClick={() => { handleDelete(row) }}>
                                            <i className="fas fa-trash action"></i>
                                        </span>
                                    </>
                                );
                            },
                        }
                    ]
                }
            ]
        },
        [data, roles, error, edit]
    );

    if (roles && data && !loading) {
        return (
            <div className='row mt-4'>
                <AddUser className='row mt-4' onSave={() => { fetch_users() }}></AddUser>
                <UsersTable className='row mt-4' columns={columns} data={data.items}></UsersTable>
            </div>
        );
    } else {
        return <Spinner animation="border" />
    }
}

export default UsersView;