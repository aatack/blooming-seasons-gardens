const initialState = [
    { id: 0, text: 'Learn React', completed: true },
    { id: 1, text: 'Learn Redux', completed: false, colour: 'red' },
    { id: 2, text: 'Build something fun!', completed: false, colour: 'blue' }
]

function nextTodoId(todos) {
    const maxId = todos.reduce((maxId, todo) => Math.max(todo.id, maxId), -1)
    return maxId + 1
}

export default function reduceTodos(state = initialState, action) {
    switch (action.type) {
        case 'todos/added': {
            return [
                ...state,
                {
                    id: nextTodoId(state),
                    text: action.payload,
                    completed: false
                }
            ]
        }
        case 'todos/toggled': {
            return state.map(todo => {
                if (todo.id !== action.payload) {
                    return todo
                }

                return {
                    ...todo,
                    completed: !todo.completed
                }
            })
        }
        case "todos/colourChanged": {
            return state.map(todo => {
                if (todo.id !== action.payload.id) {
                    return todo
                }

                return {
                    ...todo,
                    colour: action.payload.colour
                }
            })
        }
        default:
            return state
    }
}