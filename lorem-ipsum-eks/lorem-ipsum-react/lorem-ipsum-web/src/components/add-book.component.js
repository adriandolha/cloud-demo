import { withFormik, Form, Field } from 'formik';
import * as Yup from 'yup';
import { useState } from 'react';
import BookView from './book-view.component';
import BookService from '../services/books.service';

const shouldGenerateAndSave = (values) => {
    return values && values.noOfBooks > 1
}
function AddBookPage(props) {
    const {
        values,
        touched,
        errors,
        setFieldValue,
        handleSubmit,
        handleReset,
        isSubmitting,
        setSubmitting,
        setStatus,
        status,
        onSave
    } = props;
    const [error, setError] = useState(false)
    // console.log(isSubmitting, status);
    if (status && status.showBook && status.data) {

        return <BookView book_data={status.data} show={status.showBook}
            handleClose={() => {
                setStatus({ showBook: false });
                setSubmitting(false);
            }}
            handleSave={() => {
                console.log('save book');
                setSubmitting(false);
                setStatus({ showBook: false });
                onSave();
            }}></BookView>
    }
    const showProgressBar = (status && status.progress) && shouldGenerateAndSave(values);
    let crtProgressValue = 0, percentage = 0;
    if (showProgressBar) {
        crtProgressValue = (status && status.progress && status.progress.filter(x => x == true).length) || 1;
        console.log('Status update:')
        status && status.progress && status.progress.forEach((item, i) => console.log(item, i))

        if (crtProgressValue == values.noOfBooks) {
            setStatus({ progress: null });
            setSubmitting(false);
            onSave();
        }
        percentage = showProgressBar && crtProgressValue * 100 / values.noOfBooks;
        status && console.log(`Progress: ${crtProgressValue} ${percentage}`);

    }
    return (
        <>
            <div className="mb-2 me-1 d-inline-flex" >
                <Form>
                    <label htmlFor="noOfPages" className="me-2 flex-column">Pages:
                        <Field type="text" name="noOfPages" />
                    </label>
                    <label htmlFor="noOfBooks" className="me-2">Books:
                        <Field type="text" name="noOfBooks" />
                    </label>
                    <button type="submit" className="btn btn-primary btn-sm ms-0 mb-3 mt-2">{shouldGenerateAndSave(values) ? "Generate & Save" : "Generate"}</button>
                    {touched.noOfPages && errors.noOfPages && <span className="ms-1 help-block text-danger">{errors.noOfPages}</span>}
                    {touched.noOfBooks && errors.noOfBooks && <span className="ms-1 help-block text-danger">{errors.noOfBooks}</span>}
                </Form>
                {error && <div className="alert alert-danger" role="alert"> {error.message} </div>}
            </div>
            <div className={showProgressBar ? "progress visible" : "invisible"}>
                <div className="progress-bar" style={{ width: percentage + "%" }}
                    role="progressbar" aria-valuenow={"" + crtProgressValue} aria-valuemin="1" aria-valuemax={"" + values.noOfBooks}></div>
            </div>
        </>
    )
}

const AddBookFormik = withFormik({

    mapPropsToValues: (props) => {
        return {
            noOfPages: props.noOfPages || '1',
            noOfBooks: props.noOfBooks || '2'
        }
    },
    validationSchema: Yup.object().shape({
        noOfPages: Yup.number().required('Number of pages is required').positive().max(10),
        noOfBooks: Yup.number().required('Number of books is required').positive().max(5),
    }),
    handleSubmit: (values, { setSubmitting, setErrors, setStatus }) => {
        console.log(values);
        console.log('Fetch random book...')
        if (shouldGenerateAndSave(values)) {
            const noOfBooks = values.noOfBooks;
            const progress = []

            for (let i = 0; i < noOfBooks; i++) {
                progress.push(false)
            }
            console.log('Initial progress:');
            progress.forEach((item, i) => console.log(item, i))
            setStatus({ progress: progress });
            for (let i = 0; i < noOfBooks; i++) {
                let index = i + 1;

                // setTimeout(function () {
                BookService.random(values.noOfPages)
                    .then(res => {
                        if (!res.ok) {
                            return res.json().then(message => { throw new Error(message); })
                        }
                        return res.json();
                    })
                    .then(data => {
                        BookService.add(data)
                            .then(res => {
                                if (!res.ok) {
                                    return res.json().then(message => { throw new Error(message); })
                                }
                                progress[i] = true;
                                setStatus({ progress: [...progress] });
                            })
                            .catch((error) => {
                                console.log(`Error saving: ${error}`);
                                setSubmitting(false);
                                setErrors({ submit: error });
                            });
                    })
                    .catch((error) => {
                        console.log(`Error generating: ${error}`);
                        setSubmitting(false);
                        setErrors({ submit: error });
                    });
                // }, index * 2000);
            }
        } else {
            BookService.random(values.noOfPages)
                .then(res => {
                    if (!res.ok) {
                        return res.json().then(message => { throw new Error(message); })
                    }
                    return res.json();
                })
                .then(data => {
                    setStatus({ data: data, showBook: true });

                })
                .catch((error) => {
                    console.log(`Error: ${error}`);
                    setSubmitting(false);
                    setErrors({ submit: error });
                });
        }
    }
})(AddBookPage)



export default function AddBook({onSave}) {
    return (
        <AddBookFormik onSave={onSave}/>
    )
}