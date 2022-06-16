import React, { useState, useEffect, useMemo } from "react";
import UserService from '../services/user.service';
import Spinner from 'react-bootstrap/Spinner';
import UsersTable from "../components/simple-table.component";
import AddUser from "./add-user.component";
import { Flash } from "../components/flash-component";
import UsersViewList from "./user-view-list.component";
import { UsersActions, UsersRole, UsersEmail } from "./user-view.component";

function UsersView() {
    const [loading, setLoading] = useState(true);
    const [data, setData] = useState();
    const [edit, setEdit] = useState({});
    const [showAddUser, setShowAddUser] = useState(false);
    const [roles, setRoles] = useState();
    const [error, setError] = useState();
    const handleAdd = () => {
        console.log(`Adding new user...`);

    }
    console.log('rendering')
    const handleSave = (user) => {
        console.log(`Saving user...`);
        const _user = user
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
    const handleDelete = (user) => {
        console.log(`Adding new user...`);
        const _user = user
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
    const UsersHeader = (props) => {
        return <h3 className="mt-0 mt-md-1 ms-4 ms-md-0">Users
            <span onClick={handleAdd}>
                <span className="badge-secondary badge ml-2" >{data.items.length}</span>
            </span>
            <span className="btn btn-sm btn-rpimary-outline" onClick={() => {
                setShowAddUser(true)
            }}><i className="fas fa-plus action"></i></span>
        </h3>
    }





    const columns = useMemo(
        () => {
            return [
                {
                    Header: () => <UsersHeader />,
                    id: 'Users',
                    columns: [
                        {
                            Header: "Username",
                            accessor: "username",
                            Cell: (props) => (
                                <div className="">{props.row.original.username}</div>
                            )

                        },
                        {
                            Header: "Email",
                            accessor: "email",
                            Cell: (props) => {
                                const row = props.row;
                                const user = row.original
                                return <UsersEmail user={user} edit={edit} setEdit={setEdit} setError={setError} />
                            }

                        },
                        {
                            Header: 'Role',
                            id: 'role',
                            accessor: "role",
                            Cell: (props) => {
                                const row = props.row;
                                return <UsersRole user={row.original} roles={roles} />
                            },
                        },
                        {
                            Header: "Actions",
                            accessor: "actions",
                            Cell: (props) => {
                                const row = props.row;
                                const user = row.original
                                return <UsersActions user={user} handleDelete={handleDelete} handleSave={handleSave} />
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
                {error && <Flash message={error.message} onExit={() => { setError(null) }} />}

                <AddUser className='row mt-4' show={showAddUser}
                    handleClose={() => { setShowAddUser(false) }}
                    onSave={() => { fetch_users() }} roles={roles}></AddUser>
                <div className="d-none d-md-block">
                    <UsersTable columns={columns} data={data.items}></UsersTable>
                </div>
                <div className="d-sm-block d-md-none" key="users-view-list">
                    <div className="row">

                        <UsersHeader />
                    </div>
                    <UsersViewList users={data.items}
                        roles={roles}
                        edit={edit}
                        setEdit={setEdit}
                        setError={setError}
                        handleSave={handleSave}
                        handleDelete={handleDelete}
                    ></UsersViewList>
                </div>
            </div>
        );
    } else {
        return <Spinner animation="border" />
    }
}

export default UsersView;