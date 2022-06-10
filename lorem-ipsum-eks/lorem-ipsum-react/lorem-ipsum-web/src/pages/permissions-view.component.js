import React, { useState, useEffect, useMemo } from "react";
import UserService from '../services/user.service';
import Spinner from 'react-bootstrap/Spinner';
import SimpleTable from "../components/simple-table.component";
import AddPermission from "./add-permission.component";
function PermissionsView() {
    const [loading, setLoading] = useState(true);
    const [data, setData] = useState();
    const [error, setError] = useState();

    const fetch_permissions = () => {
        UserService.get_permissions()
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

    useEffect(() => {
        fetch_permissions();
    }, []);
    const handleDelete = (row) => {
        console.log('Delete permission.')
        UserService.delete_permission(row.original.name)
            .then(res => {
                if (!res.ok) {
                    return res.json().then(message => { setLoading(false); throw new Error(message); });
                }
                return res;
            })
            .then(() => fetch_permissions())
            .catch((error) => {
                console.log(`Error: ${error}`);
                setError(error);
            });
    }
    const columns = useMemo(
        () => {
            return [
                {
                    Header: () => (
                        <h3 className="mt-1">Permissions<span><span className="badge-secondary badge ml-2" >{data.items.length}</span></span></h3>
                    ),
                    id: 'Permissions',
                    columns: [

                        {
                            Header: "Name",
                            accessor: "name",
                            Cell: (props) => {
                                const row = props.row;
                                return (
                                    <span className="btn btn-primary text-light pl-1 pt-1 pb-1">
                                        <i className="fas fa-key action pe-1"></i> {props.row.values.name}
                                        <button className="btn btn-rpimary-outline" onClick={() => { handleDelete(row) }}><i className="fas fa-trash action"></i></button>
                                    </span>
                                );
                            },
                        }
                    ]
                }
            ]
        },
        [data]
    );
    if (loading) {
        return <Spinner animation="border" />
    }

    if (data && !loading) {
        return (
            <div className='mt-4'>
                <AddPermission onSave={() => { fetch_permissions() }}></AddPermission>
                <SimpleTable columns={columns} data={data.items}></SimpleTable>
            </div>
        );
    }
}

export default PermissionsView;
