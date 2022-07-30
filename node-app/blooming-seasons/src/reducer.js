import { combineReducers } from "redux"
import reduceTodos from './features/todos'
import reduceFilters from './features/filters'

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

const rootReducer = combineReducers({
    todos: reduceTodos, filtrers: reduceFilters
})

export default rootReducer
