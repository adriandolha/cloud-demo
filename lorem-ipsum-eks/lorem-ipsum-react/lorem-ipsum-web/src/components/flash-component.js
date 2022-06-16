
import React, { useEffect, useState } from 'react';


export const Flash = ({ message, onExit, cls="danger"}) => {

    let [visibility, setVisibility] = useState(true);
    useEffect(() => {
        const timer = setTimeout(() => {
            setVisibility(false)
            onExit()
        }, 2000);
        return () => clearTimeout(timer);
    }, []);

    return visibility && <span className={`fixed-bottom alert alert-${cls} text-center`}> {message} </span>
    
}