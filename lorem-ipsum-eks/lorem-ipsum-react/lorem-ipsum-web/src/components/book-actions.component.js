import authHeader from '../services/auth-header';
import React, { useState } from "react";

const API_URL = "https://localhost";

function BookActions({ row, tm, setDeleted, setView }) {
    const id = row.original.id;
    const uri = `${API_URL}/books/${id}`;
    const [loading, setLoading] = useState(false);
    const [data, setData] = useState();
    // console.log(`Actions table metadata is ${tableMetadata}`)
    const handleDelete = () => {
        console.log(id);
        console.log(`Fetching ${uri}...`);
        setLoading(true)
        fetch(uri, {
            method: 'delete', headers: new Headers({ ...authHeader() })
        })
            .then(data => {
                console.log(`Fetching ${uri} complete.`);
                return true;

            })
            .then(() => setDeleted(id))
            .then(() => setLoading(false))
            .catch((error) => {
                console.log(error);
                setLoading(false);
            })
    }

    const handleView = () => {
        console.log(id);
        setView(id);
    }

    return (
        <div>
            <span onClick={handleView} className="m-2">
                <i className="far fa-eye action"></i>
            </span>
            <span onClick={handleDelete}>
                <i className="fas fa-trash action"></i>
            </span>
            <span className={loading ? "visible" : "invisible"}>
                <i className="fas fa-spinner action fa-spin"></i>
            </span>
        </div>
    );

}

export default BookActions;