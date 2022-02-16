import React from "react";
import { useTable, usePagination } from "react-table";
import Table from 'react-bootstrap/Table';
export default function ReactTable({ columns, data, tableMetadataState }) {
  // Use the useTable Hook to send the columns and data to build the table
  const [tableMetadata, setTableMetadata] = tableMetadataState;
  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    prepareRow,
    page, // Instead of using 'rows', we'll use page,
    // which has only the rows for the active page

    // The rest of these things are super handy, too ;)
    pageCount,
    pageSize,
    pageIndex,
    gotoPage,
    nextPage,
    previousPage,
  } = useTable(
    {
      columns,
      data,
      // initialState: { pageIndex: 1 },
      manualPagination: true, // Tell the usePagination
      // hook that we'll handle our own data fetching
      // This means we'll also have to provide our own
      // pageCount.
      pageSize: tableMetadata.pageSize,
      pageIndex: tableMetadata.pageIndex,
      pageCount: Math.ceil(tableMetadata.totalCount / tableMetadata.pageSize),
    },
    usePagination
  )
  /* 
    Render the UI for your table
    - react-table doesn't have UI, it's headless. We just need to put the react-table props from the Hooks, and it will do its magic automatically
  */
  const canPreviousPage = pageIndex > 1
  const canNextPage = pageIndex < pageCount

  return (
    <>
      <pre>
        <code>
          {JSON.stringify(
            {
              pageIndex,
              pageSize,
              pageCount,
              canNextPage,
              canPreviousPage,
            },
            null,
            2
          )}
        </code>
      </pre>
      <Table {...getTableProps()} className="col-md-10" striped bordered hover>
        <thead>
          {headerGroups.map(headerGroup => (
            <tr {...headerGroup.getHeaderGroupProps()}>
              {headerGroup.headers.map(column => (
                <th {...column.getHeaderProps()}>{column.render('Header')}</th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody {...getTableBodyProps()}>
          {page.map((row, i) => {
            prepareRow(row)
            return (
              <tr {...row.getRowProps()}>
                {row.cells.map(cell => {
                  return <td {...cell.getCellProps()}>{cell.render('Cell')}</td>
                })}
              </tr>
            )
          })}
        </tbody>
      </Table>
      {/* 
          Pagination can be built however you'd like. 
          This is just a very basic UI implementation:
        */}
      <div className="pagination">
        <button onClick={() => setTableMetadata({ ...tableMetadata, ...{ pageIndex: 1 } })} disabled={!canPreviousPage}>
          {'<<'}
        </button>{' '}
        <button onClick={() => setTableMetadata({ ...tableMetadata, ...{ pageIndex: pageIndex -1 } })} disabled={!canPreviousPage}>
          {'<'}
        </button>{' '}
        <button onClick={() => setTableMetadata({ ...tableMetadata, ...{ pageIndex: pageIndex + 1 } })} disabled={!canNextPage}>
          {'>'}
        </button>{' '}
        <button onClick={() => {
          console.log('go to last page');
          setTableMetadata({ ...tableMetadata, ...{ pageIndex: pageCount } })

        }} disabled={!canNextPage}>
          {'>>'}
        </button>{' '}
        <span>
          Page{' '}
          <strong>
            {pageIndex} of {pageCount}
          </strong>{' '}
        </span>
        <span>
          | Go to page:{' '}
          <input
            type="number"
            defaultValue={pageIndex + 1}
            onChange={e => {
              console.log('go to page');
              const page = e.target.value ? Number(e.target.value) : 0
              e.target.value && setTableMetadata({ ...tableMetadata, ...{ pageIndex: page } })
            }}
            style={{ width: '100px' }}
          />
        </span>{' '}
        <select
          value={pageSize}
          onChange={e => {
            console.log('page size change');
            setTableMetadata({ ...tableMetadata, ...{ pageSize: Number(e.target.value) } })
            // setPageSize(Number(e.target.value))
          }}
        >
          {[10, 20, 30, 40, 50].map(pageSize => (
            <option key={pageSize} value={pageSize}>
              Show {pageSize}
            </option>
          ))}
        </select>
      </div>
    </>
  )
}