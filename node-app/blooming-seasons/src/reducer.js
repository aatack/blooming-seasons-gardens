const initialState = {
    todos: [
        { id: 0, text: 'Learn React', completed: true },
        { id: 1, text: 'Learn Redux', completed: false, color: 'purple' },
        { id: 2, text: 'Build something fun!', completed: false, color: 'blue' }
    ],
    filters: {
        status: 'All',
        colors: []
    }
}

export default function appReducer(state = initialState, action) {
    switch (action.type) {
        case "todos/added": {
            return wrapTodo(added)(state, action)
        }
        case "todos/toggled": {
            return wrapTodo(toggled)(state, action)
        }
        case "filters/statusChanged": {
            return wrapFilter(statusChanged)
        }
        default:
            return state
    }
}
