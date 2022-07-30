function nextTodoId(todos) {
    const maxId = todos.reduce((maxId, todo) => Math.max(todo.id, maxId), -1)
    return maxId + 1
}

function wrapTodo(todoReducer) {
    return (state, action) => {
        return { ...state, todos: todoReducer(state.todos, action.payload) }
    }
}

function added(state, payload) {
    return [
        ...state,
        { id: nextTodoId(state), text: payload, completed: false }
    ]
}

function toggled(state, payload) {
    return state.todos.map(todo => {
        if (todo.id !== payload) {
            return todo
        } else {
            return { ...todo, completed: !todo.completed }
        }
    })
}
