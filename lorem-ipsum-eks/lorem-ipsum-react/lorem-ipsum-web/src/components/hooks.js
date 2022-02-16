import React, { useState, useEffect, useCallback, useRef } from "react";
import authHeader from '../services/auth-header';

const useAsyncError = () => {
  const [_, setError] = useState();
  return useCallback(
    e => {
      setError(() => {
        throw e;
      });
    },
    [setError],
  );
};

function useFetch(uri, method, body, auth_header, setData, condition) {
  let _auth_header = auth_header ? auth_header : authHeader();
  let _method = method || 'get'
  const basic_headers = {
    'Content-Type': 'application/json'
  }
  let _settings = {
    method: _method,
  }
  if (body) _settings.body = JSON.stringify(body)

  if (_auth_header && Object.keys(_auth_header).length != 0) {
    _settings.headers = new Headers({ ..._auth_header, ...basic_headers })
  } else {
    _settings.headers = new Headers(basic_headers)

  }
  // console.log( _settings.headers.values() );
  const [loading, setLoading] = useState(true);
  const [d, setD] = useState(true);
  const [error, setError] = useState(true);
  const throwError = useAsyncError();
  const mounted = useMountedRef();

  useEffect(() => {
    if (!uri) return;
    if (!mounted.current) return;
    console.log(`Fetching ${uri}...`);

    fetch(uri, _settings)
      .then(data => {
        if (!mounted.current) throwError(new Error("component is not mounted"));
        console.log(`Fetching ${uri} complete.`);
        return data.json();

      })
      .then(setData)
      .then(() => setLoading(false))
      .catch((error) => {
        console.log(error);
        if (!mounted.current) return;

        setError(error);
        throwError(new Error(error))
      })
  }, condition);

  return {
    loading,
    d,
    error
  };
}

function useMountedRef() {
  const mounted = useRef(false);
  useEffect(() => {
    mounted.current = true;
    return () => (mounted.current = false);
  });
  return mounted;
}

export { useFetch, useAsyncError, useMountedRef };