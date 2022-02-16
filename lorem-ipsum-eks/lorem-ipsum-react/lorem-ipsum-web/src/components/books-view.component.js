import React, { useMemo, useState, useEffect } from "react";
import ErrorBoundary from "./error-boundary.component";
import BookActions from "./book-actions.component";
import ReactTable from "./book-table.component"
import { useFetch, useAsyncError } from "./hooks";
import Spinner from 'react-bootstrap/Spinner';

const DEFAULT_PAGE_SIZE = 10
const DEFAULT_OFFSET = 1

const API_URL = "https://localhost";
function Books() {
  const [{ data, totalCount, pageSize, pageIndex, deleted }, setTableMetadata] = useState({})
  const _pageSize = pageSize || DEFAULT_PAGE_SIZE;
  const _pageIndex = pageIndex || DEFAULT_OFFSET;
  const offset = Math.ceil(_pageSize * (_pageIndex - 1))
  const pagination = useMemo(() => [_pageIndex, _pageSize, deleted], [_pageIndex, _pageSize, deleted])

  const columns = useMemo(
    () => [
      {
        Header: "Books",
        // First group columns
        columns: [
          {
            Header: "id",
            accessor: "id"
          },
          {
            Header: "title",
            accessor: "title"
          },
          {
            Header: "Author",
            accessor: "author"
          },
          {
            Header: "Actions",
            accessor: "actions",
            Cell: (props) => {
              // console.log(props);
              const row = props.row;
              return (
                <BookActions row={row} tableMetadata={data, pageSize, pageIndex, deleted} setDeleted={(id, tableMetadata) => {
                  console.log(tableMetadata);
                  setTableMetadata({ ...tableMetadata, ...{ deleted: id } })
                }}></BookActions>
              );
            },
          }
        ]
      }
    ],
    [pageSize, pageIndex, deleted]
  );

  console.log('Rendering books page.')
  console.log({ data, totalCount, pageSize, pageIndex, deleted })
  console.log(pagination)

  const { loading, _data, error } = useFetch(
    `${API_URL}/books?limit=${_pageSize}&offset=${offset}`, 'get', null, null, (data) => {
      setTableMetadata({
        data: data.items,
        totalCount: data.total,
        pageSize: _pageSize,
        pageIndex: _pageIndex
      })
    },
    [_pageSize, _pageIndex, deleted]
  );
  console.log(`Loading is ${loading}`)
  if (data && !loading) {
    return (
      <ReactTable columns={columns} data={data} tableMetadataState={[{ data, totalCount, pageSize, pageIndex }, setTableMetadata]}>
      </ReactTable>
    );
  }
  if (loading || deleted) {
    return <Spinner animation="border" />
  }
}

export default function BooksView() {
  return (
    <ErrorBoundary>
      <div className="alert alert-danger alert-dismissible fade show invisible fixed-top" role="alert">
        <strong>Holy guacamole!</strong> You should check in on some of those fields below.
        <button type="button" className="close" data-dismiss="alert" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <Books />
    </ErrorBoundary>
  )
}