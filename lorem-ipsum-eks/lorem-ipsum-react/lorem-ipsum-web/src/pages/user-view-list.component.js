import { UserView } from './user-view.component';

function UsersViewList({ users, roles, edit, setEdit, setError, handleSave, handleDelete }) {
    return (
        <div className=' users-view-list'>
            {users.map(user => {
                return <div className='col-sm-12' key={user.username}>
                    <UserView user={user}
                        roles={roles}
                        edit={edit}
                        setEdit={setEdit}
                        setError={setError}
                        handleSave={handleSave}
                        handleDelete={handleDelete} />
                </div>
            })}

        </div>
    )
}

export default UsersViewList