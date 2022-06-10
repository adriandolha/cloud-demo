
import React, { useEffect, useState } from 'react';

export const Flash = ({message}) => {
  
    let [visibility, setVisibility] = useState(true);


    return (
        visibility && <span className={`alert alert-success text-sm`}>
                {message}
                <span className="close"><strong>X</strong></span>
            </span>
    )
}