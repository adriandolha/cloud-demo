import React, { useState, useEffect, useMemo } from "react";
import UserService from '../services/user.service';
import Spinner from 'react-bootstrap/Spinner';
import SimpleTable from "../components/simple-table.component";
import AddRole from "./add-role.component";
import { Flash } from "../components/flash-component";
function RolesView() {
    const [loading, setLoading] = useState(true);
    const [data, setData] = useState();
    const [error, setError] = useState();
    const [message, setMessage] = useState();
    const [edit, setEdit] = useState({});

    const handleSave = (row) => {
        console.log(`Saving role...`);
        console.log(row.original)
        UserService.update_role(row.original)
            .then(res => {
                if (!res.ok) {
                    return res.json().then(message => { throw new Error(message); })
                }
                return res.json();
            })
            .then(res => {
                setMessage('Saved.')
                fetch_roles()
            })
            // .then(() => setLoading(false))
            .catch((error) => {
                console.log(`Error: ${error}`);
                setError(error);
            });


    }
    const handleDelete = (row) => {
        console.log('Delete role.')
        UserService.delete_role(row.original)
            .then(res => {
                if (!res.ok) {
                    return res.json().then(message => { setLoading(false); throw new Error(message); });
                }
                return res;
            })
            .then(() => fetch_roles())
            .catch((error) => {
                console.log(`Error: ${error}`);
                setError(error);
            });
    }

    const handleDeletePermission = (row, perm) => {
        console.log(`Remove role permission...`);
        console.log(perm);
        console.log(row);
        const new_permissions = row.original.permissions.filter(p => p.name != perm.name)
        if (new_permissions.length == 0) {
            setError(Error('At least one permission required.'))
        } else {
            row.original.permissions = new_permissions
            setEdit({ [row.id]: { 'permissions': new_permissions } })
        }
    }
    const fetch_roles = () => {
        UserService.get_roles()
            .then(res => {
                if (!res.ok) {
                    return res.json().then(message => { setLoading(false); throw new Error(message); });
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
    const [perms, setPerms] = useState()
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
            })
            .catch((error) => {
                console.log(`Error: ${error}`);
                setError(error);
            });
    }

    useEffect(() => {
        fetch_roles()
        fetch_permissions();
    }, []);
    const columns = useMemo(
        () => {
            return [
                {
                    Header: () => (
                        <h3 className="mt-1">Roles<span>
                            <span className="badge-secondary badge ml-2" >{data.items.length}</span>
                        </span>
                            {error && <span className="ms-1 help-block fs-5 text-danger">{error.message}</span>}
                            {message && <span className="ms-1 help-block fs-5 text-success">{message}</span>}

                        </h3>
                    ),
                    id: 'Roles',
                    columns: [
                        {
                            Header: "Name",
                            accessor: "name"
                        },
                        {
                            Header: 'Permissions',
                            id: 'permissions',
                            accessor: "permissions",
                            Cell: (props) => {
                                const row = props.row;
                                return (
                                    <span>
                                        {props.row.original.permissions.map(perm => (
                                            <span className="btn btn-sm btn-primary text-light ml-1 pl-1 pt-1 pb-1">
                                                <i className="fas fa-key action pe-1"></i> {perm.name}
                                                <button className="btn btn-sm btn-rpimary-outline" onClick={() => { handleDeletePermission(row, perm) }}><i className="fas fa-trash action"></i></button>
                                            </span>
                                        ))}
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
                                        <span>
                                            <select onChange={(e) => {
                                                console.log(e.target.value)
                                                setEdit({ ...edit, 'selectedPermissions': { [row.id]: e.target.value } })
                                            }} className="custom-select mr-sm-2" id="inlineFormCustomSelect">

                                                {perms && perms.items.map(perm => {
                                                    const selectedPermission = edit && edit.selectedPermissions && edit.selectedPermissions[row.id]
                                                    if (perm.name == selectedPermission) {
                                                        return (
                                                            <option selected value={perm.name} key={perm.name}>{perm.name}</option>
                                                        )
                                                    }
                                                    return (
                                                        <option value={perm.name} key={perm.name}>{perm.name}</option>
                                                    )
                                                })}
                                            </select>
                                            <span className="btn btn-sm btn-rpimary-outline" onClick={() => {
                                                var selectedPermission = edit && edit.selectedPermissions && edit.selectedPermissions[row.id]
                                                if (!selectedPermission) {
                                                    selectedPermission = perms.items[0].name
                                                }
                                                const existing_permissions = row.original.permissions.filter(val => val.name == selectedPermission)
                                                if (existing_permissions.length > 0) {
                                                    console.log(`Found ${existing_permissions[0].name}`)
                                                } else {
                                                    console.log(`New permission ${selectedPermission}`)
                                                    const new_permissions = [
                                                        ...row.original.permissions,
                                                        { 'id': selectedPermission, 'name': selectedPermission }
                                                    ]
                                                    row.original.permissions = new_permissions
                                                    console.log(new_permissions)

                                                    setEdit({ [row.id]: { 'permissions': new_permissions } })
                                                }
                                            }}><i className="fas fa-plus action"></i></span>

                                        </span>
                                        <span className="me-2" onClick={() => { handleSave(row) }}>
                                            <i className="fas fa-save action"></i>
                                        </span>

                                        <button className="btn btn-rpimary-outline" onClick={() => { handleDelete(row) }}><i className="fas fa-trash action"></i></button>
                                    </>
                                );
                            },
                        }
                    ]
                }
            ]
        },
        [data, edit, error]
    );
    if (loading) {
        return <Spinner animation="border" />
    }

    if (data && !loading) {
        return (
            <div className='mt-4'>
                <AddRole onSave={() => { fetch_roles() }}></AddRole>

                <SimpleTable columns={columns} data={data.items}></SimpleTable>
            </div>
        );
    }
}

export default RolesView;