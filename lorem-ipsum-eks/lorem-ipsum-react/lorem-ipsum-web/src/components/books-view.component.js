import React, { useMemo, useState, useEffect } from "react";
import ErrorBoundary from "./error-boundary.component";
import BookActions from "./book-actions.component";
import ReactTable from "./book-table.component"
import { useFetch, useAsyncError } from "./hooks";
import Spinner from 'react-bootstrap/Spinner';
import BookView from './book-view.component';
import AddBook from './add-book.component';
import BookService from '../services/books.service';

const DEFAULT_PAGE_SIZE = 12
const DEFAULT_OFFSET = 1

const API_URL = "https://localhost";
function Books() {
  const [{ data, pageSize, pageIndex, deleted, view }, setTableMetadata] = useState({})
  const _pageSize = pageSize || DEFAULT_PAGE_SIZE;
  const _pageIndex = pageIndex || DEFAULT_OFFSET;
  const offset = Math.ceil(_pageSize * (_pageIndex - 1))
  const pagination = useMemo(() => [_pageIndex, _pageSize, deleted], [_pageIndex, _pageSize, deleted])
  const tableMetadata = { data: data, pageSize: _pageSize, pageIndex: _pageIndex, deleted: deleted, view: view };

  const columns = useMemo(
    () => {
      console.log('Columns update', data);
      return [
        {
          Header: "Books",
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
                const row = props.row;
                return (
                  <BookActions row={row} tm={tableMetadata} setDeleted={(id) => {
                    setTableMetadata({ ...tableMetadata, deleted: id })
                  }} setView={(id) => {
                    console.log(`View ${id}`);
                    setTableMetadata({ ...tableMetadata, view: id })
                  }}></BookActions>
                );
              },
            }
          ]
        }
      ]
    },
    [_pageSize, _pageIndex, deleted, view, data]
  );

  console.log('Rendering books page.')
  console.log(tableMetadata)

  const { loading, _data, error } = useFetch(
    `${API_URL}/books?limit=${_pageSize}&offset=${offset}`, 'get', null, null, (data) => {
      setTableMetadata({
        ...tableMetadata,
        data: data,

      })
    },
    [_pageSize, _pageIndex, deleted]
  );
  console.log(`Loading is ${loading}`)
  if (data && !loading) {
    const items = data.items;
    const totalCount = data.total;
    const showBook = () => {
      const handleClose = () => { setTableMetadata({ ...tableMetadata, view: null }) }
      const book_data = data.items.filter(item => item.id == view)[0]
      view && console.log(`View book ${view}`, book_data);
      view && items.map(item => console.log(item.id))
      return view && <BookView book_data={book_data} show={view ? "true" : "false"} handleClose={handleClose}></BookView>
    }

    const handleSearch = (event) => {
      const query = event.target.value
      BookService.search(query)
        .then(res => res.json())
        .then(new_data => {
          console.log('new data', new_data);
          setTableMetadata({ ...tableMetadata, data: new_data, pageIndex: 1 })
        })
        .catch((error) => {
          console.log(`Error: ${error}`);
          // setError(error);

        });
    }
    return (
      <React.Fragment>
        <AddBook onSave={() => {
          console.log('saveing...');
          BookService.get_all(_pageIndex, offset)
            .then(res => res.json())
            .then(new_data => {
              console.log('new data', new_data);
              const lastPageIndex = Math.ceil(new_data.total / tableMetadata.pageSize)
              setTableMetadata({ ...tableMetadata, data: new_data, pageIndex: lastPageIndex })
            })
            .catch((error) => {
              console.log(`Error: ${error}`);
              // setError(error);

            });
        }}></AddBook>

        {showBook()}
        <input id="search" type="text" onChange={handleSearch} className="me-1" /><i className="fas fa-search"></i>

        <ReactTable columns={columns} data={items} totalCount={totalCount} tableMetadataState={[tableMetadata, setTableMetadata]}>
        </ReactTable>
      </React.Fragment>
    );
  }
  if (loading || deleted) {
    return <Spinner animation="border" />
  }
}

export default function BooksView() {
  return (
    <ErrorBoundary>
      <div className="alert alert-danger alert-dismissible fade show invisible fixed-bottom" role="alert">
        <strong>Holy guacamole!</strong> You should check in on some of those fields below.
        <button type="button" className="close" data-dismiss="alert" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <Books />
    </ErrorBoundary>
  )
}